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
    elif redirect.get('destination') != '/pharmacovigilance-internship-programme' or redirect.get('permanent') is not True:
        errors.append(f'vercel.json: invalid legacy redirect {legacy}')

for legacy in ('/insights', '/insights/index.html'):
    redirect = redirects.get(legacy)
    if not redirect:
        errors.append(f'vercel.json: missing retired insights-index redirect {legacy}')
    elif redirect.get('destination') != '/resources' or redirect.get('permanent') is not True:
        errors.append(f'vercel.json: invalid retired insights-index redirect {legacy}')

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
for label, source in (('header.html', header), ('footer.html', footer)):
    if 'href="/insights"' in source:
        errors.append(f'{label}: links to retired /insights index')
for href in ('/resources#white-papers', '/resources#insights'):
    if href not in header:
        errors.append(f'header.html: missing Resources route {href}')
if 'https://blogs.theclinixai.com' not in header:
    errors.append('header.html: missing Blogs route')
for anchor in ('id="white-papers"', 'id="insights"', 'id="blogs"'):
    if anchor not in resources:
        errors.append(f'resources.html: missing resource section {anchor}')
if 'href="/insights"' in resources:
    errors.append('resources.html: links to retired /insights index')

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
if 'https://www.theclinixai.com/insights</loc>' in sitemap:
    errors.append('sitemap.xml: retired /insights index is still listed')
print(f'Pages checked: {len(html_files)}')
print(f'Errors: {len(errors)}')
for x in errors: print('ERROR',x)
print(f'Warnings: {len(warnings)}')
for x in warnings: print('WARN',x)
sys.exit(1 if errors else 0)
