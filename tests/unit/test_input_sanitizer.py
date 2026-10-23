import unittest
from codepilot.security.input_sanitizer import InputSanitizer

class TestInputSanitizer(unittest.TestCase):
    def test_script_tag_removal(self):
        raw = "Hello <script>alert('xss')</script>World"
        clean = InputSanitizer.sanitize_text(raw)
        self.assertEqual(clean, "Hello World")

    def test_event_attribute_removal(self):
        raw = '<div onclick="stealCookies()">Click me</div>'
        clean = InputSanitizer.sanitize_text(raw)
        self.assertNotIn("onclick", clean)

    def test_javascript_protocol(self):
        raw = '<a href="javascript:alert(1)">Link</a>'
        clean = InputSanitizer.sanitize_text(raw)
        self.assertNotIn("javascript:", clean)

    def test_html_escape(self):
        raw = '<b>"Bold" & Strong</b>'
        esc = InputSanitizer.escape_html(raw)
        self.assertIn("&amp;", esc)
        self.assertIn("&quot;", esc)

if __name__ == "__main__":
    unittest.main()
