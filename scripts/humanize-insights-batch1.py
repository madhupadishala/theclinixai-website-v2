#!/usr/bin/env python3
"""
Batch 1 of insights de-AI-ification: rewrites the body prose of 5 articles
to remove repeated AI-writing patterns (rule-of-three sentences, "not X, it
is Y" constructions, abstract-noun stacking, uniform paragraph cadence,
and — critically — two sections that were copy-pasted VERBATIM across
multiple articles in the original content, which is its own duplication
problem). Citations, FAQ schema, checklists structure, and the legal
disclaimer are preserved. h2/h3 ids are kept stable.
"""
from pathlib import Path
from bs4 import BeautifulSoup

INSIGHTS_DIR = Path(__file__).resolve().parent.parent / "insights"

ARTICLES = {

"aggregate-report-data-lock-quality-control": """
<p>Almost nobody blames the writer when a PBRER goes wrong. But by the time a report is actually wrong, the writer is usually the last person who could have caught it. The real damage happened weeks earlier — an undefined query nobody double-checked, a dataset that never got reconciled against the safety database, a MedDRA dictionary that quietly moved versions mid-cycle.</p>
<p>None of that shows up in the finished document. It just reads as fact.</p>
<p><strong>A report is only ever as strong as the data underneath it — no amount of good writing fixes a bad data package.</strong></p>
<p>Regulatory foundation: <a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a>; <a href="https://database.ich.org/sites/default/files/E2F_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2F</a>; <a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vii-periodic-safety-update-report-rev-1_en.pdf" rel="noopener noreferrer" target="_blank">GVP VII</a></p>
<h2 id="data-lock-governance">Data-lock governance</h2>
<p>Get the data lock point defined properly and most of the downstream chaos disappears. That means picking an actual date and timezone, agreeing what happens with data that shows up late, freezing the dictionary version, and writing down — somewhere everyone can actually find it — what counts as an approved exception. It sounds like paperwork. It's the difference between six contributors working off the same numbers and six people quietly working off six different ones.</p>
<h2 id="source-reconciliation">Source reconciliation</h2>
<p>The safety database has to agree with everything else touching the same product: submissions already filed, partner data feeds, clinical systems, the literature screening output, the signal tracker, whatever regulators have already acted on, and the exposure numbers underneath all of it. Catch a mismatch here early and it's a five-minute fix. Catch it after the report's drafted and you're rewriting under deadline pressure.</p>
<h2 id="query-specifications">Query specifications</h2>
<p>Write the query down properly — inclusion criteria, product scope, case versions, how seriousness and event groupings are defined, which MedDRA version, how nullified cases and duplicates are handled — and validate the output before anyone builds a table from it. A query nobody documented can't be reproduced, and a query that can't be reproduced can't be defended six months later when someone asks how a number was generated.</p>
<h2 id="table-to-text-consistency">Table-to-text consistency</h2>
<p>Every number that shows up more than once in the report should trace back to one controlled output, not get retyped by hand each time it's needed. A surprising share of aggregate-report errors come from exactly that — someone copying a figure from one document into another late at night. Narrative text should point to the specific table or listing it's drawing from, not just assert a number and move on.</p>
<h2 id="medical-and-regulatory-qc">Medical and regulatory QC</h2>
<p>These are three different jobs, and treating them as one review pass is how things slip through. Technical QC checks the counts and formatting. Medical QC is the harder one — someone actually pushing back on the interpretation, asking whether an emerging pattern got missed, whether the conclusion is really supported by what's in front of them. Regulatory QC checks format, region-specific content, submission requirements. Skip the medical layer and a report can pass QC while being substantively wrong.</p>
<h2 id="managing-late-changes">Managing late changes</h2>
<p>If something material changes after the data lock, that needs an impact assessment and a controlled refresh — not a quiet swap. Tables occasionally get silently replaced after a report has already been through review, and it wrecks traceability instantly. Once that happens, nobody downstream can be sure what they approved is what actually shipped.</p>
<h2 id="the-scientific-questions-every-aggregate-team-must-answer">The questions a data package alone can't answer</h2>
<p>A report that just describes the interval isn't doing its job — it needs to interrogate it. What actually changed in exposure this period? Did any events increase in frequency or change in clinical character? Did new study data shift how we understand a risk or a benefit? Did a signal assessment move the needle on the safety specification? Did a regulatory action in one market create implications somewhere else? Did the risk-minimisation data actually show the intervention working — or quietly show it isn't?</p>
<p>There's a distinction worth holding onto: new information versus new interpretation of old information. Sometimes nothing new happened this period, but the cumulative picture shifted anyway — severity looks different, a susceptible population became clearer, clinical management needs to adjust. That kind of shift matters as much as an actual new reaction, and it's the one teams miss most, because there's no new case pointing at it.</p>
<ul><li>Put interval changes in cumulative context, not in isolation.</li><li>Say plainly where exposure and case-ascertainment data fall short.</li><li>Make sure signal conclusions actually match the RMP and product information.</li><li>Name the specific action the evaluation leads to — not just the finding.</li></ul>
<h2 id="authoring-governance-and-cross-functional-accountability">Who's actually accountable for the numbers</h2>
<p>An aggregate report gets pulled together from safety operations, medical review, biostatistics, epidemiology, clinical development, regulatory affairs, labelling, and risk management — a lot of hands on one document. The author shouldn't be the one who discovers, at final review, that two of those functions were quietly working from different data cuts the whole time. That discovery has to happen weeks earlier, not at the finish line.</p>
<p>A source matrix helps: one document naming every input, its system of record, who owns it, the cut-off, and what reconciliation and approval it needs. And when review comments come back that actually change a risk classification or a benefit–risk conclusion, the rationale needs to be written down — not just fixed quietly and moved past.</p>
<ul><li>Lock the governed datasets before medical interpretation starts, not during it.</li><li>Pull every repeated number from one controlled source, every time.</li><li>Write down material judgement changes between drafts — don't let them disappear into version history.</li><li>Tie every conclusion to a follow-up action and a named owner.</li></ul>
<h2 id="a-practical-decision-scenario">A scenario worth sitting with</h2>
<p>Spontaneous case counts for a known risk jump 60% in one reporting period. Alarming at first glance — until the exposure data shows a major market expansion happened that same quarter, plus a communication campaign that almost certainly stimulated extra reporting. So some of that 60% is noise, not signal. But look closer and the proportion of cases involving hospitalisation has also gone up, specifically in one vulnerable population. That part shouldn't get waved away by the exposure explanation. A good report doesn't settle for "it's just more reporting" or "nothing changed" — it pulls the volume story apart from the clinical pattern and asks whether that one population needs a targeted action, regardless of what's driving the overall count.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>One controlled DLP is used.</li><li>Queries are versioned.</li><li>Sources reconcile.</li><li>MedDRA and product dictionaries are fixed.</li><li>Tables trace to outputs.</li><li>Medical conclusions trace to evidence.</li><li>Late changes are assessed and approved.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-is-a-data-lock-point">What is a data lock point?</h3>
<p>The agreed cut-off date. Everything in the periodic report has to fall before it.</p>
<h3 id="why-reconcile-datasets">Why reconcile datasets?</h3>
<p>Because without it you end up with evidence that's missing, duplicated, or contradicts itself across sections and submissions.</p>
<h3 id="what-is-aggregate-report-qc">What is aggregate-report QC?</h3>
<p>Three separate checks — technical, medical, and regulatory — each verifying something different about the data, the interpretation, and the format.</p>
<h3 id="can-tables-be-refreshed-after-dlp">Can tables be refreshed after DLP?</h3>
<p>Only through a documented exception process with an impact assessment attached. Not quietly.</p>
<h2 id="conclusion">Conclusion</h2>
<p>Data governance and medical quality aren't two separate concerns — they're the same concern seen from different angles. Every number that can't be traced back to its source quietly weakens whatever conclusion sits on top of it.</p>
<p><strong>When two sections of a report disagree, that's rarely a formatting problem. It usually means the organisation lost track of which version of the safety truth is the real one.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a></li><li><a href="https://database.ich.org/sites/default/files/E2F_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2F</a></li><li><a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vii-periodic-safety-update-report-rev-1_en.pdf" rel="noopener noreferrer" target="_blank">GVP VII</a></li><li><a href="https://www.meddra.org/" rel="noopener noreferrer" target="_blank">MedDRA</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

"pbrer-psur-preparation": """
<p>A PBRER can hit every required section, format every table correctly, read smoothly end to end — and still fail on the thing that actually matters. That happens when the conclusion isn't really connected to the evidence sitting above it.</p>
<p>Format compliance is necessary. It's a much lower bar than a defensible benefit–risk evaluation, and it's easy to mistake one for the other under deadline pressure.</p>
<p><strong>A PBRER isn't finished when every section is filled in. It's finished when every important change in benefit, risk, and uncertainty has actually been interpreted.</strong></p>
<p>Regulatory foundation: <a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a>; <a href="https://database.ich.org/sites/default/files/E2CR2_Q%26As_Q%26As.pdf" rel="noopener noreferrer" target="_blank">ICH E2C Q&amp;A</a>; <a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vii-periodic-safety-update-report-rev-1_en.pdf" rel="noopener noreferrer" target="_blank">GVP VII</a></p>
<h2 id="start-before-the-data-lock-point">Start before the data lock point</h2>
<p>By the time extraction begins, the reporting interval, international birth date, data lock, submission schedule, product scope, indications, and territories should already be confirmed — not settled on the fly. Set the source plan and the authoring calendar before anyone pulls a single number. Teams that skip this step almost always end up re-scoping mid-cycle, which is the expensive way to find out the boundaries weren't agreed.</p>
<h2 id="build-a-governed-data-package">Build a governed data package</h2>
<p>Case data, exposure, literature, studies, signals, regulatory actions, risk-minimisation information, and any material efficacy findings all need to reconcile with each other before writing starts. Document the query logic, the MedDRA version, the case inclusion rules, and — just as important — the limitations. A data package with no documented limitations usually means nobody looked hard enough for them.</p>
<h2 id="interval-versus-cumulative-analysis">Interval versus cumulative analysis</h2>
<p>Interval data tells you what changed this period. Cumulative data tells you what that change actually means once it's sitting in context. You need both — a rise in reports that isn't checked against exposure, stimulated reporting, or market expansion can mislead a reader who only sees the interval number.</p>
<h2 id="signal-integration">Signal integration</h2>
<p>Whatever's in the signal tracker — new, ongoing, or closed — has to match what's in the report. And a report that just lists signal statuses without explaining the material conclusions behind them isn't really integrating the signal data; it's just quoting it.</p>
<h2 id="integrated-benefit-risk-evaluation">Integrated benefit–risk evaluation</h2>
<p>Name the key benefits, the key risks, and the major uncertainties for each relevant indication and population, and weigh them against therapeutic context — what else is available, how severe the disease is, whether the risk is preventable, how well risk minimisation has actually performed. Generic language here ("benefits continue to outweigh risks") is usually a sign the specific work wasn't done.</p>
<h2 id="quality-control">Quality control</h2>
<p>Cross-check every number that appears more than once, verify the data cut-offs actually match across sections, trace every claim back to its source, and — this is the part that gets skipped under time pressure — challenge any conclusion that reads stronger than the evidence supporting it.</p>
<h2 id="the-scientific-questions-every-aggregate-team-must-answer">Questions worth asking before the conclusion gets written</h2>
<p>A useful report interrogates the interval instead of just narrating it. What changed in exposure? Did any events increase, or shift in clinical character? Did new studies change how a risk or benefit is understood? Did a signal assessment move the safety specification? Did a regulatory action somewhere else create an implication here? Did the risk-minimisation data show the intervention actually working, or quietly failing?</p>
<p>Distinguish new information from new interpretation of information you already had. Sometimes no new event type appears, but the cumulative picture still shifts — severity, frequency, a newly clear susceptible population, a change in how the product should be managed clinically. That kind of shift deserves the same attention as an actual new reaction, precisely because there's no obvious new case flagging it.</p>
<ul><li>Explain interval changes against cumulative context, not on their own.</li><li>State plainly where exposure and case-ascertainment data are limited.</li><li>Make sure signal conclusions actually reconcile with the RMP and product information.</li><li>Name the concrete action the evaluation leads to.</li></ul>
<h2 id="authoring-governance-and-cross-functional-accountability">Cross-functional accountability, in practice</h2>
<p>A PBRER passes through safety operations, medical review, biostatistics, epidemiology, clinical development, regulatory affairs, labelling, and risk management before it's done. The author shouldn't find out at final review that two of those functions were quietly working from different data cuts or scopes the entire time — that has to surface far earlier.</p>
<p>A controlled source matrix — naming every input, its owner, its cut-off, its format, and what approval it needs — prevents most of that. And when a review comment actually changes a risk classification or a benefit–risk conclusion, write down why. Silent fixes erode the trail an inspector will eventually want to follow.</p>
<ul><li>Freeze governed datasets before final medical interpretation begins.</li><li>Draw every repeated number from one controlled source.</li><li>Record material judgement changes between drafts.</li><li>Connect every conclusion to a follow-up action and a named owner.</li></ul>
<h2 id="a-practical-decision-scenario">Working through a real example</h2>
<p>Say spontaneous case counts for a known risk rise 60% in a reporting period. It looks bad — until exposure data shows a major market expansion plus a communication campaign that likely stimulated extra reporting, which explains a chunk of that increase. But the proportion of cases involving hospitalisation has also risen, specifically within one vulnerable population. That detail shouldn't be absorbed into the "it's just more reporting" explanation. The report needs to separate the volume story from the clinical pattern and decide, independently, whether that population needs a targeted response.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>Reporting interval and scope are correct.</li><li>All sources reconcile.</li><li>Exposure methodology is documented.</li><li>Signals match governed records.</li><li>Important risks and benefits are prioritised.</li><li>Conclusion is evidence-linked.</li><li>Actions and RMP changes are explicit.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-is-a-pbrer">What is a PBRER?</h3>
<p>An ICH periodic report bringing together cumulative safety, exposure, benefit, and risk information for a marketed product.</p>
<h3 id="are-psur-and-pbrer-identical">Are PSUR and PBRER identical?</h3>
<p>Closely related, but not interchangeable — regional terminology, format, and submission requirements still need to be applied correctly.</p>
<h3 id="what-is-a-dlp">What is a DLP?</h3>
<p>The data lock point — the agreed cut-off date for what's included in the report.</p>
<h3 id="what-makes-a-strong-conclusion">What makes a strong conclusion?</h3>
<p>A transparent comparison of key benefits, key risks, uncertainties, and the actions required as a result — not a restated summary.</p>
<h2 id="conclusion">Conclusion</h2>
<p>The best PBRERs make the decision visible on the page — what changed, how the evidence was weighed, and why the benefit–risk conclusion still holds.</p>
<p><strong>Don't let the conclusion become the least-challenged paragraph in the most important cumulative safety document you write.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a></li><li><a href="https://database.ich.org/sites/default/files/E2CR2_Q%26As_Q%26As.pdf" rel="noopener noreferrer" target="_blank">ICH E2C Q&amp;A</a></li><li><a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-vii-periodic-safety-update-report-rev-1_en.pdf" rel="noopener noreferrer" target="_blank">GVP VII</a></li><li><a href="https://database.ich.org/sites/default/files/M4E_R2__Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH M4E(R2)</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

"sae-reporting-clinical-trials": """
<p>A site can handle a hospitalisation exactly right — fast, clinically sound, participant stabilised within the hour — and still end up with a safety-reporting failure, if the sponsor doesn't learn about it for two days.</p>
<p>Clinical care and safety reporting are genuinely different jobs. Both start at the site. Neither one should wait on the other to finish.</p>
<p><strong>The first SAE report doesn't need every answer. It needs enough accurate information to start the sponsor's assessment without losing the clock.</strong></p>
<p>Regulatory foundation: <a href="https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf" rel="noopener noreferrer" target="_blank">ICH E6(R3)</a>; <a href="https://database.ich.org/sites/default/files/E2A_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2A</a>; <a href="https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-safety-reporting-investigational-drugs-and-devices" rel="noopener noreferrer" target="_blank">FDA Investigator Safety Guidance</a>; <a href="https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sponsor-responsibilities-safety-reporting-requirements-and-safety-assessment-ind-and" rel="noopener noreferrer" target="_blank">FDA Sponsor Safety Guidance</a></p>
<h2 id="what-qualifies-as-an-sae">What actually qualifies as an SAE</h2>
<p>Death, life-threatening, requires or extends hospitalisation, causes persistent or significant disability, a congenital anomaly, or medically important for some other reason. "Life-threatening" means actual risk at the time it happened — not a worst-case hypothetical version of the same event.</p>
<p>Protocol-specific requirements and whatever regional rules apply still sit on top of this.</p>
<h2 id="investigator-participant-level-responsibility">What sits with the investigator</h2>
<p>Medical care comes first, always. After that: recognising and documenting the event, assessing seriousness and causality, and getting the SAE to the sponsor as fast as the protocol allows — initial transmission first, details following.</p>
<p>Keep the source evidence intact. If an assessment changes later, explain the change rather than quietly overwriting the original.</p>
<h2 id="sponsor-programme-level-responsibility">What sits with the sponsor</h2>
<p>The sponsor is looking at the report against the whole development programme, not just this one case — deciding whether it meets expedited reporting thresholds and whether it points to something bigger. Sponsor medical review that just repeats the site's form back isn't doing its job; it needs to actually test the diagnosis, the timing, the alternative explanations, whether the event was expected, and how it fits the aggregate picture.</p>
<h2 id="the-awareness-date-control">Why the awareness date matters more than people think</h2>
<p>Someone has to define, in writing, when the sponsor is officially "aware" — which people or vendors can legitimately receive SAE information, and how weekends and out-of-office gaps get handled. The first valid receipt needs to stay traceable no matter what happens after it.</p>
<p>A database-entry timestamp is not the same thing as the actual organisational receipt date. Don't let the two get confused.</p>
<h2 id="minimum-initial-information">What the first report actually needs</h2>
<p>An identifiable participant, an identifiable reporter, the suspected product where relevant, the event, the seriousness criterion, onset, outcome, the study, and the investigator's assessment. That's it — don't hold the initial report hostage to a discharge summary or a lab report that hasn't arrived yet.</p>
<h2 id="targeted-follow-up">Follow-up that's actually targeted</h2>
<p>Diagnosis confirmation, clinical course, treatment given, hospital dates, labs and imaging, dose and exposure history, dechallenge and rechallenge, concomitant medications, medical history, alternative causes — pulled in based on what the specific case actually needs, prioritised by clinical and reporting impact, not requested as one generic checklist every time.</p>
<h2 id="endpoint-events-and-protocol-exceptions">Endpoint events aren't a shortcut</h2>
<p>Some serious events double as efficacy or safety endpoints and get handled through a protocol-defined process instead of the standard pathway. That's fine — as long as it was agreed in advance, documented, and not something a site improvises on its own. Anything that falls outside a defined exception goes through the normal SAE route, no exceptions to the exception.</p>
<h2 id="reconciliation-and-oversight">Reconciliation, and why it matters more than it sounds like it should</h2>
<p>EDC, SAE forms, the safety database, clinical database, lab data, adjudication records, mortality data — these all need to agree with each other. Where they don't, resolve it without compromising blinded integrity. And track the metrics that actually matter: initial-report timeliness, follow-up ageing, discrepancies, repeat failures from the same site — not just raw case volume, which tells you almost nothing about whether the process is working.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>SAE criteria are understood.</li><li>Site provides medical care first.</li><li>Initial report is not delayed for completeness.</li><li>Sponsor awareness date is preserved.</li><li>Investigator causality is retained.</li><li>Medical follow-up is targeted.</li><li>Endpoint exceptions are protocol-controlled.</li><li>EDC and safety data reconcile.</li><li>Late reports receive impact assessment.</li><li>Sites receive feedback and retraining where needed.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="how-quickly-should-an-investigator-report-an-sae">How quickly should an investigator report an SAE?</h3>
<p>As fast as the protocol and applicable requirements allow — FDA's current guidance treats "immediate" as roughly one calendar day for the initial information.</p>
<h3 id="must-an-sae-be-related-to-the-investigational-product">Must an SAE be related to the investigational product?</h3>
<p>No. Seriousness and causality are separate questions — investigators generally report SAEs regardless of suspected relationship, subject to the protocol and applicable rules.</p>
<h3 id="can-follow-up-be-sent-later">Can follow-up be sent later?</h3>
<p>Yes, and it should be. Don't hold the initial notification back while follow-up information is still being gathered.</p>
<h3 id="who-decides-whether-an-sae-is-a-susar">Who decides whether an SAE is a SUSAR?</h3>
<p>The sponsor makes that call, weighing seriousness, causality, and expectedness — while keeping the investigator's original evidence intact.</p>
<h3 id="why-reconcile-edc-and-safety-databases">Why reconcile EDC and safety databases?</h3>
<p>To catch serious events that were omitted, duplicated, or recorded inconsistently between the two.</p>
<h2 id="conclusion">Conclusion</h2>
<p>The site sees the clinical reality first. The sponsor sees whether that reality changes anything about the wider development programme.</p>
<p>A well-controlled SAE pathway connects those two views before delay, incomplete evidence, or blurred ownership gets a chance to compromise participant protection.</p>
<p><strong>Report what's known, preserve what's uncertain, and keep following the evidence until the safety decision actually holds up.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf" rel="noopener noreferrer" target="_blank">ICH E6(R3)</a></li><li><a href="https://database.ich.org/sites/default/files/E2A_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2A</a></li><li><a href="https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-safety-reporting-investigational-drugs-and-devices" rel="noopener noreferrer" target="_blank">FDA Investigator Safety Guidance</a></li><li><a href="https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sponsor-responsibilities-safety-reporting-requirements-and-safety-assessment-ind-and" rel="noopener noreferrer" target="_blank">FDA Sponsor Safety Guidance</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

"disproportionality-analysis-pharmacovigilance": """
<p>A disproportionality score can be perfectly correct mathematically and mean nothing clinically. The same score can also surface a pattern no individual reviewer would ever have spotted on their own.</p>
<p>What separates those two outcomes isn't the math. It's how the result gets read afterward.</p>
<p><strong>Disproportionality measures reporting imbalance. It doesn't measure incidence, absolute risk, or causality — and treating it as if it does is the single most common mistake in this field.</strong></p>
<p>Regulatory foundation: <a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-ix-addendum-i-methodological-aspects-signal-detection-spontaneous-reports-suspected-adverse-reactions_en.pdf" rel="noopener noreferrer" target="_blank">GVP IX Addendum</a>; <a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-ix-signal-management-rev-1_en.pdf" rel="noopener noreferrer" target="_blank">GVP IX</a>; <a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/pharmacovigilance-research-development/eudravigilance" rel="noopener noreferrer" target="_blank">EudraVigilance</a></p>
<h2 id="what-disproportionality-analysis-measures">What it's actually measuring</h2>
<p>It compares how often a drug–event pair shows up in reporting against how often other drug–event pairs show up in the same database. That's it. It's a hypothesis-generation tool for spontaneous-report data, not a diagnostic instrument — and most of the confusion around it comes from forgetting that distinction.</p>
<h2 id="prr-ror-and-ic">PRR, ROR, and IC — not interchangeable</h2>
<p>PRR compares event proportions for your product against comparators. ROR pulls odds from a two-by-two table. IC is a Bayesian measure, most associated with VigiBase. Different measures with different thresholds can flag different alerts on the exact same underlying data — which is worth remembering before treating any single number as definitive.</p>
<h2 id="what-the-numbers-cannot-tell-you">What the numbers genuinely can't tell you</h2>
<p>Spontaneous databases don't have reliable exposure denominators, and they're full of under-reporting, duplicates, missing data, and stimulated reporting. A high score isn't an incidence rate. A low score doesn't prove the product is safe. Neither reading survives contact with how the underlying data actually gets collected.</p>
<h2 id="stratification-and-sensitivity-analysis">Stratification and sensitivity checks</h2>
<p>Age, sex, country, indication, time period, reporter type, and which comparator you chose — any one of these can shift the result meaningfully. Running a sensitivity analysis, testing whether the pattern survives a few reasonable alternative assumptions, is how you find out whether you're looking at a real signal or an artifact of one specific setup.</p>
<h2 id="from-statistic-to-medical-review">Where the statistic hands off to a person</h2>
<p>Case narratives, chronology, coding accuracy, duplicates, outcomes, plausible alternative causes, the product's actual role — all of it needs a human reviewer once a statistic flags something. Compare against labels, literature, class effects, epidemiology, exposure. The number opens the door; it doesn't walk through it.</p>
<ul><li>Confirm the exact drug and event definitions.</li><li>Inspect the contributing cases individually.</li><li>Evaluate reporting context and likely biases.</li><li>Look for clinical coherence across the case series.</li><li>Define the specific safety question that needs validating.</li></ul>
<h2 id="common-interpretation-errors">Where people go wrong reading these</h2>
<p>Calling something a "positive signal" purely because a threshold got crossed. Comparing scores across different databases as if they're on the same scale. Ignoring small cell counts because the ratio looks dramatic. And the mirror-image mistake: treating the absence of disproportionality as proof there's no association at all, when it might just mean the data can't see it yet.</p>
<h2 id="ai-and-statistical-signal-detection">Where AI actually helps, and where it doesn't</h2>
<p>AI is genuinely useful for semantic grouping of related events and speeding up case review. It's also capable of amplifying exactly the same reporting biases it was trained on, if nobody's watching for that. Both the statistical output and anything AI-assisted need transparent methodology and a medically qualified person reviewing the result — neither replaces that.</p>
<h2 id="how-experienced-signal-teams-challenge-the-evidence">How experienced reviewers actually stress-test a signal</h2>
<p>They go looking for whatever might weaken the apparent association — duplicate cases, stimulated reporting, publicity effects, channeling bias, market growth, country-specific reporting quirks, concomitant treatment, the natural course of the underlying disease. That's not an attempt to make a safety concern disappear. It's exactly how a team avoids turning an avoidable false conclusion into a regulatory action nobody can walk back easily.</p>
<p>The opposite failure matters just as much. A numerically weak pattern shouldn't get dismissed if the clinical picture is distinctive, the outcomes are serious, the latency is plausible, or several cases show consistent dechallenge and rechallenge. Good signal work means being equally suspicious of amplification and of false reassurance — most teams are only trained to watch for one of those.</p>
<ul><li>Separate absence of evidence from evidence of absence.</li><li>Keep contradictory cases in view and explain what they do to the picture.</li><li>Compare the event at preferred-term, grouped-concept, and clinical-syndrome level.</li><li>Write down why the chosen comparator and time window are the right ones.</li></ul>
<h2 id="operational-governance-that-prevents-silent-signal-failure">Where signals quietly die if nobody's watching</h2>
<p>A signal tracker needs to hold the detection date, validation date, the accountable owner, status, the evidence actually reviewed, decisions made, actions taken, deadlines, and what closes or reopens the signal. Meeting minutes are not a signal-management system on their own — the record has to show how the conclusion evolved as new evidence came in, not just where it landed.</p>
<p>The handoffs between functions are where things go missing. Literature, case processing, medical review, epidemiology, regulatory affairs, labelling, risk management — each one might be holding a piece of the evidence, and a real governance model stops a relevant finding from getting trapped inside just one of them.</p>
<ul><li>Set escalation timelines by risk and urgency, not a fixed default.</li><li>Reconcile signal records against PBRERs, RMPs, and label changes.</li><li>Track overdue actions and gaps in the evidence, not just open signals.</li><li>Reopen closed signals when materially new information actually shows up.</li></ul>
<h2 id="a-practical-decision-scenario">A scenario that comes up more than you'd expect</h2>
<p>Three reports of the same rare neurological syndrome. Small case count, no disproportionality threshold crossed. But each case has plausible latency, extensive exclusion of alternative causes, and improvement after the drug was withdrawn. A mature signal system doesn't close this just because the statistic is quiet — it defines the clinical concept properly, pulls related cases and literature, weighs class and mechanistic evidence, and records whether the pattern is worth formal validation. This is exactly why quantitative surveillance can't stand alone.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>Database version and data cut are recorded.</li><li>Drug and event definitions are governed.</li><li>Duplicates and small counts are examined.</li><li>Comparator and stratification are justified.</li><li>Case-level review follows the alert.</li><li>No causality or incidence claim is made from disproportionality alone.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-is-prr">What is PRR?</h3>
<p>A measure comparing how often an event is reported for one product against how often it's reported for other products.</p>
<h3 id="what-is-ror">What is ROR?</h3>
<p>A reporting-odds measure, calculated from a two-by-two contingency table.</p>
<h3 id="what-is-ic">What is IC?</h3>
<p>A Bayesian disproportionality measure, used in global signal-detection contexts like VigiBase.</p>
<h3 id="does-a-positive-score-confirm-causality">Does a positive score confirm causality?</h3>
<p>No — it generates or supports a hypothesis that still needs medical and scientific assessment behind it.</p>
<h2 id="conclusion">Conclusion</h2>
<p>Disproportionality is useful precisely because of what it doesn't claim to do: it tells you where reporting looks unusual, nothing more. What happens after that is where the real work of signal management actually lives.</p>
<p><strong>Statistics can point at the door. Only clinical evidence can tell you whether there's an actual safety problem behind it.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-ix-addendum-i-methodological-aspects-signal-detection-spontaneous-reports-suspected-adverse-reactions_en.pdf" rel="noopener noreferrer" target="_blank">GVP IX Addendum</a></li><li><a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-gvp-module-ix-signal-management-rev-1_en.pdf" rel="noopener noreferrer" target="_blank">GVP IX</a></li><li><a href="https://www.ema.europa.eu/en/human-regulatory-overview/research-development/pharmacovigilance-research-development/eudravigilance" rel="noopener noreferrer" target="_blank">EudraVigilance</a></li><li><a href="https://www.fda.gov/drugs/surveillance/fda-adverse-event-reporting-system-faers" rel="noopener noreferrer" target="_blank">FDA FAERS</a></li><li><a href="https://who-umc.org/vigibase/" rel="noopener noreferrer" target="_blank">WHO VigiBase</a></li></ul>
<aside class="article-disclaimer"><strong>Professional scope:</strong> This article provides scientific and operational pharmacovigilance guidance. Applicable legislation, current regional requirements, company procedures and product-specific obligations must be assessed before regulatory action.</aside>
""",

"benefit-risk-evaluation-pharmacovigilance": """
<p>A medicine doesn't have one fixed benefit–risk balance that holds everywhere. It shifts by indication, by disease severity, by age, by comorbidity, by what else is available to treat the same condition, by dose, by how well the risk is actually being controlled in practice.</p>
<p>Which is why "benefits outweigh risks," stated on its own with no context, can sound completely reasonable and say almost nothing.</p>
<p><strong>Benefit–risk evaluation isn't arithmetic. It's structured judgement — the job is making the evidence, the values, and the uncertainty visible, not collapsing them into one number.</strong></p>
<p>Regulatory foundation: <a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a>; <a href="https://database.ich.org/sites/default/files/M4E_R2__Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH M4E(R2)</a>; <a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-module-v-risk-management-systems-rev-2_en.pdf" rel="noopener noreferrer" target="_blank">GVP V</a></p>
<h2 id="define-the-decision-context">Start by naming the actual decision</h2>
<p>Indication, population, how serious the disease is, whether there's unmet need, what alternatives exist, treatment duration, and — the part that's easy to skip — what decision is actually being made here. A benefit–risk write-up with no stated decision behind it tends to drift into generality fast.</p>
<h2 id="characterise-key-benefits">Characterising the benefits properly</h2>
<p>Magnitude, clinical relevance, how durable the effect is, which patients respond, how strong the underlying evidence actually is, and whether any of it translates cleanly into real-world practice. "It works" isn't a characterisation — for whom, by how much, and how confident are we, is.</p>
<h2 id="characterise-key-risks">Characterising the risks properly</h2>
<p>Seriousness, frequency, whether it's reversible, whether it's preventable, latency, which populations are more susceptible, and how much uncertainty is still attached. Reporting counts on their own tell you almost nothing about any of this.</p>
<h2 id="compare-on-common-dimensions">Comparing benefits and risks honestly</h2>
<p>Structured tables and frameworks make the differences visible without pretending that outcomes as different as, say, symptom relief and organ toxicity can be converted into one objective score. They usually can't — and a framework that implies otherwise is hiding a value judgement, not avoiding one.</p>
<h2 id="uncertainty-and-sensitivity">Where the uncertainty actually lives</h2>
<p>Name the missing evidence directly, then ask whether a reasonable alternative assumption would flip the conclusion. A conclusion that's genuinely robust survives that test — or it comes with a clear statement of exactly what would need to change for it to flip.</p>
<h2 id="from-conclusion-to-action">What a conclusion should actually lead to</h2>
<p>Continued monitoring, an additional study, revising the RMP, new risk-minimisation measures, a label change, restricted use, or escalating to the regulator. A benefit–risk conclusion that doesn't point toward one of these is missing its own point.</p>
<h2 id="ai-supported-benefit-risk">Where AI fits in this, honestly</h2>
<p>It can organise evidence and check internal consistency well. It can't supply the social values, the clinical accountability, or the regulatory judgement that this kind of decision actually requires. Anything AI-assisted here still needs to trace back to governed evidence a person can inspect.</p>
<h2 id="turning-a-safety-concern-into-a-measurable-control-strategy">Turning a concern into something you can actually measure</h2>
<p>Every important risk needs to become a concrete control problem. Which patients are susceptible? Under what clinical circumstances does the harm actually happen? Who — a prescriber, a patient, a system somewhere — is positioned to interrupt that pathway? What has to change in their knowledge or behaviour for that to happen? Which intervention is proportionate to the risk and actually feasible to run?</p>
<p>Skip that chain and risk management turns into a pile of documents nobody's really testing. Do it properly, and the additional PV activities fill the actual knowledge gap, the minimisation measures target the real causal pathway, and the effectiveness evaluation tells you honestly whether any of it changed how the product gets used.</p>
<ul><li>Define the target population and the specific preventable failure pathway.</li><li>Connect every additional activity to a decision-relevant knowledge gap.</li><li>Say plainly what success and failure will actually look like.</li><li>Decide in advance what happens if the measure underperforms.</li></ul>
<h2 id="benefit-risk-governance-across-the-product-lifecycle">Reassessing as the picture changes</h2>
<p>Benefit–risk needs a fresh look whenever a signal gets validated, an aggregate report finds a material change, new study data lands, utilisation patterns shift, a new population starts getting exposed, or the risk-minimisation results challenge assumptions the team made earlier. It has to stay indication- and population-specific — a global restatement doesn't hold up.</p>
<p>Governance means recording the decision context, the evidence version used, the key benefits and risks, the uncertainty, the expert judgement behind it, and the resulting action. A conclusion nobody can reconstruct months later isn't durable enough to survive an inspection, let alone a real patient-safety decision.</p>
<ul><li>Align signal, PBRER, and RMP conclusions with each other.</li><li>Write down dissent and whatever uncertainty stayed unresolved.</li><li>Set the thresholds that would trigger a reassessment.</li><li>Track whether the actions taken actually achieved what they were meant to.</li></ul>
<h2 id="a-practical-decision-scenario">Where this can quietly go wrong</h2>
<p>Take an educational programme built to prevent a serious drug interaction. It reaches 98% of target prescribers — looks like a clear success on delivery. Then a utilisation study shows the contraindicated co-prescribing hasn't actually changed. The correct read isn't "the programme worked, the materials went out." Something in comprehension, workflow, or timing is breaking down, and the organisation has to dig into which one before deciding whether to modify the intervention or replace it — and keep measuring outcomes either way.</p>
<h2 id="inspection-ready-checklist">Inspection-ready checklist</h2>
<ul><li>Decision context is defined.</li><li>Benefits are clinically meaningful.</li><li>Risks include severity and preventability.</li><li>Population differences are considered.</li><li>Uncertainty is explicit.</li><li>Alternative assumptions are tested.</li><li>Conclusion leads to action and monitoring.</li></ul>
<h2 id="frequently-asked-questions">Frequently asked questions</h2>
<h3 id="what-is-benefit-risk-evaluation">What is benefit–risk evaluation?</h3>
<p>A structured assessment of a product's favourable and unfavourable effects, the uncertainty around them, and the therapeutic context they sit in.</p>
<h3 id="is-benefit-risk-one-numerical-score">Is benefit–risk one numerical score?</h3>
<p>Usually not. Quantitative tools can support the judgement, but clinical outcomes and human values rarely reduce cleanly to one comparable number.</p>
<h3 id="can-benefit-risk-differ-by-population">Can benefit–risk differ by population?</h3>
<p>Yes, meaningfully — baseline risk, treatment benefit, available alternatives, and susceptibility can all shift the balance from one population to the next.</p>
<h3 id="when-should-benefit-risk-be-reassessed">When should benefit–risk be reassessed?</h3>
<p>Whenever material new evidence shows up — signals, exposure changes, efficacy findings, or results from risk-control measures.</p>
<h2 id="conclusion">Conclusion</h2>
<p>A defensible benefit–risk conclusion doesn't hide the complexity underneath it. It structures that complexity so whoever's deciding can actually see what evidence supports continued use, which patients stand to benefit, which might be harmed, and what has to happen next.</p>
<p><strong>The conclusion only earns credibility when it says not just that benefits outweigh risks, but for whom, under what conditions, and with what uncertainty still left over.</strong></p>
<h2 id="authoritative-references">Authoritative references</h2>
<ul><li><a href="https://database.ich.org/sites/default/files/E2C_R2_Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH E2C(R2)</a></li><li><a href="https://database.ich.org/sites/default/files/M4E_R2__Guideline.pdf" rel="noopener noreferrer" target="_blank">ICH M4E(R2)</a></li><li><a href="https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-good-pharmacovigilance-practices-module-v-risk-management-systems-rev-2_en.pdf" rel="noopener noreferrer" target="_blank">GVP V</a></li><li><a href="https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline/guideline-good-pharmacovigilance-practices-gvp-module-xvi-risk-minimisation-measures-rev-3_en.pdf" rel="noopener noreferrer" target="_blank">GVP XVI</a></li></ul>
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
