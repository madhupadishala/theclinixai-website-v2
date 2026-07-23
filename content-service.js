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

  const initialise = () => document.querySelectorAll('[data-wp-posts]').forEach(loadFeed);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialise, { once: true });
  else initialise();
})();
