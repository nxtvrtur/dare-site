#!/usr/bin/env python3
"""Update all service pages: AKONY font, SVG nav logo, hamburger nav, mobile CSS, scroll reveal."""

import re

AKONY_FONT = "@font-face{font-family:'AKONY';src:url('./fonts/AKONY.otf') format('opentype'),url('./fonts/AKONY.ttf') format('truetype');font-weight:normal;font-style:normal;font-display:swap}\n"

# The --fa variable addition to :root
ROOT_WITH_FA = ":root{--bk:#0a0a0a;--wh:#fff;--off:#f7f6f3;--br:#e0e0e0;--mu:#888;--f:'Inter',sans-serif;--fa:'AKONY','Inter',sans-serif}"
ROOT_WITHOUT_FA = ":root{--bk:#0a0a0a;--wh:#fff;--off:#f7f6f3;--br:#e0e0e0;--mu:#888;--f:'Inter',sans-serif}"

NAV_LOGO_HTML = '''<a href="index.html" class="nav-logo">
      <svg height="18" viewBox="0 0 587 326" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M234.03 133.731H60.5611V149.015H0.191045V87.8805H21.588L40.8836 45.2776C54.7661 15.0925 78.2009 0 111.188 0H279.116V87.8805H294.4V149.015H234.03V133.731ZM87.4984 87.8805H218.746V45.8507H126.089C113.353 45.8507 104.31 51.6457 98.9611 63.2358L87.4984 87.8805Z" fill="white"/>
        <path d="M586.522 133.731H518.51L503.035 114.627H385.352L369.877 133.731H301.865L410.188 0H478.2L586.522 133.731ZM472.086 76.4178L444.194 42.0298L416.301 76.4178H472.086Z" fill="white"/>
        <path d="M0 191.045H209.555C222.888 191.045 234.806 192.573 245.311 195.63C255.815 198.686 264.704 202.762 271.976 207.857C279.249 212.824 284.804 218.491 288.642 224.86C292.481 231.228 294.4 237.787 294.4 244.537C294.4 251.16 292.481 257.719 288.642 264.215C284.804 270.583 279.249 276.314 271.976 281.409C264.704 286.376 255.815 290.388 245.311 293.445C234.806 296.501 222.888 298.03 209.555 298.03H60.3701V324.776H0V191.045ZM60.3701 236.895V252.179H185.313C225.312 252.179 237.724 247.562 245.311 244.537C237.724 241.99 225.312 236.895 185.313 236.895H60.3701Z" fill="white"/>
        <path d="M388.84 273.512V239.124H521.616C519.451 235.049 516.139 231.482 511.682 228.426C507.224 225.369 501.174 223.841 493.532 223.841H380.964C374.546 223.841 371.337 226.388 371.337 231.482V235.303H302.201V231.482C302.201 225.242 303.806 219.447 307.015 214.097C310.223 208.748 314.745 204.099 320.579 200.151C326.559 196.203 333.706 193.146 342.02 190.981C350.48 188.688 359.815 187.542 370.025 187.542H519.515C528.685 187.542 537.345 189.389 545.497 193.082C553.648 196.776 560.716 201.807 566.703 208.175C572.816 214.416 577.592 221.739 581.031 230.145C584.597 238.424 586.38 247.148 586.38 256.318C586.38 265.488 584.597 274.276 581.031 282.682C577.592 290.961 572.816 298.284 566.703 304.652C560.716 310.893 553.648 315.86 545.497 319.554C537.345 323.247 528.685 325.094 519.515 325.094H370.025C359.815 325.094 350.48 324.012 342.02 321.846C333.706 319.554 326.559 316.434 320.579 312.485C314.745 308.537 310.223 303.888 307.015 298.539C303.806 293.19 302.201 287.395 302.201 281.154V277.333H371.337V281.154C371.337 286.249 374.546 288.796 380.964 288.796H493.532C501.174 288.796 507.224 287.267 511.682 284.211C516.139 281.154 519.451 277.588 521.616 273.512H388.84Z" fill="white"/>
      </svg>
    </a>'''

