from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import re, sys
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
print(f'Pages checked: {len(html_files)}')
print(f'Errors: {len(errors)}')
for x in errors: print('ERROR',x)
print(f'Warnings: {len(warnings)}')
for x in warnings: print('WARN',x)
sys.exit(1 if errors else 0)
