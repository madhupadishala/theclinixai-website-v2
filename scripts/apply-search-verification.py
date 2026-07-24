#!/usr/bin/env python3
"""Apply exact Google and Bing verification tokens to the homepage."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--google", required=True, help="Google Search Console verification token")
    parser.add_argument("--bing", required=True, help="Bing Webmaster Tools verification token")
    args = parser.parse_args()
    path = ROOT / "index.html"
    source = path.read_text(encoding="utf-8")
    source = re.sub(r'<meta\s+name="google-site-verification"[^>]*>', "", source)
    source = re.sub(r'<meta\s+name="msvalidate\.01"[^>]*>', "", source)
    tags = (
        f'<meta name="google-site-verification" content="{html.escape(args.google, quote=True)}">'
        f'<meta name="msvalidate.01" content="{html.escape(args.bing, quote=True)}">'
    )
    source = source.replace("</head>", tags + "</head>", 1)
    path.write_text(source, encoding="utf-8")
    print("Google and Bing verification metadata applied to index.html.")


if __name__ == "__main__":
    main()
