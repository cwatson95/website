
/* ============ UI drive, DOM-stub pattern ================================= *
 * boot() is never touched by selfTest, so it gets its own harness.  The rule
 * from the Known-bad list: exercising an interaction is not testing it — every
 * drag check proves the frame loop is IDLE first, then acts, then asserts the
 * drawn geometry MOVED and the state behind it changed.
 * Every name here is prefixed with u so that nothing collides with the sim
 * (which already owns label, box, frame, disc, ring, simpson, R, ...).       */
/* guarded: jsc has no ObjC bridge, and this harness writes no files — it is
   the fast engine to iterate on before the final osascript pass */
if(typeof ObjC !== 'undefined') ObjC.import('Foundation');

let UPASS = 0, UFAIL = 0;
const uok = (c, n) => { if(c) UPASS++; else { UFAIL++; console.log('FAIL — ' + n); } };

/* ---- recording 2-D context ---- */
function uMakeRec(){
  const ops = []; const st = {font: '10px x', textAlign: 'left', textBaseline: 'alphabetic'};
  const P = () => {};
  const c = {ops,
    save: P, restore: P, setTransform: P, translate: P, rotate: P, scale: P, setLineDash: P,
    beginPath(){ c._p = []; }, moveTo(x, y){ c._p && c._p.push([x, y]); },
    lineTo(x, y){ c._p && c._p.push([x, y]); }, closePath: P,
    rect(x, y, w, h){ c._p && c._p.push([x, y], [x + w, y + h]); },
    arc(x, y, r){ c._p && c._p.push([x, y, r]); },
    fill(){ if(c._p && c._p.length) ops.push(['f'].concat(c._p.flat())); },
    stroke(){ if(c._p && c._p.length) ops.push(['s'].concat(c._p.flat())); },
    clip: P, fillRect(x, y, w, h){ ops.push(['r', x, y, w, h]); }, strokeRect: P, clearRect: P,
    fillText(t, x, y){ ops.push(['t', t, Math.round(x), Math.round(y)]); }, strokeText: P,
    measureText(t){ const m = /(\d+(?:\.\d+)?)px/.exec(st.font || '');
      return {width: ('' + t).length * (m ? parseFloat(m[1]) : 10) * 0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
  };
  Object.defineProperty(c, 'font', {get: () => st.font, set: v => st.font = v});
  for(const k of ['fillStyle', 'strokeStyle', 'lineWidth', 'globalAlpha', 'textAlign',
                  'textBaseline', 'lineJoin', 'lineCap'])
    Object.defineProperty(c, k, {get: () => st[k], set: v => st[k] = v});
  return c;
}
const uSig = c => JSON.stringify(c.ops).length + ':' + c.ops.length;
const uGeom = c => JSON.stringify(c.ops.filter(o => o[0] !== 't'));
const uTexts = c => c.ops.filter(o => o[0] === 't').map(o => o[1]);

/* ---- DOM stub ----
   innerHTML is a SETTER that strips tags into textContent.  A real browser
   derives one from the other; the shared tools/ui_drive.js does not, and every
   control built with h(tag,{html:...}) — which is how a chip whose label
   carries an entity has to be built — then reports an EMPTY textContent and
   every finder declares it missing (Known-bad, drum_head.html).  This file's
   model chips are built exactly that way. */
let UREC = uMakeRec();
function uEl(tag){
  const e = {tagName: (tag || 'div').toUpperCase(), children: [], style: {}, dataset: {},
    _h: {}, className: '', id: '', value: '0', checked: false, hidden: false, disabled: false,
    textContent: '',
    appendChild(c){ this.children.push(c);
      if(c && c.nodeType === 3) this.textContent = (this.textContent || '') + c.textContent;
      else if(c && c.textContent) this.textContent = (this.textContent || '') + c.textContent;
      return c; },
    setAttribute(k, v){ this[k] = v; },
    addEventListener(k, f){ (this._h[k] = this._h[k] || []).push(f); },
    removeEventListener(){},
    setPointerCapture(){}, releasePointerCapture(){},
    classList: {_s: {}, add(k){ this._s[k] = 1; }, remove(k){ delete this._s[k]; },
                toggle(){}, contains(k){ return !!this._s[k]; }},
    getBoundingClientRect(){ return {left: 0, top: 0, width: 1400, height: 820}; },
    getContext(){ return UREC; },
    querySelector(s){ return this._find(s)[0] || null; },
    querySelectorAll(s){ return this._find(s); },
    _find(s){
      const out = [];
      const want = (s || '').trim();
      const walk = n => { for(const ch of n.children || []){
        if(want === '#info' && ch.id === 'info') out.push(ch);
        else if(want === '#phys' && ch.id === 'phys') out.push(ch);
        else if(want === '.chips' && ch.className === 'chips') out.push(ch);
        else if(want === 'input' && ch.tagName === 'INPUT') out.push(ch);
        walk(ch); } };
      walk(this); return out;
    },
    fire(k, ev){ for(const f of (this._h[k] || [])) f(Object.assign({
      preventDefault(){}, stopPropagation(){}, clientX: 0, clientY: 0, pointerId: 1, buttons: 1}, ev || {})); },
  };
  let _html = '';
  Object.defineProperty(e, 'innerHTML', {
    get: () => _html,
    set: v => { _html = '' + v; e.textContent = plain(_html); },
  });
  return e;
}
const UNODES = {};
for(const id of ['scene', 'panel', 'tabs', 'readout', 'eqbar', 'tag', 'hint', 'errbox', 'sub'])
  UNODES[id] = uEl(id === 'scene' ? 'canvas' : 'div'), UNODES[id].id = id;

globalThis.document = {
  readyState: 'complete',
  getElementById: id => UNODES[id] || null,
  createElement: uEl,
  createTextNode: t => ({nodeType: 3, textContent: '' + t, children: []}),
  addEventListener(){},
};
const UWINH = {};
let URAF = null;
globalThis.window = {
  devicePixelRatio: 1,
  addEventListener(k, f){ (UWINH[k] = UWINH[k] || []).push(f); },
  requestAnimationFrame(f){ URAF = f; return 1; },
};
globalThis.requestAnimationFrame = f => { URAF = f; return 1; };
let UTNOW = 0;
/* Pump real frames.  This is the ONLY path on which the `dirty` flag matters:
   driving a redraw through refresh() instead tests nothing. */
function upump(n){ for(let i = 0; i < (n || 1); i++){ const f = URAF; if(!f) return;
  URAF = null; UTNOW += 16; f(UTNOW); } }
function uFrameGeom(k){ UREC = uMakeRec(); upump(k || 3); return uGeom(UREC); }

/* ---- boot ---- */
let uBootErr = null;
try{ boot(); }catch(e){ uBootErr = e; }
uok(!uBootErr, 'boot() completes without throwing' + (uBootErr ? ': ' + (uBootErr.stack || uBootErr) : ''));
uok(UNODES.errbox.style.display !== 'block', 'no error was captured into #errbox after boot');
const UNTABS = UNODES.tabs.children.length;
uok(UNTABS === 6, 'the tab bar was built (' + UNTABS + ' tabs, expected 6)');
uok(UNODES.panel.children.length >= 9, 'the control panel was built ('
  + UNODES.panel.children.length + ' groups, floor 9)');
uok((UNODES.readout.innerHTML || '').length > 200, 'the readout rendered');
uok((UNODES.eqbar.innerHTML || '').indexOf('NaN') < 0, 'the equation bar has no NaN');
uok((UNODES.hint.textContent || '').length > 10, 'the hint line rendered');

/* ---- every tab draws, and draws something different ---- */
const uSigs = {};
for(let i = 0; i < UNTABS; i++){
  UREC = uMakeRec();
  UNODES.tabs.children[i].fire('click');
  uok(UREC.ops.length > 20, 'tab ' + i + ' drew content (' + UREC.ops.length + ' ops)');
  uok(UNODES.errbox.style.display !== 'block', 'tab ' + i + ' drew without error');
  /* canvas has no entity parser: a &word; or a <tag> reaching fillText is a bug
     the audit would otherwise only find in the PNG (Known-bad) */
  const bad = uTexts(UREC).filter(t => /&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/.test('' + t));
  uok(!bad.length, 'tab ' + i + ' draws no raw entity or tag' + (bad.length ? ': "' + bad[0] + '"' : ''));
  const nanny = uTexts(UREC).filter(t => /NaN|undefined/.test('' + t));
  uok(!nanny.length, 'tab ' + i + ' draws no NaN/undefined' + (nanny.length ? ': "' + nanny[0] + '"' : ''));
  uSigs['t' + i] = uSig(UREC);
}
uok(new Set(Object.values(uSigs)).size === UNTABS,
  'every tab draws a different picture (' + new Set(Object.values(uSigs)).size + '/' + UNTABS + ')');

/* ---- the chip rows ---- */
function uFindChips(labels){
  /* match on the EXACT labels and the row's arity: a substring match finds the
     wrong row (Known-bad, twice) */
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.className === 'chips' && ch.children.length === labels.length){
      let all = true;
      for(let i = 0; i < labels.length; i++)
        if((ch.children[i].textContent || '') !== labels[i]) all = false;
      if(all) hit = ch;
    }
    walk(ch); } };
  walk(UNODES.panel);
  return hit;
}
const uModelChips = uFindChips(MODEL_LIST.map(o => plain(o.name)));
const uLightChips = uFindChips(LIGHT_LIST.map(o => o.name));
const uSpeedChips = uFindChips(SPEED_LIST.map(o => o.name));
const uDbChips = uFindChips(DB_LIST.map(o => o.name));
const uSerChips = uFindChips(SERIES_LIST.map(o => o.name));
uok(!!uModelChips, 'found the 7-model chip row');
uok(!!uLightChips, 'found the white/monochromatic chip row');
uok(!!uSpeedChips, 'found the speed chip row');
uok(!!uDbChips, 'found the de Broglie representation chip row');
uok(!!uSerChips, 'found the series chip row');

