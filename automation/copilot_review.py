"""Native Copilot reviews and GitHub notifications. No model key or mail service."""
import argparse
import hashlib
import json
import os
import re
from urllib.error import HTTPError
from urllib.parse import quote

try:
    from .review import GitHub, inspect_paths
except ImportError:
    from review import GitHub, inspect_paths

COPILOT = {'copilot', 'copilot-pull-request-reviewer[bot]'}
MARKER = '<!-- elevate-copilot-status -->'


def display(value):
    """Keep untrusted text from altering table structure or notifying extra people."""
    return str(value).replace('@', '@\u200b').replace('<', '&lt;').replace('>', '&gt;').replace('|', '\\|').replace('\r', '').replace('\n', '<br>')


def render_report(api, pr, roots, review, report, issues, ready, findings, merged_sha=None, merge_note=None):
    participant = pr['user']['login']
    state = 'Merged — assessment complete' if merged_sha else ('Approved — awaiting merge' if ready else 'Action required' if review or issues else 'Review pending')
    icon = '✅' if merged_sha else '🟢' if ready else '🟠' if review or issues else '⏳'
    body = MARKER + '\n## Aditi Elevate · Assessment report\n\n'
    body += f'### {icon} {state}\n\n'
    body += f'**Participant:** {participant}  \n**Submission:** {display(pr["title"])}  \n'
    body += f'**PR:** [#{pr["number"]}](https://github.com/{api.repo}/pull/{pr["number"]})\n\n'
    if merged_sha:
        body += '> **Anjali — next action:** Unblock the next learning stage. The approved submission is merged into main.\n\n'
        body += '**Participant:** assessment complete. No further fixes are requested for this submission.\n'
    elif ready:
        body += '> **Anjali — next action:** wait for the merged confirmation before unblocking the next stage.\n\n'
        body += '**Participant:** review gates passed; merge is pending.\n'
    elif review or issues:
        body += '> **Anjali — next action:** Keep this assessment pending until approval and merge are confirmed.\n\n'
        body += '**Participant:** address the required actions below. Optional improvements do not block approval.\n'
    else:
        body += '> **Anjali — next action:** Wait for the assessment review.\n\n'
        body += '**Participant:** review pending; no code changes are requested by this status report.\n'
    if merge_note:
        body += '\n**Merge status:** ' + display(merge_note) + '\n'
    required = list(issues)
    if not review:
        required.append('Wait for Copilot to review the current revision. Previous-revision reviews do not count.')
    elif not ready and not merged_sha:
        if review['state'] != 'APPROVED':
            required.append('Obtain an approving review of the current revision after addressing feedback. COMMENTED is not an approval.')
        if report:
            if report['question_status'] != 'found':
                required.append('Add the full assigned question to the PR or link the exact same assessment from another PR.')
            if report['needs_execution']:
                required.append('Supply the missing execution/validation evidence for reviewer verification.')
        required.append('Required CI checks and material review blockers must be cleared. Clearly marked advisory feedback does not require a code change; repository merge rules still apply.')
    if required:
        body += '\n### Required actions\n\n' + '\n'.join(f'{i}. {display(item)}' for i, item in enumerate(required, 1)) + '\n'
    body += '\n### Grading rubric\n\n'
    if report and report['criteria']:
        body += f'Question source: [PR #{report["source_pr"]}](https://github.com/{api.repo}/pull/{report["source_pr"]}).\n\n'
        for criterion in report['criteria']:
            result = criterion['result'].upper() if criterion.get('blocking', True) else 'ADVISORY — non-blocking'
            icon = {'PASS': '✅', 'FAIL': '❌', 'UNVERIFIED': '⏳'}.get(result, '💡')
            body += f'- {icon} **{result} — {display(criterion["requirement"])}**\n  Evidence: {display(criterion["evidence"])}\n'
    else:
        body += 'Detailed assessment evidence is available in the linked review below.\n'
    findings = [f for f in findings if not f['body'].lstrip().startswith('ADVISORY:')]
    if findings:
        body += '\n### Code review findings\n\n'
        for i, finding in enumerate(findings[:20], 1):
            body += f'{i}. [{display(finding["path"])} — review comment]({finding["html_url"]})\n\n'
            text = finding['body'][:2000]
            body += '   > ' + display(text) + (' … (read the linked comment for details)' if len(finding['body']) > 2000 else '') + '\n\n'
        if len(findings) > 20:
            body += 'Additional findings are available in the linked review.\n'
    body += '\n### Optional improvements — not required for approval\n\n'
    body += ('\n'.join('- ' + display(s) for s in report['improvements'][:2]) if report and report['improvements'] else 'None. No extra polish is required.') + '\n'
    body += '\n### Submission and review details\n\n'
    for root in sorted(roots):
        ref = merged_sha or pr['head']['sha']
        body += f'- **{"Merged folder" if merged_sha else "Submission folder"}:** [{display(root)}](https://github.com/{api.repo}/tree/{ref}/{quote(root, safe="/")})\n'
    if review:
        body += f'- **Review evidence:** [{review["state"]}]({review["html_url"]})\n'
    body += f'- **Reviewed revision:** `{pr["head"]["sha"][:12]}`\n'
    if merged_sha:
        body += f'- **Merge commit:** [{merged_sha[:12]}](https://github.com/{api.repo}/commit/{merged_sha})\n'
    body += '\n---\nValidation scope: submission paths, review evidence, CI status and merge eligibility. The bot does not execute participant code.\n'
    if len(body) > 60000:
        raise RuntimeError('Assessment report exceeds comment limit')
    return body


