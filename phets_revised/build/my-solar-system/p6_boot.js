
/* ================================================================== *
 *  boot — panel, tabs, handlers, frame loop                           *
 * ================================================================== */
function boot(){
  const canvas = document.getElementById('scene');
  const panel = document.getElementById('panel');
  const tabsEl = document.getElementById('tabs');
  const roEl = document.getElementById('readout');
  const eqEl = document.getElementById('eqbar');
  const tagEl = document.getElementById('tag');
  const hintEl = document.getElementById('hint');
  const errEl = document.getElementById('errbox');
  const S = makeScene(canvas), st = S.st;
  let dirty = false;

  function fail(e){ errEl.style.display = 'block'; errEl.textContent = String(e && e.stack || e); }
  window.addEventListener('error', ev => fail(ev.error || ev.message));

  function setView(k){
    if(st.view !== k){ st.view = k; syncMasses(); }
    [].forEach.call(tabsEl.children, (b, i) => b.className = TABS[i][0] === st.view ? 'active' : '');
    syncChips(); syncPanel(); dirty = true; refresh();
  }
  TABS.forEach(([k, lab2]) => {
    tabsEl.appendChild(h('button', {class: st.view === k ? 'active' : '', onclick: () => setView(k), html: lab2}));
  });

  const rows = {};
  function slider(key, lab2, lo, hi, step2, fmtf, onchg){
    const inp = h('input', {type: 'range', min: lo, max: hi, step: step2, value: st[key]});
    const val = h('span', {class: 'val'});
    const rowEl = h('div', {class: 'sliderrow'}, h('label', null, lab2), inp, val);
    const sync = () => { inp.value = st[key]; val.textContent = fmtf(st[key]); };
    inp.addEventListener('input', () => {
      st[key] = parseFloat(inp.value);
      if(onchg) onchg();
      val.textContent = fmtf(st[key]); syncPanel(); dirty = true; refresh();
    });
    rows[key] = {row: rowEl, sync, inp}; sync(); return rowEl;
  }
  function checkbox(key, lab2, onchg){
    const inp = h('input', {type: 'checkbox'}); inp.checked = st[key];
    const el = h('label', null, inp, lab2);
    inp.addEventListener('change', () => {
      st[key] = inp.checked; if(onchg) onchg(); syncPanel(); dirty = true; refresh();
    });
    rows['cb_' + key] = {row: el, inp, sync: () => { inp.checked = st[key]; }};
    return el;
  }
  function chipRow(list, key, onPick){
    const wrapEl = h('div', {class: 'chips'});
    list.forEach(o => {
      const c = h('button', {class: 'chip' + (st[key] === o.id ? ' on' : ''), html: o.name, onclick: () => {
        st[key] = o.id; if(onPick) onPick(o);
        [].forEach.call(wrapEl.children, (b, i) => b.className = 'chip' + (list[i].id === st[key] ? ' on' : ''));
        syncChips(); syncPanel(); dirty = true; refresh(); }});
      wrapEl.appendChild(c);
    });
    return wrapEl;
  }
  const CHIPROWS = [];
  function trackChips(g, list, key){ CHIPROWS.push([g, list, key]); }
  function enable(key, on){
    const r = rows[key]; if(!r) return;
    if(r.inp) r.inp.disabled = !on;
    r.row.style.opacity = on ? '1' : '0.42';
  }

  const gSys = h('div', {class: 'grp'}, h('h3', null, 'the orbital system'));
  const presetChips = chipRow(PRESETS, 'preset', o => {
    if(o.id === 'custom') return;                    /* "custom" is the label, not a system */
    SIM.lab = sysLoad(o.id);
    st.nb = SIM.lab.S.n; st.running = false;
    histReset(); syncMasses();
  });
  gSys.appendChild(presetChips); trackChips(gSys, PRESETS, 'preset');
  const nbChips = chipRow(NBODIES, 'nb', o => {
    sysSetN(SIM.lab, o.id); st.preset = 'custom'; st.running = false; histReset(); syncMasses();
  });
  gSys.appendChild(nbChips); trackChips(gSys, NBODIES, 'nb');
  gSys.appendChild(h('div', {class: 'btnrow'},
    h('button', {onclick: () => { const sys = curSys(); sysRestart(sys);
      if(sysKey(st.view) === 'lab') histReset(); else ehistReset();
      st.running = false; syncMasses(); dirty = true; refresh(); }}, 'return the bodies'),
    h('button', {onclick: () => { const sys = curSys(); sysComFrame(sys);
      if(sysKey(st.view) === 'lab') histReset(); else ehistReset();
      dirty = true; refresh(); }}, 'centre-of-mass frame')));
  const sysTag = h('div', {class: 'tag'}); gSys.appendChild(sysTag);

  const gBodies = h('div', {class: 'grp'}, h('h3', null, 'the bodies'));
  for(let i = 0; i < 4; i++)
    gBodies.appendChild(slider('mass' + (i + 1), 'body ' + (i + 1) + ' mass', PHET.MASS_MIN, PHET.MASS_MAX, 0.1,
      v => massStr(v) + ' &times;10&sup2;&#8312; kg', () => setMass(i, st['mass' + (i + 1)])));
  const bodyTag = h('div', {class: 'tag'}); gBodies.appendChild(bodyTag);

  const gShow = h('div', {class: 'grp'}, h('h3', null, 'show'));
  gShow.appendChild(h('div', {class: 'checks'},
    checkbox('path', 'paths'), checkbox('com', 'centre of mass'),
    checkbox('velocity', 'velocity arrows (drag the tips)'), checkbox('speedLab', 'speed'),
    checkbox('gravity', 'gravity arrows'), checkbox('grid', 'grid, 1 AU'),
    checkbox('tape', 'measuring tape'), checkbox('values', 'the values table')));
  gShow.appendChild(slider('fpow', 'gravity arrows &times;10^n', PHET.FORCE_POW_MIN, PHET.FORCE_POW_MAX, 1,
    v => '&times;10^' + fmt(v, 0)));
  gShow.appendChild(h('div', {class: 'btnrow'},
    h('button', {onclick: () => { sysClearPaths(curSys()); dirty = true; refresh(); }}, 'clear the paths')));
  const showTag = h('div', {class: 'tag'}); gShow.appendChild(showTag);

  const gCmp = h('div', {class: 'grp'}, h('h3', null, 'the comparison'),
    h('div', {class: 'checks'}, checkbox('shadow', 'run PhET&rsquo;s own step beside ours')));
  const cmpTag = h('div', {class: 'tag'}); gCmp.appendChild(cmpTag);

  const gClock = h('div', {class: 'grp'}, h('h3', null, 'the clock'));
  gClock.appendChild(h('div', {class: 'checks'}, checkbox('running', 'time runs')));
  const speedChips = chipRow(SPEEDS, 'speed'); gClock.appendChild(speedChips); trackChips(gClock, SPEEDS, 'speed');
  gClock.appendChild(slider('zoom', 'zoom', PHET.ZOOM_MIN, PHET.ZOOM_MAX, 1,
    v => fmt(PHET.ZOOM_LO + (PHET.ZOOM_HI - PHET.ZOOM_LO) * (v - 1) / 5, 0) + ' per AU'));
  gClock.appendChild(h('div', {class: 'btnrow'},
    h('button', {onclick: () => { const was = st.running; st.running = true; runStep(); st.running = was;
                                  dirty = true; refresh(); }}, 'step'),
    h('button', {onclick: () => { const sys = curSys(); sysRestart(sys); st.running = false;
                                  if(sysKey(st.view) === 'lab') histReset(); else ehistReset();
                                  syncMasses(); dirty = true; refresh(); }}, 'restart'),
    h('button', {onclick: () => { const v = st.view; Object.assign(st, DEFAULTS); st.view = v; simReset();
                                  syncChips(); syncPanel(); dirty = true; refresh(); }}, 'reset all')));
  const clockTag = h('div', {class: 'tag'}); gClock.appendChild(clockTag);

  const gInfo = h('div', {class: 'grp'}, h('h3', null, 'what you are looking at'), h('div', {id: 'info'}),
    h('div', {class: 'src', html: 'Remake of PhET Interactive Simulations&rsquo; <b>My Solar System</b> '
      + '(University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      + 'PhET&rsquo;s values are read out of its published build and named as PhET&rsquo;s: G = 4.4567 AU(km/s)&sup2; per '
      + '10&sup2;&#8312; kg, the mass slider 0.1&ndash;300, the radius rule max(0.03, 0.023 m<sup>1/3</sup>) AU, the '
      + 'zoom 25&ndash;125 per AU, the 20-AU path cap and the eleven orbital systems. Years and true km/s use '
      + 'AU = 149,597,870.7 km (IAU 2012), the Julian year and G = 6.6743e-11 (CODATA). Everything else is computed '
      + 'here and pinned in selfTest to build/my-solar-system/derive.py (scipy solve_ivp, rtol 1e-12).'}));
  const gPhys = h('div', {class: 'grp'}, h('h3', null, 'the physics'), h('div', {id: 'phys'}));
  [gSys, gBodies, gShow, gCmp, gClock, gInfo, gPhys].forEach(g => panel.appendChild(g));
  const infoEl = gInfo.querySelector('#info'), physEl = gPhys.querySelector('#phys');

  function syncChips(){
    for(const [g, list, key] of CHIPROWS){
      const cws = g.querySelectorAll('.chips');
      for(const cw of cws){
        if(cw.children.length !== list.length) continue;
        let match = 0;
        for(let i = 0; i < list.length; i++) if(cw.children[i].textContent === plain(String(list[i].name))) match++;
        if(match === list.length)
          [].forEach.call(cw.children, (b, i) => b.className = 'chip' + (list[i].id === ST[key] ? ' on' : ''));
      }
    }
  }
  function syncPanel(){
    const v = st.view, sys = curSys(), lab = sysKey(v) === 'lab';
    gSys.hidden = !lab;
    gCmp.hidden = (v !== 'conserve');
    for(const k in rows) rows[k].sync();
    for(let i = 0; i < 4; i++) rows['mass' + (i + 1)].row.hidden = i >= sys.S.n;
    enable('fpow', st.gravity);
    enable('cb_values', v !== 'lab');            /* the lab always lists its bodies */
    sysTag.innerHTML = lab ? 'every system loads with its centre of mass brought to rest, as PhET loads them; touching '
      + 'anything makes it custom.' : '';
    bodyTag.innerHTML = 'a mass below ' + fmt(PHET.MASS_MIN, 1) + ' is a test body (PhET shows &le; 0.1); the radius is '
      + 'PhET&rsquo;s max(0.03, 0.023 m<sup>1/3</sup>) AU, so a body is drawn to scale but never below 0.03 AU.';
    showTag.innerHTML = 'velocity arrows are ' + fmt(VSCALE, 1) + ' px per km/s; gravity arrows are 60 px at a pull of '
      + fmt(F_REF, 0) + ' in these units, times the power.';
    cmpTag.innerHTML = 'PhET takes 4000/N substeps a frame with ONE force evaluation each; ours takes as many as the '
      + 'closest pair needs, with four. Both are drawn from the same start.';
    clockTag.innerHTML = 'space runs and pauses &nbsp; <b>r</b> returns the bodies &nbsp; 1&ndash;4 switch views. One frame '
      + 'is ' + PHET.FRAME.toExponential(3) + ' model units = ' + fmt(yrOf(PHET.FRAME) * 365.25, 3) + ' d at normal speed.';
  }

  function refresh(){
    try{
      const M = S.model();
      roEl.innerHTML = readoutHTML(M);
      eqEl.innerHTML = eqbarHTML(M);
      tagEl.innerHTML = tagHTML(M);
      hintEl.textContent = dragsHere(st.view)
        ? 'drag a body, or the tip of its velocity arrow · space runs · 1–4 switch views'
        : 'space runs · r returns the bodies · 1–4 switch views';
      infoEl.innerHTML = INFO[st.view] || '';
      physEl.innerHTML = DERIV[st.view] || '';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown', e => {
    canvas.setPointerCapture(e.pointerId);
    const r = canvas.getBoundingClientRect();
    if(S.pointer('down', e.clientX - r.left, e.clientY - r.top)){ canvas.classList.add('dragging'); dirty = true; syncPanel(); refresh(); }
  });
  canvas.addEventListener('pointermove', e => {
    if(!canvas.classList.contains('dragging') && e.buttons === 0) return;
    const r = canvas.getBoundingClientRect();
    if(S.pointer('move', e.clientX - r.left, e.clientY - r.top)){ dirty = true; syncPanel(); roEl.innerHTML = readoutHTML(S.model()); }
  });
  const up = () => { canvas.classList.remove('dragging'); if(S.pointer('up', 0, 0)){ dirty = true; syncMasses(); syncPanel(); refresh(); } };
  canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);

  window.addEventListener('keydown', e => {
    if(e.key === ' '){ e.preventDefault(); st.running = !st.running; syncPanel(); dirty = true; refresh(); }
    else if(e.key === 'r'){ const sys = curSys(); sysRestart(sys); st.running = false;
                            if(sysKey(st.view) === 'lab') histReset(); else ehistReset();
                            syncMasses(); syncPanel(); dirty = true; refresh(); }
    else if(e.key >= '1' && e.key <= String(TABS.length)) setView(TABS[+e.key - 1][0]);
  });

  function resize(){
    const r = canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(r.width * dpr); canvas.height = Math.round(r.height * dpr);
    canvas.getContext('2d').setTransform(dpr, 0, 0, dpr, 0, 0);
    S.W = r.width; S.H = r.height;
  }
  window.addEventListener('resize', () => { resize(); dirty = true; refresh(); });

  let frameN = 0;
  function frameLoop(){
    frameN++;
    const advanced = S.step();
    if(advanced || dirty){
      dirty = false;
      try{ S.draw(); if(advanced && frameN % 10 === 0) roEl.innerHTML = readoutHTML(S.model()); }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  simReset(); resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO = {
  intro: 'Two bodies, one law. Newton’s inverse square between them is all there is here, and everything you see — the '
    + 'ellipse, the speeding up near periapsis, the two bodies wheeling about a point that never moves — comes out of '
    + 'it. The centre of mass is the quiet one: with no outside force it either stays put or drifts in a straight line '
    + 'for ever, whatever the two bodies do, because the forces they exert on each other are equal and opposite. Drag a '
    + 'body or the tip of its green velocity arrow (the clock stops while you do, as PhET’s does) and the whole future '
    + 'changes. PhET’s own default is a 250 and a 25, and it is the system the third view solves exactly.',
  lab: 'PhET’s eleven orbital systems, and the room to build your own. Sun and planet is the two-body case; add a moon '
    + 'and you have the oldest unsolved problem in mechanics. The trojan asteroids sit 60° ahead of and behind the '
    + 'planet and stay there (Lagrange, 1772); the slingshot is how Voyager was thrown outward — the comet leaves with '
    + '90 % more energy about the star than it arrived with, taken from the planet’s orbit; the four star ballet is an '
    + 'exact homographic solution, four stars on four similar ellipses keeping a perfect square. "Hyperbolic" is worth '
    + 'a look: its three fly-bys are at 0.878, 0.929 and 0.995 of the escape speed, so all three are bound — the last '
    + 'one comes back after 1,791 years.',
  exact: 'Two bodies are the case that can be solved, and Newton solved it. Write r for the separation and the two '
    + 'equations collapse into one: r accelerates as −μr/|r|³ with μ = G(m₁+m₂), which is the one-body problem Kepler’s '
    + 'laws describe. Each body then traces a scaled copy of that conic about the centre of mass — the heavier one '
    + 'makes the smaller loop, in the ratio of the masses — while the centre of mass itself moves in a straight line. '
    + 'The orange curves here are that answer, drawn from the state this run started at, and the panel below is the '
    + 'distance between it and the integration. It grows, slowly, and the growth is the integrator, not the physics.',
  conserve: 'Three things cannot change in an isolated system: its momentum, its angular momentum and its energy. A '
    + 'numerical method keeps some of them exactly and some of them only nearly, and which is which is a property of '
    + 'the method, not of the physics. This one (PEFRL, fourth order) applies its forces in equal and opposite pairs, '
    + 'so momentum and angular momentum survive to the last bit — measured here at a few parts in 10¹⁵ over thousands '
    + 'of frames. The energy is different: it wobbles by the order of the method and returns, which is what a '
    + 'symplectic integrator buys you. PhET’s own step, run beside it on the same system, carries the PEFRL '
    + 'coefficients but evaluates the force once a step instead of four times, which makes it first order — halve the '
    + 'step and its error halves, while this one drops by sixteen.'
};

function FR(t, b){ return '<span class="frac"><span class="t">' + t + '</span><span class="b">' + b + '</span></span>'; }
function EQ(n, body){ return '<div class="eq"><span class="n">[' + n + ']</span>' + body + '</div>'; }
const DERIV = {
  intro: '<h4>the law, and its units</h4>'
    + EQ(1, 'm<sub>i</sub> <b>r</b>&Prime;<sub>i</sub> = &minus;G &sum;<sub>j&ne;i</sub> ' + FR('m<sub>i</sub>m<sub>j</sub>(<b>r</b><sub>i</sub> &minus; <b>r</b><sub>j</sub>)', '|<b>r</b><sub>i</sub> &minus; <b>r</b><sub>j</sub>|&sup3;'))
    + EQ(2, '<span class="rm">units:</span> AU, 10&sup2;&#8312; kg, &ldquo;km/s&rdquo;; G = 4.4567 <span class="rm">(PhET&rsquo;s)</span>; 1 time unit = ' + fmt(T_U_YR, 4) + ' yr')
    + EQ(3, '<span class="rm">CODATA gives</span> G = G<sub>SI</sub>&middot;10&sup2;&#8312;/(AU&middot;10&#8310;) = ' + fmt(G_SI_UNITS, 4) + ' <span class="rm">in the same units, so PhET&rsquo;s &ldquo;km/s&rdquo; is</span> ' + fmt(KMS_TRUE, 6) + ' km/s')
    + '<p>PhET solves its time unit from its own G rather than from the AU and the km/s, which is where the 0.05 % comes from. Its presets are kept exactly, so they move here as they move there.</p>'
    + '<div class="cite">pins: the constants, the eleven systems after the centre-of-mass subtraction, the body radii &mdash; derive.py</div>',
  lab: '<h4>what each system is</h4>'
    + EQ(1, '<span class="rm">every system loads with</span> &sum;m<sub>i</sub><b>v</b><sub>i</sub> = 0 <span class="rm">(PhET&rsquo;s followCenterOfMass)</span>')
    + EQ(2, '<span class="rm">trojans:</span> L4, L5 <span class="rm">at</span> &plusmn;60&deg;; <span class="rm">measured libration</span> &minus;62.9&deg;&hellip;&minus;57.1&deg; <span class="rm">and</span> +55.8&deg;&hellip;+64.7&deg;')
    + EQ(3, '<span class="rm">four star ballet:</span> &mu;<sub>eff</sub> = Gm(1/&radic;2 + &frac14;), e = 0.3837, T = 0.2870 <span class="rm">units; the square stays square to 2e-14</span>')
    + EQ(4, '<span class="rm">&ldquo;hyperbolic&rdquo;:</span> v/v<sub>esc</sub> = 0.878, 0.929, 0.995 &nbsp;&rArr;&nbsp; e = 0.954, 0.926, 0.990 &mdash; <span class="rm">all three are bound</span>')
    + '<p>A collision here merges the pair and conserves mass, momentum and the centre of mass. PhET instead keeps the heavier body&rsquo;s mass and gives it the lighter one&rsquo;s momentum, so its total mass falls; both conserve momentum.</p>'
    + '<div class="cite">pins: every preset&rsquo;s energy, angular momentum and centre of mass; the trojan libration, the ballet&rsquo;s period and closure, the slingshot&rsquo;s 90.7 % energy gain, the &ldquo;hyperbolic&rdquo; eccentricities &mdash; derive.py (solve_ivp, rtol 1e-12)</div>',
  exact: '<h4>two bodies, in closed form</h4>'
    + EQ(1, '<b>r</b> = <b>r</b>&#8322; &minus; <b>r</b>&#8321; &nbsp;&rArr;&nbsp; <b>r</b>&Prime; = &minus;&mu;<b>r</b>/|<b>r</b>|&sup3;, &nbsp; &mu; = G(m&#8321; + m&#8322;)')
    + EQ(2, '<b>R</b> = ' + FR('m&#8321;<b>r</b>&#8321; + m&#8322;<b>r</b>&#8322;', 'm&#8321; + m&#8322;') + ' &nbsp;&rArr;&nbsp; <b>R</b>&Prime; = 0: <span class="rm">the centre of mass drifts in a straight line</span>')
    + EQ(3, '<b>r</b>&#8321; = <b>R</b> &minus; ' + FR('m&#8322;', 'M') + '<b>r</b>, &nbsp; <b>r</b>&#8322; = <b>R</b> + ' + FR('m&#8321;', 'M') + '<b>r</b> &nbsp;<span class="rm">— two similar conics, in the ratio of the masses</span>')
    + EQ(4, '<span class="rm">and on that conic:</span> M = E &minus; e sin E = n(t &minus; t&#8320;), &nbsp; T = 2&pi;&radic;(a&sup3;/&mu;)')
    + '<p>The same Kepler solver as keplers-laws.html, from the same engine file. The error drawn below is the integrator&rsquo;s alone: the exact solution is evaluated from the start state at the same instant.</p>'
    + '<div class="cite">pins: a, e, T of PhET&rsquo;s Intro system; the integration against the closed form at four times to 1e-9 AU; the closure of the exact solution after one period &mdash; derive.py</div>',
  conserve: '<h4>what the method keeps</h4>'
    + EQ(1, '<span class="rm">a kick:</span> &Delta;<b>v</b><sub>i</sub> = c h <b>a</b><sub>i</sub>, <span class="rm">built pairwise, so</span> &sum;m<sub>i</sub>&Delta;<b>v</b><sub>i</sub> = 0 <span class="rm">and</span> &sum;m<sub>i</sub><b>r</b><sub>i</sub>&times;&Delta;<b>v</b><sub>i</sub> = 0')
    + EQ(2, '<span class="rm">a drift:</span> <b>r</b><sub>i</sub> &rarr; <b>r</b><sub>i</sub> + c h <b>v</b><sub>i</sub> <span class="rm">leaves</span> <b>r</b>&times;<b>v</b> <span class="rm">alone &mdash; so p and L are exact, to rounding</span>')
    + EQ(3, 'PEFRL: &xi; = 0.17861790, &lambda; = &minus;0.21234183, &chi; = &minus;0.06626458 &nbsp;<span class="rm">(four force evaluations a step; error &prop; h&#8308;)</span>')
    + EQ(4, "PhET's step: <span class=\"rm\">the same coefficients, ONE acceleration &rArr;</span> x + vh + &frac12;ah&sup2;, v + ah &nbsp;<span class=\"rm\">(error &prop; h)</span>")
    + '<p>Measured by halving the step four times on the Sun&ndash;planet system: ratios 16.0, 16.0, 16.6 (order 4.02) against 1.9, 2.0, 2.0 (order 0.97). PhET hides it with 4,000/N substeps a frame &mdash; even so its energy drifts 3.7e-6 in the first second.</p>'
    + '<div class="cite">pins: both orders; |&Delta;E/E| &le; 6.1e-10, |&Delta;L/L| &le; 1.3e-14 and |&Delta;p|/p &le; 7e-15 over 2,000 frames of four systems &mdash; derive.py</div>'
};
