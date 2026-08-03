# TheClinixAI Website

Public marketing site for TheClinixAI (theclinixai.com) — pharmacovigilance
platform, services, academy and research content. Static HTML/CSS/JS,
deployed on Vercel.

## Stack

- Static HTML pages with a shared `header.html` / `footer.html` loaded via `fetch()`
- `style.css` for global styles, `site.js` for shared behaviour
- Vercel serverless functions in `api/` for the contact form, application form,
  whitepaper requests and analytics event logging
- Content for `/insights`, `/resources` and the blogs feed served from
  `data/*.json`
- `sitemap_generator.py` regenerates `sitemap.xml` from the live HTML files
  (see below)

## Running locally

```bash
python -m http.server 8081
```

Then open `http://localhost:8081`. Don't open the HTML files directly by
double-clicking — the shared header/footer are loaded via `fetch()`, which
needs an actual server.

## Deploying

Push to `main`. Vercel auto-deploys from this branch. Redirects, headers and
clean-URL routing are configured in `vercel.json`.

## Sitemap

Run `python sitemap_generator.py` after adding, removing, or renaming pages.
It walks every `.html` file, builds the corresponding clean URL, and skips
any page whose own `<link rel="canonical">` points somewhere else (i.e. a
page that's marked as a duplicate of another URL won't be submitted to
Google as if it were separate). Commit the regenerated `sitemap.xml`.

## Project structure

```
/               top-level pages (about, contact, services, etc.)
/services/      individual PV service pages
/insights/      pharmacovigilance guides and articles
/api/           Vercel serverless functions
/data/          JSON content for insights, blogs, press, whitepapers
/scripts/       build and maintenance scripts — see scripts/README.md
/assets/        images and media
```

## Notes

- `63c00e...b7b2.txt` at the repo root is a search-console domain
  verification file — required, don't delete it.
- `llms.txt` describes the site for AI crawlers, separate from `robots.txt`.
