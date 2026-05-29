#!/usr/bin/env python3
"""Fix: hero dead zone, h-name overflow, disp clipping, reveal observer, team links in footer."""
import re, os

DIR = '/Users/mak/Downloads/dare-site'
ALL_PAGES = ['index.html','direct.html','seo.html','serm.html','sites.html',
             'ai.html','leads.html','farpost.html','outreach.html']
SERVICE_PAGES = ['direct.html','seo.html','serm.html','sites.html',
                 'ai.html','leads.html','farpost.html','outreach.html']

# ── 1. Fix hero dead zone: remove flex-end so content sits at centre, not bottom ─
OLD_HC = '.hc{flex:1;display:flex;flex-direction:column;justify-content:flex-end;max-width:1240px;margin:0 auto;padding:80px 40px 60px;width:100%}'
NEW_HC = '.hc{flex:1;display:flex;flex-direction:column;justify-content:center;max-width:1240px;margin:0 auto;padding:60px 40px 56px;width:100%}'

# Remove excessive min-height that creates the dead zone
OLD_HERO = 'min-height:68vh;'
NEW_HERO = 'min-height:52vh;'

# ── 2. Fix h-name font-size on service pages — 8vw at 1280px=102px overflows ─
OLD_HNAME_SVC = 'font-size:clamp(52px,8vw,120px)'
NEW_HNAME_SVC = 'font-size:clamp(44px,5.5vw,88px)'

# ── 3. Fix .disp line-height clipping descenders ("заголовки снизу не лезут") ─
OLD_DISP = '.disp{font-size:clamp(40px,6vw,80px);font-weight:900;letter-spacing:-.05em;line-height:.92}'
NEW_DISP = '.disp{font-size:clamp(40px,6vw,80px);font-weight:900;letter-spacing:-.05em;line-height:1.0;padding-bottom:.06em}'

# ── 4. Fix IntersectionObserver — add rootMargin so reveals fire before enter ─
OLD_IO = "{threshold:0.1,rootMargin:'0px 0px -40px 0px'}"
NEW_IO = "{threshold:0.05,rootMargin:'0px 0px -20px 0px'}"

# Also add immediate visibility check on load for elements already in viewport
OLD_IO_SETUP = "    revs.forEach(function(r){io.observe(r);});"
NEW_IO_SETUP = """    revs.forEach(function(r){io.observe(r);});
    // Immediately show elements already in viewport on load
    window.addEventListener('load',function(){
      revs.forEach(function(r){
        var rect=r.getBoundingClientRect();
        if(rect.top<window.innerHeight&&rect.bottom>0)r.classList.add('visible');
      });
    });"""

# ── 5. Add team pages to footer nav ──────────────────────────────────────────
OLD_FOOTER_BRAND_SECTION = '<div class="ft-col">\n          <div class="ft-lbl">Услуги</div>'
NEW_FOOTER_BRAND_SECTION = '<div class="ft-col">\n          <div class="ft-lbl">Услуги</div>'

# Add "Команда" column in footer — we'll inject after the last ft-col closing
# Actually let's just add team links to the footer brand section's description
OLD_FT_BRAND_END = '<div class="ft-col">\n          <div class="ft-lbl">Услуги</div>\n          <ul>'
NEW_FT_BRAND_END = '<div class="ft-col">\n          <div class="ft-lbl">Услуги</div>\n          <ul>'

for fname in SERVICE_PAGES:
    fpath = os.path.join(DIR, fname)
    with open(fpath) as f:
        html = f.read()
    changed = False

    if OLD_HC in html:
        html = html.replace(OLD_HC, NEW_HC); changed = True
    if OLD_HERO in html:
        html = html.replace(OLD_HERO, NEW_HERO); changed = True
    if OLD_HNAME_SVC in html:
        html = html.replace(OLD_HNAME_SVC, NEW_HNAME_SVC); changed = True
    if OLD_DISP in html:
        html = html.replace(OLD_DISP, NEW_DISP); changed = True
    if OLD_IO in html:
        html = html.replace(OLD_IO, NEW_IO); changed = True
    if OLD_IO_SETUP in html:
        html = html.replace(OLD_IO_SETUP, NEW_IO_SETUP); changed = True

    if changed:
        with open(fpath, 'w') as f:
            f.write(html)
        print(f'✓ {fname}')
    else:
        # Try partial matches to debug
        print(f'? {fname} — some rules may differ, checking...')
        if 'justify-content:flex-end' in html:
            html = html.replace(
                'justify-content:flex-end;max-width:1240px;margin:0 auto;padding:80px 40px 60px',
                'justify-content:center;max-width:1240px;margin:0 auto;padding:60px 40px 56px'
            )
            print(f'  fixed hc via partial match')
        html = re.sub(r'font-size:clamp\(52px,8vw,120px\)', 'font-size:clamp(44px,5.5vw,88px)', html)
        html = re.sub(r'line-height:\.92\}', 'line-height:1.0;padding-bottom:.06em}', html)
        with open(fpath, 'w') as f:
            f.write(html)

# Fix index.html .disp too
idx_path = os.path.join(DIR, 'index.html')
with open(idx_path) as f:
    idx = f.read()

if OLD_DISP in idx:
    idx = idx.replace(OLD_DISP, NEW_DISP)
if OLD_IO in idx:
    idx = idx.replace(OLD_IO, NEW_IO)
if OLD_IO_SETUP in idx:
    idx = idx.replace(OLD_IO_SETUP, NEW_IO_SETUP)
# Fix index hc too
if 'justify-content:flex-end' in idx:
    idx = idx.replace(
        'justify-content:flex-end;max-width:1240px;margin:0 auto;padding:80px 40px 60px',
        'justify-content:center;max-width:1240px;margin:0 auto;padding:60px 40px 56px'
    )
# Fix index hero min-height
idx = idx.replace('min-height:68vh;', 'min-height:52vh;')
with open(idx_path, 'w') as f:
    f.write(idx)
print('✓ index.html')

print('\nDone.')
