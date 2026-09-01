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
    # Handles both the empty placeholder (first run on a page) and an
    # already-baked header/footer from a previous run (re-bake after
    # header.html/footer.html changes). The closing "</header></div>" and
    # "</footer></div>" sequences are unique per page since each page has
    # exactly one header and one footer.
    html, n_header_empty = re.subn(
        r'<div id="site-header"></div>',
        f'<div id="site-header">{header_html}</div>',
        html,
    )
    if not n_header_empty:
        html, n_header_baked = re.subn(
            r'<div id="site-header">.*?</header></div>',
            f'<div id="site-header">{header_html}</div>',
            html,
            flags=re.S,
        )
    else:
        n_header_baked = 0

    html, n_footer_empty = re.subn(
        r'<div id="site-footer"></div>',
        f'<div id="site-footer">{footer_html}</div>',
        html,
    )
    if not n_footer_empty:
        html, n_footer_baked = re.subn(
            r'<div id="site-footer">.*?</footer></div>',
            f'<div id="site-footer">{footer_html}</div>',
            html,
            flags=re.S,
        )
    else:
        n_footer_baked = 0

    return html, (n_header_empty or n_header_baked), (n_footer_empty or n_footer_baked)

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
    unchanged = 0
    skipped_no_match = 0

    for path in find_html_files():
        original = path.read_text(encoding="utf-8")

        if 'id="site-header"' not in original:
            skipped_no_match += 1
            continue

        updated, n_header, n_footer = inline_into(original, header_html, footer_html)
        if not (n_header or n_footer):
            skipped_no_match += 1
        elif updated == original:
            unchanged += 1
        else:
            path.write_text(updated, encoding="utf-8")
            changed += 1

    print(f"Updated header/footer in {changed} pages.")
    print(f"Already up to date (skipped): {unchanged}")
    print(f"No site-header/site-footer match found (skipped): {skipped_no_match}")

if __name__ == "__main__":
    sys.exit(main())
