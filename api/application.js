const RESEND_ENDPOINT = 'https://api.resend.com/emails';
const MAX_BODY_BYTES = 4_500_000;
const MIN_FORM_AGE_MS = 1_500;
const MAX_FORM_AGE_MS = 24 * 60 * 60 * 1_000;
const ALLOWED_RESUME_TYPES = new Set(['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']);

const clean = (value, max) => typeof value === 'string' ? value.replace(/\u0000/g, '').trim().slice(0, max) : '';
const escape = value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
function fail(code, statusCode = 400) { const error = new Error(code); error.statusCode = statusCode; throw error; }
function parse(request) { let body = request.body; if (typeof body === 'string') { if (Buffer.byteLength(body, 'utf8') > MAX_BODY_BYTES) fail('PAYLOAD_TOO_LARGE', 413); try { body = JSON.parse(body); } catch { fail('INVALID_JSON'); } } if (!body || typeof body !== 'object' || Array.isArray(body)) fail('INVALID_BODY'); if (Buffer.byteLength(JSON.stringify(body), 'utf8') > MAX_BODY_BYTES) fail('PAYLOAD_TOO_LARGE', 413); return body; }
function validateResume(body) { const resume = body.resume; if (!resume || typeof resume !== 'object') fail('MISSING_RESUME'); const name = clean(resume.name, 160).replace(/[^A-Za-z0-9._ -]/g, '_'); const type = clean(resume.type, 120); const content = clean(resume.content, 4_200_000); if (!name || !content || !ALLOWED_RESUME_TYPES.has(type) || !/\.(pdf|doc|docx)$/i.test(name)) fail('INVALID_RESUME'); return { name, type, content }; }
function normalise(body) {
  const route = clean(body.route, 20);
  if (!['academy', 'careers'].includes(route)) fail('INVALID_ROUTE');
  if (route === 'careers') {
    const application = { route, role: clean(body.role, 120), firstName: clean(body.firstName, 60), secondName: clean(body.secondName, 60), mobileNumber: clean(body.mobileNumber, 40), experience: clean(body.experience, 60), currentOrganization: clean(body.currentOrganization, 120), noticePeriod: clean(body.noticePeriod, 60), resume: validateResume(body) };
    if (!application.role || !application.firstName || !application.secondName || !application.mobileNumber) fail('MISSING_REQUIRED_FIELDS');
    if (!/^[0-9+().\-\s]{6,40}$/.test(application.mobileNumber)) fail('INVALID_MOBILE_NUMBER');
    return application;
  }
  const application = { firstName: clean(body.firstName, 60), lastName: clean(body.lastName, 60), whatsapp: clean(body.whatsapp, 40), email: clean(body.email, 254), experience: clean(body.experience, 60), internshipType: clean(body.internshipType, 90), route, resume: validateResume(body) };
  if (!application.firstName || !application.lastName || !application.whatsapp || !application.email || !application.experience || !application.internshipType) fail('MISSING_REQUIRED_FIELDS');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(application.email)) fail('INVALID_EMAIL');
  if (!/^[0-9+().\-\s]{6,40}$/.test(application.whatsapp)) fail('INVALID_WHATSAPP');
  return application;
}
function allowedOrigin(request) { const origin = request.headers?.origin; if (!origin) return true; try { const hostname = new URL(origin).hostname.toLowerCase(); return hostname === 'theclinixai.com' || hostname === 'www.theclinixai.com' || (process.env.VERCEL_ENV !== 'production' && hostname.endsWith('.vercel.app')); } catch { return false; } }
module.exports = async function handler(request, response) {
  response.setHeader('Cache-Control', 'no-store, max-age=0'); response.setHeader('X-Content-Type-Options', 'nosniff');
  if (request.method !== 'POST') { response.setHeader('Allow', 'POST'); return response.status(405).json({ ok: false, error: 'METHOD_NOT_ALLOWED' }); }
  if (!allowedOrigin(request)) return response.status(403).json({ ok: false, error: 'ORIGIN_NOT_ALLOWED' });
  const requestId = globalThis.crypto?.randomUUID?.() || `application-${Date.now()}`;
  try {
    const body = parse(request); if (clean(body.website, 160)) return response.status(200).json({ ok: true });
    const formAge = Date.now() - Number(body.formStartedAt); if (!Number.isFinite(formAge) || formAge < MIN_FORM_AGE_MS || formAge > MAX_FORM_AGE_MS) fail('INVALID_FORM_SESSION');
    const application = normalise(body); const apiKey = process.env.RESEND_API_KEY; const from = process.env.CONTACT_FROM_EMAIL; const to = application.route === 'careers' ? (process.env.CAREERS_TO_EMAIL || 'careers@theclinixai.com') : (process.env.ACADEMY_TO_EMAIL || 'academy@theclinixai.com');
    if (!apiKey || !from) { console.error('APPLICATION_DELIVERY', JSON.stringify({ requestId, status: 'configuration_error' })); return response.status(503).json({ ok: false, error: 'DELIVERY_UNAVAILABLE' }); }
    const fullName = application.route === 'careers' ? `${application.firstName} ${application.secondName}` : `${application.firstName} ${application.lastName}`;
    const title = application.route === 'careers' ? `Career application — ${application.role}` : 'Academy application';
    const fields = application.route === 'careers' ? [['Role', application.role], ['First name', application.firstName], ['Second name', application.secondName], ['Mobile number', application.mobileNumber], ['Experience', application.experience || 'Not provided'], ['Current organization', application.currentOrganization || 'Not provided'], ['Notice period', application.noticePeriod || 'Not provided'], ['Request ID', requestId]] : [['Name', fullName], ['WhatsApp', application.whatsapp], ['Email', application.email], ['Experience', application.experience], ['Internship type', application.internshipType], ['Route', application.route], ['Request ID', requestId]];
    const table = fields.map(([label, value]) => `<tr><th style="padding:8px;text-align:left;background:#f3f6fb;border:1px solid #dbe3ef">${escape(label)}</th><td style="padding:8px;border:1px solid #dbe3ef">${escape(value)}</td></tr>`).join('');
    const text = `${title}\n\n${fields.map(([label, value]) => `${label}: ${value}`).join('\n')}\n\nResume: ${application.resume.name}`;
    const payload = { from, to: [to], subject: `[TheClinixAI] ${title} — ${fullName}`, text, html: `<div style="font-family:Arial,sans-serif;color:#0f172a"><h1 style="font-size:22px">${escape(title)}</h1><table style="border-collapse:collapse;width:100%;max-width:700px">${table}</table></div>`, attachments: [{ filename: application.resume.name, content: application.resume.content, content_type: application.resume.type }], headers: { 'X-Entity-Ref-ID': requestId } };
    if (application.route === 'academy' && application.email) payload.reply_to = application.email;
    const provider = await fetch(RESEND_ENDPOINT, { method: 'POST', headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (!provider.ok) { console.error('APPLICATION_DELIVERY', JSON.stringify({ requestId, status: 'provider_error', providerStatus: provider.status })); return response.status(502).json({ ok: false, error: 'DELIVERY_FAILED' }); }
    console.info('APPLICATION_DELIVERY', JSON.stringify({ requestId, status: 'delivered', route: application.route })); return response.status(200).json({ ok: true, requestId });
  } catch (error) { const status = Number(error?.statusCode) || 500; const publicError = status >= 500 ? 'DELIVERY_UNAVAILABLE' : error.message; console.error('APPLICATION_DELIVERY', JSON.stringify({ requestId, status: 'request_error', error: publicError })); return response.status(status).json({ ok: false, error: publicError }); }
};