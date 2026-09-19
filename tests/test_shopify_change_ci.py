import tempfile
import unittest
from pathlib import Path

from shopify_change_ci import scan, write_report


class ShopifyChangeCITests(unittest.TestCase):
    def test_detects_high_risk_legacy_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app.ts").write_text(
                'const version = "2024-10";\nfetch("/admin/api/2024-10/products.json");\n',
                encoding="utf-8",
            )
            findings = scan(root)
            rules = {f["rule"] for f in findings}
            self.assertIn("old-api-version", rules)
            self.assertIn("rest-admin-products", rules)
            self.assertTrue(any(f["severity"] == "high" for f in findings))

    def test_detects_september_2026_events_breaking_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "events.ts").write_text(
                'const eventId = headers.get("shopify-event-id");\n'
                'payload.fields_changed.forEach(handleField);\n',
                encoding="utf-8",
            )
            rules = {f["rule"] for f in scan(root)}
            self.assertIn("events-removed-id-header", rules)
            self.assertIn("events-fields-changed-array", rules)

    def test_accepts_new_fields_changed_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "events.ts").write_text(
                'for (const field of payload.fields_changed.updated) handleField(field);\n',
                encoding="utf-8",
            )
            self.assertNotIn("events-fields-changed-array", {f["rule"] for f in scan(root)})

    def test_ignores_vendor_and_node_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ("node_modules", "vendor", "dist", "build"):
                target = root / folder
                target.mkdir()
                (target / "legacy.js").write_text('const v = "2024-10";', encoding="utf-8")
            self.assertEqual(scan(root), [])

    def test_report_groups_duplicate_root_causes(self):
        findings = [
            {"rule": "legacy-price-rule", "severity": "high", "file": "a.ts", "line": 1,
             "message": "Legacy PriceRule surface detected; verify against the target Shopify API release.", "excerpt": "PriceRule"},
            {"rule": "legacy-price-rule", "severity": "high", "file": "b.ts", "line": 2,
             "message": "Legacy PriceRule surface detected; verify against the target Shopify API release.", "excerpt": "priceRule"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            write_report(findings, report)
            text = report.read_text(encoding="utf-8")
            self.assertIn("**Overall risk:** HIGH", text)
            self.assertIn("**Root-cause risks:** 1 (1 high, 0 medium)", text)
            self.assertIn("**Affected locations:** 2", text)

    def test_clean_repo_produces_low_risk_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app.ts").write_text("const healthy = true;", encoding="utf-8")
            findings = scan(root)
            report = root / "report.md"
            write_report(findings, report)
            text = report.read_text(encoding="utf-8")
            self.assertEqual(findings, [])
            self.assertIn("**Overall risk:** LOW", text)
            self.assertIn("No configured compatibility risks were detected.", text)


if __name__ == "__main__":
    unittest.main()
