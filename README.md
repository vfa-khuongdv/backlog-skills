# AGENT-SKILLS

AI agent skills collection. Installable via `npx skills add vfa-khuongdv/backlog-skills`.

## Installation

```bash
npx skills add vfa-khuongdv/backlog-skills
```

Works on **OpenCode** and **Claude Code**.

## Skills

### backlog-add-japanese

Create bilingual English-Japanese Backlog wiki from an existing text file.

```
> Convert README.MD to Backlog wiki format, add **English and **Japanese sections
```

### backlog-md-convert

Convert Markdown to Backlog wiki format.

```
> Convert RELEASE_NOTES.md to Backlog wiki format, save as RELEASE_NOTES.txt
```

```
> Convert RELEASE_NOTES.md for Google Chat, save as gc_RELEASE_NOTES.txt
```

### pr-description

Generate Pull Request descriptions from git diff between feature and base branches. Auto-detects ticket number from branch name. See [EXAMPLES.md](skills/pr-description/EXAMPLES.md) for sample output.

```
> Create PR description from branch feature/20344-coin-analytics against develop
```

### pr-review

Comprehensive pull request review against requirements and code quality standards. Accepts a GitHub PR URL/PR number or reviews local uncommitted changes.

```
> Review this pull request: https://github.com/owner/repo/pull/123
```
