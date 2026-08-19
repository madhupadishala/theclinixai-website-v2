#!/usr/bin/env python3
"""
Breaks the identical 7-header skeleton shared by all 15 /services/ pages.
Content (paragraphs, lists, FAQ answers) is preserved verbatim.
Only section order and header wording change, per-page, so no two pages
share the same shape or the same header text.
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup

SERVICES_DIR = Path(__file__).resolve().parent.parent / "services"

GENERIC = {
    "matters": "Why this service matters",
    "includes": "What the service includes",
    "process": "Delivery process",
    "reg": "Regulatory and quality alignment",
    "deliverables": "Typical deliverables",
    "faq": "Frequently asked questions",
}

# Per-slug: custom header text for each reorderable section + the order to render them in.
# "related" (Related services) always stays last and its header is untouched.
CONFIG = {
    "aggregate-reporting": {
        "order": ["deliverables", "matters", "includes", "process", "reg", "faq"],
        "headers": {
            "matters": "The data-lock problem this service is built around",
            "includes": "What's covered end to end",
            "process": "How an engagement runs",
            "reg": "ICH and EMA alignment",
            "deliverables": "What you receive",
            "faq": "Questions clients ask before signing off",
        },
    },
    "ai-strategy": {
        "order": ["faq", "matters", "includes", "process", "reg", "deliverables"],
        "headers": {
            "matters": "Build, buy, or consult — why this matters first",
            "includes": "What the engagement covers",
            "process": "How we work with your team",
            "reg": "Where governance fits an AI decision",
            "deliverables": "What you walk away with",
            "faq": "The questions worth asking before you commit",
        },
    },
    "icsr-processing": {
        "order": ["process", "includes", "matters", "reg", "deliverables", "faq"],
        "headers": {
            "matters": "Why case-processing quality is the real bottleneck",
            "includes": "Scope of the service",
            "process": "Where cases actually move through the pipeline",
            "reg": "Staying aligned with expedited reporting obligations",
            "deliverables": "What's delivered",
            "faq": "Common questions",
        },
    },
    "inspection-readiness": {
        "order": ["reg", "matters", "includes", "deliverables", "process", "faq"],
        "headers": {
            "matters": "Why readiness has to be continuous, not seasonal",
            "includes": "What's in scope",
            "process": "How a readiness engagement is structured",
            "reg": "Aligning with inspector expectations",
            "deliverables": "What you get",
            "faq": "Frequently asked questions",
        },
    },
    "literature-monitoring": {
        "order": ["matters", "includes", "deliverables", "process", "reg", "faq"],
        "headers": {
            "matters": "Why we built this instead of reselling a generic tool",
            "includes": "What the service covers",
            "process": "How screening runs in practice",
            "reg": "Regulatory alignment",
            "deliverables": "Outputs",
            "faq": "Questions we're asked most",
        },
    },
    "medical-review": {
        "order": ["deliverables", "includes", "matters", "process", "reg", "faq"],
        "headers": {
            "matters": "What a trained reviewer catches that automation doesn't",
            "includes": "Scope of medical review support",
            "process": "How review is structured",
            "reg": "Regulatory and quality alignment",
            "deliverables": "Typical deliverables",
            "faq": "Frequently asked questions",
        },
    },
    "oracle-argus-safety": {
        "order": ["includes", "process", "matters", "deliverables", "reg", "faq"],
        "headers": {
            "matters": "Why configuration choices outlast go-live",
            "includes": "What's covered",
            "process": "How we approach an Argus engagement",
            "reg": "Regulatory and quality alignment",
            "deliverables": "What you receive",
            "faq": "Frequently asked questions",
        },
    },
    "psmf-management": {
        "order": ["matters", "process", "includes", "deliverables", "reg", "faq"],
        "headers": {
            "matters": "Treating the PSMF as a living document, not a file",
            "includes": "What the service includes",
            "process": "How updates get triggered and tracked",
            "reg": "Regulatory and quality alignment",
            "deliverables": "Typical deliverables",
            "faq": "Frequently asked questions",
        },
    },
    "pv-team-setup": {
        "order": ["reg", "includes", "process", "matters", "deliverables", "faq"],
        "headers": {
            "matters": "Building a PV function from zero headcount",
            "includes": "What's in scope",
            "process": "The sequence we follow",
            "reg": "Regulatory and quality alignment",
            "deliverables": "What you get",
            "faq": "Frequently asked questions",
        },
    },
    "quality-management": {
        "order": ["faq", "includes", "matters", "process", "deliverables", "reg"],
        "headers": {
            "matters": "QMS as prevention infrastructure, not paperwork",
            "includes": "What's covered",
            "process": "How we build the system with you",
            "reg": "Regulatory and quality alignment",
            "deliverables": "Typical deliverables",
            "faq": "Frequently asked questions",
        },
    },
    "regulatory-submissions": {
        "order": ["process", "matters", "reg", "includes", "deliverables", "faq"],
        "headers": {
            "matters": "Why the submission clock is tighter than it looks",
            "includes": "What the service covers",
            "process": "Where the hours actually go",
            "reg": "Regulatory and quality alignment",
            "deliverables": "Typical deliverables",
            "faq": "Frequently asked questions",
        },
    },
    "signal-management": {
        "order": ["includes", "matters", "process", "faq", "reg", "deliverables"],
        "headers": {
            "matters": "Why a closed signal needs a documented reasoning chain",
            "includes": "Scope of the service",
            "process": "From detection to closure",
            "reg": "Regulatory and quality alignment",
            "deliverables": "Typical deliverables",
            "faq": "Frequently asked questions",
        },
    },
    "training-workforce": {
        "order": ["matters", "deliverables", "includes", "process", "faq", "reg"],
        "headers": {
            "matters": "Where competency gaps actually show up in audits",
            "includes": "What's in scope",
            "process": "How training is structured",
            "reg": "Regulatory and quality alignment",
            "deliverables": "What you get",
            "faq": "Frequently asked questions",
        },
    },
    "veeva-vault-safety": {
        "order": ["reg", "matters", "process", "includes", "faq", "deliverables"],
        "headers": {
            "matters": "Vault vs. Argus — the decision factors that matter",
            "includes": "What's covered",
            "process": "How we run the comparison and migration",
            "reg": "Regulatory and quality alignment",
            "deliverables": "Typical deliverables",
            "faq": "Frequently asked questions",
        },
    },
    "vendor-oversight": {
        "order": ["deliverables", "process", "matters", "includes", "faq", "reg"],
        "headers": {
            "matters": "The red flags that show up before an audit does",
            "includes": "What's in scope",
            "process": "How oversight is structured",
            "reg": "Regulatory and quality alignment",
            "deliverables": "Typical deliverables",
            "faq": "Frequently asked questions",
        },
    },
}


def key_for_header(text):
    for k, v in GENERIC.items():
        if v == text.strip():
            return k
    return None


def restructure(path: Path, cfg: dict):
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    prose = soup.select_one("div.shell.prose")
    if prose is None:
        print(f"SKIP (no prose div): {path.name}")
        return False

    # Walk children, grouping into sections keyed by the generic header they start with.
    sections = {}
    related_nodes = []
    current_key = None
    current_related = False
    for child in list(prose.children):
        name = getattr(child, "name", None)
        if name == "h2":
            text = child.get_text()
            k = key_for_header(text)
            if k == "related" or text.strip() == "Related services":
                current_related = True
                current_key = None
                related_nodes.append(child.extract())
                continue
            if k is None:
                print(f"  WARNING unrecognized h2 '{text}' in {path.name}")
                current_key = None
                current_related = False
                continue
            current_related = False
            current_key = k
            sections[k] = {"header": child.extract(), "body": []}
            continue
        if current_related:
            related_nodes.append(child.extract())
        elif current_key is not None:
            sections[current_key]["body"].append(child.extract())

    missing = [k for k in GENERIC if k not in sections]
    if missing:
        print(f"  WARNING missing sections {missing} in {path.name}")

    order = cfg["order"]
    headers = cfg["headers"]

    # Rebuild in new order with new header text
    for k in order:
        if k not in sections:
            continue
        new_h2 = soup.new_tag("h2")
        new_h2.string = headers[k]
        prose.append(new_h2)
        for node in sections[k]["body"]:
            prose.append(node)

    # Related services block goes back at the end, unchanged
    for node in related_nodes:
        prose.append(node)

    path.write_text(str(soup), encoding="utf-8")
    return True


def main():
    changed = 0
    for slug, cfg in CONFIG.items():
        path = SERVICES_DIR / f"{slug}.html"
        if not path.exists():
            print(f"MISSING FILE: {path}")
            continue
        if restructure(path, cfg):
            changed += 1
            print(f"OK: {slug}.html")
    print(f"\n{changed}/{len(CONFIG)} pages restructured")


if __name__ == "__main__":
    main()
