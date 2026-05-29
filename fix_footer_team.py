#!/usr/bin/env python3
"""Add 'Команда' column to footer of all service pages."""
import re, os

DIR = '/Users/mak/Downloads/dare-site'
ALL_PAGES = ['index.html','direct.html','seo.html','serm.html','sites.html',
             'ai.html','leads.html','farpost.html','outreach.html']

TEAM_COL = '<div class="ft-col"><h5>Команда</h5><ul>\n        <li><a href="andrey.html">Андрей</a></li>\n        <li><a href="artur.html">Артур</a></li>\n      </ul></div>\n      '

for fname in ALL_PAGES:
    fpath = os.path.join(DIR, fname)
    with open(fpath) as f:
        html = f.read()

    if 'andrey.html' in html:
        print(f'skip {fname}')
        continue

    # Find the Контакты ft-col and insert team column before it
    m = re.search(r'<div class="ft-col"><h5>Контакты</h5>', html)
    if m:
        html = html[:m.start()] + TEAM_COL + html[m.start():]
        with open(fpath, 'w') as f:
            f.write(html)
        print(f'✓ {fname}')
    else:
        # Try with ft-lbl pattern (index/team pages style)
        m2 = re.search(r'<div class="ft-col">\s*<div class="ft-lbl">Контакты', html)
        if m2:
            team_col2 = '<div class="ft-col">\n          <div class="ft-lbl">Команда</div>\n          <ul>\n            <li><a href="andrey.html">Андрей</a></li>\n            <li><a href="artur.html">Артур</a></li>\n          </ul>\n        </div>\n        '
            html = html[:m2.start()] + team_col2 + html[m2.start():]
            with open(fpath, 'w') as f:
                f.write(html)
            print(f'✓ {fname} (ft-lbl style)')
        else:
            print(f'! {fname} — footer pattern not found')

print('\nDone.')
