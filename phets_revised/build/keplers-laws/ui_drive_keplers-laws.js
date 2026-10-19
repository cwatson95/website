/* ============ UI drive test for keplers-laws.html ======================= *
 * DOM-stub pattern (lineage: build_lagr/ui_drive_lp.js, with the
 * innerHTML -> textContent fix the shared tools/ui_drive.js still lacks).
 * It boots the real UI, clicks every tab, drives every slider, checkbox,
 * chip and button, fires the keys, resizes -- and, the part that matters,
 * drags the planet and the tip of its velocity arrow THROUGH THE FRAME LOOP
 * from a proven-idle baseline, one axis at a time.                         */
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
  /* a browser derives textContent from innerHTML; the stub does the same through plain() */
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
/* the planet and the tip of its velocity arrow, in canvas pixels */
function planetPxU(){
  const b = mainBox(RECU, 1400, 820, ST.view), map = orbitMap(b, viewRadius());
  const M = buildModel();
  return {b, map, PX: map.X(M.now.x), PY: map.Y(M.now.y),
          TX: map.X(M.now.x) + M.now.vx * VSCALE, TY: map.Y(M.now.y) - M.now.vy * VSCALE};
}

/* ---- boot ---- */
let bootErrU = null;
try{ boot(); }catch(e){ bootErrU = e; }
uok(!bootErrU, 'boot() completes without throwing' + (bootErrU ? ': ' + (bootErrU.stack || bootErrU) : ''));
uok(NODESU.errbox.style.display !== 'block', 'no error captured after boot');
uok(NODESU.tabs.children.length === 5, 'five view tabs were built');
uok(NODESU.panel.children.length >= 11, 'the control panel has its groups (' + NODESU.panel.children.length + ')');
uok(roU().length > 300, 'the readout rendered');
uok((NODESU.eqbar.innerHTML || '').indexOf('NaN') < 0, 'the equation bar has no NaN');
uok(roU().indexOf('1.5000') >= 0, 'the readout prints a = 1.5000 AU off the model');
uok(roU().indexOf('our Sun') >= 0, 'and names our Sun');

/* ---- every tab draws, differently, cleanly ---- */
const FLOORSU = [20, 30, 30, 30, 30];   /* derived from what each view emits at 1400x820 */
const sigsU = {};
for(let i = 0; i < 5; i++){
  RECU = makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length >= FLOORSU[i], 'tab ' + i + ' emits at least ' + FLOORSU[i] + ' ops (' + RECU.ops.length + ')');
  uok(NODESU.errbox.style.display !== 'block', 'tab ' + i + ' drew without error');
  assertCleanU(RECU, 'tab ' + i);
  sigsU['t' + i] = sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size === 5, 'every tab draws a different picture');

/* ---- the clock: still while paused, painting while it runs ---- */
NODESU.tabs.children[0].fire('click');
idleU('the first law view paints nothing while the clock is paused');
{ const rc = findLabelledU('time runs');
  uok(!!rc && rc.checked === false, 'the clock is paused by default, as PhET starts');
  rc.checked = true; rc.fire('change');
  uok(ST.running === true, 'ticking it starts the clock');
  paintsU('and the view paints every frame');
  const t0 = SIM.t; pumpU(5); uok(SIM.t > t0, 'the clock advanced (' + SIM.t.toFixed(4) + ' yr)');
  const ro0 = roU(); pumpU(12); uok(roU() !== ro0, 'the readout refreshes as the clock runs');
  keyU(' '); uok(ST.running === false, 'space pauses'); idleU('and the loop goes idle');
  keyU(' '); uok(ST.running === true, 'space resumes'); keyU(' '); }

