# TheClinixAI Website — Stage 1

This repository contains the rebuilt UI and code foundation for the TheClinixAI public website.

## What changed

- Rewritten global visual system using Manrope, Inter and IBM Plex Mono.
- Replaced rigid 50/50 templates with editorial, asymmetric and scenario-aware layouts.
- Rewritten human, professional copy across all public pages.
- Removed repeated uppercase section labels and templated dash-led copy.
- Added proof-shaped product fragments that show evidence, reasoning and auditability without exposing full product screens.
- Retained the WordPress REST API content architecture for the Resources page.
- Preserved analytics, API, PWA, robots and sitemap foundations.

## Local testing

Open a terminal in this folder and run:

```bash
python -m http.server 8081
```

Then open:

```text
http://localhost:8081
```

Do not open the HTML files by double-clicking because the shared header and footer are loaded through `fetch()`.

## Three-stage delivery model

1. **Stage 1 — UI, copy and code foundation:** complete in this package.
2. **Stage 2 — Custom media production and placement:** product fragments, compliance visuals, social preview and responsive crops.
3. **Stage 3 — Final QA and release package:** performance, browser/mobile QA, SEO validation and deployment-ready ZIP.
