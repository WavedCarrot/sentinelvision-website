import os

website_dir = r'H:\sentinelvision_website'

pages = [
    'index.html', 'pricing.html', 'order.html', 'gallery.html',
    'about.html', 'docs.html', 'changelog.html', 'download.html',
    'privacy.html', 'terms.html', 'platform.html'
]

OLD_BRAND = (
    '    <a href="index.html" class="brand">\n'
    '      <img src="img/logo.svg" alt="SentinelVision Pro" class="brand-logo">\n'
    '    </a>'
)

NEW_BRAND = (
    '    <a href="index.html" class="brand">\n'
    '      <img src="img/logo.svg" alt="SentinelVision Pro" class="brand-logo">\n'
    '      <div class="brand-text">\n'
    '        <strong>SentinelVision</strong>\n'
    '        <span>Pro Security Platform</span>\n'
    '      </div>\n'
    '    </a>'
)

OLD_FOOTER = (
    '      <a href="changelog.html">Changelog</a>\n'
    '      <a href="platform.html">Platform</a>\n'
    '      <a href="privacy.html">Privacy</a>\n'
    '      <a href="terms.html">Terms</a>'
)

NEW_FOOTER = (
    '      <a href="changelog.html">Changelog</a>\n'
    '      <a href="platform.html">Platform</a>\n'
    '      <a href="quote.html">Get a Quote</a>\n'
    '      <a href="privacy.html">Privacy</a>\n'
    '      <a href="terms.html">Terms</a>'
)

for page in pages:
    path = os.path.join(website_dir, page)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix navbar brand text
    if OLD_BRAND in content:
        content = content.replace(OLD_BRAND, NEW_BRAND)
        print(f'[NAVBAR FIXED] {page}')
    elif NEW_BRAND in content:
        print(f'[NAVBAR OK]    {page}')
    else:
        print(f'[NAVBAR MISS]  {page}')

    # Add quote.html to footer
    if 'quote.html' not in content:
        if OLD_FOOTER in content:
            content = content.replace(OLD_FOOTER, NEW_FOOTER)
            print(f'[FOOTER FIXED] {page}')
        else:
            print(f'[FOOTER MISS]  {page}')
    else:
        print(f'[FOOTER OK]    {page}')

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

print('\nAll done.')
