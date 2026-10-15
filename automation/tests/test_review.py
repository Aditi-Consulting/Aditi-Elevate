import unittest
from unittest.mock import patch
from automation.review import inspect_paths
from automation.ai_review import grade_passes, question_valid, human_objections, process_ai

QUESTION = {'status': 'found', 'source_pr': 4,
            'question_quote': 'Return the sum of the transaction amounts.',
            'matching_reason': 'Question explicitly supplied in the current PR.',
            'criteria': [{'id': 'sum', 'requirement': 'Return the sum'}]}
GRADE = {'criteria': [{'id': 'sum', 'result': 'pass', 'evidence': 'main.py: return sum(values)', 'feedback': ''}],
         'blockers': [], 'improvements': ['Add descriptive type annotations.'],
         'summary': 'Matches the question by inspection.', 'needs_execution': False}


class FakeAPI:
    repo = 'org/repo'

    def __init__(self):
        self.writes, self.reviews = [], []
        self.changed = False
        self.reads = 0

    def get(self, path):
        self.reads += 1
        return {'number': 4, 'state': 'open', 'draft': False, 'base': {'ref': 'main'},
                'head': {'sha': 'changed' if self.changed and self.reads > 1 else 'abc'},
                'user': {'login': 'student'}, 'changed_files': 1, 'title': 'Transactions',
                'body': QUESTION['question_quote'], 'html_url': 'https://github.com/org/repo/pull/4'}

    def pages(self, path):
        if path.endswith('/files'):
            return [{'filename': 'participants/student/python/chapter-01-basics/assessment-01-test/main.py', 'status': 'added'}]
        if path.endswith('/reviews'):
            return self.reviews
        return []

    def unresolved(self, number):
        return False

    def request(self, path, data, method=None):
        self.writes.append((path, data))


class ReviewTests(unittest.TestCase):
    def test_grade_requires_all_criteria_with_evidence(self):
        self.assertTrue(grade_passes(QUESTION, GRADE))
        for change in [{'criteria': []}, {'blockers': ['Incorrect sum']}, {'needs_execution': True},
                       {'criteria': [dict(GRADE['criteria'][0], result='unverified')]},
                       {'criteria': [dict(GRADE['criteria'][0], evidence='')]},
                       {'criteria': GRADE['criteria'] * 2}]:
            self.assertFalse(grade_passes(QUESTION, dict(GRADE, **change)))

    def test_question_provenance(self):
        candidates = [{'number': 4, 'body': QUESTION['question_quote']}]
        self.assertTrue(question_valid(QUESTION, candidates))
        self.assertFalse(question_valid(dict(QUESTION, source_pr=99), candidates))
        self.assertFalse(question_valid(dict(QUESTION, question_quote='An invented question never assigned'), candidates))
        self.assertFalse(question_valid(dict(QUESTION, status='ambiguous'), candidates))

    def test_human_objections_cannot_be_overridden(self):
        review = {'id': 1, 'user': {'login': 'Teacher'}, 'state': 'CHANGES_REQUESTED'}
        self.assertTrue(human_objections([review]))
        self.assertFalse(human_objections([review, dict(review, id=2, state='APPROVED')]))

    def test_scope_and_cache(self):
        root = 'participants/Student/python/chapter-01-basics/assessment-01-transactions/'
        file = {'filename': root + 'main.py', 'status': 'added'}
        self.assertEqual(inspect_paths([file], 'student')[0], [])
        self.assertTrue(inspect_paths([file], 'other')[0])
        self.assertTrue(inspect_paths([dict(file, previous_filename='.github/workflows/ci.yml')], 'student')[0])
        cache = dict(file, filename=root + '__pycache__/main.pyc')
        self.assertTrue(inspect_paths([cache], 'student')[0])
        self.assertEqual(inspect_paths([dict(cache, status='removed')], 'student')[0], [])

    def run_process(self, api, question=QUESTION, grade=GRADE, dry_run=False, omitted=None):
        readme = 'participants/student/python/chapter-01-basics/assessment-01-test/README.md'
        with patch('automation.ai_review.snapshot', return_value=({readme: 'Setup and instructions'}, omitted or [])), \
             patch('automation.ai_review.checks_state', return_value=({}, [])), \
             patch('automation.ai_review.model_call', side_effect=[question, grade]) as model, \
             patch('automation.ai_review.email_report') as mail:
            process_ai(api, 4, [], dry_run)
            return model.call_count, mail.call_count

    def test_pass_creates_approval_and_email(self):
        api = FakeAPI()
        self.assertEqual(self.run_process(api), (2, 1))
        self.assertEqual(api.writes[0][1]['event'], 'APPROVE')
        self.assertEqual(api.writes[0][1]['commit_id'], 'abc')

    def test_missing_question_requests_clarification_and_emails(self):
        api = FakeAPI()
        self.assertEqual(self.run_process(api, question=dict(QUESTION, status='missing')), (1, 1))
        self.assertEqual(api.writes[0][1]['event'], 'COMMENT')
        self.assertIn('Question unavailable', api.writes[0][1]['body'])

    def test_dry_run_makes_no_ai_calls_or_writes(self):
        api = FakeAPI()
        self.assertEqual(self.run_process(api, dry_run=True), (0, 0))
        self.assertEqual(api.writes, [])

    def test_new_commit_prevents_stale_approval(self):
        api = FakeAPI()
        api.changed = True
        self.run_process(api)
        self.assertEqual(api.writes, [])

    def test_unread_files_prevent_approval(self):
        api = FakeAPI()
        self.run_process(api, omitted=['dataset.csv'])
        self.assertEqual(api.writes[0][1]['event'], 'COMMENT')

    def test_failed_criterion_requests_changes(self):
        api = FakeAPI()
        self.run_process(api, grade=dict(GRADE, criteria=[dict(GRADE['criteria'][0], result='fail')]))
        self.assertEqual(api.writes[0][1]['event'], 'CHANGES_REQUESTED')

    def test_previous_approval_is_revoked_before_regrading(self):
        api = FakeAPI()
        api.reviews = [{'id': 5, 'user': {'login': 'github-actions[bot]'},
                        'body': '<!-- elevate-ai:old -->', 'state': 'APPROVED'}]
        self.run_process(api)
        self.assertTrue(api.writes[0][0].endswith('/dismissals'))


if __name__ == '__main__':
    unittest.main()
