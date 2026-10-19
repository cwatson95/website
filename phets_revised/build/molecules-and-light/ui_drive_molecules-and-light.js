/* ============ UI drive test for molecules-and-light.html ================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build/molecule-polarity).
 * The three sim-specific thresholds: the chip rows are found by arity AND
 * label (light source 4, molecule 8, animation 2); the panel has 10 groups;
 * 8 inputs (3 sliders, 5 checkboxes).  Every drag, the wheel, the animation
 * and each button are driven THROUGH the frame loop from a proven-idle
 * baseline, and each asserts the drawing MOVED or the state CHANGED --
 * exercising an interaction is not testing it (Known-bad).                   *
 * ========================================================================== */
ObjC.import('Foundation');

let UPASS = 0, UFAIL = 0;
const uok = (c, n) => { if (c) UPASS++; else { UFAIL++; console.log('UI FAIL — ' + n); } };

function makeRecU() {
  const ops = [];
  const stt = {font: '10px x', textAlign: 'left', textBaseline: 'alphabetic'};
  const P = () => {};
  const c = {ops,
    save: P, restore: P, setTransform: P, translate: P, rotate: P, scale: P, setLineDash: P,
    beginPath() { c._p = []; }, moveTo(x, y) { if (c._p) c._p.push([x, y]); },
    lineTo(x, y) { if (c._p) c._p.push([x, y]); }, closePath: P,
    rect(x, y, w, h) { if (c._p) c._p.push([x, y], [x + w, y + h]); },
    arc(x, y, r) { if (c._p) c._p.push([x, y, r]); },
    fill() { if (c._p && c._p.length) ops.push(['f'].concat(c._p.flat())); },
    stroke() { if (c._p && c._p.length) ops.push(['s'].concat(c._p.flat())); },
    clip: P,
    fillRect(x, y, w, h) { ops.push(['r', x, y, w, h]); },
    strokeRect(x, y, w, h) { ops.push(['R', x, y, w, h]); }, clearRect: P,
    fillText(t, x, y) { ops.push(['t', String(t), Math.round(x), Math.round(y)]); }, strokeText: P,
    measureText(t) {
      const m = /(\d+(?:\.\d+)?)px/.exec(stt.font || '');
      return {width: ('' + t).length * (m ? parseFloat(m[1]) : 10) * 0.52};
    },
    createLinearGradient() { return {addColorStop() {}}; },
  };
  Object.defineProperty(c, 'font', {get: () => stt.font, set: v => { stt.font = v; }});
  for (const k of ['fillStyle', 'strokeStyle', 'lineWidth', 'globalAlpha', 'textAlign',
                   'textBaseline', 'lineJoin', 'lineCap'])
    Object.defineProperty(c, k, {get: () => stt[k], set: v => { stt[k] = v; }});
  return c;
}
const geomU = c => JSON.stringify(c.ops.filter(o => o[0] !== 't'));
const entReU = /&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
function assertCleanU(rec, label) {
  let bad = null;
  for (const o of rec.ops) if (o[0] === 't') {
    if (entReU.test(o[1])) { bad = 'entity/tag "' + String(o[1]).slice(0, 40) + '"'; break; }
    if (/NaN|undefined|Infinity/.test(o[1])) { bad = 'NaN/undefined "' + String(o[1]).slice(0, 40) + '"'; break; }
  }
  uok(!bad, label + ' text ops clean' + (bad ? ' (' + bad + ')' : ''));
}
let RECU = makeRecU();
function mkElU(tag) {
  const e = {tagName: (tag || 'div').toUpperCase(), children: [], style: {}, dataset: {},
    _h: {}, className: '', id: '', value: '0', checked: false, hidden: false, disabled: false,
    textContent: '',
    appendChild(c) {
      this.children.push(c);
      if (c && c.nodeType === 3) this.textContent = (this.textContent || '') + c.textContent;
      else if (c && c.textContent) this.textContent = (this.textContent || '') + c.textContent;
      return c;
    },
    setAttribute(k, v) { this[k] = v; },
    addEventListener(k, f) { (this._h[k] = this._h[k] || []).push(f); },
    removeEventListener() {}, setPointerCapture() {}, releasePointerCapture() {},
    classList: {_on: {}, add(c) { this._on[c] = 1; }, remove(c) { delete this._on[c]; },
                toggle(c) { this._on[c] ? delete this._on[c] : this._on[c] = 1; },
                contains(c) { return !!this._on[c]; }},
    getBoundingClientRect() { return {left: 0, top: 0, width: 1400, height: 820}; },
    getContext() { return RECU; },
    querySelector(s) { return this._find(s)[0] || null; },
    querySelectorAll(s) { return this._find(s); },
    _find(s) {
      const out = [], want = (s || '').trim();
      const walk = n => {
        for (const ch of n.children || []) {
          if (want === '#info' && ch.id === 'info') out.push(ch);
          else if (want === '#phys' && ch.id === 'phys') out.push(ch);
          else if (want === '.chips' && ch.className === 'chips') out.push(ch);
          else if (want === 'input' && ch.tagName === 'INPUT') out.push(ch);
          walk(ch);
        }
      };
      walk(this);
      return out;
    },
    fire(k, ev) {
      for (const f of (this._h[k] || []))
        f(Object.assign({preventDefault() {}, stopPropagation() {}, clientX: 0, clientY: 0,
                         pointerId: 1, buttons: 1, deltaY: 0}, ev || {}));
    },
  };
  /* a real browser derives textContent from innerHTML; the shared stub did not (Known-bad) */
  let _html = '';
  Object.defineProperty(e, 'innerHTML', {
    get() { return _html; },
    set(v) { _html = '' + v; e.textContent = ('' + v).replace(/<[^>]*>/g, ''); }});
  return e;
}
const NODESU = {};
for (const id of ['scene', 'panel', 'tabs', 'readout', 'eqbar', 'tag', 'hint', 'errbox', 'sub'])
  NODESU[id] = mkElU(id === 'scene' ? 'canvas' : 'div'), NODESU[id].id = id;
