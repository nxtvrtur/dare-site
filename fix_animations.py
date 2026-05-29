#!/usr/bin/env python3
"""Fix corrupted HTML from bad animation patch and apply correct stagger/card-lift classes."""
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

def add_class_to_attr(html, existing_class, new_class):
    """
    Add new_class to any element that has existing_class in its class attribute.
    Handles both class="existing_class" and class="existing_class otherclass" etc.
    Does not add if new_class already present.
    """
    def replacer(m):
        full = m.group(0)
        classes = m.group(1)
        class_list = classes.split()
        if new_class not in class_list and existing_class in class_list:
            class_list.append(new_class)
        return 'class="' + ' '.join(class_list) + '"'
    # Match class="..." capturing everything inside quotes
    return re.sub(r'class="([^"]*)"', replacer, html)

def add_class_only_when_sole(html, existing_class, new_class):
    """Add new_class only when existing_class is the exact sole class (no prefix/suffix words)."""
    def replacer(m):
        classes = m.group(1).split()
        if existing_class in classes and new_class not in classes:
            classes.append(new_class)
        return 'class="' + ' '.join(classes) + '"'
    return re.sub(r'class="([^"]*)"', replacer, html)

service_dirs = ['direct','seo','serm','sites','leads','farpost','outreach']
base = '/Users/mak/Downloads/dare-site'

for d in service_dirs:
    path = os.path.join(base, d, 'index.html')
    if not os.path.exists(path):
        print(f'SKIP (missing): {path}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── STEP 1: Undo corrupted changes from previous script ──────────────────

    # Fix "tl stagger"-item" → "tl-item", "tl stagger"-p" → "tl-p", etc.
    # Pattern: `class="tl stagger"-SUFFIX"` → `class="tl-SUFFIX"`
    html = re.sub(r'class="tl stagger"-(\w+)"', r'class="tl-\1"', html)

    # Fix `class="feat-list stagger" reveal"` → `class="feat-list reveal"`
    html = re.sub(r'class="feat-list stagger" reveal"', 'class="feat-list reveal"', html)

    # Fix `class="price-grid stagger" reveal"` → `class="price-grid reveal"`
    html = re.sub(r'class="price-grid stagger" reveal"', 'class="price-grid reveal"', html)
    html = re.sub(r'class="price-grid3 stagger" reveal"', 'class="price-grid3 reveal"', html)

    # Fix `class="p-card card-lift" feat"` → `class="p-card feat"`
    html = re.sub(r'class="p-card card-lift" feat"', 'class="p-card feat"', html)
    html = re.sub(r'class="p3-card card-lift" feat"', 'class="p3-card feat"', html)

    # Fix `class="c-strip stagger" ` (if any broken variant)
    html = re.sub(r'class="c-strip stagger" ', 'class="c-strip "', html)
    html = re.sub(r'class="h-stats stagger" ', 'class="h-stats "', html)

    # Fix tl-num / tl-body that got double-corrupted in SEO (they were already renamed, then broke)
    # Restore original tl-p / tl-b names first (we'll rename them properly below)
    if d == 'seo':
        html = re.sub(r'class="tl-num"', 'class="tl-p"', html)
        html = re.sub(r'class="tl-body"', 'class="tl-b"', html)
        html = html.replace('.tl-num{', '.tl-p{')
        html = html.replace('.tl-body{', '.tl-b{')

    # Remove any ANIMATIONS block that was added (we'll re-add cleanly)
    html = re.sub(r'\n/\* ═+\s*ANIMATIONS\s*═+\s*\*/.*?\.card-lift:hover \{[^}]+\}\n', '', html, flags=re.DOTALL)

    # Remove any stagger observe JS that was added
    html = re.sub(r'\n// Stagger observe\ndocument\.querySelectorAll.*?io\.observe\(el\);\s*\}\);\n', '', html, flags=re.DOTALL)

    # ── STEP 2: Remove any duplicate "stagger" or "card-lift" left in class attrs ──
    def clean_classes(m):
        classes = m.group(1).split()
        seen = []
        for c in classes:
            if c not in seen:
                seen.append(c)
        return 'class="' + ' '.join(seen) + '"'
    html = re.sub(r'class="([^"]*)"', clean_classes, html)

    # ── STEP 3: Apply animation CSS cleanly before </style> ──────────────────
    if 'ANIMATIONS' not in html:
        html = html.replace('</style>\n</head>', ANIMATION_CSS + '</style>\n</head>', 1)

    # ── STEP 4: Add stagger to appropriate containers (using safe replacer) ──
    # price-grid (but NOT price-grid3 separately — handle both)
    html = add_class_to_attr(html, 'price-grid', 'stagger')
    html = add_class_to_attr(html, 'price-grid3', 'stagger')
    # feat-list
    html = add_class_to_attr(html, 'feat-list', 'stagger')
    # tl (only the container div with exactly class="tl", not tl-item etc)
    html = add_class_only_when_sole(html, 'tl', 'stagger')
    # c-strip
    html = add_class_to_attr(html, 'c-strip', 'stagger')
    # h-stats
    html = add_class_to_attr(html, 'h-stats', 'stagger')

    # ── STEP 5: Add card-lift to price cards ─────────────────────────────────
    html = add_class_to_attr(html, 'p-card', 'card-lift')
    html = add_class_to_attr(html, 'p3-card', 'card-lift')

    # ── STEP 6: SEO timeline class rename ────────────────────────────────────
    if d == 'seo':
        # CSS
        html = html.replace('.tl-p{', '.tl-num{')
        html = html.replace('.tl-b{', '.tl-body{')
        # HTML: rename class="tl-p" → class="tl-num", class="tl-b" → class="tl-body"
        # Use safe attr replacer
        def seo_rename(m):
            classes = m.group(1).split()
            out = []
            for c in classes:
                if c == 'tl-p': out.append('tl-num')
                elif c == 'tl-b': out.append('tl-body')
                else: out.append(c)
            return 'class="' + ' '.join(out) + '"'
        html = re.sub(r'class="([^"]*)"', seo_rename, html)
        # Also update mobile media query override
        html = html.replace('.tl-item{grid-template-columns:80px 1fr}',
                             '.tl-item{grid-template-columns:80px 1fr}')

    # ── STEP 7: Inject stagger observer JS ───────────────────────────────────
    if 'Stagger observe' not in html:
        if 'IntersectionObserver' in html:
            # Append to existing observer block - find end of last script block
            # Insert before </body>
            html = html.replace('</body>', '<script>' + STAGGER_OBSERVE_JS + '</script>\n</body>', 1)
        else:
            html = html.replace('</body>', '<script>' + STAGGER_OBSERVE_JS + '</script>\n</body>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'FIXED & PATCHED: {path}')

print('Done.')
