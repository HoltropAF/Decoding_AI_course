"""Run from the repository root with python -m unittest discover -s course/tests."""
import unittest

from course.build_dashboard import h2_sections, parse_self_check, section


class MarkdownSections(unittest.TestCase):
    def test_extraction_and_indexing_skip_fenced_headings(self):
        text = "\n".join([
            "# Chapter", "## First", "\x60\x60\x60\x60markdown", "## Exercise: inside",
            "\x60\x60\x60", "## Exercise: still inside", "~~~~", "## Still inside",
            "\x60\x60\x60\x60", "## Exercise: actual", "Instructions.", "~~~js", "## Inside tilde",
            "~~~~", "## Last", "The end.",
        ])
        self.assertEqual([title for title, _ in h2_sections(text)], ["First", "Exercise: actual", "Last"])
        self.assertTrue(section(text, r"Exercise").startswith("## Exercise: actual\n"))
        self.assertIn("## Inside tilde", section(text, r"Exercise"))

    def test_done_when_keeps_ids_when_items_move_or_labels_change(self):
        original = "## Done when\n\n- [ ] Old wording <!-- checklist:m1-0 -->\n- [ ] Another <!-- checklist:m1-1 -->"
        changed = "## Done when\n\n- [ ] Another <!-- checklist:m1-1 -->\n- [ ] New wording <!-- checklist:m1-0 -->"
        self.assertEqual([item["id"] for item in parse_self_check(original, "m1")["done"]], ["m1-0", "m1-1"])
        self.assertEqual(parse_self_check(changed, "m1")["done"], [
            {"id": "m1-1", "text": "Another"}, {"id": "m1-0", "text": "New wording"},
        ])

    def test_done_when_requires_unique_ids(self):
        text = "## Done when\n\n- [ ] One <!-- checklist:m1-0 -->\n- [ ] Two <!-- checklist:m1-0 -->"
        with self.assertRaisesRegex(SystemExit, "unique checklist ID"):
            parse_self_check(text, "m1")


if __name__ == "__main__":
    unittest.main()
