import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_works_no_props(self):
        node = LeafNode("p", "some text")
        self.assertEqual(node.to_html(), "<p>some text</p>")
    
    def test_works_with_single_prop(self):
        node = LeafNode("p", "some text", props={ "style": "color: black;" })
        self.assertEqual(node.to_html(), "<p style=\"color: black;\">some text</p>")

    def test_works_with_multi_props(self):
        node = LeafNode("p", "some text", props={ "style": "color: black;", "class": "bold-text" })
        self.assertEqual(node.to_html(), "<p style=\"color: black;\" class=\"bold-text\">some text</p>")

    def test_fail_when_no_value(self):
        with self.assertRaises(Exception):
            node = LeafNode("p", None)

    def test_raw_value_when_no_tag(self):
        node = LeafNode(None, "some text")
        self.assertEqual(node.to_html(), "some text")


if __name__ == "__main__":
    unittest.main()