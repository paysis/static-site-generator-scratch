import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode

class TestBlockMarkdown(unittest.TestCase):
    def test_success(self):
        text = \
"""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        sections = markdown_to_blocks(text)
        self.assertEqual(sections, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n" \
            "* This is a list item\n" \
            "* This is another list item"
        ])

    def test_multi_line_break(self):
        text = \
"""# This is a heading


This is a paragraph of text. It has some **bold** and *italic* words inside of it.





* This is the first list item in a list block
* This is a list item
* This is another list item"""
        sections = markdown_to_blocks(text)
        self.assertEqual(sections, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n" \
            "* This is a list item\n" \
            "* This is another list item"
        ])

    def test_block_type_paragraph(self):
        block = "Some text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_headings(self):
        test_cases = [
            "# h1",
            "## h2",
            "### h3",
            "#### h4",
            "##### h5",
            "###### h6"
        ]
        for test_case in test_cases:
            block_type = block_to_block_type(test_case)
            self.assertEqual(block_type, BlockType.HEADING)
    
    def test_code_blocks_type(self):
        block = "```\nprint(\"hello world\")\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote_type(self):
        block = "> quote unquote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list(self):
        test_cases = [
            "* food\n* fish\n* dish",
            "- dang\n- bang\n- bang bang\n- hello"
        ]
        for test_case in test_cases:
            block_type = block_to_block_type(test_case)
            self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        test_cases = [
            "1. A\n2. B\n3. C\n4. D",
            "1. A A A\n2. B A A"
        ]
        for test_case in test_cases:
            block_type = block_to_block_type(test_case)
            self.assertEqual(block_type, BlockType.ORDERED_LIST)

class MarkdownToHtmlTest(unittest.TestCase):
    def test_markdown_to_html_heading_and_paragraph(self):
        text = "# big title\n\nthis is some text\n"
        node = markdown_to_html_node(text)
        t = ParentNode("div", [
            ParentNode("h1", [
                LeafNode(None, "big title")
            ]),
            ParentNode("p", [
                LeafNode(None, "this is some text")
            ])
        ])
        self.assertEqual(node, t)

    def test_markdown_to_html_code_and_quote_and_multi_heading(self):
        text = "# big title\n\nthis is some text\n\n> this `is` quote\n\n## second title\n\n```\na big chunk of code\n```\n\n"
        node = markdown_to_html_node(text)
        t = ParentNode("div", [
            ParentNode("h1", [
                LeafNode(None, "big title")
            ]),
            ParentNode("p", [
                LeafNode(None, "this is some text")
            ]),
            ParentNode("blockquote", [
                LeafNode(None, "this "),
                LeafNode("code", "is"),
                LeafNode(None, " quote")
            ]),
            ParentNode("h2", [
                LeafNode(None, "second title")
            ]),
            ParentNode("pre", [
                ParentNode("code", [
                    LeafNode(None, "a big chunk of code")
                ])
            ])
        ])
        self.assertEqual(node, t)


if __name__ == "__main__":
    unittest.main()