function uClickTab(k){
  for(let i = 0; i < UNTABS; i++) if(TABS[i][0] === k) UNODES.tabs.children[i].fire('click');
}
/* every model, on the box view and on the levels view */
for(const v of ['box', 'levels']){
  uClickTab(v);
  for(let i = 0; i < uModelChips.children.length; i++){
    UREC = uMakeRec();
    uModelChips.children[i].fire('click');
    upump(20);
    uok(UREC.ops.length > 20, v + ' / ' + MODEL_LIST[i].id + ' draws (' + UREC.ops.length + ' ops)');
    uok(UNODES.errbox.style.display !== 'block', v + ' / ' + MODEL_LIST[i].id + ' without error');
    uok(ST.model === MODEL_LIST[i].id, v + ' / the chip actually selected ' + MODEL_LIST[i].id);
  }
}
/* the three de Broglie pictures, on the standing-wave view */
uClickTab('wave');
for(let i = 0; i < uDbChips.children.length; i++){
  UREC = uMakeRec();
  uDbChips.children[i].fire('click');
  uok(UREC.ops.length > 10, 'wave / ' + DB_LIST[i].id + ' draws (' + UREC.ops.length + ' ops)');
  uok(ST.dbRep === DB_LIST[i].id, 'the chip selected ' + DB_LIST[i].id);
}
/* every series */
uClickTab('series');
for(let i = 0; i < uSerChips.children.length; i++){
  UREC = uMakeRec();
  uSerChips.children[i].fire('click');
  uok(UREC.ops.length > 20, 'series / ' + SERIES_LIST[i].id + ' draws (' + UREC.ops.length + ' ops)');
  uok(ST.series === SERIES_LIST[i].id, 'the chip selected series ' + SERIES_LIST[i].id);
}

