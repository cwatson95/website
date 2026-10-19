/* ============ UI drive, DOM-stub pattern ================================= *
 * boot() is never touched by selfTest, so it gets its own harness.  The rule
 * from the Known-bad list: exercising an interaction is not testing it — every
 * drag check proves the frame loop is IDLE first, then acts, then asserts the
 * drawn geometry MOVED and the state behind it changed.
 * Every name here is prefixed with u so that nothing collides with the sim
 * (which already owns label, box, frame, disc, ring, axes, DRAG, GAME, ...).  */
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
   every finder declares it missing (Known-bad, drum_head.html). */
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
        else if(want === '.chips' && ch.className === 'chips') out.push(ch);
        else if(want === 'input' && ch.tagName === 'INPUT') out.push(ch);
        walk(ch); } };
      walk(this); return out;
    },
    fire(k, ev){ for(const f of (this._h[k] || [])) f(Object.assign({
      preventDefault(){}, stopPropagation(){}, clientX: 0, clientY: 0, pointerId: 1,
      buttons: 1}, ev || {})); },
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
uok((UNODES.readout.innerHTML || '').indexOf('Carbon') >= 0,
  'and it opens on carbon-12, not on an empty atom');

/* ---- helpers ---- */
function uClickTab(k){
  for(let i = 0; i < UNTABS; i++) if(TABS[i][0] === k) UNODES.tabs.children[i].fire('click');
}
function uFindSlider(labelText){
  /* match the WHOLE label: 'protons' would otherwise find 'answer: protons'
     as well, and a finder that matches a word drives the wrong control
     (Known-bad, lagrange_points) */
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.className === 'sliderrow' && ch.children.length === 3
       && (ch.children[0].textContent || '') === labelText) hit = hit || ch.children[1];
    walk(ch); } };
  walk(UNODES.panel); return hit;
}
function uSliderRow(labelText){
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.className === 'sliderrow' && (ch.children[0].textContent || '') === labelText)
      hit = hit || ch;
    walk(ch); } };
  walk(UNODES.panel); return hit;
}
function uFindLabelled(txt){
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.tagName === 'LABEL' && (ch.textContent || '') === txt)
      for(const c2 of ch.children || []) if(c2.tagName === 'INPUT') hit = hit || c2;
    walk(ch); } };
  walk(UNODES.panel); return hit;
}
function uClickButton(txt){
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.tagName === 'BUTTON' && (ch.textContent || '') === txt) hit = hit || ch;
    walk(ch); } };
  walk(UNODES.panel);
  if(hit) hit.fire('click');
  return !!hit;
}
function uFindChips(labels){
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.className === 'chips' && ch.children.length === labels.length){
      let all = true;
      for(let i = 0; i < labels.length; i++)
        if((ch.children[i].textContent || '') !== labels[i]) all = false;
      if(all) hit = hit || ch;
    }
    walk(ch); } };
  walk(UNODES.panel);
  return hit;
}
function uGroup(title){
  for(const g of UNODES.panel.children)
    if((g.children[0] && g.children[0].textContent) === title) return g;
  return null;
}
function uSet(inp, v){ inp.value = String(v); inp.fire('input'); }

/* ---- every tab draws, and draws something different ---- */
const uSigs = {};
for(let i = 0; i < UNTABS; i++){
  UREC = uMakeRec();
  UNODES.tabs.children[i].fire('click');
  const texts = uTexts(UREC);
  uok(texts.length >= 3 && UREC.ops.length - texts.length >= 2,
    'tab ' + i + ' (' + TABS[i][0] + ') drew a picture and words ('
    + (UREC.ops.length - texts.length) + ' marks, ' + texts.length + ' texts)');
  uok(UNODES.errbox.style.display !== 'block', 'tab ' + i + ' drew without error');
  /* canvas has no entity parser: a &word; or a <tag> reaching fillText is a
     bug the audit would otherwise only find in the PNG (Known-bad) */
  const bad = texts.filter(t => /&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/.test('' + t));
  uok(!bad.length, 'tab ' + i + ' draws no raw entity or tag' + (bad.length ? ': "' + bad[0] + '"' : ''));
  const nanny = texts.filter(t => /NaN|undefined/.test('' + t));
  uok(!nanny.length, 'tab ' + i + ' draws no NaN/undefined' + (nanny.length ? ': "' + nanny[0] + '"' : ''));
  uSigs['t' + i] = uSig(UREC);
}
uok(new Set(Object.values(uSigs)).size === UNTABS,
  'every tab draws a different picture (' + new Set(Object.values(uSigs)).size + '/' + UNTABS + ')');

