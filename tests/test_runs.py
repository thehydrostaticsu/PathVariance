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
        export = parse_export(data)
        self.assertEqual(export.runs[0].run_id, "run000")

    def test_arg_signature_stable(self):
        s1 = Step(tool="a", args={"b": 1, "a": 2})
        s2 = Step(tool="a", args={"a": 2, "b": 1})
        self.assertEqual(s1.arg_signature(), s2.arg_signature())

    def test_bad_json_via_string(self):
        from pathvariance.runs import load_export

        with self.assertRaises(ParseError):
            load_export("{not json")

    def test_outcome_type_checked(self):
        data = {"task": "t", "runs": [{"outcome": "yes", "steps": [{"tool": "a"}]}]}
        with self.assertRaises(ParseError):
            parse_export(data)


if __name__ == "__main__":
    unittest.main()

# draft note 1383
