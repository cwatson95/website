/* ============ UI drive test for gravity-and-orbits.html ================ *
 * DOM-stub pattern (lineage: build_lagr/ui_drive_lp.js via
 * build/keplers-laws/ and build/my-solar-system/).  It boots the real UI,
 * clicks every tab, drives every slider, checkbox, chip and button, fires the
 * keys, resizes -- and drags a body and the tip of a velocity arrow THROUGH
 * THE FRAME LOOP from a proven-idle baseline, one axis at a time.          */
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
/* EXACT match on the decoded label, never a substring: "PhET" appears in the gravity
   checkbox's label as well as the comparison one, and "mass" in three of them -- a substring
   finder drove the wrong control and failed an assertion for a reason with nothing to do with
   the sim (the Known-bad entry from lenses.html, met again here). */
function findLabelledU(label){ const out = [];
  const walk = n => { for(const ch of n.children || []){
    if(ch.tagName === 'LABEL' && plain(ch.textContent || '') === label)
      for(const c2 of ch.children || []) if(c2.tagName === 'INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0] || null; }
function sliderRowU(needle){ let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.className === 'sliderrow' && ch.children[0] && plain(ch.children[0].textContent || '') === needle) hit = ch;
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
function mapU(){ return sysMap(mainBox(RECU, 1400, 820, ST.view), buildModel()); }

/* ---- boot ---- */
let bootErrU = null;
try{ boot(); }catch(e){ bootErrU = e; }
uok(!bootErrU, 'boot() completes without throwing' + (bootErrU ? ': ' + (bootErrU.stack || bootErrU) : ''));
uok(NODESU.errbox.style.display !== 'block', 'no error captured after boot');
uok(NODESU.tabs.children.length === 5, 'five view tabs were built');
uok(NODESU.panel.children.length >= 8, 'the control panel has its groups (' + NODESU.panel.children.length + ')');
uok(roU().length > 300, 'the readout rendered');
uok((NODESU.eqbar.innerHTML || '').indexOf('NaN') < 0, 'the equation bar has no NaN');
uok(roU().indexOf('6.67408') >= 0, "the readout names PhET's G");
uok(roU().indexOf('1727.4') >= 0 && roU().indexOf('1737.4') >= 0,
    "... and both Moon radii, PhET's and NASA's");
uok(roU().indexOf('1 Earth mass') >= 0, "... and PhET's own Earth-mass readout");

/* ---- every tab draws, differently, cleanly ---- */
const FLOORSU = [14, 20, 20, 20, 20];
const sigsU = {};
for(let i = 0; i < 5; i++){
  RECU = makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length >= FLOORSU[i], 'tab ' + i + ' emits at least ' + FLOORSU[i] + ' ops (' + RECU.ops.length + ')');
  uok(NODESU.errbox.style.display !== 'block', 'tab ' + i + ' drew without error');
  assertCleanU(RECU, 'tab ' + i);
  sigsU['t' + i] = sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size === 5, 'every tab draws a different picture');

/* ---- the clock ---- */
NODESU.tabs.children[0].fire('click');
idleU('the model view paints nothing while the clock is paused');
{ const rc = findLabelledU('time runs');
  uok(!!rc && rc.checked === false, 'the clock starts paused, as PhET starts');
  rc.checked = true; rc.fire('change');
  uok(ST.running === true, 'ticking it starts the clock');
  paintsU('and every frame paints');
  const t0 = SIM.model.t; pumpU(6); uok(SIM.model.t > t0, 'the clock advanced (' + fmt(SIM.model.t / PH.DAY, 3) + ' d)');
  const ro0 = roU(); pumpU(12); uok(roU() !== ro0, 'the readout refreshes as it runs');
  uok(SIM.model.paths[1].length > 5, 'and the path is being kept (' + SIM.model.paths[1].length + ' points)');
  keyU(' '); uok(ST.running === false, 'space pauses'); idleU('and the loop goes idle');
  uok(clickButtonU('clear the path'), 'found the path eraser');
  uok(SIM.model.paths[1].length === 0, 'which empties it');
  uok(clickButtonU('return the bodies'), 'found the return button');
  uok(SIM.model.t === 0, '... which puts the clock back to zero'); }

/* ---- gravity off: PhET's switch, and what it does ---- */
{ const gc = findLabelledU('gravity acts (PhET\u2019s on/off switch)');
  uok(!!gc && gc.checked === true, 'gravity starts on, as PhET starts it');
  const sys = SIM.model, v0 = Math.hypot(sys.S.vx[1], sys.S.vy[1]);
  const ux = sys.S.vx[1] / v0, uy = sys.S.vy[1] / v0, x0 = sys.S.x[1], y0 = sys.S.y[1];
  gc.checked = false; gc.fire('change');
  uok(ST.gravity === false, 'unticking it switches gravity off');
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change');
  pumpU(120);
  rc.checked = false; rc.fire('change');
  const dx = sys.S.x[1] - x0, dy = sys.S.y[1] - y0;
  uok(Math.hypot(dx, dy) > 0, 'and the planet moves');
  uok(Math.abs(dx * uy - dy * ux) / Math.hypot(dx, dy) < 1e-13,
      '... in an exactly straight line (' + (Math.abs(dx * uy - dy * ux) / Math.hypot(dx, dy)).toExponential(2) + ' off it)');
  uok(Math.abs(Math.hypot(sys.S.vx[1], sys.S.vy[1]) - v0) === 0, '... at exactly constant speed');
  RECU = makeRecU(); NODESU.tabs.children[0].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /gravity is OFF/.test(o[1])), '... and the canvas says gravity is off');
  gc.checked = true; gc.fire('change');
  uok(ST.gravity === true, 'and it switches back on');
  keyU('g'); uok(ST.gravity === false, 'the g key flips it too');
  keyU('g'); }
{ /* cutting gravity MID-ORBIT is the thing PhET's switch is for: the body must stay where it
     is, keep the clock it has, and leave along the tangent from there */
  uok(clickButtonU('reset all'), 'reset all before the mid-orbit cut');
  const sys = SIM.model, rc = findLabelledU('time runs');
  rc.checked = true; rc.fire('change'); pumpU(200); rc.checked = false; rc.fire('change');
  const tCut = sys.t, xCut = sys.S.x[1], yCut = sys.S.y[1];
  const vx = sys.S.vx[1], vy = sys.S.vy[1], v = Math.hypot(vx, vy);
  uok(tCut > 0 && Math.abs(yCut) > 1e9, 'the planet is well round its orbit before the cut');
  const gc2 = findLabelledU('gravity acts (PhET’s on/off switch)');
  gc2.checked = false; gc2.fire('change');
  uok(sys.t === tCut, 'cutting gravity does NOT rewind the clock');
  uok(sys.S.x[1] === xCut && sys.S.y[1] === yCut, '... and does not move the planet');
  rc.checked = true; rc.fire('change'); pumpU(200); rc.checked = false; rc.fire('change');
  const dx = sys.S.x[1] - xCut, dy = sys.S.y[1] - yCut;
  uok(Math.abs(dx * vy / v - dy * vx / v) / Math.hypot(dx, dy) < 1e-13,
      '... and it leaves along the tangent AT THE CUT, not from the start');
  uok(Math.abs(Math.hypot(sys.S.vx[1], sys.S.vy[1]) - v) === 0, '... at exactly the speed it had');
  /* NOT "exactly zero" here: the start states have their velocity along an axis, so the cross
     product is exactly zero there, but a cut in mid-orbit has a general direction and the
     residual is rounding -- the canvas prints the measured number either way */
  uok(sys.coast.dev / sys.coast.travel < 1e-13, '... with the measured residual at '
      + (sys.coast.dev / sys.coast.travel).toExponential(2) + ' of the path');
  gc2.checked = true; gc2.fire('change'); }
uok(clickButtonU('reset all'), 'reset all after the gravity test');

/* ---- the real drags, from a proven-idle baseline ---- */
NODESU.tabs.children[0].fire('click');
idleU('idle before the body drag');
{ const map = mapU();
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(10);
  rc.checked = false; rc.fire('change');
  uok(SIM.model.t > 0, 'the clock is off zero before the drag');
  const bx = SIM.model.S.x[1], by = SIM.model.S.y[1];
  NODESU.scene.fire('pointerdown', {clientX: map.X(bx), clientY: map.Y(by)});
  uok(DRAGM.what === 'body' && DRAGM.i === 1, 'pointer-down on the planet grabs it');
  idleU("the grab's own repaint has drained (proven-idle baseline)");
  NODESU.scene.fire('pointermove', {clientX: map.X(bx) + 50, clientY: map.Y(by), buttons: 1});
  uok(Math.abs(SIM.model.S.x[1] - map.wx(map.X(bx) + 50)) < 1e-3, 'the body follows the pointer in x');
  uok(Math.abs(SIM.model.S.y[1] - by) < 1e-6, '... and stays at the same y: one axis at a time');
  uok(SIM.model.t === 0, '... and the clock restarted');
  RECU = makeRecU(); pumpU(3);
  uok(geomU(RECU).length > 300, 'the drag repaints THROUGH the frame loop (the dirty flag)');
  /* the whole point of the dragging class: a move that reports NO buttons still belongs to
     the drag in progress.  Without it the handler returns early -- and a mutant that removed
     the class survived a sweep, because every move the harness fired carried buttons: 1. */
  const bx2 = SIM.model.S.x[1];
  NODESU.scene.fire('pointermove', {clientX: map.X(bx) + 80, clientY: map.Y(by), buttons: 0});
  uok(Math.abs(SIM.model.S.x[1] - map.wx(map.X(bx) + 80)) < 1e-3,
      'a move reporting no buttons still moves the body: that is what the dragging class is for');
  uok(SIM.model.S.x[1] !== bx2, '... and it really moved');
  NODESU.scene.fire('pointermove', {clientX: map.X(bx) + 50, clientY: map.Y(by), buttons: 1});
  idleU('and goes idle again');
  NODESU.scene.fire('pointerup', {});
  uok(DRAGM.what === null, 'pointer-up releases');
  uok(Math.abs(SIM.model.start[1][1] - SIM.model.S.x[1]) < 1e-6, '... and saves the new start'); }
uok(clickButtonU('reset all'), 'reset all between the drags');
idleU('idle before the velocity drag');
{ const map = mapU(), i = 1, vs = velScale(SIM.model);
  const TX = map.X(SIM.model.S.x[i]) + SIM.model.S.vx[i] * vs, TY = map.Y(SIM.model.S.y[i]) - SIM.model.S.vy[i] * vs;
  const vy0 = SIM.model.S.vy[i];
  NODESU.scene.fire('pointerdown', {clientX: TX, clientY: TY});
  uok(DRAGM.what === 'vel' && DRAGM.i === i, 'pointer-down on the V tip grabs the velocity');
  idleU('proven-idle baseline before the velocity move');
  NODESU.scene.fire('pointermove', {clientX: TX, clientY: TY + 30, buttons: 1});
  uok(Math.abs(SIM.model.S.vy[i] - (vy0 - 30 / vs)) < 1e-6, 'the tip sets v exactly: '
      + fmt(SIM.model.S.vy[i], 2) + ' = ' + fmt(vy0, 2) + ' - 30 px / ' + sigf(vs, 4) + ' px per m/s');
  uok(Math.abs(SIM.model.S.vx[i]) < 1e-9, '... with no sideways velocity from a vertical drag');
  RECU = makeRecU(); pumpU(3);
  uok(geomU(RECU).length > 300, 'the velocity drag repaints through the loop');
  NODESU.scene.fire('pointermove', {clientX: TX + 17, clientY: TY, buttons: 1});
  uok(Math.abs(SIM.model.S.vx[i] - 17 / vs) < 1e-6, 'a sideways drag sets v_x = 17 px / the scale');
  uok(Math.abs(SIM.model.S.vy[i] - vy0) < 1e-6, '... leaving v_y where it was');
  NODESU.scene.fire('pointerup', {}); }
uok(clickButtonU('reset all'), 'reset all after the drags');
/* the measuring tape */
{ const tc = findLabelledU('measuring tape'); tc.checked = true; tc.fire('change');
  const map = mapU(), sys = SIM.model;
  NODESU.scene.fire('pointerdown', {clientX: map.X(sys.tape.bx), clientY: map.Y(sys.tape.by)});
  uok(DRAGM.what === 'tapeB', 'the tape tip can be grabbed');
  const wx = map.wx(map.X(sys.tape.bx) + 40), wy = map.wy(map.Y(sys.tape.by) - 25);
  NODESU.scene.fire('pointermove', {clientX: map.X(sys.tape.bx) + 40, clientY: map.Y(sys.tape.by) - 25, buttons: 1});
  uok(Math.abs(sys.tape.bx - wx) < 1e-6 && Math.abs(sys.tape.by - wy) < 1e-6, '... and dragged where the pointer goes');
  RECU = makeRecU(); NODESU.tabs.children[0].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /km/.test(o[1])), '... and the tape reads in kilometres, as PhET does');
  NODESU.scene.fire('pointerup', {});
  tc.checked = false; tc.fire('change'); }