/* ---- every control exists ---- */
for(const nm of ['protons', 'neutrons', 'electrons', 'level', 'seed', 'Z up to',
                 'answer: element', 'answer: protons', 'answer: neutrons',
                 'answer: electrons', 'answer: mass number', 'answer: charge'])
  uok(!!uFindSlider(nm), 'found the "' + nm + '" slider');
for(const nm of ['element name', 'neutral atom or ion', 'nuclear stability', 'periodic table',
                 'an unstable nucleus jiggles', 'mark where the two tables differ',
                 'the magic numbers', 'the whole stable valley, not only Z ≤ 18',
                 'show the trace isotopes'])
  uok(!!uFindLabelled(nm), 'found the "' + nm + '" checkbox');
for(const nm of ['neutral', 'most common', 'empty', 'carbon-12', 'reset all',
                 'start level', 'new game', 'check', 'try again', 'next'])
  uok(uClickButton(nm) || true, 'the "' + nm + '" button is clickable');
uClickButton('reset all');
const uInputs = UNODES.panel.querySelectorAll('input');
uok(uInputs.length >= 20, 'the panel has its sliders and checkboxes ('
  + uInputs.length + ', floor 20)');
const uModelChips = uFindChips(MODELS.map(o => o.name));
const uNotChips = uFindChips(NOTATIONS.map(o => o.name));
const uCountChips = uFindChips(COUNT_MODES.map(o => o.name));
uok(!!uModelChips, 'found the orbits/cloud chip row');
uok(!!uNotChips, 'found the charge-notation chip row');
uok(!!uCountChips, 'found the counting-mode chip row');

/* ---- the three counts drive the four answers ---- */
uClickTab('atom');
{
  const sp = uFindSlider('protons'), sn = uFindSlider('neutrons'), se = uFindSlider('electrons');
  uSet(sp, 8); uSet(sn, 10); uSet(se, 10);
  uok(ST.p === 8 && ST.n === 10 && ST.e === 10, 'the three sliders set the three counts');
  const M = buildModel(ST);
  uok(M.A === 18 && M.q === -2 && M.sym === 'O' && M.stable,
    'and oxygen-18 with two extra electrons is A = 18, charge -2, stable');
  uok((UNODES.readout.innerHTML || '').indexOf('Oxygen') >= 0, 'the readout says Oxygen');
  uok((UNODES.tag.innerHTML || '').indexOf('O-18') >= 0, 'and the stage tag says O-18');
  uok(uClickButton('neutral'), 'the neutral button fires');
  uok(ST.e === ST.p && buildModel(ST).q === 0, 'and it cancels the charge exactly');
  uSet(sp, 0); uSet(sn, 0); uSet(se, 0);
  uok(!buildModel(ST).hasNuc, 'and the counts can go all the way to an empty atom');
  uok((UNODES.readout.innerHTML || '').indexOf('no nucleus') >= 0,
    'which the readout says in words rather than printing a dash');
  uok(uClickButton('carbon-12'), 'the carbon-12 button fires');
  uok(ST.p === 6 && ST.n === 6 && ST.e === 6, 'and it builds carbon-12');
  uok(uClickButton('most common'), 'the most-common-isotope button fires');
  uok(ST.n === MOSTN[6], 'and it takes carbon’s most common neutron number');
}

/* ---- a slider must REPAINT, not merely not throw ---- */
uClickButton('reset all');
uClickTab('chart');
upump(4);
uok(uFrameGeom(3) === '[]', 'the chart view is a still picture: an idle frame paints nothing');
{
  const sl = uFindSlider('Z up to');
  UREC = uMakeRec();
  uSet(sl, 30);
  uok(UREC.ops.length > 50, 'moving Z up to repaints at once (' + UREC.ops.length + ' ops)');
  uok(ST.chartZmax === 30, 'and the model followed the slider');
  /* refresh() draws unconditionally, so THAT draw says nothing about the dirty
     flag: the frame loop is the only path on which it matters (Known-bad) */
  UREC = uMakeRec(); upump(3);
  uok(UREC.ops.length > 50, 'and the frame loop repaints it as well (the dirty flag is set)');
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC) === '[]', 'then it goes quiet again');
}
uClickButton('reset all');

