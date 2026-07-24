(() => {
  'use strict';
  const endpoint = '/api/analytics-event';
  const storageKey = 'clinixai_attribution_v1';
  const sessionKey = 'clinixai_session_v1';
  const allowedUtm = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  const sessionId = sessionStorage.getItem(sessionKey) || (crypto.randomUUID?.() || `s-${Date.now()}-${Math.random().toString(16).slice(2)}`);
  sessionStorage.setItem(sessionKey, sessionId);

  const query = new URLSearchParams(location.search);
  const incoming = Object.fromEntries(allowedUtm.filter(key => query.has(key)).map(key => [key, query.get(key).slice(0, 160)]));
  let attribution = {};
  try { attribution = JSON.parse(localStorage.getItem(storageKey) || '{}'); } catch {}
  if (Object.keys(incoming).length) {
    attribution = { first: attribution.first || incoming, last: incoming };
    localStorage.setItem(storageKey, JSON.stringify(attribution));
  }

  function emit(event, detail = {}) {
    const payload = {
      event,
      path: location.pathname,
      page_title: document.title.slice(0, 180),
      session_id: sessionId,
      timestamp: new Date().toISOString(),
      attribution,
      ...detail
    };
    const body = JSON.stringify(payload);
    if (navigator.sendBeacon) navigator.sendBeacon(endpoint, new Blob([body], { type: 'application/json' }));
    else fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body, keepalive: true }).catch(() => {});
    if (typeof window.gtag === 'function') window.gtag('event', event, detail);
    window.dispatchEvent(new CustomEvent('clinixai:analytics', { detail: payload }));
  }

  emit('page_view', { referrer_host: document.referrer ? new URL(document.referrer).hostname : '' });

  document.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link) return;
    const href = link.getAttribute('href') || '';
    const label = (link.textContent || link.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 120);
    if (href.startsWith('/contact') || /discovery|demo|contact|discuss/i.test(label)) emit('cta_click', { label, destination: href });
    if (/\.(pdf|docx|zip)(?:$|\?)/i.test(href)) emit('resource_download', { label, destination: href.split('?')[0] });
    if (/^https?:\/\//i.test(href) && new URL(href).hostname !== location.hostname) emit('outbound_click', { label, destination_host: new URL(href).hostname });
  });

  document.querySelectorAll('form').forEach(form => {
    let started = false;
    form.addEventListener('focusin', () => {
      if (started) return;
      started = true;
      emit('form_start', { form_action: form.getAttribute('action') || location.pathname });
    });
    form.addEventListener('submit', () => emit('form_submit', { form_action: form.getAttribute('action') || location.pathname }));
    const values = { ...(attribution.first || {}), ...(attribution.last || {}) };
    Object.entries(values).forEach(([name, value]) => {
      let input = form.querySelector(`input[name="${name}"]`);
      if (!input) {
        input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        form.appendChild(input);
      }
      input.value = String(value);
    });
  });

  const reached = new Set();
  addEventListener('scroll', () => {
    const available = document.documentElement.scrollHeight - innerHeight;
    if (available <= 0) return;
    const depth = Math.round((scrollY / available) * 100);
    [25, 50, 75, 90].forEach(mark => {
      if (depth >= mark && !reached.has(mark)) {
        reached.add(mark);
        emit('scroll_depth', { percent: mark });
      }
    });
  }, { passive: true });
})();
