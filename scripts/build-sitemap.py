#!/usr/bin/env python3
"""Build sitemap.xml from canonical URLs in public HTML pages."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"404.html", "header.html", "footer.html", "insights/index.html"}
CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)


def main() -> None:
    urls: set[str] = set()
    for page in ROOT.rglob("*.html"):
        relative = page.relative_to(ROOT).as_posix()
        if relative in EXCLUDED:
            continue
        match = CANONICAL_RE.search(page.read_text(encoding="utf-8"))
        if match:
            urls.add(match.group(1))

    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    root = ET.Element(f"{{{namespace}}}urlset")
    today = date.today().isoformat()
    for location in sorted(urls, key=lambda value: (value.count("/"), value)):
        node = ET.SubElement(root, f"{{{namespace}}}url")
        ET.SubElement(node, f"{{{namespace}}}loc").text = location
        ET.SubElement(node, f"{{{namespace}}}lastmod").text = today

    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    tree.write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    print(f"Sitemap written with {len(urls)} canonical URLs.")


if __name__ == "__main__":
    main()