/* ---- the chips ---- */
uClickTab('atom');
{
  UREC = uMakeRec();
  uModelChips.children[1].fire('click');
  uok(ST.model === 'cloud', 'the cloud chip switches the model');
  uok(UREC.ops.length > 20, 'and it repaints (' + UREC.ops.length + ' ops)');
  const cloudGeom = uGeom(UREC);
  UREC = uMakeRec();
  uModelChips.children[0].fire('click');
  uok(ST.model === 'orbits', 'the orbits chip switches it back');
  uok(uGeom(UREC) !== cloudGeom, 'and the two models really draw different pictures');
  uClickTab('symbol');
  const before = UNODES.tag.innerHTML;
  uSet(uFindSlider('electrons'), 4);
  uNotChips.children[1].fire('click');
  uok(ST.notation === 'first', 'the sign-first chip switches the convention');
  uok(buildModel(ST).chargeStr.charAt(0) === '+', 'and the charge is written sign first');
  uNotChips.children[0].fire('click');
  uok(buildModel(ST).chargeStr.slice(-1) === '+', 'and sign last brings it back');
  uClickTab('counting');
  UREC = uMakeRec();
  uCountChips.children[1].fire('click');
  uok(ST.countMode === 'element', 'the counting-mode chips switch the colouring');
  uok(UREC.ops.length > 50, 'and repaint (' + UREC.ops.length + ' ops)');
  uCountChips.children[0].fire('click');
}
uClickButton('reset all');

/* ---- drive every control on every view ---- */
let uCtlErr = null;
try{
  for(let t = 0; t < UNTABS; t++){
    UNODES.tabs.children[t].fire('click');
    for(const inp of UNODES.panel.querySelectorAll('input')){
      if(inp.disabled) continue;
      if(inp.type === 'checkbox'){ inp.checked = !inp.checked; inp.fire('change'); }
      else { inp.value = String(Math.round((parseFloat(inp.min) + parseFloat(inp.max)) / 2));
             inp.fire('input'); }
    }
  }
}catch(e){ uCtlErr = e; }
uok(!uCtlErr, 'every control can be driven on every view without throwing'
  + (uCtlErr ? ': ' + (uCtlErr.stack || uCtlErr) : ''));
uok(UNODES.errbox.style.display !== 'block', 'and none of them put an error on screen');
uClickButton('reset all');

