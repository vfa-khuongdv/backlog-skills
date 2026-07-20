#!/usr/bin/env python3
import unittest

from convert import (
    is_horizontal_rule,
    is_table_row,
    is_table_separator,
    convert_heading,
    convert_bold,
    convert_italic,
    convert_strikethrough,
    convert_bold_italic,
    convert_link,
    convert_image,
    convert_inline_formatting,
    convert_markdown_to_google_chat,
    table_row_to_cells,
    table_cells_to_kv,
)


class TestConvertHeading(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(convert_heading('# Heading'), '*Heading*')

    def test_h2(self):
        self.assertEqual(convert_heading('## Heading'), '*Heading*')

    def test_h3(self):
        self.assertEqual(convert_heading('### Heading'), '*Heading*')

    def test_heading_with_bold(self):
        self.assertEqual(convert_heading('# **Bold** Title'), '*Bold Title*')

    def test_no_space_after_hash_not_converted(self):
        self.assertEqual(convert_heading('#Heading'), '#Heading')

    def test_not_heading(self):
        self.assertEqual(convert_heading('plain text'), 'plain text')

    def test_not_at_line_start(self):
        self.assertEqual(convert_heading('text # heading'), 'text # heading')


class TestConvertBold(unittest.TestCase):
    def test_double_asterisk(self):
        self.assertEqual(convert_bold('**bold**'), '*bold*')

    def test_double_underscore(self):
        self.assertEqual(convert_bold('__bold__'), '*bold*')

    def test_in_sentence(self):
        self.assertEqual(convert_bold('this is **bold** text'), 'this is *bold* text')

    def test_multiple_bold(self):
        self.assertEqual(convert_bold('**a** and **b**'), '*a* and *b*')

    def test_no_bold(self):
        self.assertEqual(convert_bold('plain text'), 'plain text')

    def test_single_asterisk_unchanged(self):
        self.assertEqual(convert_bold('*italic*'), '*italic*')


class TestConvertItalic(unittest.TestCase):
    def test_single_asterisk(self):
        self.assertEqual(convert_italic('*italic*'), '_italic_')

    def test_in_sentence(self):
        self.assertEqual(convert_italic('this is *italic* text'), 'this is _italic_ text')

    def test_underscore_unchanged(self):
        self.assertEqual(convert_italic('_italic_'), '_italic_')

    def test_no_italic(self):
        self.assertEqual(convert_italic('plain text'), 'plain text')

    def test_double_asterisk_not_treated_as_italic(self):
        self.assertEqual(convert_italic('**bold**'), '**bold**')


class TestConvertStrikethrough(unittest.TestCase):
    def test_double_tilde(self):
        self.assertEqual(convert_strikethrough('~~struck~~'), '~struck~')

    def test_in_sentence(self):
        self.assertEqual(convert_strikethrough('this is ~~old~~ text'), 'this is ~old~ text')

    def test_no_strikethrough(self):
        self.assertEqual(convert_strikethrough('plain text'), 'plain text')


class TestConvertBoldItalic(unittest.TestCase):
    def test_triple_asterisk(self):
        self.assertEqual(convert_bold_italic('***text***'), '_text_')

    def test_triple_underscore(self):
        self.assertEqual(convert_bold_italic('___text___'), '_text_')

    def test_in_sentence(self):
        self.assertEqual(convert_bold_italic('this is ***bold italic*** here'), 'this is _bold italic_ here')

    def test_no_match(self):
        self.assertEqual(convert_bold_italic('**bold** *italic*'), '**bold** *italic*')


class TestConvertLink(unittest.TestCase):
    def test_basic_link(self):
        self.assertEqual(convert_link('[text](url)'), 'text (url)')

    def test_in_sentence(self):
        self.assertEqual(convert_link('see [docs](http://a.b) here'), 'see docs (http://a.b) here')

    def test_no_link(self):
        self.assertEqual(convert_link('plain text'), 'plain text')


class TestConvertImage(unittest.TestCase):
    def test_basic_image(self):
        self.assertEqual(convert_image('![alt](url)'), 'alt (url)')

    def test_empty_alt(self):
        self.assertEqual(convert_image('![](url)'), ' (url)')

    def test_no_image(self):
        self.assertEqual(convert_image('plain text'), 'plain text')


class TestConvertInlineFormatting(unittest.TestCase):
    def test_applies_all(self):
        result = convert_inline_formatting('**bold** *italic* ~~struck~~ [link](url) ![img](img.png)')
        expected = '*bold* _italic_ ~struck~ link (url) img (img.png)'
        self.assertEqual(result, expected)

    def test_bold_italic_inline_formatting(self):
        result = convert_inline_formatting('***bold italic*** text')
        expected = '_bold italic_ text'
        self.assertEqual(result, expected)

    def test_image_before_link(self):
        result = convert_inline_formatting('[text](url) ![](img.png)')
        expected = 'text (url)  (img.png)'
        self.assertEqual(result, expected)

    def test_url_with_special_chars_not_mangled(self):
        result = convert_inline_formatting('[docs](http://a*b*c.com)')
        expected = 'docs (http://a*b*c.com)'
        self.assertEqual(result, expected)

    def test_bold_inside_link(self):
        result = convert_inline_formatting('[**bold** link](url)')
        expected = '*bold* link (url)'
        self.assertEqual(result, expected)


class TestIsHorizontalRule(unittest.TestCase):
    def test_hyphens(self):
        self.assertTrue(is_horizontal_rule('---'))

    def test_asterisks(self):
        self.assertTrue(is_horizontal_rule('***'))

    def test_underscores(self):
        self.assertTrue(is_horizontal_rule('___'))

    def test_not_rule(self):
        self.assertFalse(is_horizontal_rule('not a rule'))
        self.assertFalse(is_horizontal_rule(''))


class TestIsTableRow(unittest.TestCase):
    def test_pipe_present(self):
        self.assertTrue(is_table_row('| a | b |'))

    def test_no_pipe(self):
        self.assertFalse(is_table_row('plain text'))


class TestIsTableSeparator(unittest.TestCase):
    def test_standard(self):
        self.assertTrue(is_table_separator('|---|---|'))

    def test_with_colons(self):
        self.assertTrue(is_table_separator('|:---|:---:|'))

    def test_not_separator(self):
        self.assertFalse(is_table_separator('| col1 | col2 |'))
        self.assertFalse(is_table_separator('plain'))


class TestTableRowToCells(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(table_row_to_cells('| a | b | c |'), ['a', 'b', 'c'])

    def test_without_leading_pipe(self):
        self.assertEqual(table_row_to_cells('a | b | c'), ['a', 'b', 'c'])

    def test_with_formatting(self):
        self.assertEqual(table_row_to_cells('| **bold** | `code` |'), ['*bold*', '`code`'])


class TestConvertMarkdownToGoogleChat(unittest.TestCase):
    def test_headings(self):
        md = '# Title\n## Section'
        expected = '*Title*\n*Section*'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_bold(self):
        md = 'this is **bold** text'
        expected = 'this is *bold* text'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_italic(self):
        md = 'this is *italic* text'
        expected = 'this is _italic_ text'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_strikethrough(self):
        md = 'this is ~~old~~ text'
        expected = 'this is ~old~ text'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_link(self):
        md = 'see [docs](http://example.com) here'
        expected = 'see docs (http://example.com) here'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_image(self):
        md = '![logo](img.png)'
        expected = 'logo (img.png)'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_unordered_list(self):
        md = '- item1\n- item2'
        expected = '- item1\n- item2'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_ordered_list(self):
        md = '1. first\n2. second'
        expected = '1. first\n2. second'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_fenced_code_block(self):
        md = '```python\nx = 1\nprint(x)\n```'
        expected = '```python\nx = 1\nprint(x)\n```'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_horizontal_rule_removed(self):
        md = 'before\n---\nafter'
        expected = 'before\nafter'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_blockquote(self):
        md = '> quoted text\n> more quote'
        expected = 'quoted text\nmore quote'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_blockquote_with_formatting(self):
        md = '> **bold** in quote'
        expected = '*bold* in quote'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_table(self):
        md = '| Name | Age |\n|------|-----|\n| John | 30  |'
        expected = 'Name: John, Age: 30'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_table_with_bold_header(self):
        md = '| **Name** | **Age** |\n|------|-----|\n| John | 30  |'
        expected = 'Name: John, Age: 30'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_empty_lines_removed(self):
        md = 'line1\n\nline2'
        expected = 'line1\n\nline2'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_multiple_empty_lines_collapsed(self):
        md = 'line1\n\n\n\nline2'
        expected = 'line1\n\nline2'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_full_document(self):
        md = (
            '# Release Notes\n\n'
            '## Features\n\n'
            'Added **new dashboard** with *improved* UI.\n\n'
            '- Item 1\n'
            '- Item 2\n\n'
            'See [docs](http://docs.example.com) for details.\n\n'
            '```js\nconsole.log("hello")\n```\n\n'
            '> Old feature ~~removed~~ deprecated.'
        )
        expected = (
            '*Release Notes*\n'
            '\n'
            '*Features*\n'
            '\n'
            'Added *new dashboard* with _improved_ UI.\n'
            '\n'
            '- Item 1\n'
            '- Item 2\n'
            '\n'
            'See docs (http://docs.example.com) for details.\n'
            '\n'
            '```js\n'
            'console.log("hello")\n'
            '```\n'
            '\n'
            'Old feature ~removed~ deprecated.'
        )
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_bold_italic_strikethrough_combined(self):
        md = '**bold** *italic* ~~struck~~ together'
        expected = '*bold* _italic_ ~struck~ together'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_bold_italic_triple_stars(self):
        md = '***bold italic*** text'
        expected = '_bold italic_ text'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_url_with_special_chars(self):
        md = 'see [docs](http://a*b*c.com) here'
        expected = 'see docs (http://a*b*c.com) here'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)

    def test_plus_list_marker(self):
        md = '+ item1\n+ item2'
        expected = '+ item1\n+ item2'
        self.assertEqual(convert_markdown_to_google_chat(md), expected)


if __name__ == '__main__':
    unittest.main()