/* ---- the REAL drags, from a proven-idle baseline, one at a time ---- */
NODESU.tabs.children[0].fire('click');
uok(clickButtonU('reset all'), 'reset all before the drags');
idleU('idle before the planet drag');
{ /* run the clock first: "the drag restarts the clock" cannot be tested at t = 0 */
  const rc0 = findLabelledU('time runs'); rc0.checked = true; rc0.fire('change'); pumpU(12);
  rc0.checked = false; rc0.fire('change');
  uok(SIM.t > 0, 'the clock is off zero before the drag (' + SIM.t.toFixed(4) + ' yr)');
  const p = planetPxU(), px0 = buildModel().now.x, py0 = buildModel().now.y;
  NODESU.scene.fire('pointerdown', {clientX: p.PX, clientY: p.PY});
  uok(DRAGK.what === 'planet', 'pointer-down on the planet grabs it');
  idleU('the grab\'s own repaint has drained (proven-idle baseline)');
  NODESU.scene.fire('pointermove', {clientX: p.PX - 60, clientY: p.PY, buttons: 1});
  uok(ST.px < px0 - 0.2, 'the move dragged the planet inward (' + ST.px.toFixed(3) + ' AU)');
  uok(Math.abs(ST.py - py0) < 1e-9, '... at the height it was grabbed at: one axis at a time');
  uok(SIM.t === 0, '... and it restarted the clock');
  RECU = makeRecU(); pumpU(3);
  uok(geomU(RECU).length > 400, 'the drag repaints THROUGH the frame loop (the dirty flag)');
  idleU('and goes idle again');
  NODESU.scene.fire('pointerup', {});
  uok(DRAGK.what === null, 'pointer-up releases');
  uok(roU().indexOf(sigf(klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular).a, 6)) >= 0, 'the readout followed the drag (a)'); }
uok(clickButtonU('reset all'), 'reset all between the drags');
idleU('idle before the velocity drag');
{ const p = planetPxU(), vy0 = ST.vy;
  NODESU.scene.fire('pointerdown', {clientX: p.TX, clientY: p.TY});
  uok(DRAGK.what === 'vel', 'pointer-down on the arrow tip grabs the velocity');
  idleU('proven-idle baseline before the velocity move');
  NODESU.scene.fire('pointermove', {clientX: p.TX, clientY: p.TY + 40, buttons: 1});
  /* the value, not just the direction: "it went down" passes for a wrong scale and even for
     a flipped sign (the mutation sweep proved both) */
  uok(Math.abs(ST.vy - (vy0 - 40 / VSCALE)) < 1e-9, 'the tip drag sets v exactly: ' + ST.vy.toFixed(4)
      + ' km/s = ' + vy0.toFixed(4) + ' - 40 px / ' + VSCALE + ' px per km/s');
  uok(Math.abs(ST.vx) < 1e-12, '... with no sideways velocity from a vertical drag');
  RECU = makeRecU(); pumpU(3);
  uok(geomU(RECU).length > 400, 'the velocity drag repaints through the loop');
  const el = klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular);
  uok(el.a < 1.4, '... and the orbit shrank (a = ' + el.a.toFixed(3) + ' AU)');
  /* now one across, to pin the x component of the same scale */
  NODESU.scene.fire('pointermove', {clientX: p.TX + 25, clientY: p.TY, buttons: 1});
  uok(Math.abs(ST.vx - 25 / VSCALE) < 1e-9, 'a sideways drag sets v_x = 25 px / ' + VSCALE
      + ' = ' + ST.vx.toFixed(4) + ' km/s');
  uok(Math.abs(ST.vy - vy0) < 1e-9, '... leaving v_y where it was');
  NODESU.scene.fire('pointerup', {}); }
/* the escape cap: drag the tip far out and PhET's 0.99 v_esc holds */
uok(clickButtonU('reset all'), 'reset all before the escape drag');
{ const p = planetPxU();
  NODESU.scene.fire('pointerdown', {clientX: p.TX, clientY: p.TY});
  NODESU.scene.fire('pointermove', {clientX: p.TX, clientY: p.TY - 400, buttons: 1});
  NODESU.scene.fire('pointerup', {});
  const el = klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular);
  uok(Math.abs(el.vKms / el.vescKms - 0.99) < 1e-9, 'a wild velocity drag is capped at 0.99 v_esc (PhET\'s rule)');
  uok(!el.allowed && el.escaping, '... and the orbit is flagged as escaping');
  pumpU(3); uok(roU().indexOf('escape') >= 0, '... which the readout says');
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change');
  const t0 = SIM.t; pumpU(6); uok(SIM.t === t0, '... and the clock will not run on it (PhET disables play)');
  rc.checked = false; rc.fire('change'); }
