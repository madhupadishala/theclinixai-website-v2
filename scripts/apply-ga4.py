#!/usr/bin/env python3
"""Update the verified GA4 measurement ID in the consent-aware site loader."""

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
    legacy_pattern = r"\n/\* GA4 START \*/.*?/\* GA4 END \*/\n"
    source = re.sub(legacy_pattern, "\n", source, flags=re.S)
    pattern = r"(const MEASUREMENT_ID = ')[A-Z0-9-]+(';)"
    source, count = re.subn(pattern, rf"\g<1>{args.measurement_id}\g<2>", source, count=1)
    if count != 1:
        raise SystemExit("Consent-aware GA4 loader was not found in site.js.")
    path.write_text(source, encoding="utf-8")
    print(f"GA4 {args.measurement_id} applied to site.js.")


if __name__ == "__main__":
    main()
