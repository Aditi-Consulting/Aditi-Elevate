"""Native Copilot reviews and GitHub notifications. No model key or mail service."""
import argparse
import hashlib
import json
import os
import re

try:
    from .review import GitHub, inspect_paths
except ImportError:
    from review import GitHub, inspect_paths

COPILOT = {'copilot', 'copilot-pull-request-reviewer[bot]'}
MARKER = '<!-- elevate-copilot-status -->'


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
                and all(c['result'] == 'pass' and c['requirement'].strip() and c['evidence'].strip()
                        for c in report['criteria']))


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


def process(api, number, actor, coordinator, request_reviews=False, dry_run=False):
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
    tree = api.get(f'git/trees/{sha}?recursive=1')
    if tree.get('truncated'):
        raise RuntimeError('Incomplete repository tree')
    paths = {f['path'] for f in tree['tree'] if f['type'] == 'blob' and f['mode'] != '120000' and f.get('size', 0)}
    for root in roots:
        if root + '/README.md' not in paths:
            issues.append('Include a nonempty assessment README.md with setup, execution, and results.')
    reviews = api.pages(f'pulls/{number}/reviews')
    current = [r for r in reviews if is_copilot(r) and r['commit_id'] == sha and r['state'] != 'PENDING']
    review = max(current, key=lambda r: r['id'], default=None)
    report = parse_report(review['body']) if review else None
    source_body = ''
    if report and report['question_status'] == 'found' and report['source_pr'] > 0:
        source_body = api.get(f'pulls/{report["source_pr"]}')['body'] or ''
    ready = bool(review and review['state'] == 'APPROVED' and report_passes(report, source_body)
                 and not issues and not has_objections(reviews)
                 and not api.unresolved(number) and checks_pass(api, sha))
    body = MARKER + f'\n## Aditi Elevate review status\n\nRevision: `{sha}`\n\n'
    if ready:
        body += '**Approved by Copilot; grading report and handoff checks passed.**\n'
    elif review:
        body += '**Not cleared for the next stage.** Copilot has reviewed this revision. '
        body += 'Clearance requires an approving review, a complete passing assessment rubric, successful checks, and resolved feedback.\n'
    else:
        body += '**Pending Copilot review. No assessment approval has been issued.**\n'
    if review:
        body += f'\n[Read the Copilot review and feedback]({review["html_url"]}).\n'
        if not report:
            body += '\nThe structured assessment rubric is missing; a general code review alone does not establish a passing grade.\n'
    if report and report['question_status'] in {'missing', 'ambiguous'}:
        body += '\nThe assignment question is missing or ambiguous. Add the full question or link the exact same assessment in another PR.\n'
    if issues:
        body += '\n### Submission updates needed\n' + '\n'.join('- ' + s for s in issues) + '\n'
    body += '\nThis assistant inspects submission structure and review metadata; it does not run participant code. New commits or changed requirements invalidate clearance.\n'
    comments = api.pages(f'issues/{number}/comments')
    trusted = [c for c in comments if c['user']['login'] in {actor, 'github-actions[bot]'}]
    if dry_run:
        print(json.dumps({'pr': number, 'sha': sha, 'copilot_review': review['state'] if review else None,
                          'ready': ready, 'structure_feedback': issues}))
        return
    fresh = api.get(f'pulls/{number}')
    if fresh['head']['sha'] != sha or fresh['body'] != pr['body'] or fresh['draft'] or fresh['state'] != 'open':
        return
    existing = next((c for c in reversed(trusted) if c['body'].startswith(MARKER)), None)
    if not existing:
        api.request(f'/repos/{api.repo}/issues/{number}/comments', {'body': body})
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
        key = hashlib.sha256(f'{sha}:{review["id"]}:{ready}:{pr["body"]}'.encode()).hexdigest()
        marker = f'<!-- elevate-copilot-notice:{key} -->'
        if not any(c['body'].startswith(marker) for c in trusted):
            status = 'Approved for coordinator handoff' if ready else 'Review available; participant is NOT cleared'
            api.request(f'/repos/{api.repo}/issues/{number}/comments', {'body':
                f'{marker}\n@{coordinator}: **{status}** for revision `{sha}`. '
                f'[Grading/review feedback]({review["html_url"]}). Please check the latest '
                'assessment status and current revision before unblocking the next stage.'})
    print(f'PR #{number}: {"approved handoff" if ready else "pending / needs attention"}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--request-reviews', action='store_true')
    parser.add_argument('--pr', type=int)
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
            process(api, number, actor, coordinator, args.request_reviews, args.dry_run)
        except Exception as error:
            print(f'PR #{number}: {type(error).__name__}; could not finish. No new clearance should be assumed.')
            failures.append(number)
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
