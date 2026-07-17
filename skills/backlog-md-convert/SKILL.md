---
name: backlog-md-convert
description: Convert standard Markdown to Backlog proprietary format. Use ONLY when converting Markdown content to Backlog formatting syntax.
---

# Markdown to Backlog Format Converter

Convert standard/GitHub-flavored Markdown to Backlog's proprietary wiki formatting syntax.

## Usage

```bash
python3 convert.py input.md > output.txt
cat input.md | python3 convert.py
```

## Conversion Rules

| Standard MD | Backlog | Context |
|---|---|---|
| `#` | `*` | Line start heading |
| `##` | `**` | Line start heading |
| `###` | `***` | Line start heading |
| `` ``` `` code block | `{code}...{/code}` | Fenced code |
| `>` quote | `{quote}...{/quote}` | Blockquote |
| `- ` list | `・` | Unordered list |
| `**text**` | `''text''` | Inline bold |
| Table header | Append `|h` | Tables |

Reference: https://nulab.com/backlog/enterprise/help-guide/users-guide/rules-to-formatting-texts-markdown/
