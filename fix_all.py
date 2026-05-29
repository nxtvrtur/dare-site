#!/usr/bin/env python3
"""Comprehensive fix: letter animation, SVG icons, mobile CSS, logo visibility, animations."""
import re, os

DIR = '/Users/mak/Downloads/dare-site'

# ── SVG ICONS ──────────────────────────────────────────────────────
IC_CHECK = '<svg class="ic" viewBox="0 0 14 14" fill="none"><path d="M2 7.5l3.5 3L12 3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
IC_DASH  = '<svg class="ic" viewBox="0 0 14 14" fill="none"><path d="M3 7h8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
IC_ARR   = '<svg class="ic" viewBox="0 0 14 14" fill="none"><path d="M3 11L11 3M11 3H5M11 3v6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
IC_SHIELD = '<svg class="ic" viewBox="0 0 14 14" fill="none"><path d="M7 1.5l-5 2V7c0 2.4 2 4.2 5 4.8 3-.6 5-2.4 5-4.8V3.5l-5-2z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>'

# Icon CSS to inject
IC_CSS = """
/* ── ICONS ── */
.ic{display:inline-block;width:14px;height:14px;flex-shrink:0;vertical-align:middle}
.feat-ck,.p-ck,.p3-ck,.fmt-ck{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;flex-shrink:0;margin-top:1px}"""

# ── HERO ANIMATION for service pages ───────────────────────────────
HERO_ANIM_CSS = """
@keyframes fadeUp{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.h-tag{animation:fadeUp .7s cubic-bezier(.16,1,.3,1) .05s both}
.h-name{animation:fadeUp .9s cubic-bezier(.16,1,.3,1) .15s both}
.h-sub{animation:fadeUp .8s cubic-bezier(.16,1,.3,1) .3s both}
.h-stats{animation:fadeUp .8s cubic-bezier(.16,1,.3,1) .42s both}"""

# ── COMPREHENSIVE MOBILE CSS ────────────────────────────────────────
MOBILE_CSS_FULL = """
/* ════════════════ MOBILE 900px ════════════════ */
@media(max-width:900px){
  .nav-links,.nav-btn{display:none}
  .nav-burger{display:flex;margin-left:auto}
  .w{padding:0 20px}
  .hc{padding:40px 20px 36px}
  .sec{padding:60px 0}
  .sec-sm{padding:36px 0}
  .g2{grid-template-columns:1fr;gap:36px}
  /* hero */
  .h-name{font-size:clamp(40px,12vw,72px) !important;line-height:.92}
  .h-sub{font-size:15px}
  .h-stats{display:grid;grid-template-columns:1fr 1fr;border:1px solid rgba(255,255,255,.1)}
  .hs{padding:16px 18px;border-right:1px solid rgba(255,255,255,.08) !important;border-bottom:1px solid rgba(255,255,255,.08)}
  .hs:nth-child(2n){border-right:none !important}
  .hs:last-child:nth-child(odd){grid-column:1/-1}
  /* grids */
  .price-grid3,.price-grid{grid-template-columns:1fr}
  .p3-card{border-right:none !important;border-bottom:1.5px solid var(--bk)}
  .p3-card:last-child{border-bottom:none}
  .price-grid .p-card{border-right:none !important;border-bottom:1.5px solid var(--bk)}
  .channels{grid-template-columns:repeat(3,1fr) !important}
  .ch{border-right:1.5px solid var(--bk) !important;border-bottom:1.5px solid var(--bk)}
  .ch:nth-child(3n){border-right:none !important}
  .ch:nth-last-child(-n+2){border-bottom:none}
  .formats{grid-template-columns:1fr !important}
  .fmt{border-right:none !important;border-bottom:1.5px solid var(--bk)}
  .fmt:last-child{border-bottom:none}
  .case-stats{grid-template-columns:1fr 1fr}
  .antifrod .af-body{grid-template-columns:1fr !important}
  .af-head{flex-direction:column;gap:10px !important;align-items:flex-start !important}
  .af-head-sub{margin-left:0 !important}
  .proc-item{grid-template-columns:44px 1fr}
  .tl-item{grid-template-columns:90px 1fr}
  /* footer */
  .ft-g{grid-template-columns:1fr 1fr;gap:28px}
  .ft-bot{flex-direction:column;gap:8px}
  /* contacts */
  .c-strip{grid-template-columns:1fr 1fr}
  .c-item{border-right:none !important;border-bottom:1px solid rgba(255,255,255,.1)}
  .c-item:nth-child(2n-1){border-right:1px solid rgba(255,255,255,.1) !important}
  .c-item:last-child,.c-item:nth-last-child(-n+2):nth-child(2n-1){border-bottom:none}
  /* funnel table */
  .funnel-tbl{font-size:12px}
  .dynamics-tbl{font-size:12px}
  .geo-grid{grid-template-columns:1fr 1fr !important}
  .price-solo{flex-direction:column;gap:0}
  .ps-price{border-right:none !important;border-bottom:1.5px solid var(--bk) !important}
}
@media(max-width:600px){
  .channels{grid-template-columns:repeat(2,1fr) !important}
  .ch:nth-child(3n){border-right:1.5px solid var(--bk) !important}
  .ch:nth-child(2n){border-right:none !important}
  .case-stats{grid-template-columns:1fr}
  .c-strip{grid-template-columns:1fr}
  .c-item{border-right:none !important}
  .c-item:nth-child(2n-1){border-right:none !important}
  .c-item:last-child{border-bottom:none}
  .geo-grid{grid-template-columns:1fr !important}
  .formats{grid-template-columns:1fr !important}
  .ft-g{grid-template-columns:1fr}
  .cta-sec{padding:72px 0}
  .disp{font-size:clamp(32px,10vw,56px) !important}
  .h-stats{grid-template-columns:1fr}
  .hs:nth-child(2n){border-right:none !important}
  .hs:nth-child(odd){border-right:none !important}
}"""

