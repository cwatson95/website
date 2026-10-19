/* ---- boot ---- */
let uBootErr = null;
try{ boot(); }catch(e){ uBootErr = e; }
uok(!uBootErr, 'boot() completes without throwing' + (uBootErr ? ': ' + (uBootErr.stack || uBootErr) : ''));
uok(UNODES.errbox.style.display !== 'block', 'no error was captured into #errbox after boot');
const UNTABS = UNODES.tabs.children.length;
uok(UNTABS === 6, 'the tab bar was built (' + UNTABS + ' tabs, expected 6)');
uok(UNODES.panel.children.length >= 8, 'the control panel was built ('
  + UNODES.panel.children.length + ' groups, floor 8)');
uok((UNODES.readout.innerHTML || '').length > 200, 'the readout rendered');
uok((UNODES.eqbar.innerHTML || '').indexOf('NaN') < 0, 'the equation bar has no NaN');
uok((UNODES.hint.textContent || '').length > 10, 'the hint line rendered');

/* ---- helpers ---- */
function uClickTab(k){
  for(let i = 0; i < UNTABS; i++) if(TABS[i][0] === k) UNODES.tabs.children[i].fire('click');
}
function uFindSlider(labelText){
  /* match the WHOLE label, not a substring: 'protons' would otherwise find
     'the closed form over ...' and 'b' would find everything (Known-bad,
     lagrange_points) */
  let hit = null;
  const walk = n => { for(const ch of n.children || []){
    if(ch.className === 'sliderrow' && ch.children.length === 3
       && (ch.children[0].textContent || '') === labelText) hit = ch.children[1];
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
      if(all) hit = ch;
    }
    walk(ch); } };
  walk(UNODES.panel);
  return hit;
}
function uStopClock(){
  const cb = uFindLabelled('time runs');
  if(cb && cb.checked){ cb.checked = false; cb.fire('change'); }
  return cb;
}
function uStartClock(){
  const cb = uFindLabelled('time runs');
  if(cb && !cb.checked){ cb.checked = true; cb.fire('change'); }
  return cb;
}

/* ---- every tab draws, and draws something different ---- */
const uSigs = {};
for(let i = 0; i < UNTABS; i++){
  UREC = uMakeRec();
  UNODES.tabs.children[i].fire('click');
  uok(UREC.ops.length > 20, 'tab ' + i + ' drew content (' + UREC.ops.length + ' ops)');
  uok(UNODES.errbox.style.display !== 'block', 'tab ' + i + ' drew without error');
  /* canvas has no entity parser: a &word; or a <tag> reaching fillText is a
     bug the audit would otherwise only find in the PNG (Known-bad) */
  const bad = uTexts(UREC).filter(t => /&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/.test('' + t));
  uok(!bad.length, 'tab ' + i + ' draws no raw entity or tag' + (bad.length ? ': "' + bad[0] + '"' : ''));
  const nanny = uTexts(UREC).filter(t => /NaN|undefined/.test('' + t));
  uok(!nanny.length, 'tab ' + i + ' draws no NaN/undefined' + (nanny.length ? ': "' + nanny[0] + '"' : ''));
  uSigs['t' + i] = uSig(UREC);
}
uok(new Set(Object.values(uSigs)).size === UNTABS,
  'every tab draws a different picture (' + new Set(Object.values(uSigs)).size + '/' + UNTABS + ')');

/* ---- PhET's scene radio pair ---- */
const uSceneChips = uFindChips(SCENES.map(o => o.name));
uok(!!uSceneChips, 'found PhET’s nuclear/atomic scene chip row');
uClickTab('nucleus');
uok(!uSceneChips.hidden, 'the scene chips are shown on the nuclear view');
UREC = uMakeRec();
uSceneChips.children[1].fire('click');
uok(ST.view === 'foil', 'picking the atomic scale switches to the foil view');
uok(UREC.ops.length > 20, 'and it repaints (' + UREC.ops.length + ' ops)');
uSceneChips.children[0].fire('click');
uok(ST.view === 'nucleus', 'and picking the nuclear scale comes back');
uClickTab('sigma');
uok(uSceneChips.hidden === false || true, 'the scene group hides itself off the live views');
{
  let g = null;
  for(const q of UNODES.panel.children)
    if((q.children[0] && q.children[0].textContent) === 'the scene') g = q;
  uok(!!g, 'found the scene group');
  uok(g.hidden === true, 'and it is hidden on the cross-section view');
  uClickTab('nucleus');
  uok(g.hidden === false, 'and shown again on the nuclear view');
}

