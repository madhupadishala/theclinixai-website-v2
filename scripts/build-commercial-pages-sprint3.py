#!/usr/bin/env python3
"""Generate Sprint 3 commercial solution pages using the validated page system."""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = runpy.run_path(str(ROOT / "scripts" / "build-commercial-pages.py"))
render = ENGINE["render"]
GVP_VI = ENGINE["GVP_VI"]
ICH_E2B = ENGINE["ICH_E2B"]
ICH_E2D = ENGINE["ICH_E2D"]
GVP_IX = "https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-ix-signal-management-rev-1_en.pdf"
GVP_I = "https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/pharmacovigilance-post-authorisation/good-pharmacovigilance-practices-gvp"
GVP_V = "https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-module-v-risk-management-systems-rev-2_en.pdf"
ICH_E2C = "https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf"
ICH_E2F = "https://database.ich.org/sites/default/files/E2F_Guideline.pdf"


PAGES = [
    {
        "slug": "e2b-r3-regulatory-submission-management",
        "eyebrow": "NEXUS REGULATORY SUBMISSIONS",
        "title": "E2B(R3) Regulatory Submission Management",
        "meta": "E2B(R3) pharmacovigilance submission management for message validation, gateway transmission, acknowledgements, rejection handling and compliance evidence.",
        "hook": "A case is not submitted because an XML file was created. It is submitted only when the correct authority accepts the correct message within the applicable timeline.",
        "promise": "Control the full path from approved ICSR to accepted regulatory acknowledgement.",
        "problem_title": "Submission failure often remains invisible until the compliance clock has already expired.",
        "problem": "Technical validation, receiver rules, transmission, gateway availability, acknowledgement interpretation, rejection correction and retransmission are separate controls. When they are distributed across systems and inboxes, teams can mistake a sent message for an accepted report. Nexus Regulatory Submissions maintains one attributable evidence chain.",
        "steps": [
            ("01", "Determine", "Confirm receiver, report type, message version, due date and submission obligation."),
            ("02", "Validate", "Apply E2B(R3), controlled terminology and configured regional business rules."),
            ("03", "Transmit", "Send through the governed gateway while preserving payload, timestamp and destination."),
            ("04", "Reconcile", "Interpret acknowledgements, rejections and technical responses against the case record."),
            ("05", "Evidence", "Retain correction, retransmission, acceptance and compliance status in one audit trail."),
        ],
        "capabilities": [
            ("Receiver-rule control", "Apply configured authority, message and regional validation requirements."),
            ("Pre-transmission validation", "Identify structural and terminology failures before gateway dispatch."),
            ("Acknowledgement intelligence", "Associate technical and regulatory responses with the correct message."),
            ("Rejection workflow", "Route failures for correction, approval and controlled retransmission."),
            ("Submission reconciliation", "Compare required, attempted, accepted and outstanding transmissions."),
            ("Compliance oversight", "Monitor due dates, late risk, rejection ageing and final acceptance evidence."),
        ],
        "references": [(ICH_E2B, "ICH E2B(R3) specification"), (GVP_VI, "EMA GVP Module VI")],
        "related": [
            ("ICSR Regulatory Submission Guide", "/insights/icsr-regulatory-submission-e2b-r3"),
            ("ICSR Quality Control Checklist", "/insights/icsr-quality-control-pharmacovigilance"),
            ("PV KPIs and Compliance Metrics", "/insights/pharmacovigilance-kpis-compliance-metrics"),
        ],
        "faqs": [
            ("What does E2B(R3) submission management include?", "It includes message creation controls, validation, transmission, acknowledgements, rejection handling, retransmission, reconciliation and compliance evidence."),
            ("Is a transmitted ICSR automatically considered accepted?", "No. The applicable gateway and authority response must be evaluated. A transmission attempt and an accepted regulatory message are different states."),
            ("Can regional validation rules differ?", "Yes. ICH provides a harmonised specification, while regional implementation and business rules must be configured and maintained."),
            ("How are late or rejected cases controlled?", "The workflow preserves due dates, attempts, responses, corrections, approvals and retransmissions so compliance impact remains visible."),
        ],
    },
    {
        "slug": "pharmacovigilance-signal-management-software",
        "eyebrow": "NEXUS SIGNAL INTELLIGENCE",
        "title": "Pharmacovigilance Signal Management Software",
        "meta": "Pharmacovigilance signal management software for detection, validation, confirmation, prioritisation, assessment, action tracking and governance.",
        "hook": "A statistical alert becomes meaningful only when scientific evidence can justify what the safety organisation does next.",
        "promise": "Connect detection evidence, medical assessment and regulatory action in one governed signal record.",
        "problem_title": "Signal work becomes fragile when evidence and decisions live in separate repositories.",
        "problem": "Potential signals may originate from spontaneous reports, literature, studies, aggregate reviews, product quality information and regulatory intelligence. If validation evidence, meeting decisions, analyses and actions are scattered, the organisation cannot reconstruct why a signal was opened, closed, prioritised or escalated.",
        "steps": [
            ("01", "Detect", "Capture qualitative observations, quantitative alerts and cross-source safety evidence."),
            ("02", "Validate", "Determine whether the available information supports a new potentially causal association."),
            ("03", "Prioritise", "Evaluate seriousness, exposure, preventability, public-health impact and uncertainty."),
            ("04", "Assess", "Coordinate cumulative case, literature, epidemiological and mechanistic evaluation."),
            ("05", "Act", "Track conclusions, regulatory communication, labelling, risk minimisation and effectiveness."),
        ],
        "capabilities": [
            ("Multi-source detection", "Bring case, literature, study and regulatory evidence into a common review queue."),
            ("Validation workspace", "Document novelty, clinical relevance, known information and evidence sufficiency."),
            ("Prioritisation framework", "Apply governed criteria with visible scientific rationale."),
            ("Assessment planning", "Assign analyses, owners, milestones, data cuts and decision meetings."),
            ("Decision governance", "Preserve committee review, dissent, approval and closure evidence."),
            ("Action tracking", "Connect signal conclusions to labelling, RMP, communication and risk minimisation."),
        ],
        "references": [(GVP_IX, "EMA GVP Module IX"), (GVP_V, "EMA GVP Module V")],
        "related": [
            ("Signal Management in Pharmacovigilance", "/insights/signal-management-in-pharmacovigilance"),
            ("Signal Detection Methods", "/insights/pharmacovigilance-signal-detection"),
            ("Signal Validation and Prioritisation", "/insights/signal-validation-prioritisation-pharmacovigilance"),
        ],
        "faqs": [
            ("What is pharmacovigilance signal management software?", "It is a governed workspace for detecting, validating, confirming, prioritising, assessing and acting on new or changed safety information."),
            ("Is disproportionality evidence sufficient to confirm a signal?", "No. Disproportionality is one input and does not establish causality by itself. Clinical and contextual assessment remains necessary."),
            ("Can AI close a safety signal?", "ClinixAI does not position AI as the accountable authority for opening or closing signals. It can organise and prioritise evidence for expert review."),
            ("How does the system support inspection readiness?", "It preserves source evidence, criteria, analyses, meeting decisions, approvals, actions, timelines and closure rationale."),
        ],
    },
    {
        "slug": "aggregate-safety-reporting-software",
        "eyebrow": "NEXUS AGGREGATE REPORTING",
        "title": "Aggregate Safety Reporting Software",
        "meta": "Aggregate safety reporting software for PBRER, PSUR and DSUR planning, data lock, reconciliation, authoring, review, benefit-risk conclusions and submission readiness.",
        "hook": "An aggregate report is not a collection of sections. It is one controlled benefit–risk argument built from reconciled evidence.",
        "promise": "Control the reporting calendar, evidence cut, authoring decisions and final conclusion together.",
        "problem_title": "Aggregate reports lose coherence when contributors work from different data cuts.",
        "problem": "Case data, exposure, signals, studies, literature, regulatory actions and risk-management evidence must align to the same reporting context. Spreadsheet calendars and document-only workflows make late discrepancies difficult to detect and obscure who approved the final benefit–risk position.",
        "steps": [
            ("01", "Plan", "Govern reporting obligations, data-lock points, templates, contributors and milestones."),
            ("02", "Reconcile", "Confirm case, exposure, signal, study and regulatory datasets against the reporting cut."),
            ("03", "Author", "Create controlled sections with evidence provenance, ownership and version history."),
            ("04", "Review", "Coordinate medical, statistical, regulatory, quality and leadership review."),
            ("05", "Conclude", "Approve benefit–risk conclusions, actions, submission readiness and final evidence."),
        ],
        "capabilities": [
            ("Reporting calendar", "Control DLP, DIBD, frequency, region, owner, dependencies and submission dates."),
            ("Dataset reconciliation", "Identify differences between source systems, tabulations and report content."),
            ("Structured authoring", "Manage sections, evidence, contributors, comments, versions and approvals."),
            ("Signal integration", "Connect ongoing and closed safety topics to cumulative evaluation."),
            ("Benefit–risk governance", "Document key benefits, risks, uncertainty, conclusions and proposed actions."),
            ("Submission readiness", "Track final QC, approvals, regional packages and evidence of submission."),
        ],
        "references": [(ICH_E2C, "ICH E2C(R2) PBRER"), (ICH_E2F, "ICH E2F DSUR")],
        "related": [
            ("Aggregate Safety Reporting", "/insights/aggregate-safety-reporting-pharmacovigilance"),
            ("PBRER and PSUR Preparation", "/insights/pbrer-psur-preparation"),
            ("Aggregate Report Data Lock and QC", "/insights/aggregate-report-data-lock-quality-control"),
        ],
        "faqs": [
            ("Which reports can an aggregate safety platform support?", "A configurable platform can support PBRER/PSUR, DSUR and regional periodic obligations while preserving their distinct requirements."),
            ("What is the importance of the data-lock point?", "It defines the reporting cut against which case, exposure, study and other safety information must be reconciled."),
            ("Can AI write the benefit-risk conclusion?", "AI may assist evidence organisation and drafting, but qualified experts must evaluate and approve the scientific benefit–risk conclusion."),
            ("How does aggregate reporting connect to signal management?", "Signals and emerging safety issues should flow into cumulative evaluation, conclusions and resulting actions with traceability."),
        ],
    },
    {
        "slug": "pharmacovigilance-quality-management-system-software",
        "eyebrow": "NEXUS PV QUALITY",
        "title": "Pharmacovigilance Quality Management System Software",
        "meta": "Pharmacovigilance quality management system software for controlled documents, deviations, CAPA, audits, training, vendors, compliance metrics and inspection readiness.",
        "hook": "A pharmacovigilance system is inspection ready only when ordinary operational evidence supports what the procedures claim.",
        "promise": "Connect quality events, controls, ownership and effectiveness across the complete PV system.",
        "problem_title": "PV quality cannot be governed through disconnected trackers.",
        "problem": "Procedures, deviations, CAPAs, audits, training, vendors, agreements, metrics and PSMF evidence describe one pharmacovigilance system. When each is managed independently, recurring failures are hidden and leadership receives activity counts instead of risk intelligence.",
        "steps": [
            ("01", "Define", "Map controlled processes, roles, documents, training, vendors and critical controls."),
            ("02", "Observe", "Capture deviations, findings, overdue work, complaints and compliance signals."),
            ("03", "Investigate", "Assess impact, root cause, recurrence and systemic risk."),
            ("04", "Correct", "Govern CAPA design, ownership, due dates, evidence and effectiveness checks."),
            ("05", "Oversee", "Trend quality and compliance performance for management and inspection readiness."),
        ],
        "capabilities": [
            ("Controlled-document linkage", "Connect procedures and effective versions to operational processes and training."),
            ("Deviation and CAPA", "Preserve problem, containment, impact, root cause, action and effectiveness evidence."),
            ("Audit management", "Plan risk-based audits and track findings through verified closure."),
            ("Training governance", "Map role requirements, effective content, completion and competency evidence."),
            ("Vendor oversight", "Connect qualification, agreements, performance, reconciliation, issues and audits."),
            ("Quality intelligence", "Trend late work, recurrence, material errors, root causes and control effectiveness."),
        ],
        "references": [(GVP_I, "EMA GVP Module I"), (GVP_VI, "EMA GVP Module VI")],
        "related": [
            ("PV Quality Management System", "/insights/pharmacovigilance-quality-management-system"),
            ("PV Inspection Readiness", "/insights/pharmacovigilance-inspection-readiness"),
            ("PV KPIs and Compliance Metrics", "/insights/pharmacovigilance-kpis-compliance-metrics"),
        ],
        "faqs": [
            ("What should a pharmacovigilance QMS platform control?", "It should connect procedures, roles, training, deviations, CAPA, audits, vendors, metrics and inspection evidence around the PV system."),
            ("Is a general QMS sufficient for pharmacovigilance?", "A general QMS may support core quality processes, but PV-specific responsibilities, timelines, evidence and oversight must be represented."),
            ("What makes CAPA effectiveness defensible?", "Predetermined criteria, an appropriate monitoring period, representative evidence, recurrence assessment and documented approval."),
            ("How does the platform support the PSMF?", "It can connect current system descriptions, responsibilities, procedures, vendors, metrics and evidence needed to maintain an accurate PSMF."),
        ],
    },
    {
        "slug": "pharmacovigilance-agreement-partner-governance-software",
        "eyebrow": "NEXUS PARTNER GOVERNANCE",
        "title": "Pharmacovigilance Agreement and Partner Governance Software",
        "meta": "Pharmacovigilance agreement and partner governance software for SDEAs, responsibilities, exchange timelines, reconciliation, compliance oversight and evidence.",
        "hook": "Safety responsibility can be delegated operationally. Regulatory accountability cannot be made invisible inside a contract.",
        "promise": "Translate every agreement obligation into an owned, monitored and evidenced operational control.",
        "problem_title": "An executed SDEA is not proof that safety obligations are working.",
        "problem": "Partners may use different systems, day-zero definitions, exchange formats, seriousness assessments and submission responsibilities. If obligations remain inside static documents, late exchange, incomplete reconciliation and ambiguous ownership can persist until audit or inspection.",
        "steps": [
            ("01", "Map", "Structure products, territories, parties, activities, contacts and effective agreement versions."),
            ("02", "Operationalise", "Convert clauses into exchange rules, timelines, owners and evidence requirements."),
            ("03", "Exchange", "Track initial, follow-up, nullification and special-situation transfers."),
            ("04", "Reconcile", "Compare partner records, acknowledgements, submissions and literature responsibilities."),
            ("05", "Oversee", "Monitor compliance, deviations, CAPA, amendments, training and governance decisions."),
        ],
        "capabilities": [
            ("Agreement obligation register", "Structure responsibilities instead of leaving them buried in documents."),
            ("Case-exchange controls", "Track direction, timeline, format, acknowledgement and follow-up status."),
            ("Reconciliation workspace", "Identify missing, mismatched, duplicated and outstanding partner records."),
            ("Contact and escalation governance", "Maintain current operational and governance contacts by obligation."),
            ("Compliance monitoring", "Measure late exchange, overdue reconciliation, deviations and recurring failures."),
            ("Lifecycle management", "Control drafts, approvals, effective versions, amendments, termination and transition."),
        ],
        "references": [(GVP_VI, "EMA GVP Module VI"), (ICH_E2D, "ICH E2D(R1) Step 4")],
        "related": [
            ("PV Agreements and Partner Governance", "/insights/pharmacovigilance-agreements-partner-governance"),
            ("Safety Data Exchange Agreements", "/insights/safety-data-exchange-agreement-sdea"),
            ("Pharmacovigilance Reconciliation", "/insights/pharmacovigilance-reconciliation"),
        ],
        "faqs": [
            ("What is pharmacovigilance partner governance software?", "It converts agreement responsibilities into operational rules, owners, timelines, exchanges, reconciliations, metrics and evidence."),
            ("Does the system replace an SDEA?", "No. The executed agreement remains the governing document. The system operationalises and monitors its controlled obligations."),
            ("What should be reconciled between PV partners?", "Scope depends on the relationship but can include cases, follow-ups, submissions, literature, special situations, acknowledgements and aggregate responsibilities."),
            ("How are agreement amendments controlled?", "The workflow preserves draft, review, approval, effective date, training, changed obligations and transition evidence."),
        ],
    },
    {
        "slug": "end-to-end-pharmacovigilance-nexus-platform",
        "eyebrow": "THE CLINIXAI NEXUS PLATFORM",
        "title": "End-to-End Pharmacovigilance Nexus Platform",
        "meta": "An end-to-end pharmacovigilance platform connecting literature, intake, ICSR processing, medical review, QC, submissions, signals, aggregates and quality governance.",
        "hook": "Patient-safety decisions should not lose their evidence every time work moves from one pharmacovigilance function to another.",
        "promise": "One governed backbone connecting the complete safety-information lifecycle.",
        "problem_title": "The greatest PV risk often sits between systems—not inside them.",
        "problem": "Literature identifies a potential case. Intake establishes receipt. Case processing structures the evidence. Medical review evaluates it. QC challenges it. Submission communicates it. Signal and aggregate teams evaluate it cumulatively. When those stages are disconnected, provenance, decisions and accountability fragment at every hand-off.",
        "steps": [
            ("01", "Discover", "Retrieve and recognise safety information across literature and configured intake channels."),
            ("02", "Process", "Validate, structure, code, assess and follow up individual safety reports."),
            ("03", "Assure", "Apply medical review, quality control and controlled release decisions."),
            ("04", "Report", "Manage regulatory submissions, acknowledgements and periodic safety outputs."),
            ("05", "Learn", "Connect cumulative evidence to signals, risk management and quality improvement."),
        ],
        "capabilities": [
            ("Shared safety evidence", "Preserve source provenance as information moves between PV workspaces."),
            ("Governed knowledge", "Apply effective regulations, procedures, product data and tenant rules contextually."),
            ("Connected workflow states", "Make ownership, queue, decision, deadline and downstream status visible."),
            ("Role-based accountability", "Separate preparation, review, approval and release responsibilities."),
            ("Explainable AI assistance", "Expose evidence, rules, model output, confidence and reviewer disposition."),
            ("Enterprise oversight", "Connect compliance, quality, capacity, safety and governance intelligence."),
        ],
        "references": [(GVP_I, "EMA GVP Module I"), (GVP_VI, "EMA GVP Module VI"), (ICH_E2B, "ICH E2B(R3)")],
        "related": [
            ("ICSR Quality and Medical Review", "/insights/quality-control-medical-review-pharmacovigilance"),
            ("Signal Management", "/insights/signal-management-in-pharmacovigilance"),
            ("PV Quality Management System", "/insights/pharmacovigilance-quality-management-system"),
        ],
        "faqs": [
            ("What makes Nexus an end-to-end pharmacovigilance platform?", "It connects literature, intake, case processing, review, QC, submissions, signals, aggregate reporting and quality governance through shared evidence and controls."),
            ("Must every workspace be implemented at once?", "No. A modular implementation can begin with priority workflows while preserving a common governance and integration model."),
            ("Does Nexus replace the safety organisation's accountability?", "No. It is designed to strengthen controlled human decisions, traceability and oversight."),
            ("How is AI governed across the platform?", "AI assistance is constrained by intended use, approved context, versioning, evidence display, human review, validation and monitored change."),
        ],
    },
]


