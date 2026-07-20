#!/usr/bin/env python3
"""
Convert standard Markdown to Google Chat formatting syntax.

Google Chat supports a subset of Markdown:
  Bold: *text*        Italic: _text_        Strikethrough: ~text~
  Inline code: `text`  Code block: ``` ```    Bullet list: - or *
  No headings, tables, blockquotes, or horizontal rules.

Usage:
    python3 convert.py input.md > output.txt
    cat input.md | python3 convert.py
"""

import sys
import re
from typing import List


def convert_heading(line: str) -> str:
    match = re.match(r'^(#{1,6})\s+(.+)$', line)
    if match:
        text = match.group(2)
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
        text = re.sub(r'___(.+?)___', r'\1', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'~~(.+?)~~', r'\1', text)
        text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'\1', text)
        text = re.sub(r'(?<!_)_([^_\n]+)_(?!_)', r'\1', text)
        text = convert_link(text)
        text = convert_image(text)
        return f'*{text}*'
    return line


def convert_bold(line: str) -> str:
    line = re.sub(r'\*\*(.+?)\*\*', r'*\1*', line)
    line = re.sub(r'__(.+?)__', r'*\1*', line)
    return line


def convert_italic(line: str) -> str:
    return re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'_\1_', line)


def convert_strikethrough(line: str) -> str:
    return re.sub(r'~~(.+?)~~', r'~\1~', line)


def convert_bold_italic(line: str) -> str:
    """Convert ***text*** or ___text___ (bold+italic) to _text_ (italic only).
    Google Chat doesn't support nested formatting, so bold+italic is simplified."""
    line = re.sub(r'\*\*\*(.+?)\*\*\*', r'_\1_', line)
    line = re.sub(r'___(.+?)___', r'_\1_', line)
    return line


def convert_link(line: str) -> str:
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', line)


def convert_image(line: str) -> str:
    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'\1 (\2)', line)


_URL_PLACEHOLDERS = []


def _protect_urls_before_format(line: str) -> str:
    """Replace (url) portions with placeholders to prevent formatting mangle."""
    _URL_PLACEHOLDERS.clear()
    def _save(m):
        _URL_PLACEHOLDERS.append(m.group(0))
        return f'\x00U{len(_URL_PLACEHOLDERS) - 1}\x00'
    return re.sub(r'\(https?://[^\)]+\)', _save, line)


def _restore_urls_after_format(line: str) -> str:
    """Restore url placeholders after formatting applied."""
    for i, url in enumerate(_URL_PLACEHOLDERS):
        line = line.replace(f'\x00U{i}\x00', url)
    return line


def convert_inline_formatting(line: str) -> str:
    line = convert_image(line)
    line = convert_link(line)
    line = _protect_urls_before_format(line)
    line = convert_bold_italic(line)
    line = convert_italic(line)
    line = convert_bold(line)
    line = convert_strikethrough(line)
    return _restore_urls_after_format(line)


def is_horizontal_rule(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return bool(re.match(r'^(\s*([-*_])\s*){3,}$', stripped))


def is_table_row(line: str) -> bool:
    return '|' in line


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    return bool(re.match(r'^\|?[\s]*:?-+:?[\s]*(\|[\s]*:?-+:?[\s]*)+\|?$', stripped))


def table_row_to_cells(line: str) -> List[str]:
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    return [convert_inline_formatting(c) for c in cells]


def table_cells_to_kv(header_cells: List[str], row_cells: List[str]) -> str:
    pairs = []
    for i, val in enumerate(row_cells):
        label = header_cells[i] if i < len(header_cells) else f'Col{i}'
        pairs.append(f'{label}: {val}')
    return ', '.join(pairs)


def _collapse_blank_lines(lines: List[str]) -> List[str]:
    collapsed: List[str] = []
    prev_blank = False
    for line in lines:
        is_blank = not line.strip()
        if is_blank:
            if not prev_blank and collapsed:
                collapsed.append('')
            prev_blank = True
        else:
            collapsed.append(line)
            prev_blank = False
    while collapsed and not collapsed[-1].strip():
        collapsed.pop()
    return collapsed


def convert_markdown_to_google_chat(text: str) -> str:
    lines = text.split('\n')
    result: List[str] = []

    in_fenced_code = False
    code_lang = ''

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith('```'):
            if not in_fenced_code:
                in_fenced_code = True
                code_lang = stripped[3:].strip()
                result.append('```' + code_lang)
                i += 1
                continue
            else:
                result.append('```')
                in_fenced_code = False
                code_lang = ''
                i += 1
                continue

        if in_fenced_code:
            result.append(line)
            i += 1
            continue

        if is_horizontal_rule(line):
            i += 1
            continue

        if stripped.startswith('> '):
            content = stripped[2:]
            result.append(convert_inline_formatting(content))
            i += 1
            continue
        if stripped.startswith('>'):
            content = stripped[1:]
            result.append(convert_inline_formatting(content))
            i += 1
            continue

        if is_table_row(line) and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            header_cells = [c.strip() for c in line.strip().strip('|').split('|')]
            header_cells = [convert_inline_formatting(re.sub(r'\*\*(.+?)\*\*', r'\1', re.sub(r'__(.+?)__', r'\1', c))) for c in header_cells]
            i += 2
            while i < len(lines) and is_table_row(lines[i]):
                row_cells = table_row_to_cells(lines[i])
                result.append(table_cells_to_kv(header_cells, row_cells))
                i += 1
            continue

        if is_table_separator(line):
            i += 1
            continue

        heading_result = convert_heading(line)
        if heading_result != line:
            result.append(heading_result)
            i += 1
            continue

        result.append(convert_inline_formatting(line))
        i += 1

    result = _collapse_blank_lines(result)
    return '\n'.join(result)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    output = convert_markdown_to_google_chat(content)
    sys.stdout.write(output)


if __name__ == '__main__':
    main()
