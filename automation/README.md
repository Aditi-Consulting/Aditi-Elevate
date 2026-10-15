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

The participant PR template requests the full question or an explicit source PR.
Copilot instructions request a source-grounded grading rubric, file/line evidence,
and constructive improvements. The assistant accepts a structured report only from
Copilot's bot review for the current commit. It checks the source quote against
the referenced PR, requires every criterion to pass, checks structure/README,
checks CI and unresolved conversations, and requires an actual APPROVED review
before notifying Anjali of clearance. It never manufactures approval from silence
or positive prose. Native Copilot approvals do not guarantee the handoff checks
pass; Anjali should use the latest assessment status before unblocking anyone.

Copilot output is not a guaranteed structured API. Missing/malformed rubrics and
unverifiable results stay pending for manual attention. A general code review may
provide useful feedback without being a complete assessment grade. Missing or
ambiguous questions identified in its report are highlighted on the PR. Every new
review result is linked in a coordinator notification; nonpassing results explicitly
say the participant is NOT cleared. No participant code executes in this workflow.

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
This workflow does not merge PRs or unlock the learning platform.

References: [Copilot review and approval](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review),
[GitHub notifications](https://docs.github.com/en/subscriptions-and-notifications/concepts/about-notifications).
