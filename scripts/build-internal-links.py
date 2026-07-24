#!/usr/bin/env python3
"""Build bidirectional scientific-to-commercial internal links."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSIGHTS = ROOT / "insights"

TOPIC_SOLUTIONS = {
    "Clinical Trial Safety": ("/aggregate-safety-reporting-software", "Aggregate Safety Reporting Software"),
    "PV Audits & CAPA": ("/pharmacovigilance-quality-management-system-software", "PV Quality Management System"),
    "Pharmacoepidemiology & Real-World Evidence": ("/pharmacovigilance-signal-management-software", "Signal Management Software"),
    "PV Quality Management System": ("/pharmacovigilance-quality-management-system-software", "PV Quality Management System"),
    "PV Agreements & Partner Governance": ("/pharmacovigilance-agreement-partner-governance-software", "Partner Governance Software"),
    "Special Situations": ("/pharmacovigilance-case-intake-automation", "Safety Intake Automation"),
    "Signal Management": ("/pharmacovigilance-signal-management-software", "Signal Management Software"),
    "Aggregate Safety Reporting": ("/aggregate-safety-reporting-software", "Aggregate Safety Reporting Software"),
    "Risk Management & Benefit–Risk": ("/end-to-end-pharmacovigilance-nexus-platform", "Nexus Pharmacovigilance Platform"),
    "ICSR Quality, Medical Review & Submission": ("/icsr-case-processing-software", "ICSR Case Processing Software"),
}

SLUG_OVERRIDES = {
    "icsr-quality-control-pharmacovigilance": ("/icsr-quality-control-automation", "ICSR Quality Control Automation"),
    "icsr-medical-review-pharmacovigilance": ("/pharmacovigilance-medical-review-software", "Medical Review Software"),
    "icsr-regulatory-submission-e2b-r3": ("/e2b-r3-regulatory-submission-management", "E2B(R3) Submission Management"),
    "pharmacovigilance-signal-detection": ("/pharmacovigilance-signal-management-software", "Signal Management Software"),
    "safety-data-exchange-agreement-sdea": ("/pharmacovigilance-agreement-partner-governance-software", "Partner Governance Software"),
}


def main() -> None:
    articles = json.loads((INSIGHTS / "articles.json").read_text(encoding="utf-8"))
    changed = 0
    for article in articles:
        path = INSIGHTS / f"{article['slug']}.html"
        source = path.read_text(encoding="utf-8")
        source = re.sub(
            r'\s*<section class="solution-bridge".*?</section>\s*',
            "\n",
            source,
            flags=re.S,
        )
        url, title = SLUG_OVERRIDES.get(
            article["slug"],
            TOPIC_SOLUTIONS.get(
                article["topic"],
                ("/end-to-end-pharmacovigilance-nexus-platform", "Nexus Pharmacovigilance Platform"),
            ),
        )
        bridge = f'''
    <section class="solution-bridge">
      <div>
        <span>FROM SCIENTIFIC GUIDANCE TO CONTROLLED EXECUTION</span>
        <h2>Operationalise this workflow in {title}.</h2>
        <p>Connect source evidence, accountable review, governed decisions and inspection-ready traceability within the ClinixAI Nexus architecture.</p>
      </div>
      <a href="{url}">Explore the solution →</a>
    </section>
'''
        marker = '    <section class="related-section">'
        if marker not in source:
            raise RuntimeError(f"Related-section marker missing in {path}")
        source = source.replace(marker, bridge + marker, 1)
        path.write_text(source, encoding="utf-8")
        changed += 1
    print(f"Internal solution bridges applied to {changed} scientific articles.")


if __name__ == "__main__":
    main()
