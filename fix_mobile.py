#!/usr/bin/env python3
"""Final mobile fix: hero font size, overflow-x, cursor hide, logo monochrome."""
import os, re

DIR = '/Users/mak/Downloads/dare-site'
SERVICE = ['direct.html','seo.html','serm.html','sites.html','ai.html','leads.html','farpost.html','outreach.html']

# ── The new comprehensive mobile CSS to REPLACE old one ─────────────────
# Applied to all service pages
SERVICE_MOBILE = """
/* ═══════════════════ MOBILE ═══════════════════ */
html,body{overflow-x:hidden}
@media(pointer:coarse),(hover:none){.cursor,.cursor-ring{display:none!important}}
@media(max-width:900px){
  .nav-links,.nav-btn{display:none}
  .nav-burger{display:flex;margin-left:auto}
  .w{padding:0 20px}
  .hc{padding:40px 20px 36px}
  .sec{padding:56px 0}
  .sec-sm{padding:32px 0}
  .g2{grid-template-columns:1fr;gap:32px}
  /* hero — scale to fit longest word (ПРОДВИЖЕНИЕ 11 chars) */
  .h-name{font-size:clamp(18px,7vw,44px)!important;line-height:.92;overflow:hidden}
  .h-sub{font-size:14px}
  /* stats — 2-col grid */
  .h-stats{display:grid;grid-template-columns:1fr 1fr;gap:0}
  .hs{padding:14px 16px;border-right:1px solid rgba(255,255,255,.08)!important;border-bottom:1px solid rgba(255,255,255,.08)}
  .hs:nth-child(2n){border-right:none!important}
  .hs-v{font-size:18px}
  /* grids */
  .price-grid3,.price-grid{grid-template-columns:1fr}
  .p3-card{border-right:none!important;border-bottom:1.5px solid var(--bk)}
  .p3-card:last-child{border-bottom:none}
  .p-card{border-right:none!important;border-bottom:1.5px solid var(--bk)}
  .p-card:last-child{border-bottom:none}
  .channels{grid-template-columns:repeat(3,1fr)!important}
  .ch{border-right:1.5px solid var(--bk)!important;border-bottom:1.5px solid var(--bk)}
  .ch:nth-child(3n){border-right:none!important}
  .ch:nth-last-child(-n+2){border-bottom:none}
  .formats{grid-template-columns:1fr!important}
  .fmt{border-right:none!important;border-bottom:1.5px solid var(--bk)}
  .fmt:last-child{border-bottom:none}
  .case-stats{grid-template-columns:1fr 1fr}
  .antifrod .af-body{grid-template-columns:1fr!important}
  .af-head{flex-direction:column;gap:10px;align-items:flex-start}
  .af-head-sub{margin-left:0!important}
  .proc-item{grid-template-columns:44px 1fr}
  .tl-item{grid-template-columns:80px 1fr}
  .c-strip{grid-template-columns:1fr 1fr}
  .c-item{border-right:none!important;border-bottom:1px solid rgba(255,255,255,.1)}
  .c-item:nth-child(odd){border-right:1px solid rgba(255,255,255,.1)!important}
  .c-item:nth-last-child(-n+2):nth-child(odd){border-bottom:none}
  .c-item:last-child{border-bottom:none}
  .ft-g{grid-template-columns:1fr 1fr;gap:28px}
  .ft-bot{flex-direction:column;gap:8px}
  .cta-sec{padding:64px 0}
  .disp{font-size:clamp(32px,9vw,56px)!important}
  .funnel-tbl,.dynamics-tbl{font-size:11px;overflow-x:auto;display:block}
  .geo-grid{grid-template-columns:1fr 1fr!important}
  .price-solo{flex-direction:column;gap:0}
  .ps-price{border-right:none!important;border-bottom:1.5px solid var(--bk)!important}
}
@media(max-width:480px){
  .h-name{font-size:clamp(16px,6.5vw,36px)!important}
  .channels{grid-template-columns:1fr 1fr!important}
  .ch:nth-child(3n){border-right:1.5px solid var(--bk)!important}
  .ch:nth-child(2n){border-right:none!important}
  .case-stats{grid-template-columns:1fr}
  .c-strip{grid-template-columns:1fr}
  .c-item{border-right:none!important}
  .c-item:nth-child(odd){border-right:none!important}
  .geo-grid{grid-template-columns:1fr!important}
  .ft-g{grid-template-columns:1fr}
  .hs-v{font-size:16px}
}"""

