"""Create HTML redirect stubs at old .html paths pointing to new clean URLs."""
import os

ROOT = r'H:\sentinelvision_website'

PAGES = [
    'about', 'changelog', 'contact', 'docs', 'download',
    'gallery', 'order', 'platform', 'pricing', 'privacy',
    'quote', 'terms', 'updates',
]

TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=/{page}/">
  <link rel="canonical" href="https://sentinelvision.net.za/{page}/">
</head>
<body>
  <script>window.location.replace("/{page}/");</script>
</body>
</html>'''

for page in PAGES:
    path = os.path.join(ROOT, f'{page}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE.format(page=page))
    print(f'Created redirect: {page}.html -> /{page}/')

print('Done')
