#!/usr/bin/env python3
"""Convert internal .html hrefs to canonical clean URLs."""
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parent
EXCLUDED = {".git", "node_modules", ".vercel"}
HREF_RE = re.compile(r"href=(?P<q>['\"])(?P<url>[^'\"]+)(?P=q)", re.I)


def html_files():
    for path in ROOT.rglob("*.html"):
        if not any(part in EXCLUDED for part in path.parts):
            yield path


def clean_target(raw: str, source: Path) -> str:
    lowered = raw.lower()
    if raw.startswith(("#", "//")) or re.match(r"^[a-z][a-z0-9+.-]*:", lowered):
        return raw

    match = re.match(r"^(?P<path>[^?#]*)(?P<suffix>[?#].*)?$", raw)
    if not match:
        return raw
    target, suffix = match.group("path"), match.group("suffix") or ""
    if not target.lower().endswith(".html"):
        return raw

    source_rel = source.relative_to(ROOT).as_posix()
    source_dir = PurePosixPath(source_rel).parent
    if target.startswith("/"):
        resolved = PurePosixPath(target.lstrip("/"))
    else:
        resolved = source_dir / PurePosixPath(target)

    parts = []
    for part in resolved.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
        else:
            parts.append(part)

    if not parts:
        return "/" + suffix
    filename = parts[-1]
    if filename.lower() == "index.html":
        clean = "/" + "/".join(parts[:-1])
        clean = clean.rstrip("/") or "/"
    else:
        parts[-1] = filename[:-5]
        clean = "/" + "/".join(parts)
    return clean + suffix


def process(path: Path) -> int:
    original = path.read_text(encoding="utf-8")
    changes = 0

    def replace(match: re.Match) -> str:
        nonlocal changes
        raw = match.group("url")
        cleaned = clean_target(raw, path)
        if cleaned != raw:
            changes += 1
        return f"href={match.group('q')}{cleaned}{match.group('q')}"

    updated = HREF_RE.sub(replace, original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        print(f"Fixed {changes:3d} links: {path.relative_to(ROOT)}")
    return changes


def main():
    total = sum(process(path) for path in html_files())
    remaining = []
    for path in html_files():
        for match in HREF_RE.finditer(path.read_text(encoding="utf-8")):
            url = match.group("url")
            if url.lower().split("?", 1)[0].split("#", 1)[0].endswith(".html") and not re.match(r"^[a-z][a-z0-9+.-]*:", url.lower()):
                remaining.append((path, url))
    print(f"Total internal .html links fixed: {total}")
    if remaining:
        for path, url in remaining[:20]:
            print(f"REMAINING {path.relative_to(ROOT)} -> {url}")
        raise SystemExit(f"Failed: {len(remaining)} internal .html links remain")


if __name__ == "__main__":
    main()
