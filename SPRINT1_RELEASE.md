# TheClinixAI Sprint 1 — Production Trust and Search Discovery

This release closes the four production gaps identified on 25 July 2026.

## Included

- Resend-backed enquiry delivery to `CONTACT_TO_EMAIL`
- PII-safe application logs
- contact-form loading, success and failure states
- GA4 `generate_lead` only after confirmed provider delivery
- permanent redirects from both legacy Academy URLs
- deployed IndexNow root key and verified-submit workflow
- contact-handler tests and expanded site QA

## Required Vercel variables

- `RESEND_API_KEY`
- `CONTACT_FROM_EMAIL`
- `CONTACT_TO_EMAIL`

Configure them for Production and Preview, then redeploy.

## Validate locally

```powershell
node .\scripts\test-contact-handler.js
python .\scripts\qa-site.py
python .\scripts\conversion-audit.py
python .\scripts\indexnow-submit.py --dry-run
```

## Activate after deployment

After Vercel reports the production deployment as Ready:

```powershell
python .\scripts\indexnow-submit.py
```

An IndexNow HTTP `200` means submitted successfully. HTTP `202` means accepted with key validation pending.

## Production acceptance

1. Submit one real enquiry through `/contact`.
2. Confirm it arrives at the configured inbox.
3. Confirm the browser shows the success state rather than raw JSON.
4. Confirm Vercel logs contain request IDs/statuses but no enquiry contents.
5. Confirm both legacy Academy URLs permanently redirect to `/pharmacovigilance-internship-programme`.
6. Confirm GA4 Realtime receives `generate_lead` only for the delivered enquiry.
