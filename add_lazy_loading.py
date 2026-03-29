import re, glob, os

def process(html):
    def fix(m):
        tag = m.group(0)
        if 'loading=' in tag:
            return tag
        # Footer logos get lazy loading
        if 'brand-logo-footer' in tag:
            return tag[:-1].rstrip() + ' loading="lazy">'
        # Skip navbar brand-logo (above the fold, should stay eager)
        if 'brand-logo' in tag and 'footer' not in tag:
            return tag
        # All other images get lazy loading
        return tag[:-1].rstrip() + ' loading="lazy">'
    return re.sub(r'<img[^>]+>', fix, html)

changed = 0
for path in glob.glob(r'H:/sentinelvision_website/*.html'):
    txt = open(path, encoding='utf-8').read()
    new = process(txt)
    if new != txt:
        open(path, 'w', encoding='utf-8').write(new)
        print('Updated:', os.path.basename(path))
        changed += 1
    else:
        print('No change:', os.path.basename(path))
print(f'Done. {changed} files updated.')
