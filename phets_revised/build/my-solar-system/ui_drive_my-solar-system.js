/* ============ UI drive test for my-solar-system.html ==================== *
 * DOM-stub pattern (lineage: build_lagr/ui_drive_lp.js via
 * build/keplers-laws/ui_drive_keplers-laws.js).  It boots the real UI, clicks
 * every tab, drives every slider, checkbox, chip and button, fires the keys,
 * resizes -- and drags a body and the tip of a velocity arrow THROUGH THE
 * FRAME LOOP from a proven-idle baseline, one axis at a time.              */
ObjC.import('Foundation');

let UPASS = 0, UFAIL = 0;
const uok = (c, n) => { if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — ' + n); } };

function makeRecU(){
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
    clip: P, fillRect(x, y, w, h){ ops.push(['r', x, y, w, h]); }, strokeRect(x, y, w, h){ ops.push(['R', x, y, w, h]); },
    clearRect: P,
    fillText(t, x, y){ ops.push(['t', String(t), Math.round(x), Math.round(y)]); }, strokeText: P,
    measureText(t){ const m = /(\d+(?:\.\d+)?)px/.exec(st.font || ''); return {width: ('' + t).length * (m ? parseFloat(m[1]) : 10) * 0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; }
  };
  Object.defineProperty(c, 'font', {get: () => st.font, set: v => st.font = v});
  for(const k of ['fillStyle', 'strokeStyle', 'lineWidth', 'globalAlpha', 'textAlign', 'textBaseline', 'lineJoin', 'lineCap'])
    Object.defineProperty(c, k, {get: () => st[k], set: v => st[k] = v});
  return c;
}
const sigU = c => JSON.stringify(c.ops).length + ':' + c.ops.length;
const geomU = c => JSON.stringify(c.ops.filter(o => o[0] !== 't'));
const entReU = /&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
function assertCleanU(rec, label){
  let bad = null;
  for(const o of rec.ops) if(o[0] === 't'){
    if(entReU.test(o[1])){ bad = 'entity/tag "' + String(o[1]).slice(0, 40) + '"'; break; }
    if(/NaN|undefined/.test(o[1])){ bad = 'NaN/undefined "' + String(o[1]).slice(0, 40) + '"'; break; }
  }
  uok(!bad, label + ' text ops clean' + (bad ? ' (' + bad + ')' : ''));
}
let RECU = makeRecU();
function mkElU(tag){
  const e = {tagName: (tag || 'div').toUpperCase(), children: [], style: {}, dataset: {},
    _h: {}, className: '', id: '', value: '0', checked: false, hidden: false, disabled: false, textContent: '',
    appendChild(c){ this.children.push(c);
      if(c && c.nodeType === 3) this.textContent = (this.textContent || '') + c.textContent;
      else if(c && c.textContent) this.textContent = (this.textContent || '') + c.textContent;
      return c; },
    setAttribute(k, v){ this[k] = v; },
    addEventListener(k, f){ (this._h[k] = this._h[k] || []).push(f); },
    removeEventListener(){}, setPointerCapture(){}, releasePointerCapture(){},
    classList: {_on: {}, add(c){ this._on[c] = 1; }, remove(c){ delete this._on[c]; },
                toggle(c){ this._on[c] ? delete this._on[c] : this._on[c] = 1; }, contains(c){ return !!this._on[c]; }},
    getBoundingClientRect(){ return {left: 0, top: 0, width: 1400, height: 820}; },
    getContext(){ return RECU; },
    querySelector(s){ return this._find(s)[0] || null; },
    querySelectorAll(s){ return this._find(s); },
    _find(s){ const out = []; const want = (s || '').trim();
      const walk = n => { for(const ch of n.children || []){
        if(want === '#info' && ch.id === 'info') out.push(ch);
        else if(want === '#phys' && ch.id === 'phys') out.push(ch);
        else if(want === '.chips' && ch.className === 'chips') out.push(ch);
        else if(want === 'input' && ch.tagName === 'INPUT') out.push(ch);
        walk(ch); } };
      walk(this); return out; },
    fire(k, ev){ for(const f of (this._h[k] || [])) f(Object.assign({preventDefault(){}, stopPropagation(){}, clientX: 0, clientY: 0, pointerId: 1, buttons: 0}, ev || {})); }
  };
  let _html = '';
  Object.defineProperty(e, 'innerHTML', {get(){ return _html; },
    set(v){ _html = '' + v; e.textContent = (typeof plain === 'function') ? plain('' + v) : ('' + v).replace(/<[^>]*>/g, ''); }});
  return e;
}
const NODESU = {};
for(const id of ['scene', 'panel', 'tabs', 'readout', 'eqbar', 'tag', 'hint', 'errbox', 'sub'])
  NODESU[id] = mkElU(id === 'scene' ? 'canvas' : 'div'), NODESU[id].id = id;
globalThis.document = {readyState: 'complete', getElementById: id => NODESU[id] || null, createElement: mkElU,
  createTextNode: t => ({nodeType: 3, textContent: '' + t, children: []}), addEventListener(){}};
const WINHU = {}; let RAFU = null;
globalThis.window = {devicePixelRatio: 1, addEventListener(k, f){ (WINHU[k] = WINHU[k] || []).push(f); },
  requestAnimationFrame(f){ RAFU = f; return 1; }};
globalThis.requestAnimationFrame = f => { RAFU = f; return 1; };
let TNOWU = 0;
function pumpU(n){ for(let i = 0; i < (n || 1); i++){ const f = RAFU; if(!f) return; RAFU = null; TNOWU += 16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown || [])) f({key: k, preventDefault(){}}); }
function findLabelledU(needle){ const out = [];
  const walk = n => { for(const ch of n.children || []){
    if(ch.tagName === 'LABEL' && (ch.textContent || '').indexOf(needle) >= 0) for(const c2 of ch.children || []) if(c2.tagName === 'INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0] || null; }
function sliderRowU(needle){ let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.className === 'sliderrow' && ch.children[0] && (ch.children[0].textContent || '').indexOf(needle) >= 0) hit = ch;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function sliderU(needle){ const r = sliderRowU(needle); return r ? r.children[1] : null; }
function chipU(label, arity){ let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.className === 'chips' && ch.children.length === arity) for(const c of ch.children) if(c.textContent === label) hit = c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ let hit = null;
  const walk = n => { for(const ch of n.children || []){ if(ch.tagName === 'BUTTON' && (ch.textContent || '') === needle) hit = ch; walk(ch); } };
  walk(NODESU.panel); if(hit) hit.fire('click'); return !!hit; }
function idleU(label){ pumpU(3); RECU = makeRecU(); pumpU(3); uok(geomU(RECU) === '[]', label); }
function paintsU(label){ pumpU(1); RECU = makeRecU(); pumpU(2); uok(geomU(RECU).length > 50, label); }
const roU = () => NODESU.readout.innerHTML || '';
function mapU(){ return sysMap(mainBox(RECU, 1400, 820, ST.view), viewRadius()); }

/* ---- boot ---- */
let bootErrU = null;
try{ boot(); }catch(e){ bootErrU = e; }
uok(!bootErrU, 'boot() completes without throwing' + (bootErrU ? ': ' + (bootErrU.stack || bootErrU) : ''));
uok(NODESU.errbox.style.display !== 'block', 'no error captured after boot');
uok(NODESU.tabs.children.length === 4, 'four view tabs were built');
uok(NODESU.panel.children.length >= 7, 'the control panel has its groups (' + NODESU.panel.children.length + ')');
uok(roU().length > 300, 'the readout rendered');
uok((NODESU.eqbar.innerHTML || '').indexOf('NaN') < 0, 'the equation bar has no NaN');
uok(roU().indexOf('4.4567') >= 0, "the readout names PhET's G off the model");
uok(roU().indexOf('2.7498') >= 0, '... and the 2.7498-yr period of its two bodies');

/* ---- every tab draws, differently, cleanly ---- */
const FLOORSU = [14, 14, 30, 30];
const sigsU = {};
for(let i = 0; i < 4; i++){
  RECU = makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length >= FLOORSU[i], 'tab ' + i + ' emits at least ' + FLOORSU[i] + ' ops (' + RECU.ops.length + ')');
  uok(NODESU.errbox.style.display !== 'block', 'tab ' + i + ' drew without error');
  assertCleanU(RECU, 'tab ' + i);
  sigsU['t' + i] = sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size === 4, 'every tab draws a different picture');

/* ---- the clock ---- */
NODESU.tabs.children[0].fire('click');
idleU('the intro view paints nothing while the clock is paused');
{ const rc = findLabelledU('time runs');
  uok(!!rc && rc.checked === false, 'the clock starts paused, as PhET starts');
  rc.checked = true; rc.fire('change');
  uok(ST.running === true, 'ticking it starts the clock');
  paintsU('and every frame paints');
  const t0 = SIM.intro.t; pumpU(6); uok(SIM.intro.t > t0, 'the clock advanced (' + SIM.intro.t.toFixed(5) + ' model units)');
  const ro0 = roU(); pumpU(12); uok(roU() !== ro0, 'the readout refreshes as it runs');
  uok(SIM.intro.paths[1].length > 5, 'and the path is being kept (' + SIM.intro.paths[1].length + ' points)');
  keyU(' '); uok(ST.running === false, 'space pauses'); idleU('and the loop goes idle');
  uok(clickButtonU('clear the paths'), 'found the path eraser');
  uok(SIM.intro.paths[1].length === 0, 'which empties them');
  keyU(' '); pumpU(3); keyU(' '); }

/* ---- the real drags, from a proven-idle baseline ---- */
uok(clickButtonU('reset all'), 'reset all before the drags');
idleU('idle before the body drag');
{ const map = mapU(), x0 = SIM.intro.S.x[1], y0 = SIM.intro.S.y[1];
  /* run first, so "the drag restarts the clock" is not vacuous */
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(10);
  rc.checked = false; rc.fire('change');
  uok(SIM.intro.t > 0, 'the clock is off zero before the drag');
  const bx = SIM.intro.S.x[1], by = SIM.intro.S.y[1];
  NODESU.scene.fire('pointerdown', {clientX: map.X(bx), clientY: map.Y(by)});
  uok(DRAGM.what === 'body' && DRAGM.i === 1, 'pointer-down on the planet grabs it');
  idleU('the grab\'s own repaint has drained (proven-idle baseline)');
  NODESU.scene.fire('pointermove', {clientX: map.X(bx) + 50, clientY: map.Y(by), buttons: 1});
  uok(Math.abs(SIM.intro.S.x[1] - map.wx(map.X(bx) + 50)) < 1e-9, 'the body follows the pointer in x');
  uok(Math.abs(SIM.intro.S.y[1] - by) < 1e-9, '... and stays at the same y: one axis at a time');
  uok(SIM.intro.t === 0, '... and the clock restarted');
  RECU = makeRecU(); pumpU(3);
  uok(geomU(RECU).length > 300, 'the drag repaints THROUGH the frame loop (the dirty flag)');
  idleU('and goes idle again');
  NODESU.scene.fire('pointerup', {});
  uok(DRAGM.what === null, 'pointer-up releases');
  uok(Math.abs(SIM.intro.start[1][1] - SIM.intro.S.x[1]) < 1e-12, '... and saves the new start'); }
uok(clickButtonU('reset all'), 'reset all between the drags');
idleU('idle before the velocity drag');
{ const map = mapU(), i = 1;
  const TX = map.X(SIM.intro.S.x[i]) + SIM.intro.S.vx[i] * VSCALE, TY = map.Y(SIM.intro.S.y[i]) - SIM.intro.S.vy[i] * VSCALE;
  const vy0 = SIM.intro.S.vy[i];
  NODESU.scene.fire('pointerdown', {clientX: TX, clientY: TY});
  uok(DRAGM.what === 'vel' && DRAGM.i === i, 'pointer-down on the arrow tip grabs the velocity');
  idleU('proven-idle baseline before the velocity move');
  NODESU.scene.fire('pointermove', {clientX: TX, clientY: TY + 30, buttons: 1});
  uok(Math.abs(SIM.intro.S.vy[i] - (vy0 - 30 / VSCALE)) < 1e-9, 'the tip sets v exactly: ' + SIM.intro.S.vy[i].toFixed(4)
      + ' = ' + vy0.toFixed(4) + ' - 30 px / ' + VSCALE + ' px per km/s');
  uok(Math.abs(SIM.intro.S.vx[i]) < 1e-12, '... with no sideways velocity from a vertical drag');
  RECU = makeRecU(); pumpU(3);
  uok(geomU(RECU).length > 300, 'the velocity drag repaints through the loop');
  NODESU.scene.fire('pointermove', {clientX: TX + 17, clientY: TY, buttons: 1});
  uok(Math.abs(SIM.intro.S.vx[i] - 17 / VSCALE) < 1e-9, 'a sideways drag sets v_x = 17 px / ' + VSCALE);
  uok(Math.abs(SIM.intro.S.vy[i] - vy0) < 1e-9, '... leaving v_y where it was');
  NODESU.scene.fire('pointerup', {}); }
uok(clickButtonU('reset all'), 'reset all after the drags');
/* the measuring tape */
{ const tc = findLabelledU('measuring tape'); tc.checked = true; tc.fire('change');
  const map = mapU();
  NODESU.scene.fire('pointerdown', {clientX: map.X(SIM.tape.bx), clientY: map.Y(SIM.tape.by)});
  uok(DRAGM.what === 'tapeB', 'the tape tip can be grabbed');
  NODESU.scene.fire('pointermove', {clientX: map.X(2.2), clientY: map.Y(-1.1), buttons: 1});
  uok(Math.abs(SIM.tape.bx - 2.2) < 1e-9 && Math.abs(SIM.tape.by + 1.1) < 1e-9, '... and dragged where the pointer goes');
  NODESU.scene.fire('pointerup', {});
  tc.checked = false; tc.fire('change'); }

/* ---- the masses ---- */
{ const ms = sliderU('body 2 mass');
  uok(!!ms, 'found the body-2 mass slider');
  RECU = makeRecU(); ms.value = '120'; ms.fire('input');
  uok(SIM.intro.S.m[1] === 120, 'the slider sets the mass on the system itself');
  uok(SIM.intro.start[1][0] === 120, '... and on the state restart returns to');
  uok(RECU.ops.length > 10, '... and the view redrew at once (' + RECU.ops.length + ' ops)');
  const two = twoBodyReduce(SIM.intro.S, G_MSS);
  uok(roU().indexOf(fmt(yrOf(two.el.T), 4)) >= 0, 'the readout carries the new period');
  uok(clickButtonU('reset all'), 'reset all after the mass test'); }

/* ---- the lab: the orbital systems ---- */
NODESU.tabs.children[1].fire('click');
uok(ST.view === 'lab', 'on the lab view');
{ const c = chipU('four star ballet', 12);
  uok(!!c, 'found the four star ballet chip');
  RECU = makeRecU(); c.fire('click');
  uok(ST.preset === 'fourStar' && SIM.lab.S.n === 4, 'which loads four bodies');
  uok(ST.nb === 4, '... and sets the body count to match');
  uok(roU().indexOf('four star ballet') >= 0, '... and the readout names it');
  uok(RECU.ops.length > 20, '... redrawn at once');
  assertCleanU(RECU, 'the ballet');
  const com = nbodyCom(SIM.lab.S);
  uok(Math.hypot(com.vx, com.vy) < 1e-12, 'every system loads with its centre of mass at rest, as PhET loads them');
  const h = chipU(plain('“hyperbolic”'), 12);
  uok(!!h, 'found the "hyperbolic" chip');
  h.fire('click');
  uok(ST.preset === 'hyperbolic' && SIM.lab.S.n === 4, 'which loads its four bodies');
  { const mu = G_MSS * SIM.lab.S.m[0];
    const el = conicFromState(SIM.lab.S.x[1] - SIM.lab.S.x[0], SIM.lab.S.y[1] - SIM.lab.S.y[0],
                              SIM.lab.S.vx[1] - SIM.lab.S.vx[0], SIM.lab.S.vy[1] - SIM.lab.S.vy[0], mu);
    uok(el.kind === 'ellipse', '... whose first fly-by is a bound ellipse, not a hyperbola (e = ' + fmt(el.e, 3) + ')'); }
  const n2 = chipU('2', 4);
  uok(!!n2, 'found the body-count chips');
  n2.fire('click');
  uok(SIM.lab.S.n === 2 && ST.preset === 'custom', 'dropping to two bodies makes it a custom system');
  const n4 = chipU('4', 4); n4.fire('click');
  uok(SIM.lab.S.n === 4, '... and four brings two spares back');
  chipU('Sun, planet', 12).fire('click');
  uok(SIM.lab.S.n === 2, 'back to the Sun and planet'); }
{ /* the buttons that move the whole system */
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(20);
  rc.checked = false; rc.fire('change');
  const t0 = SIM.lab.t;
  uok(t0 > 0, 'the lab clock ran');
  uok(clickButtonU('return the bodies'), 'found the return button');
  uok(SIM.lab.t === 0, 'which puts the clock back to zero');
  const c0 = nbodyCom(SIM.lab.S);
  uok(Math.abs(c0.x) > 0.1, 'the Sun-planet system has its centre of mass off the origin');
  uok(clickButtonU('centre-of-mass frame'), 'found the centre-of-mass button');
  const c1 = nbodyCom(SIM.lab.S);
  uok(Math.abs(c1.x) < 1e-12 && Math.hypot(c1.vx, c1.vy) < 1e-12, 'which brings it to the origin and stops it');
  uok(clickButtonU('reset all'), 'reset all after the lab buttons'); }

/* ---- the analysis views ---- */
NODESU.tabs.children[2].fire('click');
uok(ST.view === 'exact', 'on the exact-orbit view');
{ uok(roU().indexOf('exact') >= 0 || roU().indexOf('Kepler') >= 0, 'the readout compares against the exact orbit');
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(40);
  rc.checked = false; rc.fire('change');
  const M = buildModel();
  uok(M.ex && M.ex.err < 1e-8, 'after 40 frames the integration is still on the exact orbit ('
      + M.ex.err.toExponential(2) + ' AU)');
  uok(SIM.ehist.length >= 40, 'the error history grew with the run');
  RECU = makeRecU(); NODESU.tabs.children[2].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /Kepler/.test(o[1])), 'the canvas names the exact solution');
  assertCleanU(RECU, 'the exact view'); }
