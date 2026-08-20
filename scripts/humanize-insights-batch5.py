#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup

INSIGHTS_DIR = Path(__file__).resolve().parent.parent / "insights"

ARTICLES = {

"icsr-quality-control-pharmacovigilance": """
<p>A case can be fully populated, medically plausible, and still be wrong. The patient's age might have been calculated off an uncertain date. The event might be coded correctly but assigned to the wrong product. A hospitalization can show up in the narrative while the seriousness field still says non-serious. A submission can sail through technical validation and still fail the most basic quality test there is: does the case actually represent the source?</p>
<p><strong>ICSR quality control isn't proofreading. It's controlled reconstruction of the evidence before the case becomes a regulatory record.</strong></p>
<p>This is exactly why mature pharmacovigilance organizations don't measure quality by counting completed fields. They measure it by source fidelity, internal consistency, traceability, procedural compliance, and whether an independent reviewer could actually defend every material decision in the case.</p>
<p>The regulatory foundation runs through <a href="https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/pharmacovigilance-post-authorisation/good-pharmacovigilance-practices-gvp" rel="noopener noreferrer" target="_blank">EMA Good Pharmacovigilance Practices</a>, including <a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-module-i-pharmacovigilance-systems-their-quality-systems_en.pdf" rel="noopener noreferrer" target="_blank">GVP Module I</a> for the quality system and <a href="https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vi-collection-management-submission-reports-suspected-adverse-reactions-medicinal-products-rev-2_en.pdf" rel="noopener noreferrer" target="_blank">GVP Module VI</a> for collection, management, and submission of suspected adverse-reaction reports.</p>
<h2 id="what-icsr-quality-control-actually-means">What ICSR quality control actually means</h2>
<p>ICSR QC is the systematic comparison of a processed safety case against its source documents, governed conventions, and applicable procedural requirements. The point is to catch errors or omissions that could affect patient safety, case interpretation, reportability, timelines, transmission, or downstream analysis.</p>
<p>QC doesn't replace case processing, and it doesn't replace medical review either. Processing builds the structured record. QC verifies it. Medical review resolves the clinical judgments that need qualified interpretation behind them.</p>
<div class="article-table-wrap"><table><tr><th><strong>Function</strong></th><th><strong>Primary question</strong></th><th><strong>Output</strong></th></tr><tr><td>Processing</td><td>Was the safety information entered and coded?</td><td>A processing-complete case</td></tr><tr><td>Quality control</td><td>Does the record faithfully and consistently represent the source?</td><td>A corrected and traceable case</td></tr><tr><td>Medical review</td><td>Are the medical assessments scientifically defensible?</td><td>A medically coherent case</td></tr><tr><td>Submission readiness</td><td>Can the correct message be transmitted and accepted on time?</td><td>A regulator-ready ICSR</td></tr></table></div>
<h2 id="the-complete-icsr-qc-framework">The complete ICSR QC framework</h2>
<h3 id="1-receipt-source-and-day-zero-verification">1. Receipt, source and day-zero verification</h3>
<p>Confirm every source item, receipt date, awareness date, routing record, and follow-up version. Day zero needs to be backed by when the organization first had sufficient information under the applicable framework — not by when the safety department happened to open the case file.</p>
<p>Email bodies, attachments, call notes, partner transmissions, literature documents, and translations all need to stay connected to the case. If an inspector can't reconstruct what was received and when, the case isn't audit-ready, no matter how complete it looks otherwise.</p>
<h3 id="2-case-validity-and-identifiers">2. Case validity and identifiers</h3>
<p>Verify the identifiable patient, identifiable reporter, suspect product, and suspected adverse reaction or other reportable safety information. Confirm identifiers, source country, reporter qualification, primary-source status, and duplicate linkage all match the available evidence.</p>
<p>Identifiable doesn't mean fully identified. And a name on its own doesn't automatically make someone a reliable reporter, if the rest of the source looks fictitious or can't support the existence of a real person behind it.</p>
<h3 id="3-patient-and-reporter-data">3. Patient and reporter data</h3>
<p>Check age, date of birth, sex, weight, medical history, pregnancy status, reporter type, contactability, and country. Keep reported, calculated, estimated, masked, unknown, and not-applicable data distinguishable from each other — don't let them get silently converted into one another somewhere along the way.</p>
<h3 id="4-product-exposure-and-treatment-chronology">4. Product exposure and treatment chronology</h3>
<p>Confirm medicinal-product identity, role, formulation, route, dose, frequency, indication, therapy dates, batch information, and action taken. Event onset needs to be checked against exposure. A dechallenge can't be positive if the medicine kept going unchanged, and a rechallenge can't be claimed without documented re-exposure behind it.</p>
<h3 id="5-event-and-product-coding">5. Event and product coding</h3>
<p>Code medical events using the controlled current version of <a href="https://www.meddra.org/" rel="noopener noreferrer" target="_blank">MedDRA</a>. Code products against the governed product dictionary and, where relevant, <a href="https://who-umc.org/whodrug/whodrug-global/" rel="noopener noreferrer" target="_blank">WHODrug Global</a>.</p>
<p>The code has to represent the documented concept — not a diagnosis someone imagined from partial symptoms. Under-coding throws away clinically relevant information. Over-coding manufactures certainty that isn't there. QC needs to compare verbatim text, selected term, specificity, hierarchy, and duplicate-event handling every time.</p>
<h3 id="6-seriousness-severity-and-outcome">6. Seriousness, severity and outcome</h3>
<p>Verify each seriousness criterion is actually supported. Don't let the word "severe" get quietly converted into regulatory seriousness — they're not the same thing. Check hospitalization dates, interventions, disability, congenital outcomes, death information, medical importance, and event outcome against the source and narrative.</p>
<h3 id="7-narrative-quality">7. Narrative quality</h3>
<p>A good narrative lets a competent reader reconstruct source, patient context, exposure, event chronology, investigations, treatment, action taken, outcome, reporter assessment, and company assessment. It shouldn't invent chronology, imply causality nobody actually reported, or hide conflicting information.</p>
<h3 id="8-cross-field-consistency">8. Cross-field consistency</h3>
<ul><li>Do event onset and therapy dates support the recorded temporal relationship?</li><li>Does the narrative agree with structured seriousness, outcome and action-taken fields?</li><li>Are laboratory results, units, normal ranges and dates represented accurately?</li><li>Are suspect, interacting, concomitant and treatment-product roles consistent?</li><li>Are reporter and company causality assessments distinguishable?</li><li>Does the case version contain all relevant follow-up without losing earlier evidence?</li></ul>
<h3 id="9-regulatory-classification-and-submission-readiness">9. Regulatory classification and submission readiness</h3>
<p>QC needs to confirm initial versus follow-up status, seriousness, expectedness, reporting category, destinations, and due dates, using the correct effective product and market configuration. Technical completeness can't make up for a wrong regulatory decision underneath it.</p>
<p>The transmitted message also has to comply with the applicable <a href="https://www.ich.org/page/e2br3-individual-case-safety-report-icsr-specification-and-related-files" rel="noopener noreferrer" target="_blank">ICH E2B(R3) specification</a> and regional rules like the <a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/pharmacovigilance-research-development/eudravigilance/electronic-reporting-suspected-adverse-reactions" rel="noopener noreferrer" target="_blank">EMA electronic-reporting framework</a>.</p>
<h2 id="how-qc-findings-should-be-classified">How QC findings should be classified</h2>
<div class="article-table-wrap"><table><tr><th><strong>Level</strong></th><th><strong>Meaning</strong></th><th><strong>Examples</strong></th></tr><tr><td>Critical</td><td>May affect validity, patient safety, expedited reporting, destination or compliance</td><td>Missed serious event; incorrect day zero; wrong suspect; unsupported invalidation</td></tr><tr><td>Major</td><td>Materially affects accuracy or interpretation</td><td>Contradictory chronology; omitted test result; incorrect coding specificity</td></tr><tr><td>Minor</td><td>Limited immediate impact but requires correction or coaching</td><td>Non-material wording, formatting or metadata defect</td></tr></table></div>
<p>Base finding severity on potential impact, not on how strongly the reviewer feels about it that day. Every finding needs a correction, a responsible person, a completion time, and an audit trail behind it. Trends should feed training, system controls, SOP updates, and corrective or preventive action — not sit forgotten in a review log.</p>
<h2 id="risk-based-qc-is-not-reduced-accountability">Risk-based QC is not reduced accountability</h2>
<p>A risk-based model can vary review depth by case seriousness, complexity, product maturity, emerging issues, jurisdiction, processor performance, and error history. It should never create blind spots around validity, day zero, seriousness, reportability, or submission destination — those stay non-negotiable regardless of risk tier.</p>
<p><strong>A low QC sampling rate is only defensible when measured evidence shows the process reliably controls critical error — not because the organization wants higher throughput.</strong></p>
<h2 id="what-ai-can-support-in-icsr-qc">What AI can support in ICSR QC</h2>
<p>Automation is genuinely useful for comparing fields, catching missing data, validating dates, spotting contradictions, checking dictionaries and E2B structure, and prioritizing complex cases. AI can extract chronology, compare narratives against source documents, and suggest potential review findings.</p>
<p>But an AI model can just as easily produce a fluent, unsupported medical conclusion. It needs to operate within a defined and validated context of use, show the evidence behind every flag it raises, preserve human override, and escalate uncertainty rather than paper over it. False negatives deserve particular attention here — a missed serious or reportable feature can stay invisible indefinitely if nobody's watching for it.</p>
<h2 id="practical-case-qc-checklist">Practical case-QC checklist</h2>
<ul><li>All source items, translations and receipt dates are attributable.</li><li>Validity criteria and case identifiers are supported.</li><li>Patient and reporter data match the source.</li><li>Product roles, exposure, indications and therapy dates are correct.</li><li>Events and products are coded to governed dictionaries without unsupported inference.</li><li>Seriousness is supported and distinguished from severity.</li><li>Narrative, source and structured fields tell the same story.</li><li>Follow-up changes are captured without losing earlier evidence.</li><li>Expectedness, reportability, destinations and due dates are correct.</li><li>E2B validation, transmission status and acknowledgements are controlled.</li><li>Findings, rework, overrides and approvals are auditable.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-is-icsr-quality-control">What is ICSR quality control?</h3>
<p>It is the systematic verification that a processed safety case accurately represents its source and is complete, consistent, traceable and procedurally compliant before submission.</p>
<h3 id="is-qc-the-same-as-medical-review">Is QC the same as medical review?</h3>
<p>No. QC primarily confirms fidelity and consistency. Medical review evaluates clinical coherence and consequential medical assessments.</p>
<h3 id="can-the-processor-perform-qc">Can the processor perform QC?</h3>
<p>Models vary, but sufficient independence and compensating controls are needed to reduce confirmation bias and prove objective review.</p>
<h3 id="does-e2b-validation-prove-case-quality">Does E2B validation prove case quality?</h3>
<p>No. It proves technical or business-rule conformance; it does not prove that chronology, seriousness, coding or medical interpretation are correct.</p>
<h3 id="can-ai-replace-icsr-qc">Can AI replace ICSR QC?</h3>
<p>AI can support comparison and detection, but consequential findings require governed human accountability and validated performance.</p>
<h2 id="conclusion">Conclusion</h2>
<p>A quality case doesn't just reach submission. It carries faithful evidence, consistent data, visible uncertainty, and an auditable decision path behind it. That standard protects the individual case — and every signal, aggregate report, and benefit–risk conclusion later built on top of it.</p>
<p><strong>If the source says one thing and the database implies another, the database isn't complete. It's wrong.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/pharmacovigilance-post-authorisation/good-pharmacovigilance-practices-gvp" rel="noopener noreferrer" target="_blank">EMA — Good Pharmacovigilance Practices</a></li><li><a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-module-i-pharmacovigilance-systems-their-quality-systems_en.pdf" rel="noopener noreferrer" target="_blank">EMA — GVP Module I</a></li><li><a href="https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vi-collection-management-submission-reports-suspected-adverse-reactions-medicinal-products-rev-2_en.pdf" rel="noopener noreferrer" target="_blank">EMA — GVP Module VI</a></li><li><a href="https://www.ich.org/page/e2br3-individual-case-safety-report-icsr-specification-and-related-files" rel="noopener noreferrer" target="_blank">ICH — E2B(R3)</a></li><li><a href="https://www.meddra.org/" rel="noopener noreferrer" target="_blank">MedDRA</a></li><li><a href="https://who-umc.org/whodrug/whodrug-global/" rel="noopener noreferrer" target="_blank">UMC — WHODrug Global</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

"icsr-medical-review-pharmacovigilance": """
<p>A medically fluent narrative can still describe a clinically incoherent case. The event might precede exposure. A positive dechallenge might get selected while treatment was still ongoing. An expected event might be assessed against the wrong reference document. A serious outcome might be sitting quietly behind a mild-looking term.</p>
<p><strong>Medical review isn't the final signature on a processed case. It's the point where the organization takes scientific accountability for what the case actually means.</strong></p>
<p>The reviewer has to hold two boundaries at once: never ignore a clinically important pattern, and never turn incomplete information into a diagnosis or causal conclusion the source can't actually support.</p>
<p>The operational foundation is set out in <a href="https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vi-collection-management-submission-reports-suspected-adverse-reactions-medicinal-products-rev-2_en.pdf" rel="noopener noreferrer" target="_blank">EMA GVP Module VI</a> and the harmonised post-approval safety guidance in the <a href="https://www.ich.org/page/efficacy-guidelines" rel="noopener noreferrer" target="_blank">ICH efficacy-guideline framework</a>. Medical judgment still has to follow effective company procedures, product information, and regional requirements on top of that.</p>
<h2 id="what-medical-review-must-accomplish">What medical review must accomplish</h2>
<p>Medical review determines whether the clinical story, the coding, and the assessments hold together — whether they're coherent, appropriately cautious, and defensible. It evaluates the whole case. It doesn't just rubber-stamp isolated database selections one at a time.</p>
<ul><li>Reconstruct the chronology of exposure, onset, intervention, withdrawal, rechallenge and outcome.</li><li>Determine whether reported diagnoses and selected medical concepts are supported.</li><li>Assess seriousness and medical importance without confusing seriousness with intensity.</li><li>Evaluate expectedness against the correct effective reference safety information.</li><li>Evaluate causality while preserving reporter and company assessments separately.</li><li>Identify alternative explanations, missing evidence and medically meaningful follow-up.</li><li>Confirm that the narrative communicates the clinical course without inference beyond the source.</li></ul>
<h2 id="clinical-coherence-begins-with-chronology">Clinical coherence begins with chronology</h2>
<p>A temporal relationship matters for a lot of causal interpretations, but sequence alone doesn't prove anything. Verify first dose, last dose, dose changes, onset, worsening, treatment, dechallenge, rechallenge, and recovery. If a date's uncertain, leave it uncertain — don't quietly firm it up to make the timeline read cleaner.</p>
<p>Chronology also surfaces errors the fields themselves hide. If liver-test abnormalities started before exposure, the case can still be valid if a reporter suspected the medicine — but the company's medical assessment shouldn't imply exposure started the event when the timeline says otherwise. If symptoms came back before re-exposure happened, that claimed positive rechallenge needs a hard look.</p>
<h2 id="diagnosis-preserve-the-source-test-the-evidence">Diagnosis: preserve the source, test the evidence</h2>
<p>A diagnosis might be explicitly reported, confirmed through investigations, provisionally suspected, or inferred from a pattern. These are four different states, and I don't treat them as equivalent. Preserve the source diagnosis, and let the coding and narrative wording make the actual level of certainty clear.</p>
<p>Watch for medically important patterns — mucosal involvement with blistering, hepatic injury patterns, symptoms compatible with anaphylaxis — without turning a possibility into a confirmed diagnosis. The right move might be targeted follow-up, additional coding under controlled convention, or escalation. It's rarely "just write down the scarier diagnosis and move on."</p>
<h2 id="seriousness-is-not-severity">Seriousness is not severity</h2>
<p>Severity describes intensity. Seriousness is a regulatory classification tied to outcomes or interventions — death, life threat, hospitalization, disability, congenital anomaly, or another medically important condition. A severe migraine can stay non-serious. A clinically subtle arrhythmia can be serious.</p>
<p>The <a href="https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/pharmacovigilance-post-authorisation/eudravigilance/important-medical-event-terms-list-version-281" rel="noopener noreferrer" target="_blank">EMA Important Medical Events list</a> helps keep identification of these events consistent, but it doesn't replace case-specific judgment or prove seriousness on its own.</p>
<h2 id="expectedness-requires-the-correct-reference">Expectedness requires the correct reference</h2>
<p>Expectedness isn't decided by general medical knowledge, and it's not about whether the event is common. It comes down to the applicable, effective reference safety information for the product and reporting context. Term specificity, nature, severity, and outcome all factor into that decision.</p>
<p>Know which version was actually effective at the relevant time. An event sitting in the current label might have been unlisted when the case became reportable. And a broad class statement might not cover a clinically distinct presentation, even if it looks related on the surface.</p>
<h2 id="causality-is-structured-reasoning-not-a-score">Causality is structured reasoning — not a score</h2>
<div class="article-table-wrap"><table><tr><th><strong>Evidence domain</strong></th><th><strong>Questions for medical review</strong></th></tr><tr><td>Temporality</td><td>Did exposure precede the event? Is latency compatible?</td></tr><tr><td>Dechallenge/rechallenge</td><td>Did the event change after withdrawal or re-exposure, and is that change documented?</td></tr><tr><td>Biological plausibility</td><td>Is the pattern compatible with pharmacology, mechanism or known class effects?</td></tr><tr><td>Alternative causes</td><td>Could disease, infection, procedures, concomitant therapy or background risk explain the event?</td></tr><tr><td>Objective evidence</td><td>Do tests, imaging, pathology or specialist assessments support the concept?</td></tr><tr><td>Prior knowledge</td><td>Is the association known, emerging, labelled or biologically unexpected?</td></tr></table></div>
<p>Keep reporter causality and company causality distinguishable from each other. A company can disagree with the reporter, but the reporter's judgment doesn't get erased because of that disagreement. And an absent assessment shouldn't quietly turn into "not related" — silence isn't the same as a conclusion.</p>
<h2 id="dechallenge-and-rechallenge-common-traps">Dechallenge and rechallenge: common traps</h2>
<ul><li>Improvement after treatment discontinuation is not necessarily positive dechallenge if the natural disease course or treatment of the event explains recovery.</li><li>A medicine must actually be stopped or meaningfully reduced before a dechallenge conclusion is made.</li><li>Rechallenge requires documented re-exposure; persistence of symptoms is not rechallenge.</li><li>A negative rechallenge may be uninterpretable if dose, latency or concomitant treatments changed.</li><li>For long half-life products, improvement may not occur immediately after withdrawal.</li></ul>
<h2 id="medical-follow-up-should-change-the-evidence">Medical follow-up should change the evidence</h2>
<p>A generic follow-up form can collect a lot of fields without resolving the actual uncertainty. Aim follow-up at questions that could genuinely change validity, seriousness, expectedness, causality, diagnosis, outcome, or regulatory action — not just questions that are easy to ask.</p>
<ul><li>Hepatic events: baseline and serial values, upper limits of normal, competing causes, imaging, viral studies, action taken and recovery.</li><li>Severe cutaneous reactions: morphology, body-surface involvement, mucosal involvement, biopsy, hospitalisation and treatment.</li><li>Pregnancy: exposure window, gestational age, prenatal testing, outcome and infant follow-up.</li><li>Death: date and cause, terminal course, relationship to the event and autopsy findings.</li><li>Medication error or overdose: circumstances, actual exposure, clinical consequences, intervention and preventability.</li></ul>
<h2 id="narrative-review-the-clinical-story-must-remain-honest">Narrative review: the clinical story must remain honest</h2>
<p>The narrative should pull together chronology, investigation, treatment, and outcome while still preserving uncertainty. It shouldn't imply a diagnosis, dechallenge, or causality that was never actually established. Conflicting dates should be described, or resolved through follow-up — not quietly smoothed over.</p>
<p><strong>A polished narrative that hides uncertainty isn't high quality. It's high-confidence misrepresentation.</strong></p>
<h2 id="medical-review-and-ai">Medical review and AI</h2>
<p>AI can extract chronology, surface potential contradictions, suggest coding concepts, and identify gaps in follow-up. It can also produce a convincing diagnosis from incomplete symptoms, infer causality straight from sequence, and mix up severity with seriousness — all fluently enough that it's easy to miss.</p>
<p>A safe model shows its source evidence, states its uncertainty, stays within approved knowledge, and escalates consequential decisions instead of resolving them silently. Medical accountability stays with qualified people. The system supports the reasoning. It doesn't get to manufacture it.</p>
<h2 id="medical-review-checklist">Medical-review checklist</h2>
<ul><li>Exposure and event chronology is clinically possible and internally consistent.</li><li>Diagnoses and codes reflect the level of evidence available.</li><li>Seriousness criteria and medical importance are supported.</li><li>Expectedness uses the correct effective reference safety information.</li><li>Reporter and company causality are separated.</li><li>Dechallenge and rechallenge conclusions are evidence-based.</li><li>Alternative explanations and concomitant therapies are considered.</li><li>Follow-up questions are medically targeted.</li><li>Narrative and structured assessments communicate the same clinical story.</li><li>Uncertainty, limitations and overrides are visible in the audit trail.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-is-medical-review-in-pharmacovigilance">What is medical review in pharmacovigilance?</h3>
<p>It is the qualified clinical evaluation of an ICSR's chronology, diagnosis, seriousness, expectedness, causality, alternative explanations, follow-up needs and narrative coherence.</p>
<h3 id="is-every-severe-adverse-event-serious">Is every severe adverse event serious?</h3>
<p>No. Severity describes intensity; seriousness is based on defined outcomes or medical importance.</p>
<h3 id="does-a-positive-temporal-relationship-prove-causality">Does a positive temporal relationship prove causality?</h3>
<p>No. It supports consideration but must be evaluated with plausibility, dechallenge, rechallenge, alternative causes and objective evidence.</p>
<h3 id="can-a-company-change-reporter-causality">Can a company change reporter causality?</h3>
<p>The company can record its own assessment, but the reporter's assessment should remain preserved and distinguishable.</p>
<h3 id="can-ai-conduct-medical-review">Can AI conduct medical review?</h3>
<p>It can assist with evidence extraction and consistency checks, but consequential medical conclusions require governed human accountability.</p>
<h2 id="conclusion">Conclusion</h2>
<p>Medical review doesn't exist to make every case sound medically complete. It exists to make every conclusion proportionate to the evidence actually behind it. The reviewer's job isn't picking the strongest diagnosis or the safest regulatory answer — it's choosing the most defensible interpretation and keeping the uncertainty visible.</p>
<p><strong>A pharmacovigilance decision is only strong when another competent reviewer can trace the same evidence and see exactly how the conclusion was reached.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vi-collection-management-submission-reports-suspected-adverse-reactions-medicinal-products-rev-2_en.pdf" rel="noopener noreferrer" target="_blank">EMA — GVP Module VI</a></li><li><a href="https://www.ich.org/page/efficacy-guidelines" rel="noopener noreferrer" target="_blank">ICH — Efficacy guidelines</a></li><li><a href="https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/pharmacovigilance-post-authorisation/eudravigilance/important-medical-event-terms-list-version-281" rel="noopener noreferrer" target="_blank">EMA — Important Medical Events terms</a></li><li><a href="https://www.meddra.org/" rel="noopener noreferrer" target="_blank">MedDRA</a></li></ul>
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
    print(f"\\n{len(ARTICLES)}/{len(ARTICLES)} articles rewritten")


if __name__ == "__main__":
    main()