uok(clickButtonU('reset all'), 'reset all after the tape');

/* ---- the systems and the screens ---- */
{ const c = chipU('Planet and Space Station', 4);
  uok(!!c, 'found the Planet-and-Space-Station chip');
  RECU = makeRecU(); c.fire('click');
  uok(ST.system === 'planetSatellite' && SIM.model.S.n === 2, 'which loads the Earth and the station');
  uok(roU().indexOf('Space Station') >= 0, '... and the readout names it');
  uok(RECU.ops.length > 20, '... redrawn at once');
  assertCleanU(RECU, 'the station system');
  uok(roU().indexOf('Earth minutes') >= 0, "... and the clock reads Earth minutes here, as PhET's does");
  const el = SIM.model.ref.el;
  uok(Math.abs(el.T / 60 - 91.4) < 0.2, "the station's orbit is 91.4 min (" + fmt(el.T / 60, 2) + ')');
  const c3 = chipU('Sun, Planet and Moon', 4); c3.fire('click');
  uok(ST.system === 'starPlanetMoon' && SIM.model.S.n === 3, 'three bodies for Sun, Planet and Moon');
  uok(SIM.model.ref === null, '... and no closed form for them');
  uok(SIM.model.S.boost === 10200, "... and the Model screen's 10200 boost is in force");
  uok(sliderU('body 3 mass').disabled === true, "... and its moon's mass slider is dead, as PhET builds it");
  uok(sliderU('body 2 mass').disabled === false, '... while the planet’s is live');
  const c1 = chipU('Sun and Planet', 4); c1.fire('click');
  uok(ST.system === 'starPlanet', 'back to the Sun and the planet'); }
{ /* the screen chips: live on the analysis views, disabled on the two PhET screens */
  NODESU.tabs.children[0].fire('click');
  const ms = chipU('Model', 2), ts = chipU('To Scale', 2);
  uok(!!ms && !!ts, 'found the screen chips');
  uok(ms.disabled === true, '... disabled on the Model tab, where the tab IS the screen');
  NODESU.tabs.children[2].fire('click');
  uok(ms.disabled === false, '... and live on the analysis views');
  RECU = makeRecU(); ts.fire('click');
  uok(ST.screen === 'scale' && curKey() === 'scale', 'To Scale selects the To Scale system');
  uok(RECU.ops.length > 20, '... redrawn at once');
  /* and landing on a PhET screen's own tab selects that screen -- the tab IS the screen there */
  NODESU.tabs.children[0].fire('click');
  uok(ST.screen === 'model' && curKey() === 'model', 'the Model tab selects the Model screen');
  NODESU.tabs.children[1].fire('click');
  uok(ST.screen === 'scale' && curKey() === 'scale', '... and the To Scale tab the To Scale one');
  NODESU.tabs.children[2].fire('click');
  ms.fire('click'); }

