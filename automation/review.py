"""Submission hygiene and human approval handoff. Never executes participant code."""
import json
from urllib.request import Request, urlopen

def blocking_thread(thread):
    if thread['isResolved']:
        return False
    comments = thread.get('comments', {}).get('nodes', [])
    if comments:
        first = comments[0]
        author = first.get('author') or {}
        if (author.get('__typename') == 'Bot'
                and author.get('login', '').lower() in {'copilot', 'copilot-pull-request-reviewer', 'copilot-pull-request-reviewer[bot]'}
                and first['body'].lstrip().startswith('ADVISORY:')):
            return False
    # Unclassified/human feedback must be evaluated, never silently dismissed.
    return True


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
                      nodes { isResolved comments(first:1) { nodes { body author { login __typename } } } }
                      pageInfo { hasNextPage endCursor }
                    }
                  }
                }
              }''', 'variables': {'owner': owner, 'name': name, 'number': number, 'cursor': cursor}})
            if data.get('errors'):
                raise RuntimeError('Unable to verify review threads')
            threads = data['data']['repository']['pullRequest']['reviewThreads']
            if any(blocking_thread(thread) for thread in threads['nodes']):
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
            if (parts[-1] in {'CODEOWNERS', 'AGENTS.md', 'CLAUDE.md', 'GEMINI.md', 'REVIEW.md', 'SKILL.md', 'copilot-instructions.md'}
                    or parts[-1].endswith('.instructions.md') or '.github' in parts):
                issues.add('Bot/instruction changes require Siddharthas-Aditi or AniiBee25 review and cannot be auto-merged as an assessment.')
            if len(parts) < 3 or parts[0] != 'participants' or parts[1].lower() != author.lower():
                issues.add('Keep all changes within your own assessment folder under participants/<github-username>/.')
                continue
            roots.add('/'.join(parts[:min(5, len(parts) - 1)]))
            if file['status'] != 'removed' and '.env' in parts:
                issues.add('Remove committed .env files that may expose credentials; use a credential-free example file.')
    return sorted(issues), roots