NODESU.tabs.children[3].fire('click');
uok(ST.view === 'conserve', 'on the conservation view');
{ const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(40);
  rc.checked = false; rc.fire('change');
  const M = buildModel(), c = M.cn;
  uok(c.hist.length >= 40, 'the conservation history grew');
  uok(c.dL < 1e-12 && c.dP < 1e-12, 'L and p are exact to rounding over the run');
  uok(c.shadow && c.shadow.t > 0, "PhET's own step ran beside ours");
  uok(c.order.slope('pefrl') > 3.8 && c.order.slope('phet') < 1.2,
      'the orders measured on this system: PEFRL ' + fmt(c.order.slope('pefrl'), 2) + ', PhET ' + fmt(c.order.slope('phet'), 2));
  RECU = makeRecU(); NODESU.tabs.children[3].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /order/.test(o[1])), 'the canvas prints the measured orders');
  assertCleanU(RECU, 'the conservation view');
  const sc = findLabelledU('PhET');
  uok(!!sc && sc.checked === true, 'the comparison is on by default');
  RECU = makeRecU(); sc.checked = false; sc.fire('change');
  uok(ST.shadow === false && RECU.ops.length > 20, 'and can be turned off');
  sc.checked = true; sc.fire('change'); }

/* ---- the show checkboxes, the zoom, the keys ---- */
NODESU.tabs.children[0].fire('click');
{ const cm = findLabelledU('centre of mass');
  RECU = makeRecU(); cm.checked = true; cm.fire('change');
  uok(ST.com === true && RECU.ops.some(o => o[0] === 't' && /centre of mass/.test(o[1])), 'the centre-of-mass cross is drawn and labelled');
  const gv = findLabelledU('gravity arrows');
  uok(!!gv, 'found the gravity checkbox');
  uok(sliderU('gravity arrows').disabled === true, 'its power slider waits for it');
  gv.checked = true; gv.fire('change');
  uok(sliderU('gravity arrows').disabled === false, '... and is live once the arrows are on');
  const gp = sliderU('gravity arrows'); gp.value = '2'; gp.fire('input');
  uok(ST.fpow === 2, 'the power is set');
  const vt = findLabelledU('the values table');
  vt.checked = true; vt.fire('change');
  uok(roU().indexOf('body 1') >= 0, 'the values table lists the bodies');
  const zs = sliderU('zoom');
  uok(!!zs, 'found the zoom slider');
  const R0 = viewRadius(); zs.value = '1'; zs.fire('input');
  uok(viewRadius() > R0, 'zooming out widens the view (' + fmt(viewRadius(), 2) + ' AU)');
  zs.value = '6'; zs.fire('input');
  uok(viewRadius() < R0, 'and zooming in narrows it');
  zs.value = String(PHET.ZOOM_DEF); zs.fire('input'); }