globalThis.document = {readyState: 'complete', getElementById: id => NODESU[id] || null,
  createElement: mkElU,
  createTextNode: t => ({nodeType: 3, textContent: '' + t, children: []}),
  addEventListener() {}};
const WINHU = {};
let RAFU = null;
globalThis.window = {devicePixelRatio: 1, addEventListener(k, f) { (WINHU[k] = WINHU[k] || []).push(f); },
  requestAnimationFrame(f) { RAFU = f; return 1; }};
globalThis.requestAnimationFrame = f => { RAFU = f; return 1; };
let TNOWU = 0;
function pumpU(n) { for (let i = 0; i < (n || 1); i++) { const f = RAFU; if (!f) return; RAFU = null; TNOWU += 16; f(TNOWU); } }
function settleU(max) {
  let quiet = 0, n = 0;
  while (quiet < 3 && n < (max || 4000)) { RECU = makeRecU(); pumpU(1); n++; quiet = RECU.ops.length ? 0 : quiet + 1; }
  return n;
}
function keyU(k) { for (const f of (WINHU.keydown || [])) f({key: k, preventDefault() {}}); }
function sliderU(label) {
  let hit = null;
  const walk = n => {
    for (const ch of n.children || []) {
      if (ch.className === 'sliderrow' && ch.children[0] && (ch.children[0].textContent || '') === label)
        hit = ch.children[1];
      walk(ch);
    }
  };
  walk(NODESU.panel);
  return hit;
}
function checkU(label) {
  let hit = null;
  const walk = n => {
    for (const ch of n.children || []) {
      if (ch.tagName === 'LABEL' && (ch.textContent || '') === label)
        for (const c2 of ch.children || []) if (c2.tagName === 'INPUT') hit = c2;
      walk(ch);
    }
  };
  walk(NODESU.panel);
  return hit;
}
function chipsU(arity) {
  const out = [];
  const walk = n => { for (const ch of n.children || []) { if (ch.className === 'chips' && ch.children.length === arity) out.push(ch); walk(ch); } };
  walk(NODESU.panel);
  return out;
}
function chipU(label, arity) {
  for (const cw of chipsU(arity)) for (const c of cw.children) if (c.textContent === label) return c;
  return null;
}
function buttonU(needle) {
  let hit = null;
  const walk = n => { for (const ch of n.children || []) { if (ch.tagName === 'BUTTON' && (ch.textContent || '') === needle) hit = ch; walk(ch); } };
  walk(NODESU.panel);
  return hit;
}
function clickU(needle) { const b = buttonU(needle); if (b) b.fire('click'); return !!b; }
function tabU(i) { NODESU.tabs.children[i].fire('click'); }
function tabIndex(k) { return TABS.findIndex(t => t[0] === k); }
function dragU(x0, y0, x1, y1) {
  NODESU.scene.fire('pointerdown', {clientX: x0, clientY: y0});
  NODESU.scene.fire('pointermove', {clientX: x1, clientY: y1});
  NODESU.scene.fire('pointerup', {});
}
/* pointerdown sets the dirty flag itself, so a drag fired in one go cannot
   test whether the MOVE handler sets it: press, drain the loop, prove it is
   idle again, and only then move (Known-bad: anything that forces a draw
   between an idle proof and the action re-arms the flag). */
