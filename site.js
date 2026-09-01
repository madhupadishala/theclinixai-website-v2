/* CLINIXAI CONSENT + GA4 START */
(() => {
  'use strict';

  const MEASUREMENT_ID = 'G-CVZZ0ZGPGQ';
  const CONSENT_KEY = 'clinixai_consent_v1';
  const CONSENT_VERSION = 1;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() {
    window.dataLayer.push(arguments);
  };

  const googleConsent = analytics => ({
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: analytics ? 'granted' : 'denied',
    functionality_storage: 'granted',
    personalization_storage: 'denied',
    security_storage: 'granted'
  });

  window.gtag('consent', 'default', {
    ...googleConsent(false),
    wait_for_update: 500
  });
  window.gtag('set', 'ads_data_redaction', true);
  window.gtag('set', 'url_passthrough', false);

  let savedConsent = null;
  try {
    const parsed = JSON.parse(localStorage.getItem(CONSENT_KEY) || 'null');
    if (parsed?.version === CONSENT_VERSION && typeof parsed.analytics === 'boolean') {
      savedConsent = parsed;
    }
  } catch {}

  const consentState = {
    analytics: savedConsent?.analytics === true,
    decided: Boolean(savedConsent)
  };
  window.ClinixAIConsent = consentState;

  let googleAnalyticsLoaded = false;
  const loadGoogleAnalytics = () => {
    if (googleAnalyticsLoaded || !consentState.analytics) return;
    googleAnalyticsLoaded = true;
    window.gtag('js', new Date());
    window.gtag('config', MEASUREMENT_ID, {
      send_page_view: false,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(MEASUREMENT_ID)}`;
    script.dataset.clinixaiGa4 = 'true';
    document.head.appendChild(script);
  };

  const announceConsent = () => {
    window.dispatchEvent(new CustomEvent('clinixai:consentchange', {
      detail: { analytics: consentState.analytics, decided: consentState.decided }
    }));
  };

  const applyConsent = (analytics, persist = true) => {
    consentState.analytics = Boolean(analytics);
    consentState.decided = true;
    if (persist) {
      localStorage.setItem(CONSENT_KEY, JSON.stringify({
        version: CONSENT_VERSION,
        analytics: consentState.analytics,
        updated_at: new Date().toISOString()
      }));
    }
    window.gtag('consent', 'update', googleConsent(consentState.analytics));
    if (consentState.analytics) loadGoogleAnalytics();
    announceConsent();
  };

  if (savedConsent) {
    window.gtag('consent', 'update', googleConsent(consentState.analytics));
    loadGoogleAnalytics();
  }

  const mountConsentControls = () => {
    if (document.querySelector('[data-consent-banner]')) return;

    const banner = document.createElement('section');
    banner.className = 'consent-banner';
    banner.dataset.consentBanner = 'true';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-modal', 'false');
    banner.setAttribute('aria-labelledby', 'consent-title');
    banner.hidden = consentState.decided;
    banner.innerHTML = `
      <div class="consent-banner__mark" aria-hidden="true">C</div>
      <div class="consent-banner__copy">
        <p class="consent-banner__eyebrow">Privacy choices</p>
        <h2 id="consent-title">Your privacy. Your decision.</h2>
        <p>We use essential storage to operate this website. With your permission, analytics helps us understand which ClinixAI content and services are useful. We never send form contents to analytics.</p>
        <div class="consent-banner__links">
          <a href="/privacy-policy">Privacy policy</a>
          <a href="/cookie-policy">Cookie policy</a>
        </div>
      </div>
      <div class="consent-banner__actions">
        <button class="consent-button consent-button--primary" type="button" data-consent-accept>Accept analytics</button>
        <button class="consent-button consent-button--secondary" type="button" data-consent-reject>Reject optional</button>
        <button class="consent-button consent-button--text" type="button" data-consent-manage>Manage settings</button>
      </div>`;

    const settingsButton = document.createElement('button');
    settingsButton.className = 'cookie-settings-button';
    settingsButton.type = 'button';
    settingsButton.dataset.cookieSettings = 'true';
    settingsButton.setAttribute('aria-label', 'Open cookie settings');
    settingsButton.innerHTML = '<span aria-hidden="true">◌</span> Cookie settings';

    const modal = document.createElement('div');
    modal.className = 'consent-modal';
    modal.dataset.consentModal = 'true';
    modal.hidden = true;
    modal.innerHTML = `
      <div class="consent-modal__backdrop" data-consent-close></div>
      <section class="consent-modal__panel" role="dialog" aria-modal="true" aria-labelledby="consent-settings-title">
        <div class="consent-modal__head">
          <div>
            <p class="consent-banner__eyebrow">ClinixAI privacy centre</p>
            <h2 id="consent-settings-title">Cookie settings</h2>
          </div>
          <button class="consent-modal__close" type="button" aria-label="Close cookie settings" data-consent-close>×</button>
        </div>
        <div class="consent-option">
          <div>
            <strong>Essential storage</strong>
            <p>Required for security and remembering your privacy choice. It cannot be switched off.</p>
          </div>
          <span class="consent-status">Always active</span>
        </div>
        <label class="consent-option consent-option--toggle">
          <div>
            <strong>Analytics</strong>
            <p>Helps us measure visits, content engagement and enquiry journeys without sending form contents.</p>
          </div>
          <input type="checkbox" data-consent-analytics>
          <span class="consent-switch" aria-hidden="true"></span>
        </label>
        <p class="consent-modal__note">Advertising and personalised-advertising storage remain disabled on this website.</p>
        <div class="consent-modal__actions">
          <button class="consent-button consent-button--primary" type="button" data-consent-save>Save preferences</button>
          <button class="consent-button consent-button--secondary" type="button" data-consent-reject>Reject optional</button>
        </div>
      </section>`;

    document.body.append(banner, settingsButton, modal);

    const analyticsToggle = modal.querySelector('[data-consent-analytics]');
    let restoreFocus = null;

    const closeModal = () => {
      modal.hidden = true;
      document.documentElement.classList.remove('consent-modal-open');
      restoreFocus?.focus();
    };
    const openModal = trigger => {
      restoreFocus = trigger || document.activeElement;
      analyticsToggle.checked = consentState.analytics;
      modal.hidden = false;
      document.documentElement.classList.add('consent-modal-open');
      modal.querySelector('.consent-modal__close').focus();
    };
    const finishChoice = analytics => {
      applyConsent(analytics);
      banner.hidden = true;
      closeModal();
    };

    document.addEventListener('click', event => {
      const target = event.target.closest(
        '[data-consent-accept],[data-consent-reject],[data-consent-manage],[data-consent-save],[data-consent-close],[data-cookie-settings]'
      );
      if (!target) return;
      if (target.matches('[data-consent-accept]')) finishChoice(true);
      else if (target.matches('[data-consent-reject]')) finishChoice(false);
      else if (target.matches('[data-consent-manage],[data-cookie-settings]')) openModal(target);
      else if (target.matches('[data-consent-save]')) finishChoice(analyticsToggle.checked);
      else if (target.matches('[data-consent-close]')) closeModal();
    });

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !modal.hidden) closeModal();
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountConsentControls, { once: true });
  } else {
    mountConsentControls();
  }
})();
/* CLINIXAI CONSENT + GA4 END */

async function loadPartial(id,file){const el=document.getElementById(id);if(!el||el.childElementCount>0)return;try{const r=await fetch(file);el.innerHTML=await r.text()}catch(e){console.error(e)}}
Promise.all([loadPartial('site-header','/header.html'),loadPartial('site-footer','/footer.html')]).then(()=>{const h=document.querySelector('[data-header]'),btn=document.querySelector('.menu-toggle'),nav=document.querySelector('.primary-nav');window.addEventListener('scroll',()=>h?.classList.toggle('is-scrolled',scrollY>12));btn?.addEventListener('click',()=>{const open=nav.classList.toggle('open');btn.setAttribute('aria-expanded',String(open))});const path=location.pathname,resourcesMenu=document.querySelector('[data-resources-menu]'),careersMenu=document.querySelector('[data-careers-menu]'),resourceMenus=[resourcesMenu,careersMenu].filter(Boolean);if(path==='/resources'||path==='/insights'||path.startsWith('/insights/'))resourcesMenu?.classList.add('is-current');if(path==='/careers'||path.startsWith('/careers')||path==='/academy')careersMenu?.classList.add('is-current');const closeMenu=menu=>{menu.classList.remove('is-open');menu.querySelector('.nav-resource-menu__toggle')?.setAttribute('aria-expanded','false')};resourceMenus.forEach(menu=>{menu.querySelector('.nav-resource-menu__toggle')?.addEventListener('click',event=>{event.stopPropagation();const open=menu.classList.toggle('is-open');menu.querySelector('.nav-resource-menu__toggle').setAttribute('aria-expanded',String(open));resourceMenus.filter(m=>m!==menu).forEach(closeMenu)})});document.addEventListener('click',event=>{resourceMenus.forEach(menu=>{if(!menu.contains(event.target))closeMenu(menu)})});document.addEventListener('keydown',event=>{if(event.key==='Escape')resourceMenus.forEach(closeMenu)});document.querySelectorAll('.primary-nav a').forEach(a=>{const href=a.getAttribute('href')||'';if(href===path||href===`${path}.html`)a.setAttribute('aria-current','page')})});

const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;

document.querySelectorAll('[data-showcase]').forEach(box=>{
  const track=box.querySelector('.showcase-track');
  if(!track)return;
  const scope=box.closest('section')||box.parentElement;
  const prev=scope?.querySelector('[data-prev]');
  const next=scope?.querySelector('[data-next]');
  const interval=Math.max(4200,Number(box.dataset.interval||6500));
  const step=()=>{const card=track.querySelector(':scope > *');if(!card)return 320;const gap=parseFloat(getComputedStyle(track).columnGap||getComputedStyle(track).gap||'16')||16;return card.getBoundingClientRect().width+gap};
  const canMove=()=>track.scrollWidth>track.clientWidth+8;
  const go=d=>{if(!canMove())return;track.scrollBy({left:d*step(),behavior:reduced?'auto':'smooth'})};
  prev?.addEventListener('click',()=>go(-1));
  next?.addEventListener('click',()=>go(1));
  let visible=false;
  let timer=null;
  const stop=()=>{if(timer){clearInterval(timer);timer=null}};
  const start=()=>{stop();if(reduced||!visible||!canMove())return;timer=setInterval(()=>{if(box.matches(':hover,:focus-within'))return;const atEnd=track.scrollLeft+track.clientWidth>=track.scrollWidth-8;track.scrollTo({left:atEnd?0:track.scrollLeft+step(),behavior:'smooth'})},interval)};
  new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;start()},{threshold:.28}).observe(box);
  new MutationObserver(start).observe(track,{childList:true});
  box.addEventListener('mouseenter',stop);
  box.addEventListener('mouseleave',start);
  box.addEventListener('focusin',stop);
  box.addEventListener('focusout',start);
  window.addEventListener('resize',start);
});

document.querySelectorAll('[data-outcomes]').forEach(stack=>{const cards=[...stack.children];let i=0;cards[0]?.classList.add('active');if(!reduced)setInterval(()=>{cards[i].classList.remove('active');i=(i+1)%cards.length;cards[i].classList.add('active')},3000)});

const box=document.querySelector('[data-word-limit]'),count=document.querySelector('[data-word-count]');box?.addEventListener('input',()=>{let words=box.value.trim()?box.value.trim().split(/\s+/):[];if(words.length>300){box.value=words.slice(0,300).join(' ');words=words.slice(0,300)}if(count)count.textContent=`${words.length} / 300 words`});

document.querySelectorAll('[data-modal-open]').forEach(b=>b.addEventListener('click',()=>document.getElementById(b.dataset.modalOpen)?.classList.add('open')));document.querySelectorAll('[data-modal-close]').forEach(b=>b.addEventListener('click',()=>b.closest('.modal')?.classList.remove('open')));document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.modal.open').forEach(m=>m.classList.remove('open'))});

if(!document.querySelector('script[data-clinixai-analytics]')){const analytics=document.createElement('script');analytics.src='/analytics.js?v=20260724-consent';analytics.defer=true;analytics.dataset.clinixaiAnalytics='true';document.head.appendChild(analytics)}


/* CLINIXAI SEARCH-INTENT FAQ START */
(() => {
  const FAQS = {
    '/ai-literature-screening-pharmacovigilance': [
      ['How does AI literature screening support pharmacovigilance teams?', 'AI literature screening helps teams organize search results, identify product and safety concepts, prioritize review and preserve traceable evidence. A qualified safety professional remains responsible for confirming relevance and making the final decision.'],
      ['Can AI literature screening replace human medical review?', 'No. AI can accelerate repetitive review steps and surface evidence, but medical relevance, case validity, country obligations and reportability require governed human oversight. The intended model is human-in-the-loop decision support.'],
      ['How should a pharmacovigilance team validate AI literature screening?', 'Validation should use a representative labelled dataset and report sensitivity, specificity, precision, recall, false negatives, false positives and subgroup performance. Teams should also test audit trails, overrides, version control, access controls and performance after change.'],
      ['What evidence should buyers request from an AI literature screening provider?', 'Buyers should request the intended-use statement, validation methodology, dataset characteristics, error analysis, human-review controls, auditability, security boundaries and change-governance process. Demonstrations alone are not evidence of production suitability.']
    ],
    '/pharmacovigilance-literature-monitoring-software': [
      ['How can pharmacovigilance literature monitoring software reduce manual workload?', 'Literature monitoring software can consolidate searches, deduplicate citations, organize product matches and route articles for review. The benefit comes from reducing avoidable handling while retaining documented human decisions for safety-relevant content.'],
      ['What should pharmacovigilance literature monitoring software track?', 'A governed system should track the search strategy, database, run date, retrieved records, duplicates, screening decisions, reviewer actions, supporting evidence, follow-up and final disposition. The record should remain attributable and reproducible.'],
      ['Can literature monitoring software support weekly and local literature searches?', 'Software can schedule global and local searches, record missed runs and preserve versioned search strategies. Actual source coverage and frequency must be configured to the marketing-authorisation holder’s products, countries and approved procedures.'],
      ['How should a company evaluate literature monitoring software pricing?', 'Evaluate total operating cost rather than licence price alone. Consider implementation, source access, configuration, validation, reviewer effort, integrations, support, change control and the cost of correcting false negatives or poorly documented decisions.']
    ],
    '/nexus-platform': [
      ['What pharmacovigilance processes is the ClinixAI Nexus platform designed to support?', 'Nexus is designed as a governed pharmacovigilance workspace connecting intake, literature, case assessment, quality oversight and safety intelligence. Availability and production readiness should be confirmed module by module during a discovery review.'],
      ['How does the ClinixAI Nexus platform maintain decision traceability?', 'The design emphasizes source-linked evidence, attributable user actions, decision reasons, review status, overrides and version history. Final traceability depends on the configured workflow, integrations and approved operating procedures.'],
      ['Can the ClinixAI Nexus platform integrate with an existing safety system?', 'Integration feasibility depends on the existing safety database, available APIs, data standards, security requirements and validated interfaces. The appropriate pattern is determined during technical discovery rather than assumed from a generic connector claim.'],
      ['Who should participate in a ClinixAI Nexus platform evaluation?', 'Include pharmacovigilance operations, medical review, quality, validation, information security, privacy and system owners. A cross-functional evaluation prevents a technically attractive workflow from creating regulatory or operational gaps.']
    ],
    '/icsr-case-processing-software': [
      ['How does ICSR case processing software support pharmacovigilance operations?', 'ICSR software can structure intake, triage, data entry, coding, medical review, quality control and submission preparation. It should support the approved process without obscuring who made each safety decision or why.'],
      ['What controls are essential in ICSR case processing software?', 'Essential controls include role-based access, audit trails, case versioning, duplicate management, controlled terminology, workflow status, due-date monitoring, validation evidence and secure data handling. Requirements should be risk assessed before configuration.'],
      ['Can ICSR case processing software automate case validity decisions?', 'Software can highlight identifiable patient, reporter, suspect product and adverse-event evidence, but ambiguous cases require qualified review. Automation should explain the supporting source text and allow documented confirmation or override.'],
      ['How should an organisation plan ICSR software implementation?', 'Start with intended use, process mapping, data requirements, interfaces, roles and validation strategy. Follow with controlled configuration, migration testing, user acceptance, training, release approval and post-production monitoring.']
    ],
    '/icsr-quality-control-automation': [
      ['How can ICSR quality control automation improve review consistency?', 'Quality-control automation can apply repeatable checks for completeness, chronology, coding, consistency and required documentation. It should prioritize risks and show the evidence behind each flag so reviewers can confirm or reject it.'],
      ['Which ICSR quality checks should remain under human control?', 'Medical judgement, causality interpretation, narrative adequacy, clinically meaningful chronology and context-dependent exceptions require qualified human review. Automated checks should support—not silently replace—those decisions.'],
      ['How should automated ICSR quality-control performance be measured?', 'Measure defect detection by category, false-positive burden, false negatives, reviewer agreement, override reasons and time saved. Results should be stratified by case type and monitored after rules, models or source formats change.'],
      ['Does ICSR quality-control automation eliminate the need for sampling?', 'Not automatically. Sampling and oversight should be based on validated performance, process risk, defect trends and procedural requirements. Organisations should reduce review only when evidence supports the residual risk.']
    ],
    '/aggregate-safety-reporting-software': [
      ['How does aggregate safety reporting software support PBRER, PSUR and DSUR preparation?', 'Aggregate reporting software can organize data-lock activities, source reconciliation, analyses, authoring tasks, review comments and approvals. Regulatory interpretation and benefit-risk conclusions remain the responsibility of qualified contributors.'],
      ['What should an aggregate safety reporting system make traceable?', 'The system should connect source data, analyses, document sections, contributors, review comments, approvals, versions and submission milestones. Traceability should allow a reviewer to understand how each material conclusion was supported.'],
      ['Can aggregate reporting software prevent data-lock delays?', 'It can expose missing inputs, reconciliation gaps, overdue tasks and unresolved reviews earlier. Preventing delay also requires clear ownership, realistic planning, escalation routes and timely source-system availability.'],
      ['How should teams compare aggregate safety reporting software?', 'Compare supported report types, workflow flexibility, data lineage, authoring controls, integrations, validation, security, implementation effort and reviewer usability. Feature counts alone do not show whether the system fits an approved reporting process.']
    ],
    '/pharmacovigilance-signal-management-software': [
      ['How does pharmacovigilance signal management software support signal governance?', 'Signal management software can centralize detection outputs, validation evidence, assessments, decisions, actions and review history. It should make governance clearer without converting statistical alerts into unsupported safety conclusions.'],
      ['What is the difference between a safety alert and a validated signal?', 'An alert is an observation requiring review; it is not automatically a validated signal. Validation considers clinical relevance, strength of evidence, alternative explanations, novelty and the applicable product context.'],
      ['Which data sources can pharmacovigilance signal management software use?', 'Potential sources include spontaneous reports, literature, clinical studies, observational data, product complaints and regulatory information. Source suitability, licensing, quality and limitations must be documented for the intended analysis.'],
      ['How should signal management software preserve auditability?', 'It should record source data references, methods, thresholds, reviewer actions, decision rationale, approvals, changes and follow-up. Users must be able to reconstruct the path from detection through closure or escalation.']
    ],
    '/hospital-medication-safety-software': [
      ['How can hospital medication safety software improve incident reporting?', 'Medication safety software can provide a consistent reporting route, capture essential context, route events to the right reviewers and track corrective actions. A psychologically safe reporting culture is still necessary for complete and timely reporting.'],
      ['What information should a hospital medication incident report capture?', 'Capture the medication, event, patient context, stage of the medication-use process, outcome, contributing factors, immediate actions and reporter details permitted by policy. Data collection should remain proportionate and privacy controlled.'],
      ['Can medication safety software support root-cause analysis and CAPA?', 'Software can organize evidence, contributing factors, actions, owners, due dates and effectiveness checks. The quality of root-cause analysis still depends on multidisciplinary review and avoiding conclusions unsupported by evidence.'],
      ['How should hospitals evaluate medication safety software pricing?', 'Consider reporting volume, users, workflow configuration, integrations, implementation, training, support, analytics and security—not only the subscription fee. A phased engagement may be appropriate when the reporting process is still maturing.']
    ],
    '/academy': [
      ['What practical work is included in the ClinixAI pharmacovigilance internship?', 'The programme uses controlled internal learning scenarios covering literature screening, case thinking, quality review and role-specific PV activities according to the selected route. It does not involve processing client cases or submitting reports for a marketing-authorisation holder.'],
      ['Is the ClinixAI pharmacovigilance internship a job or employment offer?', 'No. It is a structured learning and internal-project engagement, not salaried employment or a job guarantee. Participation evidence reflects verified attendance, assignments, review and contribution under the programme policy.'],
      ['How long is the ClinixAI pharmacovigilance internship?', 'The published routes are designed as three-month programmes. Schedule, mentoring level, eligibility and included learning areas differ by route and should be reviewed before applying.'],
      ['How should applicants choose between free and paid pharmacovigilance internship routes?', 'Choose based on the required depth, mentoring, schedule and intended capability—not the certificate alone. Applicants should compare the visible programme table, confirm eligibility and ask about deliverables before making a payment decision.']
    ],
    '/services': [
      ['Which pharmacovigilance services does TheClinixAI provide?', 'TheClinixAI presents capabilities across literature monitoring, ICSR operations, medical review, quality management, aggregate reporting, signal management, submissions, inspection readiness and PV technology strategy. Scope is confirmed for each engagement.'],
      ['How does a pharmacovigilance consulting engagement begin?', 'It begins with a discovery discussion covering the problem, products, countries, systems, procedures, volume, risks and expected outcome. The resulting scope should define responsibilities, assumptions, deliverables, timeline and acceptance criteria.'],
      ['Can TheClinixAI support a limited pharmacovigilance project budget?', 'A focused assessment, pilot, advisory package or phased implementation may be possible when the scope and risk boundaries are clear. Pricing should be based on actual deliverables and governance needs rather than an unsupported generic package.'],
      ['What information is needed for a pharmacovigilance service quotation?', 'Share the required service, jurisdictions, product lifecycle, approximate volume, systems, integrations, timeline, validation expectations and current pain points. Sensitive or personal data should not be sent during the initial enquiry.']
    ]
  };

  const normalizedPath = location.pathname.replace(/\.html$/, '').replace(/\/+$/, '') || '/';
  const items = FAQS[normalizedPath];
  if (!items || document.querySelector('[data-search-faq]')) return;

  const mount = () => {
    const main = document.querySelector('main');
    if (!main || document.querySelector('[data-search-faq]')) return;
    const section = document.createElement('section');
    section.className = 'search-faq';
    section.dataset.searchFaq = 'true';
    section.setAttribute('aria-labelledby', 'search-faq-title');
    section.innerHTML = '<div class="shell"><p class="search-faq__eyebrow">QUESTIONS BUYERS AND REVIEWERS ASK</p><h2 id="search-faq-title">Frequently asked questions</h2><div class="search-faq__list"></div></div>';
    const list = section.querySelector('.search-faq__list');
    items.forEach(([question, answer], index) => {
      const details = document.createElement('details');
      details.className = 'search-faq__item';
      if (index === 0) details.open = true;
      const summary = document.createElement('summary');
      summary.textContent = question;
      const paragraph = document.createElement('p');
      paragraph.textContent = answer;
      details.append(summary, paragraph);
      list.append(details);
    });
    main.append(section);

    const schema = document.createElement('script');
    schema.type = 'application/ld+json';
    schema.dataset.searchFaqSchema = 'true';
    schema.textContent = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: items.map(([question, answer]) => ({
        '@type': 'Question',
        name: question,
        acceptedAnswer: { '@type': 'Answer', text: answer }
      }))
    });
    document.head.append(schema);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount, { once: true });
  } else {
    mount();
  }
})();
/* CLINIXAI SEARCH-INTENT FAQ END */
