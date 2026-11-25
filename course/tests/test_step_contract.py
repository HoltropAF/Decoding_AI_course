"""Run with python -m unittest discover -s course/tests."""
from copy import deepcopy
import unittest

from course.build_dashboard import STEP_CONTRACT, MODULES, build_module, validate_steps


class StepContract(unittest.TestCase):
    def setUp(self):
        self.chapter = {
            "kind": "doc", "key": "guide", "label": "Chapter", "phase": "learn",
            "doc": {"title": "Lesson", "path": "chapter.md", "md": "# Lesson"},
        }

    def validate(self, *steps, contract=STEP_CONTRACT):
        validate_steps([{"id": "fixture", "steps": list(steps)}], contract)

    def test_current_course_satisfies_contract(self):
        validate_steps([build_module(module) for module in MODULES], STEP_CONTRACT)

    def test_another_kind_can_reuse_a_registered_renderer(self):
        contract = deepcopy(STEP_CONTRACT)
        contract["kinds"]["reading"] = contract["kinds"]["doc"]
        self.validate({**self.chapter, "kind": "reading"}, contract=contract)
        self.assertEqual(contract["kinds"]["reading"], "chapter")

    def test_kind_must_name_a_renderer_declared_by_the_contract(self):
        contract = deepcopy(STEP_CONTRACT)
        contract["kinds"]["doc"] = "typo"
        with self.assertRaisesRegex(SystemExit, "unknown renderer"):
            self.validate(self.chapter, contract=contract)

    def test_unknown_kind_and_phase_fail_with_step_context(self):
        for changes, message in [
            ({"kind": "unknown"}, "unknown step kind"),
            ({"phase": "unknown"}, "unknown step phase"),
            ({"phase": []}, "unknown step phase"),
        ]:
            with self.subTest(changes=changes), self.assertRaisesRegex(SystemExit, f"fixture step 1.*{message}"):
                self.validate(self.chapter | changes)

    def test_invalid_document_payload_and_optional_fields_fail(self):
        test_cases = [
            (self.chapter | {"doc": {"title": "Missing path"}}, "doc must be document"),
            (self.chapter | {"kind": "docs", "docs": []}, "docs must be documents"),
            (self.chapter | {"kind": "docs", "docs": [self.chapter["doc"]], "toggles": "yes"}, "toggles must be boolean"),
            (self.chapter | {"kind": "slides", "path": "slides.md", "md": "# slide", "recap": "yes"}, "recap must be boolean"),
        ]
        for step, message in test_cases:
            with self.subTest(step=step), self.assertRaisesRegex(SystemExit, message):
                self.validate(step)

    def test_duplicate_and_unsafe_route_keys_fail(self):
        with self.assertRaisesRegex(SystemExit, "step key must be unique and URL-safe"):
            self.validate(self.chapter, self.chapter)
        with self.assertRaisesRegex(SystemExit, "step key must be unique and URL-safe"):
            self.validate(self.chapter | {"key": "nested.route"})


if __name__ == "__main__":
    unittest.main()
