#!/usr/bin/env python3
"""Release-blocking SEO and internal-link audit for the static website."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
EXCLUDED_DIRS = {".git", ".github", "node_modules", ".vercel"}
EXCLUDED_FILES = {"404.html", "header.html", "footer.html"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = []
        self.in_title = False
        self.meta_description = False
        self.canonical = None
        self.h1_count = 0
        self.links = []
        self.text = []
        self.in_script_style = 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag in {"script", "style"}:
            self.in_script_style += 1
        if tag == "meta" and data.get("name", "").lower() == "description" and data.get("content", "").strip():
            self.meta_description = True
        if tag == "link" and data.get("rel", "").lower() == "canonical":
            self.canonical = data.get("href")
        if tag == "h1":
            self.h1_count += 1
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in {"script", "style"} and self.in_script_style:
            self.in_script_style -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if not self.in_script_style:
            self.text.append(data)


def pages():
    return sorted(
        p for p in ROOT.rglob("*.html")
        if p.name not in EXCLUDED_FILES and not any(part in EXCLUDED_DIRS for part in p.parts)
    )


def expected_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "https://www.theclinixai.com/"
    if rel.endswith("/index.html"):
        return "https://www.theclinixai.com/" + rel[:-11].rstrip("/")
    return "https://www.theclinixai.com/" + rel[:-5]


def local_target_exists(source: Path, href: str) -> bool:
    parsed = urlsplit(href)
    if parsed.scheme or href.startswith(("#", "//", "mailto:", "tel:")):
        return True
    path = parsed.path
    if not path:
        return True
    if path.startswith("/"):
        clean = path.strip("/")
        candidates = [ROOT / (clean + ".html"), ROOT / clean / "index.html"]
        if not clean:
            candidates = [ROOT / "index.html"]
    else:
        base = source.parent / path
        candidates = [base, Path(str(base) + ".html"), base / "index.html"]
    return any(candidate.exists() for candidate in candidates)


def audit():
    errors = []
    warnings = []
    all_pages = pages()
    for path in all_pages:
        parser = PageParser()
        raw = path.read_text(encoding="utf-8")
        try:
            parser.feed(raw)
        except Exception as exc:
            errors.append(f"{path}: invalid HTML parser input: {exc}")
            continue
        rel = path.relative_to(ROOT)
        if not "".join(parser.title).strip():
            errors.append(f"{rel}: missing title")
        if not parser.meta_description:
            errors.append(f"{rel}: missing meta description")
        if parser.canonical != expected_url(path):
            errors.append(f"{rel}: canonical {parser.canonical!r} != {expected_url(path)!r}")
        if parser.h1_count != 1:
            errors.append(f"{rel}: expected exactly one H1, found {parser.h1_count}")
        for href in parser.links:
            path_only = href.split("?", 1)[0].split("#", 1)[0].lower()
            if path_only.endswith(".html") and not re.match(r"^[a-z][a-z0-9+.-]*:", href.lower()):
                errors.append(f"{rel}: .html internal link remains: {href}")
            if not local_target_exists(path, href):
                errors.append(f"{rel}: broken internal link: {href}")
        words = re.findall(r"\b[\w’'-]+\b", " ".join(parser.text))
        if path.as_posix().startswith(str(ROOT / "services")) and len(words) < 500:
            errors.append(f"{rel}: service page has only {len(words)} words (<500)")
        elif len(words) < 250:
            warnings.append(f"{rel}: thin page ({len(words)} words)")

    insights_index = ROOT / "insights" / "index.html"
    insight_pages = [p for p in (ROOT / "insights").glob("*.html") if p.name != "index.html"]
    if not insights_index.exists():
        errors.append("insights/index.html missing")
    else:
        index_raw = insights_index.read_text(encoding="utf-8")
        missing = [p.stem for p in insight_pages if f'/insights/{p.stem}' not in index_raw]
        if missing:
            errors.append(f"insights/index.html does not link {len(missing)} articles: {', '.join(missing[:10])}")

    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        errors.append("sitemap.xml missing")
    else:
        tree = ET.parse(sitemap)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [node.text for node in tree.findall("s:url/s:loc", ns)]
        dates = {node.text for node in tree.findall("s:url/s:lastmod", ns)}
        if len(locs) != len(set(locs)):
            errors.append("sitemap contains duplicate URLs")
        if len(dates) < 2:
            errors.append("sitemap lastmod dates are identical")
        if "https://www.theclinixai.com/insights" not in locs:
            errors.append("/insights missing from sitemap")

    print(f"Audited {len(all_pages)} HTML pages")
    print(f"Warnings: {len(warnings)}")
    for item in warnings[:30]:
        print("WARNING", item)
    if errors:
        print(f"Errors: {len(errors)}")
        for item in errors:
            print("ERROR", item)
        return 1
    print("PASS: all MASTER_SPEC release gates satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(audit())