FOOTER_LOGO_HTML = '''<a href="index.html" class="nav-logo" style="display:inline-flex">
          <svg height="18" viewBox="0 0 587 326" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M234.03 133.731H60.5611V149.015H0.191045V87.8805H21.588L40.8836 45.2776C54.7661 15.0925 78.2009 0 111.188 0H279.116V87.8805H294.4V149.015H234.03V133.731ZM87.4984 87.8805H218.746V45.8507H126.089C113.353 45.8507 104.31 51.6457 98.9611 63.2358L87.4984 87.8805Z" fill="white"/>
            <path d="M586.522 133.731H518.51L503.035 114.627H385.352L369.877 133.731H301.865L410.188 0H478.2L586.522 133.731ZM472.086 76.4178L444.194 42.0298L416.301 76.4178H472.086Z" fill="white"/>
            <path d="M0 191.045H209.555C222.888 191.045 234.806 192.573 245.311 195.63C255.815 198.686 264.704 202.762 271.976 207.857C279.249 212.824 284.804 218.491 288.642 224.86C292.481 231.228 294.4 237.787 294.4 244.537C294.4 251.16 292.481 257.719 288.642 264.215C284.804 270.583 279.249 276.314 271.976 281.409C264.704 286.376 255.815 290.388 245.311 293.445C234.806 296.501 222.888 298.03 209.555 298.03H60.3701V324.776H0V191.045ZM60.3701 236.895V252.179H185.313C225.312 252.179 237.724 247.562 245.311 244.537C237.724 241.99 225.312 236.895 185.313 236.895H60.3701Z" fill="white"/>
            <path d="M388.84 273.512V239.124H521.616C519.451 235.049 516.139 231.482 511.682 228.426C507.224 225.369 501.174 223.841 493.532 223.841H380.964C374.546 223.841 371.337 226.388 371.337 231.482V235.303H302.201V231.482C302.201 225.242 303.806 219.447 307.015 214.097C310.223 208.748 314.745 204.099 320.579 200.151C326.559 196.203 333.706 193.146 342.02 190.981C350.48 188.688 359.815 187.542 370.025 187.542H519.515C528.685 187.542 537.345 189.389 545.497 193.082C553.648 196.776 560.716 201.807 566.703 208.175C572.816 214.416 577.592 221.739 581.031 230.145C584.597 238.424 586.38 247.148 586.38 256.318C586.38 265.488 584.597 274.276 581.031 282.682C577.592 290.961 572.816 298.284 566.703 304.652C560.716 310.893 553.648 315.86 545.497 319.554C537.345 323.247 528.685 325.094 519.515 325.094H370.025C359.815 325.094 350.48 324.012 342.02 321.846C333.706 319.554 326.559 316.434 320.579 312.485C314.745 308.537 310.223 303.888 307.015 298.539C303.806 293.19 302.201 287.395 302.201 281.154V277.333H371.337V281.154C371.337 286.249 374.546 288.796 380.964 288.796H493.532C501.174 288.796 507.224 287.267 511.682 284.211C516.139 281.154 519.451 277.588 521.616 273.512H388.84Z" fill="white"/>
          </svg>
        </a>'''

# Old logo text with SVG 'D' mark
OLD_LOGO_CSS = ".logo{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:900;letter-spacing:.12em;color:#fff;flex-shrink:0}"

NEW_LOGO_CSS = """.nav-logo{display:flex;align-items:center;flex-shrink:0}
.nav-logo svg{height:18px;width:auto}"""

# Hamburger CSS to add
HAMBURGER_CSS = """
/* hamburger */
.nav-burger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:8px;z-index:300}
.nav-burger span{display:block;width:22px;height:1.5px;background:#fff;transition:transform .3s,opacity .3s}
.nav-burger.open span:nth-child(1){transform:translateY(6.5px) rotate(45deg)}
.nav-burger.open span:nth-child(2){opacity:0}
.nav-burger.open span:nth-child(3){transform:translateY(-6.5px) rotate(-45deg)}
/* mobile overlay */
.nav-mobile{position:fixed;inset:0;background:var(--bk);z-index:250;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:40px;gap:8px;opacity:0;pointer-events:none;transition:opacity .3s}
.nav-mobile.open{opacity:1;pointer-events:all}
.nav-mobile a{font-size:clamp(28px,6vw,48px);font-weight:800;letter-spacing:-.03em;color:rgba(255,255,255,.35);transition:color .2s;display:block;padding:8px 0}
.nav-mobile a:hover{color:#fff}
.nav-mobile .nm-contact{font-size:14px;color:rgba(255,255,255,.3);margin-top:32px;line-height:1.8}
/* scroll reveal */
.reveal{opacity:0;transform:translateY(28px);transition:opacity .75s cubic-bezier(.16,1,.3,1),transform .75s cubic-bezier(.16,1,.3,1)}
.reveal.visible{opacity:1;transform:none}
.reveal-left{opacity:0;transform:translateX(-28px);transition:opacity .75s cubic-bezier(.16,1,.3,1),transform .75s cubic-bezier(.16,1,.3,1)}
.reveal-left.visible{opacity:1;transform:none}"""