uok(clickButtonU('reset all'), 'reset all after the escape drag');
/* the measuring tape */
{ const tc = findLabelledU('measuring tape'); tc.checked = true; tc.fire('change');
  const b = mainBox(RECU, 1400, 820, ST.view), map = orbitMap(b, viewRadius());
  NODESU.scene.fire('pointerdown', {clientX: map.X(SIM.tape.bx), clientY: map.Y(SIM.tape.by)});
  uok(DRAGK.what === 'tapeB', 'the tape\'s tip can be grabbed');
  NODESU.scene.fire('pointermove', {clientX: map.X(2.4), clientY: map.Y(-0.8), buttons: 1});
  uok(Math.abs(SIM.tape.bx - 2.4) < 1e-9 && Math.abs(SIM.tape.by + 0.8) < 1e-9, '... and dragged where the pointer goes');
  NODESU.scene.fire('pointerup', {});
  tc.checked = false; tc.fire('change'); }

/* ---- the first-law checkboxes, and the ones that gate others ---- */
{ const fc = findLabelledU('foci'), sc = findLabelledU('string');
  uok(!!fc && !!sc, 'found the foci and string checkboxes');
  uok(sc.disabled === true, 'the string is disabled until the foci are shown');
  fc.checked = true; fc.fire('change');
  uok(ST.foci === true && sc.disabled === false, 'ticking the foci enables the string');
  RECU = makeRecU(); sc.checked = true; sc.fire('change');
  uok(ST.string === true && RECU.ops.length > 20, 'the string redraws at once (' + RECU.ops.length + ' ops)');
  uok(RECU.ops.some(o => o[0] === 't' && /d₁/.test(o[1])), '... and labels d₁ on the canvas');
  const ac = findLabelledU('axes'), mc = findLabelledU('semiaxes');
  uok(mc.disabled === true, 'the semiaxes wait for the axes');
  ac.checked = true; ac.fire('change'); mc.checked = true; mc.fire('change');
  uok(ST.axes && ST.semiaxes && mc.disabled === false, 'both on');
  const ec = findLabelledU('eccentricity'); ec.checked = true; ec.fire('change');
  uok(ST.ecc === true, 'the eccentricity segment is on');
  assertCleanU(RECU, 'the first law with every overlay'); }

/* ---- the second law ---- */
NODESU.tabs.children[1].fire('click');
uok(ST.view === 'second', 'on the second law view');
{ const ds = sliderU('period divisions');
  uok(!!ds, 'found the divisions slider');
  RECU = makeRecU(); ds.value = '6'; ds.fire('input');
  uok(ST.div === 6 && RECU.ops.length > 20, 'six divisions, redrawn at once (' + RECU.ops.length + ' ops)');
  uok(roU().indexOf('6') >= 0, 'the readout says six');
  const M = buildModel();
  uok(Math.abs(M.sec.full - PI * M.el.a * M.el.b / 6) < 1e-12, 'each sector is pi a b / 6');
  const av = findLabelledU('area values'), tv = findLabelledU('time values');
  av.checked = true; av.fire('change'); tv.checked = true; tv.fire('change');
  RECU = makeRecU(); pumpU(1); NODESU.tabs.children[1].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /AU²/.test(o[1])), 'the area values are written on the sectors');
  assertCleanU(RECU, 'the second law with values');
  /* play erases the sectors and they fill again */
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change');
  uok(SIM.sweep.erased === true, 'pressing play erases the areas, as PhET does');
  pumpU(30);
  const M2 = buildModel(), filled = M2.sec.frac.filter(f => f > 0).length;
  uok(filled >= 1 && filled <= 3, 'a few sectors have filled after 30 frames (' + filled + ')');
  uok(M2.sec.frac.every(f => f <= 1 + 1e-12), 'no sector goes past its own area');
  rc.checked = false; rc.fire('change');
  uok(clickButtonU('erase the sectors'), 'found the eraser');
  { /* PhET fills a sector from its own cut, so right after an erase only the sector the planet
       is in shows anything, and exactly the part between its cut and the planet */
    const M3 = buildModel(), D = TAU / M3.sec.N, Mn = M3.el.M0 + M3.el.n * SIM.t;
    const k = ((Math.floor(Mn / D) % M3.sec.N) + M3.sec.N) % M3.sec.N;
    const want = (Mn - Math.floor(Mn / D) * D) / D;
    uok(Math.abs(M3.sec.frac[k] - want) < 1e-12, 'which leaves only the part between the last cut and the planet');
    uok(M3.sec.frac.filter((f, i) => i !== k && f > 1e-12).length === 0, '... and every other sector empty'); }
  const ap = findLabelledU('apoapsis'), pe = findLabelledU('periapsis');
  uok(ap.disabled === false, 'the apsides are live on an eccentric orbit');
  ap.checked = true; ap.fire('change'); pe.checked = true; pe.fire('change');
  RECU = makeRecU(); NODESU.tabs.children[1].fire('click');
  uok(RECU.ops.some(o => o[0] === 't' && /periapsis/.test(o[1])), 'and are labelled on the orbit');
  const cc = findLabelledU('hold the orbit circular'); cc.checked = true; cc.fire('change');
  uok(ST.circular === true && buildModel().el.e < 1e-12, 'held circular, e is zero');
  uok(findLabelledU('apoapsis').disabled === true, '... and the apsides go dead, as PhET disables them');
  cc.checked = false; cc.fire('change'); }

