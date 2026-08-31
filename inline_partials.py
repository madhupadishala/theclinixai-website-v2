#!/usr/bin/env python3
"""
Inlines header.html and footer.html directly into every static page,
replacing the empty <div id="site-header"></div> / <div id="site-footer"></div>
placeholders that were previously populated only via client-side JS fetch.

Why: search crawlers (especially Bing, and Google on a delayed/uncertain
second pass) do not reliably execute the JS that fetched these partials,
so the real nav links were often invisible on first crawl. Baking them
into the raw HTML makes the site structure visible with zero JS required.

Run this any time header.html or footer.html changes, then commit the
regenerated pages alongside the partial change.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SKIP_FILES = {"header.html", "footer.html"}
SKIP_DIRS = {"node_modules", ".git"}

def load_partial(name):
    return (ROOT / name).read_text(encoding="utf-8").strip()

def inline_into(html, header_html, footer_html):
    html, n_header = re.subn(
        r'<div id="site-header"></div>',
        f'<div id="site-header">{header_html}</div>',
        html,
    )
    html, n_footer = re.subn(
        r'<div id="site-footer"></div>',
        f'<div id="site-footer">{footer_html}</div>',
        html,
    )
    return html, n_header, n_footer

def find_html_files():
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        yield path

def main():
    header_html = load_partial("header.html")
    footer_html = load_partial("footer.html")

    changed = 0
    already_inlined = 0
    no_placeholder = 0

    for path in find_html_files():
        original = path.read_text(encoding="utf-8")

        if 'id="site-header">' in original and '<div id="site-header"></div>' not in original:
            already_inlined += 1
            continue

        if '<div id="site-header"></div>' not in original:
            no_placeholder += 1
            continue

        updated, n_header, n_footer = inline_into(original, header_html, footer_html)
        if n_header or n_footer:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    print(f"Inlined header/footer into {changed} pages.")
    print(f"Already inlined (skipped): {already_inlined}")
    print(f"No placeholder found (skipped): {no_placeholder}")

if __name__ == "__main__":
    sys.exit(main())
