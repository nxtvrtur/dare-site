#!/usr/bin/env python3
"""Add animation CSS and stagger/card-lift classes to all service pages."""
import os, re

ANIMATION_CSS = """
/* ═══════════════════ ANIMATIONS ═══════════════════ */
.stagger > * {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity .55s cubic-bezier(.16,1,.3,1), transform .55s cubic-bezier(.16,1,.3,1);
}
.stagger.visible > *:nth-child(1) { transition-delay: .05s; opacity: 1; transform: none; }
.stagger.visible > *:nth-child(2) { transition-delay: .10s; opacity: 1; transform: none; }
.stagger.visible > *:nth-child(3) { transition-delay: .15s; opacity: 1; transform: none; }
.stagger.visible > *:nth-child(4) { transition-delay: .20s; opacity: 1; transform: none; }
.stagger.visible > *:nth-child(5) { transition-delay: .25s; opacity: 1; transform: none; }
.stagger.visible > *:nth-child(6) { transition-delay: .30s; opacity: 1; transform: none; }
.stagger.visible > *:nth-child(7) { transition-delay: .35s; opacity: 1; transform: none; }
.stagger.visible > *:nth-child(8) { transition-delay: .40s; opacity: 1; transform: none; }
@keyframes countUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: none; }
}
.stat-num { animation: countUp .8s cubic-bezier(.16,1,.3,1) both; }
.hover-line { position: relative; }
.hover-line::after {
  content: '';
  position: absolute;
  bottom: -2px; left: 0;
  height: 1.5px;
  width: 0;
  background: currentColor;
  transition: width .3s ease;
}
.hover-line:hover::after { width: 100%; }
.card-lift {
  transition: transform .25s cubic-bezier(.16,1,.3,1), box-shadow .25s cubic-bezier(.16,1,.3,1);
}
.card-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0,0,0,.12);
}
"""

STAGGER_OBSERVE_JS = """
// Stagger observe
document.querySelectorAll('.stagger').forEach(function(el){
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  },{threshold:.1});
  io.observe(el);
});
"""

service_dirs = ['direct','seo','serm','sites','leads','farpost','outreach']
base = '/Users/mak/Downloads/dare-site'

for d in service_dirs:
    path = os.path.join(base, d, 'index.html')
    if not os.path.exists(path):
        print(f'SKIP (missing): {path}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already patched
    if 'ANIMATIONS' in html:
        print(f'SKIP (already patched): {path}')
        continue

    # 1. Insert animation CSS before </style>
    # Find the last </style> before </head>
    html = html.replace('</style>\n</head>', ANIMATION_CSS + '</style>\n</head>', 1)

    # 2. Add stagger class to price-grid, feat-list, tl (timeline), h-stats
    # price-grid
    html = re.sub(r'class="price-grid(?!")', 'class="price-grid stagger"', html)
    html = re.sub(r'class="price-grid3(?!")', 'class="price-grid3 stagger"', html)
    # feat-list
    html = re.sub(r'class="feat-list(?!")', 'class="feat-list stagger"', html)
    # tl (timeline)
    html = re.sub(r'class="tl(?!")', 'class="tl stagger"', html)
    # c-strip (metrics row)
    html = re.sub(r'class="c-strip(?!")', 'class="c-strip stagger"', html)
    # h-stats
    html = re.sub(r'class="h-stats(?!")', 'class="h-stats stagger"', html)

    # 3. Add card-lift to p-card, fmt (formats), ch (channels)
    html = re.sub(r'class="p-card(?!")', 'class="p-card card-lift"', html)
    html = re.sub(r'class="p3-card(?!")', 'class="p3-card card-lift"', html)

    # 4. SEO-specific: rename .tl-p -> .tl-num and .tl-b -> .tl-body (class names in HTML and CSS)
    if d == 'seo':
        # CSS class definitions
        html = html.replace('.tl-p{', '.tl-num{')
        html = html.replace('.tl-b{', '.tl-body{')
        # HTML class attributes (exact matches only, avoid .tl-body-* conflicts)
        html = re.sub(r'class="tl-p"', 'class="tl-num"', html)
        html = re.sub(r'class="tl-b"', 'class="tl-body"', html)
        # Also update mobile override if present
        html = html.replace('.tl-item{grid-template-columns:80px 1fr}', '.tl-item{grid-template-columns:80px 1fr}')

    # 5. Inject stagger JS observer before closing </script> or before </body>
    # Look for existing IntersectionObserver script block
    if 'IntersectionObserver' in html and 'stagger' not in html:
        # append to existing observer block
        html = html.replace('});\n</script>', '});\n' + STAGGER_OBSERVE_JS + '\n</script>', 1)
    elif '</script>\n</body>' in html and 'stagger' not in html:
        html = html.replace('</script>\n</body>', STAGGER_OBSERVE_JS + '\n</script>\n</body>', 1)
    elif '</body>' in html and 'stagger' not in html:
        # Add a new script block
        html = html.replace('</body>', '<script>\n' + STAGGER_OBSERVE_JS + '\n</script>\n</body>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'PATCHED: {path}')

print('Done.')
