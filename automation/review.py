"""Submission hygiene and human approval handoff. Never executes participant code."""
import json
import re
from urllib.request import Request, urlopen

AREAS = {'python', 'machine-learning', 'deep-learning', 'nlp', 'fastapi', 'langchain', 'langgraph'}


class GitHub:
    def __init__(self, repo, token):
        self.repo = repo
        self.token = token

    def request(self, path, data=None, method=None):
        req = Request('https://api.github.com' + path,
                      data=json.dumps(data).encode() if data is not None else None,
                      method=method,
                      headers={'Authorization': 'Bearer ' + self.token,
                               'Accept': 'application/vnd.github+json',
                               'X-GitHub-Api-Version': '2022-11-28'})
        with urlopen(req, timeout=30) as response:
            return json.load(response)

    def get(self, suffix):
        return self.request(f'/repos/{self.repo}/{suffix}')

    def pages(self, suffix):
        result = []
        for page in range(1, 101):
            rows = self.get(f'{suffix}{"&" if "?" in suffix else "?"}per_page=100&page={page}')
            result.extend(rows)
            if len(rows) < 100:
                return result
        raise RuntimeError('Pagination limit reached; manual review required.')

    def unresolved(self, number):
        owner, name = self.repo.split('/')
        cursor = None
        while True:
            data = self.request('/graphql', {'query': '''
              query($owner:String!, $name:String!, $number:Int!, $cursor:String) {
                repository(owner:$owner,name:$name) {
                  pullRequest(number:$number) {
                    reviewThreads(first:100,after:$cursor) {
                      nodes { isResolved }
                      pageInfo { hasNextPage endCursor }
                    }
                  }
                }
              }''', 'variables': {'owner': owner, 'name': name, 'number': number, 'cursor': cursor}})
            if data.get('errors'):
                raise RuntimeError('Unable to verify review threads')
            threads = data['data']['repository']['pullRequest']['reviewThreads']
            if any(not thread['isResolved'] for thread in threads['nodes']):
                return True
            if not threads['pageInfo']['hasNextPage']:
                return False
            cursor = threads['pageInfo']['endCursor']


def inspect_paths(files, author):
    issues, roots = set(), set()
    for file in files:
        paths = [file['filename']]
        if file.get('previous_filename'):
            paths.append(file['previous_filename'])
        for path in paths:
            parts = path.split('/')
            if len(parts) < 6 or parts[0] != 'participants' or parts[1].lower() != author.lower():
                issues.add('Keep all changes within your own assessment folder under participants/<github-username>/.')
                continue
            roots.add('/'.join(parts[:5]))
            if parts[2] not in AREAS:
                issues.add('Use a documented learning-area folder (for example python or machine-learning).')
            if not re.fullmatch(r'chapter-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*', parts[3]):
                issues.add('Use chapter-NN-name with lowercase words separated by hyphens.')
            if not re.fullmatch(r'assessment-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*', parts[4]):
                issues.add('Use assessment-NN-name with lowercase words separated by hyphens.')
            if file['status'] != 'removed' and (any(p in {'.venv', 'venv', '__pycache__', 'node_modules', '.env'} for p in parts)
                                                or path.endswith(('.pyc', '.pyo'))):
                issues.add('Remove local environments, caches, compiled Python files, and .env files from the submission.')
    if len(roots) != 1:
        issues.add('Submit exactly one assessment per pull request.')
    return sorted(issues), roots
