"""Add Open Graph + Twitter Card meta tags to all website pages."""
import os, re

BASE_URL = 'https://sentinelvision.net.za'
SITE_NAME = 'SentinelVision Pro'
# Default OG image (use the logo or a screenshot if available)
DEFAULT_IMAGE = 'https://sentinelvision.net.za/img/logo.svg'

# Per-page overrides: (title, description, url, image)
PAGE_META = {
    'index.html': (
        'SentinelVision Pro — AI Security Platform',
        'AI-powered security software with zone detection, loitering alerts, weapon detection, people counting and real-time Telegram alerts. Delivered pre-configured and ready to use.',
        f'{BASE_URL}/',
        DEFAULT_IMAGE,
    ),
    'about.html': (
        'About — SentinelVision Pro',
        'The story behind SentinelVision Pro — AI security software built in South Africa to give property owners real protection without cloud fees.',
        f'{BASE_URL}/about.html',
        DEFAULT_IMAGE,
    ),
    'changelog.html': (
        'Changelog — SentinelVision Pro',
        'Full release history for SentinelVision Pro. See what changed in each version.',
        f'{BASE_URL}/changelog.html',
        DEFAULT_IMAGE,
    ),
    'docs.html': (
        'Documentation — SentinelVision Pro',
        'Setup guides, camera RTSP configuration, feature guides and troubleshooting for SentinelVision Pro.',
        f'{BASE_URL}/docs.html',
        DEFAULT_IMAGE,
    ),
    'download.html': (
        'Download — SentinelVision Pro',
        'Request the SentinelVision Pro installer. Fill in a short form and receive the download link by email.',
        f'{BASE_URL}/download.html',
        DEFAULT_IMAGE,
    ),
    'gallery.html': (
        'Gallery — SentinelVision Pro',
        'See SentinelVision Pro in action. Dashboard, live zone detection, Telegram alerts, people counting analytics and more.',
        f'{BASE_URL}/gallery.html',
        DEFAULT_IMAGE,
    ),
    'order.html': (
        'Order License — SentinelVision Pro',
        'Order a SentinelVision Pro license. Select your feature and duration, submit your details and receive your activation key within 24 hours.',
        f'{BASE_URL}/order.html',
        DEFAULT_IMAGE,
    ),
    'platform.html': (
        'The SentinelVision Platform — AI Security System',
        'A complete, pre-configured AI security system. One unit. Multiple cameras. Full local control. No cloud. No IT expertise required.',
        f'{BASE_URL}/platform.html',
        DEFAULT_IMAGE,
    ),
    'pricing.html': (
        'Pricing — SentinelVision Pro',
        'Transparent license pricing for SentinelVision Pro. Zone Detection, Loitering, Weapon Detection, People Counting, Full Bundle. Prices in ZAR.',
        f'{BASE_URL}/pricing.html',
        DEFAULT_IMAGE,
    ),
    'privacy.html': (
        'Privacy Policy — SentinelVision Pro',
        'Privacy Policy for SentinelVision Pro. How we collect, use and protect your personal information.',
        f'{BASE_URL}/privacy.html',
        DEFAULT_IMAGE,
    ),
    'quote.html': (
        'Get a Hardware Quote — SentinelVision Pro',
        'Get a quote for the SentinelVision hardware unit. Choose your bundle, fill in your details, and we\'ll respond within 24 hours.',
        f'{BASE_URL}/quote.html',
        DEFAULT_IMAGE,
    ),
    'terms.html': (
        'Terms of Service — SentinelVision Pro',
        'Terms of Service for SentinelVision Pro software licenses and website usage.',
        f'{BASE_URL}/terms.html',
        DEFAULT_IMAGE,
    ),
    'updates.html': (
        'Request a Software Update — SentinelVision Pro',
        'Running an older version of SentinelVision? Request the latest update package here. We\'ll email it to you within 24 hours.',
        f'{BASE_URL}/updates.html',
        DEFAULT_IMAGE,
    ),
}

def make_og_block(title, description, url, image):
    return f'''  <!-- Open Graph / Social sharing -->
  <meta property="og:type"        content="website">
  <meta property="og:site_name"   content="{SITE_NAME}">
  <meta property="og:title"       content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url"         content="{url}">
  <meta property="og:image"       content="{image}">
  <!-- Twitter Card -->
  <meta name="twitter:card"        content="summary">
  <meta name="twitter:title"       content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image"       content="{image}">'''

target_dir = os.path.dirname(os.path.abspath(__file__))
fixed = 0

for filename, (title, description, url, image) in PAGE_META.items():
    fpath = os.path.join(target_dir, filename)
    if not os.path.exists(fpath):
        print(f'  SKIP (not found): {filename}')
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'og:title' in content:
        print(f'  Already has OG: {filename}')
        continue

    og_block = make_og_block(title, description, url, image)

    # Insert after the canonical link (or before </head> as fallback)
    if 'rel="canonical"' in content:
        content = content.replace(
            f'  <link rel="canonical" href="{url}">',
            f'  <link rel="canonical" href="{url}">\n{og_block}'
        )
        # Handle index.html canonical which has trailing slash
        if 'og:title' not in content:
            # Try any canonical line
            content = re.sub(
                r'(\s+<link rel="canonical"[^>]+>)',
                r'\1\n' + og_block,
                content, count=1
            )
    else:
        content = content.replace('</head>', og_block + '\n</head>', 1)

    with open(fpath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print(f'  Fixed: {filename}')
    fixed += 1

print(f'\nAdded OG tags to {fixed} file(s).')