/* ---- to scale: the honest picture ---- */
NODESU.tabs.children[1].fire('click');
uok(ST.view === 'scale', 'on the To Scale view');
{ RECU = makeRecU(); NODESU.tabs.children[1].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /true sizes/.test(o[1])), 'the canvas prints the true drawn sizes');
  uok(RECU.ops.some(o => o[0] === 't' && /one pixel/.test(o[1])), '... and marks the one-pixel line');
  /* TWO ops reading exactly "Earth": the legend entry and the pointer's own label.  Checking
     for one of them matched the legend and let the pointer rule be deleted (a sweep proved it). */
  uok(RECU.ops.filter(o => o[0] === 't' && o[1] === 'Earth').length >= 2,
      '... and points at the Earth, which is a fortieth of a pixel (legend + pointer label)');
  assertCleanU(RECU, 'to scale');
  const cfg = sceneCfg('scale', 'starPlanet');
  uok(cfg.bodies[1].r === PH.EARTH_RADIUS, 'the To Scale Earth is its true radius');
  uok(sceneCfg('model', 'starPlanet').bodies[1].r === 800 * PH.EARTH_RADIUS, '... against 800x on the Model screen'); }

/* ---- the analysis views ---- */
NODESU.tabs.children[2].fire('click');
uok(ST.view === 'circ', 'on the circular-orbit view');
{ const vs = sliderU('v / v_c');
  uok(!!vs, 'found the v/v_c slider');
  RECU = makeRecU(); vs.value = '1'; vs.fire('input');
  const M = buildModel();
  uok(Math.abs(M.ci.el.e) < 1e-15, 'at exactly 1.00 the orbit is a circle (e = ' + M.ci.el.e.toExponential(1) + ')');
  uok(RECU.ops.length > 20, '... redrawn at once');
  vs.value = '1.42'; vs.fire('input');
  uok(buildModel().ci.el.kind !== 'ellipse', 'past sqrt(2) it is unbound');
  RECU = makeRecU(); NODESU.tabs.children[2].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /unbound/.test(o[1])), '... and the canvas says so');
  vs.value = '0.5'; vs.fire('input');
  const slow = buildModel().ci.el;
  uok(slow.kind === 'ellipse' && Math.abs(slow.Q - buildModel().ci.r) < 1e-3 * buildModel().ci.r,
      'below v_c the start is apoapsis');
  vs.value = '1'; vs.fire('input');
  RECU = makeRecU(); NODESU.tabs.children[2].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /slope 3\/2/.test(o[1])), 'the third-law panel names its slope');
  assertCleanU(RECU, 'the circular-orbit view'); }
