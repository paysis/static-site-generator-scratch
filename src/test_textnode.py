import unittest

from textnode import TextType, TextNode, text_node_to_html_node

from enum import Enum
class EvilEnum(Enum):
    EVIL = "evil"

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_when_url_is_none(self):
        node = TextNode("This is a text node", TextType.ITALIC, url = None)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_when_text_is_different_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_same_images_are_equal(self):
        node = TextNode("A penguin", TextType.IMAGE, url="http://x.x/penguin")
        node2 = TextNode("A penguin", TextType.IMAGE, url="http://x.x/penguin")
        self.assertEqual(node, node2)

    def test_given_text_success(self):
        node = TextNode("some text", TextType.TEXT)
        ret = text_node_to_html_node(node)
        self.assertEqual(ret.to_html(), "some text")

    def test_given_bold_success(self):
        node = TextNode("some text", TextType.BOLD)
        ret = text_node_to_html_node(node)
        self.assertEqual(ret.to_html(), "<b>some text</b>")

    def test_given_italic_success(self):
        node = TextNode("some text", TextType.ITALIC)
        ret = text_node_to_html_node(node)
        self.assertEqual(ret.to_html(), "<i>some text</i>")

    def test_given_code_success(self):
        node = TextNode("some code", TextType.CODE)
        ret = text_node_to_html_node(node)
        self.assertEqual(ret.to_html(), "<code>some code</code>")

    def test_given_link_success(self):
        node = TextNode("my profile", TextType.LINK, "https://github.com/paysis")
        ret = text_node_to_html_node(node)
        self.assertEqual(ret.to_html(), "<a href=\"https://github.com/paysis\">my profile</a>")

    def test_given_image_success(self):
        node = TextNode("a penguin", TextType.IMAGE, "https://penguin.com/a.jpg")
        ret = text_node_to_html_node(node)
        try:
            self.assertEqual(ret.to_html(), "<img src=\"https://penguin.com/a.jpg\" alt=\"a penguin\"></img>")
        except:
            self.assertEqual(ret.to_html(), "<img alt=\"a penguin\" src=\"https://penguin.com/a.jpg\"></img>")

    def test_given_non_existant_type_fail(self):
        node = TextNode("some text", EvilEnum.EVIL)
        with self.assertRaises(Exception):
            ret = text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()