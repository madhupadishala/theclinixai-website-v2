# Search-engine activation

The technical files are ready. Verification and submission require the site owner's authenticated accounts.

## Google Search Console

1. Add the domain property `theclinixai.com`.
2. Complete DNS verification, or copy the HTML verification token.
3. If using HTML-token verification, run:

   `python scripts/apply-search-verification.py --google "TOKEN" --bing "TOKEN"`

4. Commit and deploy the updated `index.html`.
5. Submit `https://www.theclinixai.com/sitemap.xml`.
6. Inspect the homepage, `/insights`, `/resources`, the 12 commercial pages and representative scientific articles.
7. Request indexing only for priority pages; let the sitemap support discovery of the full set.

## Bing Webmaster Tools

1. Import the verified Google Search Console property or create a Bing property.
2. Submit the same XML sitemap.
3. Use `scripts/indexnow-submit.py` after generating an IndexNow key:

   `python scripts/indexnow-submit.py --key "YOUR_SECURE_KEY" --dry-run`

4. Deploy the generated key text file.
5. Run the command again without `--dry-run`.

## Measurement cadence

- Week 1: coverage, crawl errors and canonical selection.
- Weeks 2–4: impressions, query relevance and branded visibility.
- Days 30–60: pages ranking in positions 11–30; improve internal links and titles.
- Days 60–90: CTR and conversion optimisation based on actual queries.

Do not change titles repeatedly during early discovery. Record every material SEO change and compare equivalent time windows.
