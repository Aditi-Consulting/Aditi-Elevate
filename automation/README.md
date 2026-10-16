# Copilot assessment review and GitHub notifications

Uses native GitHub Copilot code review and GitHub comments mentioning `@AniiBee25`.
No OpenAI API key, external model calls, SMTP service or mail credentials are used.
GitHub delivers inbox/optional email notifications according to Anjali's settings.

## Enable ongoing automation

1. Merge the reviewed automation PR into main. Its scheduled workflow reconciles
   open participant PRs every 15 minutes (GitHub schedules can be delayed).
2. Enable automatic Copilot reviews in the repository ruleset targeting main,
   including **Review new pushes**. Confirm organization policies and Copilot usage
   allowances cover participant PRs. Personal Copilot access alone does not prove
   organization-wide automatic-review coverage. The workflow does not purchase
   licenses or alter billing settings.
3. Enable Copilot approvals if available and permitted. Approvals are a public
   preview and off by default. A COMMENT review never counts as an approval.
4. Include `.github/copilot-instructions.md` in participant branches: Copilot reads
   instructions from the PR head branch. Existing PR branches must incorporate the
   instructions before a re-review can be expected to produce assessment rubrics.
5. Set optional Actions variable `ELEVATE_REQUIRED_CHECKS` to comma-separated trusted
   test check names. Protect automation/instruction files with maintainer review,
   dismiss stale approvals, and require conversation resolution.

The participant PR template requests the question or an explicit source PR.
Copilot reviews core correctness and material security/run issues, with short,
actionable feedback. A native APPROVED review for the current commit is required;
COMMENT reviews, positive prose or absence of findings never count as approval.
Structured rubric tables are optional. When supplied, explicit core failures,
unverified core requirements or an invalid source question still prevent merging.
Missing JSON does not create a participant task or prevent a valid native approval.

The assistant checks ownership, configured CI and unresolved material/unclassified
feedback before merging. Clearly marked Copilot ADVISORY threads are non-blocking
for the assistant, subject to repository rules. Reports and coordinator notices
state whether the participant is merged and ready for the next stage. No participant
code executes in this workflow.

## Run against existing PRs

```sh
python3 -m unittest discover -s automation/tests
GH_TOKEN="$(gh auth token)" GITHUB_REPOSITORY=Aditi-Consulting/Aditi-Elevate \
  COMMENT_ACTOR="$(gh api user --jq .login)" \
  python3 automation/copilot_review.py --dry-run
```

Remove `--dry-run` to publish status comments. Add `--request-reviews` to make
initial Copilot review requests with the authenticated user's GitHub access. An
existing Copilot request anywhere in the PR timeline suppresses duplicate requests;
re-request explicitly in GitHub for revisions or a failed/stalled request. Native
automatic-review settings handle new commits in ongoing operation.

The local command uses the authenticated user's identity; Actions uses
`github-actions[bot]`. Both read trusted code, inspect participant metadata, and
never install participant dependencies. The Actions workflow needs to exist on
main before it can be dispatched; running the script locally is a separate operation.

Notifications are deduplicated by revision, review ID, readiness and PR body.
Writes and review changes are not transactional; always verify current status.
Source questions and model-derived rubric coverage still require maintainer audit.
The workflow merges eligible assessment PRs, closing them automatically. Anjali still unlocks the learning platform.

References: [Copilot review and approval](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review),
[GitHub notifications](https://docs.github.com/en/subscriptions-and-notifications/concepts/about-notifications).


## Merge and reporting policy

The workflow runs with `--merge-approved` and contents-write permission. A local
run must also supply `--merge-approved` to perform merges. Dry run never writes or
merges, even if that flag is supplied.

A current-commit Copilot approval is required, along with CI success, cleared
material feedback and correct participant ownership. Custom JSON is optional. The
assistant rechecks these gates immediately before a SHA-bound squash merge. GitHub
must report a clean, mergeable PR, and existing repository rules remain in effect.
Squash merging must be enabled. Unknown mergeability, stale commits, revoked
approvals, conflicts or rejected API requests keep the PR open for attention.

Every changed path, including rename origins, must belong to the PR author's
`participants/<github-username>/` folder. Chapter and assessment naming is advisory.
The merge preserves these paths on main; it does not move files or modify another
participant's folder. Wrongly located submissions must be corrected and reviewed
again before merging. Branches are retained for traceability.

Reports show participant, assignment, revision, folder links, decision, required
actions, grading evidence, linked code findings and optional improvements. Each
coordinator notice links to the full report and states whether the next stage may
be unblocked. Only a confirmed successful merge produces a completion notice,
including the merge commit and a stable link to the participant's merged folder.

GitHub merge and comment publication are separate operations. If a comment request
fails after a successful merge, maintainers must confirm the merge and publish the
handoff manually; a failed notification never rolls back committed work.


## Practical review scope

This is a learning assessment, not a production-readiness audit. Block only on
incorrect core behavior for normal or explicitly required inputs, missing required
functionality, inability to run the solution, material security issues, or invalid
ML evaluation. Require concrete evidence and a correction for each blocker.
Do not require exotic-input hardening unless the assignment calls for it.

Style, formatting, type hints, docstrings, extra test coverage, minor documentation,
folder spelling below the username, generated caches and alternate architectures
are not approval gates. README presence alone is not a gate. Participant folder
ownership and credential protection remain enforced. Optional criteria marked
`blocking:false` cannot fail the grade; at least one core criterion must pass.
Older reports without this field retain their original blocking meaning.

Copilot should consolidate all material findings in the first review and check only
fixes/regressions in subsequent reviews. No inline nitpicks; at most two advisory
suggestions in the summary. Explicit Copilot ADVISORY threads do not block the
assistant. Human/unclassified threads and changes-requested reviews still require
reviewer disposition. Existing branch rules may require resolving advisory threads;
the assistant does not override those rules or silently dismiss historical comments.

A missing machine-readable report is not an approval gate or a request for
participant code changes. This policy takes effect in native Copilot reviews
when the updated instruction file is present in the participant PR head branch.
Merge the reviewed automation draft and sync participant branches before re-review.
