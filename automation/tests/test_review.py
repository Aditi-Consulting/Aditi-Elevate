import json
import unittest
from unittest.mock import patch
from automation.review import inspect_paths, blocking_thread
from automation.copilot_review import parse_report, report_passes, has_objections, is_copilot, checks_pass

REPORT = {'question_status': 'found', 'source_pr': 4,
          'question_quote': 'Calculate the sum of transaction amounts.',
          'criteria': [{'requirement': 'Sum', 'result': 'pass', 'evidence': 'src/transaction.py: sum(values)'}],
          'needs_execution': False, 'improvements': ['Add descriptive types.']}


class Tests(unittest.TestCase):
    def test_parse_complete_report(self):
        body = 'Review\n```elevate-report\n' + json.dumps(REPORT) + '\n```'
        self.assertEqual(parse_report(body), REPORT)

    def test_malformed_reports_fail_closed(self):
        for body in ['', 'Looks good; approve!', '```elevate-report\n{}\n```',
                     '```elevate-report\n[]\n```', '```elevate-report\ninvalid\n```']:
            self.assertIsNone(parse_report(body))

    def test_all_requirements_and_evidence_required(self):
        self.assertTrue(report_passes(REPORT, REPORT['question_quote']))
        for changes in [{'criteria': []}, {'needs_execution': True}, {'question_status': 'missing'},
                        {'criteria': [{'requirement': 'Sum', 'result': 'unverified', 'evidence': 'Unknown'}]},
                        {'criteria': [{'requirement': 'Sum', 'result': 'pass', 'evidence': ''}]}]:
            self.assertFalse(report_passes(dict(REPORT, **changes), REPORT['question_quote']))

    def test_source_quote_must_exist(self):
        self.assertFalse(report_passes(REPORT, 'Another assignment entirely.'))

    def test_only_copilot_bot_reviews_trusted(self):
        self.assertTrue(is_copilot({'user': {'login': 'copilot-pull-request-reviewer[bot]', 'type': 'Bot'}}))
        self.assertFalse(is_copilot({'user': {'login': 'copilot', 'type': 'User'}}))

    def test_change_request_blocks_until_cleared(self):
        review = {'id': 1, 'user': {'login': 'teacher'}, 'state': 'CHANGES_REQUESTED'}
        self.assertTrue(has_objections([review]))
        self.assertFalse(has_objections([review, dict(review, id=2, state='APPROVED')]))

    def test_scope_and_rename(self):
        file = {'filename': 'participants/student/python/chapter-01-basics/assessment-01-test/main.py', 'status': 'added'}
        self.assertEqual(inspect_paths([file], 'student')[0], [])
        self.assertTrue(inspect_paths([dict(file, previous_filename='.github/workflows/ci.yml')], 'student')[0])
        self.assertTrue(inspect_paths([file], 'other')[0])

    def test_missing_required_check_and_failed_status_block(self):
        class API:
            def get(self, path):
                return {'total_count': 0, 'check_runs': []}
            def pages(self, path):
                return []
        with patch.dict('os.environ', {'REQUIRED_CHECKS': 'trusted-tests'}):
            self.assertFalse(checks_pass(API(), 'abc'))

from automation.copilot_review import merge_approved, render_report


class PracticalPolicyTests(unittest.TestCase):
    def test_nested_policy_files_cannot_be_auto_merged(self):
        for name in ['AGENTS.md', 'SKILL.md', 'copilot-instructions.md', 'review.instructions.md', '.github/config.yml']:
            files = [{'filename': 'participants/student/task/' + name, 'status': 'added'}]
            self.assertTrue(inspect_paths(files, 'student')[0])

    def test_renamed_policy_file_remains_protected(self):
        files = [{'filename': 'participants/student/task/notes.md', 'status': 'renamed',
                  'previous_filename': 'participants/student/task/AGENTS.md'}]
        self.assertTrue(inspect_paths(files, 'student')[0])
    def test_optional_failures_do_not_block(self):
        advisory = {'requirement': 'Type annotations', 'result': 'fail', 'evidence': 'Optional', 'blocking': False}
        report = dict(REPORT, criteria=REPORT['criteria'] + [advisory])
        self.assertTrue(report_passes(report, REPORT['question_quote']))
        self.assertFalse(report_passes(dict(REPORT, criteria=[advisory]), REPORT['question_quote']))

    def test_minor_folder_and_cache_details_do_not_block(self):
        files = [{'filename': 'participants/student/pillar-2/chapter01/assignment_1/__pycache__/main.pyc', 'status': 'added'},
                 {'filename': 'participants/student/other-assignment/main.py', 'status': 'added'}]
        self.assertEqual(inspect_paths(files, 'student')[0], [])

    def test_credentials_still_block(self):
        files = [{'filename': 'participants/student/task/.env', 'status': 'added'}]
        self.assertTrue(inspect_paths(files, 'student')[0])

    def test_only_explicit_bot_advisories_are_nonblocking(self):
        thread = {'isResolved': False, 'comments': {'nodes': [
            {'body': 'ADVISORY: consider type hints', 'author': {'login': 'copilot-pull-request-reviewer', '__typename': 'Bot'}}]}}
        self.assertFalse(blocking_thread(thread))
        thread['comments']['nodes'][0]['body'] = 'BLOCKER: wrong result for normal input'
        self.assertTrue(blocking_thread(thread))
        thread['comments']['nodes'][0]['body'] = 'Please inspect this behavior'
        self.assertTrue(blocking_thread(thread))

    def test_invalid_blocking_type_is_rejected(self):
        report = dict(REPORT, criteria=[dict(REPORT['criteria'][0], blocking='false')])
        self.assertIsNone(parse_report('```elevate-report\n' + json.dumps(report) + '\n```'))


