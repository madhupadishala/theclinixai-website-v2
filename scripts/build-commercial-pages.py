#!/usr/bin/env python3
"""Generate Sprint 2 commercial solution pages for TheClinixAI."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.theclinixai.com"
GVP_VI = "https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vi-collection-management-submission-reports-suspected-adverse-reactions-medicinal-products-rev-2_en.pdf"
ICH_E2B = "https://ich.org/page/e2br3-individual-case-safety-report-icsr-specification-and-related-files"
ICH_E2D = "https://www.ich.org/news/ich-e2dr1-guideline-reaches-step-4-ich-process"
EMA_MLM = "https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/pharmacovigilance-post-authorisation/medical-literature-monitoring"

PAGES = [
    {
        "slug": "pharmacovigilance-literature-monitoring-software",
        "eyebrow": "NEXUS LITERATURE INTELLIGENCE",
        "title": "Pharmacovigilance Literature Monitoring Software",
        "meta": "AI-assisted pharmacovigilance literature monitoring software for governed search, screening, ICSR identification, evidence traceability and inspection-ready oversight.",
        "hook": "A literature review is not complete because a search was run. It is complete only when every retrieved publication, screening decision and safety escalation can be defended.",
        "promise": "Turn fragmented literature surveillance into one governed, traceable safety workflow.",
        "problem_title": "Literature monitoring fails between retrieval and accountability.",
        "problem": "Safety teams rarely struggle because scientific literature does not exist. They struggle because product dictionaries drift, searches are inconsistently executed, local and global sources are separated, duplicate publications are reviewed repeatedly, and screening decisions are difficult to reconstruct during inspection. Nexus Literature Intelligence connects those decisions without replacing accountable medical judgement.",
        "steps": [
            ("01", "Define", "Govern products, active ingredients, synonyms, territories, databases and review frequency."),
            ("02", "Retrieve", "Execute version-controlled searches across configured literature sources and capture the complete result set."),
            ("03", "Normalise", "Standardise metadata, link duplicate records and preserve the original evidence source."),
            ("04", "Screen", "Prioritise publications with explainable AI while reviewers retain the final inclusion and escalation decision."),
            ("05", "Evidence", "Maintain the search, reviewer action, rationale, source and downstream disposition in one audit trail."),
        ],
        "capabilities": [
            ("Governed search strategies", "Version product concepts, Boolean logic, database syntax and effective dates."),
            ("Global and local source control", "Map source responsibilities, language, territory, cadence and evidence of execution."),
            ("Duplicate intelligence", "Link PMID, DOI, title and source variants without deleting evidence."),
            ("Human-in-the-loop screening", "Use AI to prioritise work while preserving reviewer authority and rationale."),
            ("ICSR candidate escalation", "Route potential cases with evidence context into the governed intake workflow."),
            ("Inspection-ready metrics", "Track completed searches, review ageing, exclusions, escalations and missed schedules."),
        ],
        "references": [(GVP_VI, "EMA GVP Module VI"), (EMA_MLM, "EMA Medical Literature Monitoring")],
        "related": [
            ("Literature Screening in Pharmacovigilance", "/insights"),
            ("Pharmacovigilance Search Strategy", "/insights"),
            ("AI Literature Screening", "/insights"),
        ],
        "faqs": [
            ("What is pharmacovigilance literature monitoring software?", "It is a governed system for planning searches, retrieving publications, screening safety relevance, documenting decisions and escalating potential safety information with traceability."),
            ("Does AI make the final literature-screening decision?", "No. ClinixAI positions AI as decision support. Qualified reviewers retain responsibility for inclusion, exclusion, case identification and escalation."),
            ("Can the workflow support local and global literature?", "Yes. Source, country, language, frequency and ownership can be configured within one oversight model."),
            ("Does the system replace regulatory procedures?", "No. It operationalises configured procedures and controls; the marketing authorisation holder remains accountable for regulatory compliance."),
        ],
    },
    {
        "slug": "ai-literature-screening-pharmacovigilance",
        "eyebrow": "GOVERNED AI FOR DRUG SAFETY",
        "title": "AI Literature Screening in Pharmacovigilance",
        "meta": "Governed AI literature screening for pharmacovigilance with evidence-grounded prioritisation, human oversight, explainable decisions and controlled validation.",
        "hook": "The value of AI is not the number of abstracts it can classify. The value is whether a safety professional can verify why the classification was proposed.",
        "promise": "Accelerate screening without allowing speed to outrun scientific accountability.",
        "problem_title": "Black-box classification is not a pharmacovigilance control.",
        "problem": "A model can produce a confident answer and still miss the safety context that matters: product identity, active MAH relevance, patient evidence, suspected reaction, special situations or reportability context. ClinixAI grounds screening assistance in retrieved evidence, governed product data and explicit rules, then exposes the rationale to the reviewer.",
        "steps": [
            ("01", "Context", "Load approved product, procedural and screening context for the specific tenant and workflow."),
            ("02", "Extract", "Identify explicit product, patient, event, reporter, country and special-situation evidence."),
            ("03", "Assess", "Apply governed inclusion, exclusion and escalation logic without inventing missing facts."),
            ("04", "Review", "Present the proposed decision, evidence spans, confidence and flags to a qualified reviewer."),
            ("05", "Learn safely", "Measure overrides and failure patterns through controlled validation—not uncontrolled self-learning."),
        ],
        "capabilities": [
            ("Evidence-grounded outputs", "Every proposed decision points back to publication evidence and governed context."),
            ("False-negative controls", "Low-confidence and rule-sensitive records can be routed for mandatory human review."),
            ("Product intelligence", "Resolve brands, generics, active ingredients, salts and synonyms before assessment."),
            ("Explainable exclusion", "Capture the rule and evidence supporting each proposed exclusion."),
            ("Validation datasets", "Test defined scenarios, edge cases, languages and publication types before release."),
            ("Lifecycle governance", "Version prompts, models, rules, knowledge and performance evidence."),
        ],
        "references": [(GVP_VI, "EMA GVP Module VI"), (ICH_E2D, "ICH E2D(R1) Step 4")],
        "related": [
            ("Signal Detection in Pharmacovigilance", "/insights/pharmacovigilance-signal-detection"),
            ("PV Inspection Readiness", "/insights/pharmacovigilance-inspection-readiness"),
            ("PV Quality Management System", "/insights/pharmacovigilance-quality-management-system"),
        ],
        "faqs": [
            ("Can AI safely automate literature screening?", "AI can support prioritisation and structured evidence extraction when its context, validation, limitations and human oversight are explicitly governed."),
            ("How should false negatives be controlled?", "Controls should combine recall-oriented search, conservative routing, confidence thresholds, mandatory review scenarios, sampling and periodic performance evaluation."),
            ("Is generative AI explainability enough for validation?", "No. Explainability is one control. Validation also requires intended use, representative datasets, acceptance criteria, version control, deviations and documented human oversight."),
            ("Does ClinixAI allow autonomous regulatory decisions?", "No. Final pharmacovigilance and regulatory decisions remain with authorised professionals."),
        ],
    },
    {
        "slug": "pharmacovigilance-case-intake-automation",
        "eyebrow": "NEXUS SAFETY INTAKE",
        "title": "Pharmacovigilance Case Intake Automation",
        "meta": "Pharmacovigilance case intake automation for multichannel safety information capture, day-zero control, minimum criteria assessment, triage and traceable routing.",
        "hook": "The reporting clock does not wait for the safety department to create a case.",
        "promise": "Capture safety information where it enters the organisation and preserve the evidence that starts the clock.",
        "problem_title": "Day zero is often lost before case processing begins.",
        "problem": "Reports can enter through medical information, quality, sales, partners, literature, websites and patient programmes. When intake is fragmented across inboxes and spreadsheets, awareness dates become contestable and source evidence can be separated from the case. Nexus Safety Intake creates a governed front door for safety information without confusing intake with final case assessment.",
        "steps": [
            ("01", "Receive", "Capture structured and unstructured safety information from configured organisational channels."),
            ("02", "Preserve", "Retain the original source, receipt timestamp, attachments and routing history."),
            ("03", "Identify", "Propose minimum-criteria evidence and flag missing or ambiguous information."),
            ("04", "Triage", "Prioritise seriousness, special situations, deadlines and potential duplicates for review."),
            ("05", "Route", "Create a controlled hand-off to case processing with no loss of provenance."),
        ],
        "capabilities": [
            ("Multichannel intake", "Bring email, forms, literature, partners and operational referrals into one queue."),
            ("Day-zero evidence", "Preserve awareness timestamps and organisational routing history."),
            ("Minimum-criteria assistance", "Highlight patient, reporter, product and event evidence for reviewer confirmation."),
            ("Follow-up initiation", "Identify missing critical information and launch controlled follow-up actions."),
            ("Duplicate pre-check", "Compare incoming reports against configured identity and event signals."),
            ("SLA visibility", "Track untriaged, incomplete, high-priority and ageing intake records."),
        ],
        "references": [(GVP_VI, "EMA GVP Module VI"), (ICH_E2D, "ICH E2D(R1) Step 4")],
        "related": [
            ("ICSR Validity and Case Processing", "/insights/quality-control-medical-review-pharmacovigilance"),
            ("Special Situations in PV", "/insights/special-situations-in-pharmacovigilance"),
            ("Partner Governance", "/insights/pharmacovigilance-agreements-partner-governance"),
        ],
        "faqs": [
            ("What does pharmacovigilance case intake automation cover?", "It covers controlled receipt, source preservation, awareness-date evidence, preliminary minimum-criteria identification, triage and routing into the case workflow."),
            ("Is intake the same as ICSR case processing?", "No. Intake establishes and preserves incoming safety information. Case processing performs the governed case assessment, coding, narrative, medical review, QC and submission preparation."),
            ("Can a non-safety employee trigger day zero?", "Regional rules and company procedures govern awareness, but safety information received by relevant parts of an organisation can affect regulatory timelines. Routing controls therefore matter."),
            ("Can AI declare a report valid automatically?", "ClinixAI can identify evidence and flag gaps, but authorised users confirm validity and regulatory consequences."),
        ],
    },
    {
        "slug": "icsr-case-processing-software",
        "eyebrow": "NEXUS ICSR WORKSPACE",
        "title": "ICSR Case Processing Software",
        "meta": "ICSR case processing software for governed adverse-event workflows, duplicate control, MedDRA and product coding, narratives, assessment, follow-up and E2B(R3) readiness.",
        "hook": "A completed data-entry form is not a scientifically coherent ICSR.",
        "promise": "Connect source evidence, structured data and medical reasoning throughout the case lifecycle.",
        "problem_title": "Case quality deteriorates when each processing step becomes a separate hand-off.",
        "problem": "Validity, duplicate assessment, coding, seriousness, expectedness, causality, narrative, follow-up and reportability are related decisions. Fragmented tools hide those relationships and make rework inevitable. Nexus Case Processing keeps evidence and decisions connected while preserving role-based accountability.",
        "steps": [
            ("01", "Validate", "Confirm minimum criteria, case type, source, receipt information and required follow-up."),
            ("02", "Structure", "Capture patient, reporter, products, events, tests, history and chronology with provenance."),
            ("03", "Assess", "Support coding, seriousness, expectedness, causality and reportability decisions."),
            ("04", "Review", "Route controlled medical review and quality review with query resolution."),
            ("05", "Prepare", "Produce submission-ready structured data and preserve every change in the audit trail."),
        ],
        "capabilities": [
            ("End-to-end case workspace", "Keep intake evidence, structured fields and review decisions in one controlled record."),
            ("Duplicate and linkage controls", "Identify potential duplicates and preserve follow-up, parent-child and case relationships."),
            ("Terminology integration", "Support governed MedDRA and medicinal-product coding workflows."),
            ("Narrative intelligence", "Assist chronology-based narrative preparation without adding unsupported facts."),
            ("Follow-up management", "Prioritise clinically meaningful missing information and document attempts."),
            ("E2B(R3) readiness", "Align structured output with electronic ICSR transmission requirements."),
        ],
        "references": [(GVP_VI, "EMA GVP Module VI"), (ICH_E2B, "ICH E2B(R3) specification"), (ICH_E2D, "ICH E2D(R1) Step 4")],
        "related": [
            ("ICSR Quality and Medical Review", "/insights/quality-control-medical-review-pharmacovigilance"),
            ("ICSR Quality-Control Checklist", "/insights/icsr-quality-control-pharmacovigilance"),
            ("ICSR Regulatory Submission", "/insights/icsr-regulatory-submission-e2b-r3"),
        ],
        "faqs": [
            ("What is ICSR case processing software?", "It is a controlled workspace for receiving, validating, structuring, coding, medically assessing, reviewing and preparing individual case safety reports."),
            ("Does ICSR software determine causality automatically?", "It may organise relevant evidence and support assessment, but medical and regulatory accountability remains with qualified professionals."),
            ("What is E2B(R3) readiness?", "It means case data can be structured and validated against the applicable ICH electronic ICSR specification and regional implementation requirements."),
            ("Can case processing and QC occur in the same workflow?", "Yes, but processing, medical review and quality review should retain distinct roles, controls and audit evidence."),
        ],
    },
    {
        "slug": "icsr-quality-control-automation",
        "eyebrow": "NEXUS QUALITY WORKSPACE",
        "title": "ICSR Quality Control Automation",
        "meta": "ICSR quality control automation for source-to-field verification, consistency checks, coding review, narrative reconciliation, reportability and submission readiness.",
        "hook": "Quality control is not a final spelling check. It is the last controlled challenge to whether the case tells the same scientific story as the source.",
        "promise": "Focus reviewers on material scientific risk while automation handles repeatable consistency checks.",
        "problem_title": "Checklist completion does not guarantee case integrity.",
        "problem": "A case can be technically complete and still be scientifically inconsistent: chronology may conflict with structured dates, seriousness may not match the clinical description, the narrative may omit decisive evidence, or the submission fields may differ from the approved assessment. Nexus Quality Workspace combines deterministic checks, evidence comparison and reviewer judgement.",
        "steps": [
            ("01", "Compare", "Reconcile source evidence against structured case fields and the narrative."),
            ("02", "Challenge", "Flag contradictions in dates, products, events, seriousness, assessments and reportability."),
            ("03", "Prioritise", "Rank findings by potential patient-safety, compliance and submission impact."),
            ("04", "Resolve", "Create attributable queries and preserve response, correction and approval history."),
            ("05", "Release", "Confirm critical controls and produce a defensible submission-readiness decision."),
        ],
        "capabilities": [
            ("Source-to-field verification", "Highlight omissions and mismatches between evidence and structured data."),
            ("Cross-field consistency", "Detect chronology, coding, seriousness and assessment contradictions."),
            ("Narrative reconciliation", "Compare decisive source facts with the approved case narrative."),
            ("Risk-based QC", "Apply defined review depth based on case type, complexity and compliance risk."),
            ("Query governance", "Track finding ownership, response, correction, approval and recurrence."),
            ("Quality intelligence", "Trend material errors by process, team, vendor, product and root-cause category."),
        ],
        "references": [(GVP_VI, "EMA GVP Module VI"), (ICH_E2B, "ICH E2B(R3) specification")],
        "related": [
            ("Complete ICSR QC Checklist", "/insights/icsr-quality-control-pharmacovigilance"),
            ("PV Quality Management System", "/insights/pharmacovigilance-quality-management-system"),
            ("PV KPIs and Compliance Metrics", "/insights/pharmacovigilance-kpis-compliance-metrics"),
        ],
        "faqs": [
            ("What can be automated in ICSR quality control?", "Deterministic validation, completeness checks, source-to-field comparison, consistency rules and finding prioritisation can be automated or assisted."),
            ("Can automation replace an ICSR QC reviewer?", "No. Material scientific interpretation, medical coherence and final approval require accountable human review."),
            ("What is risk-based ICSR QC?", "It applies controlled review depth based on defined risk factors while preserving mandatory checks and documented rationale."),
            ("How does QC automation support inspections?", "It preserves the check performed, evidence reviewed, finding, response, correction, reviewer and approval history."),
        ],
    },
    {
        "slug": "pharmacovigilance-medical-review-software",
        "eyebrow": "NEXUS MEDICAL REVIEW",
        "title": "Pharmacovigilance Medical Review Software",
        "meta": "Pharmacovigilance medical review software for clinically coherent ICSR assessment, seriousness, expectedness, causality, follow-up and evidence-grounded oversight.",
        "hook": "Medical review is where structured case data must become a clinically defensible safety assessment.",
        "promise": "Bring chronology, clinical evidence and governed reference information into one review decision.",
        "problem_title": "Medical judgement weakens when evidence is scattered across fields and attachments.",
        "problem": "Reviewers need to understand the patient, exposure, event course, investigations, dechallenge, rechallenge, alternative causes, seriousness and reference safety information as one clinical story. Nexus Medical Review assembles that context and highlights inconsistencies without pretending that an algorithm can own the judgement.",
        "steps": [
            ("01", "Orient", "Present the case chronology, source evidence, coded data and prior assessments together."),
            ("02", "Evaluate", "Review diagnosis, seriousness, expectedness, causality and alternative explanations."),
            ("03", "Challenge", "Identify missing clinical evidence, contradictions and follow-up priorities."),
            ("04", "Conclude", "Document the medical rationale, company assessment and regulatory consequences."),
            ("05", "Approve", "Preserve the responsible reviewer, evidence considered, version and final decision."),
        ],
        "capabilities": [
            ("Clinical chronology", "Transform fragmented dates and events into a reviewable exposure–event sequence."),
            ("Seriousness support", "Surface regulatory criteria and medically important-event considerations."),
            ("Expectedness context", "Present the controlled reference safety information and effective version."),
            ("Causality evidence", "Organise temporality, dechallenge, rechallenge, known association and alternatives."),
            ("Follow-up prioritisation", "Identify missing information most likely to change assessment or reportability."),
            ("Medical rationale traceability", "Preserve the evidence, reasoning, reviewer and approved conclusion."),
        ],
        "references": [(GVP_VI, "EMA GVP Module VI"), (ICH_E2D, "ICH E2D(R1) Step 4")],
        "related": [
            ("Medical Review of ICSRs", "/insights/icsr-medical-review-pharmacovigilance"),
            ("Quality Control and Medical Review", "/insights/quality-control-medical-review-pharmacovigilance"),
            ("Special Situations in Pharmacovigilance", "/insights/special-situations-in-pharmacovigilance"),
        ],
        "faqs": [
            ("What does pharmacovigilance medical review software support?", "It organises case chronology, source evidence, seriousness, expectedness, causality, follow-up needs and medical rationale for accountable review."),
            ("Does the software make the company causality assessment?", "No. It supports evidence review and consistency; the authorised medical reviewer owns the assessment."),
            ("How is expectedness supported?", "The workflow can present the governed reference safety information, version and relevant event terms for reviewer determination."),
            ("Can medical review occur before QC?", "Workflow order depends on controlled procedures, but the roles and decisions must be clear. ClinixAI supports configurable processing, medical-review and QC routing."),
        ],
    },
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def schema(page: dict) -> str:
    url = f"{BASE}/{page['slug']}"
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE}/#organization",
                "name": "TheClinixAI",
                "alternateName": ["ClinixAI", "The Clinix AI"],
                "url": f"{BASE}/",
                "logo": {"@type": "ImageObject", "url": f"{BASE}/icon-512.png"},
            },
            {
                "@type": "SoftwareApplication",
                "@id": f"{url}#software",
                "name": page["title"],
                "description": page["meta"],
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "Web",
                "provider": {"@id": f"{BASE}/#organization"},
            },
            {
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in page["faqs"]
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Nexus Platform", "item": f"{BASE}/nexus-platform"},
                    {"@type": "ListItem", "position": 3, "name": page["title"], "item": url},
                ],
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def render(page: dict) -> str:
    url = f"{BASE}/{page['slug']}"
    steps = "".join(
        f'<article class="solution-step"><span>{number}</span><h3>{esc(title)}</h3><p>{esc(copy)}</p></article>'
        for number, title, copy in page["steps"]
    )
    capabilities = "".join(
        f'<article class="solution-capability"><i></i><h3>{esc(title)}</h3><p>{esc(copy)}</p></article>'
        for title, copy in page["capabilities"]
    )
    references = " · ".join(
        f'<a href="{esc(link)}" target="_blank" rel="noopener">{esc(label)}</a>'
        for link, label in page["references"]
    )
    related = "".join(
        f'<a class="solution-related-card" href="{esc(link)}"><span>SCIENTIFIC GUIDE</span><strong>{esc(title)}</strong><b>Read evidence →</b></a>'
        for title, link in page["related"]
    )
    faqs = "".join(
        f'<details><summary>{esc(question)}</summary><p>{esc(answer)}</p></details>'
        for question, answer in page["faqs"]
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(page["title"])} | TheClinixAI</title>
<meta name="description" content="{esc(page["meta"])}"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}"><meta property="og:title" content="{esc(page["title"])} | TheClinixAI">
<meta property="og:description" content="{esc(page["meta"])}"><meta property="og:url" content="{url}">
<meta property="og:type" content="website"><meta property="og:image" content="{BASE}/assets/media/product-ui/ui-ai-nexus-console.png">
<meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/icon-32.png"><link rel="stylesheet" href="/style.css?v=20260723g">
<script type="application/ld+json">{schema(page)}</script></head>
<body class="solution-page"><a class="skip" href="#main">Skip to content</a><div id="site-header"></div><main id="main">
<section class="solution-hero"><div class="solution-orb solution-orb-a"></div><div class="solution-orb solution-orb-b"></div><div class="shell solution-hero-grid">
<div><p class="solution-kicker">{esc(page["eyebrow"])}</p><h1>{esc(page["title"])}</h1><p class="solution-hook">{esc(page["hook"])}</p>
<div class="actions"><a class="button button-primary" href="/contact">Book a discovery call</a><a class="button solution-ghost" href="#workflow">Explore the workflow</a></div></div>
<div class="solution-console"><span>GOVERNED WORKFLOW</span><strong>{esc(page["promise"])}</strong><div class="solution-console-lines"><i></i><i></i><i></i><i></i></div><small>Evidence · Control · Human accountability</small></div>
</div></section>
<section class="solution-trust"><div class="shell"><span>Source traceability</span><span>Role-based decisions</span><span>Version-controlled rules</span><span>Inspection-ready evidence</span></div></section>
<section class="solution-section"><div class="shell solution-problem"><p class="solution-kicker">THE OPERATIONAL RISK</p><h2>{esc(page["problem_title"])}</h2><p>{esc(page["problem"])}</p></div></section>
<section class="solution-section solution-section-dark" id="workflow"><div class="shell"><p class="solution-kicker">CONTROLLED END-TO-END FLOW</p><h2>One workflow. Five accountable decisions.</h2><div class="solution-steps">{steps}</div></div></section>
<section class="solution-section"><div class="shell"><div class="solution-section-head"><div><p class="solution-kicker">CAPABILITY ARCHITECTURE</p><h2>Designed around the work safety teams must defend.</h2></div><p>Automation handles repeatable structure. Qualified professionals retain scientific and regulatory authority.</p></div><div class="solution-capabilities">{capabilities}</div></div></section>
<section class="solution-section solution-governance"><div class="shell solution-governance-grid"><div><p class="solution-kicker">GOVERNED AI</p><h2>Assistance is visible. Accountability remains human.</h2></div><div><p>ClinixAI is designed to show the evidence, rule, model output, confidence, reviewer action and final disposition as separate records. The system does not convert an AI suggestion into an invisible regulatory decision.</p><ul><li>Defined intended use and controlled configuration</li><li>Tenant-specific knowledge and procedural context</li><li>Model, prompt, rule and knowledge versioning</li><li>Human override with attributable rationale</li><li>Performance monitoring and controlled change</li></ul></div></div></section>
<section class="solution-section"><div class="shell solution-regulatory"><p class="solution-kicker">REGULATORY CONTEXT</p><h2>Built to support governed execution—not to replace regional requirements.</h2><p>Configuration and validation must reflect the marketing authorisation holder’s products, procedures, territories and applicable requirements. Primary references for this solution include {references}.</p></div></section>
<section class="solution-section solution-science"><div class="shell"><div class="solution-section-head"><div><p class="solution-kicker">RELATED SCIENTIFIC GUIDANCE</p><h2>Explore the decisions behind the workflow.</h2></div></div><div class="solution-related">{related}</div></div></section>
<section class="solution-section"><div class="shell solution-faq"><p class="solution-kicker">QUESTIONS SAFETY LEADERS ASK</p><h2>Frequently asked questions</h2>{faqs}</div></section>
<section class="solution-final"><div class="shell"><div><p class="solution-kicker">EXPLORE NEXUS</p><h2>Bring this workflow into one governed safety-intelligence backbone.</h2></div><a class="button button-secondary" href="/contact">Discuss your operating model</a></div></section>
</main><div id="site-footer"></div><script src="/site.js"></script></body></html>'''


def update_nexus_links() -> None:
    path = ROOT / "nexus-platform.html"
    source = path.read_text(encoding="utf-8")
    replacements = {
        '<a class="button button-primary" href="contact.html">Explore More</a>': '<a class="button button-primary" href="/pharmacovigilance-literature-monitoring-software">Explore Literature Intelligence</a>',
        '<a class="button button-primary" href="contact.html">Explore Intake Workspace</a>': '<a class="button button-primary" href="/pharmacovigilance-case-intake-automation">Explore Intake Workspace</a>',
        '<a class="button button-primary" href="contact.html">Book a Demo</a>': '<a class="button button-primary" href="/icsr-case-processing-software">Explore Case Processing</a>',
        '<a class="button button-primary" href="contact.html">Let\'s Connect</a>': '<a class="button button-primary" href="/pharmacovigilance-medical-review-software">Explore Medical Review</a>',
        '<a class="button button-primary" href="contact.html">Quick Connect</a>': '<a class="button button-primary" href="/icsr-quality-control-automation">Explore Quality Control</a>',
    }
    for old, new in replacements.items():
        source = source.replace(old, new, 1)
    path.write_text(source, encoding="utf-8")


def main() -> None:
    for page in PAGES:
        (ROOT / f"{page['slug']}.html").write_text(render(page), encoding="utf-8")
    update_nexus_links()
    print(f"Generated {len(PAGES)} commercial solution pages.")


if __name__ == "__main__":
    main()