/* ---- the third law ---- */
NODESU.tabs.children[2].fire('click');
uok(ST.view === 'third', 'on the third law view');
{ uok(roU().indexOf('T') >= 0, 'the readout carries the period');
  const p3 = chipU('3', 3);
  uok(!!p3, 'found a power chip row');
  /* the a-power row comes first; set a^3 then T^2 */
  const rows = [];
  const walk = n => { for(const ch of n.children || []){ if(ch.className === 'chips' && ch.children.length === 3
      && ch.children[0].textContent === '1') rows.push(ch); walk(ch); } };
  walk(NODESU.panel);
  uok(rows.length === 2, 'both power rows found (' + rows.length + ')');
  RECU = makeRecU(); rows[0].children[2].fire('click');
  uok(ST.pa === 3 && RECU.ops.length > 20, 'a^3 chosen and redrawn (' + RECU.ops.length + ' ops)');
  rows[1].children[1].fire('click');
  uok(ST.pt === 2, 'T^2 chosen');
  const M = buildModel();
  uok(M.thd.th.correct, 'the model knows this is the right pair');
  uok(Math.abs(M.thd.th.ratio - klConst(ST.mass)) < 1e-12, 'and the ratio is 4 pi^2/GM');
  uok(roU().indexOf(fmt(klConst(ST.mass), 5)) >= 0, 'which the readout prints');
  const ll = findLabelledU('log–log axes');
  uok(!!ll, 'found the log-log checkbox');
  RECU = makeRecU(); ll.checked = true; ll.fire('change');
  uok(ST.loglog === true && RECU.ops.length > 20, 'log-log redraws (' + RECU.ops.length + ' ops)');
  uok(RECU.ops.some(o => o[0] === 't' && /slope/.test(o[1])), '... and prints the measured slope');
  uok(RECU.ops.some(o => o[0] === 't' && /Jupiter/.test(o[1])), '... with PhET\'s planets on the line');
  ll.checked = false; ll.fire('change');
  /* the target orbits */
  const jc = chipU('Jupiter', 6);
  uok(!!jc, 'found the Jupiter target chip');
  jc.fire('click');
  uok(ST.target === 'jupiter', 'Jupiter is the target');
  uok(roU().indexOf('11.858') >= 0, 'the readout gives its period, 11.858 yr');
  uok(clickButtonU('put the planet on it'), 'found the "put the planet on it" button');
  { const el = klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular);
    uok(Math.abs(el.a - 5.2) < 1e-9 && Math.abs(el.e - 0.0484) < 1e-9, 'which puts it on Jupiter\'s orbit exactly');
    uok(Math.abs(el.T - periodOf(5.2, starMu(1))) < 1e-12, '... with Jupiter\'s period'); }
  chipU('none', 6).fire('click');
  uok(clickButtonU('forget the trace'), 'found the trace eraser');
  uok(Math.abs(SIM.trace.aMin - SIM.trace.aMax) < 1e-12, 'which forgets every visited a but the current one');
  const zf = chipU('far', 2); zf.fire('click'); uok(ST.zoom === 'far', 'zoomed out');
  chipU('near', 2).fire('click'); }

