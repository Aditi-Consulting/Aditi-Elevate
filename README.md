# Aditi Elevate — Pillar 2

Welcome to the **Aditi Consulting Elevate Program**. This repository is the shared workspace for all employees assigned to **Pillar 2** to develop their skills, submit assessments, and receive feedback.

**Keep all Pillar 2 projects, assignments, and assessments in this repository. Request a review from `Siddharthas-Aditi` for every submission, and address and resolve all review comments before moving to the next assignment or task.**

## Quick start

1. Create a GitHub account using your **Aditi official email address**.
2. Share your GitHub username with **Anjali** and confirm that you have access to this repository.
3. Install the required tools listed below, with help from IT Support if needed.
4. Clone this repository and create a branch for your assessment.
5. Add your work to your employee folder under the appropriate learning area and chapter.
6. Open a pull request and request a review from **`Siddharthas-Aditi`**.
7. Address feedback and resolve review comments before starting the next task.

## GitHub account and repository access

- Use your **Aditi official email address** when creating your GitHub account.
- Share your GitHub username with **Anjali** after account creation so repository access can be coordinated.
- Accept any organization or repository invitation you receive, then verify that you can access [Aditi-Consulting/elevate](https://github.com/Aditi-Consulting/elevate).
- If you cannot access the repository or push a branch, contact Anjali for access assistance.

## Required software and tools

Have the following ready before beginning the learning path:

| Tool | Purpose |
| --- | --- |
| Python | Run Python programs and install project dependencies. |
| GitHub account and repository access | Collaborate, submit assessments, and request reviews. |
| Git | Clone the repository and manage changes from the command line. |
| GitHub Desktop | Manage branches, commits, and pushes using a desktop interface. |
| Visual Studio Code (VS Code) | Write, run, and debug project code. |
| Jupyter Notebook | Create and run notebooks for experiments and assessments. |

GitHub is an online platform; Git and GitHub Desktop are local tools. Use the Python and package versions specified by your chapter or assessment.

**If any required tool is unavailable on your machine, contact the IT Support Team and have it installed before starting Pillar 2.**

## Pillar 2 learning areas

| Learning area | Folder name |
| --- | --- |
| Python | `python` |
| Machine Learning | `machine-learning` |
| Deep Learning | `deep-learning` |
| Natural Language Processing (NLP) | `nlp` |
| FastAPI | `fastapi` |
| LangChain | `langchain` |
| LangGraph | `langgraph` |

Follow the chapters and assessment instructions assigned to you in the program.

## Organize your assessments

Create a project folder for the chapter you are currently working on **inside this shared repository**. For this workspace, an employee's chapter project is a folder, not a separate GitHub repository or nested Git repository.

Use the following structure as you add submissions. These folders are examples and should be created when needed:

```text
elevate/
├── README.md
└── participants/
    └── <github-username>/
        └── <learning-area>/
            └── chapter-01-<chapter-name>/
                └── assessment-01-<assessment-name>/
                    ├── README.md
                    ├── requirements.txt
                    ├── src/
                    ├── notebooks/
                    └── tests/
```

- Replace placeholders with your GitHub username and the assigned chapter and assessment names.
- Use lowercase folder names with hyphens, such as `chapter-01-python-basics`.
- Keep your submissions within your own employee folder. Do not modify another participant's work.
- Include only the folders your assessment needs; a notebook-only submission may not need `src/` or `tests/`.
- Keep related code, notebooks, documentation, and permitted supporting files together in the assessment folder.

## Create and submit an assessment

### 1. Clone the shared repository

In GitHub Desktop, select **File → Clone repository → URL**, enter the repository URL below, and choose a local folder:

```text
https://github.com/Aditi-Consulting/elevate.git
```

Alternatively, use a terminal:

```bash
git clone https://github.com/Aditi-Consulting/elevate.git
cd elevate
```

You only need to clone once. For later assessments, use your existing local copy.

### 2. Create a branch for the assessment

Start from the latest default branch. The commands below assume it is named `main`; use the repository's actual default branch if different. Commit any work in progress on its existing branch before switching branches.

```bash
git switch main
git pull origin main
git switch -c assessment/your-username/python-ch01-assessment01
```

Replace `your-username` and the assessment details with your own. Use a separate branch and pull request for each assessment. In GitHub Desktop, select the default branch, fetch and pull updates, then create a new branch.

### 3. Complete your work and document it

Create your assessment folder using the structure above. Implement the assignment and include a local `README.md` that explains:

- **Participant:** your name and GitHub username.
- **Assessment:** learning area, chapter, and assessment title or number.
- **Objective:** the problem or task you were assigned.
- **Approach:** your solution and key design decisions.
- **Setup:** Python version, dependencies, and configuration requirements.
- **How to run:** exact commands or notebook execution steps, relative to the assessment folder.
- **Validation and results:** checks performed, expected output, and relevant results.
- **References and limitations:** sources used, assumptions, and any known issues.

Include a dependency file, such as `requirements.txt`, when your solution uses third-party packages. Run your code or notebook before submission; for notebooks, restart the kernel and run all cells in order.

Do not commit passwords, API keys, access tokens, private employee or client data, local virtual environments, or generated caches. Use environment variables for credentials and document required variable names without their values. Reference large datasets or model files through an approved location instead of committing them.

### 4. Commit and push your assessment

Review your changes and stage only the files for your assessment. For example, after replacing the sample path and branch name with your own:

```bash
git status
git add participants/your-username/python/chapter-01-python-basics/assessment-01-fundamentals/
git commit -m "Add Python chapter 01 assessment 01"
git push -u origin assessment/your-username/python-ch01-assessment01
```

In GitHub Desktop, review the changed files, enter a meaningful commit message, commit to your assessment branch, then select **Publish branch** or **Push origin**.

### 5. Open a pull request and request review

1. Open [the shared repository](https://github.com/Aditi-Consulting/elevate) on GitHub.
2. Select **Compare & pull request**, or go to **Pull requests → New pull request**.
3. Set the base to the repository's default branch and compare it with your assessment branch.
4. Use a clear title, such as **`[Pillar 2][Python][Chapter 01] Assessment 01 — Your Name`**.
5. Fill in the description using the template below, then create the pull request when your work is ready.
6. In the pull request's **Reviewers** section, request a review from **`Siddharthas-Aditi`**. Adding someone as an assignee or mentioning them in the description does not replace a review request.
7. If the reviewer is not available in the selector, contact Anjali to coordinate access or reviewer availability.

Copy this template into your pull request description:

```markdown
## Assessment details
- Participant:
- GitHub username:
- Learning area:
- Chapter:
- Assessment title / number:
- Submission folder:

## Summary
Describe the task and what you implemented.

## How to run
Provide setup instructions and execution steps, or link to the assessment README.

## Validation and results
List the checks you ran and the results you observed.

## Questions or known limitations
Describe anything that needs reviewer attention, or write "None".

## Submission checklist
- [ ] My work is in my participant folder under the correct chapter and assessment.
- [ ] My assessment README includes setup and execution instructions.
- [ ] I ran my code or restarted and ran all notebook cells successfully.
- [ ] Required dependencies and references are documented.
- [ ] I checked that the submission contains no credentials or restricted data.
- [ ] I reviewed the changed files and removed unrelated changes.
```

### 6. Address feedback and complete the review

- Read all review comments and requested changes.
- Make corrections on the **same assessment branch**, then commit and push them. The existing pull request updates automatically.
- Reply to comments with a brief explanation of what changed. Ask for clarification in the relevant review thread if feedback is unclear.
- Resolve review conversations after addressing the feedback, following the reviewer's guidance.
- Re-request a review from **`Siddharthas-Aditi`** when the revisions are ready.
- **Address and resolve all review comments before proceeding to the next assignment or task.** Wait for reviewer approval and follow the maintainer's merge process; opening a pull request alone does not complete the review.

## Support and responsibilities

| Need | Contact |
| --- | --- |
| Share your GitHub username or coordinate repository access | **Anjali** |
| Request an assessment review or clarify review feedback | **`Siddharthas-Aditi`**, through the assessment pull request |
| Install required tools or resolve machine setup issues | **IT Support Team** |

Keep submissions focused, document your work clearly, and respond to feedback promptly. These practices help every participant learn consistently and keep assessment reviews efficient.

Thank you for your cooperation and commitment to the **Aditi Elevate Program**.