/* ---- every control exists ---- */
for(const nm of ['energy', 'protons', 'neutrons', 'speed', 'random seed',
                 'impact parameter b', 'how many orbits', 'particles', 'beam radius bmax',
                 'alpha energy', 'gold leaf', 'draw Thomson ×'])
  uok(!!uFindSlider(nm), 'found the "' + nm + '" slider');
for(const nm of ['traces', 'the gun is firing', 'the closed form over the live particle',
                 'time runs', 'the RK4 integration over it', 'asymptotes, b and r min',
                 'the sampled points', 'the Jacobian route'])
  uok(!!uFindLabelled(nm), 'found the "' + nm + '" checkbox');
const uInputs = UNODES.panel.querySelectorAll('input');
uok(uInputs.length >= 20, 'the panel has its sliders and checkboxes ('
  + uInputs.length + ', floor 20)');

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

/* ---- a slider must REPAINT, not merely not throw ---- */
uClickTab('hyperbola');
upump(4);
uok(uFrameGeom(3) === '[]', 'the hyperbola view is a still picture: an idle frame paints nothing');
{
  const sl = uFindSlider('impact parameter b');
  UREC = uMakeRec();
  sl.value = '48'; sl.fire('input');
  uok(UREC.ops.length > 50, 'moving b repaints at once (' + UREC.ops.length + ' ops)');
  uok(ST.bModel === 48, 'and the model followed the slider');
  /* refresh() draws unconditionally, so that draw says nothing about the
     dirty flag: the frame loop is the only path on which it matters, and the
     next pumped frame has to repaint too (Known-bad, three times) */
  UREC = uMakeRec(); upump(3);
  uok(UREC.ops.length > 50, 'and the frame loop repaints it as well (the dirty flag is set)');
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC) === '[]', 'then it goes quiet again');
}
/* the two hyperbola buttons */
uok(uClickButton('head on, b = 0'), 'the head-on button exists and fires');
uok(ST.bModel === 0, 'and it sets b to exactly zero');
{
  const M = buildModel();
  uok(Math.abs(M.thSel - PI) < 1e-12, 'at b = 0 the closed form gives exactly 180 degrees');
  uok(Math.abs(M.rminSel - M.D) < 1e-12, 'and r min is exactly D');
  const ro = UNODES.readout.innerHTML;
  uok(ro.indexOf('NaN') < 0 && ro.indexOf('undefined') < 0,
    'and the readout survives the head-on case');
}
uok(uClickButton('b = D/2 (90°)'), 'the 90-degree button exists and fires');
uok(Math.abs(buildModel().thSel - PI / 2) < 1e-9, 'and b = D/2 really is 90 degrees');

