# Conversion analytics activation

The website records privacy-limited conversion events through `/api/analytics-event`. It does not transmit form-field contents as analytics data.

## Events

- `page_view`
- `cta_click`
- `form_start`
- `form_submit`
- `resource_download`
- `outbound_click`
- `scroll_depth` at 25%, 50%, 75% and 90%

UTM source, medium, campaign, content and term are retained as first-touch and last-touch attribution and appended to forms as hidden fields.

## GA4 activation

1. Create the production web data stream in the site owner's Google Analytics account.
2. Copy the exact GA4 measurement ID.
3. Run:

   `python scripts/apply-ga4.py --measurement-id "G-XXXXXXXXXX"`

4. Commit and deploy `site.js`.
5. Use GA4 DebugView to verify the seven events.
6. Mark `form_submit` and qualified `cta_click` events as key events only after verifying event quality.

## Privacy and governance

- Do not add patient, case, health or free-text form content to analytics.
- Do not use analytics endpoints for safety-report intake.
- Review retention, consent and privacy requirements for the applicable audience and region.
- Maintain a release record whenever tracking behaviour changes.
