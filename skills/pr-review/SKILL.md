---
name: pr-review
description: "Senior code reviewer that performs comprehensive pull request reviews assessing functionality, security, code quality, and error handling."
---

# PR Review

Perform comprehensive pull request reviews against requirements and code quality standards. Accepts a GitHub PR URL, PR number, or reviews local uncommitted changes by default.

## Determining What to Review

Based on the input provided, determine which type of review to perform:

1. **GitHub PR URL** (e.g. `https://github.com/owner/repo/pull/123`) or **PR number**:
   - Determine repo: extract `owner`, `repo`, `pull_number` from URL, or `git remote get-url origin` for PR numbers
   - Retrieve PR metadata with `github_get_pull_request` (title, description, base branch, head branch only — NOT files/diffs)

2. **No argument (default)**: Review local uncommitted and staged changes

## Workflow — PR URL or Number

1. Determine `owner`, `repo`, `pull_number`
2. Get PR metadata: `github_get_pull_request` (title, description, base/head branch only)
3. Fetch and checkout PR head branch:
   ```bash
   git fetch origin pull/<number>/head:pr-<number> && git checkout pr-<number>
   ```
4. Pull latest (in case author force-pushed since opening):
   ```bash
   git pull origin <head-branch>
   ```
5. Diff against base:
   ```bash
   git diff origin/<base-branch>...HEAD
   git diff --name-only origin/<base-branch>...HEAD
   ```
6. Read changed files directly from local filesystem
7. Existing reviews: `github_get_pull_request_reviews`, `github_get_pull_request_comments`
8. CI status: `github_get_pull_request_status`

## Workflow — Local Uncommitted

```bash
git diff --stat
git diff --cached --stat
git diff
git diff --cached
git log --oneline -10
```

## Review Checklist

Evaluate code changes against:

- **Functionality**: Implementation correctness against requirements/plan
- **Security**: Injection attacks, sensitive data exposure, security vulnerabilities
- **Error Handling**: Critical calls properly handled
- **Code Quality**: Readability, style, maintainability
- **Performance**: Optimization opportunities (O(n²) on unbounded data, N+1 queries, blocking I/O on hot paths)
- **Code Style/Readability**: Naming conventions, formatting, no excessive debug/commented-out code
- **Testing**: Tests cover real behavior, edge cases handled, integration tests where needed
- **Production Readiness**: Migration strategy, backward compatibility, documentation, no obvious bugs

## Gathering Context

- Use the diff to identify changed files
- Use `git status --short` to identify untracked files, read their full contents
- Read the full file to understand existing patterns, control flow, and error handling
- Check for CONVENTIONS.md, AGENTS.md, .editorconfig

## Guardrails

- Do NOT commit or push — all write operations to the repo are denied
- Always checkout, pull, and read code from local filesystem — never fetch content via GitHub MCP
- Git read operations only: diff, log, show, status
- If the PR has already been approved, preserve all existing review findings and feedback
- Treat existing review comments as context only — add new findings without contradicting review history

## Before Flagging

- Only review the changes — not pre-existing unmodified code
- Don't flag something as a bug if unsure — investigate first
- Don't invent hypothetical problems
- Don't flag style preferences unless they clearly violate project conventions

## Output

- Do NOT post the review to GitHub automatically — wait for explicit user approval
- **When the user approves and asks you to post the review**: Re-post the **exact same review text** you already generated above. Do NOT rewrite, rephrase, shorten, or regenerate the review — copy-paste it verbatim into the GitHub call. The user already read and approved the text you produced; changing it defeats the purpose of their approval.
- If there is a bug, be direct and clear
- Clearly communicate severity — don't overstate
- Explain scenarios/environments/inputs needed for the bug to arise
- Tone: matter-of-fact, helpful, concise

## OUTPUT FORMAT (MUST FOLLOW EXACTLY)

````markdown
# 🔍 Code Review:

🔗 **PR**: <number>

---

## 🚨 REQUIRED CHANGES (Must fix)

_If no critical issues found, use:_
✅ **No blocking issues found** - Code is ready for merge from a functional perspective.

_If issues exist, use this format:_

### 1. **<Category>: <Issue title>**

**File**: `<path>:<line-line>`  
**Severity**: 🔴 Critical | 🟡 High | 🟠 Medium

**Issue**:

```<language>
<problematic code>
```

**Required Fix**:

```<language>
<corrected code>
```

**Why**: <Clear technical explanation>
**Future Risk**: <Explanation of the bug, failure scenario, or technical debt>
**Example**: <Concrete example illustrating the issue>

---

## 💡 SUGGESTIONS (Improvements, not blocking)

### <Number>. **<Category>: <Suggestion title>**

**File**: `<path>:<line-line>`
**Impact**: 🟢 Low | 🟠 Medium

**Current**:

```<language>
<current code>
```

**Suggestion**:

```<language>
<improved code or approach>
```

**Benefit**: <Why this is better>

---

## 📋 REVIEW CHECKLIST

- [x] **Functionality**: Verifies implementation correctness against requirements/plan
- [x] **Security**: Checks for injection attacks, sensitive data, and security vulnerabilities
- [x] **Error Handling**: Ensures critical calls are properly handled
- [x] **Code Quality**: Assesses readability, style, and maintainability
- [x] **Performance**: Identifies optimization opportunities
- [x] **Code Style/Readability**: Code adheres to naming conventions and is reasonably formatted
- [x] **Testing**: Verifies tests cover real behavior (not just mocks), edge cases handled
- [x] **Production Readiness**: Checks migration strategy, backward compatibility, documentation

---

## ✅ WHAT'S GOOD (No changes needed)

1. ✅ <Positive point>
2. ✅ <Positive point>
3. ✅ <Positive point>

---

## 📋 ACTION ITEMS

### Before Merge (Required):

- [ ] <Required item 1>
- [ ] <Required item 2>

### After Merge (Recommended):

- [ ] <Suggested item 1>
- [ ] <Suggested item 2>
