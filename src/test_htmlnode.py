import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_works(self):
        node = HTMLNode("p", "some text", props={ "style": "color: black;" })
        self.assertEqual(node.props_to_html(), " style=\"color: black;\"")
    
    def test_multiple_props_to_html_works(self):
        node = HTMLNode("p", "some text", props={ "style": "color: black;", "class": "bold-text" })
        self.assertEqual(node.props_to_html(), " style=\"color: black;\" class=\"bold-text\"")

    def test_when_props_is_none(self):
        node = HTMLNode("p", "some text")
        self.assertEqual(node.props_to_html(), "")

    def test_when_both_value_and_children_are_none_should_fail(self):
        with self.assertRaises(Exception):
            node = HTMLNode("p")

if __name__ == "__main__":
    unittest.main()