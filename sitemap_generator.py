#!/usr/bin/env python3
"""Generate a canonical sitemap from deployable HTML files using real Git dates.

A page is left out of the sitemap if its own <link rel="canonical"> tag
points somewhere other than its own URL — that's how a page marks itself
as a duplicate of another page, so it shouldn't be submitted to Google
as a separate indexable URL.
"""
from pathlib import Path
from datetime import datetime, timezone
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://www.theclinixai.com"
OUTPUT = ROOT / "sitemap.xml"
EXCLUDED_DIRS = {".git", ".github", "node_modules", ".vercel"}
EXCLUDED_FILES = {"404.html", "header.html", "footer.html"}
CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.I)


def html_files():
    return sorted(
        p for p in ROOT.rglob("*.html")
        if p.name not in EXCLUDED_FILES and not any(part in EXCLUDED_DIRS for part in p.parts)
    )


def is_self_canonical(path: Path, url: str) -> bool:
    """Return False if this page declares a canonical pointing elsewhere,
    meaning another URL is the primary version and this one should be
    left out of the sitemap."""
    match = CANONICAL_RE.search(path.read_text(encoding="utf-8"))
    if not match:
        return True
    return match.group(1).rstrip("/") == url.rstrip("/")


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return BASE_URL + "/"
    if rel.endswith("/index.html"):
        return BASE_URL + "/" + rel[:-11].rstrip("/")
    return BASE_URL + "/" + rel[:-5]


def lastmod(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=True
        )
        value = result.stdout.strip()
        if value:
            return datetime.fromisoformat(value).astimezone(timezone.utc).date().isoformat()
    except Exception:
        pass
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).date().isoformat()


def priority(url: str) -> str:
    path = url.removeprefix(BASE_URL).strip("/")
    if not path:
        return "1.0"
    if path in {"services", "nexus-platform"}:
        return "0.9"
    if path in {"about", "contact", "resources", "insights"}:
        return "0.8"
    if path.startswith(("insights/", "services/", "research-")):
        return "0.7"
    if path.startswith(("privacy-policy", "cookie-policy")):
        return "0.3"
    return "0.6"


def changefreq(url: str) -> str:
    path = url.removeprefix(BASE_URL).strip("/")
    if path.startswith("insights"):
        return "weekly"
    if path in {"", "services", "resources", "academy", "careers"}:
        return "weekly"
    return "monthly"


def generate():
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    root = ET.Element(f"{{{ns}}}urlset")
    seen = set()
    for path in html_files():
        url = url_for(path)
        if not is_self_canonical(path, url):
            continue
        if url in seen:
            raise RuntimeError(f"Duplicate sitemap URL: {url}")
        seen.add(url)
        item = ET.SubElement(root, f"{{{ns}}}url")
        ET.SubElement(item, f"{{{ns}}}loc").text = url
        ET.SubElement(item, f"{{{ns}}}lastmod").text = lastmod(path)
        ET.SubElement(item, f"{{{ns}}}changefreq").text = changefreq(url)
        ET.SubElement(item, f"{{{ns}}}priority").text = priority(url)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
    dates = {lastmod(p) for p in html_files()}
    print(f"Generated sitemap.xml with {len(seen)} canonical URLs and {len(dates)} unique lastmod dates")
    if len(dates) < 2:
        raise RuntimeError("Sitemap lastmod dates are still identical")


if __name__ == "__main__":
    generate()
