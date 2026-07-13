(() => {
  'use strict';
  const config = window.CLINIXAI_ANALYTICS || {};
  const consentKey = 'clinixai-analytics-consent-v1';
  const getConsent = () => localStorage.getItem(consentKey);
  const setConsent = (value) => localStorage.setItem(consentKey, value);

  function loadScript(src, id) {
    if (document.getElementById(id)) return;
    const script = document.createElement('script');
    script.id = id; script.async = true; script.src = src;
    document.head.appendChild(script);
  }

  function enableAnalytics() {
    if (!config.enabled) return;
    if (config.googleMeasurementId) {
      loadScript(`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(config.googleMeasurementId)}`, 'clinixai-ga');
      window.dataLayer = window.dataLayer || [];
      window.gtag = window.gtag || function(){ window.dataLayer.push(arguments); };
      window.gtag('js', new Date());
      window.gtag('config', config.googleMeasurementId, { anonymize_ip: true, send_page_view: true });
    }
    if (config.clarityProjectId) {
      (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=1;t.src='https://www.clarity.ms/tag/'+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,'clarity','script',config.clarityProjectId);
    }
  }

  function track(name, parameters = {}) {
    if (getConsent() !== 'accepted') return;
    if (typeof window.gtag === 'function') window.gtag('event', name, parameters);
  }

  function bindEvents() {
    document.addEventListener('click', (event) => {
      const link = event.target.closest('a');
      if (!link) return;
      const href = link.getAttribute('href') || '';
      if (href.includes('contact') || href.includes('#demo')) track('cta_click', { link_text: link.textContent.trim(), link_url: href });
      if (/\.(pdf|docx?|xlsx?)($|\?)/i.test(href)) track('file_download', { file_url: href });
      if (link.host && link.host !== location.host) track('outbound_click', { link_url: link.href });
    });
    document.addEventListener('submit', (event) => {
      const form = event.target.closest('form');
      if (form) track('form_submit', { form_name: form.getAttribute('name') || form.id || 'website_form' });
    });
  }

  function createBanner() {
    if (!config.enabled || !config.consentRequired || getConsent()) return;
    const banner = document.createElement('section');
    banner.className = 'consent-banner'; banner.setAttribute('role','dialog');
    banner.setAttribute('aria-label','Analytics preferences');
    banner.innerHTML = `<p>We use optional analytics to understand website performance. No analytics load until you accept.</p><div class="consent-actions"><button class="btn btn-light" type="button" data-consent="declined">Decline</button><button class="btn btn-primary" type="button" data-consent="accepted">Accept analytics</button></div>`;
    banner.addEventListener('click', (event) => {
      const button = event.target.closest('[data-consent]'); if (!button) return;
      const value = button.dataset.consent; setConsent(value); banner.remove();
      if (value === 'accepted') enableAnalytics();
    });
    document.body.appendChild(banner);
  }

  function init() {
    bindEvents();
    if (getConsent() === 'accepted') enableAnalytics();
    else createBanner();
  }
  window.clinixaiTrack = track;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true}); else init();
})();
