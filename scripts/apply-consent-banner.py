#!/usr/bin/env python3
"""Prepare all public pages for the consent-aware ClinixAI release."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_VERSION = "20260724-consent"
EXCLUDED = {"header.html", "footer.html"}


def version_asset(source: str, asset: str) -> tuple[str, int]:
    pattern = rf'((?:src|href)=["\'])(?:/)?{re.escape(asset)}(?:\?v=[^"\']+)?(["\'])'
    return re.subn(
        pattern,
        rf"\g<1>/{asset}?v={ASSET_VERSION}\g<2>",
        source,
        flags=re.I,
    )


def main() -> None:
    required = {
        ROOT / "site.js": "CLINIXAI CONSENT + GA4 START",
        ROOT / "style.css": "PRIVACY CENTRE + CONSENT MODE V2",
        ROOT / "privacy-policy.html": "Privacy, explained with precision.",
        ROOT / "cookie-policy.html": "Cookie choices without ambiguity.",
    }
    for path, marker in required.items():
        if not path.exists() or marker not in path.read_text(encoding="utf-8"):
            raise SystemExit(f"Consent release file is missing or incomplete: {path.name}")

    pages_changed = 0
    site_refs = 0
    style_refs = 0
    for page in ROOT.rglob("*.html"):
        relative = page.relative_to(ROOT).as_posix()
        if relative in EXCLUDED or any(part.startswith(".") for part in page.relative_to(ROOT).parts):
            continue
        source = page.read_text(encoding="utf-8")
        updated, count_site = version_asset(source, "site.js")
        updated, count_style = version_asset(updated, "style.css")
        if updated != source:
            page.write_text(updated, encoding="utf-8")
            pages_changed += 1
        site_refs += count_site
        style_refs += count_style

    subprocess.run([sys.executable, str(ROOT / "scripts" / "build-sitemap.py")], check=True)
    print(
        "Consent release prepared: "
        f"{pages_changed} pages updated, {site_refs} site.js references and "
        f"{style_refs} style.css references versioned."
    )
    print("GA4 remains blocked until the visitor accepts analytics.")


if __name__ == "__main__":
    main()
