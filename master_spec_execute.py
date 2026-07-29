#!/usr/bin/env python3
"""Execute the approved MASTER_SPEC against the static ClinixAI website."""
from pathlib import Path
from html import escape
import re
import subprocess

ROOT = Path(__file__).resolve().parent

SERVICES = [
    ("literature-monitoring", "Pharmacovigilance Literature Monitoring", "global and local literature surveillance", "search strategy governance, source scheduling, screening, duplicate control, full-text follow-up and traceable case identification", "EMA GVP Module VI, applicable local literature obligations and documented quality controls", ["Approved search strategy and product synonym set", "Search execution logs and reconciliation evidence", "Screening decisions with source traceability", "Escalation of valid safety information within agreed timelines"]),
    ("icsr-processing", "ICSR Case Processing", "end-to-end individual case safety report operations", "intake, validity assessment, triage, data entry, coding, narrative development, seriousness and expectedness assessment, follow-up and submission readiness", "ICH E2A, ICH E2B(R3), EMA GVP Module VI and client reporting procedures", ["Configured case-processing workflow", "MedDRA and medicinal-product coding controls", "Medical narrative and quality review package", "Submission-ready ICSR output and audit trail"]),
    ("signal-management", "Pharmacovigilance Signal Management", "governed signal detection and assessment", "data-source planning, signal detection, validation, prioritisation, assessment, recommendation tracking and closure documentation", "EMA GVP Module IX, CIOMS signal principles and approved benefit-risk governance", ["Signal detection plan and data-source map", "Validated signal assessment records", "Decision logs and governance minutes", "Tracked actions, owners and closure evidence"]),
    ("aggregate-reporting", "Aggregate Safety Reporting", "PSUR, PBRER, DSUR and related aggregate deliverables", "data lock planning, case and exposure reconciliation, signal integration, medical writing, quality control and submission coordination", "ICH E2C(R2), ICH E2F, EMA requirements and product-specific reporting schedules", ["Data lock and reconciliation plan", "Validated line listings and summary tabulations", "Medical and benefit-risk sections", "Quality-controlled submission package"]),
    ("medical-review", "Pharmacovigilance Medical Review", "clinically defensible safety assessment", "case-level review, chronology evaluation, seriousness, expectedness, causality context, listedness, follow-up strategy and medically coherent documentation", "ICH, CIOMS, EMA GVP and client medical-review conventions", ["Medical review checklist", "Clinically coherent case assessment", "Targeted follow-up recommendations", "Documented rationale for key medical decisions"]),
    ("regulatory-submissions", "Regulatory Safety Submissions", "timely and controlled safety reporting", "submission planning, gateway readiness, E2B validation, acknowledgement reconciliation, exception management and compliance tracking", "ICH E2B(R3), regional authority specifications and reporting timelines", ["Submission calendar and responsibility matrix", "Validated transmission package", "Acknowledgement and rejection reconciliation", "Compliance metrics and exception log"]),
    ("quality-management", "Pharmacovigilance Quality Management", "inspection-ready PV quality systems", "SOP governance, deviations, CAPA, change control, training compliance, metrics, document control and management review", "EMA GVP Module I, applicable GxP expectations and risk-based quality management", ["PV quality-system framework", "Controlled SOP and work-instruction set", "Deviation, CAPA and change-control records", "Quality metrics and management-review pack"]),
    ("psmf-management", "PSMF Management", "controlled pharmacovigilance system master file maintenance", "content ownership, annex governance, change tracking, evidence collection, reconciliation and inspection-ready retrieval", "EMA GVP Module II and organisation-specific PSMF procedures", ["PSMF content map and owner matrix", "Version-controlled main body and annexes", "Change log and evidence register", "Readiness review and remediation tracker"]),
    ("inspection-readiness", "Pharmacovigilance Inspection Readiness", "evidence-led inspection preparation", "readiness assessment, document indexing, process walkthroughs, interview preparation, mock inspection, finding triage and remediation governance", "EMA, MHRA, FDA and other applicable authority expectations", ["Inspection readiness diagnostic", "Evidence room index", "Mock interview and inspection records", "Prioritised remediation and CAPA plan"]),
    ("oracle-argus-safety", "Oracle Argus Safety Services", "regulated Argus configuration and operational support", "workflow assessment, configuration support, reporting rules, validation evidence, user acceptance testing, data quality and controlled release", "computerised-system validation expectations, E2B requirements and client change control", ["Configuration assessment and gap register", "Validated requirements and test evidence", "Operational workflow and role design", "Release and post-implementation support package"]),
    ("veeva-vault-safety", "Veeva Vault Safety Services", "governed Vault Safety implementation and optimisation", "process mapping, configuration support, migration readiness, validation, user acceptance testing, training and operational stabilisation", "GxP computerised-system controls, E2B standards and approved validation procedures", ["Process and configuration blueprint", "Migration and reconciliation controls", "Validation and UAT evidence", "Training and hypercare plan"]),
    ("pv-team-setup", "Pharmacovigilance Team Setup", "practical PV operating-model design", "role definition, workload planning, procedures, competency mapping, escalation paths, quality controls and performance governance", "company safety obligations, local requirements and risk-based operating controls", ["Target operating model", "Role and responsibility matrix", "Process maps and controlled procedures", "Competency, capacity and KPI framework"]),
    ("training-workforce", "PV Training and Workforce Development", "role-based pharmacovigilance capability building", "training-needs analysis, curriculum design, practical exercises, assessment, coaching, remediation and competency evidence", "approved procedures, regulatory expectations and job-specific competency requirements", ["Training-needs matrix", "Role-based learning pathway", "Practical assessment and coaching records", "Competency and effectiveness evidence"]),
    ("ai-strategy", "Responsible AI Strategy for Pharmacovigilance", "governed AI adoption in safety operations", "use-case qualification, risk classification, human oversight, data governance, validation planning, monitoring, explainability and controlled deployment", "GxP principles, privacy requirements, computerised-system controls and approved AI governance", ["AI opportunity and risk register", "Human-oversight and decision-rights model", "Validation and monitoring strategy", "Controlled implementation roadmap"]),
    ("vendor-oversight", "Pharmacovigilance Vendor Oversight", "measurable governance of outsourced safety activities", "due diligence, safety agreements, KPI and SLA design, governance meetings, issue escalation, audits, CAPA follow-up and continuity planning", "EMA GVP Module I, contractual safety responsibilities and organisation procedures", ["Vendor qualification and risk assessment", "Safety agreement responsibility matrix", "KPI, SLA and governance dashboard", "Issue, CAPA and continuity tracker"]),
]


