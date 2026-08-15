#!/usr/bin/env python3
"""Strict, repeatable on-page SEO quality gate for the static ClinixAI site."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
BASE = "https://www.theclinixai.com"
EXCLUDED = {"404.html", "header.html", "footer.html"}
UTILITY = {"cookie-policy.html", "privacy-policy.html"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.images: list[dict[str, str | None]] = []
        self.headings: list[int] = []
        self.in_body = False
        self.hidden_depth = 0
        self.words: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag == "body":
            self.in_body = True
        if tag in {"script", "style", "noscript"}:
            self.hidden_depth += 1
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag == "img":
            self.images.append(values)
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "body":
            self.in_body = False
        if tag in {"script", "style", "noscript"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.in_body and not self.hidden_depth:
            self.words.extend(re.findall(r"[A-Za-z][A-Za-z'-]+", data))


def first(pattern: str, source: str) -> str:
    match = re.search(pattern, source, re.I | re.S)
    return unescape(re.sub(r"\s+", " ", match.group(1)).strip()) if match else ""


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("/index.html")]
    return "/" + rel.removesuffix(".html")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    records: list[dict] = []
    titles: Counter[str] = Counter()
    descriptions: Counter[str] = Counter()
    canonicals: Counter[str] = Counter()
    incoming: Counter[str] = Counter()

    paths = [p for p in sorted(ROOT.rglob("*.html")) if p.relative_to(ROOT).as_posix() not in EXCLUDED]
    routes = {route_for(p): p for p in paths}

    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        source = path.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(source)
        title = first(r"<title>(.*?)</title>", source)
        description = first(r'<meta\s+name=["\']description["\'][^>]*content=["\'](.*?)["\']', source)
        canonical = first(r'<link\s+rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', source)
        robots = first(r'<meta\s+name=["\']robots["\'][^>]*content=["\'](.*?)["\']', source).lower()
        route = route_for(path)
        expected = BASE + route
        word_count = len(parser.words)

        if not title:
            errors.append(f"{rel}: missing title")
        elif not 30 <= len(title) <= 65:
            warnings.append(f"{rel}: title length {len(title)} (target 30-65)")
        if not description:
            errors.append(f"{rel}: missing meta description")
        elif not 100 <= len(description) <= 170:
            warnings.append(f"{rel}: meta description length {len(description)} (target 100-170)")
        if canonical != expected:
            errors.append(f"{rel}: canonical {canonical or 'missing'}; expected {expected}")
        if "noindex" in robots:
            errors.append(f"{rel}: indexable page is marked noindex")
        if parser.headings.count(1) != 1:
            errors.append(f"{rel}: expected exactly one H1")
        for previous, current in zip(parser.headings, parser.headings[1:]):
            if current > previous + 1:
                warnings.append(f"{rel}: heading level jumps H{previous} to H{current}")
                break
        if rel not in UTILITY and word_count < 300:
            warnings.append(f"{rel}: thin body content ({word_count} words)")
        if "application/ld+json" not in source:
            errors.append(f"{rel}: missing structured data")
        else:
            for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', source, re.I | re.S):
                try:
                    json.loads(raw)
                except json.JSONDecodeError as exc:
                    errors.append(f"{rel}: invalid JSON-LD ({exc.msg})")
        for image in parser.images:
            if not (image.get("alt") or "").strip():
                errors.append(f"{rel}: image has empty/missing alt text")
            if not image.get("width") or not image.get("height"):
                warnings.append(f"{rel}: image missing intrinsic width/height")
                break
        internal_count = 0
        for href in parser.links:
            parsed = urlparse(href)
            if parsed.scheme in {"mailto", "tel", "javascript"} or href.startswith("#"):
                continue
            if parsed.netloc and parsed.netloc != "www.theclinixai.com":
                continue
            target = parsed.path or "/"
            if target.endswith(".html"):
                errors.append(f"{rel}: legacy .html internal link {href}")
            target = target.rstrip("/") or "/"
            if target in routes:
                incoming[target] += 1
                internal_count += 1
        if internal_count < 2 and rel not in UTILITY:
            warnings.append(f"{rel}: fewer than two contextual internal links")

        titles[title] += bool(title)
        descriptions[description] += bool(description)
        canonicals[canonical] += bool(canonical)
        records.append({"path": rel, "route": route, "title": title, "description": description,
                        "canonical": canonical, "words": word_count, "internal_links": internal_count})

    for label, values in (("title", titles), ("description", descriptions), ("canonical", canonicals)):
        for value, count in values.items():
            if value and count > 1:
                errors.append(f"duplicate {label} used by {count} pages: {value}")
    for route, path in routes.items():
        rel = path.relative_to(ROOT).as_posix()
        if route != "/" and rel not in UTILITY and incoming[route] == 0:
            errors.append(f"{rel}: orphan page with no internal links")

    root = ET.parse(ROOT / "sitemap.xml").getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    submitted = {node.text for node in root.findall("s:url/s:loc", ns) if node.text}
    expected_urls = {BASE + route for route in routes}
    if submitted != expected_urls:
        for url in sorted(expected_urls - submitted):
            errors.append(f"sitemap missing {url}")
        for url in sorted(submitted - expected_urls):
            errors.append(f"sitemap contains non-canonical/unknown URL {url}")

    report = {"pages": len(records), "errors": errors, "warnings": warnings, "records": records}
    (ROOT / "seo-quality-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"pages": len(records), "errors": len(errors), "warnings": len(warnings)}, indent=2))
    for item in errors:
        print("ERROR", item)
    for item in warnings:
        print("WARN", item)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
