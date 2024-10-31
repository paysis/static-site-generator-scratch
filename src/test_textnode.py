import unittest

from textnode import TextType, TextNode

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

if __name__ == "__main__":
    unittest.main()