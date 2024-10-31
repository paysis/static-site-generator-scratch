import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_no_children(self):
        node = ParentNode("p")
        self.assertEqual(node.to_html(), "<p></p>")
    
    def test_single_child_as_parent_node(self):
        node = ParentNode("p", [
                ParentNode("a")
            ])
        self.assertEqual(node.to_html(), "<p><a></a></p>")
    
    def test_single_child_as_leaf_node(self):
        node = ParentNode("div", [
            LeafNode("p", "some text")
        ])
        self.assertEqual(node.to_html(), "<div><p>some text</p></div>")
    
    def test_children(self):
        child1 = LeafNode("p", "some text")
        child2 = LeafNode("a", "click here", { "href": "https://github.com" })
        node = ParentNode("div", [
            child1,
            child2
        ])
        self.assertEqual(node.to_html(), "<div><p>some text</p><a href=\"https://github.com\">click here</a></div>")

    def test_children_nested(self):
        child3 = LeafNode("i", "some text")
        child2 = ParentNode("b", [child3])
        child1 = ParentNode("p", [child2])
        node = ParentNode("div", [child1])
        self.assertEqual(node.to_html(), "<div><p><b><i>some text</i></b></p></div>")

if __name__ == "__main__":
    unittest.main()