#!/usr/bin/env python3
import unittest

from convert import (
    is_horizontal_rule,
    is_table_row,
    is_table_separator,
    convert_heading,
    convert_unordered_list,
    convert_links,
    convert_bold,
    convert_inline_code,
    convert_line,
    convert_markdown_to_backlog,
)


class TestIsHorizontalRule(unittest.TestCase):
    def test_hyphens(self):
        self.assertTrue(is_horizontal_rule('---'))
        self.assertTrue(is_horizontal_rule('----'))
        self.assertTrue(is_horizontal_rule('-----'))

    def test_asterisks(self):
        self.assertTrue(is_horizontal_rule('***'))
        self.assertTrue(is_horizontal_rule('****'))

    def test_underscores(self):
        self.assertTrue(is_horizontal_rule('___'))
        self.assertTrue(is_horizontal_rule('____'))

    def test_with_spaces(self):
        self.assertTrue(is_horizontal_rule('- - -'))
        self.assertTrue(is_horizontal_rule('* * * *'))
        self.assertTrue(is_horizontal_rule('_ _ _'))

    def test_leading_trailing_whitespace(self):
        self.assertTrue(is_horizontal_rule('  ---  '))

    def test_not_horizontal_rule_two_chars(self):
        self.assertFalse(is_horizontal_rule('--'))
        self.assertFalse(is_horizontal_rule('**'))
        self.assertFalse(is_horizontal_rule('__'))

    def test_not_horizontal_rule_text(self):
        self.assertFalse(is_horizontal_rule('not a rule'))
        self.assertFalse(is_horizontal_rule('- not a rule'))

    def test_empty_string(self):
        self.assertFalse(is_horizontal_rule(''))
        self.assertFalse(is_horizontal_rule('   '))


class TestIsTableRow(unittest.TestCase):
    def test_pipe_present(self):
        self.assertTrue(is_table_row('| col1 | col2 |'))
        self.assertTrue(is_table_row('col1 | col2'))

    def test_no_pipe(self):
        self.assertFalse(is_table_row('col1 col2'))
        self.assertFalse(is_table_row(''))

    def test_pipe_in_text(self):
        self.assertTrue(is_table_row('value | another'))


class TestIsTableSeparator(unittest.TestCase):
    def test_standard_separator(self):
        self.assertTrue(is_table_separator('|---|---|'))
        self.assertTrue(is_table_separator('| --- | --- |'))

    def test_with_colons(self):
        self.assertTrue(is_table_separator('|:---|:---:|'))
        self.assertTrue(is_table_separator('| ---: | ---|'))
        self.assertTrue(is_table_separator(':---:|:---:'))

    def test_no_leading_pipe(self):
        self.assertTrue(is_table_separator('---|---'))

    def test_single_column(self):
        self.assertFalse(is_table_separator('|---|'))
        self.assertFalse(is_table_separator('---'))

    def test_not_separator(self):
        self.assertFalse(is_table_separator('| col1 | col2 |'))
        self.assertFalse(is_table_separator('not a separator'))
        self.assertFalse(is_table_separator(''))


