# Scripts

Utility scripts used to build and maintain the site. Run from the repo root
(e.g. `python scripts/seo-foundation.py`), not from inside this folder.

## Ongoing maintenance

Safe to re-run any time; these keep metadata and search-engine signals in sync.

- `seo-foundation.py` — applies repeatable static SEO metadata (titles, descriptions, robots tags) across non-article pages.
- `indexnow-submit.py` — verifies the deployed IndexNow key and submits sitemap URLs to IndexNow-participating search engines.
- `search-engine-audit.py` — checks static search-engine readiness (titles, canonicals, robots, sitemap coverage) and writes a report.
- `qa-site.py` — basic pre-deploy QA pass over the built pages.
- `conversion-audit.py` — checks CTA and analytics-event coverage across pages.
- `build-internal-links.py` — builds bidirectional links between the `/insights` articles and their related commercial/service pages.

## One-off content builders

Used to generate a batch of pages during a specific content push. Re-run only
if you're regenerating that batch from source data — otherwise leave alone,
since re-running could overwrite manual edits made directly to the HTML.

- `build-commercial-pages.py` / `build-commercial-pages-sprint3.py` — generated the `/services/*` and related commercial pages.
- `build-hospital-pages.py` — generated the hospital-audience landing pages.
- `build-entity-pages.py` — generated company/entity pages (leadership, press kit, fact sheet, etc.).
- `build-earned-authority.py` — generated the research/whitepaper pages.
- `import-docx-articles.py` — imports `/insights` articles from source `.docx` files.

## One-time setup (already applied, kept for reference)

- `apply-consent-banner.py` — added the cookie-consent banner across all pages.
- `apply-ga4.py` — set the GA4 measurement ID in the analytics loader.
- `apply-search-verification.py` — applied Google/Bing search-console verification tags to the homepage.