class MergeAPI:
    repo = 'org/repo'

    def __init__(self):
        self.pr = {'number': 4, 'head': {'sha': 'reviewed'}, 'body': REPORT['question_quote'],
                   'user': {'login': 'student'}, 'title': 'Transactions', 'state': 'open',
                   'draft': False, 'base': {'ref': 'main'}, 'mergeable': True,
                   'mergeable_state': 'clean', 'changed_files': 1}
        self.review = {'id': 10, 'user': {'login': 'copilot-pull-request-reviewer[bot]', 'type': 'Bot'},
                       'state': 'APPROVED', 'commit_id': 'reviewed', 'html_url': 'https://github.com/org/repo/pull/4#review',
                       'body': '```elevate-report\n' + json.dumps(REPORT) + '\n```'}
        self.files = [{'filename': 'participants/student/python/chapter-01-basics/assessment-01-test/main.py', 'status': 'added'}]
        self.writes = []
        self.result = {'merged': True, 'sha': 'mergedcommit'}
        self.unresolved_threads = False

    def get(self, path):
        return self.pr

    def pages(self, path):
        return self.files if path.endswith('/files') else [self.review]

    def unresolved(self, number):
        return self.unresolved_threads

    def request(self, path, data, method):
        self.writes.append((path, data, method))
        return self.result


class MergeTests(unittest.TestCase):
    def run_merge(self, api, original=None, ci=True):
        with patch('automation.copilot_review.checks_pass', return_value=ci):
            return merge_approved(api, original or dict(api.pr), api.review, REPORT)

    def test_merge_is_bound_to_reviewed_sha(self):
        api = MergeAPI()
        self.assertEqual(self.run_merge(api)[0], 'mergedcommit')
        self.assertEqual(api.writes[0][1]['sha'], 'reviewed')
        self.assertEqual(api.writes[0][1]['merge_method'], 'squash')

    def test_new_commit_cannot_merge(self):
        api = MergeAPI()
        self.assertIsNone(self.run_merge(api, dict(api.pr, head={'sha': 'old'}))[0])
        self.assertEqual(api.writes, [])

    def test_other_participant_or_rename_origin_cannot_merge(self):
        for change in [{'filename': 'participants/other/python/chapter-01-basics/assessment-01-test/main.py'},
                       {'previous_filename': 'README.md'}]:
            api = MergeAPI()
            api.files[0].update(change)
            self.assertIsNone(self.run_merge(api)[0])
            self.assertEqual(api.writes, [])

    def test_failed_checks_or_unresolved_threads_block(self):
        api = MergeAPI()
        self.assertIsNone(self.run_merge(api, ci=False)[0])
        api.unresolved_threads = True
        self.assertIsNone(self.run_merge(api)[0])
        self.assertEqual(api.writes, [])

    def test_revoked_approval_and_branch_rules_block(self):
        for change in ['approval', 'rules']:
            api = MergeAPI()
            if change == 'approval':
                api.review['state'] = 'DISMISSED'
            else:
                api.pr['mergeable_state'] = 'blocked'
            self.assertIsNone(self.run_merge(api)[0])
            self.assertEqual(api.writes, [])

    def test_unconfirmed_merge_is_not_success(self):
        api = MergeAPI()
        api.result = {'merged': False}
        self.assertIsNone(self.run_merge(api)[0])

    def test_native_approval_does_not_require_custom_json(self):
        api = MergeAPI()
        api.review['body'] = 'Approved: core assignment requirements are satisfied.'
        with patch('automation.copilot_review.checks_pass', return_value=True):
            self.assertEqual(merge_approved(api, api.pr, api.review, None)[0], 'mergedcommit')

    def test_report_distinguishes_waiting_from_merged(self):
        api = MergeAPI()
        args = (api, api.pr, {'participants/student/python/chapter-01-basics/assessment-01-test'}, api.review, REPORT, [], True, [])
        pending = render_report(*args)
        merged = render_report(*args, merged_sha='mergedcommit')
        self.assertIn('wait for the merged confirmation', pending)
        self.assertNotIn('Unblock the next learning stage', pending)
        self.assertIn('Merged — assessment complete', merged)
        self.assertIn('/tree/mergedcommit/participants/student/', merged)
        self.assertIn('| Requirement | Result | Evidence |', merged)


if __name__ == '__main__':
    unittest.main()