/* ---- the sliders and checkboxes ---- */
function uFindLabelled(txt){
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.tagName === 'LABEL' && (ch.textContent || '').indexOf(txt) >= 0)
      for(const c2 of ch.children || []) if(c2.tagName === 'INPUT') hit = hit || c2;
    walk(ch); } };
  walk(UNODES.panel); return hit;
}
function uFindSlider(labelText){
  /* match the WHOLE label, not a substring: 'n' would otherwise find
     'wavelength, nm' (Known-bad, lagrange_points) */
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.className === 'sliderrow' && ch.children.length === 3
       && (ch.children[0].textContent || '') === labelText) hit = ch.children[1];
    walk(ch); } };
  walk(UNODES.panel); return hit;
}
for(const nm of ['wavelength, nm', 'random seed', 'wavelengths round the ring', 'n', 'l', 'm',
                 'start from n', 'cascades'])
  uok(!!uFindSlider(nm), 'found the "' + nm + '" slider');
for(const nm of ['the lamp is on', 'time runs', 'the spectrometer', 'mark the nodes', 'log counts'])
  uok(!!uFindLabelled(nm), 'found the "' + nm + '" checkbox');

const uInputs = UNODES.panel.querySelectorAll('input');
uok(uInputs.length >= 14, 'the panel has its sliders and checkboxes (' + uInputs.length + ', floor 14)');
let uCtlErr = null;
try{
  for(const inp of uInputs){
    if(inp.type === 'checkbox'){ inp.checked = !inp.checked; inp.fire('change'); }
    else { inp.value = String(Math.round((parseFloat(inp.min) + parseFloat(inp.max)) / 2));
           inp.fire('input'); }
  }
}catch(e){ uCtlErr = e; }
uok(!uCtlErr, 'every control can be driven without throwing' + (uCtlErr ? ': ' + (uCtlErr.stack || uCtlErr) : ''));
uok(UNODES.errbox.style.display !== 'block', 'and none of them put an error on screen');