# ── INDEX LETTER ANIMATION FIX ─────────────────────────────────────
OLD_H_NAME_CSS = '.h-name{font-family:var(--fa);font-size:clamp(88px,14vw,210px);font-weight:normal;letter-spacing:-.02em;line-height:.88;color:#fff;margin:32px 0 28px;display:flex;overflow:hidden}'
NEW_H_NAME_CSS = '.h-name{font-family:var(--fa);font-size:clamp(88px,14vw,210px);font-weight:normal;letter-spacing:-.02em;line-height:.9;color:#fff;margin:32px 0 28px;display:flex}\n.h-letter-w{display:inline-block;overflow:hidden;padding-bottom:.12em;margin-bottom:-.12em;line-height:1.05}\n.h-letter{display:block;will-change:transform;animation:letterRise 1s cubic-bezier(.16,1,.3,1) calc(var(--i)*.07s + .08s) both}'

# Old letter spans (no wrapper)
OLD_H_LETTERS = '<span class="h-letter" style="--i:0">Д</span><span class="h-letter" style="--i:1">А</span><span class="h-letter" style="--i:2">Р</span><span class="h-letter" style="--i:3">Э</span>'
NEW_H_LETTERS = '<span class="h-letter-w"><span class="h-letter" style="--i:0">Д</span></span><span class="h-letter-w"><span class="h-letter" style="--i:1">А</span></span><span class="h-letter-w"><span class="h-letter" style="--i:2">Р</span></span><span class="h-letter-w"><span class="h-letter" style="--i:3">Э</span></span>'

# RefiRF logo fix - white SVG on off-white = invisible → add dark bg wrapper
OLD_REFIRRF = '<div class="m-logo"><img src="./clients/RefiRF.svg" alt="RefiRF"></div>'
NEW_REFIRRF = '<div class="m-logo"><img src="./clients/RefiRF.svg" alt="RefiRF" style="background:var(--bk);padding:5px 10px"></div>'

# ── PROCESS all service pages ───────────────────────────────────────
SERVICE_PAGES = ['direct.html','seo.html','serm.html','sites.html','ai.html','leads.html','farpost.html','outreach.html']
ALL_PAGES = ['index.html'] + SERVICE_PAGES