/* ---- all laws, and Kepler's equation ---- */
NODESU.tabs.children[3].fire('click');
uok(ST.view === 'all', 'on all laws');
{ const sw = findLabelledU('swept sectors');
  uok(!!sw && sw.checked === true, 'the sectors are on by default here');
  RECU = makeRecU(); sw.checked = false; sw.fire('change');
  uok(ST.swept === false && RECU.ops.length > 20, 'they can be turned off (' + RECU.ops.length + ' ops)');
  sw.checked = true; sw.fire('change'); }
NODESU.tabs.children[4].fire('click');
uok(ST.view === 'anom', 'on Kepler’s equation');
{ const ms = sliderU('t through one period');
  uok(!!ms, 'found the scrub slider');
  RECU = makeRecU(); ms.value = '0.5'; ms.fire('input');
  const M = buildModel();
  uok(Math.abs(M.an.M - PI) < 1e-9, 'half a period is a mean anomaly of pi (' + M.an.M.toFixed(6) + ')');
  uok(Math.abs(M.an.E - PI) < 1e-9, '... where E is pi too, whatever e');
  uok(RECU.ops.length > 40, 'and the construction redrew');
  ms.value = '0.18'; ms.fire('input');
  const M2 = buildModel();
  uok(M2.an.E > M2.an.M && M2.an.nu > M2.an.E, 'before apoapsis M < E < nu, as the construction shows');
  uok(M2.an.it <= 8 && Math.abs(M2.an.res) < 1e-14, 'Newton converged in ' + M2.an.it + ' steps, residual ' + M2.an.res.toExponential(1));
  uok(M2.an.stop >= 0 && M2.an.stop + 1 <= M2.an.it, 'PhET’s 0.01-rad stop comes earlier (' + (M2.an.stop + 1) + ' steps)');
  RECU = makeRecU(); NODESU.tabs.children[4].fire('click');
  assertCleanU(RECU, 'the anomaly view');
  uok(RECU.ops.some(o => o[0] === 't' && /E =/.test(o[1])), 'E is labelled on the construction');
  /* the drag is refused here, and the slider is the control */
  const before = JSON.stringify([ST.px, ST.py, ST.vx, ST.vy]);
  NODESU.scene.fire('pointerdown', {clientX: 600, clientY: 400});
  NODESU.scene.fire('pointermove', {clientX: 500, clientY: 300, buttons: 1});
  NODESU.scene.fire('pointerup', {});
  uok(JSON.stringify([ST.px, ST.py, ST.vx, ST.vy]) === before, 'the anomaly view ignores the pointer, as designed');
  /* the clock drives the slider */
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change');
  const f0 = ST.mfrac; pumpU(20);
  uok(ST.mfrac !== f0, 'the running clock moves the scrub slider with it');
  rc.checked = false; rc.fire('change'); }

