#!/usr/bin/env python3
"""Build controlled press and earned-authority assets."""

from __future__ import annotations

import csv
import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
engine = runpy.run_path(str(ROOT / "scripts" / "build-entity-pages.py"))
render = engine["render"]

PAGES = [
    (
        "press-kit",
        "TheClinixAI Press Kit",
        "Official ClinixAI press resources covering company positioning, Nexus platform context, brand references, research and media enquiries.",
        "Use current facts. Preserve the context. Attribute the source.",
        "This press kit provides a controlled starting point for journalists, analysts, event organisers, partners and institutions evaluating ClinixAI. It does not authorise claims about customers, validation status, regulatory approval, funding or market leadership unless explicitly announced.",
        [
            ("Company reference", "TheClinixAI is developing governed pharmacovigilance and patient-safety intelligence through the Nexus platform."),
            ("Product reference", "Nexus connects literature, intake, ICSR workflows, review, quality, submissions and cumulative safety activities."),
            ("Media discipline", "Use the current newsroom and named company contact before publishing status-sensitive claims."),
        ],
    ),
    (
        "company-fact-sheet",
        "TheClinixAI Company Fact Sheet",
        "A concise source of official ClinixAI company, product, research, Academy and patient-safety information for partners and media.",
        "TheClinixAI at a glance.",
        "ClinixAI operates at the intersection of pharmacovigilance, healthcare technology, scientific research and professional capability development. Its operating purpose is to strengthen traceability and accountability across patient-safety decisions.",
        [
            ("Core platform", "The Nexus platform is organised as connected pharmacovigilance workspaces on a shared governance backbone."),
            ("Knowledge programme", "ClinixAI publishes source-led scientific guides and architecture research for safety professionals."),
            ("Capability programme", "ClinixAI Academy focuses on practical PV learning, internal projects and responsible technology adoption."),
        ],
    ),
    (
        "pharmacovigilance-expert-commentary",
        "Pharmacovigilance Expert Commentary",
        "Request ClinixAI expert context on pharmacovigilance operations, governed AI, literature intelligence, ICSR quality, signals and patient safety.",
        "Regulated healthcare deserves more than generic AI commentary.",
        "ClinixAI contributors can provide operational and scientific context on how pharmacovigilance decisions are collected, assessed, reviewed, governed and evidenced. Commentary should distinguish established regulatory requirements, professional interpretation and emerging technology practice.",
        [
            ("Operational PV", "Literature, intake, cases, medical review, QC, submissions, signals, aggregates and quality systems."),
            ("Governed AI", "Intended use, evidence grounding, validation, human oversight, limitations and accountable change."),
            ("Patient safety", "Hospital reporting, medication safety, incident learning and responsible information exchange."),
        ],
    ),
]


def main() -> None:
    for page in PAGES:
        (ROOT / f"{page[0]}.html").write_text(render(*page), encoding="utf-8")

    press = ROOT / "press"
    press.mkdir(exist_ok=True)
    facts = {
        "name": "TheClinixAI",
        "alternate_names": ["ClinixAI", "The Clinix AI"],
        "website": "https://www.theclinixai.com/",
        "category": ["Pharmacovigilance technology", "Patient-safety intelligence", "Healthcare AI"],
        "platform": "Nexus",
        "official_resources": [
            "https://www.theclinixai.com/company-profile",
            "https://www.theclinixai.com/end-to-end-pharmacovigilance-nexus-platform",
            "https://www.theclinixai.com/research-scientific-programme",
            "https://www.theclinixai.com/media-newsroom",
        ],
        "restricted_claims": [
            "Do not claim regulatory approval unless an authorised announcement exists.",
            "Do not name customers or partners without an authorised announcement.",
            "Do not claim validated production status for a specific customer environment without evidence.",
        ],
    }
    (press / "company-facts.json").write_text(json.dumps(facts, indent=2), encoding="utf-8")
    rows = [
        ["Target organisation", "Target URL", "Relevance", "Asset offered", "Owner", "Status", "Evidence URL", "Next action"],
        ["", "", "", "", "", "Research", "", ""],
    ]
    with (press / "earned-authority-tracker.csv").open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(rows)
    print("Generated 3 press pages and controlled earned-authority assets.")


if __name__ == "__main__":
    main()