def replace_icons(html):
    """Replace emoji checkmarks/dashes with SVG icons."""
    # feat-ck, p-ck, p3-ck, fmt-ck with ✓
    html = re.sub(r'<span class="(feat-ck|p-ck|p3-ck|fmt-ck)">✓</span>',
                  lambda m: f'<span class="{m.group(1)}">{IC_CHECK}</span>', html)
    # same with —
    html = re.sub(r'<span class="(feat-ck|p-ck|p3-ck|fmt-ck)">—</span>',
                  lambda m: f'<span class="{m.group(1)}">{IC_DASH}</span>', html)
    # Arrow ↗ in svc-arr
    html = html.replace('<div class="svc-arr">↗</div>', f'<div class="svc-arr">{IC_ARR}</div>')
    # Shield emoji in antifrod
    html = html.replace('<div class="af-head-icon">🛡</div>', f'<div class="af-head-icon">{IC_SHIELD}</div>')
    # Channel emojis
    html = html.replace('<div class="ch-icon">✈️</div>', '<div class="ch-icon"><svg viewBox="0 0 24 24" fill="none" width="28" height="28"><path d="M21 3L3 10.5l7.5 2L14 21l3-8 4-10z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M10.5 12.5L14 9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></div>')
    html = html.replace('<div class="ch-icon">🟢</div>', '<div class="ch-icon"><svg viewBox="0 0 24 24" fill="none" width="28" height="28"><path d="M20 12c0 4.418-3.582 8-8 8a7.96 7.96 0 01-4-1.07L4 20l1.07-4A7.96 7.96 0 014 12c0-4.418 3.582-8 8-8s8 3.582 8 8z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg></div>')
    html = html.replace('<div class="ch-icon">🟦</div>', '<div class="ch-icon"><svg viewBox="0 0 24 24" fill="none" width="28" height="28"><path d="M4 6h16M4 12h8m-8 6h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M14 9l6 3-6 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
    html = html.replace('<div class="ch-icon">🛒</div>', '<div class="ch-icon"><svg viewBox="0 0 24 24" fill="none" width="28" height="28"><path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-1.5 6h13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="9" cy="21" r="1" fill="currentColor"/><circle cx="19" cy="21" r="1" fill="currentColor"/></svg></div>')
    html = html.replace('<div class="ch-icon">🌐</div>', '<div class="ch-icon"><svg viewBox="0 0 24 24" fill="none" width="28" height="28"><rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M3 9h18" stroke="currentColor" stroke-width="1.5"/><circle cx="7" cy="7" r="0.8" fill="currentColor"/><circle cx="10" cy="7" r="0.8" fill="currentColor"/></svg></div>')
    return html

def fix_mobile_css(html):
    """Replace old minimal mobile CSS with comprehensive version."""
    old = re.search(r'/\* ════════════ MOBILE ════════════ \*/.*?</style>', html, re.DOTALL)
    if old:
        html = html[:old.start()] + MOBILE_CSS_FULL + '\n</style>' + html[old.end():]
    return html

def add_hero_anim_css(html):
    """Add hero animation CSS before closing </style> on service pages."""
    if '@keyframes fadeUp' not in html:
        html = html.replace('</style>', HERO_ANIM_CSS + '\n</style>')
    return html

def add_icon_css(html):
    """Add icon CSS."""
    if '.ic{' not in html:
        html = html.replace('</style>', IC_CSS + '\n</style>')
    return html

def add_service_hero_anims(html):
    """Add animation classes to hero elements on service pages."""
    # h-tag already has class, add animation via CSS
    # h-name on service pages: add animation inline if not AKONY variant
    # h-stats: add animation
    # These are handled by CSS above
    return html

# ══════════════════════════════════════════════════════════════
# FIX index.html
# ══════════════════════════════════════════════════════════════
idx_path = os.path.join(DIR, 'index.html')
with open(idx_path) as f:
    idx = f.read()

# 1. Fix letter animation CSS
idx = idx.replace(OLD_H_NAME_CSS, NEW_H_NAME_CSS)
# 2. Fix letter HTML
idx = idx.replace(OLD_H_LETTERS, NEW_H_LETTERS)
# 3. Fix RefiRF logo (both occurrences)
idx = idx.replace(OLD_REFIRRF, NEW_REFIRRF)
# 4. Fix mobile CSS
idx = fix_mobile_css(idx)
# 5. Add icon CSS
idx = add_icon_css(idx)
# 6. Replace icons
idx = replace_icons(idx)

with open(idx_path, 'w') as f:
    f.write(idx)
print('✓ index.html')

# ══════════════════════════════════════════════════════════════
# FIX all service pages
# ══════════════════════════════════════════════════════════════
for fname in SERVICE_PAGES:
    fpath = os.path.join(DIR, fname)
    with open(fpath) as f:
        html = f.read()

    html = fix_mobile_css(html)
    html = add_hero_anim_css(html)
    html = add_icon_css(html)
    html = replace_icons(html)

    with open(fpath, 'w') as f:
        f.write(html)
    print(f'✓ {fname}')

print('\nAll done.')
