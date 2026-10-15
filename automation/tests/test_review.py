import json
import unittest
from unittest.mock import patch
from automation.review import inspect_paths
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


if __name__ == '__main__':
    unittest.main()