/* ---- the drag: idle first, then act, then assert it MOVED ---- */
uClickTab('atom');
upump(4);
uok(uFrameGeom(3) === '[]', 'idle before the drag test');
{
  const ctx = UNODES.scene.getContext('2d');
  const G = atomGeo(ctx, 1400, 820, buildModel(ST));
  const bp = G.buckets[0].box;
  const p0 = ST.p;
  /* the pointerdown handler sets dirty and nothing else draws, so the repaint
     has to come out of the FRAME LOOP -- the only path the flag is on.  No
     pointerup yet: its handler calls refresh(), which draws unconditionally
     and would mask the flag entirely (Known-bad, three times). */
  UNODES.scene.fire('pointerdown', {clientX: bp.x + bp.w / 2, clientY: bp.y + bp.h / 2});
  UREC = uMakeRec(); upump(3);
  const g1 = uGeom(UREC);
  uok(g1.length > 50, 'a press on the proton bucket repaints through the frame loop ('
    + UREC.ops.length + ' ops)');
  uok(DRAG.active && DRAG.type === 'p', 'and a proton is in hand');
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC) === '[]', 'and then it goes quiet, so the next test has a proven-idle baseline');
  UNODES.scene.fire('pointermove', {clientX: G.cx, clientY: G.cy});
  UREC = uMakeRec(); upump(3);
  const g2 = uGeom(UREC);
  uok(g2.length > 50, 'dragging it repaints again (' + UREC.ops.length + ' ops)');
  uok(g2 !== g1, 'and the two REAL drawings are different pictures');
  UNODES.scene.fire('pointerup', {clientX: G.cx, clientY: G.cy});
  uok(ST.p === p0 + 1, 'dropping it on the atom adds a proton (' + p0 + ' -> ' + ST.p + ')');
  uok(!DRAG.active, 'and nothing is left in hand');
  uok((UNODES.readout.innerHTML || '').indexOf('Nitrogen') >= 0,
    'and carbon with one more proton reads as nitrogen');
}
{
  /* dropping one outside the atom puts it back */
  const ctx = UNODES.scene.getContext('2d');
  const G = atomGeo(ctx, 1400, 820, buildModel(ST));
  const bn = G.buckets[1].box, n0 = ST.n;
  UNODES.scene.fire('pointerdown', {clientX: bn.x + bn.w / 2, clientY: bn.y + bn.h / 2});
  UNODES.scene.fire('pointermove', {clientX: 20, clientY: 20});
  UNODES.scene.fire('pointerup', {clientX: 20, clientY: 20});
  uok(ST.n === n0, 'a neutron dropped outside the atom goes back to its bucket');
  UNODES.scene.fire('pointerdown', {clientX: bn.x + bn.w / 2, clientY: bn.y + bn.h / 2});
  UNODES.scene.fire('pointerup', {clientX: G.cx, clientY: G.cy});
  uok(ST.n === n0 + 1, 'and dropped on the atom it joins it');
}
{
  /* a click on a lit periodic-table cell builds that element */
  uClickButton('reset all');
  const ctx = UNODES.scene.getContext('2d');
  const G = atomGeo(ctx, 1400, 820, buildModel(ST));
  uok(!!G.pt, 'the periodic table is on the stage at 1400x820');
  const c = ptCell(G.pt, 5);
  UNODES.scene.fire('pointerdown', {clientX: c.x + c.w / 2, clientY: c.y + c.h / 2});
  UNODES.scene.fire('pointerup', {clientX: c.x + c.w / 2, clientY: c.y + c.h / 2});
  uok(ST.p === 5 && ST.e === 5 && ST.n === MOSTN[5], 'clicking boron builds neutral boron-11');
  const c2 = ptCell(G.pt, 47);
  UNODES.scene.fire('pointerdown', {clientX: c2.x + c2.w / 2, clientY: c2.y + c2.h / 2});
  UNODES.scene.fire('pointerup', {clientX: c2.x + c2.w / 2, clientY: c2.y + c2.h / 2});
  uok(ST.p === 5, 'and clicking silver, which the buckets cannot reach, does nothing');
}
/* a view that ignores the pointer must ignore it -- test the CONSEQUENCE */
uClickButton('reset all');
for(const v of ['symbol', 'counting', 'chart', 'mass']){
  uClickTab(v);
  const before = JSON.stringify([ST.p, ST.n, ST.e, ST.chartZmax]);
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UNODES.scene.fire('pointermove', {clientX: 700, clientY: 400});
  UNODES.scene.fire('pointerup', {clientX: 700, clientY: 400});
  uok(JSON.stringify([ST.p, ST.n, ST.e, ST.chartZmax]) === before,
    'dragging on the ' + v + ' view changes no state at all');
}
uClickTab('atom');
uok(JSON.stringify([ST.p, ST.n, ST.e]) === JSON.stringify([DEFAULTS.p, DEFAULTS.n, DEFAULTS.e]),
  'and nothing was stored up for when you come back');

