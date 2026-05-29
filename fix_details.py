#!/usr/bin/env python3
"""Fix remaining details: icon sizes, service hero to AKONY, h-name animation."""
import os, re

DIR = '/Users/mak/Downloads/dare-site'

SERVICE_PAGES = ['direct.html','seo.html','serm.html','sites.html','ai.html','leads.html','farpost.html','outreach.html']

# ── 1. Fix af-head-icon to use 28px SVG
AF_ICON_CSS_OLD = '.af-head-icon{font-size:22px}'
AF_ICON_CSS_NEW = '.af-head-icon{display:flex;align-items:center}.af-head-icon svg{width:26px;height:26px}'

# ── 2. Service page h-name: switch to AKONY, bigger, letter-masked animation
# OLD h-name CSS on service pages (without AKONY)
OLD_SVC_HNAME = '.h-name{font-size:clamp(52px,8vw,110px);font-weight:900;letter-spacing:-.05em;line-height:.88;color:#fff;margin-bottom:28px}'
NEW_SVC_HNAME = '''.h-name{font-family:var(--fa);font-size:clamp(52px,8vw,120px);font-weight:normal;letter-spacing:-.02em;line-height:.9;color:#fff;margin-bottom:28px;overflow:hidden;padding-bottom:.1em}'''

# ── 3. svc-arr SVG should be bigger
OLD_ARR_IC = '<svg class="ic" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M11 3H5M11 3v6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
NEW_ARR_IC = '<svg width="18" height="18" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M11 3H5M11 3v6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ── 4. feat-ck, p-ck etc icons - make them slightly bigger
OLD_IC_CSS = '.ic{display:inline-block;width:14px;height:14px;flex-shrink:0;vertical-align:middle}\n.feat-ck,.p-ck,.p3-ck,.fmt-ck{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;flex-shrink:0;margin-top:1px}'
NEW_IC_CSS = '.ic{display:inline-block;width:14px;height:14px;flex-shrink:0;vertical-align:middle}\n.feat-ck,.p-ck,.p3-ck,.fmt-ck{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;flex-shrink:0;margin-top:0px;color:var(--bk)}\n.p-card.feat .p-ck,.fmt:last-child .fmt-ck{color:#fff}'

# ── 5. index.html mobile CSS: fix .h-name on mobile to preserve the flex layout
INDEX_MOBILE_HNAME = '  .h-name{font-size:clamp(72px,18vw,120px)}'
# Already handled in MOBILE_CSS_FULL but let's ensure index specific one is right

# ── 6. p3-ck color fix for dark featured card
P3_CK_FIX = '\n.p3-card.feat .p3-ck{color:#fff}'
P3_CK_FIX_MARKER = '.p3-card.feat .p3-ck'

for fname in SERVICE_PAGES:
    fpath = os.path.join(DIR, fname)
    with open(fpath) as f:
        html = f.read()

    # Fix af-head-icon
    html = html.replace(AF_ICON_CSS_OLD, AF_ICON_CSS_NEW)

    # Fix h-name to AKONY
    if OLD_SVC_HNAME in html:
        html = html.replace(OLD_SVC_HNAME, NEW_SVC_HNAME)

    # Fix icon sizes
    html = html.replace(OLD_ARR_IC, NEW_ARR_IC)

    # Fix icon CSS
    if OLD_IC_CSS in html:
        html = html.replace(OLD_IC_CSS, NEW_IC_CSS)

    # Fix p3-ck color for featured card
    if 'p3-card.feat' in html and P3_CK_FIX_MARKER not in html:
        html = html.replace('.p3-card.feat{', '.p3-card.feat{' + '\n')
        # Add after the last p3- rule
        html = re.sub(r'(\.p3-feats li\{[^}]+\})', r'\1' + P3_CK_FIX, html, count=1)

    with open(fpath, 'w') as f:
        f.write(html)
    print(f'✓ {fname}')

# Fix index.html too
idx_path = os.path.join(DIR, 'index.html')
with open(idx_path) as f:
    idx = f.read()

idx = idx.replace(OLD_ARR_IC, NEW_ARR_IC)
if OLD_IC_CSS in idx:
    idx = idx.replace(OLD_IC_CSS, NEW_IC_CSS)

with open(idx_path, 'w') as f:
    f.write(idx)
print('✓ index.html')

print('\nDone.')
