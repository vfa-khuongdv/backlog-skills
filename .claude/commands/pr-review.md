---
description: Review code changes against requirements and code quality standards. Accepts a GitHub PR URL, PR number, or reviews local uncommitted changes by default.
agent: pr-review
---

$ARGUMENTS

If `$ARGUMENTS` is a GitHub Pull Request URL (for example, `https://github.com/owner/repo/pull/123`) or a PR number:

1. Determine the repository information:
   - If a URL is provided, extract `owner`, `repo`, and `pull_number`.
   - If only a PR number is provided, obtain the repository from `git remote get-url origin`.

2. Retrieve PR metadata using **only** `github_get_pull_request`.
   - Use it **only** for the PR title, description, base branch, and head branch.
   - **Do not** use this API to retrieve changed files or diffs.

3. Fetch and check out the PR head branch:
   ```bash
   git fetch origin pull/<number>/head:pr-<number>
   git checkout pr-<number>
   ```

4. Update the local branch:
   ```bash
   git pull origin <head-branch>
   ```

5. Generate the diff against the base branch:
   ```bash
   git diff origin/<base-branch>...HEAD
   ```

6. List changed files:
   ```bash
   git diff --name-only origin/<base-branch>...HEAD
   ```

7. Read the changed files directly from the local filesystem using the Read tool.

8. Retrieve existing review context only:
   - `github_get_pull_request_reviews`
   - `github_get_pull_request_comments`

9. Check the CI/build status using:
   - `github_get_pull_request_status`

If `$ARGUMENTS` is empty, review the current local uncommitted changes:

```bash
git diff --stat
git diff
git log --oneline -10
```

Review guidelines:

- Perform a thorough review covering:
  - Correctness
  - Bugs and edge cases
  - Performance
  - Security
  - Maintainability
  - Readability
  - Consistency with project conventions
  - Test coverage

- Output the review in the chat using the **exact OUTPUT FORMAT** defined in your agent instructions.

- **Do not** post the review to GitHub automatically. Wait for explicit user approval before calling `github_create_pull_request_review`.

Guardrails:
- If the PR has already been approved, **do not** remove, overwrite, or invalidate previous review comments. Preserve all existing review findings and feedback.
- Treat existing review comments as context only. Add new findings without modifying or contradicting previous review history unless the issue has been resolved.
