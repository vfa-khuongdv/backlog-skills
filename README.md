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

### google-chat-md-convert

Convert Markdown to Google Chat formatting.

```
> Convert RELEASE_NOTES.md for Google Chat, save as gc_RELEASE_NOTES.txt
```

### pr-review

Comprehensive pull request review against requirements and code quality standards. Accepts a GitHub PR URL/PR number or reviews local uncommitted changes.

```
> /pr-review https://github.com/owner/repo/pull/123
```

## Platform-Specific Setup

### OpenCode — Agents & Commands

Skills are installed automatically. For the `/pr-review` command and agent persona:

1. **Agent** — Copy `agents/code-review.md` to `~/.config/opencode/agents/pr-review.md`
2. **Command** — Copy `.opencode/commands/pr-review.md` to your project's `.opencode/commands/` (or `~/.config/opencode/commands/` for global)

### Claude Code — Commands

Skills are installed automatically. For the `/pr-review` command:

Copy `.claude/commands/pr-review.md` to your project's `.claude/commands/` (or `~/.claude/commands/` for global).
