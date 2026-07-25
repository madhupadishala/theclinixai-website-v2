#!/usr/bin/env python3
"""Verify the deployed IndexNow key and submit canonical sitemap URLs."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KEY = "63c00e53c9889490fc22afa7c81c90a64b99ce578c9eb7b2"
DEFAULT_HOST = "www.theclinixai.com"
DEFAULT_ENDPOINT = "https://api.indexnow.org/indexnow"


def canonical_urls(sitemap_path: Path) -> list[str]:
    sitemap = ET.parse(sitemap_path).getroot()
    return [
        node.text.strip()
        for node in sitemap.findall(
            "{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
            "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
        )
        if node.text and node.text.strip()
    ]


def verify_live_key(key_location: str, key: str) -> None:
    request = urllib.request.Request(
        key_location,
        headers={"User-Agent": "TheClinixAI-IndexNow/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read().decode("utf-8").strip()
            if response.status != 200 or content != key:
                raise SystemExit(
                    f"IndexNow key verification failed: HTTP {response.status}, "
                    "or deployed key content did not match."
                )
    except urllib.error.URLError as error:
        raise SystemExit(
            f"IndexNow key is not live at {key_location}. "
            "Deploy the release first, then run this command again."
        ) from error


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", default=DEFAULT_KEY)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--sitemap", type=Path, default=ROOT / "sitemap.xml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="Create/confirm the local key file without submitting URLs.",
    )
    args = parser.parse_args()

    if not 8 <= len(args.key) <= 128 or not args.key.replace("-", "").isalnum():
        raise SystemExit("IndexNow key must be 8–128 alphanumeric/hyphen characters.")

    key_path = ROOT / f"{args.key}.txt"
    if not key_path.exists():
        key_path.write_text(args.key, encoding="utf-8")
    if key_path.read_text(encoding="utf-8").strip() != args.key:
        raise SystemExit(f"Local key file content does not match: {key_path}")

    key_location = f"https://{args.host}/{args.key}.txt"
    urls = canonical_urls(args.sitemap)
    payload = {
        "host": args.host,
        "key": args.key,
        "keyLocation": key_location,
        "urlList": urls,
    }

    if args.prepare_only:
        print(f"IndexNow key ready: {key_path.name}")
        return
    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return

    verify_live_key(key_location, args.key)
    request = urllib.request.Request(
        args.endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "TheClinixAI-IndexNow/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status not in (200, 202):
                raise SystemExit(f"Unexpected IndexNow response: HTTP {response.status}")
            print(
                f"IndexNow response: {response.status}; "
                f"submitted {len(urls)} canonical URLs."
            )
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        print(
            f"IndexNow submission failed: HTTP {error.code} {detail}",
            file=sys.stderr,
        )
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