keyU('2'); uok(ST.view === 'lab', '2 switches to the lab');
keyU('4'); uok(ST.view === 'conserve', '4 is conservation');
keyU('1'); uok(ST.view === 'intro', '1 goes back');
{ const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(6); rc.checked = false; rc.fire('change');
  uok(SIM.intro.t > 0, 'the clock ran before r');
  keyU('r'); uok(SIM.intro.t === 0 && ST.running === false, 'r returns the bodies and pauses'); }
{ const t0 = SIM.intro.t;
  uok(clickButtonU('step'), 'found the step button');
  uok(Math.abs(SIM.intro.t - t0 - PHET.FRAME) < 1e-18, 'one step is one frame at PhET’s rate');
  uok(ST.running === false, '... and leaves the clock paused'); }
{ const sc = chipU('slow', 3); uok(!!sc, 'found the speed chips'); sc.fire('click');
  uok(ST.speed === 'slow', 'slow selected');
  const t0 = SIM.intro.t; clickButtonU('step');
  uok(Math.abs(SIM.intro.t - t0 - PHET.FRAME * 0.25) < 1e-18, 'and a step is a quarter as long');
  chipU('normal', 3).fire('click'); }

/* ---- every control, every tab, resize, reset ---- */
let ctlErrU = null;
try{
  const inputs = NODESU.panel.querySelectorAll('input');
  uok(inputs.length === 16, 'the panel has its 6 sliders and 10 checkboxes (' + inputs.length + ')');
  for(const inp of inputs){
    if(inp.type === 'checkbox' || inp.disabled) continue;
    const lo = parseFloat(inp.min), hi = parseFloat(inp.max);
    for(const v of [lo, hi, (lo + hi) / 2]){ inp.value = String(v); inp.fire('input');
      uok(NODESU.errbox.style.display !== 'block', 'slider at ' + v + ' draws without error'); }
  }
  for(const inp of inputs){ if(inp.type !== 'checkbox' || inp.disabled) continue; inp.checked = !inp.checked; inp.fire('change'); }
  for(let v = 0; v < 4; v++){ RECU = makeRecU(); NODESU.tabs.children[v].fire('click'); assertCleanU(RECU, 'after the control sweep, tab ' + v); }
  for(const f of (WINHU.resize || [])) f();
  uok(NODESU.errbox.style.display !== 'block', 'resize handled');
  NODESU.tabs.children[1].fire('click');
  chipU('trojan asteroids', 12).fire('click');
  uok(ST.preset === 'trojan', 'the trojans are loaded before the reset');
  uok(clickButtonU('reset all'), 'found reset all');
  uok(ST.preset === 'sunPlanet' && ST.zoom === PHET.ZOOM_DEF && ST.speed === 'normal' && ST.path === true,
      'reset all restores the defaults');
  uok(ST.view === 'lab', 'and keeps the view');
  uok(SIM.lab.S.n === 2 && Math.abs(SIM.lab.S.x[1] - 2) < 1e-12, 'including the Sun-planet system itself');
  uok(chipU('Sun, planet', 12).className === 'chip on', 'syncChips restored the system chips');
}catch(e){ ctlErrU = e; }
uok(!ctlErrU, 'control sweep completes' + (ctlErrU ? ': ' + (ctlErrU.stack || ctlErrU) : ''));

console.log('UI: ' + UPASS + ' passed, ' + UFAIL + ' failed');
if(UFAIL > 0) throw new Error(UFAIL + ' UI failure(s)');
