
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
    if(st.view !== k) st.view = k;
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
        syncPanel(); dirty = true; refresh(); }});
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
  /* any change to the orbit restarts its clock, as PhET's does when the user takes hold */
  const reOrbit = () => { SIM.t = 0; ST.running = false; SIM.sweep = {erased: false, tErase: 0};
                          SIM.periodTrace = null; traceNote(klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular)); };

  const gStar = h('div', {class: 'grp'}, h('h3', null, 'the star'));
  gStar.appendChild(slider('mass', 'mass, M☉', 0.5, 2, 0.01, v => fmt(v, 2) + (v === 1 ? ' (our Sun)' : ''), () => {
    /* PhET snaps the slider to our Sun within 5 % */
    if(Math.abs(st.mass - 1) < 0.05) st.mass = 1;
    traceReset(); reOrbit();
  }));
  gStar.appendChild(h('div', {class: 'checks'}, checkbox('circular', 'hold the orbit circular', reOrbit)));
  const starTag = h('div', {class: 'tag'}); gStar.appendChild(starTag);

  const gTarget = h('div', {class: 'grp'}, h('h3', null, 'target orbit'));
  const tgtChips = chipRow(TARGETS, 'target'); gTarget.appendChild(tgtChips); trackChips(gTarget, TARGETS, 'target');
  gTarget.appendChild(h('div', {class: 'btnrow'}, h('button', {onclick: () => {
    if(st.target === 'none' || st.mass !== 1) return;
    const t = targetById(st.target);
    st.px = t.a * (1 - t.e); st.py = 0; st.vx = 0;
    st.vy = auYrToKms(Math.sqrt(starMu(st.mass) * (1 + t.e) / (t.a * (1 - t.e))));
    st.circular = false; reOrbit(); traceReset(); syncPanel(); dirty = true; refresh();
  }}, 'put the planet on it')));
  const tgtTag = h('div', {class: 'tag'}); gTarget.appendChild(tgtTag);

  const gFirst = h('div', {class: 'grp'}, h('h3', null, 'the ellipse'));
  gFirst.appendChild(h('div', {class: 'checks'},
    checkbox('foci', 'foci'), checkbox('string', 'string: d₁ + d₂'), checkbox('axes', 'axes'),
    checkbox('semiaxes', 'semiaxes a, b'), checkbox('ecc', 'eccentricity c = ae')));
  const firstTag = h('div', {class: 'tag'}); gFirst.appendChild(firstTag);

  const gSecond = h('div', {class: 'grp'}, h('h3', null, 'equal areas'));
  gSecond.appendChild(slider('div', 'period divisions', PHET.DIV_MIN, PHET.DIV_MAX, 1, v => fmt(v, 0)));
  gSecond.appendChild(h('div', {class: 'checks'},
    checkbox('areaVals', 'area values'), checkbox('timeVals', 'time values'),
    checkbox('apo', 'apoapsis'), checkbox('peri', 'periapsis')));
  gSecond.appendChild(h('div', {class: 'btnrow'}, h('button', {onclick: () => { eraseSectors(); dirty = true; refresh(); }}, 'erase the sectors')));
  const secondTag = h('div', {class: 'tag'}); gSecond.appendChild(secondTag);

  const gSwept = h('div', {class: 'grp'}, h('h3', null, 'sectors'),
    h('div', {class: 'checks'}, checkbox('swept', 'swept sectors')));

  const gThird = h('div', {class: 'grp'}, h('h3', null, 'the chart'));
  gThird.appendChild(h('div', {class: 'tag'}, 'the power on a'));
  const paChips = chipRow(POWERS, 'pa'); gThird.appendChild(paChips); trackChips(gThird, POWERS, 'pa');
  gThird.appendChild(h('div', {class: 'tag'}, 'the power on T'));
  const ptChips = chipRow(POWERS, 'pt'); gThird.appendChild(ptChips); trackChips(gThird, POWERS, 'pt');
  gThird.appendChild(h('div', {class: 'checks'},
    checkbox('loglog', 'log–log axes'), checkbox('showA', 'semi-major axis on the orbit'),
    checkbox('showT', 'period trace')));
  gThird.appendChild(h('div', {class: 'btnrow'}, h('button', {onclick: () => { traceReset(); dirty = true; refresh(); }}, 'forget the trace')));
  const thirdTag = h('div', {class: 'tag'}); gThird.appendChild(thirdTag);

  const gAnom = h('div', {class: 'grp'}, h('h3', null, 'where in the orbit'));
  gAnom.appendChild(slider('mfrac', 't through one period', 0, 0.999, 0.001, v => fmt(v, 3) + ' T', () => {
    const el = klOrbit(st.px, st.py, st.vx, st.vy, st.mass, st.circular);
    if(el.allowed) SIM.t = st.mfrac * el.T;
  }));
  const anomTag = h('div', {class: 'tag'}); gAnom.appendChild(anomTag);

  const gShow = h('div', {class: 'grp'}, h('h3', null, 'show'));
  gShow.appendChild(h('div', {class: 'checks'},
    checkbox('velocity', 'velocity arrow (drag its tip)'), checkbox('speedLab', 'speed'),
    checkbox('gravity', 'gravity force'), checkbox('grid', 'grid, 1 AU'),
    checkbox('tape', 'measuring tape'), checkbox('stopwatch', 'stopwatch')));
  gShow.appendChild(slider('fpow', 'gravity arrows ×10^n', -2, 4, 1, v => '×10^' + fmt(v, 0)));
  gShow.appendChild(h('div', {class: 'btnrow'},
    h('button', {onclick: () => { SIM.swRun = !SIM.swRun; dirty = true; refresh(); }}, 'stopwatch start/stop'),
    h('button', {onclick: () => { SIM.sw = 0; SIM.swRun = false; dirty = true; refresh(); }}, 'zero it')));
  const showTag = h('div', {class: 'tag'}); gShow.appendChild(showTag);

  const gClock = h('div', {class: 'grp'}, h('h3', null, 'the clock'));
  gClock.appendChild(h('div', {class: 'checks'}, checkbox('running', 'time runs', () => { if(st.running) onPlay(); })));
  const speedChips = chipRow(SPEEDS, 'speed'); gClock.appendChild(speedChips); trackChips(gClock, SPEEDS, 'speed');
  const zoomChips = chipRow(ZOOMS, 'zoom'); gClock.appendChild(zoomChips); trackChips(gClock, ZOOMS, 'zoom');
  gClock.appendChild(h('div', {class: 'btnrow'},
    h('button', {onclick: () => { const was = st.running; st.running = true; runStep(); st.running = was; dirty = true; refresh(); }}, 'step'),
    h('button', {onclick: () => { SIM.t = 0; st.running = false; SIM.sweep = {erased: false, tErase: 0};
                                  SIM.periodTrace = null; dirty = true; refresh(); }}, 'restart'),
    h('button', {onclick: () => { const v = st.view; Object.assign(st, DEFAULTS); st.view = v; simReset();
                                  syncChips(); syncPanel(); dirty = true; refresh(); }}, 'reset all')));
  const clockTag = h('div', {class: 'tag'}); gClock.appendChild(clockTag);

  const gInfo = h('div', {class: 'grp'}, h('h3', null, 'what you are looking at'), h('div', {id: 'info'}),
    h('div', {class: 'src', html: 'Remake of PhET Interactive Simulations&rsquo; <b>Kepler&rsquo;s Laws</b> '
      + '(University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      + 'Measured: AU = 149,597,870.7 km (IAU 2012), the Julian year, GM<sub>&#9737;</sub> = 1.32712440042e20 m&sup3;/s&sup2; '
      + '(Wikipedia, &ldquo;Standard gravitational parameter&rdquo;). PhET&rsquo;s own values (G = 4.4567, our Sun = 200&times;10&sup2;&#8312; kg, '
      + 'the star radius rule, the target orbits, the 0.01-rad Newton tolerance) are read out of its published build and named as PhET&rsquo;s. '
      + 'Everything else is computed here and pinned in selfTest to build/keplers-laws/derive.py.'}));
  const gPhys = h('div', {class: 'grp'}, h('h3', null, 'the physics'), h('div', {id: 'phys'}));
  [gStar, gTarget, gFirst, gSecond, gSwept, gThird, gAnom, gShow, gClock, gInfo, gPhys].forEach(g => panel.appendChild(g));
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
    const v = st.view, el = klOrbit(st.px, st.py, st.vx, st.vy, st.mass, st.circular);
    gTarget.hidden = !(v === 'first' || v === 'third' || v === 'all');
    gFirst.hidden = !(v === 'first' || v === 'all');
    gSecond.hidden = !(v === 'second' || v === 'all');
    gSwept.hidden = (v !== 'all');
    gThird.hidden = !(v === 'third' || v === 'all');
    gAnom.hidden = (v !== 'anom');
    for(const k in rows) rows[k].sync();
    enable('cb_string', st.foci);
    enable('cb_semiaxes', st.axes);
    enable('cb_apo', el.allowed && el.e >= PHET.E_ROUND);
    enable('cb_peri', el.allowed && el.e >= PHET.E_ROUND);
    enable('fpow', st.gravity);
    enable('mfrac', el.allowed);
    [].forEach.call(tgtChips.children, c => { c.style.opacity = st.mass === 1 ? '1' : '0.42'; });
    starTag.innerHTML = 'GM = ' + sigf(starMu(st.mass), 6) + ' AU&sup3;/yr&sup2;; the star is drawn to PhET&rsquo;s radius rule, '
      + sigf(starRadius(st.mass), 3) + ' AU. The planet&rsquo;s own mass never enters the orbit.';
    tgtTag.innerHTML = st.mass === 1 ? 'PhET&rsquo;s target orbits: drag the planet until the green orbit lies on the grey one, or press the button.'
      : 'PhET allows a target orbit only for our Sun; set the mass back to 1.00 to use one.';
    firstTag.innerHTML = 'the string is the definition: the sum of the distances to the two foci is 2a everywhere on the ellipse.';
    secondTag.innerHTML = 'the cuts are equal steps of the MEAN anomaly, so every sector takes T/N = ' + plain(yrStr(el.allowed ? el.T / st.div : 0)) + '.';
    thirdTag.innerHTML = st.pa === 3 && st.pt === 2 ? 'a&sup3; with T&sup2;: a straight line, slope 4&pi;&sup2;/GM.'
      : 'try a&sup3; with T&sup2; — no other pair of powers is a straight line through the origin.';
    anomTag.innerHTML = 'the slider is the clock: it moves the planet through one period, and the construction follows.';
    showTag.innerHTML = 'the velocity arrow is ' + fmt(VSCALE, 1) + ' px per km/s; the gravity arrow is 60 px at 1 AU, times the power.';
    clockTag.innerHTML = 'space runs and pauses &nbsp; <b>r</b> restarts &nbsp; 1&ndash;5 switch views. One frame is '
      + PHET.FRAME_YR.toExponential(3) + ' yr at normal speed (PhET&rsquo;s rate).';
  }

  function refresh(){
    try{
      const M = S.model();
      roEl.innerHTML = readoutHTML(M);
      eqEl.innerHTML = eqbarHTML(M);
      tagEl.innerHTML = tagHTML(M);
      hintEl.textContent = dragsHere(st.view) ? 'drag the planet or the tip of its velocity arrow · space runs · 1–5 switch views'
                                              : 'the slider scrubs one period · space runs · 1–5 switch views';
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
  const up = () => { canvas.classList.remove('dragging'); if(S.pointer('up', 0, 0)){ dirty = true; refresh(); } };
  canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);

  window.addEventListener('keydown', e => {
    if(e.key === ' '){ e.preventDefault(); setRunning(!st.running); syncPanel(); dirty = true; refresh(); }
    else if(e.key === 'r'){ SIM.t = 0; st.running = false; SIM.sweep = {erased: false, tErase: 0};
                            SIM.periodTrace = null; syncPanel(); dirty = true; refresh(); }
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
      try{
        S.draw();
        if(advanced && ST.view === 'anom' && rows.mfrac) rows.mfrac.sync();
        if(advanced && frameN % 10 === 0) roEl.innerHTML = readoutHTML(S.model());
      }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  simReset(); resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO = {
  first: 'Kepler had Tycho Brahe’s observations of Mars, the best in the world, and eight years of arithmetic. What came out '
    + 'in 1609 was that the orbit is an ellipse with the Sun at one focus — not a circle, not a circle on a circle. An ellipse '
    + 'is the set of points whose distances to two fixed points add to a constant, which is what the “string” shows here: '
    + 'd₁ + d₂ = 2a wherever the planet is. The star sits at one focus and nothing at all sits at the other. How far the two '
    + 'foci are apart, as a fraction of a, is the eccentricity e = c/a: zero is a circle, and the Earth’s 0.0167 is so nearly '
    + 'one that you cannot see the difference — what you can see is that the Sun is off centre. Drag the planet or the tip of '
    + 'its velocity arrow and the ellipse is recomputed from the state vector alone.',
  second: 'The second law came first, in Kepler’s notebooks: the line from star to planet sweeps equal areas in equal times. '
    + 'It is conservation of angular momentum written for an orbit — dA/dt = ½|r × v| = ½|h| is a constant of the motion, '
    + 'whatever the force, as long as it points at the star. The consequence is that a planet hurries through periapsis and '
    + 'dawdles at apoapsis: Halley’s comet spends 70 of its 76 years beyond Neptune. The sectors here are cut at equal steps '
    + 'of the MEAN anomaly, i.e. at equal times, so their areas are equal by construction — and the file checks that, in the '
    + 'browser, by integrating ½r²dν over each of them and comparing with πab/N.',
  third: 'Ten years after the first two laws, in Harmonices Mundi (1619), Kepler found the one that ties different orbits '
    + 'together: T² ∝ a³. Newton showed why, and what the constant is — 4π²/GM, which depends on the star and on nothing '
    + 'else. That is why this chart is a measuring instrument: the slope of T² against a³ weighs the star. PhET’s power chips '
    + 'let you try the wrong powers, and nothing else gives a straight line through the origin. On log–log axes the law is '
    + 'log T = (3/2) log a − ½ log(GM/4π²): every orbit about one star lies on a line of slope exactly 3/2, and changing the '
    + 'star’s mass slides the line up or down without tilting it.',
  all: 'The three laws on one orbit, as PhET’s All Laws screen puts them: the shape (an ellipse with the star at a focus), '
    + 'the pace around it (equal areas in equal times), and how the pace scales with size (T² ∝ a³). The first two are about '
    + 'one orbit; the third is about the family of them. Turn the overlays on together and the relations between them show: '
    + 'the sectors are widest where the planet is slowest, which is at apoapsis, which is the far end of the semi-major axis '
    + 'whose length sets the period.',
  anom: 'Kepler’s laws say where the orbit is and how fast the area grows, but not, directly, where the planet is at a given '
    + 'time. That needs one more step, and it is the awkward one. Take the ellipse, draw the circle of radius a about its '
    + 'centre, and project the planet vertically onto it: the angle at the centre is the eccentric anomaly E. The area swept '
    + 'is proportional to M = E − e sin E, and M grows uniformly with time — that is the second law in its most useful form. '
    + 'So to find the planet at time t you must invert M = E − e sin E for E, and no combination of elementary functions does '
    + 'it. Newton’s method does, in a handful of steps: watch the tangents walk down to the root in the right-hand panel. '
    + 'PhET stops when a step falls below 0.01 rad, which is close enough to draw; this file drives the step to 1e-15.'
};

function FR(t, b){ return '<span class="frac"><span class="t">' + t + '</span><span class="b">' + b + '</span></span>'; }
function EQ(n, body){ return '<div class="eq"><span class="n">[' + n + ']</span>' + body + '</div>'; }
const DERIV = {
  first: '<h4>the orbit from the state vector</h4>'
    + EQ(1, '<span class="rm">units:</span> AU, Julian years, M<sub>&#9737;</sub>; &nbsp; &mu; = GM = K&middot;M, &nbsp; K = GM<sub>&#9737;</sub>yr&sup2;/AU&sup3; = 39.4769264 &nbsp; <span class="rm">(1 AU/yr = 4.740470464 km/s)</span>')
    + EQ(2, '<span class="rm">vis-viva:</span> ' + FR('1', 'a') + ' = ' + FR('2', 'r') + ' &minus; ' + FR('v&sup2;', '&mu;') + ' &nbsp;&middot;&nbsp; <b>e</b> = ' + FR('(v&sup2; &minus; &mu;/r)<b>r</b> &minus; (<b>r</b>&middot;<b>v</b>)<b>v</b>', '&mu;') + ' &nbsp;&middot;&nbsp; h = xv<sub>y</sub> &minus; yv<sub>x</sub>')
    + EQ(3, 'r(&nu;) = ' + FR('a(1 &minus; e&sup2;)', '1 + e cos &nu;') + ' &nbsp;&middot;&nbsp; b = a&radic;(1&minus;e&sup2;), &nbsp; c = ae, &nbsp; d&#8321; + d&#8322; = 2a, &nbsp; q = a(1&minus;e), Q = a(1+e)')
    + '<p>The direction of <b>e</b> is the direction of periapsis and its length is the eccentricity, so one vector fixes the whole ellipse. An orbit rounder than 1e-9 is treated as a circle and its periapsis put at the planet, because otherwise the direction is made of rounding noise.</p>'
    + '<div class="cite">pins: a, e, &omega;, T, b, c, q, Q for six states against derive.py, and the same elements recovered from a state solve_ivp integrated 0.61 T later (4e-14)</div>',
  second: '<h4>equal areas</h4>'
    + EQ(1, FR('dA', 'dt') + ' = &frac12;r&sup2;' + FR('d&nu;', 'dt') + ' = &frac12;|<b>r</b> &times; <b>v</b>| = &frac12;|h| &nbsp;<span class="rm">constant for any central force</span>')
    + EQ(2, 'A(sector k) = &frac12;ab &middot; &Delta;M = ' + FR('&pi;ab', 'N') + ' &nbsp;<span class="rm">when the cuts are equal steps of</span> M')
    + EQ(3, 'M = E &minus; e sin E, &nbsp; tan ' + FR('&nu;', '2') + ' = &radic;' + FR('1+e', '1&minus;e') + ' tan ' + FR('E', '2') + ' &nbsp;&middot;&nbsp; T = ' + FR('2&pi;ab', '|h|'))
    + '<p>The area of a sector is computed two ways and the two are asserted equal: the closed form &frac12;ab&Delta;M, and 8-point Gauss&ndash;Legendre quadrature of &frac12;r&sup2;d&nu; over the same range, which knows nothing about Kepler&rsquo;s equation.</p>'
    + '<div class="cite">pins: the cuts and areas for N = 2&hellip;6 against derive.py (scipy quad, worst 1.3e-15); the quadrature against the closed form in the browser at 1e-12; &frac12;|h|&Delta;t against a 20,001-gon of the swept region (6e-9)</div>',
  third: '<h4>the third law, and what it weighs</h4>'
    + EQ(1, 'T = 2&pi;&radic;(a&sup3;/&mu;) &nbsp;&rArr;&nbsp; ' + FR('T&sup2;', 'a&sup3;') + ' = ' + FR('4&pi;&sup2;', 'GM') + ' &nbsp;<span class="rm">the same for every body about that star</span>')
    + EQ(2, 'log T = ' + FR('3', '2') + ' log a &minus; &frac12; log ' + FR('GM', '4&pi;&sup2;') + ' &nbsp;<span class="rm">slope 3/2, intercept the star&rsquo;s mass</span>')
    + EQ(3, '<span class="rm">for our Sun:</span> T&sup2;/a&sup3; = 1.0000378 yr&sup2;/AU&sup3; &nbsp;<span class="rm">(1 exactly would need the Gaussian year, 365.2569 d)</span>')
    + '<p>A test body at 1 AU takes 365.2569 d, not the Julian 365.25: the 1.9e-5 difference is the definition of the year, not an error. PhET normalises its own T to a<sup>3/2</sup> exactly.</p>'
    + '<div class="cite">pins: T for PhET&rsquo;s five target orbits, T&sup2;/a&sup3; identical across them to 1e-15, the constant against 4&pi;&sup2;/GM at four star masses &mdash; derive.py</div>',
  all: '<h4>the three together</h4>'
    + EQ(1, 'r = ' + FR('a(1&minus;e&sup2;)', '1 + e cos&nu;') + ' &nbsp;&middot;&nbsp; dA/dt = &frac12;|h| &nbsp;&middot;&nbsp; T&sup2; = ' + FR('4&pi;&sup2;a&sup3;', 'GM'))
    + EQ(2, '<span class="rm">and the one that joins them:</span> &nbsp; &frac12;v&sup2; &minus; ' + FR('&mu;', 'r') + ' = &minus;' + FR('&mu;', '2a') + ', &nbsp; |h| = &radic;(&mu;a(1&minus;e&sup2;))')
    + '<p>Two numbers — the energy and the angular momentum — fix a and e, and with them the shape, the pace and the period. Everything drawn in this file comes from those two.</p>'
    + '<div class="cite">pins: the energy and |h| identities against a, e at six states; the sector areas; the period &mdash; derive.py</div>',
  anom: '<h4>Kepler&rsquo;s equation</h4>'
    + EQ(1, 'M = nt = E &minus; e sin E, &nbsp; n = &radic;(&mu;/a&sup3;) = 2&pi;/T &nbsp;<span class="rm">(M is the area swept, scaled)</span>')
    + EQ(2, 'r = a(1 &minus; e cos E), &nbsp; x<sub>orb</sub> = a(cos E &minus; e), &nbsp; y<sub>orb</sub> = b sin E')
    + EQ(3, '<span class="rm">Newton:</span> E &larr; E &minus; ' + FR('E &minus; e sin E &minus; M', '1 &minus; e cos E') + ' &nbsp;<span class="rm">safeguarded by the bracket</span> [M &minus; e, M + e]')
    + '<p>f(E) = E &minus; e sin E &minus; M is increasing (f&prime; = 1 &minus; e cos E &ge; 1 &minus; e &gt; 0), so the bracket always holds the root and a step that leaves it is replaced by a bisection. The naive safeguard &mdash; reject any step not strictly inside the bracket &mdash; stalls, because the converged step lands exactly on the bracket end it has just set: 51 iterations instead of 5 at e = 0.99 (measured in derive.py, and the reason the rule here is Numerical Recipes&rsquo;).</p>'
    + '<div class="cite">pins: E against scipy brentq at 120 (M, e) pairs to 8.9e-16, the residual, the iteration count, the small-M limit E &asymp; M/(1&minus;e), and PhET&rsquo;s 0.01-rad stop (up to 1.6e-5 rad at e = 1/3, 1.3e-4 at e = 0.967) &mdash; derive.py</div>'
};
