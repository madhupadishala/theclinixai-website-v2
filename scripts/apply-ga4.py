#!/usr/bin/env python3
"""Add a verified GA4 measurement ID to the shared site loader."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--measurement-id", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"G-[A-Z0-9]{6,20}", args.measurement_id):
        raise SystemExit("Expected a GA4 measurement ID such as G-XXXXXXXXXX.")
    path = ROOT / "site.js"
    source = path.read_text(encoding="utf-8")
    source = re.sub(r"\n/\* GA4 START \*/.*?/\* GA4 END \*/\n", "\n", source, flags=re.S)
    block = f"""
/* GA4 START */
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments)}}
gtag('js',new Date());gtag('config','{args.measurement_id}',{{send_page_view:false}});
const ga=document.createElement('script');ga.async=true;ga.src='https://www.googletagmanager.com/gtag/js?id={args.measurement_id}';document.head.appendChild(ga);
/* GA4 END */
"""
    path.write_text(source + block, encoding="utf-8")
    print(f"GA4 {args.measurement_id} applied to site.js.")


if __name__ == "__main__":
    main()
