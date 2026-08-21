#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup

INSIGHTS_DIR = Path(__file__).resolve().parent.parent / "insights"

ARTICLES = {

"aggregate-safety-reporting-pharmacovigilance": """
<p>An individual case asks, "What happened to this patient?" An aggregate report asks a harder question: "What does everything we now know mean for every patient exposed to this medicine?"</p>
<p>You can't answer that by compiling tables, copying last period's report, or listing signals without actually interpreting them.</p>
<p><strong>Aggregate reporting was never a periodic document-production exercise. It's the scheduled scientific reassessment of whether a medicine's benefits still outweigh its risks.</strong></p>
<p>Regulatory foundation: <a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a>; <a href="https://database.ich.org/sites/default/files/E2CR2_Q%26As_Q%26As.pdf" rel="noopener noreferrer" target="_blank">ICH E2C Q&amp;A</a>; <a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vii-periodic-safety-update-report-rev-1_en.pdf" rel="noopener noreferrer" target="_blank">GVP VII</a></p>
<h2 id="what-aggregate-safety-reporting-covers">What aggregate safety reporting covers</h2>
<p>Aggregate reports pull together cumulative and interval safety information across cases, studies, literature, signals, regulatory actions, exposure, and important efficacy developments. Which report type you're writing depends on where the product sits in its lifecycle and which jurisdiction you're in.</p>
<p>PBRER and PSUR come up most often in marketed-product contexts; DSUR covers investigational products still in development. Their data locks, content, and regulatory obligations aren't interchangeable — I've seen teams try to shortcut this and it never ends well.</p>
<h2 id="the-evidence-architecture">The evidence architecture</h2>
<p>A defensible report needs governed datasets and traceability running from source, through the table, to the final conclusion. Case counts alone don't mean much without exposure, reporting context, duplicates, coding strategy, and medically meaningful grouping behind them.</p>
<ul><li>Worldwide marketing-authorisation status and regulatory actions</li><li>Estimated exposure and limitations</li><li>Interval and cumulative case data</li><li>Study and literature findings</li><li>Signal evaluations and risk-management actions</li><li>Benefit information and therapeutic context</li><li>Integrated benefit–risk analysis</li></ul>
<h2 id="pbrer-psur-scientific-logic">PBRER/PSUR scientific logic</h2>
<p>ICH E2C(R2) puts benefit–risk evaluation at the center of everything. Sections shouldn't function as isolated summaries sitting next to each other. New safety information has to be interpreted against cumulative knowledge, exposure, indication, population, and available alternatives — not read in a vacuum.</p>
<h2 id="dsur-scientific-logic">DSUR scientific logic</h2>
<p>The DSUR is about the ongoing safety of the people exposed during development, right now. It pulls together serious adverse reactions, important risks, study changes, non-clinical information, regulatory actions, and the sponsor's honest assessment of whether trials can keep going safely.</p>
<h2 id="data-lock-authoring-and-governance">Data lock, authoring and governance</h2>
<p>Start planning before the data lock point, not after. Define responsibilities, source owners, query specifications, reconciliation, signal cut-offs, review cycles, and approval up front. If you discover a data inconsistency late, that's a governance failure — not just an inconvenient authoring hiccup.</p>
<h2 id="benefit-risk-evaluation">Benefit–risk evaluation</h2>
<p>The conclusion needs to name the key benefits, key risks, uncertainties, important changes, and whether more pharmacovigilance or risk minimisation is actually required. A favourable conclusion needs its own reasoning — it can't just get carried over from the previous reporting period because nothing "obviously" changed.</p>
<h2 id="automation-and-ai">Automation and AI</h2>
<p>Automation can generate validated listings, exposure tables, literature inventories, and consistency checks well. AI can help synthesize evidence and draft comparisons, but it can't independently decide where the benefit–risk balance actually lands.</p>
<p>Every generated statement needs to trace back to governed evidence, the effective data cut, and an accountable scientific reviewer who signed off on it.</p>
<h2 id="the-scientific-questions-every-aggregate-team-must-answer">The scientific questions every aggregate team must answer</h2>
<p>Interrogate the reporting period — don't just describe it. What changed in exposure? Which events increased or changed clinically? Did new studies shift the understanding of a risk or benefit? Did a signal assessment change the safety specification? Did regulatory action in one country create implications somewhere else? Did risk-minimisation data actually show an intervention worked — or that it didn't?</p>
<p>A useful report separates new information from new interpretation. Sometimes no new event shows up, and yet cumulative evidence still shifts severity, frequency, susceptible population, preventability, or clinical management. That kind of shift can matter just as much as discovering a brand-new reaction.</p>
<ul><li>Explain important interval changes against cumulative context.</li><li>State limitations of exposure and case ascertainment.</li><li>Reconcile signal conclusions with RMP and product information.</li><li>Identify concrete actions arising from the evaluation.</li></ul>
<h2 id="authoring-governance-and-cross-functional-accountability">Authoring governance and cross-functional accountability</h2>
<p>Aggregate reports get assembled across safety operations, medical review, biostatistics, epidemiology, clinical development, regulatory affairs, labelling, and risk management. The author shouldn't be finding out at final review that half these functions were working off different data cuts or product scopes — I've watched that discovery blow up a submission timeline more than once.</p>
<p>A controlled source matrix should spell out each input, system of record, owner, cut-off, format, reconciliation requirement, and approval. Resolve review comments with documented rationale, especially the ones that change a risk classification or a benefit–risk conclusion.</p>
<ul><li>Freeze governed datasets before final medical interpretation.</li><li>Use one controlled source for repeated numbers.</li><li>Record material judgement changes between drafts.</li><li>Link conclusions to follow-up actions and accountable owners.</li></ul>
<h2 id="a-practical-decision-scenario">A practical decision scenario</h2>
<p>Picture a reporting period where spontaneous case counts for a known risk jump 60%. Alarming, at first glance — until the exposure data shows a major market expansion and a communication campaign that stimulated more reporting. At the same time, the share of cases involving hospitalization has gone up in one vulnerable population. A strong aggregate report doesn't force a choice between "more reports" and "no change." It separates reporting volume from clinical pattern, evaluates severity by population, and works out whether targeted risk action is actually needed.</p>
<p>The governance lesson goes beyond this one example. A decision should never hang on a single metric, a single source, or one reviewer's unrecorded gut feeling. The full evidence chain — from detection or data extraction, through medical interpretation, cross-functional challenge, approval, and action — needs to stay visible the whole way through. That's what makes a pharmacovigilance system both scientifically credible and genuinely inspection-ready.</p>
<p>My own position on this is pretty firm: automation should speed up retrieval, reconciliation, and consistency checking. It shouldn't erase uncertainty or manufacture consensus that isn't really there. When evidence conflicts, the system needs to show that conflict, not smooth it over. When a person overrides an automated recommendation, that rationale needs to stay attributable. Speed and traceability have to improve together, or the whole thing isn't trustworthy.</p>
<h2 id="what-enterprise-grade-execution-adds">What enterprise-grade execution adds</h2>
<p>The aggregate strategy also has to account for regional schedules and formats. A global core evaluation can support several submissions, but local requirements, reporting frequencies, product scopes, and appendices can all differ underneath it. Reuse is only valuable if regional obligations stay visible and controlled — not quietly assumed to be the same everywhere.</p>
<p>Medical writing quality comes down to decision architecture. Reviewers should know which sections are descriptive, which are analytical, and which carry conclusions that could change labelling, studies, pharmacovigilance plans, or risk minimisation. Put review effort where the scientific consequence actually is — don't spread it evenly across every page just because that feels fair.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>Correct report type and data lock are confirmed.</li><li>Sources and owners are predefined.</li><li>Interval and cumulative datasets reconcile.</li><li>Exposure assumptions are explicit.</li><li>Signals and regulatory actions are current.</li><li>Benefits and risks are evaluated together.</li><li>Conclusions identify uncertainty and action.</li><li>Submission and acknowledgement evidence is retained.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-is-aggregate-safety-reporting">What is aggregate safety reporting?</h3>
<p>It is periodic cumulative evaluation of safety, exposure, benefits, signals and regulatory information for a medicinal product.</p>
<h3 id="what-is-the-difference-between-pbrer-and-dsur">What is the difference between PBRER and DSUR?</h3>
<p>PBRER focuses on marketed-product benefit–risk evaluation; DSUR focuses on investigational-product safety during development.</p>
<h3 id="is-a-psur-only-a-case-count-report">Is a PSUR only a case-count report?</h3>
<p>No. It requires integrated scientific evaluation, not merely listings and summary tabulations.</p>
<h3 id="can-ai-author-an-aggregate-report">Can AI author an aggregate report?</h3>
<p>It can assist with governed synthesis and consistency, but accountable experts must own interpretation and conclusions.</p>
<h2 id="conclusion">Conclusion</h2>
<p>A strong aggregate report doesn't hide uncertainty behind volume. It shows what changed, why it matters, and what happens next.</p>
<p>If you could have written the conclusion before you even reviewed the data, the report isn't doing its actual job.</p>
<p><strong>Periodic reporting only earns its place when each data lock forces the organisation to reconsider its benefit–risk position — not just repeat it.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a></li><li><a href="https://database.ich.org/sites/default/files/E2CR2_Q%26As_Q%26As.pdf" rel="noopener noreferrer" target="_blank">ICH E2C Q&amp;A</a></li><li><a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vii-periodic-safety-update-report-rev-1_en.pdf" rel="noopener noreferrer" target="_blank">GVP VII</a></li><li><a href="https://database.ich.org/sites/default/files/E2F_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2F</a></li><li><a href="https://database.ich.org/sites/default/files/M4E_R2__Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH M4E(R2)</a></li><li><a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-ix-signal-management-rev-1_en.pdf" rel="noopener noreferrer" target="_blank">GVP IX</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

"dsur-preparation-pharmacovigilance": """
<p>A clinical development programme can generate thousands of data points and still leave one essential question unanswered: is it still ethically and medically justified to keep exposing participants?</p>
<p>The DSUR exists to answer exactly that question, periodically and cumulatively.</p>
<p><strong>A DSUR isn't an annual archive of SUSARs. It's the sponsor's integrated safety judgment on the investigational drug and the people still being exposed to it right now.</strong></p>
<p>Regulatory foundation: <a href="https://database.ich.org/sites/default/files/E2F_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2F</a>; <a href="https://database.ich.org/sites/default/files/E2A_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2A</a>; <a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a></p>
<h2 id="purpose-and-scope">Purpose and scope</h2>
<p>ICH E2F sets a common annual format for safety reporting on investigational drugs. The DSUR pulls together worldwide development information for both the reporting period and the cumulative programme.</p>
<h2 id="development-international-birth-date-and-data-lock">Development international birth date and data lock</h2>
<p>Govern the DIBD, reporting period, product scope, combinations, and reference safety information tightly. Misalignment across trials is where incomplete or duplicated analysis usually starts.</p>
<h2 id="core-evidence">Core evidence</h2>
<p>Include worldwide authorisation status, actions taken for safety reasons, trial inventory, exposure, serious adverse reactions, important findings, non-clinical information, literature, signals, and any changes to the investigator's brochure.</p>
<h2 id="cumulative-safety-evaluation">Cumulative safety evaluation</h2>
<p>Analyze patterns across trials, doses, routes, populations, and indications. Be upfront about small numbers, unblinding limits, and comparator context — burying those caveats doesn't make the analysis stronger, it just makes it harder to trust.</p>
<h2 id="risks-and-trial-continuation">Risks and trial continuation</h2>
<p>Assess new risks for their impact on informed consent, protocol, monitoring, investigator communication, RSI, recruitment, or whether the trial can keep going at all.</p>
<h2 id="dsur-qc-and-governance">DSUR QC and governance</h2>
<p>Reconcile clinical, safety, regulatory, and non-clinical sources against each other. Make sure deaths, withdrawals, important deviations, and actions taken stay consistent across every section and appendix — inconsistencies here are exactly what an inspector notices first.</p>
<h2 id="the-scientific-questions-every-aggregate-team-must-answer">The scientific questions every aggregate team must answer</h2>
<p>Interrogate the reporting period — don't just describe it. What changed in exposure? Which events increased or changed clinically? Did new studies shift the understanding of a risk or benefit? Did a signal assessment change the safety specification? Did regulatory action in one country create implications somewhere else? Did risk-minimisation data actually show an intervention worked — or that it didn't?</p>
<p>A useful report separates new information from new interpretation. Sometimes no new event shows up, and yet cumulative evidence still shifts severity, frequency, susceptible population, preventability, or clinical management. That kind of shift can matter just as much as discovering a brand-new reaction.</p>
<ul><li>Explain important interval changes against cumulative context.</li><li>State limitations of exposure and case ascertainment.</li><li>Reconcile signal conclusions with RMP and product information.</li><li>Identify concrete actions arising from the evaluation.</li></ul>
<h2 id="authoring-governance-and-cross-functional-accountability">Authoring governance and cross-functional accountability</h2>
<p>Aggregate reports get assembled across safety operations, medical review, biostatistics, epidemiology, clinical development, regulatory affairs, labelling, and risk management. The author shouldn't be finding out at final review that half these functions were working off different data cuts or product scopes.</p>
<p>A controlled source matrix should spell out each input, system of record, owner, cut-off, format, reconciliation requirement, and approval. Resolve review comments with documented rationale, especially the ones that change a risk classification or a benefit–risk conclusion.</p>
<ul><li>Freeze governed datasets before final medical interpretation.</li><li>Use one controlled source for repeated numbers.</li><li>Record material judgement changes between drafts.</li><li>Link conclusions to follow-up actions and accountable owners.</li></ul>
<h2 id="a-practical-decision-scenario">A practical decision scenario</h2>
<p>Picture a reporting period where spontaneous case counts for a known risk jump 60%. Alarming, at first glance — until the exposure data shows a major market expansion and a communication campaign that stimulated more reporting. At the same time, the share of cases involving hospitalization has gone up in one vulnerable population. A strong aggregate report doesn't force a choice between "more reports" and "no change." It separates reporting volume from clinical pattern, evaluates severity by population, and works out whether targeted risk action is actually needed.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>DIBD and scope are governed.</li><li>Trial inventory and exposure reconcile.</li><li>SUSAR and death data are complete.</li><li>RSI version is correct.</li><li>Signals and actions are current.</li><li>Participant-protection implications are explicit.</li><li>Approvals and submissions are traceable.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-is-a-dsur">What is a DSUR?</h3>
<p>An annual cumulative safety report for investigational drugs during clinical development.</p>
<h3 id="is-a-dsur-the-same-as-a-pbrer">Is a DSUR the same as a PBRER?</h3>
<p>No. DSUR focuses on development safety and trial participants; PBRER focuses on marketed-product benefit–risk.</p>
<h3 id="what-is-the-dibd">What is the DIBD?</h3>
<p>The development international birth date used to establish the annual reporting cycle.</p>
<h3 id="does-the-dsur-replace-expedited-susar-reporting">Does the DSUR replace expedited SUSAR reporting?</h3>
<p>No. Periodic reporting and expedited reporting serve different obligations.</p>
<h2 id="conclusion">Conclusion</h2>
<p>A DSUR should say clearly whether the evidence still supports continuing development — and what needs to change to protect participants if the safety profile has shifted.</p>
<p><strong>If a DSUR doesn't actually change how the programme gets monitored, communicated, or governed, it's stopped being patient protection and turned into paperwork.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://database.ich.org/sites/default/files/E2F_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2F</a></li><li><a href="https://database.ich.org/sites/default/files/E2A_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2A</a></li><li><a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

}


def replace_article(slug, new_html):
    path = INSIGHTS_DIR / f"{slug}.html"
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    article = soup.select_one("article.article-content")
    new_soup = BeautifulSoup(new_html, "html.parser")
    article.clear()
    for child in list(new_soup.children):
        article.append(child)
    path.write_text(str(soup), encoding="utf-8")
    return True


def main():
    for slug, html in ARTICLES.items():
        replace_article(slug, html)
        print(f"OK: {slug}.html")


if __name__ == "__main__":
    main()
