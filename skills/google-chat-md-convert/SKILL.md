---
name: google-chat-md-convert
description: Convert standard Markdown to Google Chat formatting syntax. Use ONLY when converting Markdown content for Google Chat messages.
---

# Markdown to Google Chat Format Converter

Convert standard/GitHub-flavored Markdown to Google Chat's supported text formatting.

## Usage

```bash
python3 convert.py input.md > output.txt
cat input.md | python3 convert.py
```

## Conversion Rules

| Standard MD | Google Chat | Notes |
|---|---|---|
| `#` ... `######` headings | `*text*` (bold) | Headings become bold text |
| `**text**` / `__text__` | `*text*` | Bold |
| `*text*` | `_text_` | Italic |
| `_text_` | `_text_` | Italic (unchanged) |
| `~~text~~` | `~text~` | Strikethrough |
| `` `code` `` | `` `code` `` | Inline code (unchanged) |
| ``` ```code``` ``` | ``` ```code``` ``` | Code block (unchanged) |
| `***text***` / `___text___` | `_text_` (italic) | Bold+italic → italic only |
| `- ` / `* ` / `+ ` list | `- ` / `* ` / `+ ` | Unordered list (unchanged) |
| `[text](url)` | `text (url)` | Links (URLs auto-link in Google Chat) |
| `![alt](url)` | `alt (url)` | Images |
| `> quote` | plain text | Blockquote (strips prefix) |
| `---` horizontal rule | removed | Not supported |
| Table | `Key: Value, Key: Value` | Converted to key-value pairs |
