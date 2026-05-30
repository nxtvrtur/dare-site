/* ══════════════════════════════════════════════════════════════════
   ДАРЭ · motion.js — single self-bootstrapping motion runtime.
   Loaded (defer) on all 13 pages AFTER vendor/gsap, ScrollTrigger, lenis.
   Feature-detects every hook so one HTML can't drift from another.
   Owns: reveals, WebGL hero + gating, hamburger, chat, count-up,
   magnetic CTAs, split-hero, velocity marquee, page transition.
   Honors prefers-reduced-motion / low-power in lockstep with motion.css.
   ══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var html = document.documentElement;
  html.classList.add('js-motion'); // gate: kills no-JS reveal-hide, enables motion CSS

  var gsap = window.gsap || null;
  var ST = window.ScrollTrigger || null;
  var LenisCtor = window.Lenis || null;

  var mqReduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var conn = navigator.connection || {};
  var lowPower = (navigator.deviceMemory && navigator.deviceMemory < 4) || conn.saveData === true;
  function reduced() { return mqReduce.matches; }
  var finePointer = window.matchMedia('(hover:hover) and (pointer:fine)').matches;

  if (lowPower) html.classList.add('mo-lite');

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function safe(label, fn) { try { fn(); } catch (e) { /* never let one feature break the page */ if (window.console) console.warn('[motion] ' + label, e); } }

  var lenis = null;

  /* ─────────────────────────── REVEALS ─────────────────────────── */
  function initReveals() {
    var els = $$('.reveal, .reveal-left, .stagger');
    if (reduced()) { els.forEach(function (el) { el.classList.add('visible'); }); return; }
    // svc-grid child stagger parity (some pages relied on inline JS for this)
    $$('.svc-grid').forEach(function (grid) {
      $$('.svc-card', grid).forEach(function (c, i) { if (!c.style.transitionDelay) c.style.transitionDelay = (i * 0.05) + 's'; });
    });
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -10% 0px' });
    els.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('visible'); // above-fold: show now
      else io.observe(el);
    });
    // safety net — nothing stays invisible
    setTimeout(function () {
      els.forEach(function (el) { if (!el.classList.contains('visible')) { var r = el.getBoundingClientRect(); if (r.top < window.innerHeight * 1.2) el.classList.add('visible'); } });
    }, 1400);
  }

  /* ──────────────── CLIP-WIPE HEADERS + PERSPECTIVE LIFT ───────────────
     Tag section headers and card grids; CSS in motion.css does the rest. */
  function initTexture() {
    if (reduced()) return;
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('mo-in'); io.unobserve(e.target); } });
    }, { threshold: 0.2, rootMargin: '0px 0px -8% 0px' });
    $$('.sh .t1').forEach(function (t) { t.classList.add('mo-wipe'); io.observe(t); });
    $$('.svc-grid, .why-grid, .case-cards, .price-deck, .pdeck, .wi-grid').forEach(function (g, gi) {
      g.classList.add('mo-lift');
      $$(':scope > *', g).forEach(function (ch, i) { ch.style.setProperty('--li', i); });
      io.observe(g);
    });
  }

  /* ─────────────────────── HAMBURGER / MOBILE NAV ─────────────────────── */
  function initBurger() {
    var burger = $('#burger') || $('.nav-burger');
    var mob = $('#navMobile') || $('.nav-mobile');
    if (!burger || !mob) return;
    function setOpen(open) {
      burger.classList.toggle('open', open);
      mob.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      mob.setAttribute('aria-hidden', open ? 'false' : 'true');
      document.body.style.overflow = open ? 'hidden' : '';
    }
    burger.setAttribute('aria-expanded', 'false');
    mob.setAttribute('aria-hidden', 'true');
    burger.addEventListener('click', function () { setOpen(!mob.classList.contains('open')); });
    $$('a', mob).forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && mob.classList.contains('open')) setOpen(false); });
  }

  /* ─────────────────────────── CHAT WIDGET ─────────────────────────── */
  function initChat() {
    var bubble = $('#chatBubble'), toggle = $('#chatToggle');
    if (!bubble || !toggle) return;
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      bubble.classList.toggle('open');
      if (bubble.classList.contains('open')) { var i = $('#cpInput'); if (i) setTimeout(function () { i.focus(); }, 320); }
    });
    document.addEventListener('click', function (e) { if (bubble && !bubble.contains(e.target)) bubble.classList.remove('open'); });
    var body = $('#cpBody'), inp = $('#cpInput'), send = $('#cpSend');
    var history = [], busy = false;
    function addMsg(t, u) { if (!body) return null; var el = document.createElement('div'); el.className = 'cp-msg' + (u ? ' user' : ''); el.textContent = t; body.appendChild(el); body.scrollTop = body.scrollHeight; return el; }
    function typing() { if (!body) return null; var el = document.createElement('div'); el.className = 'cp-typing'; el.innerHTML = '<span></span><span></span><span></span>'; body.appendChild(el); body.scrollTop = body.scrollHeight; return el; }
    function submit() {
      if (busy) return;
      var v = inp ? inp.value.trim() : ''; if (!v) return;
      addMsg(v, true); inp.value = ''; history.push({ role: 'user', content: v });
      busy = true; var t = typing();
      fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: v, history: history.slice(-20) }) })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (t) t.remove();
          var reply = (d && d.ok && d.reply) ? d.reply : ((d && d.error) || 'Не получилось ответить. Напишите в Telegram: t.me/coodare');
          addMsg(reply, false); history.push({ role: 'assistant', content: reply }); busy = false;
        })
        .catch(function () { if (t) t.remove(); addMsg('Сеть недоступна. Напишите нам в Telegram: t.me/coodare', false); busy = false; });
    }
    if (send) send.addEventListener('click', submit);
    if (inp) inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') submit(); });
  }

  /* ───────────────────── WebGL MESH-GRADIENT HERO + GATING ───────────────────── */
  var glStop = null, glReq = null;
  function initHeroGL() {
    var canvas = $('#heroCanvas'); if (!canvas) return;
    var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (!gl) { canvas.style.display = 'none'; return; }
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    function resize() { canvas.width = canvas.offsetWidth * dpr; canvas.height = canvas.offsetHeight * dpr; gl.viewport(0, 0, canvas.width, canvas.height); }
    resize();
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(resize, 150); });
    var vs = 'attribute vec2 pos;void main(){gl_Position=vec4(pos,0.,1.);}';
    var fs = [
      'precision highp float;uniform float t;uniform vec2 res;',
      'const vec3 C0=vec3(0.,0.,0.);const vec3 C1=vec3(.05,.05,.06);const vec3 C2=vec3(.12,.12,.13);const vec3 C3=vec3(1.,1.,1.);',
      'void main(){vec2 uv=gl_FragCoord.xy/res;uv.y=1.-uv.y;float s=t*.16;',
      'vec2 p0=vec2(.5+.42*cos(s*.73),.5+.42*sin(s*.51));vec2 p1=vec2(.5+.42*cos(s*.41+2.09),.5+.42*sin(s*.63+2.09));',
      'vec2 p2=vec2(.5+.38*cos(s*.52+4.19),.5+.38*sin(s*.34+4.19));vec2 p3=vec2(.5+.36*cos(s*.61+1.05),.5+.36*sin(s*.47+3.49));',
      'float e=2.5e-4;float d0=1./(dot(uv-p0,uv-p0)+e);float d1=1./(dot(uv-p1,uv-p1)+e);float d2=1./(dot(uv-p2,uv-p2)+e);float d3=1./(dot(uv-p3,uv-p3)+e);',
      'float wt=d0+d1+d2+d3;vec3 col=(C0*d0+C1*d1+C2*d2+C3*d3)/wt;gl_FragColor=vec4(col,1.);}'
    ].join('\n');
    function mk(tp, src) { var sh = gl.createShader(tp); gl.shaderSource(sh, src); gl.compileShader(sh); return sh; }
    var prog = gl.createProgram(); gl.attachShader(prog, mk(gl.VERTEX_SHADER, vs)); gl.attachShader(prog, mk(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(prog); gl.useProgram(prog);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var aPos = gl.getAttribLocation(prog, 'pos'); gl.enableVertexAttribArray(aPos); gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);
    var uT = gl.getUniformLocation(prog, 't'), uR = gl.getUniformLocation(prog, 'res');
    var t0 = performance.now(), tScale = 1, simT = 0, last = t0;
    window.__moHeroTimeScale = function (v) { tScale = v; }; // ScrollTrigger scrub hook
    function frame(now) {
      var dt = (now - last) / 1000; last = now; simT += dt * tScale;
      gl.uniform1f(uT, simT); gl.uniform2f(uR, canvas.width, canvas.height);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    function draw() { frame(performance.now()); glReq = requestAnimationFrame(draw); }
    function start() { if (!glReq && !reduced()) { last = performance.now(); draw(); } }
    function stop() { if (glReq) { cancelAnimationFrame(glReq); glReq = null; } }
    glStop = stop;
    // single static frame for reduced-motion, then never loop
    if (reduced()) { frame(performance.now()); return; }
    // gate on hero visibility + tab visibility (biggest perf win)
    var hero = canvas.closest('.hero') || canvas;
    var vis = true, onscreen = true;
    var io = new IntersectionObserver(function (ents) { onscreen = ents[0].isIntersecting; (vis && onscreen) ? start() : stop(); }, { threshold: 0.02 });
    io.observe(hero);
    document.addEventListener('visibilitychange', function () { vis = !document.hidden; (vis && onscreen) ? start() : stop(); });
    start();
    // scrubbed exit: slow the gradient + parallax as hero leaves (GSAP optional)
    if (gsap && ST && finePointer) {
      gsap.to({}, {}); // ensure gsap live
      ST.create({
        trigger: hero, start: 'top top', end: 'bottom top', scrub: true,
        onUpdate: function (self) { tScale = 1 - self.progress * 0.65; gsap.set(canvas, { yPercent: -self.progress * 18 }); }
      });
    }
  }

  /* ─────────────────────────── COUNT-UP STATS ─────────────────────────── */
  var NUM_RE = /^(\d{1,3}(?:[  ]\d{3})+|\d+)([.,]\d+)?$/; // 8 · 2025 · 35 000 · 6.7
  function initCounters() {
    if (reduced() || !gsap) return;
    var sel = '[data-count], .hs-v, .as-v, .cs-v, .ci-v, .ci-stats b, .p-price, .stat-num';
    var groups = [];
    $$(sel).forEach(function (el) {
      var raw = (el.getAttribute('data-count') || el.textContent).trim();
      // split a trailing unit (₽, %, нед, etc.) from the numeric head
      var m = raw.match(/^([\d   .,]+)(\s*\S.*)?$/);
      if (!m) return;
      var numStr = m[1].trim(), suffix = (m[2] || '');
      if (!NUM_RE.test(numStr)) return;
      var decimals = /[.,]/.test(numStr) ? (numStr.split(/[.,]/)[1] || '').length : 0;
      var target = parseFloat(numStr.replace(/[  ]/g, '').replace(',', '.'));
      if (!isFinite(target) || target === 0) return;
      el.__mo = { target: target, decimals: decimals, suffix: suffix, finalText: raw };
      groups.push(el);
    });
    if (!groups.length) return;
    function fmt(v, d) { return new Intl.NumberFormat('ru-RU', { minimumFractionDigits: d, maximumFractionDigits: d }).format(v); }
    groups.forEach(function (el) {
      ST.create({
        trigger: el, start: 'top 85%', once: true,
        onEnter: function () {
          var o = { v: 0 }, info = el.__mo;
          gsap.to(o, {
            v: info.target, duration: 1.1, ease: 'power3.out',
            onUpdate: function () { el.textContent = fmt(info.decimals ? o.v : Math.round(o.v), info.decimals) + info.suffix; },
            onComplete: function () { el.textContent = info.finalText; } // exact original text restored
          });
        }
      });
    });
  }

  /* ─────────────────────────── MAGNETIC CTAs ─────────────────────────── */
  function initMagnetic() {
    if (reduced() || !gsap || !finePointer) return;
    $$('.btn, .nav-btn, .pdeck-cta, .cc-link, .ci-link').forEach(function (el) {
      var strength = el.classList.contains('cc-link') || el.classList.contains('ci-link') ? 6 : 10;
      var qx = gsap.quickTo(el, 'x', { duration: 0.4, ease: 'power3' });
      var qy = gsap.quickTo(el, 'y', { duration: 0.4, ease: 'power3' });
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        qx((e.clientX - (r.left + r.width / 2)) / (r.width / 2) * strength);
        qy((e.clientY - (r.top + r.height / 2)) / (r.height / 2) * strength);
      });
      el.addEventListener('pointerleave', function () { gsap.to(el, { x: 0, y: 0, duration: 0.6, ease: 'elastic.out(1,0.5)' }); });
    });
  }

  /* ─────────────────────────── SPLIT-TEXT HERO ─────────────────────────── */
  function splitHero() {
    if (reduced()) return;
    var h = $('.h-name'); if (!h) return;
    if (h.querySelector('.h-letter') || h.querySelector('.mo-char')) return; // index already split — skip
    // preserve forced <br> line breaks (e.g. "SEO-<br>ПРОДВИЖЕНИЕ")
    var lines = h.innerHTML.split(/<br\s*\/?>/i)
      .map(function (s) { return s.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim(); })
      .filter(function (s) { return s.length; });
    if (!lines.length) return;
    h.textContent = '';
    h.classList.add('mo-split');
    var di = 0;
    lines.forEach(function (line, li) {
      var words = line.split(' ');
      words.forEach(function (word, wi) {
        // break opportunities after hyphen/dot/dashes inside a long word
        var chunks = word.split(/(?<=[-.–—])/);
        chunks.forEach(function (chunk, ci) {
          if (!chunk) return;
          var w = document.createElement('span'); w.className = 'mo-word';
          Array.from(chunk).forEach(function (ch) {
            var c = document.createElement('span'); c.className = 'mo-char'; c.textContent = ch;
            c.style.setProperty('--d', (di * 0.04) + 's'); di++;
            w.appendChild(c);
          });
          h.appendChild(w);
          if (ci < chunks.length - 1) h.appendChild(document.createElement('wbr'));
        });
        if (wi < words.length - 1) h.appendChild(document.createTextNode(' '));
      });
      if (li < lines.length - 1) h.appendChild(document.createElement('br'));
    });
    function fit() {
      // shrink-to-fit so an over-wide unbreakable word can never overflow the hero
      h.style.fontSize = '';
      var guard = 0;
      while (h.scrollWidth > h.clientWidth + 1 && guard < 40) {
        var cs = parseFloat(getComputedStyle(h).fontSize); if (!cs) break;
        h.style.fontSize = (cs * 0.96) + 'px'; guard++;
      }
    }
    // visibility never depends on font-load (which can hang); reveal immediately, fit repeatedly
    requestAnimationFrame(function () { fit(); h.classList.add('mo-in'); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit).catch(function () {});
    window.addEventListener('load', fit);
    setTimeout(fit, 700);
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(fit, 200); });
  }

  /* ─────────────────────────── DISP CTA SPLIT-LINE ─────────────────────────── */
  function initDisp() {
    if (reduced() || !gsap || !ST) return;
    var disp = $('.cta-sec .disp'); if (!disp) return;
    var spans = $$('span', disp);
    if (spans.length < 2) return; // pages using <br> keep the plain reveal
    gsap.set(spans[0], { xPercent: -8, autoAlpha: 0 });
    gsap.set(spans[1], { xPercent: 8, autoAlpha: 0 });
    ST.create({
      trigger: disp, start: 'top 80%', once: true,
      onEnter: function () {
        gsap.to(spans[0], { xPercent: 0, autoAlpha: 1, duration: 0.9, ease: 'expo.out' });
        gsap.to(spans[1], { xPercent: 0, autoAlpha: 1, duration: 0.9, ease: 'expo.out', delay: 0.08 });
      }
    });
  }

  /* ─────────────────────────── VELOCITY MARQUEE ─────────────────────────── */
  function initMarquee() {
    var wrap = $('.marquee-wrap'), track = $('.marquee-track');
    if (!wrap || !track) return;
    wrap.classList.add('mo-spot');
    if (reduced() || !lenis) return;
    var base = 1;
    lenis.on('scroll', function (e) {
      var v = Math.min(Math.abs(e.velocity || 0) / 10, 3);
      track.style.animationDuration = (32 / (base + v)) + 's';
      track.style.transform = ''; // let CSS animation own transform
    });
  }

  /* ─────────────────────────── SMOOTH SCROLL (Lenis) ─────────────────────────── */
  function initLenis() {
    if (reduced() || lowPower || !LenisCtor) return;
    lenis = new LenisCtor({ lerp: 0.09, wheelMultiplier: 1, smoothWheel: true, smoothTouch: false });
    if (gsap && gsap.ticker) {
      gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
      gsap.ticker.lagSmoothing(0);
      if (ST) lenis.on('scroll', ST.update);
    } else {
      function raf(t) { lenis.raf(t); requestAnimationFrame(raf); } requestAnimationFrame(raf);
    }
    // route in-page anchors through Lenis, clearing the 64px fixed nav
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href'); if (id.length < 2) return;
        var t = document.querySelector(id); if (!t) return;
        e.preventDefault(); lenis.scrollTo(t, { offset: -64 });
      });
    });
  }

  /* ─────────────────────────── PAGE TRANSITION ─────────────────────────── */
  function initPageTransition() {
    if (reduced()) return;
    function isInternal(a) {
      if (!a || !a.href) return false;
      if (a.target === '_blank' || a.hasAttribute('download')) return false;
      var href = a.getAttribute('href') || '';
      if (/^(#|mailto:|tel:|javascript:)/.test(href)) return false;
      return a.origin === location.origin;
    }
    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest && e.target.closest('a'); if (!isInternal(a)) return;
      if (a.pathname === location.pathname) return; // same page anchor handled by Lenis
      e.preventDefault();
      document.body.classList.add('mo-fade-out'); // opacity-only fade (keeps fixed nav/logo steady)
      setTimeout(function () { window.location.href = a.href; }, 280);
    });
    window.addEventListener('pageshow', function (ev) { if (ev.persisted) document.body.classList.remove('mo-fade-out'); });
  }

  /* ─────────────── LEAD MODAL (overlay form -> /api/send) ─────────────── */
  function initLeadForm() {
    if ($('#leadModal')) return;
    var m = document.createElement('div');
    m.className = 'lead-modal'; m.id = 'leadModal';
    m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true');
    m.setAttribute('aria-label', 'Обсудить проект'); m.setAttribute('aria-hidden', 'true');
    m.innerHTML =
      '<div class="lm-backdrop" data-lead-close></div>' +
      '<div class="lm-card">' +
        '<button class="lm-close" type="button" data-lead-close aria-label="Закрыть">&times;</button>' +
        '<div class="lm-title">Обсудим проект</div>' +
        '<div class="lm-sub">Оставьте контакты — перезвоним, подберём направление и посчитаем стоимость. Без обязательств.</div>' +
        '<form class="lm-form" id="leadForm" novalidate>' +
          '<input class="lm-input" name="name" placeholder="Ваше имя" autocomplete="name" required>' +
          '<input class="lm-input" name="phone" type="tel" inputmode="tel" placeholder="Телефон" autocomplete="tel" required>' +
          '<textarea class="lm-input" name="message" rows="3" placeholder="Кратко о задаче (необязательно)"></textarea>' +
          '<button class="lm-submit lf-submit" type="submit">Отправить заявку</button>' +
          '<div class="lm-status" id="lmStatus"></div>' +
        '</form>' +
      '</div>';
    document.body.appendChild(m);
    var card = m.querySelector('.lm-card');
    var form = m.querySelector('#leadForm'), status = m.querySelector('#lmStatus');
    var els = form.elements, lastFocus = null;
    function open(prefill) {
      lastFocus = document.activeElement;
      if (prefill && els['message'] && !els['message'].value) els['message'].value = prefill;
      m.classList.add('open'); m.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden';
      setTimeout(function () { try { els['name'].focus(); } catch (e) {} }, 60);
    }
    function close() { m.classList.remove('open'); m.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; if (lastFocus) try { lastFocus.focus(); } catch (e) {} }
    window.__openLead = open;
    m.addEventListener('click', function (e) { if (e.target.hasAttribute && e.target.hasAttribute('data-lead-close')) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && m.classList.contains('open')) close(); });
    // triggers (capture phase so it beats page-transition + magnetic): nav CTA, pricing CTA, [data-lead]
    document.addEventListener('click', function (e) {
      var t = e.target.closest && e.target.closest('.nav-btn, .pdeck-cta, [data-lead]');
      if (!t) return;
      e.preventDefault(); e.stopPropagation();
      var pre = '';
      var pc = t.closest && t.closest('.pdeck-card');
      if (pc) { var tier = pc.querySelector('.pdeck-tier'); if (tier) pre = 'Интересует тариф «' + tier.textContent.trim() + '»'; }
      open(pre);
    }, true);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (els['name'].value || '').trim(), phone = (els['phone'].value || '').trim(), msg = (els['message'].value || '').trim();
      if (!name || !phone) { status.className = 'lm-status err'; status.textContent = 'Заполните имя и телефон'; return; }
      var btn = form.querySelector('.lm-submit'), old = btn.textContent;
      btn.disabled = true; btn.textContent = 'Отправляем…'; status.className = 'lm-status'; status.textContent = '';
      fetch('/api/send', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: name, phone: phone, message: msg }) })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d && d.ok) {
            card.innerHTML = '<button class="lm-close" type="button" data-lead-close aria-label="Закрыть">&times;</button>' +
              '<div class="lm-ok"><div class="lm-ok-ic">✓</div><div class="lm-ok-t">Заявка отправлена</div><div class="lm-ok-s">Спасибо! Свяжемся с вами в ближайшее время.</div></div>';
          } else { btn.disabled = false; btn.textContent = old; status.className = 'lm-status err'; status.textContent = (d && d.error) || 'Не отправилось. Позвоните: +7 995 870-22-27'; }
        })
        .catch(function () { btn.disabled = false; btn.textContent = old; status.className = 'lm-status err'; status.textContent = 'Сеть недоступна. Позвоните: +7 995 870-22-27'; });
    });
  }

  /* ─────────────────────────── SCROLL PROGRESS BAR ─────────────────────────── */
  function initProgress() {
    if (reduced()) return;
    var bar = document.createElement('div'); bar.className = 'mo-progress'; document.body.appendChild(bar);
    function upd() {
      var st = window.scrollY || document.documentElement.scrollTop;
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(st / h * 100, 100) : 0) + '%';
    }
    if (lenis) lenis.on('scroll', upd); else window.addEventListener('scroll', upd, { passive: true });
    window.addEventListener('resize', upd); upd();
  }

  /* ─────────────────────────── A11Y: skip link ─────────────────────────── */
  function initSkipLink() {
    if ($('.mo-skip')) return;
    var nav = $('nav'); var main = $('section') || $('main');
    if (main && !main.id) main.id = 'main';
    var a = document.createElement('a');
    a.className = 'mo-skip'; a.href = '#' + (main ? main.id : 'main'); a.textContent = 'К содержимому';
    a.style.cssText = 'position:fixed;top:8px;left:8px;z-index:1000;background:#fff;color:#0a0a0a;padding:8px 14px;font-size:12px;font-weight:700;transform:translateY(-150%);transition:transform .2s';
    a.addEventListener('focus', function () { a.style.transform = 'none'; });
    a.addEventListener('blur', function () { a.style.transform = 'translateY(-150%)'; });
    document.body.insertBefore(a, document.body.firstChild);
  }

  /* ─────────────────────────── BOOT ─────────────────────────── */
  function boot() {
    if (gsap && ST) { gsap.registerPlugin(ST); }
    safe('reveals', initReveals);
    safe('texture', initTexture);
    safe('burger', initBurger);
    safe('chat', initChat);
    safe('heroGL', initHeroGL);
    safe('lenis', initLenis);
    safe('counters', initCounters);
    safe('magnetic', initMagnetic);
    safe('splitHero', splitHero);
    safe('disp', initDisp);
    safe('marquee', initMarquee);
    safe('pageTransition', initPageTransition);
    safe('leadForm', initLeadForm);
    safe('progress', initProgress);
    safe('skipLink', initSkipLink);
    if (ST) ST.refresh();
  }

  // react to OS reduced-motion toggle without reload
  mqReduce.addEventListener('change', function () {
    if (reduced()) {
      if (glStop) glStop();
      if (lenis) { try { lenis.destroy(); } catch (e) {} lenis = null; }
      $$('.reveal, .reveal-left, .stagger').forEach(function (el) { el.classList.add('visible'); });
    }
  });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