function pressU(x0, y0) { NODESU.scene.fire('pointerdown', {clientX: x0, clientY: y0}); }
function moveU(x1, y1) { NODESU.scene.fire('pointermove', {clientX: x1, clientY: y1}); }
function releaseU() { NODESU.scene.fire('pointerup', {}); }
function forceDrawU() { RECU = makeRecU(); tabU(tabIndex(ST.view)); return geomU(RECU); }
function idleProofU(label) {
  settleU();
  RECU = makeRecU();
  pumpU(3);
  uok(geomU(RECU) === '[]', label + ': the loop is idle first');
}
/* every proven-idle test needs the animation off; the chamber view runs by default */
function quietU() {
  ST.running = false;
  const cb = checkU('running');
  if (cb) { cb.checked = false; cb.fire('change'); }
}

/* ---- boot ---- */
let bootErrU = null;
try { boot(); } catch (e) { bootErrU = e; }
uok(!bootErrU, 'boot() completes without throwing' + (bootErrU ? ': ' + (bootErrU.stack || bootErrU) : ''));
uok(NODESU.errbox.style.display !== 'block', 'no error captured after boot');
uok(NODESU.tabs.children.length === TABS.length, TABS.length + ' view tabs were built');
uok(NODESU.tabs.children.map(b => b.textContent).join('|') === TABS.map(t => t[1]).join('|'),
    'the tabs are lower-case noun phrases: ' + NODESU.tabs.children.map(b => b.textContent).join(', '));
const NGROUPS = 10, NINPUTS = 8;
uok(NODESU.panel.children.length === NGROUPS,
    'the control panel has its ' + NGROUPS + ' groups (' + NODESU.panel.children.length + ')');
uok(NODESU.panel.querySelectorAll('input').length === NINPUTS,
    'and its ' + NINPUTS + ' inputs (' + NODESU.panel.querySelectorAll('input').length + ')');
uok((NODESU.readout.innerHTML || '').length > 300, 'the readout rendered');
uok((NODESU.eqbar.innerHTML || '').indexOf('NaN') < 0 && NODESU.eqbar.innerHTML.length > 40,
    'the equation bar rendered');
{ const credit = NODESU.panel.children[NGROUPS - 2].textContent;
  uok(/Remake of PhET Interactive Simulations/.test(credit) && /CC-BY 4\.0/.test(credit),
      'the credit line is on the panel');
  uok(/CCCBDB/.test(credit), 'and it names where the measured numbers came from');
  uok(/1\.5\.33/.test(credit), "and which PhET build PhET's values came from");
  uok(/QUOTED/.test(credit), 'and says outright which numbers were only quoted');
}
/* the three chip rows, by arity AND label */
uok(chipsU(4).length === 1 && chipU('Infrared', 4), 'the light-source row has PhET’s four bands');
uok(chipsU(8).length === 1 && chipU('CO2', 8), 'the molecule row has PhET’s eight molecules');
uok(chipsU(2).length === 1 && chipU('PhET’s animation', 2), 'the animation row has two chips');

/* ---- every tab draws, and draws something different ---- */
{ const sigs = [];
  for (let i = 0; i < TABS.length; i++) {
    RECU = makeRecU();
    tabU(i);
    uok(RECU.ops.length > 20, 'tab ' + i + ' (' + TABS[i][1] + ') drew content (' + RECU.ops.length + ' ops)');
    uok(NODESU.errbox.style.display !== 'block', 'tab ' + i + ' drew without error');
    assertCleanU(RECU, 'tab ' + i);
    uok((NODESU.readout.innerHTML || '').length > 200, 'tab ' + i + ' rendered a readout');
    uok(!/NaN|undefined/.test(NODESU.readout.innerHTML + NODESU.eqbar.innerHTML + NODESU.tag.innerHTML),
        'tab ' + i + ' readout, eqbar and tag are clean');
    uok((NODESU.panel.querySelector('#info').textContent || '').length > 400,
        'tab ' + i + ' has a paragraph of prose in the panel');
    sigs.push(geomU(RECU));
  }
  uok(new Set(sigs).size === TABS.length, 'every tab draws a different picture (' + new Set(sigs).size + '/' + TABS.length + ')');
}

