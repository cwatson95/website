
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
    if(st.view !== k){
      st.view = k;
      /* the two PhET screens ARE views here, so landing on one selects that screen; the three
         analysis views read whichever screen the chips hold */
      if(k === 'model' || k === 'scale') st.screen = k;
      syncMasses();
    }
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
    const sync = () => { inp.value = st[key]; val.innerHTML = fmtf(st[key]); };
    inp.addEventListener('input', () => {
      st[key] = parseFloat(inp.value);
      if(onchg) onchg();
      val.innerHTML = fmtf(st[key]); syncPanel(); dirty = true; refresh();
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

  const gSys = h('div', {class: 'grp'}, h('h3', null, 'the system'));
  const sysChips = chipRow(SYSTEMS, 'system', o => loadSystem(o.id));
  gSys.appendChild(sysChips); trackChips(gSys, SYSTEMS, 'system');
  const scrChips = chipRow(SCREENS, 'screen', () => { syncMasses(); });
  gSys.appendChild(scrChips); trackChips(gSys, SCREENS, 'screen');
  const sysTag = h('div', {class: 'tag'}); gSys.appendChild(sysTag);

  const gBodies = h('div', {class: 'grp'}, h('h3', null, 'the masses'));
  for(let i = 0; i < 3; i++)
    gBodies.appendChild(slider('mass' + i, 'body ' + (i + 1) + ' mass', 0.5, 2, 0.01,
      v => massLabel(i, v), () => setMass(i, st['mass' + i])));
  const bodyTag = h('div', {class: 'tag'}); gBodies.appendChild(bodyTag);
  function massLabel(i, mult){
    const sys = curSys();
    if(!sys || i >= sys.S.n) return fmt(mult, 2) + '&times;';
    return fmt(mult, 2) + '&times; = ' + massReadout(sys.S, i, sys.cfg.id);
  }

  const gShow = h('div', {class: 'grp'}, h('h3', null, 'gravity, and what is drawn'));
  gShow.appendChild(h('div', {class: 'checks'},
    checkbox('gravity', 'gravity acts (PhET&rsquo;s on/off switch)', () => { coastAnchor(curSys()); }),
    checkbox('velocity', 'velocity arrows (drag the V)'),
    checkbox('force', 'gravity-force arrows'), checkbox('path', 'path'),
    checkbox('massOn', 'mass'), checkbox('grid', 'grid'),
    checkbox('tape', 'measuring tape'), checkbox('com', 'centre of mass')));
  gShow.appendChild(slider('fpow', 'gravity arrows &times;10^n', -2, 8, 1, v => '&times;10^' + fmt(v, 0)));
  gShow.appendChild(h('div', {class: 'btnrow'},
    h('button', {onclick: () => { sysClearPaths(curSys()); dirty = true; refresh(); }}, 'clear the path')));
  const showTag = h('div', {class: 'tag'}); gShow.appendChild(showTag);

  const gCirc = h('div', {class: 'grp'}, h('h3', null, 'the start speed'));
  gCirc.appendChild(slider('vfrac', 'v / v_c', 0.1, 1.8, 0.01, v => fmt(v, 2) + '&times; v_c'));
  const circTag = h('div', {class: 'tag'}); gCirc.appendChild(circTag);

  const gCmp = h('div', {class: 'grp'}, h('h3', null, 'the comparison'),
    h('div', {class: 'checks'}, checkbox('shadow', 'run PhET&rsquo;s own step beside ours')));
  const cmpTag = h('div', {class: 'tag'}); gCmp.appendChild(cmpTag);

  const gClock = h('div', {class: 'grp'}, h('h3', null, 'the clock'));
  gClock.appendChild(h('div', {class: 'checks'}, checkbox('running', 'time runs')));
  const speedChips = chipRow(SPEEDS, 'speed'); gClock.appendChild(speedChips); trackChips(gClock, SPEEDS, 'speed');
  gClock.appendChild(slider('zoom', 'zoom', PH.ZOOM_MIN, PH.ZOOM_MAX, 0.05, v => fmt(v, 2) + '&times;'));
  gClock.appendChild(h('div', {class: 'btnrow'},
    h('button', {onclick: () => { const was = st.running; st.running = true; runStep(); st.running = was;
                                  dirty = true; refresh(); }}, 'step'),
    h('button', {onclick: () => { sysRestart(curSys()); st.running = false; syncMasses();
                                  dirty = true; refresh(); }}, 'return the bodies'),
    h('button', {onclick: () => { const v = st.view; Object.assign(st, DEFAULTS); st.view = v;
                                  if(v === 'model' || v === 'scale') st.screen = v;
                                  simReset(); syncChips(); syncPanel(); dirty = true; refresh(); }}, 'reset all')));
  const clockTag = h('div', {class: 'tag'}); gClock.appendChild(clockTag);

  const gInfo = h('div', {class: 'grp'}, h('h3', null, 'what you are looking at'), h('div', {id: 'info'}),
    h('div', {class: 'src', html: 'Remake of PhET Interactive Simulations&rsquo; <b>Gravity and Orbits</b> '
      + '(University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      + 'PhET&rsquo;s values are read out of its published build (1.6.28) and named as PhET&rsquo;s: '
      + 'G = 6.67408e-11, Sun 1.989e30 kg / 6.957e8 m, Earth 5.9724e24 kg / 6.371e6 m at 1.47098074e11 m '
      + 'moving 30,300 m/s, Moon 7.346e22 kg / 1.7274e6 m at 3.633e8 m moving 1,082 m/s, Space Station '
      + '419,725 kg / 45.5 m at 6,718,045.5 m moving 7,706 m/s, the 86,400 s day and 36,000 s base step, '
      + 'and every exaggeration factor of the Model screen. The measured column is the NASA planetary fact '
      + 'sheets (Sun, Earth, Moon) and NASA&rsquo;s ISS Facts and Figures, each at the precision that page '
      + 'prints. Everything else is computed here and pinned in selfTest to '
      + 'build/gravity-and-orbits/derive.py (scipy brentq and solve_ivp, DOP853 at rtol 1e-13).'}));
  const gPhys = h('div', {class: 'grp'}, h('h3', null, 'the physics'), h('div', {id: 'phys'}));
  [gSys, gBodies, gShow, gCirc, gCmp, gClock, gInfo, gPhys].forEach(g => panel.appendChild(g));
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
    const v = st.view, sys = curSys();
    gCirc.hidden = (v !== 'circ');
    gCmp.hidden = (v !== 'cons');
    for(const k in rows) rows[k].sync();
    for(let i = 0; i < 3; i++){
      rows['mass' + i].row.hidden = i >= sys.S.n;
      /* PhET builds the Sun-Planet-Moon moon with massSettable false, so its slider is
         dead there; a live control that is ignored is worse than no control */
      enable('mass' + i, i < sys.S.n && sys.S.settable[i]);
    }
    enable('fpow', st.force);
    /* the screen chips are the analysis views' own control; on the two PhET screens the tab IS
       the screen, so a live chip row there would be a control that contradicts the tab */
    [].forEach.call(scrChips.children, c => { c.disabled = (v === 'model' || v === 'scale'); });
    scrChips.style.opacity = (v === 'model' || v === 'scale') ? '0.42' : '1';
    sysTag.innerHTML = 'PhET&rsquo;s four systems, on its two screens. The Model screen draws the bodies far '
      + 'bigger than they are (and bends two things to keep the picture working); To Scale draws them true. '
      + 'On the first two views the tab picks the screen; on the analysis views these chips do.';
    bodyTag.innerHTML = 'PhET&rsquo;s sliders run from half to double each body&rsquo;s own mass, and the '
      + 'readout is PhET&rsquo;s own (Earth masses, or Space Station masses). Setting a mass stops the clock '
      + 'and starts the run again, as PhET does. Halving the Sun puts the Earth above escape speed: '
      + 'e = ' + fmt(REF.mass.half.e, 3) + ', unbound.';
    showTag.innerHTML = 'velocity arrows are ' + sigf(velScale(sys) * 1000, 3) + ' px per km/s here; gravity '
      + 'arrows are ' + fmt(FSCALE, 0) + ' px at the pull the pair starts with (' + sigf(fRef(sys), 3)
      + ' N), times the power. Gravity off is a pure drift &mdash; straight lines, constant speed.';
    circTag.innerHTML = 'the conic is computed in closed form from the state, not integrated: at exactly '
      + '1.00 the eccentricity is 0 to the last bit, and at &radic;2 the energy is zero to 4e-16 of GM/r.';
    cmpTag.innerHTML = 'PhET&rsquo;s shipped step evaluates the force ONCE and reuses it for all four kicks, '
      + 'which is first order; ours evaluates it four times, which is the fourth-order method PhET names. '
      + 'Both start from the same state.';
    clockTag.innerHTML = 'space runs and pauses &nbsp; <b>g</b> flips gravity &nbsp; <b>r</b> returns the '
      + 'bodies &nbsp; 1&ndash;5 switch views. One frame is ' + sigf(curFrameDt(sys), 4) + ' s = '
      + plain(timeStrFine(curFrameDt(sys), sys.cfg.minutes)) + ' (PhET&rsquo;s 0.13125 &times; '
      + sigf(sys.cfg.dt, 5) + ' s &times; ' + speedSteps() + ').';
  }

  function refresh(){
    try{
      const M = S.model();
      roEl.innerHTML = readoutHTML(M);
      eqEl.innerHTML = eqbarHTML(M);
      tagEl.innerHTML = tagHTML(M);
      hintEl.textContent = dragsHere(st.view)
        ? 'drag a body, or the tip of its V arrow · space runs · g flips gravity · 1–5 switch views'
        : 'space runs · g flips gravity · r returns the bodies · 1–5 switch views';
      infoEl.innerHTML = INFO[st.view] || '';
      physEl.innerHTML = DERIV[st.view] || '';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown', e => {
    canvas.setPointerCapture(e.pointerId);
    const r = canvas.getBoundingClientRect();
    /* no dirty flag here: refresh() draws unconditionally on this same path, so a flag would
       be a second guard on one path and its mutant would be equivalent (it was, in a sweep) */
    if(S.pointer('down', e.clientX - r.left, e.clientY - r.top)){ canvas.classList.add('dragging'); syncPanel(); refresh(); }
  });
  canvas.addEventListener('pointermove', e => {
    if(!canvas.classList.contains('dragging') && e.buttons === 0) return;
    const r = canvas.getBoundingClientRect();
    if(S.pointer('move', e.clientX - r.left, e.clientY - r.top)){ dirty = true; roEl.innerHTML = readoutHTML(S.model()); }
  });
  const up = () => { canvas.classList.remove('dragging'); if(S.pointer('up', 0, 0)){ dirty = true; syncMasses(); syncPanel(); refresh(); } };
  canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);

  window.addEventListener('keydown', e => {
    if(e.key === ' '){ e.preventDefault(); st.running = !st.running; syncPanel(); dirty = true; refresh(); }
    else if(e.key === 'g'){ st.gravity = !st.gravity; coastAnchor(curSys()); syncPanel(); dirty = true; refresh(); }
    else if(e.key === 'r'){ sysRestart(curSys()); st.running = false; syncMasses(); syncPanel(); dirty = true; refresh(); }
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
  model: 'PhET’s Model screen, and the bargain it makes. The physics is Newton’s, with PhET’s own masses and '
    + 'speeds, but nothing about the drawing is honest: the Sun is fifty times too big, the Earth eight hundred, '
    + 'and in Sun-Planet-Moon the Moon has been pushed out to 1.7 drawn planet radii — twenty-four times its real '
    + 'distance — and given 10,200 times the planet’s pull so that it still goes round. PhET also nails the star '
    + 'down. All of that is printed on the canvas here, because the alternative is a picture that quietly claims '
    + 'to be something it is not. What the screen buys in return is the one thing you cannot get from the honest '
    + 'drawing: you can see all the bodies at once. Switch gravity off with the checkbox or the g key and watch '
    + 'everything leave in a straight line — that is Newton’s first law, and it is exactly what the code does.',
  scale: 'The same systems, drawn true, which is PhET’s point in shipping both. At PhET’s own zoom the Sun is '
    + 'about two and a half pixels across and the Earth a fortieth of a pixel; the space station, 94 m of truss, '
    + 'is three thousandths of a pixel beside an Earth four hundred pixels wide. Anything under twelve pixels '
    + 'gets a line pointing at it and its name, which is what PhET does and what happens here. The panels below '
    + 'are the reason: put the diameters and the separation on one logarithmic axis and they span eight orders '
    + 'of magnitude, so no single linear picture can hold both. Nothing is nailed down and nothing is boosted on '
    + 'this screen, which is why the conservation view finds it exact.',
  circ: 'Why any speed at all keeps you up. A body going sideways at speed v on a circle of radius r needs a '
    + 'centripetal pull mv²/r to stay on it; gravity supplies GMm/r². Set those equal and the mass cancels — '
    + 'which is why a feather and the space station orbit alike — leaving v = √(GM/r), one speed for each radius '
    + 'and no other. The slider is the ratio to that speed. Below it the orbit falls inside the circle and the '
    + 'start point becomes apoapsis; above it the orbit swings out and the start point becomes periapsis; at √2 '
    + 'the energy reaches zero and the body never returns. The first panel is that law on a log axis, with '
    + 'PhET’s three real orbits sitting on it; the second is what follows by squaring, T² ∝ a³, which Kepler '
    + 'found seventy years before Newton explained it.',
  exact: 'Two bodies are the case that can be solved, and this is the solution. Take the state vector, get the '
    + 'elements from it in closed form — vis-viva gives a, the eccentricity vector gives e and the direction of '
    + 'periapsis, the sign of xv_y − yv_x gives the sense of travel — and then the position at any later time '
    + 'comes from Kepler’s equation M = E − e sin E, solved by Newton on a bracket in a few iterations. No '
    + 'integration anywhere. The orange curve is that answer, anchored at the state this run started from, and '
    + 'the rings are where it puts the bodies at this instant. The panel below is the distance between that and '
    + 'the integrated position, which is the integrator’s error and nothing else. Three bodies have no such '
    + 'answer, which is why Sun-Planet-Moon draws the system with a sentence where the comparison would be.',
  cons: 'Three quantities cannot change in an isolated system, and a numerical method keeps some of them exactly '
    + 'and others only nearly. This one applies its forces as equal and opposite pairs and moves positions along '
    + 'straight lines, so momentum and angular momentum survive to the last bit whatever the step, and the '
    + 'energy wobbles by the order of the method and comes back. On the To Scale screen you can watch that: '
    + 'momentum and angular momentum flat at a few parts in 10¹⁵, energy at a part in 10¹³. On the Model screen '
    + 'they are not flat at all, and the reason is not numerical — a nailed-down star takes momentum from '
    + 'nowhere, and a moon that feels 10,200 times the planet’s pull with no reaction breaks Newton’s third law '
    + 'outright. The lower left panel halves the step four times and reads off the order of both integrators: '
    + 'four for the real PEFRL, one for PhET’s as shipped.'
};

function FR(t, b){ return '<span class="frac"><span class="t">' + t + '</span><span class="b">' + b + '</span></span>'; }
function EQ(n, body){ return '<div class="eq"><span class="n">[' + n + ']</span>' + body + '</div>'; }
const DERIV = {
  model: '<h4>the law, and what this screen changes</h4>'
    + EQ(1, 'm<sub>i</sub><b>r</b>&Prime;<sub>i</sub> = &minus;G&sum;<sub>j&ne;i</sub> '
        + FR('m<sub>i</sub>m<sub>j</sub>(<b>r</b><sub>i</sub>&minus;<b>r</b><sub>j</sub>)',
             '|<b>r</b><sub>i</sub>&minus;<b>r</b><sub>j</sub>|&sup3;') + ', &nbsp; G = 6.67408&times;10&#8315;&sup1;&sup1;')
    + EQ(2, '<span class="rm">drawn radii:</span> Sun &times;50, Earth &times;800, Moon &times;800, '
        + 'station &times;20000 <span class="rm">(PhET&rsquo;s own factors)</span>')
    + EQ(3, '<span class="rm">and in Sun-Planet-Moon:</span> r<sub>moon</sub> = 1.7 R<sub>planet,drawn</sub> = '
        + sigf(REF.modelmoon.r, 4) + ' m = ' + fmt(REF.modelmoon.rratio, 2) + '&times; <span class="rm">the real</span>, '
        + 'v &times;21, F<sub>moon&larr;planet</sub> &times;10200 <span class="rm">(no reaction)</span>')
    + '<p>A circular orbit at that radius with the plain pull needs ' + fmt(REF.modelmoon.vc_plain, 1)
    + ' m/s; with the boost it needs ' + fmt(REF.modelmoon.vc_boost, 0) + ' m/s, against the '
    + fmt(REF.modelmoon.v, 0) + ' m/s PhET gives it. The boost that would make it exactly circular is '
    + fmt(REF.modelmoon.boost_for_circle, 0) + '.</p>'
    + '<div class="cite">pins: every scene&rsquo;s state after PhET&rsquo;s centre-of-momentum shift, its energy, '
    + 'angular momentum and momentum, and all four exaggeration factors &mdash; derive.py</div>',
  scale: '<h4>the sizes, and why two screens</h4>'
    + EQ(1, '<span class="rm">PhET&rsquo;s view scale:</span> 1.5&times;10&#8315;&#8313; &times; zoom '
        + '<span class="rm">view units per metre, on a 987.5 &times; 772.5 stage</span>')
    + EQ(2, '<span class="rm">so at its own zoom:</span> Sun ' + sigf(REF.px.starPlanet[0].px, 4)
        + ' px across, Earth ' + sigf(REF.px.starPlanet[1].px, 4) + ' px, Moon '
        + sigf(REF.px.starPlanetMoon[2].px, 4) + ' px, station ' + sigf(REF.px.planetSatellite[1].px, 4) + ' px')
    + EQ(3, '<span class="rm">the span:</span> station 91 m &hellip; Sun&ndash;Earth 1.47&times;10&sup1;&sup1; m '
        + '&mdash; nine orders of magnitude in one picture')
    + '<p>PhET&rsquo;s own rule, kept here: a body whose drawn diameter falls to 12 px or less gets a leader line and its name, and nothing is drawn below one pixel.</p>'
    + '<div class="cite">pins: the true drawn diameter of every body at PhET&rsquo;s zoom, and the view half-height its scale implies &mdash; derive.py</div>',
  circ: '<h4>where v = &radic;(GM/r) comes from</h4>'
    + EQ(1, '<span class="rm">circular motion needs</span> F = mv&sup2;/r; <span class="rm">gravity supplies</span> F = GMm/r&sup2;')
    + EQ(2, 'GMm/r&sup2; = mv&sup2;/r &nbsp;&rArr;&nbsp; v = &radic;(GM/r) &nbsp;<span class="rm">(m cancels: every body orbits alike)</span>')
    + EQ(3, 'T = 2&pi;r/v = 2&pi;&radic;(r&sup3;/GM) &nbsp;&rArr;&nbsp; T&sup2;/a&sup3; = 4&pi;&sup2;/GM '
        + '<span class="rm">&mdash; Kepler&rsquo;s third law</span>')
    + EQ(4, '&frac12;v&sup2; &minus; GM/r = 0 &nbsp;&rArr;&nbsp; v<sub>esc</sub> = &radic;(2GM/r) = &radic;2 v<sub>c</sub>')
    + EQ(5, '<span class="rm">with the masses in it:</span> T&sup2;/a&sup3; = 4&pi;&sup2;/G(M+m) '
        + '<span class="rm">&mdash; Kepler&rsquo;s law is exact only for a test mass</span>')
    + '<p>That (T<sub>m</sub>/T<sub>s</sub>)&sup2; = (r<sub>m</sub>/r<sub>s</sub>)&sup3; for two circular '
    + 'orbits about the same mass is an <em>identity</em> of [3], not a measurement, and it is asserted as one. '
    + 'The measurement is [5]: the space station&rsquo;s T&sup2;/a&sup3; about the Earth is '
    + fmt(100 * ((PH.EARTH_MASS + PH.MOON_MASS) / (PH.EARTH_MASS + PH.STATION_MASS) - 1), 2)
    + ' % larger than the Moon&rsquo;s &mdash; a bigger total mass gives a smaller constant &mdash; and that '
    + 'figure is exactly the Moon&rsquo;s own mass as a fraction of the Earth&rsquo;s. The Moon is not a test '
    + 'particle. The periods behind it are the ones the elements give, and derive.py '
    + 'separately measures each by integrating the orbit until it closes (agreeing to 2e-9).</p>'
    + '<div class="cite">pins: v_c and T at all three radii to 1e-12 by two routes each, the mass-corrected third law to 1e-13, the integrated period against the Kepler period to 1e-8, and the conic at seven start speeds including e = 0 at exactly 1.00 &mdash; derive.py</div>',
  exact: '<h4>the closed form</h4>'
    + EQ(1, '<span class="rm">from the state:</span> a = ' + FR('1', '2/r &minus; v&sup2;/&mu;')
        + ', &nbsp; <b>e</b> = ' + FR('(v&sup2;&minus;&mu;/r)<b>r</b> &minus; (<b>r</b>&middot;<b>v</b>)<b>v</b>', '&mu;'))
    + EQ(2, 'M = E &minus; e sin E = n(t &minus; t&#8320;), &nbsp; n = &radic;(&mu;/a&sup3;)')
    + EQ(3, 'r = a(1 &minus; e cos E), &nbsp; x = a(cos E &minus; e), &nbsp; y = a&radic;(1&minus;e&sup2;) sin E')
    + EQ(4, '<span class="rm">a FIXED star:</span> &mu; = GM; <span class="rm">two free bodies:</span> &mu; = G(M+m), '
        + '<span class="rm">and each traces a similar conic about the centre of mass</span>')
    + '<p>Kepler&rsquo;s equation is solved by Newton safeguarded on the bracket [M &minus; e, M + e] to 1e-15 in the step; derive.py checks the solver against scipy&rsquo;s brentq (worst residual '
    + REF.kepler_resid.toExponential(1) + ') and the whole answer against solve_ivp at rtol 1e-13.</p>'
    + '<div class="cite">pins: a, e, T, periapsis and apoapsis of every two-body scene on both screens; the integration against the closed form after 400 frames; the period measured from the run &mdash; derive.py</div>',
  cons: '<h4>what the method keeps, and what PhET bends</h4>'
    + EQ(1, '<span class="rm">a kick:</span> &Delta;<b>v</b><sub>i</sub> = ch<b>a</b><sub>i</sub>, <span class="rm">built pairwise &rArr;</span> &sum;m<sub>i</sub>&Delta;<b>v</b><sub>i</sub> = 0, &nbsp; &sum;m<sub>i</sub><b>r</b><sub>i</sub>&times;&Delta;<b>v</b><sub>i</sub> = 0')
    + EQ(2, 'PEFRL: &xi; = 0.17861790, &lambda; = &minus;0.21234183, &chi; = &minus;0.06626458 '
        + '<span class="rm">(PhET&rsquo;s own coefficients; four force evaluations a step, error &prop; h&#8308;)</span>')
    + EQ(3, "PhET's step: <span class=\"rm\">the same composition with ONE acceleration &rArr;</span> "
        + '<b>r</b> + <b>v</b>h + &frac12;<b>a</b>h&sup2;, <b>v</b> + <b>a</b>h <span class="rm">(error &prop; h)</span>')
    + EQ(4, '<span class="rm">gravity off:</span> <b>r</b> &rarr; <b>r</b> + <b>v</b>h <span class="rm">and nothing else &mdash; a straight line, exactly</span>')
    + '<p>Measured by halving the step over 40 days: ratios 16.00, 16.00, 15.97 (order '
    + fmt(REF.orders.pefrl.order, 3) + ') against 1.99, 1.99, 2.00 (order ' + fmt(REF.orders.phet.order, 3)
    + '). The step counts stay coarse on purpose: at 1600 steps PEFRL&rsquo;s own error is 3&times;10&#8315;&sup3; m, '
    + 'which IS the roundoff floor of a 10&sup1;&sup1;-metre coordinate, and the measured ratio falls to 1.2 on correct code.</p>'
    + '<div class="cite">pins: |&Delta;E/E|, |&Delta;L/L| and |&Delta;p|/p over 4,000 frames of all eight scenes; the momentum the Model screen loses; gravity-off straight lines at zero residual; both orders &mdash; derive.py</div>'
};
