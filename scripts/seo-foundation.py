#!/usr/bin/env python3
"""Apply repeatable static SEO metadata to ClinixAI's non-article pages."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.theclinixai.com"

PAGES = {
    "index.html": ("/", "WebSite"),
    "about.html": ("/about", "AboutPage"),
    "academy.html": ("/academy", "WebPage"),
    "contact.html": ("/contact", "ContactPage"),
    "nexus-platform.html": ("/nexus-platform", "WebPage"),
    "services.html": ("/services", "WebPage"),
    "resources.html": ("/resources", "CollectionPage"),
    "insights/index.html": ("/insights", "CollectionPage"),
    "research-001-beyond-automation.html": (
        "/research-001-beyond-automation",
        "ScholarlyArticle",
    ),
    "research-002-compliant-ai-literature-screening.html": (
        "/research-002-compliant-ai-literature-screening",
        "ScholarlyArticle",
    ),
    "research-003-ai-nexus-intake-engine.html": (
        "/research-003-ai-nexus-intake-engine",
        "ScholarlyArticle",
    ),
    "whitepaper-beyond-automation.html": (
        "/research-001-beyond-automation",
        "ScholarlyArticle",
    ),
    "whitepaper-search-to-safety.html": (
        "/whitepaper-search-to-safety",
        "ScholarlyArticle",
    ),
}

ORGANIZATION = {
    "@type": "Organization",
    "@id": f"{BASE}/#organization",
    "name": "TheClinixAI",
    "alternateName": ["ClinixAI", "The Clinix AI"],
    "url": f"{BASE}/",
    "logo": {
        "@type": "ImageObject",
        "url": f"{BASE}/icon-512.png",
    },
    "sameAs": [
        "https://www.linkedin.com/company/theclinixai/",
        "https://www.instagram.com/theclinixai/",
    ],
}


def extract(pattern: str, source: str) -> str:
    match = re.search(pattern, source, flags=re.I | re.S)
    if not match:
        raise ValueError(f"Required metadata not found: {pattern}")
    return html.unescape(match.group(1).strip())


def apply_page(path: Path, route: str, schema_type: str) -> None:
    source = path.read_text(encoding="utf-8")
    title = extract(r"<title>(.*?)</title>", source)
    description = extract(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', source
    )
    canonical = f"{BASE}{route}"

    source = re.sub(
        r'<link\s+rel=["\']canonical["\'][^>]*>',
        "",
        source,
        flags=re.I,
    )
    source = re.sub(
        r'<meta\s+property=["\']og:(?:title|description|url|type|image)["\'][^>]*>',
        "",
        source,
        flags=re.I,
    )
    source = re.sub(
        r'<meta\s+name=["\']twitter:(?:card|image)["\'][^>]*>',
        "",
        source,
        flags=re.I,
    )
    source = re.sub(
        r'<script\s+type=["\']application/ld\+json["\']\s+data-site-schema>.*?</script>',
        "",
        source,
        flags=re.I | re.S,
    )

    page_node = {
        "@type": schema_type,
        "@id": f"{canonical}#webpage",
        "url": canonical,
        "name": title,
        "description": description,
        "isPartOf": {"@id": f"{BASE}/#website"},
        "about": {"@id": f"{BASE}/#organization"},
        "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
    }
    if schema_type == "ScholarlyArticle":
        page_node.update(
            {
                "headline": title,
                "publisher": {"@id": f"{BASE}/#organization"},
                "author": {"@id": f"{BASE}/#organization"},
                "mainEntityOfPage": canonical,
            }
        )

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            ORGANIZATION,
            {
                "@type": "WebSite",
                "@id": f"{BASE}/#website",
                "url": f"{BASE}/",
                "name": "TheClinixAI",
                "publisher": {"@id": f"{BASE}/#organization"},
            },
            page_node,
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{BASE}/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": title,
                        "item": canonical,
                    },
                ],
            },
        ],
    }
    metadata = (
        f'<link rel="canonical" href="{canonical}">'
        f'<meta property="og:title" content="{html.escape(title, quote=True)}">'
        f'<meta property="og:description" content="{html.escape(description, quote=True)}">'
        f'<meta property="og:url" content="{canonical}">'
        '<meta property="og:type" content="website">'
        f'<meta property="og:image" content="{BASE}/icon-512.png">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:image" content="{BASE}/icon-512.png">'
        '<script type="application/ld+json" data-site-schema>'
        f'{json.dumps(graph, ensure_ascii=False, separators=(",", ":"))}'
        "</script>"
    )
    source = source.replace("</head>", f"{metadata}</head>", 1)
    path.write_text(source, encoding="utf-8")


def main() -> None:
    for relative, (route, schema_type) in PAGES.items():
        apply_page(ROOT / relative, route, schema_type)

    not_found = ROOT / "404.html"
    source = not_found.read_text(encoding="utf-8")
    source = re.sub(
        r'<meta\s+name=["\']robots["\'][^>]*>',
        '<meta name="robots" content="noindex,nofollow">',
        source,
        count=1,
        flags=re.I,
    )
    not_found.write_text(source, encoding="utf-8")
    print(f"SEO metadata applied to {len(PAGES)} pages; 404 remains noindex.")


if __name__ == "__main__":
    main()