/* ---- the chamber really animates, and stops when told ---- */
{ tabU(tabIndex('chamber'));
  clickU('reset all');
  tabU(tabIndex('chamber'));
  const t0 = CH.t;
  RECU = makeRecU();
  pumpU(40);
  uok(CH.t > t0, 'the chamber clock advances while it is running (' + fmt(CH.t, 3) + ' s)');
  uok(RECU.ops.length > 50, 'and the frame loop paints while it does');
  uok(CH.fired > 0, 'the source has fired photons (' + CH.fired + ')');
  quietU();
  idleProofU('the paused chamber');
  const t1 = CH.t;
  pumpU(20);
  uok(CH.t === t1, 'with "running" off the clock is frozen');
  /* the step button must advance it by exactly one frame */
  clickU('step one frame');
  uok(Math.abs(CH.t - t1 - 1 / 60) < 1e-12, 'and "step one frame" advances exactly one frame');
}
/* ---- firing one photon is a real, countable action ---- */
{ quietU();
  const n0 = CH.fired;
  uok(clickU('fire one photon'), 'the "fire one photon" button exists');
  uok(CH.fired === n0 + 1, 'and it fires exactly one photon (' + n0 + ' -> ' + CH.fired + ')');
  const p = CH.photons[CH.photons.length - 1];
  uok(p && Math.abs(p.x - PHET.EMITTER_X) < 1e-9 && Math.abs(p.vx - PHET.PHOTON_SPEED) < 1e-9,
      "(PhET) it starts at x = -1350 moving right at 3000");
  keyU('f');
  uok(CH.fired === n0 + 2, 'and the f key does the same');
}
/* ---- reset molecule really resets the counters ---- */
{ quietU();
  clickU('fire one photon');
  clickU('fire one photon');
  uok(CH.fired >= 2, 'a sentinel: two photons are in flight before the reset');
  uok(clickU('reset molecule'), 'the "reset molecule" button exists');
  uok(CH.fired === 0 && CH.photons.length === 0 && CH.state === 'idle',
      'and it clears the counters, the photons and the state');
}
/* ---- the space bar toggles running, and only that ---- */
{ ST.running = false;
  keyU(' ');
  uok(ST.running === true, 'the space bar starts the clock');
  keyU(' ');
  uok(ST.running === false, 'and stops it again');
}

/* ---- the drag must MOVE the drawing, through the frame loop ---- */
tabU(tabIndex('modes'));
quietU();
for (const [nm, dx, dy] of [['horizontal', 260, 0], ['vertical', 0, 190]]) {
  keyU('r');
  clickU('reset all');
  quietU();
  tabU(tabIndex('modes'));
  idleProofU('modes, ' + nm + ' drag');
  const before = forceDrawU();
  const th0 = ST.camTheta, ph0 = ST.camPhi;
  pressU(400, 300);
  settleU();
  RECU = makeRecU();
  pumpU(3);
  uok(geomU(RECU) === '[]', 'the press alone leaves the loop idle again');
  RECU = makeRecU();
  moveU(400 + dx, 300 + dy);
  pumpU(3);
  uok(geomU(RECU).length > 50, 'a ' + nm + ' drag marks the frame loop dirty');
  releaseU();
  const after = forceDrawU();
  uok(after !== before && after.length > 50, 'and the ' + nm + ' drag moved the molecule');
  if (dx) uok(Math.abs(ST.camTheta - th0) > 1e-3, 'theta really changed (' + th0 + ' -> ' + ST.camTheta + ')');
  else uok(Math.abs(ST.camPhi - ph0) > 1e-3, 'phi really changed (' + ph0 + ' -> ' + ST.camPhi + ')');
}
/* the wheel: resetCam() sets dirty itself, so drain it and prove idleness first */
{ clickU('reset all');
  quietU();
  tabU(tabIndex('modes'));
  keyU('r');
  idleProofU('the wheel test');
  const z0 = ST.zoom;
  RECU = makeRecU();
  NODESU.scene.fire('wheel', {deltaY: -500});
  pumpU(3);
  uok(geomU(RECU).length > 50, 'the wheel marks the frame loop dirty');
  uok(ST.zoom > z0, 'and the wheel zoomed in (' + z0 + ' -> ' + ST.zoom + ')');
  const zoomed = forceDrawU();
  ST.zoom = z0;
  const plainPic = forceDrawU();
  uok(zoomed !== plainPic, 'the zoomed picture differs from the un-zoomed one');
}
/* a view that ignores the pointer must really ignore it -- test the
   CONSEQUENCE (the camera), not the immediate frame */
{ clickU('reset all');
  quietU();
  tabU(tabIndex('table'));
  const th0 = ST.camTheta;
  dragU(300, 300, 520, 380);
  uok(ST.camTheta === th0, 'a drag on a 2-D view leaves the camera exactly where it was');
  NODESU.scene.fire('wheel', {deltaY: -500});
  uok(ST.zoom === 1, 'and so does the wheel');
}

