#!/usr/bin/env python3
"""Batch 2 of insights de-AI-ification: 3 of Dr. Harsha's CT-safety articles."""
from pathlib import Path
from bs4 import BeautifulSoup

INSIGHTS_DIR = Path(__file__).resolve().parent.parent / "insights"

ARTICLES = {

"susar-assessment-reporting-timelines": """
<p>I get asked to sign off on more "obvious" SUSARs than I'd like — fatal events, alarming lab values, cases that feel urgent the moment you read them. Feeling urgent doesn't make something a SUSAR. A fatal event isn't automatically one. An unexpected event isn't automatically one. Even a serious, unexpected event isn't a SUSAR unless there's a reasonable suspicion the investigational product actually caused it.</p>
<p>Speed matters, sure. But speed without the right classification just adds noise, and noise makes it harder to see the safety signal that's actually there.</p>
<p><strong>A SUSAR isn't shorthand for "this looks alarming." It's a conclusion you build from three separate things: seriousness, suspected causality, and unexpectedness.</strong></p>
<p>Regulatory foundation: <a href="https://database.ich.org/sites/default/files/E2A_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2A</a>; <a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/reporting-safety-information-clinical-trials" rel="noopener noreferrer" target="_blank">EMA clinical-trial safety reporting</a>; <a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/clinical-trials-regulation" rel="noopener noreferrer" target="_blank">EU Clinical Trials Regulation</a>; <a href="https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sponsor-responsibilities-safety-reporting-requirements-and-safety-assessment-ind-and" rel="noopener noreferrer" target="_blank">FDA Sponsor Safety Guidance</a></p>
<h2 id="the-three-part-susar-test">The three-part SUSAR test</h2>
<p>First: does the event meet a seriousness criterion? Second: is there a reasonable possibility of a causal relationship? Third: how does the reaction's nature and severity compare against the applicable RSI? All three need to hold up before I'll call something a SUSAR.</p>
<h2 id="seriousness">Seriousness</h2>
<p>Document the exact criterion and the facts behind it. "Severe" on its own isn't enough — medically important events can qualify even without a hospitalization, if intervention was needed to prevent a serious outcome. Fatal and life-threatening cases get triaged first, every time.</p>
<h2 id="causality">Causality</h2>
<p>I look at temporal relationship, mechanism, dose, dechallenge, rechallenge, alternative causes, underlying disease, concomitant therapies, and class evidence — and I keep both the investigator's and the sponsor's opinions on file. You can't justify under-reporting just because the sponsor disagrees, where the rules call for reporting based on either party's reasonable assessment.</p>
<h2 id="expectedness-and-the-rsi">Expectedness and the RSI</h2>
<p>Expectedness is a regulatory comparison, not a question of whether a clinician could picture the event happening. Use the controlled RSI that applies to the trial, region, and assessment date. A reaction can still be unexpected even if something similar is listed, if the specificity, severity, or outcome differs meaningfully.</p>
<h2 id="seven-and-fifteen-day-reporting">Seven- and fifteen-day reporting</h2>
<p>Fatal or life-threatening SUSARs generally need an initial report as soon as possible, and no later than seven calendar days, under EU/ICH-aligned frameworks — with follow-up handled per applicable rules. Other SUSARs generally follow a fifteen-day window. These are regulatory maximums, not something to aim for. Destination, clock start, and follow-up obligations all differ by jurisdiction, so don't assume one region's rule applies everywhere.</p>
<h2 id="blinded-trials">Blinded trials</h2>
<p>You need a controlled mechanism to determine treatment assignment when reporting requires it, while still limiting access to protect trial integrity. Placebo cases and comparator responsibilities need protocol- and region-specific handling. Every unblinding action should be attributable — I want to know exactly who did it, when, and why, every time.</p>
<h2 id="follow-up-amendment-and-downgrade">Follow-up, amendment, and downgrade</h2>
<p>Submit material follow-up as it comes in — don't wait for a perfect final narrative. If later evidence changes the diagnosis, seriousness, causality, or expectedness, update the report transparently rather than quietly erasing the earlier decision. A downgrade doesn't mean the original assessment was made in bad faith.</p>
<h2 id="communicating-new-risk">Communicating new risk</h2>
<p>Filing the expedited report doesn't automatically protect participants. Investigators and ethics bodies may need prompt notification when something materially affects conduct, consent, or safety measures. That said, blasting out every unassessed single case creates its own problem — alert fatigue that makes people tune out the notifications that actually matter.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>Seriousness criterion evidenced.</li><li>Causality medically reasoned.</li><li>Correct RSI version used.</li><li>Nature and severity compared.</li><li>Clock start documented.</li><li>Fatal/life-threatening cases prioritised.</li><li>Unblinding controlled.</li><li>Destinations regionally mapped.</li><li>Follow-up and acknowledgements tracked.</li><li>Investigator communication is risk-based.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-does-susar-stand-for">What does SUSAR stand for?</h3>
<p>Suspected unexpected serious adverse reaction.</p>
<h3 id="are-all-fatal-saes-susars">Are all fatal SAEs SUSARs?</h3>
<p>No. Causality and unexpectedness must also be assessed.</p>
<h3 id="what-is-the-seven-day-rule">What is the seven-day rule?</h3>
<p>Fatal or life-threatening SUSARs generally require initial expedited reporting as soon as possible and no later than seven calendar days under applicable frameworks.</p>
<h3 id="what-is-the-fifteen-day-rule">What is the fifteen-day rule?</h3>
<p>Other qualifying SUSARs generally require reporting within fifteen calendar days, subject to regional requirements.</p>
<h3 id="can-expectedness-be-assessed-from-general-medical-knowledge">Can expectedness be assessed from general medical knowledge?</h3>
<p>No. Regulatory expectedness is assessed against the applicable controlled RSI.</p>
<h2 id="conclusion">Conclusion</h2>
<p>SUSAR reporting earns credibility when whoever's receiving it can see the evidence behind every word: suspected, unexpected, serious, reaction.</p>
<p>The goal was never to maximize how many reports go out. It's to get important new risks communicated fast enough to protect participants, without drowning the real signal in poorly assessed noise.</p>
<p><strong>Fast reporting protects the clock. Disciplined assessment protects the science.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://database.ich.org/sites/default/files/E2A_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2A</a></li><li><a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/reporting-safety-information-clinical-trials" rel="noopener noreferrer" target="_blank">EMA clinical-trial safety reporting</a></li><li><a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/clinical-trials-regulation" rel="noopener noreferrer" target="_blank">EU Clinical Trials Regulation</a></li><li><a href="https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sponsor-responsibilities-safety-reporting-requirements-and-safety-assessment-ind-and" rel="noopener noreferrer" target="_blank">FDA Sponsor Safety Guidance</a></li><li><a href="https://www.ema.europa.eu/en/documents/other/clinical-trial-information-system-ctis-sponsor-handbook_en.pdf" rel="noopener noreferrer" target="_blank">CTIS Sponsor Handbook</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

"development-safety-update-report-dsur": """
<p>I've reviewed DSURs where every required section was present, the tables reconciled, the case listings were complete, and the submission went out on time — and the report still failed at the one thing it was supposed to do: tell anyone whether the risk to trial participants had actually changed.</p>
<p>A DSUR isn't an annual archive. It's the sponsor's documented safety judgment across the whole development programme, and that judgment is either defensible or it isn't.</p>
<p><strong>The value of a DSUR was never about how much data got assembled. It's about the quality of the decision that comes out the other end.</strong></p>
<p>Regulatory foundation: <a href="https://database.ich.org/sites/default/files/E2F_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2F</a>; <a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/reporting-safety-information-clinical-trials" rel="noopener noreferrer" target="_blank">EMA clinical-trial safety reporting</a>; <a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/clinical-trials-regulation" rel="noopener noreferrer" target="_blank">EU Clinical Trials Regulation</a>; <a href="https://www.ema.europa.eu/en/documents/other/clinical-trial-information-system-ctis-sponsor-handbook_en.pdf" rel="noopener noreferrer" target="_blank">CTIS Sponsor Handbook</a></p>
<h2 id="what-is-a-dsur">What is a DSUR?</h2>
<p>The Development Safety Update Report is the ICH common standard for annual safety reporting on investigational drugs, including marketed products under further study. It summarizes interval findings, cumulative experience, and the sponsor's evolving read on risk. Regional submission requirements and recipients still need to be mapped separately — the DSUR format doesn't handle that for you.</p>
<h2 id="development-international-birth-date-and-reporting-period">Development international birth date and reporting period</h2>
<p>The DIBD anchors the whole annual cycle. Data lock, reporting interval, submission due dates, and first/last report logic all need to be controlled consistently across regions and studies. Administrative cut-offs and mid-cycle changes shouldn't create gaps or double-counted periods — I've seen both happen when this isn't tightly governed.</p>
<h2 id="governance-and-planning">Governance and planning</h2>
<p>Name an accountable author, a medical lead, a regulatory lead, data owners, reviewers, and an approver. Start with a content plan, a source inventory, prior commitments, current signal status, and known data limitations. Collecting data late compresses the analysis window and turns what should be scientific review into last-minute document assembly.</p>
<h2 id="data-sources-and-reconciliation">Data sources and reconciliation</h2>
<p>Pull together clinical-trial exposure, interval and cumulative cases, deaths, withdrawals, study status, nonclinical findings, literature, regulatory actions, safety-relevant manufacturing information, and any significant external evidence. Then reconcile the safety database against the clinical database, study listings, exposure calculations, SUSAR submissions, and prior DSUR totals — this is where most of the real errors hide.</p>
<h2 id="estimated-exposure">Estimated exposure</h2>
<p>Present interval and cumulative exposure along with your methods, assumptions, and limitations. Stratify meaningfully by treatment, dose, population, or programme context where you can, without breaking the blind. A precise-looking denominator built on weak assumptions should be described honestly as exactly that.</p>
<h2 id="case-information-and-summary-tabulations">Case information and summary tabulations</h2>
<p>Present serious adverse reactions and relevant cases consistently, with clear coding versions and case cut-off rules, and explain any material differences from previous reports. Listings are evidence inputs. They are not the analysis, and treating them as one is a mistake I see fairly often.</p>
<h2 id="significant-findings-and-actions">Significant findings and actions</h2>
<p>Discuss completed and ongoing studies, nonclinical information, literature, other DSURs, lack of efficacy where it's safety-relevant, and any important manufacturing changes. Describe what safety actions were taken and why. Connect the dots across sources instead of reporting each one in its own isolated section.</p>
<h2 id="overall-safety-assessment">Overall safety assessment</h2>
<p>Evaluate identified and potential risks, new information on known risks, and how population, dose, duration, and interactions play into the picture, along with remaining uncertainties. Say plainly whether the investigator's brochure, protocol, consent, monitoring, or development plan should change as a result. State disagreements and evidence limitations openly — hiding them doesn't make the DSUR stronger, it makes it weaker.</p>
<h2 id="benefit-risk-conclusions">Benefit–risk conclusions</h2>
<p>The conclusion needs to integrate efficacy or anticipated benefit with cumulative risk in the context of where development actually stands. It should name emerging issues, planned investigations, and risk controls, each with an accountable timeline. "The benefit–risk remains favourable" isn't a conclusion by itself — it needs the reasoning behind it spelled out.</p>
<h2 id="quality-control-and-inspection-readiness">Quality control and inspection readiness</h2>
<p>Check cross-section consistency, table totals, RSI version, DIBD, submission history, actions taken, references, and sign-off. Keep the datasets, queries, decisions, and approvals that built the report — an inspector should be able to reproduce the important conclusions straight from your governed sources.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>DIBD and reporting period verified.</li><li>Regional requirements mapped.</li><li>Prior DSUR commitments reviewed.</li><li>Study status and exposure reconcile.</li><li>Case counts match governed sources.</li><li>SUSAR and submission data reconcile.</li><li>Signals and actions are current.</li><li>New nonclinical and literature evidence assessed.</li><li>Benefit–risk reasoning is explicit.</li><li>Limitations and missing data disclosed.</li><li>Review and approval are attributable.</li><li>Post-submission commitments are tracked.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="how-often-is-a-dsur-prepared">How often is a DSUR prepared?</h3>
<p>Generally annually, anchored to the development international birth date, subject to regional requirements.</p>
<h3 id="what-does-a-dsur-cover">What does a DSUR cover?</h3>
<p>The worldwide development programme for the investigational drug, integrating interval and cumulative safety information and benefit–risk assessment.</p>
<h3 id="is-a-dsur-only-a-case-line-listing-report">Is a DSUR only a case-line-listing report?</h3>
<p>No. Listings and tabulations support the central purpose: cumulative safety and benefit–risk evaluation.</p>
<h3 id="can-one-dsur-cover-multiple-indications">Can one DSUR cover multiple indications?</h3>
<p>ICH E2F generally supports one DSUR for one investigational drug across indications where appropriate, with meaningful stratification and explanation.</p>
<h3 id="what-is-the-biggest-dsur-quality-risk">What is the biggest DSUR quality risk?</h3>
<p>A report that compiles complete data but fails to analyse whether the safety profile or participant-protection measures should change.</p>
<h2 id="conclusion">Conclusion</h2>
<p>A strong DSUR lets leadership, investigators, and regulators see not just what happened over the year, but what the total evidence actually means now.</p>
<p>Its credibility comes from reconciled data, honestly stated uncertainty, and actions that actually follow from the conclusion — not just restate it.</p>
<p><strong>A DSUR only closes one reporting period by opening the next safety decision.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://database.ich.org/sites/default/files/E2F_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2F</a></li><li><a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/reporting-safety-information-clinical-trials" rel="noopener noreferrer" target="_blank">EMA clinical-trial safety reporting</a></li><li><a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/clinical-trials-regulation" rel="noopener noreferrer" target="_blank">EU Clinical Trials Regulation</a></li><li><a href="https://www.ema.europa.eu/en/documents/other/clinical-trial-information-system-ctis-sponsor-handbook_en.pdf" rel="noopener noreferrer" target="_blank">CTIS Sponsor Handbook</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

"clinical-trial-safety-pharmacovigilance": """
<p>A participant is hospitalized during a blinded trial. The investigator calls the event unrelated. The sponsor's medical reviewer sees a plausible mechanism. The reference safety information lists something similar — but with a different severity and outcome.</p>
<p>The case doesn't become a SUSAR because one person ticks a box. It becomes a regulatory decision only once seriousness, causality, and expectedness have all been assessed against controlled evidence.</p>
<p>Clinical-trial safety, then, isn't case forwarding. It's continuous, traceable medical judgment applied to protect participants.</p>
<p><strong>The investigator sees the participant. The sponsor sees the whole development programme. You need both perspectives for a safe decision — but accountability can't get blurred between them.</strong></p>
<p>Regulatory foundation: <a href="https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf" rel="noopener noreferrer" target="_blank">ICH E6(R3)</a>; <a href="https://database.ich.org/sites/default/files/E2A_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2A</a>; <a href="https://database.ich.org/sites/default/files/E2F_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2F</a>; <a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/reporting-safety-information-clinical-trials" rel="noopener noreferrer" target="_blank">EMA clinical-trial safety reporting</a></p>
<h2 id="why-clinical-trial-safety-is-different-from-post-marketing-pharmacovigilance">Why clinical-trial safety is different from post-marketing pharmacovigilance</h2>
<p>During development, exposure is protocol-controlled, data get actively collected, and the safety profile is still forming. The protocol, investigator's brochure, reference safety information, randomization, and study endpoints all shape how you assess a case.</p>
<p>Don't just copy post-marketing terminology into a trial context. Clinical-trial safety runs on pre-authorization requirements, study documents, and regional rules that don't map cleanly onto post-marketing frameworks.</p>
<h2 id="the-safety-information-chain">The safety-information chain</h2>
<p>It starts with the participant and the site, moves through investigator assessment and sponsor receipt, and continues through medical review, case processing, aggregate evaluation, regulatory reporting, investigator communication, and safety governance. A delay at any single point in that chain eats into the short reporting window you have left after sponsor awareness.</p>
<ul><li>Participant observation and clinical care.</li><li>Site documentation and investigator assessment.</li><li>Rapid SAE transmission to the sponsor.</li><li>Sponsor-wide medical and aggregate evaluation.</li><li>SUSAR reporting and investigator communication.</li><li>Ongoing benefit–risk and trial action.</li></ul>
<h2 id="ae-ar-sae-and-sar-are-not-interchangeable">AE, AR, SAE, and SAR aren't interchangeable</h2>
<p>An adverse event doesn't require a causal link. An adverse reaction carries a reasonable possibility of one. Seriousness comes from outcome criteria and medical importance — not from how intense the symptom felt. A serious adverse reaction only becomes a SUSAR once it's also unexpected against the applicable reference safety information.</p>
<h2 id="investigator-responsibilities">Investigator responsibilities</h2>
<p>The investigator's job is to protect the participant, provide the right medical care, document what happened, and report serious adverse events to the sponsor promptly, per the protocol and applicable rules. Don't wait for complete records before reporting — follow-up can fill in the missing detail later. The investigator's causality assessment is essential source evidence, but it doesn't remove the sponsor's own obligation to make its own assessment.</p>
<h2 id="sponsor-responsibilities">Sponsor responsibilities</h2>
<p>The sponsor has to maintain systems that can receive safety information, evaluate individual and aggregate data, determine reportability, submit required reports, inform investigators and authorities, update safety documents, and act when the risk picture changes. Delegating to a CRO or vendor doesn't remove sponsor responsibility — the agreements, oversight, reconciliation, and escalation paths all need to protect the reporting clock regardless of who's doing the day-to-day work.</p>
<h2 id="seriousness-causality-and-expectedness">Seriousness, causality, and expectedness</h2>
<p>These are three separate decisions, not one. Seriousness evaluates outcome. Causality evaluates whether there's a reasonable possibility the investigational product caused the event. Expectedness compares the nature and severity of the reaction against the approved reference safety information. A known clinical concept isn't automatically expected if the specificity or severity you're actually seeing doesn't match the RSI.</p>
<h2 id="the-susar-decision">The SUSAR decision</h2>
<p>A SUSAR is suspected, unexpected, and serious — all three need support. Keep the investigator's and sponsor's causality positions, the effective RSI version, the medical reasoning, and any unblinding decision on record. Fatal or life-threatening SUSARs generally follow the shorter seven-day initial reporting window under the major frameworks; others generally follow fifteen days. Exact destinations and follow-up obligations stay jurisdiction-specific.</p>
<h2 id="blinding-and-controlled-unblinding">Blinding and controlled unblinding</h2>
<p>Blinding protects trial integrity, but participant safety and regulatory compliance can require identifying the treatment. Unblinding should follow the protocol and a controlled procedure, stay limited to people who genuinely need the information, and leave a clear record of who knew what and when. Operational convenience isn't a reason to break the blind. Avoiding a reportable safety assessment isn't a reason to keep it intact.</p>
<h2 id="reference-safety-information-governance">Reference safety information governance</h2>
<p>The RSI needs to be identifiable, approved, and version-controlled. Assess expectedness against the version that actually applies to the trial and jurisdiction, with clear effective dates and transition rules. Safety reviewers need the exact wording in front of them — not an informal list of "expected events" someone remembers from memory.</p>
<h2 id="follow-up-and-case-quality">Follow-up and case quality</h2>
<p>High-value follow-up addresses diagnosis, onset, seriousness criterion, dose, treatment dates, dechallenge, rechallenge, alternative causes, relevant tests, concomitant therapies, and outcome. Ask questions that actually reflect the clinical question you're trying to answer. Source-data corrections, case amendments, and significant follow-up all need to stay attributable and auditable.</p>
<h2 id="aggregate-assessment-and-dsur">Aggregate assessment and DSUR</h2>
<p>Some risks only become visible when you look across participants, treatment arms, studies, or external sources. The DSUR pulls together interval safety data with cumulative exposure, important findings, actions taken, and the evolving benefit–risk picture. A programme can hit every individual SUSAR timeline and still fail participant protection if nobody's evaluating the pattern across cases.</p>
<h2 id="actions-beyond-reporting">Actions beyond reporting</h2>
<p>New information might call for urgent safety measures, a protocol amendment, revised informed consent, an investigator's brochure update, additional monitoring, an enrollment pause, or trial termination. Reporting is communication. Risk control is the actual objective. Governance should document the evidence, who made the accountable decision, how it was implemented, and confirmation that sites actually received and acted on critical information.</p>
<h2 id="technology-and-ai-with-accountable-review">Technology and AI, with accountable review</h2>
<p>Automation can detect SAE language, reconcile EDC and safety databases, prioritize follow-up, and support expectedness comparison. What it shouldn't do is invent causality, miss a negation, or stand in for medically accountable SUSAR determination. Validation needs to specifically challenge false negatives, endpoint events, blinded data, changing RSI versions, multilingual reports, and cross-study duplicates.</p>
<h2 id="the-inspection-test">The inspection test</h2>
<p>An inspector might trace a single event from the source record all the way through site report, sponsor awareness, medical assessment, RSI comparison, submission, acknowledgement, and investigator communication. Every timestamp and every judgment call needs to reconcile. A complete case isn't enough if you can't reconstruct why the participant-safety decision was made the way it was.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>Protocol defines safety collection and reporting.</li><li>Investigators understand immediate SAE reporting.</li><li>Sponsor awareness is consistently dated.</li><li>Seriousness and severity remain distinct.</li><li>Investigator and sponsor causality are retained.</li><li>RSI versions and effective dates are controlled.</li><li>SUSAR decisions are medically documented.</li><li>Unblinding follows a controlled process.</li><li>Submissions and acknowledgements reconcile.</li><li>Individual cases feed aggregate review.</li><li>DSUR data are cross-functional and traceable.</li><li>Risk actions reach sites and participants.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-is-clinical-trial-pharmacovigilance">What is clinical-trial pharmacovigilance?</h3>
<p>The collection, assessment, reporting and cumulative oversight of safety information arising during clinical development to protect participants and inform benefit–risk decisions.</p>
<h3 id="is-every-sae-a-susar">Is every SAE a SUSAR?</h3>
<p>No. A SUSAR must be serious, suspected to be causally related and unexpected against the applicable RSI.</p>
<h3 id="can-a-sponsor-disagree-with-investigator-causality">Can a sponsor disagree with investigator causality?</h3>
<p>Yes, but both assessments and the sponsor's medical reasoning should be retained, and regional reporting rules must be applied.</p>
<h3 id="what-is-the-difference-between-serious-and-severe">What is the difference between serious and severe?</h3>
<p>Seriousness is based on regulatory outcome criteria; severity describes intensity.</p>
<h3 id="does-expedited-reporting-replace-aggregate-review">Does expedited reporting replace aggregate review?</h3>
<p>No. Individual reporting and programme-level cumulative evaluation are complementary controls.</p>
<h2 id="conclusion">Conclusion</h2>
<p>Clinical-trial safety works when what one participant experiences can change the protection every participant after them receives.</p>
<p>That takes more than fast data entry. It takes clear roles, controlled reference information, real medical reasoning, global awareness of the pattern, and action that's proportional to the actual risk.</p>
<p><strong>The reporting clock protects compliance. The safety system has to protect the participant.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf" rel="noopener noreferrer" target="_blank">ICH E6(R3)</a></li><li><a href="https://database.ich.org/sites/default/files/E2A_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2A</a></li><li><a href="https://database.ich.org/sites/default/files/E2F_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2F</a></li><li><a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/reporting-safety-information-clinical-trials" rel="noopener noreferrer" target="_blank">EMA clinical-trial safety reporting</a></li><li><a href="https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sponsor-responsibilities-safety-reporting-requirements-and-safety-assessment-ind-and" rel="noopener noreferrer" target="_blank">FDA Sponsor Safety Guidance</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

}


def replace_article(slug: str, new_inner_html: str):
    path = INSIGHTS_DIR / f"{slug}.html"
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    article = soup.select_one("article.article-content")
    if article is None:
        print(f"SKIP (no article tag): {slug}")
        return False
    new_soup = BeautifulSoup(new_inner_html, "html.parser")
    article.clear()
    for child in list(new_soup.children):
        article.append(child)
    path.write_text(str(soup), encoding="utf-8")
    return True


def main():
    changed = 0
    for slug, html in ARTICLES.items():
        if replace_article(slug, html):
            changed += 1
            print(f"OK: {slug}.html")
    print(f"\\n{changed}/{len(ARTICLES)} articles rewritten")


if __name__ == "__main__":
    main()
