#!/usr/bin/env python3
"""
Injects real author bylines into all 40 /insights/ articles:
- Replaces "TheClinixAI PV Science & Operations" visible byline with "By {Name}, {Title}"
- Replaces JSON-LD Article.author Organization with a Person object
- Replaces <meta name="author"> with the real name
Content of the article itself is untouched by this script.
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
INSIGHTS = ROOT / "insights"
AUTHORS = json.loads((ROOT / "data" / "authors.json").read_text(encoding="utf-8"))

# slug (article) -> author key in authors.json
ASSIGNMENT = {
    # Dr. Harsha (8) — Clinical Trial Safety + ICSR Medical Review/Submission
    "sae-reporting-clinical-trials": "dr-harsha",
    "susar-assessment-reporting-timelines": "dr-harsha",
    "development-safety-update-report-dsur": "dr-harsha",
    "clinical-trial-safety-pharmacovigilance": "dr-harsha",
    "quality-control-medical-review-pharmacovigilance": "dr-harsha",
    "icsr-quality-control-pharmacovigilance": "dr-harsha",
    "icsr-medical-review-pharmacovigilance": "dr-harsha",
    "icsr-regulatory-submission-e2b-r3": "dr-harsha",

    # Dr. Surya (4) — PV Agreements & Partner Governance
    "safety-data-exchange-agreement-sdea": "dr-surya",
    "pharmacovigilance-reconciliation": "dr-surya",
    "mah-manufacturer-distributor-pharmacovigilance-responsibilities": "dr-surya",
    "pharmacovigilance-agreements-partner-governance": "dr-surya",

    # Divya Jagdish (2) — Operational CAPA
    "root-cause-analysis-capa-pharmacovigilance": "divya-jagdish",
    "capa-effectiveness-check-pharmacovigilance": "divya-jagdish",

    # Dr. Gayathri (7) — topic overviews + 2 foundational deep-dives
    "pharmacovigilance-audits-capa": "gayathri-manager",
    "post-authorisation-safety-study-pass": "gayathri-manager",
    "pharmacoepidemiology-in-pharmacovigilance": "gayathri-manager",
    "pharmacovigilance-quality-management-system": "gayathri-manager",
    "special-situations-in-pharmacovigilance": "gayathri-manager",
    "signal-validation-prioritisation-pharmacovigilance": "gayathri-manager",
    "signal-management-in-pharmacovigilance": "gayathri-manager",

    # Wany Williams (11) — remaining literature-adjacent detail articles
    "risk-based-pharmacovigilance-audit-programme": "wany-williams",
    "real-world-data-evidence-pharmacovigilance": "wany-williams",
    "pharmacoepidemiology-study-designs": "wany-williams",
    "pharmacovigilance-system-master-file-psmf": "wany-williams",
    "pharmacovigilance-inspection-readiness": "wany-williams",
    "pharmacovigilance-kpis-compliance-metrics": "wany-williams",
    "pregnancy-breastfeeding-exposure-pharmacovigilance": "wany-williams",
    "medication-errors-overdose-misuse-abuse-pharmacovigilance": "wany-williams",
    "lack-efficacy-off-label-occupational-exposure-pv": "wany-williams",
    "pharmacovigilance-signal-detection": "wany-williams",
    "disproportionality-analysis-pharmacovigilance": "wany-williams",

    # Madhu Padishala (8) — Aggregate Safety Reporting + Risk Management & Benefit-Risk
    "pbrer-psur-preparation": "madhu-padishala",
    "dsur-preparation-pharmacovigilance": "madhu-padishala",
    "aggregate-report-data-lock-quality-control": "madhu-padishala",
    "aggregate-safety-reporting-pharmacovigilance": "madhu-padishala",
    "risk-management-plan-preparation": "madhu-padishala",
    "risk-minimisation-measures-effectiveness": "madhu-padishala",
    "benefit-risk-evaluation-pharmacovigilance": "madhu-padishala",
    "risk-management-benefit-risk-pharmacovigilance": "madhu-padishala",
}


def process(path: Path, author_key: str):
    author = AUTHORS[author_key]
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # 1. Visible byline
    meta_div = soup.select_one("div.article-meta")
    if meta_div:
        first_span = meta_div.find("span")
        if first_span:
            label = author["name"]
            if author["credentials"]:
                label += f", {author['credentials']}"
            first_span.string = f"By {label}"

    # 2. <meta name="author">
    meta_author = soup.find("meta", attrs={"name": "author"})
    if meta_author:
        meta_author["content"] = author["name"]

    # 3. JSON-LD Article.author -> Person
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
        except (TypeError, ValueError):
            continue
        if isinstance(data, dict) and data.get("@type") == "Article":
            data["author"] = {
                "@type": "Person",
                "name": author["name"],
                "jobTitle": author["title"],
                "description": author["bio"],
            }
            script.string = json.dumps(data)

    path.write_text(str(soup), encoding="utf-8")


def main():
    done, missing = 0, []
    for slug, author_key in ASSIGNMENT.items():
        path = INSIGHTS / f"{slug}.html"
        if not path.exists():
            missing.append(slug)
            continue
        process(path, author_key)
        done += 1
    print(f"Updated {done} articles")
    if missing:
        print("MISSING:", missing)
    if done != 40:
        print(f"WARNING: expected 40, got {done}")


if __name__ == "__main__":
    main()
