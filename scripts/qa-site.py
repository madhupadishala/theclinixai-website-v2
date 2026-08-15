from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json, re, sys
ROOT = Path(__file__).resolve().parents[1]
IGNORE = {'mailto:', 'tel:', '#', 'javascript:'}
class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.ids=set(); self.h1=0; self.images=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if a.get('id'): self.ids.add(a['id'])
        if tag=='h1': self.h1 += 1
        if tag=='img': self.images.append(a)
errors=[]; warnings=[]
vercel = json.loads((ROOT / 'vercel.json').read_text(encoding='utf-8'))
redirects = {
    item.get('source'): item
    for item in vercel.get('redirects', [])
}
for legacy in ('/academy-individual.html', '/academy-individual'):
    redirect = redirects.get(legacy)
    if not redirect:
        errors.append(f'vercel.json: missing legacy redirect {legacy}')
    elif redirect.get('destination') != '/academy' or redirect.get('permanent') is not True:
        errors.append(f'vercel.json: invalid legacy redirect {legacy}')

for active_route in ('/insights', '/insights/index.html', '/academy', '/nexus-platform'):
    if active_route in redirects:
        errors.append(f'vercel.json: active insights directory must not redirect: {active_route}')

contact_handler = (ROOT / 'api/contact.js').read_text(encoding='utf-8')
if "https://api.resend.com/emails" not in contact_handler:
    errors.append('api/contact.js: Resend delivery is not configured')
if "console.log('CONTACT_ENQUIRY',body)" in contact_handler.replace(' ', ''):
    errors.append('api/contact.js: legacy PII logging remains')
if not (ROOT / 'contact-form.js').exists():
    errors.append('contact-form.js: missing secure form client')

indexnow_key_files = [
    path for path in ROOT.glob('*.txt')
    if re.fullmatch(r'[A-Za-z0-9-]{8,128}\.txt', path.name)
    and path.read_text(encoding='utf-8').strip() == path.stem
]
if len(indexnow_key_files) != 1:
    errors.append(f'IndexNow: expected one valid root key file, found {len(indexnow_key_files)}')

header = (ROOT / 'header.html').read_text(encoding='utf-8')
footer = (ROOT / 'footer.html').read_text(encoding='utf-8')
resources = (ROOT / 'resources.html').read_text(encoding='utf-8')
if 'href="/insights"' not in header:
    errors.append('header.html: missing active Insights directory route /insights')
for href in ('/resources#white-papers',):
    if href not in header:
        errors.append(f'header.html: missing Resources route {href}')
if 'https://blogs.theclinixai.com' not in header:
    errors.append('header.html: missing Blogs route')
for asset in (
    'assets/brand/clinixai-logo-4096.png',
    'assets/brand/clinixai-logo-light-4096.png',
    'assets/brand/clinixai-logo-header.webp',
    'assets/brand/clinixai-logo-footer.webp',
    'assets/brand/clinixai-mark-512.png',
    'favicon.ico',
    'icon-32.png',
    'icon-192.png',
    'icon-512.png',
    'apple-touch-icon.png',
):
    if not (ROOT / asset).exists():
        errors.append(f'brand asset missing: {asset}')
if '/assets/brand/clinixai-logo-header.webp' not in header:
    errors.append('header.html: production wordmark is not installed')
if '/assets/brand/clinixai-logo-footer.webp' not in footer:
    errors.append('footer.html: light production wordmark is not installed')
for anchor in ('id="white-papers"', 'id="insights"', 'id="blogs"'):
    if anchor not in resources:
        errors.append(f'resources.html: missing resource section {anchor}')
if 'href="/insights"' not in resources:
    errors.append('resources.html: missing link to active /insights directory')
if not (ROOT / 'insights' / 'index.html').exists():
    errors.append('insights/index.html: active insights directory is missing')

html_files=[p for p in ROOT.rglob('*.html') if p.name not in {'components.html','product-ui-gallery.html','header.html','footer.html','training.html'}]
for page in html_files:
    text=page.read_text(encoding='utf-8')
    parser=Parser(); parser.feed(text)
    if parser.h1 != 1: errors.append(f'{page.name}: expected one H1, found {parser.h1}')
    if '<meta name="description"' not in text and 'name="description"' not in text: warnings.append(f'{page.name}: missing meta description')
    for img in parser.images:
        if 'alt' not in img: errors.append(f'{page.name}: image missing alt')
        src=img.get('src','')
        if src and not src.startswith(('http:','https:','data:')) and not (ROOT/src.lstrip('/')).exists(): errors.append(f'{page.name}: missing image {src}')
    for link in parser.links:
        if any(link.startswith(x) for x in IGNORE) or link.startswith(('http://','https://')): continue
        target=link.split('#', 1)[0].split('?', 1)[0]
        if not target: continue
        candidate=ROOT/target.lstrip('/')
        if not candidate.exists() and candidate.suffix=='':
            html_candidate=ROOT/(target.lstrip('/')+'.html')
            index_candidate=ROOT/target.lstrip('/')/'index.html'
            candidate=html_candidate if html_candidate.exists() else index_candidate
        if not candidate.exists(): errors.append(f'{page.name}: broken link {link}')

sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
if 'https://www.theclinixai.com/insights</loc>' not in sitemap:
    errors.append('sitemap.xml: active /insights directory is missing')
print(f'Pages checked: {len(html_files)}')
print(f'Errors: {len(errors)}')
for x in errors: print('ERROR',x)
print(f'Warnings: {len(warnings)}')
for x in warnings: print('WARN',x)
sys.exit(1 if errors else 0)
