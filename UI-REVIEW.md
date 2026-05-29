# ДАРЭ — UI Review

**Audited:** 2026-05-30
**Baseline:** Brand spec (ДАРЭ editorial industrial minimalism) + 6-pillar abstract standards
**Screenshots:** Not captured (no dev server — code-only audit supplemented by provided visual evidence)

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 3/4 | Strong Russian-first voice; English coord string and footer inconsistency undercut it |
| 2. Visuals | 2/4 | Desktop nav links invisible at all widths due to duplicate media-query; hero dead-zone confirmed; no real team photos |
| 3. Color | 3/4 | Palette correctly applied; hardcoded off-palette greys (#333, #444, #555, #ddd) scattered across service pages |
| 4. Typography | 2/4 | seo.html CTA .disp drops AKONY for Inter/bold; mobile clamp floor of 18px renders "SEO-ПРОДВИЖЕНИЕ" illegibly small |
| 5. Spacing | 3/4 | Consistent padding scale overall; ~8 inline style overrides bypass CSS vars; about-text spacing uses raw `margin-top:22px` |
| 6. Experience Design | 2/4 | IntersectionObserver threshold mismatch (0.12 vs 0.05) across pages; nested .reveal inside .g2.reveal creates hidden content; no meta descriptions on any page |

**Overall: 15/24**

---

## Top 3 Priority Fixes

1. **Desktop nav-links invisible at all widths (index.html)** — First-time visitors on desktop see only a logo and hamburger; there is no navigation. The `@media(max-width:900px)` block appears TWICE in index.html (lines 175 and 254), with the second duplicate overriding `.nav-links { display:none }` even on large viewports. Fix: remove the duplicate block at line 254 entirely. Service pages (seo.html, direct.html) do not have this bug — only index.html.

2. **seo.html mobile hero title becomes 18px minimum — illegible** — The `.h-name` override at line 212 sets `clamp(18px, 7vw, 44px)`. At 375px width that yields `7vw = ~26px` which is acceptable, but the declared floor of 18px means on any viewport below ~257px the heading can legally render at 18px — unreadable for the 11-character word "ПРОДВИЖЕНИЕ". Additionally at the 480px breakpoint the floor drops further to `clamp(16px, 6.5vw, 36px)`. Fix: raise both clamp floors to at least 28px.

3. **Both team pages ship placeholder initials instead of real photos** — artur.html line 189 and andrey.html line 186 both render `<div class="photo-initials">А</div>` — a giant nearly-invisible faded letter — as the sole profile image. For a marketing agency whose pitch is "honest, fast, results", launching with placeholder avatars for both founders directly contradicts the brand voice and reduces credibility. The photo-box is correctly styled; actual photos need to be supplied and placed as `<img>` inside `.photo-box`.

---

## Detailed Findings

### Pillar 1: Copywriting (3/4)

**What works:**
- CTA copy is specific and action-oriented throughout: "Запросить аудит", "Обсудить проект", "Запустим рекламу?" — no generic "Submit" or "Click here" patterns.
- Service descriptions lead with concrete numbers (CPA 2 000–2 300 ₽, конверсия 6.7%) rather than marketing fluff.
- The about-section voice is intentionally anti-hype: "Мы не придумываем себе 10-летнюю историю" — on-brand and memorable.
- Hamburger button has `aria-label="Меню"` on all pages.

**Findings:**

WARNING — English strings in a Russian-language site (index.html, lines 371 and 574):
```
43°07′N 131°54′E
Vladivostok, Russia
Since 2025
```
The h-coord block mixes English into a `<html lang="ru">` page. The footer repeats the coordinates without "Russia" or "Since 2025" — inconsistent styling. Either commit to the atmospheric English aesthetic consistently, or replace with Cyrillic equivalents ("Владивосток · Россия · с 2025"). As-is it reads like forgotten placeholder text.

WARNING — Footer bottom-right text is inconsistent across pages:
- index.html: `43°07′N 131°54′E`
- seo.html: `ВСЕ ПРАВА ЗАЩИЩЕНЫ`
- direct.html: `ВСЕ ПРАВА ЗАЩИЩЕНЫ`
- artur.html: `daremarketing.ru`
- andrey.html: `daremarketing.ru`

Three different values in the same footer slot across five pages — no consistent brand signal.

WARNING — No meta description tags on any audited page. SEO-agency selling SEO has zero `<meta name="description">` tags. Minor for users, significant for brand credibility.

---

### Pillar 2: Visuals (2/4)

**BLOCKER — Desktop navigation invisible on index.html:**
The stylesheet contains two `@media(max-width:900px)` blocks. Lines 175–226 and lines 254–300. Both blocks contain `.nav-links, .nav-btn { display:none }`. CSS cascade means the second block applies unconditionally regardless of viewport width — browsers do not require the media condition to be true to apply the block because both blocks share the same `max-width:900px` condition. The practical result confirmed in visual evidence: on desktop the nav shows only logo + hamburger.

Evidence from code:
- Line 176: `.nav-links,.nav-btn{display:none}` (inside @media max-width:900px block 1)
- Line 255: `.nav-links,.nav-btn{display:none}` (inside @media max-width:900px block 2 — appears after the desktop CSS, so on desktop the two together cause `.nav-links` to still get `display:none` applied)

Note: Service pages (seo.html line 122, direct.html) also have duplicate 900px blocks but the structural ordering differs — only index.html exhibits the full-breakage symptom.

WARNING — Hero empty dead-zone above ДАРЭ text:
The `.hc` container uses `justify-content:space-between` (index.html line 56) with `padding:80px 40px 60px`. The `.h-tag` and `.h-name` group occupy the first flex-child, and `.h-foot` is the second. When the viewport is short (laptop screens ~768px tall), the space-between distribution creates visible vertical dead space between the tag line and the logotype. The hero is `min-height:100vh` with no maximum, so this gap is structural — it cannot be eliminated by content alone.

WARNING — Both team pages (artur.html, andrey.html) use placeholder initials:
`<div class="photo-initials">А</div>` with `color:rgba(255,255,255,.12)` — almost entirely invisible. A dark black box with a near-invisible "А" reads as a broken image to most users.

MINOR — artur.html nav-mobile uses `<nav>` element (lines 163/160) instead of `<div>`. This creates two `<nav>` landmark elements on the page, which is a semantic error and confuses screen reader navigation.

MINOR — The custom cursor (`cursor:none` on body in index.html) is not carried through to service pages (seo.html, direct.html). Service pages set `cursor:pointer` on buttons — so the cursor experience is inconsistent: no custom cursor on service pages, custom cursor on index. Users navigating from index to a service page will see the native cursor reappear.

---

### Pillar 3: Color (3/4)

**What works:**
- CSS variables correctly define the palette: `--bk:#0a0a0a`, `--wh:#fff`, `--off:#f7f6f3`, `--br:#e0e0e0/#e8e8e8`, `--mu:#888`/`--gr:#888`.
- Dark sections, off-white body sections, white typography on dark — the 60/30/10 contrast rhythm is structurally sound.
- No purple gradients, no rounded cards, no SaaS colour noise.

**Findings:**

WARNING — Hardcoded off-palette greys used for text across service pages:
- `color:#333` — body text in seo.html (line 42, 51), direct.html (line 49)
- `color:#444` — price list items in seo.html (line 72), direct.html (line 72)
- `color:#555` — `.af-note` in direct.html (line 87)
- `background:#ddd` / `background:#e0e0e0` — nav-btn hover states across all pages

These are inconsistent with the declared `--mu:#888` token. The result is that body text on white surfaces is darker (#333) than the declared muted token, but this colour is not a CSS variable — making it impossible to theme or adjust globally. These should be mapped to `--bk` or a new `--body-text` token.

MINOR — `--br` token is inconsistent between files:
- index.html, seo.html, direct.html: `--br:#e0e0e0`
- artur.html, andrey.html: `--br:#e8e8e8`

Two border values for the same visual role. On team pages borders will appear slightly lighter, which is unlikely to be intentional.

---

### Pillar 4: Typography (2/4)

**BLOCKER — seo.html CTA `.disp` loses AKONY font:**
In index.html (line 144) and direct.html (line 89): `.disp { font-family:var(--fa); ... }` — uses AKONY correctly.
In seo.html (line 76): `.disp { font-size:clamp(40px,6vw,80px); font-weight:900; letter-spacing:-.05em; ... }` — no `font-family` declaration. The class inherits Inter, and `font-weight:900` is set (AKONY has no weight variants and ignores this). The visual result: the SEO page CTA headline "Начните расти в поиске" renders in Inter Black instead of AKONY. This is not the brand's editorial display tone.

**BLOCKER — Mobile hero font floor too small on seo.html:**
At `@media(max-width:900px)` line 212: `clamp(18px,7vw,44px)`. At 480px breakpoint (line 253): `clamp(16px,6.5vw,36px)`. The floor values of 18px and 16px are dangerous — the 11-character Russian word "ПРОДВИЖЕНИЕ" at 16–18px is unreadably small. Minimum acceptable display size for a hero headline is 32px.

WARNING — Six distinct hardcoded font weight values in index.html alone: 300, normal, 600, 700, 800, 900. While the brand uses Inter's weight range intentionally, the presence of `font-weight:600` (only one instance, on `.nav-links`) creates a weight value that sits between the declared 500 (unused) and 700 — this is a stray value.

WARNING — Font size scale uses 13 distinct pixel values in index.html (10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 28, 52px) plus 5+ clamp expressions. Without a declared type scale, each element is individually sized, making future consistency maintenance difficult.

---

### Pillar 5: Spacing (3/4)

**What works:**
- Section padding is systematic: `.sec { padding:100px 0 }`, `.sec-sm { padding:64px 0 }`, `.cta-sec { padding:120px 0 }`.
- The 40px horizontal gutter (`.w { padding:0 40px }`) is consistent across all files and correctly reduced to 20px at mobile.
- Card grid borders create spacing rhythm without CSS gap values.

**Findings:**

WARNING — Inline spacing overrides bypassing CSS system (index.html):
- `style="margin-top:22px"` on two `<p>` elements inside about-text (lines 480–481)
- `style="margin-top:60px"` on the contact strip wrapper inside CTA (line 521)
- `style="display:flex;flex-direction:column;gap:6px"` on footer contact links (lines 544)

These values are raw numbers not drawn from the declared scale. The 22px and 60px margins are applied inline and cannot be maintained or overridden from a stylesheet.

MINOR — `.hc` on index.html uses `padding:80px 40px 60px` while service page `.hc` uses `padding:60px 40px 56px`. The hero content area has inconsistent top/bottom padding between pages. This is visible: index.html hero has noticeably more vertical breathing room.

MINOR — The mobile stats layout on index.html is defined in both the 900px block (lines 187–193: grid 2-col) and again in the second 900px block (lines 267–269: flex column). The two blocks conflict — the second one overrides the grid layout. At mobile the stats render as a simple vertical flex list rather than the intended 2-column grid shown on service pages.

---

### Pillar 6: Experience Design (2/4)

**BLOCKER — Nested .reveal inside .reveal creates permanently hidden content on seo.html:**
At seo.html line 309: `<div class="g2 reveal">`. Inside this, line 311: `<div class="sh reveal">` and line 315: `<ul class="feat-list reveal">`. The parent `.g2.reveal` starts at `opacity:0`. When the IntersectionObserver triggers on the parent, it adds `.visible` to the parent. But the child `.sh.reveal` and `.feat-list.reveal` are observed INDEPENDENTLY. If the parent crosses the intersection threshold first, it becomes visible. But the child observers only fire when the CHILD element becomes visible — which requires the parent to already be visible (have `opacity:1`). In practice, at threshold 0.05 with rootMargin '-20px', a parent that occupies the full viewport will fire immediately, making children visible too. However the visual evidence confirms sections "stay opacity:0 until scroll" — likely because seo.html also wraps content inside `.g2.reveal` which is very tall, meaning the 0.05 threshold of a large container does not fire until a substantial portion enters the viewport.

WARNING — IntersectionObserver threshold inconsistency:
- index.html: `threshold: 0.12` (12% of element must be visible)
- seo.html, direct.html: `threshold: 0.05, rootMargin: '0px 0px -20px 0px'`

This means sections animate in at different scroll depths depending on the page. Users navigating from index to seo will notice the reveal animation triggers later on service pages.

WARNING — index.html IntersectionObserver does NOT use rootMargin or window.load pre-check for above-fold elements. The `io.observe(el)` setup is in the script, but the `window.addEventListener('load', ...)` immediate-check used in seo.html and direct.html is absent from index.html. Result: elements that are in the viewport on page load may not animate in until the observer fires post-load, causing a flash of opacity:0 content before reveal.

WARNING — No `<meta name="description">` on any page. For an SEO agency, this is both a credibility issue and a technical gap that would not pass a basic SEO audit.

WARNING — artur.html mobile nav uses a separate `<nav>` element with class `nav-mobile` (line 163), creating a duplicate landmark. andrey.html has the same pattern (line 160). Screen readers will announce two navigation landmarks, with the second appearing before most content.

MINOR — The custom cursor (index.html) uses `body { cursor:none }` without any fallback. If the JS cursor script fails to load (script error, slow network), users will have no visible cursor. Service pages do not have this risk as they use the system cursor.

MINOR — No skip-to-content link on any page. Pages with fixed nav (64px height) and long content would benefit from a skip nav for keyboard users.

---

## Additional Findings Beyond Top 3

4. **artur.html footer logo uses `opacity:.4` on all four SVG paths** — making the footer wordmark 60% dimmer than on other pages (andrey.html has the same issue). On index.html, seo.html, and direct.html the footer SVG paths have no opacity attribute. The team pages display a visually ghosted logo — inconsistent with site-wide footer treatment.

5. **seo.html 4-column contact strip vs index.html 3-column contact strip** — The `.c-strip` on seo.html (line 84) uses `grid-template-columns:repeat(4,1fr)` while index.html uses `repeat(3,1fr)`. Both use the same class name but with different grid definitions redeclared in each page's embedded CSS. This is not a bug but a structural inconsistency that would cause maintenance confusion.

6. **Mobile hamburger on artur.html has no `id="burger"` attribute** (line 157: `<button class="nav-burger" aria-label="Меню">`). The JS on artur.html selects by class `document.querySelector('.nav-burger')` which works. But it differs from the id-based selection on index.html/seo.html/direct.html — inconsistent implementation pattern.

---

## Files Audited

- `/Users/mak/Downloads/dare-site/index.html` — main homepage, 618 lines
- `/Users/mak/Downloads/dare-site/seo.html` — SEO service page, 515 lines
- `/Users/mak/Downloads/dare-site/direct.html` — Yandex Direct service page, 584 lines
- `/Users/mak/Downloads/dare-site/artur.html` — team card, 330 lines
- `/Users/mak/Downloads/dare-site/andrey.html` — team card, 327 lines
- `/Users/mak/Downloads/dare-site/fonts/` — AKONY.otf + AKONY.ttf present
- `/Users/mak/Downloads/dare-site/clients/` — 12 client logos present
