const ALLOWED_EVENTS = new Set([
  'page_view',
  'cta_click',
  'form_start',
  'form_submit',
  'generate_lead',
  'resource_download',
  'outbound_click',
  'scroll_depth'
]);

function safeText(value, max = 180) {
  return typeof value === 'string' ? value.slice(0, max) : '';
}

module.exports = async function handler(request, response) {
  if (request.method !== 'POST') return response.status(405).json({ error: 'METHOD_NOT_ALLOWED' });
  let body = request.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { return response.status(400).json({ error: 'INVALID_JSON' }); }
  }
  if (!body || !ALLOWED_EVENTS.has(body.event)) return response.status(400).json({ error: 'INVALID_EVENT' });
  const record = {
    event: body.event,
    path: safeText(body.path, 220),
    page_title: safeText(body.page_title),
    session_id: safeText(body.session_id, 80),
    timestamp: safeText(body.timestamp, 40),
    label: safeText(body.label, 120),
    destination: safeText(body.destination, 240),
    destination_host: safeText(body.destination_host, 160),
    form_action: safeText(body.form_action, 180),
    form_id: safeText(body.form_id, 80),
    delivery: safeText(body.delivery, 40),
    percent: Number.isFinite(Number(body.percent)) ? Number(body.percent) : undefined,
    attribution: body.attribution && typeof body.attribution === 'object' ? body.attribution : {}
  };
  console.log('CLINIXAI_ANALYTICS', JSON.stringify(record));
  response.setHeader('Cache-Control', 'no-store');
  return response.status(204).end();
};
