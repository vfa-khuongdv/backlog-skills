---
name: pr-description
description: Use when creating a GitHub Pull Request description from a git diff.
---

# PR Description Generator

Generate Pull Request description from git diff. See [EXAMPLES.md](EXAMPLES.md) for sample output.

## Usage

```bash
# From current branch vs develop
git diff origin/develop...HEAD > /tmp/pr.diff
<invoke with pr-description skill> > PR_DESCRIPTION.md

# Or specify branches explicitly
git diff origin/develop...feature/xxx > /tmp/pr.diff
<invoke with pr-description skill> > PR_DESCRIPTION.md
```

The skill will automatically run `git diff` against the base branch (default: `origin/develop`) and the feature branch (default: current branch).

**Ticket detection:** Extract ticket number from branch name (e.g. `feature/20344-api-name` → `20344`). Then construct URL based on project's issue tracker (e.g. GitHub, Redmine, Backlog). Run `git branch --show-current` to get the branch name.

## Handling Large Diffs

When >10 files or >500 lines: run `git diff --stat` first to see the scope, then group changes by module/feature, and analyze each group separately to avoid context overflow. For repetitive changes (renames, lint fixes), list the pattern once with the count instead of enumerating every file.

## Output Format

No intro text. Output sections directly:

## Description

A 2-3 sentence summary of what this PR does and why. Keep it high-level — reviewers should understand the purpose without reading the code.

Ticket: [Extract from branch name (e.g. `feature/20344-api-name` → ticket `20344`). Construct full URL based on project's tracker. If not found, write "N/A"]

---

## Key Features

List 1-5 main features or changes. Each should be one line with specific technical details.

```
- New `getCoinReportSummary` query returning total coins, bonus coins, and expiration data
- addMonthlyBonusCoin mutation with atomic rollback via Prisma $transaction
```

---

## Changes Made

Every significant change, one per line. Use **bold** for the action or component name, followed by the file and what changed. Cover: new APIs, modified logic, schema migrations, config, bug fixes, tests.

```
- **Added `getCoinReportSummary` resolver** in `coin.resolver.ts` — aggregates totalHP, bonusCoins, earnedCoins, expiresAt from user and transaction records
- **Added `addMonthlyBonusCoin` mutation** in `coin.service.ts` — bulk insert + update wrapped in Prisma $transaction with per-user audit record
```

---

## Self-Review

Checklist for the PR author to self-verify before requesting review. Fill in what you actually tested or verified.

- [ ] Functionality — what did you manually test? which edge cases? integration tests pass?
- [ ] Security — are inputs validated? is auth enforced? any sensitive data exposed?
- [ ] Error Handling — are failures caught? does it rollback on error? are error messages clear?
- [ ] Code Quality — lint passes? naming consistent? complex logic documented?
- [ ] Dependencies — any new packages added? are they necessary and compatible?

---

## Manual Test Steps

2-4 scenarios the reviewer can run to verify the changes. Each with input → expected output. Keep steps specific and verifiable.

```
1. Test bonus distribution:
   - Call addMonthlyBonusCoin with userIds: ["a", "b", "c"]
   - Verify 3 users incremented, 3 transaction rows created
2. Test rollback:
   - Call with invalid UUID in middle of list
   - Verify error returned, first user unchanged, zero transaction rows
```