def merge_approved(api, pr, review, report):
    """Recheck merge gates and pin the merge to the reviewed head SHA."""
    number, sha = pr['number'], pr['head']['sha']
    fresh = api.get(f'pulls/{number}')
    if (fresh['state'] != 'open' or fresh['draft'] or fresh['base']['ref'] != 'main'
            or fresh['head']['sha'] != sha or fresh['body'] != pr['body']
            or fresh['mergeable'] is not True or fresh['mergeable_state'] != 'clean'):
        return None, 'Waiting: the revision, question, mergeability or repository merge rules changed. Refresh and re-review if needed.'
    files = api.pages(f'pulls/{number}/files')
    if len(files) != fresh['changed_files'] or inspect_paths(files, fresh['user']['login'])[0]:
        return None, 'Merge blocked: changes must belong exclusively to the participant’s correctly named assessment folder.'
    reviews = api.pages(f'pulls/{number}/reviews')
    current = [r for r in reviews if is_copilot(r) and r['commit_id'] == sha and r['state'] != 'PENDING']
    latest = max(current, key=lambda r: r['id'], default=None)
    if (not latest or latest['id'] != review['id'] or latest['state'] != 'APPROVED'
            or parse_report(latest['body']) != report or has_objections(reviews)
            or api.unresolved(number) or not checks_pass(api, sha)):
        return None, 'Merge blocked: current approval, review discussions or CI checks need attention.'
    if report:
        source = api.get(f'pulls/{report["source_pr"]}')
        if not report_passes(report, source['body'] or ''):
            return None, 'Merge blocked: a reported core requirement or assignment source could not be verified.'
    try:
        result = api.request(f'/repos/{api.repo}/pulls/{number}/merge',
                             {'sha': sha, 'merge_method': 'squash',
                              'commit_title': f'Complete assessment for {fresh["user"]["login"]} (#{number})'}, 'PUT')
    except HTTPError as error:
        if error.code not in {403, 405, 409, 422}:
            raise
        return None, f'GitHub blocked the merge (HTTP {error.code}). Check branch rules, permissions, conflicts and squash-merge settings.'
    if result.get('merged') is not True or not result.get('sha'):
        return None, 'GitHub did not confirm a successful merge. Maintainer attention is required.'
    return result['sha'], 'Squash-merged into main; the approved folder paths were preserved.'


def is_copilot(review):
    user = review['user']
    return user.get('type') == 'Bot' and user['login'].lower() in COPILOT


