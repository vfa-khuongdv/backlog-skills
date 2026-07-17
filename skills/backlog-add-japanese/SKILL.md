---
name: backlog-add-japanese
description: Add **English and **Japanese sections to Backlog-formatted content. Use when user needs to create a Japanese-localized version of English Backlog wiki text (e.g., README.txt -> README-output.txt).
---

# Add Japanese Section for Backlog

Convert a Backlog-formatted text file by adding both English and Japanese sections, suitable for posting to Backlog wiki.

## Input / Output

- **Input file**: `./README.txt` (or any path specified by user)
- **Output file**: `./README-output.txt` (default, user may override)

## Rules

### Processing steps

1. Read the input file
2. Add section marker `**English` at the very top before the original content
3. Preserve ALL original content exactly as-is below `**English`
4. Add section marker `**Japanese` after the English section
5. Translate the body content to Japanese, keeping Backlog formatting intact

### Format preservation (CRITICAL)

The Japanese translation MUST preserve the exact same Backlog wiki formatting structure:

- Keep `***` heading markers unchanged (e.g., `*** Note:` stays as structure, text translates)
- Keep `・` list markers unchanged
- Keep URLs unchanged
- Keep any `''bold''`, `{code}...{/code}`, `{quote}...{/quote}` markers unchanged
- DO NOT convert between MD and Backlog formats — preserve as-is
- Only the human-readable text gets translated

### Translation rules

- Use natural, professional Japanese suitable for business/technical documentation
- Use `です・ます` (desu/masu) polite form
- Keep technical terms like "macro", "VBA", "Microsoft Excel" in their standard Japanese technical form
- Translate section heading text but keep the heading markers

### Output structure (NO empty lines between sections)

```
**English
[original content unchanged]
**Japanese
[translated content with same Backlog formatting]
```

- `**English` immediately followed by original content (no blank line)
- Last line of English section immediately followed by `**Japanese` (no blank line)
- `**Japanese` immediately followed by Japanese content (no blank line)

## Usage

When this skill is loaded, read the specified input file, process it following the rules above, and write the result to the output file. Confirm the output path and content summary with the user.