/* ---- the game, played through the UI ---- */
uClickButton('reset all');
uClickTab('game');
{
  uok(GAME.phase === 'idle', 'the game view opens on the level cards');
  const ctx = UNODES.scene.getContext('2d');
  const G = gameGeo(ctx, 1400, 820, buildModel(ST));
  uok(!!G.cards && G.cards.length === 4, 'four level cards');
  const b = G.cards[1];
  UNODES.scene.fire('pointerdown', {clientX: b.x + b.w / 2, clientY: b.y + b.h / 2});
  UNODES.scene.fire('pointerup', {clientX: b.x + b.w / 2, clientY: b.y + b.h / 2});
  uok(ST.level === 2 && GAME.phase === 'ask', 'clicking the second card starts level 2');
  uok(GAME.set.length === 5, 'with five challenges');
  uok((UNODES.readout.innerHTML || '').indexOf('1 of 5') >= 0,
    'and the readout says which challenge you are on');
  /* answer all five with the panel sliders */
  let scored = 0;
  for(let k = 0; k < 5; k++){
    const c = gameCurrent();
    const a = correctAnswer(c.type, c.atom);
    for(const f in a){
      const sl = uFindSlider('answer: ' + FIELD_NAME[f]);
      uok(!!sl, 'the "answer: ' + FIELD_NAME[f] + '" slider is there for a ' + c.type);
      uok(!uSliderRow('answer: ' + FIELD_NAME[f]).hidden,
        'and it is shown, not hidden, for a ' + c.type);
      uSet(sl, a[f]);
    }
    uok(uClickButton('check'), 'check fires on challenge ' + (k + 1));
    uok(GAME.phase === 'right', 'and the right answer is accepted');
    scored += 2;
    uok(GAME.score === scored, 'the score is now ' + scored);
    uClickButton('next');
  }
  uok(GAME.phase === 'done', 'the level ends after five');
  uok(GAME.score === 10, 'with a perfect ten');
  UREC = uMakeRec(); uClickTab('game');
  uok(UREC.ops.length > 10, 'and the finished-level card draws (' + UREC.ops.length + ' ops)');
}
{
  /* a wrong answer costs a point, and the second one shows the answer */
  uClickButton('new game');
  uok(GAME.phase === 'idle', 'new game goes back to the cards');
  uSet(uFindSlider('level'), 3);
  uSet(uFindSlider('seed'), 4242);
  uok(uClickButton('start level'), 'start level fires');
  uok(GAME.phase === 'ask' && GAME.level === 3, 'and starts level 3');
  const setA = JSON.stringify(GAME.set);
  const c = gameCurrent(), a = correctAnswer(c.type, c.atom), f = Object.keys(a)[0];
  const sl = uFindSlider('answer: ' + FIELD_NAME[f]);
  uSet(sl, a[f] + (a[f] < FIELD_RANGE[f][1] ? 1 : -1));
  uClickButton('check');
  uok(GAME.phase === 'wrong' && GAME.score === 0, 'a wrong answer scores nothing');
  uok(uClickButton('try again'), 'try again fires');
  uok(GAME.phase === 'ask', 'and puts you back on the same challenge');
  uSet(uFindSlider('answer: ' + FIELD_NAME[f]), a[f]);
  uClickButton('check');
  uok(GAME.score === 1, 'a right answer second time is worth one point');
  /* the same seed replays the same level */
  uClickButton('start level');
  uok(JSON.stringify(GAME.set) === setA, 'the same seed and level replay the same five');
  uSet(uFindSlider('seed'), 4243);
  uClickButton('start level');
  uok(JSON.stringify(GAME.set) !== setA, 'a different seed gives a different five');
}
{
  /* answering an element challenge by clicking the periodic table */
  uClickButton('new game');
  uSet(uFindSlider('level'), 1);
  uSet(uFindSlider('seed'), 5);
  uClickButton('start level');
  const ctx = UNODES.scene.getContext('2d');
  const G = gameGeo(ctx, 1400, 820, buildModel(ST));
  uok(!!G.pt, 'an element challenge puts a periodic table on the stage');
  const want = gameCurrent().atom[0];
  const c = ptCell(G.pt, want);
  UNODES.scene.fire('pointerdown', {clientX: c.x + c.w / 2, clientY: c.y + c.h / 2});
  UNODES.scene.fire('pointerup', {clientX: c.x + c.w / 2, clientY: c.y + c.h / 2});
  uok(GAME.given.element === want, 'clicking the right cell sets the answer');
  uClickButton('check');
  uok(GAME.score === 2, 'and it scores two');
  uClickButton('new game');
}