# ── index.html mobile CSS ─────────────────────────────────────────────
INDEX_MOBILE = """
/* ═══════════════════ MOBILE ═══════════════════ */
html,body{overflow-x:hidden}
@media(pointer:coarse),(hover:none){.cursor,.cursor-ring{display:none!important}}
@media(max-width:900px){
  .nav-links,.nav-btn{display:none}
  .nav-burger{display:flex;margin-left:auto}
  .w{padding:0 20px}
  .hc{padding:48px 20px 40px}
  .sec{padding:56px 0}
  .sec-sm{padding:32px 0}
  .g2{grid-template-columns:1fr;gap:36px}
  /* hero — ДАРЭ stays large, 4 letters */
  .h-name{font-size:clamp(68px,18vw,120px)!important;line-height:.9}
  .h-sub{font-size:15px}
  .h-foot{flex-direction:column;gap:20px;align-items:flex-start}
  .h-coord{text-align:left}
  .h-stats{display:flex;flex-direction:column;gap:12px;border:none}
  .hs{padding:0;border:none!important}
  .hs-v{font-size:22px}
  /* service grid */
  .svc-grid{grid-template-columns:1fr 1fr}
  /* why grid */
  .why-grid{grid-template-columns:1fr}
  .wi{border-right:none!important}
  .wi:nth-last-child(-n+2){border-bottom:1px solid rgba(255,255,255,.1)!important}
  .wi:last-child{border-bottom:none!important}
  /* contacts */
  .c-strip{grid-template-columns:1fr 1fr}
  .c-item{border-right:none!important;border-bottom:1px solid rgba(255,255,255,.1)}
  .c-item:nth-child(odd){border-right:1px solid rgba(255,255,255,.1)!important}
  .c-item:last-child{border-bottom:none}
  /* footer */
  .ft-g{grid-template-columns:1fr 1fr;gap:28px}
  .ft-bot{flex-direction:column;gap:8px}
  /* cta */
  .cta-sec{padding:72px 0}
  .disp{font-size:clamp(32px,9vw,56px)!important}
  .btns{flex-direction:column;align-items:center}
  /* clients marquee */
  .m-logo{padding:0 24px;height:44px}
  .m-logo img{height:26px}
}
@media(max-width:480px){
  .h-name{font-size:clamp(56px,16vw,96px)!important}
  .svc-grid{grid-template-columns:1fr}
  .ft-g{grid-template-columns:1fr}
  .c-strip{grid-template-columns:1fr}
  .c-item{border-right:none!important}
  .c-item:nth-child(odd){border-right:none!important}
}"""

# ── Logo monochrome CSS for index.html marquee ────────────────────────
LOGO_MONO_CSS = """
/* logos monochrome */
.m-logo img{filter:brightness(0);opacity:.45;transition:opacity .25s,filter .25s}
.m-logo:hover img{opacity:.85;filter:brightness(0)}"""

LOGO_MONO_MARKER = '/* logos monochrome */'

# ─────────────────────────────────────────────────────────────────────
def replace_mobile_block(html, new_mobile):
    """Replace the entire mobile CSS block."""
    # match from the comment start to closing </style>
    pattern = re.compile(
        r'/\* ═+\s*MOBILE\s*═+ \*/.*?</style>',
        re.DOTALL
    )
    if pattern.search(html):
        return pattern.sub(new_mobile + '\n</style>', html)
    # fallback: append before </style>
    return html.replace('</style>', new_mobile + '\n</style>', 1)

# ─ Fix index.html ────────────────────────────────────────────────────
idx = open(f'{DIR}/index.html').read()
idx = replace_mobile_block(idx, INDEX_MOBILE)

# Add logo monochrome if not already present
if LOGO_MONO_MARKER not in idx:
    idx = idx.replace('</style>', LOGO_MONO_CSS + '\n</style>', 1)

# Remove the ИНКАР-specific invert filter (it will be darkened by brightness(0) universally)
idx = idx.replace(' style="filter:invert(1) brightness(.7)"', '')

with open(f'{DIR}/index.html', 'w') as f:
    f.write(idx)
print('✓ index.html')

# ─ Fix service pages ─────────────────────────────────────────────────
for fname in SERVICE:
    fpath = f'{DIR}/{fname}'
    html = open(fpath).read()
    html = replace_mobile_block(html, SERVICE_MOBILE)
    with open(fpath, 'w') as f:
        f.write(html)
    print(f'✓ {fname}')

print('\nDone.')
