(() => {
  const MAX_RESUME_BYTES = 3 * 1024 * 1024;
  const allowedTypes = new Set([
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ]);

  const readFile = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error('RESUME_READ_FAILED'));
    reader.onload = () => resolve(String(reader.result).split(',')[1]);
    reader.readAsDataURL(file);
  });

  document.querySelectorAll('[data-programme-select], [data-application-select]').forEach(button => {
    button.addEventListener('click', () => {
      const route = button.dataset.applicationRoute || 'academy';
      const form = document.querySelector(`[data-application-form][data-route="${route}"]`);
      const select = form?.querySelector('[name="internshipType"]');
      if (!form || !select) return;
      select.value = button.dataset.programmeSelect || button.dataset.applicationSelect || '';
      form.closest('.application-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      window.setTimeout(() => select.focus({ preventScroll: true }), 450);
    });
  });

  document.querySelectorAll('[data-application-form]').forEach(form => {
    const status = form.querySelector('[data-application-status]');
    const submit = form.querySelector('[type="submit"]');
    const startedAt = form.querySelector('[name="formStartedAt"]');
    if (startedAt) startedAt.value = String(Date.now());

    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const resume = form.querySelector('[name="resume"]')?.files?.[0];
      if (!resume) return;
      if (resume.size > MAX_RESUME_BYTES || !allowedTypes.has(resume.type)) {
        status.textContent = 'Please upload a PDF, DOC or DOCX resume no larger than 3 MB.';
        status.dataset.state = 'error';
        return;
      }

      submit.disabled = true;
      form.setAttribute('aria-busy', 'true');
      status.textContent = 'Submitting your application securely…';
      status.dataset.state = 'progress';

      try {
        const data = Object.fromEntries(new FormData(form).entries());
        data.route = form.dataset.route || 'academy';
        data.resume = { name: resume.name, type: resume.type, content: await readFile(resume) };
        const response = await fetch('/api/application', {
          method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data)
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok || !result.ok) throw new Error(result.error || 'SUBMISSION_FAILED');
        form.reset();
        if (startedAt) startedAt.value = String(Date.now());
        status.textContent = 'Application received. TheClinixAI team will review it and respond by email.';
        status.dataset.state = 'success';
      } catch (error) {
        status.textContent = 'The application could not be submitted. Please try again shortly.';
        status.dataset.state = 'error';
      } finally {
        submit.disabled = false;
        form.removeAttribute('aria-busy');
      }
    });
  });
})();