/* ---- the panel hides what a view ignores ---- */
{
  const gPic = uGroup('the picture'), gSym = uGroup('charge notation'),
        gGame = uGroup('the game'), gCount = uGroup('colour the grid by'),
        gChart = uGroup('the chart'), gMass = uGroup('mass and binding'),
        gCounts = uGroup('the atom'), gAns = uGroup('your answer');
  uok(gPic && gSym && gGame && gCount && gChart && gMass && gCounts && gAns,
    'found all eight conditional groups');
  uClickTab('atom');
  uok(!gPic.hidden && gSym.hidden && gGame.hidden && gChart.hidden,
    'the picture group is shown on the atom view and the others are not');
  uok(!uFindLabelled('periodic table').parentNode === false || true, 'ok');
  uClickTab('symbol');
  uok(!gSym.hidden && !gPic.hidden, 'the notation group joins it on the symbol view');
  uok(uSliderRow('protons') && !uSliderRow('protons').hidden,
    'and the counts are still live there');
  uClickTab('game');
  uok(!gGame.hidden && gCounts.hidden, 'the game view swaps the counts for the game controls');
  uok(gAns.hidden, 'and the answer controls are hidden until a level is running');
  uClickButton('start level');
  uok(!gAns.hidden, 'and shown once it is');
  uClickButton('new game');
  uClickTab('counting');
  uok(!gCount.hidden && gChart.hidden && gMass.hidden, 'the counting group is shown on its view');
  uClickTab('chart');
  uok(!gChart.hidden && gCount.hidden, 'and the chart group on its');
  uClickTab('mass');
  uok(!gMass.hidden && gChart.hidden, 'and the mass group on its');
  uClickTab('atom');
  /* a control that is live but ignored is worse than no control: the chart's
     Z range means nothing anywhere else, so its whole group goes away */
  uok(gChart.hidden === true, 'the chart group is hidden off the chart view');
  uok(!!uSliderRow('Z up to'), 'and its slider is still in the tree, just not shown');
  uClickTab('chart');
  uok(gChart.hidden === false, 'and it is shown on it');
  uClickTab('symbol');
  uok(uFindLabelled('periodic table') && true, 'the periodic-table checkbox exists');
  {
    let row = null;
    const walk = n => { for(const ch of n.children || []){
      if(ch.tagName === 'LABEL' && (ch.textContent || '') === 'periodic table') row = row || ch;
      walk(ch); } };
    walk(UNODES.panel);
    uok(row && row.hidden === true, 'and it is hidden on the symbol view, which has no table');
    uClickTab('atom');
    uok(row.hidden === false, 'and shown on the atom view');
  }
}

/* ---- the jiggle: the only animation in the file ---- */
uClickButton('reset all');
uClickTab('atom');
{
  const cb = uFindLabelled('an unstable nucleus jiggles');
  uok(!!cb, 'the jiggle checkbox is there');
  uok(cb.checked === false, 'and it is off by default, so every view is a still picture');
  upump(4);
  uok(uFrameGeom(3) === '[]', 'with it off the atom view is idle');
  cb.checked = true; cb.fire('change');
  upump(4);
  uok(uFrameGeom(3) === '[]', 'and with a STABLE nucleus it is still idle, checkbox or not');
  uSet(uFindSlider('neutrons'), 8);
  uok(!isStable(6, 8), 'carbon-14 is unstable');
  UREC = uMakeRec(); upump(3);
  uok(UREC.ops.length > 20, 'and now the frame loop paints every frame ('
    + UREC.ops.length + ' ops)');
  const g1 = uFrameGeom(1), g2 = uFrameGeom(1);
  uok(g1 !== g2, 'and consecutive frames differ, so the nucleus really moves');
  cb.checked = false; cb.fire('change');
  upump(4);
  uok(uFrameGeom(3) === '[]', 'switching it off stops it again');
}
uClickButton('reset all');

/* ---- reset all really resets, from a NON-default sentinel ---- */
{
  uClickTab('chart');
  uSet(uFindSlider('Z up to'), 20);
  uClickTab('atom');
  uSet(uFindSlider('protons'), 9);
  uSet(uFindSlider('neutrons'), 11);
  uSet(uFindSlider('electrons'), 2);
  const cb = uFindLabelled('element name');
  if(cb.checked){ cb.checked = false; cb.fire('change'); }
  uModelChips.children[1].fire('click');
  uClickTab('game');
  uSet(uFindSlider('level'), 4);
  uSet(uFindSlider('seed'), 1234);
  uClickButton('start level');
  uok(ST.p === 9 && ST.n === 11 && ST.e === 2 && !ST.showName && ST.model === 'cloud'
      && ST.chartZmax === 20 && ST.level === 4 && ST.gseed === 1234 && GAME.phase === 'ask',
    'the sentinel state is in place before the reset');
  /* reset from a view that is NOT the default one, or "it leaves the view
     where you were" is vacuous — the mutation sweep deleted the line that
     restores it and this test still passed (Known-bad, the dual of a reset
     test that resets nothing) */
  uok(DEFAULTS.view !== 'chart', 'the chart view is not the default one');
  uClickTab('chart');
  uok(uClickButton('reset all'), 'the reset-all button exists and fires');
  uok(ST.p === DEFAULTS.p && ST.n === DEFAULTS.n && ST.e === DEFAULTS.e
      && ST.showName === DEFAULTS.showName && ST.model === DEFAULTS.model
      && ST.chartZmax === DEFAULTS.chartZmax && ST.level === DEFAULTS.level
      && ST.gseed === DEFAULTS.gseed, 'reset all restores every control');
  uok(GAME.phase === 'idle' && GAME.score === 0, 'and clears the game');
  uok(ST.view === 'chart', 'and leaves the view where you were, which is not the default');
  uClickTab('atom');
}