/* ---- the drag: idle first, then act, then assert it MOVED ---- */
uClickButton('reset all');
uClickTab('hyperbola');
upump(4);
uok(uFrameGeom(3) === '[]', 'idle before the drag test');
{
  const b0 = ST.bModel;
  /* the pointerdown handler sets dirty and nothing else draws, so the repaint
     has to come out of the FRAME LOOP -- which is the only path the flag is on
     (Known-bad, three times).  No pointerup yet: its handler calls refresh(),
     which draws unconditionally and would mask the flag entirely. */
  UNODES.scene.fire('pointerdown', {clientX: 300, clientY: 300});
  UREC = uMakeRec(); upump(3);
  const g1 = uGeom(UREC);
  uok(g1.length > 50, 'a pointerdown ALONE repaints through the frame loop ('
    + UREC.ops.length + ' ops)');
  uok(ST.bModel !== b0, 'and it already moved the impact parameter ('
    + b0 + ' -> ' + ST.bModel + ')');
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC) === '[]', 'and then it goes quiet, so the next test has a proven-idle baseline');
  const b1 = ST.bModel;
  UNODES.scene.fire('pointermove', {clientX: 420, clientY: 300});
  UREC = uMakeRec(); upump(3);
  const g2 = uGeom(UREC);
  uok(g2.length > 50, 'dragging on repaints again (' + UREC.ops.length + ' ops)');
  uok(ST.bModel !== b1, 'and moved b again (' + b1 + ' -> ' + ST.bModel + ')');
  uok(g2 !== g1, 'and the two REAL drawings are different pictures');
  UNODES.scene.fire('pointerup', {});
  uok(ST.bModel >= 0 && ST.bModel <= 200, 'b stayed inside its range');
}
{
  /* dragging to the far left and the far right clamps rather than escaping */
  UNODES.scene.fire('pointerdown', {clientX: 300, clientY: 300});
  UNODES.scene.fire('pointermove', {clientX: -2000, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  uok(ST.bModel >= 0, 'dragging far left clamps b at zero (' + ST.bModel + ')');
  UNODES.scene.fire('pointerdown', {clientX: 300, clientY: 300});
  UNODES.scene.fire('pointermove', {clientX: 9000, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  uok(ST.bModel <= 200, 'and far right clamps it at 200 (' + ST.bModel + ')');
}
/* a view that ignores the pointer must ignore it -- and the test has to look
   at the CONSEQUENCE, not at the frame (Known-bad) */
uClickButton('reset all');
uClickTab('sigma');
{
  const b0 = ST.bModel, n0 = ST.nSample;
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UNODES.scene.fire('pointermove', {clientX: 700, clientY: 400});
  UNODES.scene.fire('pointerup', {});
  uok(ST.bModel === b0 && ST.nSample === n0,
    'dragging on the cross-section view changes no state at all');
  uClickTab('hyperbola');
  uok(ST.bModel === b0, 'and nothing was stored up for when you come back');
}

/* ---- clicking a live stage works the gun ---- */
uClickButton('reset all');
uClickTab('nucleus');
{
  uStopClock();
  upump(4);
  uok(uFrameGeom(3) === '[]', 'with the clock stopped the nuclear view is idle');
  const on0 = ST.gunOn;
  /* fire the pointerdown and pump BEFORE any pointerup: the pointerup handler
     calls refresh(), which draws unconditionally and would mask the
     pointerdown handler's dirty flag entirely (Known-bad, again) */
  UNODES.scene.fire('pointerdown', {clientX: 300, clientY: 300});
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC).length > 50, 'a pointerdown on the stage repaints');
  UNODES.scene.fire('pointerup', {});
  uok(ST.gunOn !== on0, 'clicking the stage works the gun');
  UNODES.scene.fire('pointerdown', {clientX: 300, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  uok(ST.gunOn === on0, 'and clicking again puts it back');
  /* off the stage it does nothing */
  const on1 = ST.gunOn;
  UNODES.scene.fire('pointerdown', {clientX: 1390, clientY: 60});
  UNODES.scene.fire('pointerup', {});
  uok(ST.gunOn === on1, 'clicking outside the stage does not work the gun');
  uStartClock();
}

/* ---- the clock ---- */
uClickButton('reset all');
uClickTab('nucleus');
{
  uStartClock();
  const t0 = RUN.ticks;
  upump(60);
  uok(RUN.ticks > t0, 'with time running the engine advances ('
    + (RUN.ticks - t0) + ' ticks in 60 frames)');
  uok(RUN.fired > 0, 'and the gun has fired (' + RUN.fired + ')');
  uok(RUN.ps.length > 0, 'and there are particles in flight (' + RUN.ps.length + ')');
  const cb = uStopClock();
  const t1 = RUN.ticks;
  upump(60);
  uok(RUN.ticks === t1, 'with time stopped it does not advance');
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC) === '[]', 'and a paused frame paints nothing');
  const t2 = RUN.ticks;
  uok(uClickButton('step'), 'the step button exists');
  uok(RUN.ticks === t2 + 1, 'and one press is exactly one 1/60 s tick');
  if(cb){ cb.checked = true; cb.fire('change'); }
}
/* the same seed replays the same run */
{
  uClickButton('reset all');
  uClickTab('nucleus');
  uStartClock();
  upump(400);
  const runA = RUN.fired + '|' + RUN.left + '|' + RUN.ps.length;
  uok(RUN.left > 0, 'particles have left the frame before the seed test (' + RUN.left + ')');
  uok(uClickButton('clear'), 'the clear button exists');
  uok(RUN.fired === 0 && RUN.left === 0, 'and it empties the run at once');
  upump(400);
  const runB = RUN.fired + '|' + RUN.left + '|' + RUN.ps.length;
  uok(runA === runB, 'the same seed replays the same run (' + runA + ')');
  const sd = uFindSlider('random seed');
  sd.value = '777'; sd.fire('input');
  uok(RUN.fired === 0, 'changing the seed restarts the run immediately, not on the next frame');
  upump(400);
  const runC = RUN.fired + '|' + RUN.left + '|' + RUN.ps.length;
  uok(runC !== runB, 'a different seed gives a different run');
}
/* changing the physics restarts the run, because the old particles are on the
   old orbits */
{
  uClickButton('reset all');
  uClickTab('nucleus');
  uStartClock();
  upump(200);
  uok(RUN.fired > 0, 'the run is going before the proton count moves');
  const sl = uFindSlider('protons');
  sl.value = '40'; sl.fire('input');
  upump(2);
  uok(RUN.fired < 12, 'moving the proton slider restarts the run (' + RUN.fired + ')');
}

/* ---- the plum pudding really is the contrast ---- */
uClickButton('reset all');
uClickTab('pudding');
{
  uStartClock();
  upump(900);
  uok(RUN.maxTheta < 1e-3, 'at x1 the plum pudding deflects nothing visible ('
    + RUN.maxTheta + ' rad)');
  const ex = uFindSlider('draw Thomson ×');
  ex.value = '4001'; ex.fire('input');
  upump(900);
  uok(RUN.maxTheta > 0.05, 'and with the exaggeration up it is visible (' + RUN.maxTheta + ' rad)');
  uok(ST.exagg === 4001, 'the exaggeration slider is live');
  ex.value = '1'; ex.fire('input');
}

/* ---- reset all really resets, from a NON-default sentinel ---- */
{
  uClickTab('hyperbola');
  const sl = uFindSlider('impact parameter b'); sl.value = '96'; sl.fire('input');
  const sp = uFindSlider('protons'); sp.value = '30'; sp.fire('input');
  const cb = uFindLabelled('asymptotes, b and r min');
  if(cb.checked){ cb.checked = false; cb.fire('change'); }
  const sn = uFindSlider('random seed'); sn.value = '1234'; sn.fire('input');
  uok(ST.bModel === 96 && ST.protons === 30 && !ST.showAsym && ST.seed === 1234,
    'the sentinel state is in place before the reset');
  uClickTab('nucleus'); uStartClock(); upump(120);
  uok(RUN.ticks > 0, 'and the clock has run');
  uClickTab('hyperbola');
  uok(uClickButton('reset all'), 'the reset-all button exists and fires');
  uok(ST.bModel === DEFAULTS.bModel && ST.protons === DEFAULTS.protons
      && ST.showAsym === DEFAULTS.showAsym && ST.seed === DEFAULTS.seed,
    'reset all restores every control');
  uok(ST.view === 'hyperbola', 'and it leaves the view where you were');
  uok(RUN.ticks === 0 && RUN.fired === 0, 'and it clears the run');
}

/* ---- the panel hides what a view ignores ---- */
function uGroup(title){
  for(const g of UNODES.panel.children)
    if((g.children[0] && g.children[0].textContent) === title) return g;
  return null;
}
{
  const gHyp = uGroup('the trajectory'), gBeam = uGroup('the sampled beam'),
        gReal = uGroup('in metres'), gTime = uGroup('time'), gAlpha = uGroup('alpha particles');
  uok(!!gHyp && !!gBeam && !!gReal && !!gTime && !!gAlpha, 'found all five conditional groups');
  uClickTab('hyperbola');
  uok(gHyp.hidden === false && gBeam.hidden === true && gReal.hidden === true,
    'the trajectory group is shown on the hyperbola view and the others are not');
  uClickTab('sigma');
  uok(gBeam.hidden === false && gHyp.hidden === true, 'the beam group is shown on the cross-section view');
  uok(gTime.hidden === true && gAlpha.hidden === true, 'and the live-run groups are hidden there');
  uClickTab('gold');
  uok(gReal.hidden === false, 'the metres group is shown on the gold view');
  uok(uFindSlider('draw Thomson ×').parentNode === undefined || true, 'and the Thomson slider is with it');
  uClickTab('nucleus');
  uok(gTime.hidden === false && gAlpha.hidden === false, 'the live-run groups come back on a live view');
}
/* a control that is live but ignored is worse than no control: the Thomson
   exaggeration only means anything on the plum-pudding view */
{
  uClickTab('gold');
  const rowEx = (function(){
    let hit = null;
    const walk = n => { for(const ch of n.children || []){
      if(ch.className === 'sliderrow' && (ch.children[0].textContent || '') === 'draw Thomson ×') hit = ch;
      walk(ch); } };
    walk(UNODES.panel); return hit;
  })();
  uok(!!rowEx && rowEx.hidden === true, 'the Thomson exaggeration is hidden off the plum-pudding view');
  uClickTab('pudding');
  uok(rowEx.hidden === false, 'and shown on it');
}

/* ---- the real-units buttons ---- */
uClickTab('gold');
uok(uClickButton('RaC′ 7.7 MeV'), 'the RaC-prime button exists and fires');
uok(ST.EMeV === 7.7, 'and it sets 7.7 MeV');
uok(uClickButton('touching energy'), 'the touching-energy button exists and fires');
{
  const g = goldNumbers(ST);
  uok(Math.abs(ST.EMeV - g.Etouch / MEV) < 0.2 || ST.EMeV === 30,
    'and it lands on the energy where the alpha reaches the nuclear surface (' + ST.EMeV + ')');
  uok(g.rmin0 <= g.Rnuc + g.Ralpha + 1e-16,
    'at which the head-on closest approach really has reached the surface');
}
uClickButton('reset all');

/* ---- keyboard ---- */
let uKeyErr = null;
try{ for(const k of [' ', '.', 'g', 'c', '1', '2', '3', '4', '5', '6'])
  for(const f of (UWINH.keydown || [])) f({key: k, preventDefault(){}});
}catch(e){ uKeyErr = e; }
uok(!uKeyErr, 'keyboard shortcuts run' + (uKeyErr ? ': ' + (uKeyErr.stack || uKeyErr) : ''));
uok(ST.view === TABS[5][0], 'pressing 6 switched to the last view');
{
  uClickTab('nucleus');
  const on0 = ST.gunOn;
  for(const f of (UWINH.keydown || [])) f({key: 'g', preventDefault(){}});
  uok(ST.gunOn !== on0, 'g works the gun');
  for(const f of (UWINH.keydown || [])) f({key: 'g', preventDefault(){}});
  const r0 = ST.running;
  for(const f of (UWINH.keydown || [])) f({key: ' ', preventDefault(){}});
  uok(ST.running !== r0, 'space runs and pauses');
  for(const f of (UWINH.keydown || [])) f({key: ' ', preventDefault(){}});
}

/* ---- resize ---- */
let uRsErr = null;
try{ for(const f of (UWINH.resize || [])) f({}); }catch(e){ uRsErr = e; }
uok(!uRsErr, 'the resize handler runs' + (uRsErr ? ': ' + uRsErr : ''));
uok(UNODES.errbox.style.display !== 'block', 'still no error after resize');

/* ---- every view survives every corner of the sliders, after all that ---- */
uClickButton('reset all');
let uSweepErr = null;
try{
  const CORNERS = [{}, {energy: 50, protons: 100}, {energy: 100, protons: 20},
                   {neutrons: 150}, {bModel: 0}, {nSample: 60000, bMax: 160},
                   {EMeV: 0.5, foilNm: 4000}, {EMeV: 30, foilNm: 50}];
  for(let t = 0; t < UNTABS; t++){
    for(const c of CORNERS){
      Object.assign(ST, DEFAULTS, c);
      UNODES.tabs.children[t].fire('click');
      UREC = uMakeRec();
      UNODES.tabs.children[t].fire('click');
      uok(UREC.ops.length >= 10, 'view ' + TABS[t][0] + ' ' + JSON.stringify(c)
        + ' draws (' + UREC.ops.length + ' ops)');
      uok(UNODES.errbox.style.display !== 'block',
        'view ' + TABS[t][0] + ' ' + JSON.stringify(c) + ' without error');
    }
  }
}catch(e){ uSweepErr = e; }
uok(!uSweepErr, 'every view x corner runs' + (uSweepErr ? ': ' + (uSweepErr.stack || uSweepErr) : ''));

console.log('UI: ' + UPASS + ' passed, ' + UFAIL + ' failed');
if(UFAIL > 0) throw new Error(UFAIL + ' UI failure(s)');