NODESU.tabs.children[3].fire('click');
uok(ST.view === 'exact', 'on the exact-orbit view');
{ const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(60);
  rc.checked = false; rc.fire('change');
  const M = buildModel();
  uok(M.ex && M.ex.err < 1e-6 * M.sep, 'after 60 frames the integration is still on the exact orbit ('
      + (M.ex.err / M.sep).toExponential(2) + ' of r)');
  uok(SIM.ehist.length >= 60, 'the error history grew with the run');
  RECU = makeRecU(); NODESU.tabs.children[3].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /Kepler/.test(o[1])), 'the canvas names the exact solution');
  assertCleanU(RECU, 'the exact view');
  chipU('Sun, Planet and Moon', 4).fire('click');
  RECU = makeRecU(); NODESU.tabs.children[3].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /two bodies/.test(o[1])),
      '... and says plainly that three bodies have no closed form');
  chipU('Sun and Planet', 4).fire('click'); }
NODESU.tabs.children[4].fire('click');
uok(ST.view === 'cons', 'on the conservation view');
{ const ms = chipU('To Scale', 2); ms.fire('click');
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(60);
  rc.checked = false; rc.fire('change');
  const c = buildModel().cn;
  uok(c.hist.length >= 60, 'the conservation history grew');
  uok(c.dL < 1e-12 && c.dP < 1e-12, 'L and p are exact to rounding on the To Scale screen');
  uok(c.shadow && c.shadow.t > 0, "PhET's own step ran beside ours");
  uok(c.order.slope('pefrl') > 3.8 && c.order.slope('phet') < 1.2,
      'the orders measured here: PEFRL ' + fmt(c.order.slope('pefrl'), 2) + ', PhET ' + fmt(c.order.slope('phet'), 2));
  RECU = makeRecU(); NODESU.tabs.children[4].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /order/.test(o[1])), 'the canvas prints the measured orders');
  assertCleanU(RECU, 'the conservation view');
  const sc = findLabelledU('run PhET\u2019s own step beside ours');
  uok(!!sc && sc.checked === true, 'the comparison is on by default');
  RECU = makeRecU(); sc.checked = false; sc.fire('change');
  uok(ST.shadow === false && RECU.ops.length > 20, 'and can be turned off');
  sc.checked = true; sc.fire('change');
  /* and the Model screen is measurably not conserved */
  chipU('Model', 2).fire('click');
  const rc2 = findLabelledU('time runs'); rc2.checked = true; rc2.fire('change'); pumpU(80);
  rc2.checked = false; rc2.fire('change');
  const c2 = buildModel().cn;
  uok(c2.broken.length > 0, 'the Model screen declares what it bends');
  uok(c2.dP > 1e-4, '... and its momentum is measurably not conserved (' + c2.dP.toExponential(2) + ')');
  RECU = makeRecU(); NODESU.tabs.children[4].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /Model screen/.test(o[1])), '... and the canvas says why');
  chipU('To Scale', 2).fire('click'); }