/* a slider must REPAINT, not merely not throw: prove idle, fire, assert ops
   were emitted immediately (Known-bad: a drive-every-control sweep that only
   asserts no-throw leaves every slider's repaint unpinned) */
function uClickButton(txt){
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.tagName === 'BUTTON' && (ch.textContent || '') === txt) hit = hit || ch;
    walk(ch); } };
  walk(UNODES.panel);
  if(hit) hit.fire('click');
  return !!hit;
}
uok(uClickButton('reset all'), 'the reset-all button exists and fires');
uClickTab('orbitals');
upump(4);
uok(uFrameGeom(3) === '[]', 'the orbitals view is a still picture: an idle frame paints nothing');
{
  const sl = uFindSlider('n');
  UREC = uMakeRec();
  sl.value = '5'; sl.fire('input');
  uok(UREC.ops.length > 50, 'moving n repaints at once (' + UREC.ops.length + ' ops)');
  uok(ST.n === 5, 'and the model followed the slider');
  /* refresh() draws unconditionally, so the draw above says nothing about the
     dirty flag.  The frame loop is the only path on which it matters, and the
     next pumped frame has to repaint too (Known-bad, three times). */
  UREC = uMakeRec(); upump(3);
  uok(UREC.ops.length > 50, 'and the frame loop repaints it as well (the dirty flag is set)');
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC) === '[]', 'then it goes quiet again');
  /* l and m are bounded by n, and the panel has to clamp them */
  const sll = uFindSlider('l'), slm = uFindSlider('m');
  sll.value = '5'; sll.fire('input');
  uok(ST.l === 4, 'l is clamped to n - 1 by syncPanel (' + ST.l + ')');
  slm.value = '5'; slm.fire('input');
  uok(ST.m === 4, 'm is clamped to l (' + ST.m + ')');
  sl.value = '2'; sl.fire('input');
  uok(ST.l <= 1 && Math.abs(ST.m) <= ST.l, 'lowering n re-clamps l and m (' + ST.l + ',' + ST.m + ')');
}