/* ---- every chip, and what it changes ---- */
{ clickU('reset all');
  quietU();
  tabU(tabIndex('chamber'));
  for (const bd of BANDS) {
    const c = chipU(BANDNAME[bd], 4);
    uok(!!c, 'the ' + bd + ' chip exists');
    if (!c) continue;
    RECU = makeRecU();
    c.fire('click');
    uok(ST.band === bd, 'clicking it selects ' + bd);
    uok(RECU.ops.length > 20, 'and repaints (' + RECU.ops.length + ' ops)');
    uok(CH.band === bd && CH.fired === 0, 'and rebuilds the chamber on the new band');
    assertCleanU(RECU, 'band ' + bd);
  }
  for (const mol of MOLORDER) {
    const c = chipU(mol, 8);
    uok(!!c, 'the ' + mol + ' chip exists');
    if (!c) continue;
    /* a sentinel: without one, "it rewinds the mode index" is vacuous because
       the index was already 0 (Known-bad -- set the state to a NON-default
       value immediately before asserting that an action resets it) */
    ST.modeIdx = 5;
    RECU = makeRecU();
    c.fire('click');
    uok(ST.mol === mol && ST.modeIdx === 0, 'clicking it selects ' + mol + ' and rewinds the mode index');
    uok(RECU.ops.length > 20, 'and repaints');
    assertCleanU(RECU, 'molecule ' + mol);
  }
  for (const a of ['the normal mode', 'PhET’s animation']) {
    const c = chipU(a, 2);
    uok(!!c, 'the "' + a + '" chip exists');
    if (c) { RECU = makeRecU(); c.fire('click'); uok(RECU.ops.length > 20, 'and it repaints'); }
  }
  uok(ST.anim === 'phet', 'the animation chip really switched to PhET’s offsets');
}
/* ---- the mode buttons walk the whole mode list ---- */
{ clickU('reset all');
  quietU();
  tabU(tabIndex('modes'));
  const c = chipU('CH4', 8);
  if (c) c.fire('click');
  const n = modeTable('CH4').length;
  uok(n === 9, 'methane has nine vibrations (' + n + ')');
  const seen = {};
  for (let i = 0; i < n; i++) { seen[ST.modeIdx] = 1; clickU('next mode'); }
  uok(Object.keys(seen).length === n, '"next mode" visits every one of them (' + Object.keys(seen).length + ')');
  uok(ST.modeIdx === 0, 'and wraps back to the first');
  clickU('previous mode');
  uok(ST.modeIdx === n - 1, '"previous mode" wraps the other way');
}

