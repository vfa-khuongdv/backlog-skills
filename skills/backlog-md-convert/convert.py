#!/usr/bin/env python3
"""
Convert standard Markdown to Backlog's proprietary formatting syntax.

Usage:
    python3 convert.py input.md > output.txt
    cat input.md | python3 convert.py
"""

import sys
import re
from typing import List


def is_horizontal_rule(line: str) -> bool:
    """Check if line is a horizontal rule: ---, ***, ___ (3+ chars)"""
    stripped = line.strip()
    if not stripped:
        return False
    return bool(re.match(r'^(\s*([-*_])\s*){3,}$', stripped))


def is_table_row(line: str) -> bool:
    """Check if line is part of a markdown table (contains |)"""
    return '|' in line


def convert_heading(line: str) -> str:
    """Convert # heading to * heading. Only matches at line start."""
    match = re.match(r'^(#{1,6})\s(.+)$', line)
    if match:
        num_hashes = len(match.group(1))
        if num_hashes == 2:
            stars = '***'
        else:
            stars = '*' * num_hashes
        return f'{stars} {match.group(2)}'
    return line


def convert_unordered_list(line: str) -> str:
    """Convert - /* /+ list marker to ・. Handles indentation."""
    match = re.match(r'^(\s*)[-*+]\s(.+)$', line)
    if match:
        indent = match.group(1)
        content = match.group(2)
        return f'{indent}・ {content}'
    return line


def convert_links(line: str) -> str:
    """Remove markdown link syntax, keeping only the link text.
    Images ![alt](url) are preserved untouched."""
    return re.sub(r'(?<!!)\[([^\]]+)\]\([^\)]+\)', r'\1', line)


def convert_bold(line: str) -> str:
    """Convert **bold** and __bold__ to ''bold'' (inline, not heading)."""
    line = re.sub(r'\*\*(.+?)\*\*', r"''\1''", line)
    line = re.sub(r'__(.+?)__', r"''\1''", line)
    return line


def convert_inline_code(line: str) -> str:
    """Convert `code` to "code" (inline)."""
    return re.sub(r'`([^`]+)`', r'"\1"', line)


def convert_line(line: str) -> str:
    """Apply heading, list, bold, and inline code conversion to a single line."""
    converted = convert_heading(line)
    if converted == line:
        converted = convert_unordered_list(line)
    converted = convert_links(converted)
    converted = convert_bold(converted)
    return convert_inline_code(converted)


def is_table_separator(line: str) -> bool:
    """Check if line is a markdown table separator like |---|---|"""
    stripped = line.strip()
    return bool(re.match(r'^\|?[\s]*:?-+:?[\s]*(\|[\s]*:?-+:?[\s]*)+\|?$', stripped))


def convert_markdown_to_backlog(text: str) -> str:
    """Convert standard Markdown to Backlog proprietary format."""
    lines = text.split('\n')
    result: List[str] = []

    in_fenced_code = False
    in_quote_block = False
    code_lang = ''
    quote_lines: List[str] = []

    def flush_quote():
        nonlocal in_quote_block
        if in_quote_block and quote_lines:
            result.append('{quote}')
            for ql in quote_lines:
                result.append(ql)
            result.append('{/quote}')
            quote_lines.clear()
            in_quote_block = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # --- Handle fenced code blocks ---
        if stripped.startswith('```'):
            if not in_fenced_code:
                flush_quote()
                in_fenced_code = True
                code_lang = stripped[3:].strip()
                result.append('{code}')
                if code_lang:
                    result.append(code_lang)
                i += 1
                continue
            else:
                result.append('{/code}')
                in_fenced_code = False
                code_lang = ''
                i += 1
                continue

        # Inside fenced code block: pass through unchanged
        if in_fenced_code:
            result.append(line)
            i += 1
            continue

        # --- Handle horizontal rules ---
        if is_horizontal_rule(line):
            flush_quote()
            result.append('**')
            i += 1
            continue

        # --- Handle quote blocks ---
        if stripped.startswith('> '):
            if not in_quote_block:
                in_quote_block = True
            content = stripped[2:]
            converted_content = convert_line(content)
            quote_lines.append(converted_content)
            i += 1
            continue

        # Flush quote if we were in one
        if in_quote_block:
            flush_quote()

        # --- Handle table: header row followed by separator ---
        if is_table_row(line) and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            converted_header = convert_bold(convert_line(line))
            if converted_header.rstrip().endswith('|'):
                result.append(converted_header.rstrip() + 'h')
            else:
                result.append(converted_header.rstrip() + '|h')
            i += 2  # skip header and separator
            continue

        # --- Skip orphaned separator row ---
        if is_table_separator(line):
            i += 1
            continue

        # --- Handle headings ---
        heading_result = convert_heading(line)
        if heading_result != line:
            result.append(convert_inline_code(convert_bold(convert_links(heading_result))))
            i += 1
            continue

        # --- Handle unordered lists (skip if table row) ---
        if not is_table_row(line):
            list_result = convert_unordered_list(line)
            if list_result != line:
                result.append(convert_inline_code(convert_bold(convert_links(list_result))))
                i += 1
                continue

        # --- Everything else: pass through ---
        result.append(convert_inline_code(convert_bold(convert_links(line))))
        i += 1

    # Close any remaining open blocks
    flush_quote()
    if in_fenced_code:
        result.append('{/code}')

    result = [line for line in result if line.strip()]
    return '\n'.join(result)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    output = convert_markdown_to_backlog(content)
    sys.stdout.write(output)


if __name__ == '__main__':
    main()
