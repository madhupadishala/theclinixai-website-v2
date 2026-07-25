const RESEND_ENDPOINT = 'https://api.resend.com/emails';
const MAX_BODY_BYTES = 20_000;
const MIN_FORM_AGE_MS = 1_500;
const MAX_FORM_AGE_MS = 24 * 60 * 60 * 1_000;

const FIELD_RULES = {
  fullName: { required: true, max: 120 },
  company: { required: false, max: 160 },
  designation: { required: false, max: 120 },
  email: { required: true, max: 254 },
  phone: { required: true, max: 40 },
  country: { required: false, max: 100 },
  business: { required: true, max: 120 },
  interest: { required: true, max: 120 },
  teamSize: { required: false, max: 40 },
  source: { required: false, max: 80 },
  message: { required: true, max: 2_500 },
  utm_source: { required: false, max: 160 },
  utm_medium: { required: false, max: 160 },
  utm_campaign: { required: false, max: 160 },
  utm_content: { required: false, max: 160 },
  utm_term: { required: false, max: 160 }
};

function text(value, max) {
  return typeof value === 'string'
    ? value.replace(/\u0000/g, '').trim().slice(0, max)
    : '';
}

function html(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
    .replace(/\r?\n/g, '<br>');
}

function parseBody(request) {
  let body = request.body;
  if (typeof body === 'string') {
    if (Buffer.byteLength(body, 'utf8') > MAX_BODY_BYTES) {
      const error = new Error('PAYLOAD_TOO_LARGE');
      error.statusCode = 413;
      throw error;
    }
    try {
      body = JSON.parse(body);
    } catch {
      const error = new Error('INVALID_JSON');
      error.statusCode = 400;
      throw error;
    }
  }
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    const error = new Error('INVALID_BODY');
    error.statusCode = 400;
    throw error;
  }
  if (Buffer.byteLength(JSON.stringify(body), 'utf8') > MAX_BODY_BYTES) {
    const error = new Error('PAYLOAD_TOO_LARGE');
    error.statusCode = 413;
    throw error;
  }
  return body;
}

function normalize(body) {
  const enquiry = {};
  for (const [name, rule] of Object.entries(FIELD_RULES)) {
    enquiry[name] = text(body[name], rule.max);
    if (rule.required && !enquiry[name]) {
      const error = new Error('MISSING_REQUIRED_FIELDS');
      error.statusCode = 400;
      throw error;
    }
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(enquiry.email)) {
    const error = new Error('INVALID_EMAIL');
    error.statusCode = 400;
    throw error;
  }
  if (!/^[0-9+().\-\s]{6,40}$/.test(enquiry.phone)) {
    const error = new Error('INVALID_PHONE');
    error.statusCode = 400;
    throw error;
  }
  return enquiry;
}

function row(label, value) {
  if (!value) return '';
  return `<tr><th style="padding:8px 12px;text-align:left;vertical-align:top;background:#f3f6fb;border:1px solid #dbe3ef">${html(label)}</th><td style="padding:8px 12px;border:1px solid #dbe3ef">${html(value)}</td></tr>`;
}

function buildEmail(enquiry, requestId) {
  const subject = `[TheClinixAI enquiry] ${enquiry.interest} — ${enquiry.fullName}`;
  const table = [
    row('Full name', enquiry.fullName),
    row('Company', enquiry.company),
    row('Designation', enquiry.designation),
    row('Business email', enquiry.email),
    row('Contact number', enquiry.phone),
    row('Country', enquiry.country),
    row('Operating business', enquiry.business),
    row('Area of interest', enquiry.interest),
    row('Team size', enquiry.teamSize),
    row('Source', enquiry.source),
    row('Requirement or query', enquiry.message),
    row('Campaign', enquiry.utm_campaign),
    row('UTM source', enquiry.utm_source),
    row('UTM medium', enquiry.utm_medium),
    row('Request ID', requestId)
  ].join('');
  const lines = [
    `New TheClinixAI website enquiry`,
    ``,
    `Full name: ${enquiry.fullName}`,
    `Company: ${enquiry.company || '—'}`,
    `Designation: ${enquiry.designation || '—'}`,
    `Business email: ${enquiry.email}`,
    `Contact number: ${enquiry.phone}`,
    `Country: ${enquiry.country || '—'}`,
    `Operating business: ${enquiry.business}`,
    `Area of interest: ${enquiry.interest}`,
    `Team size: ${enquiry.teamSize || '—'}`,
    `Source: ${enquiry.source || '—'}`,
    ``,
    `Requirement or query:`,
    enquiry.message,
    ``,
    `Request ID: ${requestId}`
  ];
  return {
    subject,
    text: lines.join('\n'),
    html: `<div style="font-family:Arial,sans-serif;color:#0f172a;line-height:1.5"><h1 style="font-size:22px">New website enquiry</h1><table style="border-collapse:collapse;width:100%;max-width:760px">${table}</table><p style="color:#64748b;font-size:12px">Sent securely by the TheClinixAI production contact handler.</p></div>`
  };
}