/* ---- every slider and checkbox, driven ---- */
{ clickU('reset all');
  quietU();
  const SL = [['stats', 'photons drawn', 'nStat'], ['stats', 'seed', 'statSeed'], ['air', 'surface T', 'tempK']];
  for (const [view, label, key] of SL) {
    tabU(tabIndex(view));
    const s = sliderU(label);
    uok(!!s, 'the "' + label + '" slider exists on the ' + view + ' view');
    if (!s) continue;
    const lo = parseFloat(s.min), hi = parseFloat(s.max);
    for (const v of [lo, (lo + hi) / 2, hi]) {
      RECU = makeRecU();
      s.value = String(v);
      s.fire('input');
      uok(Math.abs(ST[key] - v) < 1e-9, label + ' = ' + v + ' reaches the state');
      uok(RECU.ops.length > 20, 'and repaints (' + RECU.ops.length + ' ops)');
      assertCleanU(RECU, label + '=' + v);
      uok(NODESU.errbox.style.display !== 'block', 'and throws nothing');
    }
  }
  /* one slider gets the full treatment: proven idle, fire, assert ops appeared */
  tabU(tabIndex('air'));
  idleProofU('the surface-T slider');
  { const s = sliderU('surface T');
    RECU = makeRecU();
    s.value = '250';
    s.fire('input');
    uok(RECU.ops.length > 20, 'moving the surface-T slider paints immediately (' + RECU.ops.length + ' ops)');
    const a1 = airBlock().peak;
    s.value = '320';
    s.fire('input');
    uok(airBlock().peak > a1, 'and a hotter surface really moves the Planck peak up in wavenumber');
  }
  const CB = [['chamber', 'source on', 'source'], ['chamber', 'running', 'running'],
              ['chamber', 'slow motion', 'slow'], ['chamber', 'show the absorption radius', 'showRadius'],
              ['air', 'shade the 8–13 µm window', 'showWindow']];
  for (const [view, label, key] of CB) {
    tabU(tabIndex(view));
    const cb = checkU(label);
    uok(!!cb, 'the "' + label + '" checkbox exists on the ' + view + ' view');
    if (!cb) continue;
    const was = ST[key];
    RECU = makeRecU();
    cb.checked = !was;
    cb.fire('change');
    uok(ST[key] === !was, 'toggling it reaches the state');
    uok(RECU.ops.length > 15, 'and repaints');
    cb.checked = was;
    cb.fire('change');
    uok(ST[key] === was, 'and it toggles back');
  }
}
/* the absorption-radius checkbox must change the PICTURE, not just the flag */
{ clickU('reset all');
  quietU();
  tabU(tabIndex('chamber'));
  const before = forceDrawU();
  const cb = checkU('show the absorption radius');
  cb.checked = true;
  cb.fire('change');
  const after = forceDrawU();
  uok(after !== before, 'showing the absorption radius really adds geometry to the drawing');
}
/* the window shading likewise */
{ clickU('reset all');
  quietU();
  tabU(tabIndex('air'));
  const before = forceDrawU();
  const cb = checkU('shade the 8–13 µm window');
  cb.checked = false;
  cb.fire('change');
  const after = forceDrawU();
  uok(after !== before, 'un-shading the window really removes geometry');
}

/* ---- reset all must restore EVERY kind of state, the camera included ---- */
{ tabU(tabIndex('modes'));
  ST.camTheta = 0.9; ST.camPhi = -0.8; ST.zoom = 2.2;
  ST.tempK = 301; ST.nStat = 1500; ST.statSeed = 9; ST.modeIdx = 2;
  const cbs = checkU('shade the 8–13 µm window');
  if (cbs) { cbs.checked = false; cbs.fire('change'); }
  const cm = chipU('NO2', 8);
  if (cm) cm.fire('click');
  clickU('reset all');
  uok(ST.camTheta === DEFAULTS.camTheta && ST.camPhi === DEFAULTS.camPhi && ST.zoom === 1,
      'reset all restores the camera (through the defaults, which carry it)');
  uok(ST.tempK === DEFAULTS.tempK && ST.nStat === DEFAULTS.nStat && ST.statSeed === DEFAULTS.statSeed,
      'and every slider');
  uok(ST.mol === DEFAULTS.mol && ST.band === DEFAULTS.band && ST.showWindow === DEFAULTS.showWindow,
      'and every chip and checkbox');
  uok(ST.view === 'modes', 'and leaves the view where it was');
  uok(CH.fired === 0 && CH.mol === DEFAULTS.mol, 'and rebuilds the chamber');
}

