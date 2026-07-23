(() => {
  'use strict';

  const config = window.CLINIXAI_CONTENT_CONFIG || {};
  const ENDPOINT = config.endpoint || '/api/content';
  const BLOG_URL = config.blogUrl || 'https://blogs.theclinixai.com';
  const CACHE_TTL = (config.cacheTtlMinutes || 15) * 60 * 1000;
  const REQUEST_TIMEOUT = config.requestTimeoutMs || 8000;

  const stripHtml = (value = '') => {
    const node = document.createElement('div');
    node.innerHTML = value;
    return (node.textContent || '').replace(/\s+/g, ' ').trim();
  };

  const escapeHtml = (value = '') => String(value).replace(/[&<>'"]/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  })[character]);

  const cacheKey = (limit, category) => `clinixai:content:v3:${limit}:${category || 'all'}`;

  function readCache(key) {
    try {
      const cached = JSON.parse(localStorage.getItem(key) || 'null');
      return cached && Date.now() - cached.savedAt < CACHE_TTL ? cached.value : null;
    } catch { return null; }
  }

  function saveCache(key, value) {
    try { localStorage.setItem(key, JSON.stringify({ savedAt: Date.now(), value })); } catch {}
  }

  const getFeaturedImage = (post) => {
    const media = post?._embedded?.['wp:featuredmedia']?.[0];
    return media?.media_details?.sizes?.medium_large?.source_url || media?.source_url || '';
  };

  const getCategory = (post) => {
    const terms = post?._embedded?.['wp:term']?.flat?.() || [];
    return terms.find((term) => term.taxonomy === 'category')?.name || 'ClinixAI insight';
  };

  function renderCard(post) {
    const title = escapeHtml(stripHtml(post.title?.rendered || 'ClinixAI article'));
    const excerpt = escapeHtml(stripHtml(post.excerpt?.rendered || '').slice(0, 150));
    const link = escapeHtml(post.link || BLOG_URL);
    const category = escapeHtml(getCategory(post));
    const image = getFeaturedImage(post);
    const dateValue = post.date ? new Date(post.date) : new Date();
    const date = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }).format(dateValue);
    const imageMarkup = image ? `<img src="${escapeHtml(image)}" alt="" loading="lazy" decoding="async">` : '';

    return `<article class="wp-card">
      ${imageMarkup}
      <div class="wp-card__body">
        <span class="wp-card__meta">${category} · ${date}</span>
        <h3>${title}</h3>
        <p>${excerpt || 'Read the latest evidence-led perspective from the ClinixAI team.'}</p>
        <a class="btn btn-link" href="${link}" target="_blank" rel="noopener noreferrer">Read article →</a>
      </div>
    </article>`;
  }

  function renderLocalCard(article) {
    const title = escapeHtml(article.title || 'ClinixAI pharmacovigilance guide');
    const topic = escapeHtml(article.topic || 'Pharmacovigilance');
    const link = `/insights/${encodeURIComponent(article.slug || '')}`;
    const kind = article.mother ? 'Complete guide' : 'Specialist guide';
    return `<article class="wp-card">
      <div class="wp-card__body">
        <span class="wp-card__meta">${topic} · ${kind}</span>
        <h3>${title}</h3>
        <p>${Number(article.words || 0).toLocaleString('en-IN')} words of scientific, operational and regulatory guidance.</p>
        <a class="btn btn-link" href="${link}">Read complete guide →</a>
      </div>
    </article>`;
  }

  const topicTone = (topic = '') => {
    const tones = ['blue', 'cyan', 'violet', 'teal', 'indigo'];
    let score = 0;
    for (const character of topic) score += character.charCodeAt(0);
    return tones[score % tones.length];
  };

  function renderClusterSlide(topic, articles, index) {
    const mother = articles.find((article) => article.mother) || articles[0];
    const children = articles.filter((article) => article !== mother).slice(0, 3);
    const tone = topicTone(topic);
    const childCards = children.map((child, childIndex) => `
      <a class="cluster-child-card cluster-tone-${tone}" href="/insights/${encodeURIComponent(child.slug || '')}">
        <div class="cluster-card-visual" aria-hidden="true"><span>0${childIndex + 1}</span><i></i><i></i><i></i></div>
        <div class="cluster-child-copy">
          <span class="cluster-card-label">SPECIALIST GUIDE · ${Number(child.words || 0).toLocaleString('en-IN')} WORDS</span>
          <h4>${escapeHtml(child.title || '')}</h4>
          <strong>Read specialist guide <b>→</b></strong>
        </div>
      </a>`).join('');
    return `<section class="cluster-slide cluster-tone-${tone}" data-cluster-slide aria-label="${escapeHtml(topic)} topic cluster" ${index ? 'hidden' : ''}>
      <a class="cluster-mother-card" href="/insights/${encodeURIComponent(mother.slug || '')}">
        <div class="cluster-mother-copy">
          <span class="cluster-card-label">MOTHER GUIDE · TOPIC CLUSTER ${String(index + 1).padStart(2, '0')}</span>
          <h3>${escapeHtml(mother.title || '')}</h3>
          <p>${Number(mother.words || 0).toLocaleString('en-IN')} words of scientific, operational and regulatory guidance.</p>
          <strong>Enter the complete guide <b>→</b></strong>
        </div>
        <div class="cluster-mother-visual" aria-hidden="true">
          <span>${String(index + 1).padStart(2, '0')}</span>
          <div><i></i><i></i><i></i><i></i><i></i></div>
          <small>${escapeHtml(topic)}</small>
        </div>
      </a>
      <div class="cluster-children">${childCards}</div>
    </section>`;
  }

  function initialiseClusterShowcase(host, articles) {
    const stage = host.querySelector('[data-cluster-stage]');
    const progress = host.querySelector('[data-cluster-progress]');
    if (!stage || !progress) return;
    const grouped = articles.reduce((result, article) => {
      (result[article.topic] ||= []).push(article);
      return result;
    }, {});
    const clusters = Object.entries(grouped).filter(([, items]) => items.length);
    stage.innerHTML = clusters.map(([topic, items], index) => renderClusterSlide(topic, items, index)).join('');
    progress.innerHTML = clusters.map(([topic], index) =>
      `<button type="button" data-cluster-dot="${index}" aria-label="Show ${escapeHtml(topic)}" aria-current="${index === 0 ? 'true' : 'false'}"><span></span></button>`
    ).join('');
    const slides = [...stage.querySelectorAll('[data-cluster-slide]')];
    const dots = [...progress.querySelectorAll('[data-cluster-dot]')];
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let active = 0;
    let timer = null;
    const interval = Math.max(2200, Number(host.dataset.interval || 2600));
    const show = (next) => {
      active = (next + slides.length) % slides.length;
      slides.forEach((slide, index) => { slide.hidden = index !== active; });
      dots.forEach((dot, index) => dot.setAttribute('aria-current', String(index === active)));
    };
    const stop = () => { if (timer) window.clearInterval(timer); timer = null; };
    const start = () => {
      stop();
      if (!reducedMotion && slides.length > 1) timer = window.setInterval(() => show(active + 1), interval);
    };
    host.querySelector('[data-cluster-prev]')?.addEventListener('click', () => { show(active - 1); start(); });
    host.querySelector('[data-cluster-next]')?.addEventListener('click', () => { show(active + 1); start(); });
    dots.forEach((dot, index) => dot.addEventListener('click', () => { show(index); start(); }));
    host.addEventListener('mouseenter', stop);
    host.addEventListener('mouseleave', start);
    host.addEventListener('focusin', stop);
    host.addEventListener('focusout', start);
    host.addEventListener('pointerdown', stop);
    host.addEventListener('pointerup', start);
    document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());
    start();
  }

  async function requestLocalArticles(limit) {
    const response = await fetch('/insights/articles.json', { headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error(`Local insight index ${response.status}`);
    const articles = await response.json();
    if (!Array.isArray(articles)) throw new Error('Invalid local insight index');
    return articles
      .sort((a, b) => Number(b.mother) - Number(a.mother) || String(a.topic).localeCompare(String(b.topic)))
      .slice(0, limit);
  }

  async function requestPosts(limit, category) {
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT);
    const query = new URLSearchParams({ type: 'posts', limit: String(limit) });
    if (category) query.set('category', category);

    try {
      const response = await fetch(`${ENDPOINT}?${query.toString()}`, {
        headers: { Accept: 'application/json' }, signal: controller.signal
      });
      if (!response.ok) throw new Error(`Content service ${response.status}`);
      const payload = await response.json();
      if (!payload.ok || !Array.isArray(payload.items)) throw new Error('Invalid content payload');
      return payload.items;
    } finally {
      window.clearTimeout(timer);
    }
  }

  async function loadFeed(host) {
    const limit = Number(host.dataset.limit || config.defaultLimit || 6);
    const category = host.dataset.category || '';
    const key = cacheKey(limit, category);
    let posts = readCache(key);

    try {
      const localArticles = await requestLocalArticles(limit);
      if (localArticles.length) {
        host.innerHTML = localArticles.map(renderLocalCard).join('');
        return;
      }
      if (!posts) {
        posts = await requestPosts(limit, category);
        saveCache(key, posts);
      }
      host.innerHTML = posts.length
        ? posts.map(renderCard).join('')
        : '<article class="wp-card"><div class="wp-card__body"><span class="wp-card__meta">PUBLICATION</span><h3>Publishing starts soon.</h3><p>New ClinixAI articles will appear here automatically.</p></div></article>';
    } catch (error) {
      console.warn('ClinixAI content feed unavailable', error);
      host.innerHTML = `<article class="wp-card"><div class="wp-card__body"><span class="wp-card__meta">CLINIXAI PUBLICATION</span><h3>The insight feed is temporarily unavailable.</h3><p>Continue to the knowledge centre for the complete article library.</p><a class="btn btn-link" href="/insights">Open Insights →</a></div></article>`;
    }
  }

  async function loadClusterShowcase(host) {
    try {
      const response = await fetch('/insights/articles.json', { headers: { Accept: 'application/json' } });
      if (!response.ok) throw new Error(`Local insight index ${response.status}`);
      const articles = await response.json();
      if (!Array.isArray(articles) || !articles.length) throw new Error('Empty insight index');
      initialiseClusterShowcase(host, articles);
    } catch (error) {
      console.warn('ClinixAI cluster showcase unavailable', error);
      const stage = host.querySelector('[data-cluster-stage]');
      if (stage) stage.innerHTML = '<article class="cluster-loading"><span>THECLINIXAI INSIGHTS</span><h3>The knowledge centre is temporarily unavailable.</h3><a href="/insights">Open all insights →</a></article>';
    }
  }

  const initialise = () => {
    document.querySelectorAll('[data-wp-posts]').forEach(loadFeed);
    document.querySelectorAll('[data-cluster-showcase]').forEach(loadClusterShowcase);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialise, { once: true });
  else initialise();
})();