def parse_report(body):
    blocks = re.findall(r'```elevate-report\s*\n(.*?)\n```', body or '', re.S)
    if len(blocks) != 1:
        return None
    try:
        report = json.loads(blocks[0])
        if (report['question_status'] not in {'found', 'missing', 'ambiguous'}
                or type(report['source_pr']) is not int
                or not isinstance(report['question_quote'], str)
                or type(report['needs_execution']) is not bool
                or not isinstance(report['criteria'], list)
                or not isinstance(report['improvements'], list)
                or not all(isinstance(s, str) for s in report['improvements'])):
            return None
        for criterion in report['criteria']:
            if (criterion['result'] not in {'pass', 'fail', 'unverified'}
                    or type(criterion.get('blocking', True)) is not bool
                    or not isinstance(criterion['requirement'], str)
                    or not isinstance(criterion['evidence'], str)):
                return None
        return report
    except (ValueError, KeyError, TypeError):
        return None


def report_passes(report, source_body):
    return bool(report and report['question_status'] == 'found'
                and len(report['question_quote'].strip()) >= 20
                and report['question_quote'] in source_body
                and not report['needs_execution'] and report['criteria']
                and any(c.get('blocking', True) for c in report['criteria'])
                and all(c['result'] == 'pass' and c['requirement'].strip() and c['evidence'].strip()
                        for c in report['criteria'] if c.get('blocking', True)))


def has_objections(reviews):
    latest = {}
    for review in sorted(reviews, key=lambda r: r['id']):
        if review['state'] in {'APPROVED', 'CHANGES_REQUESTED', 'DISMISSED'}:
            latest[review['user']['login']] = review['state']
    return 'CHANGES_REQUESTED' in latest.values()


def checks_pass(api, sha):
    required = {s.strip() for s in os.environ.get('REQUIRED_CHECKS', '').split(',') if s.strip()}
    response = api.get(f'commits/{sha}/check-runs?per_page=100')
    if response['total_count'] > 100:
        return False
    latest = {}
    for check in sorted(response['check_runs'], key=lambda c: c['id']):
        if check['name'] != 'elevate-ai-review':
            latest[('check', check['name'])] = check['conclusion'] if check['status'] == 'completed' else 'pending'
    for status in reversed(api.pages(f'commits/{sha}/statuses')):
        latest[('status', status['context'])] = status['state']
    return (all(state in {'success', 'neutral', 'skipped'} for state in latest.values())
            and all(any(key[1] == name and state == 'success' for key, state in latest.items()) for name in required))


