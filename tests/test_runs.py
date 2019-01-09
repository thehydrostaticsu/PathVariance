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