uok(clickButtonU('reset all'), 'reset all after the analysis views');

/* ---- the masses ---- */
NODESU.tabs.children[0].fire('click');
{ const ms = sliderU('body 1 mass');
  uok(!!ms, 'found the body-1 mass slider');
  RECU = makeRecU(); ms.value = '2'; ms.fire('input');
  uok(Math.abs(SIM.model.S.m[0] - 2 * PH.SUN_MASS) < 1e18, 'the slider doubles the star');
  uok(Math.abs(SIM.model.start[0][0] - 2 * PH.SUN_MASS) < 1e18, '... and on the state restart returns to');
  uok(RECU.ops.length > 10, '... and the view redrew at once (' + RECU.ops.length + ' ops)');
  ms.value = '0.5'; ms.fire('input');
  uok(SIM.model.ref.el.kind === 'hyperbola', 'halving it sets the Earth free (a hyperbola)');
  uok(roU().indexOf('hyperbola') >= 0, '... and the readout says so');
  ms.value = '1'; ms.fire('input');
  uok(SIM.model.ref.el.kind === 'ellipse', 'and back to an ellipse');
  uok(clickButtonU('reset all'), 'reset all after the mass test'); }

/* ---- the show checkboxes, the zoom, the keys ---- */
{ const cm = findLabelledU('centre of mass');
  RECU = makeRecU(); cm.checked = true; cm.fire('change');
  uok(ST.com === true && RECU.ops.some(o => o[0] === 't' && /centre of mass/.test(o[1])),
      'the centre-of-mass cross is drawn and labelled');
  const gv = findLabelledU('gravity-force arrows');
  uok(!!gv, 'found the gravity-arrow checkbox');
  uok(sliderU('gravity arrows ×10^n').disabled === true, 'its power slider waits for it');
  gv.checked = true; gv.fire('change');
  uok(sliderU('gravity arrows ×10^n').disabled === false, '... and is live once the arrows are on');
  const gp = sliderU('gravity arrows ×10^n'); gp.value = '2'; gp.fire('input');
  uok(ST.fpow === 2, 'the power is set');
  const mo = findLabelledU('mass');
  mo.checked = true; mo.fire('change');
  RECU = makeRecU(); NODESU.tabs.children[0].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /Earth mass/.test(o[1])), "the mass readout is PhET's own wording");
  const zs = sliderU('zoom');
  uok(!!zs, 'found the zoom slider');
  const R0 = viewRadius(SIM.model); zs.value = String(PH.ZOOM_MIN); zs.fire('input');
  uok(viewRadius(SIM.model) > R0, 'zooming out widens the view');
  zs.value = String(PH.ZOOM_MAX); zs.fire('input');
  uok(viewRadius(SIM.model) < R0, 'and zooming in narrows it');
  zs.value = '1'; zs.fire('input'); }
