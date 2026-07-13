const BLOG_API = 'https://blogs.theclinixai.com/wp-json/wp/v2';
const ALLOWED_TYPES = new Set(['posts', 'categories']);

function safeInteger(value, fallback, min, max) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed)) return fallback;
  return Math.min(max, Math.max(min, parsed));
}

module.exports = async function handler(request, response) {
  const type = ALLOWED_TYPES.has(request.query.type) ? request.query.type : 'posts';
  const limit = safeInteger(request.query.limit, 6, 1, 12);
  const page = safeInteger(request.query.page, 1, 1, 100);
  const category = safeInteger(request.query.category, 0, 0, 999999);

  const params = new URLSearchParams({ per_page: String(limit), page: String(page) });
  if (type === 'posts') {
    params.set('_fields', 'id,date,modified,link,slug,title,excerpt,_embedded');
    params.set('_embed', 'wp:featuredmedia,author,wp:term');
    if (category) params.set('categories', String(category));
  } else {
    params.set('_fields', 'id,count,name,slug,link');
    params.set('hide_empty', 'true');
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 7000);

  try {
    const upstream = await fetch(`${BLOG_API}/${type}?${params.toString()}`, {
      headers: { Accept: 'application/json', 'User-Agent': 'TheClinixAI-Website/2.0' },
      signal: controller.signal
    });
    clearTimeout(timer);

    if (!upstream.ok) {
      return response.status(502).json({ ok: false, error: 'CONTENT_UPSTREAM_UNAVAILABLE' });
    }

    const payload = await upstream.json();
    response.setHeader('Cache-Control', 's-maxage=900, stale-while-revalidate=86400');
    response.setHeader('Content-Type', 'application/json; charset=utf-8');
    return response.status(200).json({
      ok: true,
      type,
      page,
      total: Number(upstream.headers.get('x-wp-total') || payload.length),
      totalPages: Number(upstream.headers.get('x-wp-totalpages') || 1),
      items: payload
    });
  } catch (error) {
    clearTimeout(timer);
    return response.status(503).json({ ok: false, error: 'CONTENT_SERVICE_TIMEOUT' });
  }
};
