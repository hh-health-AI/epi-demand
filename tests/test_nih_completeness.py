import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import nih_reporter as nih


class NIHTests(unittest.TestCase):
    def invoke(self, pages, cap=2):
        out = io.StringIO()
        with patch.object(nih, "post", side_effect=pages), \
             patch.object(sys, "argv", ["nih", "--fiscal-years", "2025", "--limit", str(cap), "--summarise"]), \
             contextlib.redirect_stdout(out):
            try:
                nih.main()
            except SystemExit:
                self.assertEqual(out.getvalue(), "")
                raise
        return json.loads(out.getvalue())

    def test_capped_query_has_no_summary(self):
        with self.assertRaises(SystemExit):
            self.invoke([{"meta": {"total": 3}, "results": []}])

    def test_incomplete_pages_and_missing_total_fail(self):
        for pages in [[{"meta": {"total": 2}, "results": []}], [{"results": []}]]:
            with self.assertRaises(SystemExit):
                self.invoke(pages)

    def test_complete_total_is_disclosed(self):
        rows = [{"fiscal_year": 2025, "award_amount": 10}, {"fiscal_year": 2025, "award_amount": 20}]
        result = self.invoke([{"meta": {"total": 2}, "results": rows}])
        self.assertEqual(result["coverage"], {"matched": 2, "fetched": 2, "truncated": False})
        self.assertEqual(result["by_fiscal_year"][0]["award_usd"], 30)

    def test_changed_total_fails(self):
        with self.assertRaises(SystemExit):
            self.invoke([{"meta": {"total": 2}, "results": [{"fiscal_year": 2025}]},
                         {"meta": {"total": 1}, "results": []}])


if __name__ == "__main__":
    unittest.main()
