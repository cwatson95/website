// links_harness.js — drive the Teaching ↔ Modules deep links without a browser.
//
// Two modes, one page each (both scripts hang listeners on globalThis, so
// they run in separate deno processes; dev/check_links.py runs both):
//   deno run --allow-read links_harness.js network [site_dir]
//   deno run --allow-read links_harness.js modules [site_dir] [modules_html]
// network: evals teaching_network.js against a stub DOM with #CM-22 in the
//   URL, then checks the panel's "open module" link, travel by chip click,
//   hashchange routing (module, hub, stub hub, garbage, empty), double-click
//   fit, and that the URL follows travel.
// modules: evals the inline script of the GENERATED teaching_modules.html
//   against a stub DOM built from its own sections and sidebar (the sidebar
//   gets a laid-out geometry: trunk 30 px, topic 24 px, item 34 px, list
//   600 px tall), then checks hash routing (#MA-02, #m-CM-22, #QM, #TD-1.1,
//   #MACRO_EM, junk), that only the sidebar list scrolls (never the page or
//   the reading column), trunk heading kept in view when it fits, lazy KaTeX
//   render, filter reset, and URL sync on a sidebar click.
// Exit status 1 on any failure.

const mode = Deno.args[0] || 'network';
const here = new URL('.', import.meta.url).pathname;
const site = (Deno.args[1] || here + '../..').replace(/\/$/, '');
const modHtml = Deno.args[2] || site + '/../modules/teaching_modules.html';

let fails = 0, passes = 0;
function check(cond, msg) {
  if (cond) { passes++; console.log('  ok    ' + msg); }
  else { fails++; console.log('  FAIL  ' + msg); }
}

/* ---- a browser-ish global: location + history stubs, window alias ---- */
const hist = [];
const loc = {
  hash: '', pathname: '/site/page.html', search: '',
  replace(url) { hist.push('replace ' + url); loc.hash = url.startsWith('#') && url !== '#' ? url : ''; }
};
function defineGlobal(name, value) {
  try { Object.defineProperty(globalThis, name, { value, configurable: true, writable: true }); }
  catch (e) { globalThis[name] = value; }
}
defineGlobal('location', loc);
defineGlobal('history', { replaceState(s, t, url) { hist.push(url); loc.hash = url.startsWith('#') ? url : ''; } });
defineGlobal('window', globalThis);
function setHashAndFire(h) { loc.hash = h; globalThis.dispatchEvent(new Event('hashchange')); }

function ctxStub() {
  const g = () => ({ addColorStop() {} });
  return { set fillStyle(v) {}, set strokeStyle(v) {}, set lineWidth(v) {}, set font(v) {},
    set textAlign(v) {}, set textBaseline(v) {}, setTransform() {}, beginPath() {}, moveTo() {},
    lineTo() {}, arc() {}, fill() {}, stroke() {}, fillRect() {}, fillText() {},
    createLinearGradient: g, createRadialGradient: g };
}

class El {
  constructor(tag, id) {
    this.tagName = tag; this.id = id || ''; this._text = ''; this.title = '';
    this.className = ''; this.type = ''; this.hidden = false; this.href = '';
    this.style = {}; this.children = []; this.listeners = {}; this.dataset = {};
    this.scrollTop = 0; this.scrolled = []; this.width = 0; this.height = 0;
    this.previousElementSibling = null; this.value = '';
    this.classes = new Set();
    const self = this;
    this.classList = {
      toggle(c, force) {
        const on = force === undefined ? !self.classes.has(c) : !!force;
        if (on) self.classes.add(c); else self.classes.delete(c);
        return on;
      },
      contains(c) { return self.classes.has(c); },
      add(c) { self.classes.add(c); },
      remove(c) { self.classes.delete(c); }
    };
  }
  get textContent() { return this._text; }
  set textContent(v) { this._text = String(v); if (v === '') this.children = []; }
  addEventListener(t, f) { (this.listeners[t] = this.listeners[t] || []).push(f); }
  fire(t, ev) { for (const f of (this.listeners[t] || [])) f(ev || {}); }
  dispatchEvent(ev) { this.fire(ev.type, { type: ev.type, target: this }); return true; }
  appendChild(c) { this.children.push(c); return c; }
  removeAttribute(n) { if (n === 'href') this.href = ''; }
  scrollIntoView(o) { this.scrolled.push(o); }
  getBoundingClientRect() { return { top: 0, height: 0 }; }
  getContext() { return ctxStub(); }
  setPointerCapture() {}
}