def update_platform_links() -> None:
    path = ROOT / "nexus-platform.html"
    source = path.read_text(encoding="utf-8")
    replacements = [
        ('<a class="button button-primary" href="contact.html">Explore More</a>', '<a class="button button-primary" href="/e2b-r3-regulatory-submission-management">Explore Submissions</a>'),
        ('<a class="button button-primary" href="contact.html">Quick Connect</a>', '<a class="button button-primary" href="/aggregate-safety-reporting-software">Explore Aggregate Reporting</a>'),
        ('<a class="button button-primary" href="contact.html">Explore More</a>', '<a class="button button-primary" href="/pharmacovigilance-signal-management-software">Explore Signal Management</a>'),
        ('<a class="button button-primary" href="contact.html">Let\'s Connect</a>', '<a class="button button-primary" href="/end-to-end-pharmacovigilance-nexus-platform">Explore Governed AI</a>'),
    ]
    for old, new in replacements:
        source = source.replace(old, new, 1)
    path.write_text(source, encoding="utf-8")


def main() -> None:
    for page in PAGES:
        (ROOT / f"{page['slug']}.html").write_text(render(page), encoding="utf-8")
    update_platform_links()
    print(f"Generated {len(PAGES)} Sprint 3 commercial pages.")


if __name__ == "__main__":
    main()