/* ---- the drags: idle first, then act, then assert it MOVED ---- */
uClickTab('series');
upump(4);
uok(uFrameGeom(3) === '[]', 'the series view is idle before the drag test');
{
  const before = (UREC = uMakeRec(), UNODES.tabs.children[4].fire('click'), uGeom(UREC));
  const lam0 = ST.lam;
  upump(4);
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC) === '[]', 'and idle again after the forced draw (the dirty flag drained)');
  UREC = uMakeRec();
  UNODES.scene.fire('pointerdown', {clientX: 900, clientY: 200});
  UNODES.scene.fire('pointermove', {clientX: 1000, clientY: 200});
  UNODES.scene.fire('pointerup', {});
  upump(3);
  const after = uGeom(UREC);
  uok(after.length > 50, 'a drag across the spectrum repaints (the dirty flag is set)');
  uok(ST.lam !== lam0, 'and it moved the wavelength marker (' + lam0 + ' -> ' + ST.lam + ')');
  uok(after !== before, 'and the picture is a different one');
  /* the marker is clamped to PhET's own 92-780 nm range */
  UNODES.scene.fire('pointerdown', {clientX: 60, clientY: 200});
  UNODES.scene.fire('pointerup', {});
  uok(ST.lam >= PHET.lamMin, 'dragging off the left end clamps at 92 nm (' + ST.lam + ')');
  UNODES.scene.fire('pointerdown', {clientX: 1390, clientY: 200});
  UNODES.scene.fire('pointerup', {});
  uok(ST.lam <= PHET.lamMax, 'dragging off the right end clamps at 780 nm (' + ST.lam + ')');
}
uClickTab('wave');
{
  const nu0 = ST.nu;
  UREC = uMakeRec();
  UNODES.scene.fire('pointerdown', {clientX: 900, clientY: 300});
  UNODES.scene.fire('pointermove', {clientX: 960, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  upump(3);
  uok(uGeom(UREC).length > 30, 'a drag on the mismatch curve repaints');
  uok(ST.nu !== nu0, 'and it moved nu (' + nu0 + ' -> ' + ST.nu + ')');
  uok(ST.nu >= 0.5 && ST.nu <= 7.2, 'nu stays inside its range');
}
uClickTab('box');
{
  /* stop the clock, or the box view repaints every frame and no dirty-flag
     test on it can mean anything */
  const cb0 = uFindLabelled('time runs');
  if(cb0 && cb0.checked){ cb0.checked = false; cb0.fire('change'); }
  upump(4);
  uok(uFrameGeom(3) === '[]', 'with the clock stopped the box view is idle');
  const on0 = ST.lightOn;
  /* fire the pointerdown and pump BEFORE any pointerup: the pointerup handler
     calls refresh(), which draws unconditionally, and that draw masked the
     pointerdown handler's dirty flag entirely (Known-bad, again) */
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC).length > 50, 'a pointerdown ALONE repaints (only that handler sets dirty)');
  UNODES.scene.fire('pointerup', {});
  uok(ST.lightOn !== on0, 'clicking inside the box toggles the lamp');
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  uok(ST.lightOn === on0, 'and clicking again puts it back');
  if(cb0){ cb0.checked = true; cb0.fire('change'); }
}

/* ---- the clock: it runs, it stops, and one step is one tick ---- */
uClickButton('reset all');
uClickTab('box');
{
  const cb = uFindLabelled('time runs');
  if(cb && !cb.checked){ cb.checked = true; cb.fire('change'); }
  const t0 = ATOM.t;
  upump(30);
  uok(ATOM.t > t0, 'with time running the atom advances (' + fmt(ATOM.t - t0, 3) + ' s in 30 frames)');
  cb.checked = false; cb.fire('change');
  const t1 = ATOM.t;
  upump(30);
  uok(ATOM.t === t1, 'with time stopped the atom does not advance');
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC) === '[]', 'and a paused frame paints nothing');
  const ticks0 = ATOM.ticks;
  uok(uClickButton('step'), 'the step button exists');
  uok(ATOM.ticks === ticks0 + 1, 'and one press is exactly one 1/60 s tick');
}
/* the seed makes the run reproducible, and changing it changes the run */
{
  uClickButton('reset all');
  const cb = uFindLabelled('time runs');
  if(cb && !cb.checked){ cb.checked = true; cb.fire('change'); }
  upump(240);
  const runA = ATOM.fired + '|' + ATOM.emitted + '|' + JSON.stringify(ATOM.counts);
  uClickButton('restart atom');
  upump(240);
  const runB = ATOM.fired + '|' + ATOM.emitted + '|' + JSON.stringify(ATOM.counts);
  uok(runA === runB, 'the same seed replays the same run');
  const sd = uFindSlider('random seed');
  uok(ATOM.t > 0, 'the clock has run before the seed is changed');
  sd.value = '777'; sd.fire('input');
  uok(ATOM.t === 0 && ATOM.emitted === 0,
    'changing the seed restarts the atom immediately, not on the next frame');
  upump(240);
  const runC = ATOM.fired + '|' + ATOM.emitted + '|' + JSON.stringify(ATOM.counts);
  uok(runC !== runB, 'a different seed gives a different run');
}

