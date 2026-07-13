# ClinixAI Locked About + Resources Build

## Included
- Complete About page with Purpose, Vision, Mission and six editorial profiles.
- ClinixAI Research Hub with three hard-coded online research papers.
- Distinct 3D Insights, WordPress Blogs and Media Coverage sections.
- Original PDFs stored in `assets/research/` for gated delivery.

## Founder photos
Add approved WebP portraits to `assets/founders/` using: `wany.webp`, `surya.webp`, `althaf.webp`, `harsha.webp`, `adithya.webp`, `madhu.webp`. Recommended source: 600x750, WebP, under 120 KB.

## WordPress
Set `blogUrl` in `content-config.js`. Current value: `https://blogs.theclinixai.com`.

## PDF delivery
Connect `/api/whitepaper-request` to your email/CRM workflow. Public online reading remains available; PDF requests capture name, work email and mobile number.

## Local test
`python -m http.server 8085` then open `http://localhost:8085`.
