# TheClinixAI visibility closeout

This release makes `/resources` the only knowledge-library index.

- `/insights` and `/insights/index.html` permanently redirect to `/resources`.
- The 40 individual article URLs under `/insights/<article-slug>` remain live and unchanged.
- The Resources menu contains **White Papers**, **Insights**, and **Blogs**.
- The sitemap no longer advertises the retired `/insights` index.
- Existing Academy, Careers, enquiry delivery, consent-aware GA4, and IndexNow work already present on `main` is preserved.
- The supplied logo has been cleaned into a true 4096-pixel transparent master, with optimised header/footer wordmarks and square favicon/app-icon assets.

## Release sequence

Extract this release at the repository root and replace matching files. Then run:

```powershell
python .\scripts\qa-site.py
git add header.html footer.html resources.html style.css content-service.js site.js vercel.json sitemap.xml scripts\seo-foundation.py scripts\build-sitemap.py scripts\search-engine-audit.py scripts\qa-site.py assets\brand favicon.ico icon-32.png icon-192.png icon-512.png apple-touch-icon.png FINAL_CLOSEOUT.md
git commit -m "Consolidate Resources and complete visibility closeout"
git pull --rebase origin main
git push origin main
```

After Vercel shows **Ready**, run IndexNow once:

```powershell
python .\scripts\indexnow-submit.py
```

Google Search Console already has the sitemap. It will discover this canonical change through the sitemap and permanent redirects; there is no need to request every article manually again.

The deployment completes the website-side foundation. Search engines still need time to recrawl, while legitimate external mentions and backlinks remain third-party editorial signals rather than code changes.
