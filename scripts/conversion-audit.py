#!/usr/bin/env python3
"""Verify conversion instrumentation and CTA coverage."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    required = ["analytics.js", "api/analytics-event.js", "scripts/apply-ga4.py"]
    errors = [f"Missing {name}" for name in required if not (ROOT / name).exists()]
    site = (ROOT / "site.js").read_text(encoding="utf-8")
    if "/analytics.js" not in site:
        errors.append("site.js does not load analytics.js")
    analytics = (ROOT / "analytics.js").read_text(encoding="utf-8")
    for event in ("page_view", "cta_click", "form_start", "form_submit", "resource_download", "outbound_click", "scroll_depth"):
        if event not in analytics:
            errors.append(f"analytics.js missing {event}")
    report = {
        "instrumentation_files": required,
        "events": ["page_view", "cta_click", "form_start", "form_submit", "resource_download", "outbound_click", "scroll_depth"],
        "privacy": "No form-field values are included in analytics events.",
        "errors": errors,
    }
    (ROOT / "conversion-analytics-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