def process(api, number, actor, coordinator, request_reviews=False, dry_run=False, merge_enabled=False):
    pr = api.get(f'pulls/{number}')
    if pr['draft'] or pr['state'] != 'open' or pr['base']['ref'] != 'main':
        return
    files = api.pages(f'pulls/{number}/files')
    if not any(f['filename'].startswith('participants/') for f in files):
        return
    if len(files) != pr['changed_files']:
        raise RuntimeError('Incomplete file list')
    issues, roots = inspect_paths(files, pr['user']['login'])
    sha = pr['head']['sha']
    reviews = api.pages(f'pulls/{number}/reviews')
    current = [r for r in reviews if is_copilot(r) and r['commit_id'] == sha and r['state'] != 'PENDING']
    review = max(current, key=lambda r: r['id'], default=None)
    report = parse_report(review['body']) if review else None
    source_body = ''
    if report and report['question_status'] == 'found' and report['source_pr'] > 0:
        source_body = api.get(f'pulls/{report["source_pr"]}')['body'] or ''
    ready = bool(review and review['state'] == 'APPROVED' and (report is None or report_passes(report, source_body))
                 and not issues and not has_objections(reviews)
                 and not api.unresolved(number) and checks_pass(api, sha))
    findings = [c for c in api.pages(f'pulls/{number}/comments')
                if review and c['pull_request_review_id'] == review['id'] and is_copilot(c)]
    merged_sha, merge_note = None, None
    comments = api.pages(f'issues/{number}/comments')
    trusted = [c for c in comments if c['user']['login'] in {actor, 'github-actions[bot]'}]
    if dry_run:
        print(json.dumps({'pr': number, 'sha': sha, 'copilot_review': review['state'] if review else None,
                          'ready': ready, 'structure_feedback': issues}))
        return
    fresh = api.get(f'pulls/{number}')
    if fresh['head']['sha'] != sha or fresh['body'] != pr['body'] or fresh['draft'] or fresh['state'] != 'open':
        return
    if ready and merge_enabled:
        merged_sha, merge_note = merge_approved(api, pr, review, report)
    body = render_report(api, pr, roots, review, report, issues, ready, findings, merged_sha, merge_note)
    existing = next((c for c in reversed(trusted) if c['body'].startswith(MARKER)), None)
    if not existing:
        existing = api.request(f'/repos/{api.repo}/issues/{number}/comments', {'body': body})
    elif existing['body'] != body:
        api.request(f'/repos/{api.repo}/issues/comments/{existing["id"]}', {'body': body}, 'PATCH')
    # Requests are explicit: native Copilot rulesets should handle ongoing automatic review.
    if request_reviews and not review:
        events = api.pages(f'issues/{number}/timeline')
        requested = any(e.get('event') == 'review_requested' and
                        (e.get('requested_reviewer') or {}).get('login', '').lower() in COPILOT
                        for e in events)
        if not requested:
            api.request(f'/repos/{api.repo}/pulls/{number}/requested_reviewers',
                        {'reviewers': ['copilot-pull-request-reviewer[bot]']})
            print(f'PR #{number}: Copilot review requested')
        else:
            print(f'PR #{number}: existing Copilot request; waiting (use GitHub to re-request if needed)')
    if review:
        key = hashlib.sha256(f'{sha}:{review["id"]}:{ready}:{merged_sha}:{pr["body"]}'.encode()).hexdigest()
        marker = f'<!-- elevate-copilot-notice:{key} -->'
        if not any(c['body'].startswith(marker) for c in trusted):
            status = '✅ Assessment complete — merged' if merged_sha else '🟠 Assessment pending'
            report_url = f'https://github.com/{api.repo}/pull/{number}#issuecomment-{existing["id"]}'
            notice = (f'{marker}\n## Aditi Elevate · Assessment update\n\n'
                      f'### {status}\n\n'
                      f'**Participant:** {pr["user"]["login"]}  \n'
                      f'**Submission:** {display(pr["title"])}  \n'
                      f'**PR:** [#{number}](https://github.com/{api.repo}/pull/{number})\n\n'
                      f'@{coordinator} @{pr["user"]["login"]}\n\n')
            notice += ('> **Anjali — next action:** Unblock the next learning stage.\n\n'
                       '✅ Review gates passed  \n✅ Merged into the participant’s folder on main  \n✅ No further fixes requested for this submission\n\n'
                       if merged_sha else '> **Anjali — next action:** Keep this assessment pending until approval and merge are confirmed.\n\n'
                       '**Participant:** check the required actions in the report. Optional suggestions do not block approval.\n\n')
            notice += f'[View grading results and review details]({report_url})\n\nReviewed revision: `{sha[:12]}`.\n'
            api.request(f'/repos/{api.repo}/issues/{number}/comments', {'body': notice})
    print(f'PR #{number}: {"merged" if merged_sha else "pending / needs attention"}')



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--request-reviews', action='store_true')
    parser.add_argument('--pr', type=int)
    parser.add_argument('--merge-approved', action='store_true', help='Merge only assessments passing all review and ownership gates')
    args = parser.parse_args()
    coordinator = os.environ.get('COORDINATOR', 'AniiBee25')
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9-]{0,38}', coordinator):
        raise ValueError('Invalid GitHub coordinator username')
    actor = os.environ.get('COMMENT_ACTOR', 'github-actions[bot]')
    api = GitHub(os.environ['GITHUB_REPOSITORY'], os.environ['GH_TOKEN'])
    number = args.pr
    if not number and os.environ.get('GITHUB_EVENT_PATH'):
        with open(os.environ['GITHUB_EVENT_PATH']) as stream:
            number = json.load(stream).get('pull_request', {}).get('number')
    numbers = [number] if number else [p['number'] for p in api.pages('pulls?state=open')]
    failures = []
    for number in numbers:
        try:
            process(api, number, actor, coordinator, args.request_reviews, args.dry_run, args.merge_approved)
        except Exception as error:
            print(f'PR #{number}: {type(error).__name__}; could not finish. No new clearance should be assumed.')
            failures.append(number)
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
