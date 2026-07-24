#!/usr/bin/env python3
"""Create an IndexNow key file and submit canonical sitemap URLs to Bing."""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, help="8–128 character IndexNow key")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not 8 <= len(args.key) <= 128 or not args.key.replace("-", "").isalnum():
        raise SystemExit("IndexNow key must be 8–128 alphanumeric/hyphen characters.")
    (ROOT / f"{args.key}.txt").write_text(args.key, encoding="utf-8")
    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    urls = [
        node.text
        for node in sitemap.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if node.text
    ]
    payload = {
        "host": "www.theclinixai.com",
        "key": args.key,
        "keyLocation": f"https://www.theclinixai.com/{args.key}.txt",
        "urlList": urls,
    }
    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return
    request = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        print(f"IndexNow response: {response.status}")


if __name__ == "__main__":
    main()