def page_shell(title, description, canonical, body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | TheClinixAI</title><meta name="description" content="{escape(description)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><link rel="icon" href="/clinixai-favicon-v2.png"><link rel="stylesheet" href="/style.css?v=20260729-seo"></head><body><a class="skip" href="#main">Skip to content</a><div id="site-header"></div><main id="main">{body}</main><div id="site-footer"></div><script src="/site.js?v=20260729-seo" defer></script></body></html>'''


def service_page(slug, title, focus, scope, alignment, deliverables):
    deliverable_html = ''.join(f'<li>{escape(item)}</li>' for item in deliverables)
    related = [s for s, *_ in SERVICES if s != slug][:3]
    related_html = ''.join(f'<li><a href="/services/{s}">{escape(next(x[1] for x in SERVICES if x[0] == s))}</a></li>' for s in related)
    body = f'''<section class="hero"><div class="shell hero-grid"><div class="hero-copy"><p class="eyebrow">Pharmacovigilance Services</p><h1 class="display">{escape(title)}</h1><p class="lead">ClinixAI provides {escape(focus)} through controlled processes, qualified specialists and evidence that can be inspected, reviewed and improved.</p><a class="button button-primary" href="/contact">Request a Discovery Call</a></div></div></section>
<section class="scene"><div class="shell prose"><h2>Why this service matters</h2><p>{escape(title)} is not a collection of disconnected tasks. It is a governed safety capability that must protect reporting timelines, data quality, medical judgement and traceability at the same time. ClinixAI begins by understanding the product portfolio, regulatory footprint, operating model, case volumes, partner dependencies and existing procedural controls. We then define the service boundary, decision rights, escalation routes, quality checkpoints and measurable outcomes before delivery begins.</p><p>Our approach is designed for organisations that need more than temporary capacity. We establish a repeatable operating structure so that work can be performed consistently, reviewed objectively and defended during client governance, audit or inspection. The service can be delivered as a focused remediation, a managed work package, an implementation programme or an extension of an existing pharmacovigilance function.</p>
<h2>What the service includes</h2><p>The scope covers {escape(scope)}. Each activity is mapped to an accountable owner, an approved source of truth and a defined quality control. Inputs are checked for completeness before processing; decisions are documented with sufficient rationale; exceptions are escalated through agreed channels; and outputs are reconciled before closure. Where technology is involved, configuration and automation are treated as controlled enablers rather than substitutes for pharmacovigilance accountability.</p><p>ClinixAI also builds the supporting management layer: workload visibility, ageing controls, quality metrics, trend review and action tracking. This makes performance visible early, before isolated errors develop into systematic compliance risk. Client procedures and product-specific rules remain the governing standard, with ClinixAI methods configured around them.</p>
<h2>Delivery process</h2><ol><li><strong>Discover:</strong> confirm scope, stakeholders, systems, source documents, volumes, risks and success measures.</li><li><strong>Design:</strong> map the workflow, responsibilities, controls, templates, escalation logic and evidence requirements.</li><li><strong>Validate:</strong> test the operating approach using representative scenarios and resolve gaps before scale-up.</li><li><strong>Operate:</strong> deliver through trained personnel, active supervision, documented quality review and transparent reporting.</li><li><strong>Improve:</strong> analyse deviations, rework, delays and recurring questions to strengthen the process without weakening control.</li></ol>
<h2>Regulatory and quality alignment</h2><p>The service is aligned with {escape(alignment)}. Alignment does not mean inserting regulatory names into a document. It means converting obligations into operational controls: who acts, what evidence is retained, when escalation occurs, how quality is checked and how the organisation demonstrates continuing oversight. Any client-specific SOP, safety agreement, local requirement or product rule is assessed before implementation and incorporated into controlled instructions.</p>
<h2>Typical deliverables</h2><ul>{deliverable_html}</ul><p>Final deliverables are agreed during initiation and maintained under document control. Metrics are selected to measure compliance, quality, timeliness and operational stability rather than activity alone.</p>
<h2>Frequently asked questions</h2><h3>Can this service operate with our existing SOPs and systems?</h3><p>Yes. ClinixAI first assesses the approved procedures, system configuration, role model and known constraints. Delivery is then configured to the client environment. Where a gap is identified, it is documented and taken through the appropriate governance route rather than informally bypassed.</p><h3>How is quality demonstrated?</h3><p>Quality is demonstrated through trained-role assignment, controlled checklists, independent review where required, traceable decisions, reconciliation, deviation management and trend reporting. The exact control model is proportionate to regulatory risk and the maturity of the process.</p><h3>Can ClinixAI support remediation as well as routine operations?</h3><p>Yes. We can separate immediate containment from sustainable correction, establish a prioritised remediation plan, support root-cause analysis and CAPA, and then transition the strengthened process into routine governance with measurable effectiveness checks.</p>
<h2>Related services</h2><ul>{related_html}</ul><p><a class="button button-primary" href="/contact">Discuss your requirements</a></p></div></section>'''
    return page_shell(title, f"ClinixAI {title.lower()} support covering controlled delivery, regulatory alignment, quality evidence and inspection-ready governance.", f"https://www.theclinixai.com/services/{slug}", body)


def create_service_pages():
    directory = ROOT / "services"
    directory.mkdir(exist_ok=True)
    for service in SERVICES:
        slug = service[0]
        (directory / f"{slug}.html").write_text(service_page(*service), encoding="utf-8")


def create_insights_index():
    directory = ROOT / "insights"
    articles = sorted(p for p in directory.glob("*.html") if p.name != "index.html")
    cards = []
    for article in articles:
        raw = article.read_text(encoding="utf-8")
        title_match = re.search(r"<title>(.*?)</title>", raw, re.I | re.S)
        title = re.sub(r"\s*[|–-]\s*TheClinixAI.*$", "", title_match.group(1).strip(), flags=re.I) if title_match else article.stem.replace("-", " ").title()
        description_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', raw, re.I | re.S)
        desc = description_match.group(1).strip() if description_match else "Evidence-led pharmacovigilance guidance from TheClinixAI."
        cards.append(f'<article class="resource-card"><h2><a href="/insights/{article.stem}">{escape(title)}</a></h2><p>{escape(desc)}</p><a class="text-link" href="/insights/{article.stem}">Read guide →</a></article>')
    body = f'''<section class="hero"><div class="shell"><p class="eyebrow">Knowledge Centre</p><h1 class="display">Pharmacovigilance Insights &amp; Guides</h1><p class="lead">A complete, internally connected library of source-led guidance for drug-safety operations, quality systems, signal management, aggregate reporting and regulatory decisions.</p></div></section><section class="scene"><div class="shell"><div class="resource-grid">{''.join(cards)}</div></div></section>'''
    (directory / "index.html").write_text(page_shell("Pharmacovigilance Insights & Guides", "Explore the complete ClinixAI library of pharmacovigilance insights, regulatory guides and safety intelligence.", "https://www.theclinixai.com/insights", body), encoding="utf-8")
    print(f"Created /insights directory linking {len(articles)} articles")


def update_shared_navigation():
    header = ROOT / "header.html"
    raw = header.read_text(encoding="utf-8")
    raw = raw.replace('<a href="/resources#insights">Insights</a>', '<a href="/insights">Insights</a>')
    header.write_text(raw, encoding="utf-8")
    site = ROOT / "site.js"
    raw = site.read_text(encoding="utf-8")
    raw = raw.replace("path==='/resources'||path.startsWith('/insights/')", "path==='/resources'||path==='/insights'||path.startsWith('/insights/')")
    site.write_text(raw, encoding="utf-8")


def update_resources():
    path = ROOT / "resources.html"
    raw = path.read_text(encoding="utf-8")
    if 'href="/insights"' not in raw:
        marker = '</main>'
        block = '<section class="scene"><div class="shell cta-band"><div><h2>Explore the complete PV knowledge library</h2><p>Browse every ClinixAI pharmacovigilance insight and regulatory guide from one crawlable directory.</p></div><a class="button button-primary" href="/insights">View all insights →</a></div></section>'
        raw = raw.replace(marker, block + marker)
    path.write_text(raw, encoding="utf-8")


def update_services_hub():
    path = ROOT / "services.html"
    raw = path.read_text(encoding="utf-8")
    raw = raw.replace('href="contact.html"', 'href="/contact"')
    title_map = {title.lower(): slug for slug, title, *_ in SERVICES}
    aliases = {"literature monitoring":"literature-monitoring", "icsr processing":"icsr-processing", "signal management":"signal-management", "aggregate reporting":"aggregate-reporting", "medical review":"medical-review", "regulatory submissions":"regulatory-submissions", "quality management systems":"quality-management", "psmf management":"psmf-management", "inspection readiness":"inspection-readiness", "oracle argus safety":"oracle-argus-safety", "veeva vault safety":"veeva-vault-safety", "pv team setup":"pv-team-setup", "ai strategy":"ai-strategy", "vendor oversight":"vendor-oversight"}
    for label, slug in aliases.items():
        pattern = re.compile(rf'(<article class="service-card"><h3>{re.escape(label)}</h3><p>.*?</p>)(?!<a)', re.I | re.S)
        raw = pattern.sub(rf'\1<a class="text-link" href="/services/{slug}">Read more →</a>', raw)
    intro = '<section class="scene scene-soft"><div class="shell prose"><h2>Operational depth behind every service</h2><p>ClinixAI services are designed as governed pharmacovigilance capabilities, not isolated staffing tasks. Each engagement defines scope, accountable roles, source documents, quality controls, escalation pathways, metrics and inspection evidence before delivery begins. The detailed service pages below explain how priority capabilities are structured and controlled.</p><p><a class="button button-primary" href="/services/literature-monitoring">Explore detailed service capabilities</a></p></div></section>'
    if 'Operational depth behind every service' not in raw:
        raw = raw.replace('</section><section class="scene">', '</section>' + intro + '<section class="scene">', 1)
    path.write_text(raw, encoding="utf-8")


def run(command):
    print('+', ' '.join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main():
    create_service_pages()
    create_insights_index()
    update_shared_navigation()
    update_resources()
    update_services_hub()
    run(["python", "fix_links.py"])
    run(["python", "sitemap_generator.py"])
    run(["python", "html_audit.py"])
    print("MASTER_SPEC execution completed")


if __name__ == "__main__":
    main()