class TestConvertHeading(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(convert_heading('# Heading'), '* Heading')

    def test_h2(self):
        self.assertEqual(convert_heading('## Heading'), '*** Heading')

    def test_h3(self):
        self.assertEqual(convert_heading('### Heading'), '*** Heading')

    def test_h4(self):
        self.assertEqual(convert_heading('#### Heading'), '**** Heading')

    def test_h5(self):
        self.assertEqual(convert_heading('##### Heading'), '***** Heading')

    def test_h6(self):
        self.assertEqual(convert_heading('###### Heading'), '****** Heading')

    def test_no_space_after_hash_not_converted(self):
        self.assertEqual(convert_heading('#Heading'), '#Heading')

    def test_not_at_line_start(self):
        self.assertEqual(convert_heading('text # heading'), 'text # heading')

    def test_not_heading(self):
        self.assertEqual(convert_heading('plain text'), 'plain text')

    def test_heading_with_formatting(self):
        self.assertEqual(convert_heading('## **bold** text'), '*** **bold** text')


class TestConvertUnorderedList(unittest.TestCase):
    def test_hyphen_list(self):
        self.assertEqual(convert_unordered_list('- item'), '\u30fb item')

    def test_asterisk_list(self):
        self.assertEqual(convert_unordered_list('* item'), '\u30fb item')

    def test_plus_list(self):
        self.assertEqual(convert_unordered_list('+ item'), '\u30fb item')

    def test_with_indentation(self):
        self.assertEqual(convert_unordered_list('  - item'), '  \u30fb item')
        self.assertEqual(convert_unordered_list('    * item'), '    \u30fb item')

    def test_not_list(self):
        self.assertEqual(convert_unordered_list('plain text'), 'plain text')

    def test_no_space_after_marker_not_list(self):
        self.assertEqual(convert_unordered_list('-item'), '-item')

    def test_not_greedy_with_multiple_hyphens(self):
        self.assertEqual(convert_unordered_list('---'), '---')


class TestConvertBold(unittest.TestCase):
    def test_double_asterisk(self):
        self.assertEqual(convert_bold('**bold**'), "''bold''")

    def test_double_underscore(self):
        self.assertEqual(convert_bold('__bold__'), "''bold''")

    def test_inline_in_sentence(self):
        self.assertEqual(convert_bold('this is **bold** text'), "this is ''bold'' text")

    def test_multiple_bold(self):
        self.assertEqual(convert_bold('**a** and **b**'), "''a'' and ''b''")

    def test_no_bold(self):
        self.assertEqual(convert_bold('plain text'), 'plain text')

    def test_single_asterisk_unchanged(self):
        self.assertEqual(convert_bold('*italic*'), '*italic*')

    def test_single_underscore_unchanged(self):
        self.assertEqual(convert_bold('_italic_'), '_italic_')


class TestConvertInlineCode(unittest.TestCase):
    def test_backtick_code(self):
        self.assertEqual(convert_inline_code('`code`'), '"code"')

    def test_inline_in_sentence(self):
        self.assertEqual(convert_inline_code('use `foo()` to call'), 'use "foo()" to call')

    def test_no_code(self):
        self.assertEqual(convert_inline_code('plain text'), 'plain text')

    def test_empty_backticks(self):
        self.assertEqual(convert_inline_code('``'), '``')


class TestConvertLinks(unittest.TestCase):
    def test_basic_link(self):
        self.assertEqual(convert_links('[text](url)'), 'text')

    def test_link_in_sentence(self):
        self.assertEqual(convert_links('see [docs](http://a.com) here'), 'see docs here')

    def test_multiple_links(self):
        self.assertEqual(convert_links('[a](1) and [b](2)'), 'a and b')

    def test_image_passthrough(self):
        self.assertEqual(convert_links('![alt](url)'), '![alt](url)')

    def test_image_and_link_mixed(self):
        self.assertEqual(convert_links('![img](a) and [link](b)'), '![img](a) and link')

    def test_no_link(self):
        self.assertEqual(convert_links('plain text'), 'plain text')

    def test_empty_string(self):
        self.assertEqual(convert_links(''), '')


class TestConvertLine(unittest.TestCase):
    def test_heading_line(self):
        self.assertEqual(convert_line('# Title'), '* Title')

    def test_list_line(self):
        self.assertEqual(convert_line('- item'), '\u30fb item')

    def test_bold_in_plain_line(self):
        self.assertEqual(convert_line('**hello** world'), "''hello'' world")

    def test_code_in_plain_line(self):
        self.assertEqual(convert_line('run `cmd` now'), 'run "cmd" now')

    def test_bold_and_code_together(self):
        self.assertEqual(convert_line('**foo** `bar`'), "''foo'' \"bar\"")

    def test_plain_line_unchanged(self):
        self.assertEqual(convert_line('just text'), 'just text')

    def test_link_in_line(self):
        self.assertEqual(convert_line('[click](url) here'), 'click here')

    def test_image_in_line(self):
        self.assertEqual(convert_line('see ![img](url) now'), 'see ![img](url) now')


class TestConvertMarkdownToBacklog(unittest.TestCase):
    def test_headings(self):
        md = '# H1\n## H2\n### H3'
        expected = '* H1\n*** H2\n*** H3'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_unordered_list(self):
        md = '- item1\n- item2'
        expected = '\u30fb item1\n\u30fb item2'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_nested_list(self):
        md = '- parent\n  - child'
        expected = '\u30fb parent\n  \u30fb child'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_bold(self):
        md = 'this is **bold** text'
        expected = "this is ''bold'' text"
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_inline_code(self):
        md = 'use `foo()` function'
        expected = 'use "foo()" function'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_horizontal_rule(self):
        md = 'before\n---\nafter'
        expected = 'before\n**\nafter'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_fenced_code_block(self):
        md = '```python\nx = 1\nprint(x)\n```'
        expected = '{code}\npython\nx = 1\nprint(x)\n{/code}'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_fenced_code_without_lang(self):
        md = '```\nplain\n```'
        expected = '{code}\nplain\n{/code}'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_quote_block(self):
        md = '> quoted text\n> more quote'
        expected = '{quote}\nquoted text\nmore quote\n{/quote}'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_quote_with_formatting(self):
        md = '> **bold** in quote\n> `code` in quote'
        expected = "{quote}\n''bold'' in quote\n\"code\" in quote\n{/quote}"
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_table_with_header(self):
        md = '| Name | Age |\n|------|-----|\n| John | 30  |'
        expected = '| ''Name'' | ''Age'' |h\n| John | 30  |'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_table_header_without_leading_pipe(self):
        md = '**Name** | **Age**\n---|---\nJohn | 30'
        expected = "''Name'' | ''Age''|h\nJohn | 30"
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_empty_lines_removed(self):
        md = 'line1\n\nline2'
        expected = 'line1\nline2'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_full_document(self):
        md = '# Title\n\n## Section\n\nSome **bold** and `code`.\n\n- item1\n- item2\n\n---\n\n```python\nx = 1\n```\n\n> quoted'
        expected = (
            '* Title\n'
            '*** Section\n'
            "Some ''bold'' and \"code\".\n"
            '\u30fb item1\n'
            '\u30fb item2\n'
            '**\n'
            '{code}\n'
            'python\n'
            'x = 1\n'
            '{/code}\n'
            '{quote}\n'
            'quoted\n'
            '{/quote}'
        )
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_orphan_table_separator_skipped(self):
        md = 'some text\n---|---\nmore text'
        expected = 'some text\nmore text'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_heading_with_bold_and_code(self):
        md = '# **Title** with `code`'
        expected = "* ''Title'' with \"code\""
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_list_with_bold_and_code(self):
        md = '- **important** `item`'
        expected = "\u30fb ''important'' \"item\""
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_link_conversion(self):
        md = 'see [docs](url) here'
        expected = 'see docs here'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_image_passthrough(self):
        md = '![logo](img.png) stays'
        expected = '![logo](img.png) stays'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_link_inside_heading(self):
        md = '# [Home](/) page'
        expected = '* Home page'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_link_inside_list(self):
        md = '- [docs](http://x) for help'
        expected = '\u30fb docs for help'
        self.assertEqual(convert_markdown_to_backlog(md), expected)

    def test_image_in_heading(self):
        md = '# ![logo](img.png) Title'
        expected = '* ![logo](img.png) Title'
        self.assertEqual(convert_markdown_to_backlog(md), expected)


if __name__ == '__main__':
    unittest.main()