MOBILE_CSS = """
/* ════════════ MOBILE ════════════ */
@media(max-width:900px){
  .nav-links,.nav-btn{display:none}
  .nav-burger{display:flex;margin-left:auto}
  .w,.hc{padding-left:20px;padding-right:20px}
  .sec{padding:64px 0}.sec-sm{padding:40px 0}
  .g2{grid-template-columns:1fr;gap:40px}
  .h-name{font-size:clamp(52px,14vw,88px)}
  .h-stats{flex-wrap:wrap;gap:0}
  .hs{padding:14px 20px}
  .price-grid3,.price-grid{grid-template-columns:1fr}
  .proc-item{grid-template-columns:48px 1fr}
  .ft-g{grid-template-columns:1fr 1fr;gap:32px}
  .ft-bot{flex-direction:column;gap:8px}
  .c-strip{grid-template-columns:1fr}
  .c-item{border-right:none !important;border-bottom:1px solid rgba(255,255,255,.1)}
  .c-item:last-child{border-bottom:none}
}
@media(max-width:480px){
  .ft-g{grid-template-columns:1fr}
  .h-name{font-size:clamp(42px,16vw,72px)}
}"""

MOBILE_OVERLAY_HTML = """<!-- MOBILE NAV -->
<div class="nav-mobile" id="navMobile">
  <a href="direct.html">Директ</a>
  <a href="seo.html">SEO</a>
  <a href="serm.html">SERM</a>
  <a href="sites.html">Сайты</a>
  <a href="ai.html">ИИ-Менеджер</a>
  <a href="leads.html">Лиды</a>
  <a href="farpost.html">Фарпост</a>
  <a href="outreach.html">Outreach</a>
  <div class="nm-contact">+7 995 870-22-27<br>cmo@daremarketing.ru<br>t.me/coodare</div>
</div>

"""

BURGER_BUTTON_HTML = """
    <button class="nav-burger" id="burger" aria-label="Меню">
      <span></span><span></span><span></span>
    </button>"""

HAMBURGER_JS = """
<script>
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
</script>"""

# Old nav logo HTML (the D-shape SVG + text)
OLD_NAV_LOGO = '<a href="index.html" class="logo"><svg width="22" height="21" viewBox="0 0 228 219" fill="none"><path d="M118.678 0C178.954 0 227.986 49.0356 227.986 109.315C227.986 169.595 178.954 218.318 118.678 218.318H104.936V0H118.678ZM85.573 218.318H0V0H85.573V218.318Z" fill="white"/></svg>ДАРЭ</a>'

files = ['direct.html', 'seo.html', 'serm.html', 'sites.html', 'ai.html', 'leads.html', 'farpost.html', 'outreach.html']

for fname in files:
    fpath = f'/Users/mak/Downloads/dare-site/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add AKONY font if missing
    if 'AKONY' not in html:
        html = html.replace('*,*::before,*::after', AKONY_FONT + '*,*::before,*::after')

    # 2. Add --fa to :root if missing
    if '--fa' not in html:
        html = html.replace(ROOT_WITHOUT_FA, ROOT_WITH_FA)

    # 3. Replace old logo CSS
    html = html.replace(OLD_LOGO_CSS, NEW_LOGO_CSS)

    # 4. Add hamburger CSS before </style>
    if 'nav-burger' not in html:
        html = html.replace('</style>', HAMBURGER_CSS + '\n</style>')

    # 5. Add mobile CSS before </style>
    if '@media(max-width:900px)' not in html:
        html = html.replace('</style>', MOBILE_CSS + '\n</style>')

    # 6. Add mobile overlay before <nav>
    if 'nav-mobile' not in html:
        html = html.replace('<nav>', MOBILE_OVERLAY_HTML + '<nav>')

    # 7. Replace old nav logo with new SVG logo (in nav section only)
    html = html.replace(OLD_NAV_LOGO, NAV_LOGO_HTML, 1)  # only first occurrence (nav)

    # 8. Replace footer old logo (second occurrence)
    # Footer logo is also OLD_NAV_LOGO
    if OLD_NAV_LOGO in html:
        html = html.replace(OLD_NAV_LOGO, FOOTER_LOGO_HTML, 1)

    # 9. Add burger button before </div></nav>
    if 'nav-burger' in html and 'id="burger"' not in html:
        # Add burger button before closing div of nav
        html = html.replace(
            '<a href="tel:+79958702227" class="btn nav-btn">Обсудить проект</a>\n    </div>\n</nav>',
            '<a href="tel:+79958702227" class="btn nav-btn">Обсудить проект</a>' + BURGER_BUTTON_HTML + '\n    </div>\n</nav>'
        )

    # 10. Add hamburger JS before </body>
    if 'id="burger"' in html and 'nav-mobile' in html and 'getElementById(\'burger\')' not in html:
        html = html.replace('</body>', HAMBURGER_JS + '\n</body>')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'✓ {fname}')

print('Done!')
