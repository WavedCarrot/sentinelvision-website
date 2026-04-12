"""Fix asset paths in all subdir index.html files — make them root-relative."""
import os, re

ROOT = r'H:\sentinelvision_website'

PAGES = [
    'about', 'changelog', 'contact', 'docs', 'download',
    'gallery', 'order', 'platform', 'pricing', 'privacy',
    'quote', 'terms', 'updates',
]

def fix_paths(content):
    # Relative asset refs that need to become root-relative
    # css/style.css -> /css/style.css
    content = re.sub(r'(href=["\'])css/', r'\g<1>/css/', content)
    # js/main.js etc -> /js/...
    content = re.sub(r'(src=["\'])js/', r'\g<1>/js/', content)
    # img/... -> /img/...
    content = re.sub(r'(src=["\'])img/', r'\g<1>/img/', content)
    content = re.sub(r'(href=["\'])img/', r'\g<1>/img/', content)
    return content

for page in PAGES:
    fpath = os.path.join(ROOT, page, 'index.html')
    if not os.path.exists(fpath):
        print(f'MISSING: {fpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    new = fix_paths(content)
    if new != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new)
        print(f'Fixed: {page}/index.html')
    else:
        print(f'No change: {page}/index.html')

print('Done')
