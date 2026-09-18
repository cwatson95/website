# Changelog — website

Per-project changelog (policy: Agent repo `CLAUDE.md` → "Per-project
changelogs"). Static hand-written site: no build step, no frameworks, opens
over `file://`. **Don't commit unasked** — delivery is uncommitted files in
the main checkout.

## Known-bad — do not reintroduce
- **A full-viewport overlay above an interactive canvas must set
  `pointer-events: none`** (re-enabling `auto` only on its interactive
  children). The teaching page shipped with the `.page` overlay (z-index 1,
  100vh) silently swallowing every pointer/wheel event — pan, zoom, and
  click-travel were dead while the canvas rendered fine. Fixed 2026-08-12 c.

## 2026-09-17 e — the preview draws to canvas, so a "save PDFs" browser cannot blank it

Cooper reported View still downloading the file and the viewer showing black.
Both come from one cause, and it is not the server: `curl -I` on
`https://cooper-watson.net/CV.pdf` returns `content-type: application/pdf`
with **no `Content-Disposition`, no CSP and no `X-Frame-Options`**, and the
deployed page was confirmed current. The browser is configured to save PDFs
rather than display them (Firefox: Applications -> PDF -> Save File; Chrome:
"Download PDFs instead of automatically opening them"). Under that setting an
`<iframe>` pointed at a PDF fires the download and renders nothing, so the
frame showed `--bg-1` through — the "black" box.

The `<iframe>` was therefore the wrong mechanism: correct for a default
browser, silently broken for anyone who has changed that preference. The
viewer now renders with **PDF.js onto `<canvas>`**, which never touches the
browser's PDF handler, so the preview behaves the same whatever the setting.
Pages render lazily via `IntersectionObserver` (600px margin) and closing the
viewer calls `pdf.destroy()`, so a 28-page article does not rasterise pages
nobody scrolled to. Page slots carry the first page's `aspect-ratio`, so the
scroll height is right before anything is drawn.

PDF.js 3.11.174 (UMD) loads from jsdelivr — the same CDN the modules browser
already uses for KaTeX — and is fetched only on the first View click. Verified
both URLs live (`pdf.min.js` 320 KB, `pdf.worker.min.js` 1.09 MB, HTTP 200) and
that the bundle assigns `window.pdfjsLib`, which is the entry point the script
uses. If the CDN is unreachable the viewer shows "Preview unavailable" plus a
working new-tab link rather than failing silently; with JavaScript off the
control is still a plain link to the PDF.

The dead `.doc-frame` / `.doc-fallback` rules are removed. Verified: both pages
tag-balanced (0 errors), `dev/check_links.py` green, no stale class references
left in either page or the stylesheet. **Could not check:** the rendering path
was not executed — no node/deno/browser here — so this is verified structurally
and against the live CDN, not visually.

Trade-off worth knowing: the preview now needs network access. Self-hosting
pdfjs-dist (~1.4 MB in the repo) would remove that if the CDN dependency is
unwanted.

Left uncommitted, per this changelog's header.

## 2026-09-17 d — "View PDF" opens the document in the page, not another copy of it

Two related complaints from Cooper: View and Download "appear to do the same
thing", and the CV page loaded its PDF viewer before anyone asked for it.

They were not literally identical — `download` saves the file, `target="_blank"`
opens a tab — but both just handed you the PDF, so the difference was invisible,
and a browser configured to save PDFs rather than display them makes them truly
identical. View now does something Download cannot: it builds an `<iframe>` into
an empty slot in the page and toggles to "Hide preview"; Download still saves.

New `pdf_view.js` (1.6 KB, no dependencies) delegates one click listener on the
document. The viewer is created on first click and **torn down on the second**,
so a nine-PDF page never fetches a document nobody opened — which is also the CV
fix: `cv.html`'s eager `<object>` is gone, replaced by the same empty
`<div class="doc-box" hidden>`.

Progressive enhancement: the control is still a plain link to the PDF with
`target="_blank"`, so with JavaScript off, or if the script 404s, it opens in a
new tab as before. Modified clicks (ctrl/cmd/shift/alt, middle button) are let
through untouched.

Verified: 8 viewer slots and 8 `js-view` links on research.html, 1 and 1 on
cv.html, every `data-target` resolves to a slot, all 9 PDF paths exist, **zero
eager `<object>`/`<iframe>` left in either page**, both tag-balanced (0 errors),
`dev/check_links.py` green. **Could not check:** the JS was not executed — no
node/deno on this machine — so the toggle is verified structurally, not at
runtime.

Left uncommitted, per this changelog's header.

## 2026-09-17 c — Research and CV pages are real: abstracts, view, download

Both pages were still the scaffolded placeholders ("Coming soon", and a TODO to
turn the CV badge into a real link). Cooper uploaded eight PDFs to
`my_articles/` and `CV.pdf` to the site root, so both are now filled in.

**Research.** One card per publication, newest first: title, author list with
Cooper's name marked, venue/volume/year, a DOI link, the abstract behind a
native `<details>` disclosure (no script), and *View PDF* / *Download* buttons.
Eight entries — PRA 113 063523 (2026), Fluct. Noise Lett. 25 2640002 (2026) and
its erratum, Symmetry 18 182 (2026), Universe 11 389 (2025), Symmetry 13 1469
(2021), Particles 3 642–659 (2020), Universe 6 11 (2020).

**CV.** An inline `<object>` preview of `CV.pdf` with a fallback paragraph for
browsers that will not render a PDF inline (most mobile ones), plus the same
View/Download pair and a link across to Research.

`style.css` gains one block at the end — `.pub-list`/`.pub`, the `details.abs`
disclosure, `.btn`/`.btn-row`, `.doc-frame` — in the existing azure palette, no
new colors and no webfonts.

Titles, authors, venues, DOIs and abstracts were **transcribed from the PDFs,
not recalled**: every DOI is the one printed in its own file. Two text repairs
were needed — the World Scientific files use a legacy encoding where `®`, `¯`
and `°` stand for *ff*, *fi* and *fl* (so "Kadano®–Baym" is Kadanoff–Baym), and
the Particles abstract lost an em dash in extraction ("four independent
curvature invariants—the Ricci scalar"). Verified: all 37 local links resolve,
both pages tag-balanced (0 errors), `dev/check_links.py` green.

The PDFs are ~15 MB total (largest `universe-06-00011-v2.pdf` at 8.45 MB, well
under the 100 MB file limit). Left uncommitted, per this changelog's header.

## 2026-09-17 b — the module browser is 14 pages, 3.8 MB (was one 29.7 MB page)

Regenerated with the generator's new split (modules changelog 2026-09-17 b):
`teaching_modules.html` is a ~30 KB index and each trunk is its own
`modules_<TRUNK>.html`, with figures referenced as lazily-loaded `<img>`
instead of inlined — they were 89% of the old page. Largest page is now
0.60 MB; NE went 7.44 MB -> 0.48 MB.

Old deep links are unaffected: the index forwards `#<id>` to the trunk page
that holds it, so the Teaching Network's "open module" links and any bookmark
keep working. `dev/check_links.py` passes here (270 sections over 13 trunk
pages, 143 netlinks); all 455 figure refs resolve.

**The 13 `modules_*.html` files are new and must be committed** or the index
will forward to pages that are not on the site. Left uncommitted, per this
changelog's header.

## 2026-09-17 a — the module browser's links now work on the deployed site

Every link out of `modules/teaching_modules.html` pointed at `../website/...`
— the six nav tabs and all 143 Teaching-Network back-links — which resolves to
`/website/...` here and 404s, because Pages serves the repo root and `modules/`
sits under it rather than beside it. The *inbound* links were never broken:
`../modules/teaching_modules.html` from a root page is clamped to
`/modules/...` per RFC 3986, so it lands correctly.

Regenerated with the generator's new `--deploy` flag (modules changelog
2026-09-17 a), so the links are now `../index.html`, `../teaching.html#CM-01`,
and so on. All six targets confirmed present at the repo root;
`dev/check_links.py` passes here (270 sections, 143 netlinks, all checks
passed). Added `.nojekyll`: nothing uses Jekyll and the site is 2,590 files,
so the build step is pure overhead.

Left uncommitted, per this changelog's header.

## 2026-09-16 c — The Standard Model from Symmetry joins the catalog, 60 sims

`standard_model.html` landed in `projects/simulations/` (simulations
changelog 2026-09-16 (h)): the gauge groups and their generators, one
generation with its anomalies, the Higgs potential and the masses, the
eightfold way with PDG 2026 masses, colour singlets and SU(6), and the
running couplings. A card in Atoms, Matter &amp; Light after Nuclear Clocks,
the lede and meta count moved to sixty, and the sim added to the completed
list at the bottom of `simulations/TODO.txt`; `dev/sync_sims.py` +
`dev/check_sims.py` green (60 sims, 60 copies, 60 cards).

## 2026-09-16 b — a WIP section at the bottom of the catalog

At Cooper's ask, `simulations.html` gets a last section titled WIP, and the
six sims he counts as work in progress move into it: Quaternions (from
Mathematics &amp; Machines) and the five SBS pages (from Scattering &amp;
Brillouin Physics) — `sbs_sims`, `sbs_axes_phase`, `sbs_gaslaw_manifold`,
`sbs_parent_law`, `sbs_state_surface`. The cards are moved byte-for-byte,
nothing else changes, and the count stays fifty-nine; `dev/check_sims.py`
green (59 sims, 59 copies, 59 cards). The same split is listed at the
bottom of `simulations/TODO.txt`. When one of these is finished, move its
card back to its subject section.

## 2026-09-16 a — Lagrange Points joins the catalog, 59 sims

`lagrange_points.html` landed in `projects/simulations/` (simulations
changelog 2026-09-16 (g)): the five points in the rotating frame, the
effective potential as a landscape, stability and Routh's limit, the SOHO
and JWST halos, the Queqiao halo and the Gateway NRHO, Jupiter's trojans and
the horseshoes. A card in Astrophysics &amp; Relativity after the
Ephemerides, the lede and meta count moved to fifty-nine, `dev/sync_sims.py`
+ `dev/check_sims.py` green (59 sims, 59 copies, 59 cards).

## 2026-09-15 e — Buoyancy joins the catalog, 58 sims

`buoyancy.html` landed in `projects/simulations/` (simulations changelog
2026-09-15 (d)): Archimedes' principle from the spring scale to the
metacentre, the golden crown, the Cartesian diver and the balloon. A card in
Fluids &amp; Flight, the lede and meta count moved to fifty-eight,
`dev/sync_sims.py` + `dev/check_sims.py` green (58 sims, 58 copies, 58 cards).

## 2026-09-15 d — Light Scattering: the sky from six worlds

`simulations/scattering.html` re-synced from `projects/simulations/` after its
BLUE SKY view was rebuilt (see the simulations changelog, 2026-09-15 (c)):
the sun's elevation runs from +90° to −18° through sunset and the three
twilights, and world chips switch the atmosphere between Earth, Earth without
ozone, Mars, Venus, Titan and the Moon. The Light Scattering card on
`simulations.html` now says so. `dev/sync_sims.py` + `dev/check_sims.py`
green; the copy differs from the source only by the two nav-href rewrites.

## 2026-09-15 b — the catalog catches up: eight new cards, 57 sims
### Changed
- simulations.html: eight sims that existed in projects/simulations/ but had
  no card — wave_fronts (uncarded since 2026-08-14), doppler_causality,
  pupil_plane_interferometry, sbs_state_surface, pascals_triangle, primes,
  and today's brachistochrone and cycloids — each get a card in their
  subject section, copy distilled from the sim's own header; the lede and
  meta description say fifty-seven. `dev/sync_sims.py` re-run: 57 copies in
  website/simulations/, the seven that were missing on the site now
  present, no dead cards, no uncarded sims.
- dev/check_sims.py (new): an INDEPENDENT check of the sync, sharing no
  code with sync_sims.py — copied set = source set, every copy byte-equal to
  its source apart from exactly the two documented nav-href rewrites, no
  un-rewritten href, nav targets intact, cards ↔ copies a bijection with no
  duplicates, the page tag-balanced, and the lede/meta count equal to the
  card count. Exit 1 on any problem; run it after every sync.
- projects/simulations/build_cycloid/land_site_cards.py: the idempotent
  card inserter used for this batch (anchor card + section, count words
  recomputed), so the same cards can be applied to any copy of the page.
### Verified
- check_sims.py: 57 sims, 57 copies, 57 cards, 0 problems — in the
  worktree and again against the main checkout after landing.

## 2026-09-15 c — arrival by deep link no longer clips the modules page header
### Changed
- dev/render_check/links_harness.js: the `modules` run now lays the sidebar
  out (trunk 30 px, topic 24 px, item 34 px, list 600 px tall) and checks
  that arriving by hash scrolls ONLY the list (never the page or the reading
  column), keeps the trunk heading in view when the item fits below it,
  clears a stale filter, pins the top again at `load`, and that a click
  nudges only an item that is out of view: 29 checks (was 20). The fix
  itself is in generate_webpage.py — modules changelog, same date.
### Verified
- check_links.py all green: 17 static checks, harness 28/28 (network),
  29/29 (modules).

## 2026-09-15 a — Teaching ↔ Modules: every orb opens its module, every module travels back
### Changed
- teaching.html + teaching_network.js: the panel gains an **open module**
  link (`../modules/teaching_modules.html#<id>`; a trunk hub says "browse
  the MA modules"; the CMx/QC stubs, which have no folders, show nothing).
  The page now answers deep links: `teaching.html#CM-22` glides from the
  whole sky to that orb on load, the URL follows your travel
  (`history.replaceState`, so Back still leaves the page), double-click fit
  clears it, and a hashchange travels. Two DOM-free helpers join the core,
  `nodeFromHash` / `moduleHref`. Drawing untouched: the four
  record_teaching.js display lists are byte-identical before and after.
- dev/build_network.py: bakes an 8th node field, has-module-page (folder
  `projects/modules/<TRUNK>/<ID>_*/` exists; a hub: any module in its
  trunk), so the link is offered only where a page exists, and warns when
  the network lists a module with no folder. **Rerun it when a module
  lands, not only when topic_network.txt changes.** Positions and edges
  unchanged.
- style.css: `.net-module`, plus a `[hidden]` guard inside the panel (an
  `inline-block` rule would otherwise defeat the `hidden` attribute).
- dev/check_links.py + dev/render_check/links_harness.js: the round-trip
  audit — flags ↔ folders ↔ module sections ↔ back-links (a bijection over
  the 143 module nodes; 10 hubs), teaching.html tag balance, and both
  pages' scripts driven headlessly under deno against stub DOMs (hash →
  orb, chip travel, hub/stub/garbage/empty hashes, double-click; hash →
  module for bare, `m-`-prefixed, trunk, Thermo and underscore ids, junk,
  sidebar click, lazy render). From projects/website/:
  `python3 dev/check_links.py`.
- The modules side (generate_webpage.py: hash routing + the per-module
  back-link) is in the modules changelog, same date.
### Verified
- check_links.py all green: 17 static checks, harness 28/28 (network) and
  20/20 (modules). Baked DATA: the first seven fields of all 155 nodes, all
  261 edges and the trunk names identical to before; flags 143/143 modules,
  10/12 hubs. Old-vs-new record_teaching.js frames: 4/4 `cmp` clean.
- Not verifiable here (no headless browser on this Mac): a real-browser
  pass. The glide-on-load and `replaceState` over `file://` are the two
  things worth a look.

## 2026-08-14 b — edits.txt: name, email, ORCID, CV link
### Changed
- Per Cooper's `edits.txt`: the homepage now says **Cooper K. Watson**
  (h1, title, meta description, footer); About's contact card switches the
  email to cooper_watson@tamu.edu and gains an ORCID link
  (0000-0001-8245-541X) and a link to the CV page. The CV file itself
  (cv.pdf) still doesn't exist — the link points at cv.html until it does.
### Verified
- Both pages tag-balanced (html.parser); mailto/ORCID/CV hrefs grepped at
  their destinations; other pages' name/footer deliberately unchanged
  (edits.txt says homepage).

## 2026-08-14 a — the whole catalog: all 49 simulations
### Changed
- simulations.html: the six launch cards become the full catalog — every
  sim in projects/simulations/ (49 today), grouped into eleven subject
  sections from Mechanics & Control to Mathematics & Machines, each
  description distilled from the sim's own header comment. The original
  six cards keep their copy.
- dev/sync_sims.py: the hand-kept SIMS list is gone. The script now
  discovers every top-level `*.html` in the source directory (finished
  sims land there by house rule, so discovery IS the catalog), copies all
  of them with the two nav-href rewrites, deletes stale copies whose
  source is gone, and audits simulations.html against the copied set —
  a card linking a missing sim is an ERROR, a copied sim with no card a
  WARNING. Adding a sim to the site is now: land the sim, add its card,
  rerun `python3 dev/sync_sims.py` from projects/website/.
- style.css: `.sim-catalog` section spacing for the grouped gallery.
### Verified
- Independent checker (not the sync script itself): all 49 copies are
  byte-equal to source-plus-exactly-the-two-documented-rewrites; no
  un-rewritten `../website/` or `../modules/` hrefs remain; every copy
  keeps its `../index.html` and `../../modules/` nav targets; card hrefs
  ↔ copied files is a bijection with no duplicate cards; simulations.html
  tag-balanced. Re-verified from the main checkout after landing.

## 2026-08-12 f — Modules tab in the site nav
### Changed
- All six pages' header nav gains **Modules** between Teaching and
  Simulations, pointing at `../modules/teaching_modules.html` (the generated
  modules browser; it marks itself current). The homepage hero pills are
  deliberately unchanged — Modules is a header tab only.
- `dev/sync_sims.py`: second rewrite for the in-site sim copies,
  `href="../modules/` → `href="../../modules/`; copies re-synced.
- Note: the Modules tab points one level OUTSIDE the site folder, so it is
  the one nav target that would need copying in (or dropping) if the folder
  is ever deployed alone; everything else stays self-contained.
### Verified
- Nav audit: 6/6 pages + 6/6 sim copies — full seven-tab order, correct
  Modules href per location, correct aria-current; target file exists.

## 2026-08-12 e — sims wear the site theme; sync rewrites nav hrefs
### Changed
- Every sim in projects/simulations/ now carries this site's background
  (`#070b18`) and the six-tab site nav — see the simulations changelog,
  2026-08-12 (d). In the source tree the tabs point at `../website/*.html`;
  `dev/sync_sims.py` now rewrites `href="../website/` → `href="../` while
  copying, so the six in-site copies navigate inside the self-contained site
  folder. Copies re-synced (their sha256s now differ from the source by
  exactly that rewrite).
### Verified
- All six copies: site-nav present, zero `../website/` hrefs left, every
  rewritten target (`../index.html` … `../cv.html`) exists; sims' selfTests
  green from the copied path.

## 2026-08-12 d — first six simulations on the site
### Added
- `simulations/` — the site's own copies of six sims from
  projects/simulations/ (orbitals, steam_carnot_cycle, lattice, ephemerides,
  synth, cart_pendulum), placed by `dev/sync_sims.py` so the site stays one
  self-contained folder (file:// now, static hosting later).
  **projects/simulations/ remains the source of truth** — after a sim changes
  there, rerun from projects/website/: `python3 dev/sync_sims.py`. To put
  another sim on the site: add it to SIMS in that script + a card in
  simulations.html.
- simulations.html: placeholder cards replaced by six whole-card launch links,
  descriptions distilled from each sim's own header comment; `a.card` hover
  styling in style.css.
- Note: the request said "lattics.html"; the actual file is `lattice.html`.
### Verified
- Tag balance on simulations.html; all six card hrefs resolve to the copied
  files; sync_sims.py prints size + sha256 per copy; main-checkout landing
  re-synced from the default source path and byte-compared clean.

## 2026-08-12 c — network interaction fix; blue void; homepage stars
### Fixed
- teaching.html ignored all mouse input (no pan, no zoom, no click-travel)
  while rendering fine. Root cause: the full-viewport `.page` overlay holding
  the nav and panel sits at z-index 1 above the canvas, so it received every
  pointer/wheel event and the canvas listeners never fired. Fix in style.css:
  `pointer-events: none` on the overlay, restored to `auto` on the nav links
  and the panel; plus `touch-action: none` on the canvas so touch drags pan
  the sky instead of scrolling the page. (See Known-bad.)
### Changed
- The void is now the site's dark blue (vertical gradient `#070b18 →
  `#04060c`, the other pages' background) instead of pure black; the black
  orbs now read as true black discs against it.
- Stars glimmer like the homepage: same size/alpha/twinkle parameters, same
  ice-blue `#9fd8ff`, occasional cross flares; parallax layers kept.
- Verified headlessly: overview frame pair differs (op counts 1101/1099,
  mean|diff| 0.02/255 — smooth twinkle), arrival frame diff 1.76/255; frames
  inspected for the blue gradient, star flares, and orb contrast.

## 2026-08-12 b — teaching network page
### Added
- `teaching.html` is now the network: an empty near-black void, sparse specks
  of light glimmering, every topic a small black orb outlined by a thin white
  halo. Data = `projects/modules/topic_network.txt` — 155 nodes (143 modules +
  12 trunk hubs), 261 edges (129 prerequisite-chain, 84 `~`cross-links, 38 KEY
  BRIDGES segments, 10 hub spokes) — baked into `teaching_network.js` by
  `dev/build_network.py`, so the page stays `file://` (nothing fetched).
  Constellation layout: hubs pinned on an affinity-ordered ring (big trunks
  interleaved with small), each trunk's chain wound as an arc-length spiral;
  cross-links/bridges render as long faint threads (bridges brighter). Click
  an orb to glide there; drag pans; wheel zooms about the cursor; double-click
  empty void fits the whole sky. Side panel lists the current topic and its
  links as travel buttons (bridge links first). `prefers-reduced-motion` gets
  static frames + instant travel; hidden tabs pause.
- `dev/build_network.py` — parser (trunk sections, module lines, `~` tags,
  KEY BRIDGES incl. wrapped lines; consecutive ids in a bridge become edges,
  `..` ranges contribute endpoints) + seeded constellation layout + DATA
  baking between AUTO-GENERATED markers; `--preview` renders the layout to a
  PNG. Rerun from `projects/website/` after editing topic_network.txt:
  `python3 dev/build_network.py`
- `dev/render_check/record_teaching.js`; `rasterise.py` gained arc + fillText.
### Verified
- Parse: 0 unresolved cross-links. Layout previewed: 12 separated clusters.
- Headless frames: overview pair differs in 115/161 speck alphas (glimmer),
  glide-mid and CM-22 arrival differ 2.3–3.2/255 (travel), orbs render as
  black discs + thin white rings; a synthwave frame re-rasterised unchanged
  as a regression check after the rasteriser upgrade.

## 2026-08-12 a — initial skeleton
### Added
- Six linked pages: `index.html` (homepage), `about.html`, `teaching.html`,
  `simulations.html`, `research.html`, `cv.html`, sharing `style.css` and a
  common top nav (`aria-current` marks the active page). Placeholder copy is
  tagged with `<!-- TODO -->` comments.
- `synthwave.js` — homepage background canvas. Layout after
  `watermarked_preview.mp4` (flat perspective floor grid scrolling slowly
  toward the viewer, wireframe mountains at the horizon, starfield sky);
  palette sampled from `example_wave.mp4` frames (sky `#123453→#173f65`, mesh
  ramp `#123a63→#0b5a94→#1089c4→#1bbeeb→#7deeff`), background pulled darker
  than the video per `README.md` ("soft dark violet/blue") — deliberately NOT
  the preview's magenta/orange. The ridge is a triangulated mesh whose heights
  drift through 2-octave value noise (~20 s features + slow swell), per
  `example_wave.mp4`. Deterministic (seeded PRNG / integer-hash noise), honors
  `prefers-reduced-motion` (static frame), pauses when the tab is hidden,
  devicePixelRatio-aware. Drawing core is DOM-free for headless verification.
- `dev/render_check/` — no headless browser on this Mac, so: `record_frames.js`
  (deno) loads `synthwave.js` with a stub 2D context and records display
  lists; `rasterise.py` (matplotlib) turns them into PNGs and prints
  frame-to-frame mean|diff| as the motion check. Regenerate with:
  `cd dev/render_check && deno run --allow-read --allow-write record_frames.js`
  `&& python3 rasterise.py out/frame_*.json`. PNG/JSON outputs are generated
  artifacts — don't commit them.
### Verified
- Frames rasterised at t = 0 / 2.5 / 5 / 7.5 s and inspected against the two
  reference videos; nonzero frame-to-frame diffs confirm the ridge undulates
  and the floor scrolls. Cross-links between all six pages checked by hand.