keyU('2'); uok(ST.view === 'scale', '2 switches to To Scale');
keyU('5'); uok(ST.view === 'cons', '5 is conservation');
keyU('1'); uok(ST.view === 'model', '1 goes back');
{ const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(6); rc.checked = false; rc.fire('change');
  uok(SIM.model.t > 0, 'the clock ran before r');
  keyU('r'); uok(SIM.model.t === 0 && ST.running === false, 'r returns the bodies and pauses'); }
{ const t0 = SIM.model.t;
  uok(clickButtonU('step'), 'found the step button');
  uok(Math.abs(SIM.model.t - t0 - frameDt(SIM.model.cfg, 4)) < 1e-9, "one step is one frame at PhET's normal rate");
  uok(ST.running === false, '... and leaves the clock paused'); }
{ const sc = chipU('slow', 3); uok(!!sc, 'found the speed chips'); sc.fire('click');
  uok(ST.speed === 0, 'slow selected');
  const t0 = SIM.model.t; clickButtonU('step');
  uok(Math.abs(SIM.model.t - t0 - frameDt(SIM.model.cfg, 1)) < 1e-9, 'and a step is a quarter as long');
  chipU('fast', 3).fire('click');
  const t1 = SIM.model.t; clickButtonU('step');
  uok(Math.abs(SIM.model.t - t1 - frameDt(SIM.model.cfg, 7)) < 1e-9, '... and fast is seven substeps, as PhET has it');
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
  for(let v = 0; v < 5; v++){ RECU = makeRecU(); NODESU.tabs.children[v].fire('click'); assertCleanU(RECU, 'after the control sweep, tab ' + v); }
  for(const f of (WINHU.resize || [])) f();
  uok(NODESU.errbox.style.display !== 'block', 'resize handled');
  NODESU.tabs.children[0].fire('click');
  chipU('Planet and Moon', 4).fire('click');
  uok(ST.system === 'planetMoon', 'the Planet-and-Moon system is loaded before the reset');
  uok(clickButtonU('reset all'), 'found reset all');
  uok(ST.system === 'starPlanet' && ST.zoom === 1 && ST.speed === 1 && ST.gravity === true && ST.path === true,
      'reset all restores the defaults');
  uok(ST.view === 'model', 'and keeps the view');
  uok(SIM.model.S.n === 2 && Math.abs(SIM.model.S.x[1] - PH.EARTH_X) < 1, 'including PhET’s Sun and Planet');
  uok(chipU('Sun and Planet', 4).className === 'chip on', 'syncChips restored the system chips');
}catch(e){ ctlErrU = e; }
uok(!ctlErrU, 'control sweep completes' + (ctlErrU ? ': ' + (ctlErrU.stack || ctlErrU) : ''));

console.log('UI: ' + UPASS + ' passed, ' + UFAIL + ' failed');
if(UFAIL > 0) throw new Error(UFAIL + ' UI failure(s)');
