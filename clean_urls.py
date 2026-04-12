"""
Convert GitHub Pages site from /page.html to /page/ (clean URLs).
- Creates a subdirectory for each HTML page (except index.html)
- Copies the file as index.html inside the subdirectory
- Updates all href/src/canonical/og:url/.html references across every file
- Updates sitemap.xml
"""
import os, shutil, re

ROOT = r'H:\sentinelvision_website'

# Pages to convert (skip index.html — stays at root)
PAGES = [
    'about', 'changelog', 'contact', 'docs', 'download',
    'gallery', 'order', 'platform', 'pricing', 'privacy',
    'quote', 'terms', 'updates',
]

# Step 1: Create subdirs and copy files
for page in PAGES:
    src = os.path.join(ROOT, f'{page}.html')
    dst_dir = os.path.join(ROOT, page)
    dst = os.path.join(dst_dir, 'index.html')
    if os.path.exists(src):
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy2(src, dst)
        print(f'Copied {page}.html -> {page}/index.html')

# Step 2: Rewrite links in all HTML files (root + subdirs)
# Collect all HTML files
html_files = []
for fname in os.listdir(ROOT):
    if fname.endswith('.html'):
        html_files.append(os.path.join(ROOT, fname))
for page in PAGES:
    p = os.path.join(ROOT, page, 'index.html')
    if os.path.exists(p):
        html_files.append(p)

def rewrite_html_links(content):
    # Replace href="page.html" and href="./page.html" -> href="/page/"
    for page in PAGES:
        # href="page.html", href='page.html'
        content = re.sub(
            rf'(href=["\'])(?:\./)?{re.escape(page)}\.html(["\'])',
            rf'\g<1>/{page}/\2',
            content
        )
        # canonical and og:url
        content = content.replace(
            f'https://sentinelvision.net.za/{page}.html',
            f'https://sentinelvision.net.za/{page}/'
        )
    # Fix index.html refs -> /
    content = re.sub(r'href=["\'](?:\./)?index\.html["\']', 'href="/"', content)
    content = content.replace(
        'https://sentinelvision.net.za/index.html',
        'https://sentinelvision.net.za/'
    )
    return content

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = rewrite_html_links(content)
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated links: {os.path.relpath(fpath, ROOT)}')

# Step 3: Update sitemap.xml
sitemap = os.path.join(ROOT, 'sitemap.xml')
with open(sitemap, 'r', encoding='utf-8') as f:
    sm = f.read()
for page in PAGES:
    sm = sm.replace(
        f'https://sentinelvision.net.za/{page}.html',
        f'https://sentinelvision.net.za/{page}/'
    )
sm = sm.replace(
    'https://sentinelvision.net.za/index.html',
    'https://sentinelvision.net.za/'
)
with open(sitemap, 'w', encoding='utf-8') as f:
    f.write(sm)
print('Updated sitemap.xml')

# Step 4: Delete old .html files (after everything is confirmed copied)
for page in PAGES:
    old = os.path.join(ROOT, f'{page}.html')
    if os.path.exists(old):
        os.remove(old)
        print(f'Removed {page}.html')

print('\nDone! All pages now at /<page>/')
