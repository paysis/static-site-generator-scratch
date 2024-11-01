import unittest

from markdown_util import extract_title

class TestMarkdownUtil(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Hello"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello")

    def test_spaced_title(self):
        markdown = "# Hello World   "
        title = extract_title(markdown)
        self.assertEqual(title, "Hello World")

    def test_multiline_title(self):
        markdown = "# Hello World \n\nthis is some text\n"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello World")

if __name__ == "__main__":
    unittest.main()