if (mode === 'network') {
  const src = await Deno.readTextFile(site + '/teaching_network.js');
  const ids = {};
  for (const [tag, id] of [['canvas', 'net'], ['h2', 'net-title'], ['p', 'net-sub'],
                           ['div', 'net-links'], ['a', 'net-module']]) ids[id] = new El(tag, id);
  ids['net-module'].hidden = true;
  defineGlobal('document', {
    getElementById: (i) => ids[i] || null, createElement: (t) => new El(t),
    addEventListener() {}, readyState: 'complete', hidden: false
  });
  defineGlobal('requestAnimationFrame', () => 1);   // the loop never ticks: t stays 0
  defineGlobal('cancelAnimationFrame', () => {});
  defineGlobal('innerWidth', 1280); defineGlobal('innerHeight', 720);
  defineGlobal('devicePixelRatio', 1);
  defineGlobal('matchMedia', () => ({ matches: false }));

  loc.hash = '#CM-22';
  (0, eval)(src);                                  // boot() runs here, hash in the URL
  const TN = globalThis.TeachingNetwork;
  check(!!TN, 'teaching_network.js defines TeachingNetwork');

  // the DOM-free helpers, on a fresh state
  const st = TN.createState(1280, 720, 20260812);
  const cm22 = st.byId['CM-22'];
  check(TN.nodeFromHash(st, '#CM-22') === cm22, 'nodeFromHash: #CM-22 -> CM-22');
  check(TN.nodeFromHash(st, '#%43M-22') === cm22, 'nodeFromHash decodes %43M-22');
  check(TN.nodeFromHash(st, 'CM-22') === cm22, 'nodeFromHash accepts a bare id');
  check(TN.nodeFromHash(st, '') === -1 && TN.nodeFromHash(st, '#') === -1 &&
        TN.nodeFromHash(st, undefined) === -1, 'nodeFromHash: empty / undefined -> -1');
  check(TN.nodeFromHash(st, '#constructor') === -1 && TN.nodeFromHash(st, '#nope-99') === -1,
        'nodeFromHash: unknown / prototype names -> -1');
  check(TN.nodeFromHash(st, '#%E0%A4%A') === -1, 'nodeFromHash survives a malformed escape');
  check(TN.moduleHref(st.nodes[cm22]) === '../modules/teaching_modules.html#CM-22', 'moduleHref(CM-22)');
  check(TN.moduleHref(st.nodes[st.byId['MA']]) === '../modules/teaching_modules.html#MA', 'moduleHref(MA hub)');
  check(TN.moduleHref(st.nodes[st.byId['CMx']]) === '' && TN.moduleHref(null) === '',
        'moduleHref: stub hub (no modules) and null -> empty');
  const nMod = st.nodes.filter(n => !n.hub).length;
  const nFlag = st.nodes.filter(n => !n.hub && n.mod).length;
  const hubsFlag = st.nodes.filter(n => n.hub && n.mod).map(n => n.id);
  check(nFlag === nMod, `every module node is flagged has-page (${nFlag}/${nMod})`);
  check(hubsFlag.length === 10 && !hubsFlag.includes('CMx') && !hubsFlag.includes('QC'),
        'hubs with pages: ' + hubsFlag.join(' '));

  // boot() with #CM-22 in the URL
  const title = ids['net-title'], sub = ids['net-sub'], links = ids['net-links'], mod = ids['net-module'];
  check(title.textContent === st.nodes[cm22].label, 'boot with #CM-22: panel title is the CM-22 label');
  check(sub.textContent.indexOf('CM-22') === 0, 'boot with #CM-22: subtitle starts with the id');
  check(mod.hidden === false && mod.href === '../modules/teaching_modules.html#CM-22',
        'boot with #CM-22: "open module" link points at the module page');
  check(mod.textContent === 'open module CM-22', 'link text: ' + mod.textContent);
  check(hist.length === 0, 'URL untouched when it already names the orb');
  check(links.children.length === st.adj[cm22].length,
        `panel lists all ${st.adj[cm22].length} neighbours of CM-22`);

  // click a chip: travel, and the URL follows
  const chip = links.children[0], chipId = chip.textContent;
  chip.fire('click');
  check(title.textContent === st.nodes[st.byId[chipId]].label, 'chip click travels to ' + chipId);
  check(hist[hist.length - 1] === '#' + chipId && loc.hash === '#' + chipId,
        'URL follows travel: ' + hist[hist.length - 1]);
  check(mod.href === '../modules/teaching_modules.html#' + chipId, 'link follows travel');

  // hashchange: hub, stub hub, garbage, empty
  setHashAndFire('#MA');
  check(title.textContent === st.nodes[st.byId['MA']].label &&
        mod.textContent === 'browse the MA modules' && mod.href.endsWith('#MA'),
        'hashchange #MA: hub panel + "browse the MA modules"');
  setHashAndFire('#CMx');
  check(mod.hidden === true && mod.href === '', 'hashchange #CMx: stub trunk has no page, link hidden');
  const before = title.textContent;
  setHashAndFire('#nonsense');
  check(title.textContent === before, 'hashchange #nonsense: ignored');
  setHashAndFire('');
  check(title.textContent === 'The Teaching Network' && mod.hidden === true,
        'hashchange empty: back to the whole sky, link hidden');
  check(links.children.length === 12, 'overview panel lists the 12 trunks');

  // double-click on empty space: whole sky, hash cleared
  setHashAndFire('#QM-04');
  check(title.textContent === st.nodes[st.byId['QM-04']].label, 'hashchange #QM-04 travels');
  ids.net.fire('dblclick', { clientX: -5000, clientY: -5000 });
  check(title.textContent === 'The Teaching Network' && loc.hash === '' &&
        !hist[hist.length - 1].startsWith('#'), 'double-click fit clears the URL hash');
} else {
  const html = await Deno.readTextFile(modHtml);
  const scripts = [...html.matchAll(/<script defer>([\s\S]*?)<\/script>/g)];
  check(scripts.length === 1, 'exactly one inline deferred script in teaching_modules.html');
  const js = scripts[0][1];
  const sections = [];
  for (const m of html.matchAll(/<section id="(m-[^"]+)" class="module( on)?"/g)) {
    const e = new El('section', m[1]); e.classes.add('module'); if (m[2]) e.classes.add('on');
    sections.push(e);
  }

  // the sidebar, in document order, with a laid-out geometry
  const LIST_TOP = 141, VIEW = 600, HEIGHT = { trunk: 30, subtrunk: 24, item: 34 };
  const listHtml = /<div id="list">([\s\S]*?)<\/div>\s*<\/nav>/.exec(html)[1];
  const list = new El('div', 'list');
  list.clientHeight = VIEW;
  list.getBoundingClientRect = () => ({ top: LIST_TOP, height: VIEW });
  const rows = [], items = [];
  let y = 0, prev = null;
  for (const m of listHtml.matchAll(/<div class="(trunk|subtrunk)">([^<]*)<\/div>|<button class="item" data-t="([^"]+)">/g)) {
    const kind = m[1] || 'item';
    const e = new El(kind === 'item' ? 'button' : 'div');
    e.classes.add(kind);
    if (kind === 'item') { e.dataset.t = m[3]; items.push(e); } else e.textContent = m[2];
    e.y = y; e.h = HEIGHT[kind]; y += e.h;
    e.getBoundingClientRect = () => ({ top: LIST_TOP + e.y - list.scrollTop, height: e.h });
    e.previousElementSibling = prev; prev = e; rows.push(e);
  }
  check(sections.length > 0 && sections.length === items.length,
        `${sections.length} sections, ${items.length} sidebar buttons (list ${y} px tall)`);
  const byId = new Map(sections.map(s => [s.id, s]));
  const item = (t) => items.find(b => b.dataset.t === t);
  const headingOf = (it) => { let h = it.previousElementSibling;
    while (h && !h.classes.has('trunk') && !h.classes.has('subtrunk')) h = h.previousElementSibling; return h; };
  const visible = (e) => e.y >= list.scrollTop && e.y + e.h <= list.scrollTop + VIEW;

  const main = new El('main', 'main'), filter = new El('input', 'filter');
  const docEl = { scrollTop: 0 }, body = { scrollTop: 0 };
  let scrollToCalls = 0;
  defineGlobal('document', {
    documentElement: docEl, body,
    querySelectorAll(sel) { return sel === '.item' ? items : sel === '.module' ? sections
      : sel === '.trunk' ? rows.filter(r => r.classes.has('trunk'))
      : sel === '.subtrunk' ? rows.filter(r => r.classes.has('subtrunk')) : []; },
    querySelector(sel) {
      if (sel === '.module.on') return sections.find(s => s.classes.has('on')) || null;
      const m = /^\.module\[id\^="([^"]+)"\]$/.exec(sel);
      if (m) return sections.find(s => s.id.startsWith(m[1])) || null;
      throw new Error('stub: unsupported selector ' + sel);
    },
    getElementById(id) {
      return byId.get(id) || ({ main, filter, list })[id] || null;
    },
    addEventListener() {}
  });
  defineGlobal('scrollTo', () => { scrollToCalls++; });
  defineGlobal('requestAnimationFrame', (f) => { f(); return 1; });
  const rendered = [];
  defineGlobal('renderMathInElement', (el) => rendered.push(el.id));
  const onOf = () => sections.filter(s => s.classes.has('on')).map(s => s.id).join();
  const activeOf = () => items.filter(b => b.classes.has('active')).map(b => b.dataset.t).join();
  const dirty = () => { main.scrollTop = 57; docEl.scrollTop = 40; body.scrollTop = 40; };  // as if something scrolled
  const pinned = () => main.scrollTop === 0 && docEl.scrollTop === 0 && body.scrollTop === 0;

  loc.hash = '#MA-02';
  (0, eval)(js);
  check(onOf() === 'm-MA-01', 'before DOMContentLoaded the first MA module is the one marked on');
  dirty();
  globalThis.dispatchEvent(new Event('DOMContentLoaded'));
  check(onOf() === 'm-MA-02' && activeOf() === 'm-MA-02', 'load with #MA-02 shows MA-02 (sidebar active)');
  check(rendered.join() === 'm-MA-02', 'only the hash module was KaTeX-rendered at load: ' + rendered.join());
  let it = item('m-MA-02'), hd = headingOf(it);
  check(items.every(b => b.scrolled.length === 0), 'scrollIntoView is never used (it would scroll the page too)');
  check(hd && hd.classes.has('trunk') && hd.textContent.startsWith('MA') && visible(hd) && visible(it) &&
        list.scrollTop === Math.max(0, hd.y - 6),
        `arrival at MA-02: list scrolled to its trunk heading (${list.scrollTop} px), item in view`);
  check(pinned() && scrollToCalls >= 1, 'arrival pins the page and the reading column to the top');
  check(hist.length === 0, 'URL untouched on hash arrival');
  globalThis.dispatchEvent(new Event('load'));
  check(pinned(), 'still pinned after load');

  dirty();
  setHashAndFire('#m-CM-22');
  it = item('m-CM-22'); hd = headingOf(it);
  check(onOf() === 'm-CM-22', 'hashchange #m-CM-22 (prefixed form) shows CM-22');
  check(visible(it) && !visible(hd) && Math.abs(list.scrollTop - (it.y - VIEW / 3)) < 0.5,
        `CM-22 is too deep for its heading to fit: item a third down the list (${list.scrollTop} px)`);
  check(pinned(), 'hashchange arrival pins the top too');
  setHashAndFire('#QM');
  it = item('m-QM-01'); hd = headingOf(it);
  check(onOf() === 'm-QM-01' && visible(hd) && visible(it) && list.scrollTop === Math.max(0, hd.y - 6),
        'hashchange #QM (a trunk) shows its first module under the QM heading');
  setHashAndFire('#TD-1.1');
  it = item('m-TD-1.1'); hd = headingOf(it);
  check(onOf() === 'm-TD-1.1' && hd.classes.has('subtrunk') && visible(hd) && visible(it),
        'hashchange #TD-1.1 (Thermo id with a dot) shows it under its Topic heading');
  setHashAndFire('#MACRO_EM');
  it = item('m-MACRO_EM-01');
  check(onOf() === 'm-MACRO_EM-01' && visible(it), 'hashchange #MACRO_EM (underscore trunk) shows its first module');
  const keep = onOf(), keepScroll = list.scrollTop;
  setHashAndFire('#NE-99');
  check(onOf() === keep, 'unknown id leaves the page as it was');
  setHashAndFire('#"><img src=x onerror=1>');
  check(onOf() === keep, 'junk hash is ignored (no selector built from it)');
  setHashAndFire('#MA-');
  check(onOf() === keep, 'a dangling "#MA-" is ignored');
  setHashAndFire('');
  check(onOf() === keep && list.scrollTop === keepScroll, 'empty hash leaves the page and the list as they were');
  check(hist.length === 0, 'hash routing never rewrites the URL');

  // a filter in the box would hide the target: arrival clears it
  filter.value = 'tensor';
  let filterInputs = 0; filter.addEventListener('input', () => filterInputs++);
  setHashAndFire('#CM-01');
  check(filter.value === '' && filterInputs === 1 && onOf() === 'm-CM-01', 'arrival clears the sidebar filter');

  // a sidebar click keeps the URL in step, nudges only when out of view, renders once
  const before = list.scrollTop;
  it = item('m-CM-03');                                  // in view after CM-01's arrival
  check(visible(it), 'CM-03 is in view');
  it.onclick();
  check(onOf() === 'm-CM-03' && hist[hist.length - 1] === '#CM-03' && loc.hash === '#CM-03',
        'sidebar click shows CM-03 and sets #CM-03');
  check(list.scrollTop === before, 'clicking an item in view does not move the list');
  it = item('m-ST-18');                                  // far below
  it.onclick();
  check(onOf() === 'm-ST-18' && visible(it) && list.scrollTop === it.y + it.h - VIEW + 8,
        'clicking an item out of view nudges it to the bottom edge');
  it = item('m-CM-22'); it.onclick();
  check(rendered.filter(x => x === 'm-CM-22').length === 1, 'a module renders once (cached)');
  const ne01 = item('m-NE-01');
  ne01.onclick();
  check(onOf() === 'm-NE-01' && loc.hash === '#NE-01', 'sidebar click on NE-01 (no orb) still sets #NE-01');
  check(main.scrollTop === 0, 'reading column at the top after clicks');
}

console.log(`${passes} passed, ${fails} failed (${mode})`);
if (fails) Deno.exit(1);
