import unittest
from inline_markdown import split_nodes_delimiter, TextNode, TextType, extract_markdown_images, extract_markdown_links, split_nodes_image_or_link

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

class TestExtractor(unittest.TestCase):
    def test_given_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        ret = extract_markdown_images(text)
        self.assertIsInstance(ret, list)
        self.assertIn(('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ret)
        self.assertIn(('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg'), ret)

    def test_given_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        ret = extract_markdown_links(text)
        self.assertIsInstance(ret, list)
        self.assertIn(("to youtube", "https://www.youtube.com/@bootdotdev"), ret)
        self.assertIn(("to boot dev", "https://www.boot.dev"), ret)

    def test_given_links_split_success(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image_or_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ])
    
    def test_given_images_split_success(self):
        node = TextNode(
            "This is text with a image ![alt](https://a.c/a.jpg) and ![another alt](https://penguin.com/a.jpg)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image_or_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://a.c/a.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another alt", TextType.IMAGE, "https://penguin.com/a.jpg")
        ])

    def test_given_both_link_and_image_split_success(self):
        node = TextNode(
            "This is text with both link and image [click here](https://a.c/account) and ![another alt](https://penguin.com/a.jpg)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image_or_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with both link and image ", TextType.TEXT),
            TextNode("click here", TextType.LINK, "https://a.c/account"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another alt", TextType.IMAGE, "https://penguin.com/a.jpg")
        ])

if __name__ == "__main__":
    unittest.main()