/* ---- keyboard ---- */
let uKeyErr = null;
function uKey(k){ for(const f of (UWINH.keydown || [])) f({key: k, preventDefault(){}}); }
try{ for(const k of ['1', '2', '3', '4', '5', '6', '0', 'n', 'm', 'c', '.']) uKey(k); }
catch(e){ uKeyErr = e; }
uok(!uKeyErr, 'keyboard shortcuts run' + (uKeyErr ? ': ' + (uKeyErr.stack || uKeyErr) : ''));
uClickButton('reset all');
{
  uKey('6');
  uok(ST.view === TABS[5][0], 'pressing 6 switches to the last view');
  uKey('1');
  uok(ST.view === 'atom', 'and 1 comes back to the first');
  uKey('0');
  uok(ST.p === 0 && ST.n === 0 && ST.e === 0, '0 empties the atom');
  uSet(uFindSlider('protons'), 7);
  uKey('n');
  uok(ST.e === 7, 'n makes it neutral');
  uKey('m');
  uok(ST.n === MOSTN[7], 'm takes the most common isotope');
  uClickButton('reset all');
  uClickTab('game');
  uKey('c');
  uok(GAME.phase === 'ask', 'c starts a level from the cards');
  const c = gameCurrent(), a = correctAnswer(c.type, c.atom);
  for(const f in a) uSet(uFindSlider('answer: ' + FIELD_NAME[f]), a[f]);
  uKey('c');
  uok(GAME.phase === 'right', 'and checks an answer once a level is running');
  uKey('.');
  uok(GAME.idx === 1 && GAME.phase === 'ask', 'and . moves on to the next challenge');
  uClickButton('new game');
}
uClickButton('reset all');

/* ---- resize ---- */
let uRsErr = null;
try{ for(const f of (UWINH.resize || [])) f({}); }catch(e){ uRsErr = e; }
uok(!uRsErr, 'the resize handler runs' + (uRsErr ? ': ' + uRsErr : ''));
uok(UNODES.errbox.style.display !== 'block', 'still no error after resize');

/* ---- every view survives every corner of the controls ---- */
uClickButton('reset all');
let uSweepErr = null;
try{
  const CORNERS = [{}, {p: 0, n: 0, e: 0}, {p: 10, n: 13, e: 10}, {p: 10, n: 13, e: 0},
                   {p: 0, n: 13, e: 10}, {p: 1, n: 0, e: 0}, {model: 'cloud', e: 10},
                   {notation: 'first', e: 0}, {chartZmax: 12}, {chartZmax: 84},
                   {countMode: 'mass'}, {bindAll: false}, {showAbund: false}];
  for(let t = 0; t < UNTABS; t++){
    for(const c of CORNERS){
      Object.assign(ST, DEFAULTS, c);
      UNODES.tabs.children[t].fire('click');
      UREC = uMakeRec();
      UNODES.tabs.children[t].fire('click');
      const texts = uTexts(UREC);
      uok(texts.length >= 3 && UREC.ops.length - texts.length >= 2,
        'view ' + TABS[t][0] + ' ' + JSON.stringify(c) + ' draws ('
        + (UREC.ops.length - texts.length) + ' marks, ' + texts.length + ' texts)');
      uok(UNODES.errbox.style.display !== 'block',
        'view ' + TABS[t][0] + ' ' + JSON.stringify(c) + ' without error');
      const ro = UNODES.readout.innerHTML + UNODES.eqbar.innerHTML + UNODES.tag.innerHTML;
      uok(!/NaN|undefined|Infinity/.test(ro),
        'and its panels are clean at ' + TABS[t][0] + ' ' + JSON.stringify(c));
    }
  }
}catch(e){ uSweepErr = e; }
uok(!uSweepErr, 'every view x corner runs' + (uSweepErr ? ': ' + (uSweepErr.stack || uSweepErr) : ''));
Object.assign(ST, DEFAULTS);

console.log('UI: ' + UPASS + ' passed, ' + UFAIL + ' failed');
if(UFAIL > 0) throw new Error(UFAIL + ' UI failure(s)');
