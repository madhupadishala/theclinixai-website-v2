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

async function loadPartial(id,file){const el=document.getElementById(id);if(!el)return;try{const r=await fetch(file);el.innerHTML=await r.text()}catch(e){console.error(e)}}
Promise.all([loadPartial('site-header','/header.html'),loadPartial('site-footer','/footer.html')]).then(()=>{const h=document.querySelector('[data-header]'),btn=document.querySelector('.menu-toggle'),nav=document.querySelector('.primary-nav');window.addEventListener('scroll',()=>h?.classList.toggle('is-scrolled',scrollY>12));btn?.addEventListener('click',()=>{const open=nav.classList.toggle('open');btn.setAttribute('aria-expanded',String(open))});const path=location.pathname,resourcesMenu=document.querySelector('[data-resources-menu]');if(path==='/resources'||path.startsWith('/insights/'))resourcesMenu?.classList.add('is-current');document.addEventListener('click',event=>{if(!resourcesMenu?.contains(event.target))resourcesMenu?.removeAttribute('open')});document.addEventListener('keydown',event=>{if(event.key==='Escape')resourcesMenu?.removeAttribute('open')});document.querySelectorAll('.primary-nav a').forEach(a=>{const href=a.getAttribute('href')||'';if(href===path||href===`${path}.html`)a.setAttribute('aria-current','page')})});

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