/* ---- the star mass, the stopwatch, the steppers ---- */
NODESU.tabs.children[0].fire('click');
uok(clickButtonU('reset all'), 'reset all before the mass tests');
{ const ms = sliderU('mass');
  uok(!!ms, 'found the mass slider');
  RECU = makeRecU(); ms.value = '1.8'; ms.fire('input');
  uok(ST.mass === 1.8 && RECU.ops.length > 20, 'a heavier star, redrawn at once (' + RECU.ops.length + ' ops)');
  const el = klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular);
  uok(el.T < 1.5, 'the period fell with the heavier star (' + el.T.toFixed(3) + ' yr)');
  uok(roU().indexOf('1.80') >= 0, 'the readout carries the mass');
  ms.value = '1.02'; ms.fire('input');
  uok(ST.mass === 1, 'within 5 % the slider snaps to our Sun, as PhET snaps it');
  ms.value = '0.5'; ms.fire('input');
  { const e2 = buildModel().el;
    uok(ST.mass === 0.5 && Math.abs(e2.a - 3) < 1e-9, 'at half the mass the same launch doubles a to 3 AU (' + e2.a.toFixed(4) + ')');
    uok(e2.allowed && e2.vKms / e2.vescKms < 0.9801, '... still short of PhET\'s escape flag'); }
  ms.value = '1'; ms.fire('input'); }
{ const sc = findLabelledU('stopwatch'); sc.checked = true; sc.fire('change');
  uok(clickButtonU('stopwatch start/stop'), 'found the stopwatch button');
  uok(SIM.swRun === true, 'which starts it');
  const rc = findLabelledU('time runs'); rc.checked = true; rc.fire('change'); pumpU(10);
  uok(SIM.sw > 0, 'and it counts with the clock (' + SIM.sw.toFixed(4) + ' yr)');
  rc.checked = false; rc.fire('change');
  uok(clickButtonU('zero it'), 'found the zero button');
  uok(SIM.sw === 0 && SIM.swRun === false, 'which zeroes and stops it');
  sc.checked = false; sc.fire('change'); }
{ const t0 = SIM.t;
  uok(clickButtonU('step'), 'found the step button');
  uok(Math.abs(SIM.t - t0 - PHET.FRAME_YR) < 1e-15, 'one step is one frame at PhET’s rate');
  uok(ST.running === false, '... and leaves the clock paused');
  uok(clickButtonU('restart'), 'found restart');
  uok(SIM.t === 0, 'which returns the planet to where the orbit was set'); }

/* ---- every control, every tab, resize, reset ---- */
let ctlErrU = null;
try{
  const inputs = NODESU.panel.querySelectorAll('input');
  uok(inputs.length === 25, 'the panel has its 4 sliders and 21 checkboxes (' + inputs.length + ')');
  for(const inp of inputs){
    if(inp.type === 'checkbox' || inp.disabled) continue;
    const lo = parseFloat(inp.min), hi = parseFloat(inp.max);
    for(const v of [lo, hi, (lo + hi) / 2]){ inp.value = String(v); inp.fire('input');
      uok(NODESU.errbox.style.display !== 'block', 'slider at ' + v + ' draws without error'); }
  }
  for(const inp of inputs){ if(inp.type !== 'checkbox' || inp.disabled) continue;
    inp.checked = !inp.checked; inp.fire('change'); }
  for(let v = 0; v < 5; v++){ RECU = makeRecU(); NODESU.tabs.children[v].fire('click'); assertCleanU(RECU, 'after the control sweep, tab ' + v); }
  for(const f of (WINHU.resize || [])) f();
  uok(NODESU.errbox.style.display !== 'block', 'resize handled');
  keyU('3'); uok(ST.view === 'third', '3 switches to the third law');
  keyU('5'); uok(ST.view === 'anom', '5 is Kepler’s equation');
  keyU('1'); uok(ST.view === 'first', '1 goes back');
  keyU('r'); uok(SIM.t === 0 && ST.running === false, 'r restarts and pauses');
  chipU('slow', 3).fire('click'); uok(ST.speed === 'slow', 'the speed chips work');
  uok(clickButtonU('reset all'), 'found reset all');
  uok(ST.mass === 1 && ST.div === 4 && ST.target === 'none' && ST.speed === 'normal' && ST.pa === 1 && ST.pt === 1,
     'reset all restores the defaults');
  uok(ST.view === 'first', 'and keeps the view');
  uok(Math.abs(ST.px - 2) < 1e-12 && Math.abs(ST.vy - V_DEF) < 1e-12, 'including the default orbit');
  uok(chipU('normal', 3).className === 'chip on', 'syncChips restored the speed chips');
}catch(e){ ctlErrU = e; }
uok(!ctlErrU, 'control sweep completes' + (ctlErrU ? ': ' + (ctlErrU.stack || ctlErrU) : ''));

console.log('UI: ' + UPASS + ' passed, ' + UFAIL + ' failed');
if(UFAIL > 0) throw new Error(UFAIL + ' UI failure(s)');
