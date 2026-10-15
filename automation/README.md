# Aditi Elevate assessment review bot

Reviews participant PRs, provides a requirement-by-requirement grading report,
approves passing submissions, and emails Anjali the report. Missing or ambiguous
questions generate a clarification on the PR and an email to Anjali. Every graded
submission receives improvement suggestions, including passing submissions.

## Policy

The bot extracts the question from the PR body. If absent, it can reuse another
PR's question when an explicit source reference or matching assessment ID and
compatible task establish the same assessment. Similar topics alone are insufficient.
It validates an exact quote against the source PR and cites that PR in the report.

It generates an atomic pass/fail rubric **before** seeing the solution, then reviews
the full assessment folder at the exact commit, including unchanged files. Every
criterion receives pass/fail/unverified, code evidence, and feedback. There is no
invented numeric threshold: all requirements must pass.

This is **AI static review, not execution-backed verification**. Participant code
and tests are never run. Notebook outputs are excluded. If execution is necessary
to establish correctness, the bot escalates. ML metrics, external data and binary
assets will generally need human review in this initial implementation.

Approval additionally requires correct submission structure, no omitted files,
successful configured CI checks, and no outstanding human changes request or
unresolved thread. Failed criteria request changes; uncertainty receives a comment.
Anjali receives approved reports and missing-question requests by email. The bot
does not merge PRs or unlock the learning platform. Anjali verifies the current PR
status before unblocking the participant.

AI judgments can be wrong and participant-authored questions can omit actual
requirements. Maintainers should audit source questions and sampled approvals.
Add trusted execution tests in a separate disposable environment for stronger
verification. Never execute participant code in this privileged workflow.

## Activation

Merge this branch into main, enable Actions, and configure these repository settings:

| Setting | Type | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | Actions secret | Approved OpenAI API project key |
| `ELEVATE_REVIEW_MODEL` | Actions variable | Available model supporting Responses structured outputs |
| `ELEVATE_REQUIRED_CHECKS` | Actions variable | Comma-separated required CI check names; optional until CI exists |
| `ELEVATE_SMTP_HOST` | Actions variable | Approved SMTP submission server |
| `ELEVATE_SMTP_PORT` | Actions variable | STARTTLS port; default 587 |
| `ELEVATE_SMTP_FROM` | Actions variable | Authorized sender address |
| `ELEVATE_SMTP_USERNAME` | Actions secret | Mail service username |
| `ELEVATE_SMTP_PASSWORD` | Actions secret | Mail service credential |

Recipient: `anjali.bhardwaj@aditiconsulting.com`. Use an approved mail service account.
The SMTP adapter requires STARTTLS/password authentication; OAuth-only providers
need a different adapter. Submission source and PR questions are sent to the
configured OpenAI project with `store: false`, incurring API usage charges.

Enable **Allow GitHub Actions to create and approve pull requests** under Settings
→ Actions → General → Workflow permissions. Organization policies may restrict
this. Allow the token to dismiss its previous reviews if dismissal restrictions
are configured. No administrator token is required.

Enable branch protection with stale approval dismissal, conversation resolution,
and trusted execution checks. Protect `.github/` and `automation/` with maintainer
review. Workflow success means the assistant ran, not that an assessment passed.

Run **Assessment review assistant** manually to process existing PRs. Creation,
edits, commits, and reopening trigger reviews; a 15-minute scheduled scan reconciles
CI results and review changes. GitHub may delay schedules. Only open, non-draft PRs
targeting main are processed; wait for coordinator handoff before merging.

The same input fingerprint is reviewed once. Changed questions, commits, checks,
or human objections invalidate previous bot decisions. Changes to the PR question
catalog may trigger regrading and additional API cost. Dismissing a bot review
suppresses reapproval for that fingerprint.

Missing API/mail configuration fails the workflow. If mail fails after approval,
a rerun retries delivery without regrading unchanged inputs. A bot-authored comment
records successful email delivery. Email and GitHub writes are not transactional:
a crash between delivery and its marker can cause duplicate mail. Likewise, PR
changes between final checks and publication remain possible. Reports are bound
to a commit and become historical after updates.

## Validation

```sh
python3 -m unittest discover -s automation/tests
GH_TOKEN="$(gh auth token)" GITHUB_REPOSITORY=Aditi-Consulting/Aditi-Elevate \
  python3 automation/ai_review.py --dry-run
```

Dry run reads GitHub only: no model calls, reviews or email. Unit tests simulate
model and mail responses. Real model responses, approval permissions and mail
delivery need verification after credentials are configured. Uses Python's
standard library only.

Limits fail closed: 80 text files, 120 KB per file, 240 KB source, 160 KB question
catalog and 100 check runs. Oversized/unreadable inputs require maintainer review;
they cannot silently pass. Only trusted main code executes in the privileged
workflow. PR files are read as data; participant dependencies are never installed.

References: [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses)
and [GitHub pull_request_target security](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target).
