import os, glob

target_dir = r'H:\sentinelvision_website'

# Exact mappings confirmed by scanning the actual files.
# Each garbled triple is: original UTF-8 bytes read as cp1252, then re-saved as UTF-8.
# U+00E2 U+20AC = â€ prefix (UTF-8 of  cp1252-decoded 0xE2 0x80)
replacements = [
    # â€ sequences (original UTF-8 prefix E2 80)
    ('\u00e2\u20ac\u201c', '\u2013'),  # â€" -> – (EN DASH,   E2 80 93)
    ('\u00e2\u20ac\u201d', '\u2014'),  # â€" -> — (EM DASH,   E2 80 94)
    ('\u00e2\u20ac\u2122', '\u2019'),  # â€™ -> ' (apostrophe, E2 80 99)
    ('\u00e2\u20ac\u00a6', '\u2026'),  # â€¦ -> … (ellipsis,  E2 80 A6)
    ('\u00e2\u20ac\u02dc', '\u2018'),  # â€˜ -> ' (left quote, E2 80 98)
    ('\u00e2\u20ac\u0153', '\u201c'),  # â€œ -> " (left dquote, E2 80 9C)
    # â† sequences (original UTF-8 prefix E2 86: arrows)
    ('\u00e2\u2020\u2019', '\u2192'),  # â†' -> → (right arrow, E2 86 92)
    ('\u00e2\u2020\u2018', '\u2190'),  # â†  -> ← (left arrow,  E2 86 90)
    ('\u00e2\u2020\u201d', '\u2191'),  # â†' -> ↑ (up arrow,    E2 86 91)
    ('\u00e2\u2020\u201c', '\u2193'),  # â†" -> ↓ (down arrow,  E2 86 93)
    # âœ sequences (original UTF-8 prefix E2 9C: dingbats)
    ('\u00e2\u0153\u201c', '\u2713'),  # âœ" -> ✓ (check mark, E2 9C 93)
    ('\u00e2\u0153\u2014', '\u2714'),  # âœ" -> ✔ (heavy check, E2 9C 94)
    ('\u00e2\u0153\u2013', '\u2718'),  # âœ˜ -> ✘ (heavy cross, E2 9C 98)
    # â" sequences (original UTF-8 prefix E2 94: box drawing light)
    ('\u00e2\u201d\u20ac', '\u2500'),  # â"€ -> ─ (light horiz, E2 94 80)
    ('\u00e2\u201d\u201a', '\u2502'),  # â"‚ -> │ (light vert,  E2 94 82)
    ('\u00e2\u201d\u201c', '\u251c'),  # â"" -> ├ (light right, E2 94 9C)
    ('\u00e2\u201d\u2022', '\u2524'),  # â"¤ -> ┤ (light left,  E2 94 A4)
    ('\u00e2\u201d\u2014', '\u252c'),  # â"¬ -> ┬ (light down,  E2 94 AC)
    ('\u00e2\u201d\u00b4', '\u2534'),  # â"´ -> ┴ (light up,   E2 94 B4)
    ('\u00e2\u201d\u00bc', '\u253c'),  # â"¼ -> ┼ (light cross, E2 94 BC)
    # â• sequences (original UTF-8 prefix E2 95: box drawing double)
    ('\u00e2\u2022\u0090', '\u2550'),  # â•\x90 -> ═ (dbl horiz, E2 95 90)
    ('\u00e2\u2022\u0091', '\u2551'),  # â•' -> ║ (dbl vert,   E2 95 91)
    ('\u00e2\u2022\u0097', '\u2557'),  # â•— -> ╗ (dbl top-r,  E2 95 97)
    ('\u00e2\u2022\u009d', '\u255d'),  # â•  -> ╝ (dbl bot-r,  E2 95 9D)
    ('\u00e2\u2022\u0091', '\u2551'),  # â•' -> ║
    ('\u00e2\u2022\u0094', '\u2554'),  # â•" -> ╔ (dbl top-l,  E2 95 94)
    ('\u00e2\u2022\u009a', '\u255a'),  # â•š -> ╚ (dbl bot-l,  E2 95 9A)
]

extensions = ['*.html', '*.css', '*.js']
files = []
for ext in extensions:
    files.extend(glob.glob(os.path.join(target_dir, '**', ext), recursive=True))

fixed_count = 0
for fpath in sorted(files):
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    new_content = content
    for bad, good in replacements:
        new_content = new_content.replace(bad, good)
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        print(f'Fixed: {os.path.basename(fpath)}')
        fixed_count += 1

if fixed_count == 0:
    print('No files needed fixing.')
else:
    print(f'\nFixed {fixed_count} file(s).')

# Verify no garbled sequences remain
print('\n--- Verification ---')
remaining = 0
for fpath in sorted(files):
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    # Check for U+00E2 followed by non-ASCII (potential mojibake)
    hits = sum(1 for i, c in enumerate(content)
               if ord(c) == 0x00e2 and i+1 < len(content) and ord(content[i+1]) > 0x7f)
    if hits:
        print(f'  Still has {hits} hit(s): {os.path.basename(fpath)}')
        # Print unique triplets still present
        triples_left = {}
        for i, c in enumerate(content):
            if ord(c) == 0x00e2 and i+2 < len(content) and ord(content[i+1]) > 0x7f:
                t = content[i:i+3]
                if t not in triples_left:
                    triples_left[t] = content[max(0,i-10):i+15]
        for t, ctx in list(triples_left.items())[:5]:
            cps = tuple(ord(x) for x in t)
            print(f'    U+{cps[0]:04X} U+{cps[1]:04X} U+{cps[2]:04X} in: {repr(ctx)}')
        remaining += hits
if remaining == 0:
    print('  All clear - no garbled symbols remaining.')
