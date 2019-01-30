import json
import unittest

from pathvariance.runs import ParseError, Step, parse_export


class TestParseExport(unittest.TestCase):
    def test_object_shape(self):
        data = {
            "task": "t",
            "runs": [{"run_id": "r1", "steps": [{"tool": "a"}]}],
        }
        export = parse_export(data)
        self.assertEqual(export.task, "t")
        self.assertEqual(len(export), 1)
        self.assertEqual(export.runs[0].tools(), ("a",))

    def test_bare_list_needs_default_task(self):
        data = [{"run_id": "r1", "steps": [{"tool": "a"}]}]
        export = parse_export(data)
        self.assertEqual(export.task, "task")

    def test_task_override(self):
        data = [{"steps": [{"tool": "a"}]}]
        export = parse_export(data, task="custom")
        self.assertEqual(export.task, "custom")

    def test_arguments_alias_accepted(self):
        data = {
            "task": "t",
            "runs": [{"steps": [{"tool": "a", "arguments": {"k": 1}}]}],
        }
        export = parse_export(data)
        self.assertEqual(export.runs[0].steps[0].args, {"k": 1})

    def test_missing_tool_raises(self):
        data = {"task": "t", "runs": [{"steps": [{"args": {}}]}]}
        with self.assertRaises(ParseError):
            parse_export(data)

    def test_non_dict_args_raises(self):
        data = {"task": "t", "runs": [{"steps": [{"tool": "a", "args": 3}]}]}
        with self.assertRaises(ParseError):
            parse_export(data)

    def test_missing_task_raises(self):
        with self.assertRaises(ParseError):
            parse_export({"runs": [{"steps": [{"tool": "a"}]}]})

    def test_empty_runs_raises(self):
        with self.assertRaises(ParseError):
            parse_export({"task": "t", "runs": []})

    def test_generated_run_id(self):
        data = {"task": "t", "runs": [{"steps": [{"tool": "a"}]}]}
