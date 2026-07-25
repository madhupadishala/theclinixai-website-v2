(() => {
  'use strict';

  const form = document.querySelector('[data-contact-form]');
  if (!form) return;

  const submit = form.querySelector('[type="submit"]');
  const status = form.querySelector('[data-contact-status]');
  const startedAt = form.querySelector('[name="formStartedAt"]');
  if (startedAt) startedAt.value = String(Date.now());

  const setStatus = (message, state) => {
    if (!status) return;
    status.textContent = message;
    status.dataset.state = state;
    status.hidden = false;
  };

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    submit.disabled = true;
    submit.dataset.originalLabel ||= submit.textContent;
    submit.textContent = 'Sending securely…';
    form.setAttribute('aria-busy', 'true');
    setStatus('Delivering your enquiry to the TheClinixAI team…', 'progress');

    try {
      const payload = Object.fromEntries(new FormData(form).entries());
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json'
        },
        body: JSON.stringify(payload)
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok || !result.ok) throw new Error(result.error || 'DELIVERY_FAILED');

      setStatus(result.message || 'Thank you. Your enquiry has been delivered.', 'success');
      window.dispatchEvent(new CustomEvent('clinixai:leadconfirmed', {
        detail: { form_id: 'contact', delivery: 'confirmed' }
      }));
      form.reset();
      if (startedAt) startedAt.value = String(Date.now());
      submit.textContent = 'Enquiry delivered';
    } catch {
      setStatus('We could not deliver your enquiry right now. Please try again or email support@theclinixai.com.', 'error');
      submit.textContent = submit.dataset.originalLabel;
    } finally {
      submit.disabled = false;
      form.removeAttribute('aria-busy');
    }
  });
})();
