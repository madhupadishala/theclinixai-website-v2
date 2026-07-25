const assert = require('node:assert/strict');
const handler = require('../api/contact.js');

function responseMock() {
  return {
    statusCode: 200,
    headers: {},
    payload: undefined,
    setHeader(name, value) { this.headers[name] = value; },
    status(code) { this.statusCode = code; return this; },
    json(payload) { this.payload = payload; return this; },
    end() { return this; }
  };
}

function validBody(overrides = {}) {
  return {
    fullName: 'Test Lead',
    company: 'Test Pharma',
    designation: 'PV Lead',
    email: 'lead@example.com',
    phone: '+91 9000000000',
    country: 'India',
    business: 'Pharmaceutical Manufacturer',
    interest: 'Literature Intelligence',
    teamSize: '11–50',
    source: 'Google Search',
    message: 'We need to assess a governed literature monitoring workflow.',
    website: '',
    formStartedAt: Date.now() - 4_000,
    ...overrides
  };
}

async function run() {
  const originalFetch = global.fetch;
  const originalInfo = console.info;
  const originalError = console.error;
  const capturedLogs = [];
  console.info = (...args) => capturedLogs.push(args.join(' '));
  console.error = (...args) => capturedLogs.push(args.join(' '));
  process.env.RESEND_API_KEY = 're_test_key';
  process.env.CONTACT_FROM_EMAIL = 'TheClinixAI Website <website@notifications.theclinixai.com>';
  process.env.CONTACT_TO_EMAIL = 'support@theclinixai.com';
  process.env.VERCEL_ENV = 'production';

  try {
    {
      const response = responseMock();
      await handler({ method: 'GET', headers: {} }, response);
      assert.equal(response.statusCode, 405);
    }

    {
      let called = false;
      global.fetch = async () => { called = true; throw new Error('should not send'); };
      const response = responseMock();
      await handler({
        method: 'POST',
        headers: { origin: 'https://www.theclinixai.com' },
        body: validBody({ website: 'spam.example' })
      }, response);
      assert.equal(response.statusCode, 200);
      assert.equal(called, false);
    }

    {
      let providerRequest;
      global.fetch = async (url, options) => {
        providerRequest = { url, options };
        return {
          ok: true,
          status: 200,
          json: async () => ({ id: 'email_test_123' })
        };
      };
      const response = responseMock();
      await handler({
        method: 'POST',
        headers: { origin: 'https://www.theclinixai.com' },
        body: validBody()
      }, response);
      assert.equal(response.statusCode, 200);
      assert.equal(response.payload.ok, true);
      assert.equal(providerRequest.url, 'https://api.resend.com/emails');
      const email = JSON.parse(providerRequest.options.body);
      assert.deepEqual(email.to, ['support@theclinixai.com']);
      assert.equal(email.reply_to, 'lead@example.com');
      assert.match(email.subject, /Literature Intelligence/);
    }

    {
      global.fetch = async () => ({ ok: false, status: 422, json: async () => ({}) });
      const response = responseMock();
      await handler({
        method: 'POST',
        headers: { origin: 'https://www.theclinixai.com' },
        body: validBody()
      }, response);
      assert.equal(response.statusCode, 502);
      assert.equal(response.payload.ok, false);
    }

    {
      const response = responseMock();
      await handler({
        method: 'POST',
        headers: { origin: 'https://attacker.example' },
        body: validBody()
      }, response);
      assert.equal(response.statusCode, 403);
    }

    const joinedLogs = capturedLogs.join('\n');
    for (const pii of [
      'Test Lead',
      'Test Pharma',
      'lead@example.com',
      '+91 9000000000',
      'governed literature monitoring workflow'
    ]) {
      assert.equal(joinedLogs.includes(pii), false, `PII leaked into logs: ${pii}`);
    }
    console.log('Contact handler tests: PASS');
  } finally {
    global.fetch = originalFetch;
    console.info = originalInfo;
    console.error = originalError;
  }
}

run().catch(error => {
  console.error(error);
  process.exit(1);
});
