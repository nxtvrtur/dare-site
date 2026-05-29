#!/usr/bin/env python3
"""Add burger button HTML and JS to service pages."""

BURGER_BTN = '''    <button class="nav-burger" id="burger" aria-label="Меню">
      <span></span><span></span><span></span>
    </button>'''

HAMBURGER_JS = '''<script>
(function(){
  var burger=document.getElementById('burger');
  var mob=document.getElementById('navMobile');
  if(!burger||!mob)return;
  burger.addEventListener('click',function(){
    burger.classList.toggle('open');
    mob.classList.toggle('open');
    document.body.style.overflow=mob.classList.contains('open')?'hidden':'';
  });
  mob.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click',function(){
      burger.classList.remove('open');
      mob.classList.remove('open');
      document.body.style.overflow='';
    });
  });
  // Scroll reveal
  var revs=document.querySelectorAll('.reveal,.reveal-left');
  if(revs.length){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){if(e.isIntersecting)e.target.classList.add('visible');});
    },{threshold:0.1,rootMargin:'0px 0px -40px 0px'});
    revs.forEach(function(r){io.observe(r);});
  }
})();
</script>'''

files = ['direct.html', 'seo.html', 'serm.html', 'sites.html', 'ai.html', 'leads.html', 'farpost.html', 'outreach.html']

for fname in files:
    fpath = f'/Users/mak/Downloads/dare-site/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Add burger button before </div>\n</nav>
    if 'id="burger"' not in html:
        # Find the closing sequence of nav
        old = '    <a href="tel:+79958702227" class="btn nav-btn">Обсудить проект</a>\n  </div>\n</nav>'
        new = '    <a href="tel:+79958702227" class="btn nav-btn">Обсудить проект</a>\n' + BURGER_BTN + '\n  </div>\n</nav>'
        if old in html:
            html = html.replace(old, new)
            print(f'  Added burger button to {fname}')
        else:
            # Try with 4-space indent on </div>
            old2 = '    <a href="tel:+79958702227" class="btn nav-btn">Обсудить проект</a>\n    </div>\n</nav>'
            new2 = '    <a href="tel:+79958702227" class="btn nav-btn">Обсудить проект</a>\n' + BURGER_BTN + '\n    </div>\n</nav>'
            if old2 in html:
                html = html.replace(old2, new2)
                print(f'  Added burger button (4-space) to {fname}')
            else:
                print(f'  WARNING: Could not find nav closing in {fname}')
                # Print context around nav-btn
                idx = html.find('class="btn nav-btn"')
                if idx >= 0:
                    print(f'    Context: {repr(html[idx:idx+100])}')

    # Add JS before </body>
    if 'getElementById(\'burger\')' not in html:
        html = html.replace('</body>', HAMBURGER_JS + '\n</body>')
        print(f'  Added JS to {fname}')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✓ {fname}')
