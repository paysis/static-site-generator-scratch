import unittest
from delimiter import split_nodes_delimiter, TextNode, TextType

class TestDelimiter(unittest.TestCase):
    def test_default_given_case(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ])
    
    def test_given_multiple_parts_success(self):
        node = TextNode("This is a text with two `code` and `blocks` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with two ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("blocks", TextType.CODE),
            TextNode(" here", TextType.TEXT)
        ])

    def test_given_nested_not_equal_since_not_supported_yet(self):
        node = TextNode("This is *italic and **bold** text* here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertNotEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic and **bold** text", TextType.ITALIC),
            TextNode(" here", TextType.TEXT)
        ])

if __name__ == "__main__":
    unittest.main()