/* ---- reset all really resets ---- */
{
  /* set a NON-default first, or 'it was already at the default' passes for the
     wrong reason (Known-bad: sentinel before the reset) */
  uClickTab('orbitals');
  const sl = uFindSlider('n'); sl.value = '6'; sl.fire('input');
  const slnu = uFindSlider('wavelengths round the ring'); slnu.value = '5.5'; slnu.fire('input');
  uModelChips.children[0].fire('click');
  const cbx = uFindLabelled('the spectrometer');
  if(cbx.checked){ cbx.checked = false; cbx.fire('change'); }
  upump(60);
  uok(ST.n === 6 && ST.nu === 5.5 && ST.model === MODEL_LIST[0].id && !ST.showSpectro,
    'the sentinel state is in place before the reset');
  const tBefore = ATOM.t;
  uok(tBefore > 0 || ST.model === 'billiard', 'the clock had run before the reset');
  uClickButton('reset all');
  uok(ST.n === DEFAULTS.n && ST.nu === DEFAULTS.nu && ST.model === DEFAULTS.model
      && ST.showSpectro === DEFAULTS.showSpectro, 'reset all restores every control');
  uok(ST.view === 'orbitals', 'and it leaves the view where you were');
  uok(ATOM.t === 0 && ATOM.emitted === 0, 'and it restarts the atom');
}

/* ---- the panel hides what a view ignores ---- */
{
  uClickTab('orbitals');
  const qGroup = (function(){
    for(const g of UNODES.panel.children)
      if((g.children[0] && g.children[0].textContent) === 'the quantum numbers') return g;
    return null;
  })();
  uok(!!qGroup, 'found the quantum-numbers group');
  uok(qGroup.hidden === false, 'the quantum numbers are shown on the orbitals view');
  uClickTab('series');
  uok(qGroup.hidden === true, 'and hidden on the series view');
  const eGroup = (function(){
    for(const g of UNODES.panel.children)
      if((g.children[0] && g.children[0].textContent) === 'the ensemble') return g;
    return null;
  })();
  uok(!!eGroup && eGroup.hidden === true, 'the ensemble group is hidden off the rates view');
  uClickTab('rates');
  uok(eGroup.hidden === false, 'and shown on it');
}

/* ---- the line buttons ---- */
uClickTab('box');
uok(uClickButton('Lyman α 122'), 'the Lyman-alpha button exists and fires');
uok(ST.lam === phetLam(1, 2) && ST.light === 'mono', 'and it sets 122 nm monochromatic');
uok(uClickButton('Hα 656'), 'the H-alpha button exists and fires');
uok(ST.lam === phetLam(2, 3), 'and it sets 656 nm');
uok(uClickButton('off a line 300'), 'the off-a-line button exists and fires');
uok(ST.lam === 300 && !transitionForPhetLam(ST.lam), 'and 300 nm really is not a transition');

/* ---- keyboard ---- */
let uKeyErr = null;
try{ for(const k of [' ', 'r', '.', '1', '2', '3', '4', '5', '6'])
  for(const f of (UWINH.keydown || [])) f({key: k, preventDefault(){}});
}catch(e){ uKeyErr = e; }
uok(!uKeyErr, 'keyboard shortcuts run' + (uKeyErr ? ': ' + (uKeyErr.stack || uKeyErr) : ''));
uok(ST.view === TABS[5][0], 'pressing 6 switched to the last view');

/* ---- resize ---- */
let uRsErr = null;
try{ for(const f of (UWINH.resize || [])) f({}); }catch(e){ uRsErr = e; }
uok(!uRsErr, 'the resize handler runs' + (uRsErr ? ': ' + uRsErr : ''));
uok(UNODES.errbox.style.display !== 'block', 'still no error after resize');

/* ---- every view survives every model, after all that ---- */
uClickButton('reset all');
let uSweepErr = null;
try{
  for(let t = 0; t < UNTABS; t++){
    UNODES.tabs.children[t].fire('click');
    for(let i = 0; i < uModelChips.children.length; i++){
      if(uModelChips.hidden) break;
      uModelChips.children[i].fire('click');
      UREC = uMakeRec();
      upump(6);
      UREC = uMakeRec();
      UNODES.tabs.children[t].fire('click');
      uok(UREC.ops.length >= 10, 'view ' + TABS[t][0] + ' / ' + MODEL_LIST[i].id
        + ' draws (' + UREC.ops.length + ' ops)');
      uok(UNODES.errbox.style.display !== 'block', 'view ' + TABS[t][0] + ' / '
        + MODEL_LIST[i].id + ' without error');
    }
  }
}catch(e){ uSweepErr = e; }
uok(!uSweepErr, 'every view x model combination runs' + (uSweepErr ? ': ' + (uSweepErr.stack || uSweepErr) : ''));

console.log('UI: ' + UPASS + ' passed, ' + UFAIL + ' failed');
if(UFAIL > 0) throw new Error(UFAIL + ' UI failure(s)');