function allowedOrigin(request) {
  const origin = request.headers?.origin;
  if (!origin) return true;
  try {
    const hostname = new URL(origin).hostname.toLowerCase();
    if (hostname === 'theclinixai.com' || hostname === 'www.theclinixai.com') return true;
    return process.env.VERCEL_ENV !== 'production' && hostname.endsWith('.vercel.app');
  } catch {
    return false;
  }
}

module.exports = async function handler(request, response) {
  response.setHeader('Cache-Control', 'no-store, max-age=0');
  response.setHeader('X-Content-Type-Options', 'nosniff');

  if (request.method !== 'POST') {
    response.setHeader('Allow', 'POST');
    return response.status(405).json({ ok: false, error: 'METHOD_NOT_ALLOWED' });
  }
  if (!allowedOrigin(request)) {
    return response.status(403).json({ ok: false, error: 'ORIGIN_NOT_ALLOWED' });
  }

  const requestId = globalThis.crypto?.randomUUID?.() || `lead-${Date.now()}`;

  try {
    const body = parseBody(request);

    // Honeypot: acknowledge silently so automated senders receive no useful signal.
    if (text(body.website, 160)) {
      console.info('CONTACT_DELIVERY', JSON.stringify({ requestId, status: 'honeypot_rejected' }));
      return response.status(200).json({ ok: true, message: 'Enquiry received.' });
    }

    const startedAt = Number(body.formStartedAt);
    const formAge = Date.now() - startedAt;
    if (!Number.isFinite(startedAt) || formAge < MIN_FORM_AGE_MS || formAge > MAX_FORM_AGE_MS) {
      return response.status(400).json({ ok: false, error: 'INVALID_FORM_SESSION' });
    }

    const enquiry = normalize(body);
    const apiKey = process.env.RESEND_API_KEY;
    const from = process.env.CONTACT_FROM_EMAIL;
    const to = process.env.CONTACT_TO_EMAIL;
    if (!apiKey || !from || !to) {
      console.error('CONTACT_DELIVERY', JSON.stringify({ requestId, status: 'configuration_error' }));
      return response.status(503).json({ ok: false, error: 'DELIVERY_UNAVAILABLE' });
    }

    const content = buildEmail(enquiry, requestId);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10_000);
    let resendResponse;
    try {
      resendResponse = await fetch(RESEND_ENDPOINT, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from,
          to: [to],
          reply_to: enquiry.email,
          subject: content.subject,
          text: content.text,
          html: content.html,
          headers: { 'X-Entity-Ref-ID': requestId }
        }),
        signal: controller.signal
      });
    } finally {
      clearTimeout(timeout);
    }

    if (!resendResponse.ok) {
      console.error('CONTACT_DELIVERY', JSON.stringify({
        requestId,
        status: 'provider_error',
        providerStatus: resendResponse.status
      }));
      return response.status(502).json({ ok: false, error: 'DELIVERY_FAILED' });
    }

    const result = await resendResponse.json().catch(() => ({}));
    console.info('CONTACT_DELIVERY', JSON.stringify({
      requestId,
      status: 'delivered',
      providerMessageId: text(result.id, 100)
    }));
    return response.status(200).json({
      ok: true,
      message: 'Thank you. Your enquiry has been delivered to the TheClinixAI team.',
      requestId
    });
  } catch (error) {
    const statusCode = Number(error?.statusCode) || (error?.name === 'AbortError' ? 504 : 500);
    const publicError = statusCode >= 500 ? 'DELIVERY_UNAVAILABLE' : error.message;
    console.error('CONTACT_DELIVERY', JSON.stringify({
      requestId,
      status: 'request_error',
      error: publicError
    }));
    return response.status(statusCode).json({ ok: false, error: publicError });
  }
};