/* ---- the keyboard ---- */
{ for (let i = 1; i <= TABS.length; i++) {
    keyU(String(i));
    uok(ST.view === TABS[i - 1][0], 'key ' + i + ' switches to ' + TABS[i - 1][1]);
  }
  tabU(tabIndex('modes'));
  ST.camTheta = 0.4; ST.camPhi = -0.9; ST.zoom = 2.4;
  keyU('r');
  uok(ST.camTheta === DEFAULTS.camTheta && ST.camPhi === DEFAULTS.camPhi && ST.zoom === 1,
      'r resets all three camera values');
  ST.camTheta = 0.4; ST.camPhi = -0.9; ST.zoom = 2.4;
  uok(clickU('reset view'), 'the "reset view" button exists');
  uok(ST.camTheta === DEFAULTS.camTheta && ST.camPhi === DEFAULTS.camPhi && ST.zoom === 1,
      'and it is the other path to the same reset');
}

/* ---- resize, and the narrow stage ---- */
{ clickU('reset all');
  quietU();
  for (const [w, hh] of [[1400, 820], [1000, 700], [760, 520], [560, 380]]) {
    NODESU.scene.getBoundingClientRect = () => ({left: 0, top: 0, width: w, height: hh});
    for (const f of (WINHU.resize || [])) f({});
    for (let i = 0; i < TABS.length; i++) {
      RECU = makeRecU();
      tabU(i);
      uok(RECU.ops.length > 15, w + 'x' + hh + ' tab ' + i + ' still draws (' + RECU.ops.length + ' ops)');
      assertCleanU(RECU, w + 'x' + hh + ' tab ' + i);
      uok(NODESU.errbox.style.display !== 'block', w + 'x' + hh + ' tab ' + i + ' drew without error');
    }
  }
  NODESU.scene.getBoundingClientRect = () => ({left: 0, top: 0, width: 1400, height: 820});
  for (const f of (WINHU.resize || [])) f({});
}

/* ---- the panel hides what a view does not use ---- */
{ clickU('reset all');
  tabU(tabIndex('stats'));
  uok(NODESU.panel.children[5].hidden === false, 'the ensemble group is shown on the statistics view');
  uok(NODESU.panel.children[6].hidden === true, 'and the atmosphere group is not');
  tabU(tabIndex('air'));
  uok(NODESU.panel.children[6].hidden === false, 'the atmosphere group is shown on the atmosphere view');
  uok(NODESU.panel.children[5].hidden === true, 'and the ensemble group is not');
  tabU(tabIndex('chamber'));
  uok(NODESU.panel.children[3].hidden === false, 'the animation group is shown on the chamber view');
  tabU(tabIndex('modes'));
  uok(NODESU.panel.children[4].hidden === false, 'the mode group is shown on the normal-modes view');
  uok(NODESU.panel.children[3].hidden === true, 'and the animation group is not');
}

/* ---- the modes view animates, and stopping it stops the paint ---- */
{ clickU('reset all');
  tabU(tabIndex('modes'));
  const p0 = MODEPHASE;
  RECU = makeRecU();
  pumpU(10);
  uok(MODEPHASE > p0, 'the normal-mode animation advances its phase');
  uok(RECU.ops.length > 50, 'and paints while it does');
  quietU();
  idleProofU('the paused normal-mode view');
  const p1 = MODEPHASE;
  pumpU(10);
  uok(MODEPHASE === p1, 'and "running" off freezes the phase');
}

/* ---- the readout carries the numbers a reader would check ---- */
{ clickU('reset all');
  tabU(tabIndex('chamber'));
  const cm = chipU('CO2', 8);
  if (cm) cm.fire('click');
  const ro = NODESU.readout.innerHTML;
  uok(/850\.00|850/.test(ro), 'the readout prints the 850 nm wavelength');
  uok(/1\.458|1\.459/.test(ro), 'and the 1.4586 eV it corresponds to');
  uok(/vibrates/.test(ro), "and PhET's own verdict for CO2 in the infrared");
  const cb = chipU('Ultraviolet', 4);
  if (cb) cb.fire('click');
  const ro2 = NODESU.readout.innerHTML;
  uok(/12\.39|12\.4/.test(ro2), 'and switching to the ultraviolet prints 12.398 eV');
  uok(ro2 !== ro, 'the readout really changed with the band');
}

/* the orchestrator's verify_one.py parses `<n> passed, <m> failed` out of a
   line containing "UI", so the count must sit immediately before the word */
console.log('UI drive: ' + UPASS + ' passed, ' + UFAIL + ' failed');
if (UFAIL > 0) throw new Error(UFAIL + ' UI failure(s)');
