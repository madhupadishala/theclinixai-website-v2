# Repo cleanup — what changed and how to apply it

I don't have push access to your GitHub, so this is packaged as a patch file
(`repo-cleanup.patch`) for you to review and apply yourself. 40 files
changed, net -1,946 lines.

## How to apply

```bash
cd theclinixai-website-v2          # your local clone
git checkout main
git pull
git apply --check repo-cleanup.patch   # dry run, should print nothing if clean
git am repo-cleanup.patch              # applies it as a real commit
git push
```

If `git apply --check` complains about conflicts, it means something changed
in the repo since I cloned it — tell me and I'll regenerate the patch against
the current `main`.

## What changed

### 1. Deleted 19 files that made the repo look bot-maintained
These were internal working notes / one-off automation logs, not real
documentation or site content — the kind of thing that gives it away as
AI/agency-generated rather than a person's ongoing project:

`CONVERSION_ANALYTICS_ACTIVATION.md`, `FINAL_CLOSEOUT.md`,
`FINAL_RELEASE_NOTES.md`, `PRESS_BACKLINK_ACTIVATION.md`, `QA_FINAL.txt`,
`QA_FINAL_UPDATED.txt`, `QA_MERGE_OUTPUT.txt`, `QA_MERGE_REPORT.txt`,
`SEARCH_ENGINE_ACTIVATION.md`, `SPRINT1_RELEASE.md`, `STAGE_1_NOTES.md`,
`search-engine-readiness-report.json`, `conversion-analytics-report.json`,
`html_audit.py`, `fix_links.py`, `master_spec_execute.py`,
`README_FINAL.md`, `README_LOCKED_PAGES.md`, `README_UPDATED_PACKAGE.md`

None of these are referenced by the live site or the build. Safe to delete.

### 2. One README instead of four
`README.md` is now a normal project README — stack, how to run locally, how
to deploy, project structure. No more "Stage 1 / Stage 2 / Stage 3 delivery
package" agency language.

### 3. One sitemap generator instead of two
Deleted `scripts/build-sitemap.py` (the canonical-tag-based one). Kept
`sitemap_generator.py` at the root (the git-date-based one) — and improved
it: it now also reads each page's own `<link rel="canonical">` tag and
**skips the page from the sitemap if that tag points somewhere else.** That
means future duplicate pages get automatically excluded instead of quietly
slipping back in, which is exactly what caused the two-generator drift
before.

### 4. Fixed the one genuine duplicate page
`end-to-end-pharmacovigilance-nexus-platform.html`'s canonical tag now
points to `/nexus-platform` (the shorter, higher-priority URL) instead of
itself. It's excluded from the regenerated sitemap as a result. The page
itself is untouched — still live, just marked as secondary to the primary
URL, so Google consolidates ranking signal there instead of splitting it.

### 5. Fixed the real content-duplication problem: 15 templated meta descriptions
Every `/services/*.html` page shared the exact same meta description
template, just swapping the service name in
(`"ClinixAI [X] support covering controlled delivery, regulatory alignment,
quality evidence and inspection-ready governance."`). That's the actual
thin/duplicate-content signal — not the root-vs-services page pairs, which
target genuinely different search intent (software buyer vs. services
buyer) and are fine to keep as-is.

Rewrote all 15 (`<meta name="description">`, `og:description`, and
`twitter:description`) using each page's own real intro copy, so they're
now specific and different from each other. Example:

- Before: *"ClinixAI aggregate safety reporting support covering controlled
  delivery, regulatory alignment, quality evidence and inspection-ready
  governance."*
- After: *"ClinixAI PSUR, PBRER and DSUR authoring, data lock,
  reconciliation and benefit-risk conclusions, delivered through
  controlled, inspection-ready processes."*

### 6. Documented the `scripts/` folder
Added `scripts/README.md` explaining what each of the 15 scripts does and
whether it's safe to re-run — split into ongoing maintenance tools vs.
one-off content generators vs. one-time setup scripts already applied.
Nothing deleted here; these are legitimate build tooling, they just weren't
documented.

### 7. Regenerated `sitemap.xml`
109 URLs (was 110 — the duplicate nexus-platform page dropped out
correctly). Everything else matches what was already confirmed correct.

## What I deliberately did NOT touch

- The root `*-software.html` pages vs. `/services/*` pages (e.g.
  `pharmacovigilance-signal-management-software.html` vs.
  `services/signal-management.html`) — these target different search
  intent and have genuinely different content beyond the meta description.
  Merging or redirecting these would lose real keyword targeting. Worth
  keeping an eye on in Search Console over the next month, but not a fix to
  force through blind.
- The `63c00e...b7b2.txt` verification file — this is your search-console
  domain verification token, deleting it would break domain verification.
- The one-off `build-*.py` content-generation scripts — kept as reference
  tooling even though they're single-purpose, since deleting build tools
  you might need again is riskier than leaving them documented.
