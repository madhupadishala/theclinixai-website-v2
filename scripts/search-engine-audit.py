#!/usr/bin/env python3
"""Audit static search-engine readiness and emit a machine-readable report."""

from __future__ import annotations

import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"404.html", "header.html", "footer.html"}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    pages = []
    for path in sorted(ROOT.rglob("*.html")):
        relative = path.relative_to(ROOT).as_posix()
        if relative in EXCLUDE:
            continue
        source = path.read_text(encoding="utf-8")
        checks = {
            "title": bool(re.search(r"<title>.+?</title>", source, re.S)),
            "description": 'name="description"' in source,
            "canonical": 'rel="canonical"' in source,
            "robots": 'name="robots"' in source,
            "h1": len(re.findall(r"<h1(?:\s|>)", source)) == 1,
            "schema": "application/ld+json" in source,
            "og_title": 'property="og:title"' in source,
            "og_description": 'property="og:description"' in source,
        }
        for name, passed in checks.items():
            if not passed:
                errors.append(f"{relative}: missing or invalid {name}")
        pages.append({"path": relative, **checks})

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: https://www.theclinixai.com/sitemap.xml" not in robots:
        errors.append("robots.txt: canonical sitemap declaration missing")

    sitemap_path = ROOT / "sitemap.xml"
    root = ET.parse(sitemap_path).getroot()
    sitemap_urls = {
        node.text
        for node in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if node.text
    }
    canonical_urls = set()
    for page in pages:
        source = (ROOT / page["path"]).read_text(encoding="utf-8")
        match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', source)
        if match:
            canonical_urls.add(match.group(1))
    missing = sorted(canonical_urls - sitemap_urls)
    extra = sorted(sitemap_urls - canonical_urls)
    if missing:
        errors.append(f"sitemap.xml: missing canonical URLs: {missing}")
    if extra:
        warnings.append(f"sitemap.xml: URLs without matching canonical: {extra}")

    report = {
        "pages_checked": len(pages),
        "canonical_urls": len(canonical_urls),
        "sitemap_urls": len(sitemap_urls),
        "errors": errors,
        "warnings": warnings,
        "pages": pages,
    }
    (ROOT / "search-engine-readiness-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps({key: report[key] for key in ("pages_checked", "canonical_urls", "sitemap_urls", "errors", "warnings")}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
