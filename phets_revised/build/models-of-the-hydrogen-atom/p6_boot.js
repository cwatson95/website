
/* ================================================================== *
 *  boot — panel, tabs, handlers, frame loop                          *
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
    st.view = k;
    [].forEach.call(tabsEl.children, (b, i) => b.className = TABS[i][0] === st.view ? 'active' : '');
    syncChips(); syncPanel(); dirty = true; refresh();
  }
  TABS.forEach(([k, lab2]) => {
    tabsEl.appendChild(h('button', {class: st.view === k ? 'active' : '', onclick: () => setView(k)}, lab2));
  });

  const rows = {};
  function slider(key, lab2, lo, hi, step2, fmtf, onchg){
    const inp = h('input', {type: 'range', min: lo, max: hi, step: step2, value: st[key]});
    const val = h('span', {class: 'val'});
    const rowEl = h('div', {class: 'sliderrow'}, h('label', null, lab2), inp, val);
    const sync = () => { inp.value = st[key]; val.textContent = fmtf(st[key]); };
    inp.addEventListener('input', () => {
      st[key] = parseFloat(inp.value);
      val.textContent = fmtf(st[key]);
      if(onchg) onchg();
      syncPanel(); dirty = true; refresh();
    });
    rows[key] = {row: rowEl, sync, inp}; sync(); return rowEl;
  }
  function checkbox(key, lab2, onchg){
    const inp = h('input', {type: 'checkbox'}); inp.checked = st[key];
    const el = h('label', null, inp, lab2);
    inp.addEventListener('change', () => {
      st[key] = inp.checked;
      if(onchg) onchg();
      syncPanel(); dirty = true; refresh();
    });
    rows['cb_' + key] = {row: el, sync: () => { inp.checked = st[key]; }};
    return el;
  }
  function chipRow(list, key, onPick){
    const wrapEl = h('div', {class: 'chips'});
    list.forEach(o => {
      const c = h('button', {class: 'chip' + (st[key] === o.id ? ' on' : ''), html: o.name, onclick: () => {
        const was = st[key]; st[key] = o.id; if(onPick) onPick(o, was);
        [].forEach.call(wrapEl.children, (b, i) => b.className = 'chip' + (list[i].id === st[key] ? ' on' : ''));
        syncPanel(); dirty = true; refresh();
      }});
      wrapEl.appendChild(c);
    });
    return wrapEl;
  }
  const CHIPROWS = [];
  function trackChips(g, list, key){ CHIPROWS.push([g, list, key]); }
  function btn(label2, fn){ return h('button', {onclick: () => { fn(); syncPanel(); dirty = true; refresh(); }}, label2); }

  /* ---- the model ---- */
  const gModel = h('div', {class: 'grp'}, h('h3', null, 'the model'));
  const modelChips = chipRow(MODEL_LIST, 'model', (o, was) => { if(o.id !== was) atomReset(st); });
  gModel.appendChild(modelChips); trackChips(gModel, MODEL_LIST, 'model');
  const modelTag = h('div', {class: 'tag'}); gModel.appendChild(modelTag);

  /* ---- the light ---- */
  const gLight = h('div', {class: 'grp'}, h('h3', null, 'the light source'));
  const lampChecks = h('div', {class: 'checks'}, checkbox('lightOn', 'the lamp is on'));
  gLight.appendChild(lampChecks);
  const lightChips = chipRow(LIGHT_LIST, 'light'); gLight.appendChild(lightChips);
  trackChips(gLight, LIGHT_LIST, 'light');
  gLight.appendChild(slider('lam', 'wavelength, nm', PHET.lamMin, PHET.lamMax, 1,
    v => fmt(v, 0) + ' nm'));
  const lineBtns = h('div', {class: 'btnrow'},
    btn('Lyman α 122', () => { st.light = 'mono'; st.lam = phetLam(1, 2); }),
    btn('Hα 656', () => { st.light = 'mono'; st.lam = phetLam(2, 3); }),
    btn('off a line 300', () => { st.light = 'mono'; st.lam = 300; }));
  gLight.appendChild(lineBtns);
  const lightTag = h('div', {class: 'tag'}); gLight.appendChild(lightTag);

  /* ---- time ---- */
  const gTime = h('div', {class: 'grp'}, h('h3', null, 'time'));
  gTime.appendChild(h('div', {class: 'checks'}, checkbox('running', 'time runs')));
  const speedChips = chipRow(SPEED_LIST, 'speed'); gTime.appendChild(speedChips);
  trackChips(gTime, SPEED_LIST, 'speed');
  gTime.appendChild(h('div', {class: 'btnrow'},
    btn('step', () => { atomStepOnce(st); }),
    btn('restart atom', () => { atomReset(st); }),
    btn('reset all', () => { const v = st.view; Object.assign(st, DEFAULTS); st.view = v; atomReset(st); syncChips(); })));
  gTime.appendChild(slider('seed', 'random seed', 1, 999999, 1, v => fmt(v, 0), () => atomReset(st)));
  const timeTag = h('div', {class: 'tag'}); gTime.appendChild(timeTag);

  /* ---- what is drawn ---- */
  const gShow = h('div', {class: 'grp'}, h('h3', null, 'what is drawn'));
  gShow.appendChild(h('div', {class: 'checks'},
    checkbox('showExact', 'the true n² radii / true ladder'),
    checkbox('showSpectro', 'the spectrometer'),
    checkbox('showPhet', 'mark the nodes'),
    checkbox('logCount', 'log counts')));
  const dbChips = chipRow(DB_LIST, 'dbRep'); gShow.appendChild(dbChips);
  trackChips(gShow, DB_LIST, 'dbRep');
  gShow.appendChild(slider('nu', 'wavelengths round the ring', 0.5, 7.2, 0.05, v => fmt(v, 2)));
  const showTag = h('div', {class: 'tag'}); gShow.appendChild(showTag);

  /* ---- the quantum numbers ---- */
  const gQ = h('div', {class: 'grp'}, h('h3', null, 'the quantum numbers'));
  /* l <= n-1 and |m| <= l are clamped in ONE place, syncPanel, which runs
     after every control change.  Clamping here as well made either copy's
     mutant equivalent and the sweep reported it as a survivor (Known-bad). */
  gQ.appendChild(slider('n', 'n', 1, NMAX, 1, v => fmt(v, 0)));
  gQ.appendChild(slider('l', 'l', 0, NMAX - 1, 1, v => fmt(v, 0)));
  gQ.appendChild(slider('m', 'm', -(NMAX - 1), NMAX - 1, 1, v => fmt(v, 0)));
  const qTag = h('div', {class: 'tag'}); gQ.appendChild(qTag);

  /* ---- the spectrum ---- */
  const gSer = h('div', {class: 'grp'}, h('h3', null, 'the spectrum'));
  const serChips = chipRow(SERIES_LIST, 'series'); gSer.appendChild(serChips);
  trackChips(gSer, SERIES_LIST, 'series');
  const serTag = h('div', {class: 'tag'}); gSer.appendChild(serTag);

  /* ---- the ensemble ---- */
  const gEns = h('div', {class: 'grp'}, h('h3', null, 'the ensemble'));
  gEns.appendChild(slider('fromN', 'start from n', 2, NMAX, 1, v => fmt(v, 0)));
  gEns.appendChild(slider('trials', 'cascades', 200, 20000, 200, v => fmt(v, 0)));
  const ensTag = h('div', {class: 'tag'}); gEns.appendChild(ensTag);

  const gInfo = h('div', {class: 'grp'}, h('h3', null, 'what you are looking at'),
    h('div', {id: 'info'}),
    h('div', {class: 'src', html: 'Remake of PhET Interactive Simulations&rsquo; Models of the Hydrogen Atom '
      + '(University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      + 'PhET&rsquo;s values (both screens, the six models, the 475-unit box, the 300 units/s photon, the orbit '
      + 'radii 15/44/81/124/174/233, the level heights, the 1240/13.6 integer wavelengths, the transition-strength '
      + 'table, the 0.75 s and 1.0 s waits, the 0.5 and 0.1 emission chances, the 150 nm plum-pudding line, the '
      + 'classical spiral, the 0.4 white-light bias, the metastable (2,0,0) handler) are read from its build 1.0.9. '
      + 'Everything about hydrogen itself is exact and pinned in selfTest to build/models-of-the-hydrogen-atom/'
      + 'derive.py (scipy.constants CODATA 2022, scipy.special genlaguerre and sph_harm_y, scipy quad, and the '
      + 'mulberry32 stream reproduced bit for bit). Measured lines: NIST, <i>Handbook of Basic Atomic Spectroscopic '
      + 'Data</i>, Strong Lines of Hydrogen (H I); vacuum&ndash;air conversion Edl&eacute;n 1966, Metrologia 2, 71.'}));
  const gPhys = h('div', {class: 'grp'}, h('h3', null, 'the physics'), h('div', {id: 'phys'}));
  [gModel, gLight, gTime, gShow, gQ, gSer, gEns, gInfo, gPhys].forEach(g => panel.appendChild(g));
  const infoEl = gInfo.querySelector('#info'), physEl = gPhys.querySelector('#phys');

  function syncChips(){
    for(const [g, list, key] of CHIPROWS){
      const cws = g.querySelectorAll('.chips');
      for(const cw of cws){
        if(cw.children.length !== list.length) continue;
        let match = 0;
        for(let i = 0; i < list.length; i++) if(cw.children[i].textContent === plain(list[i].name)) match++;
        if(match === list.length)
          [].forEach.call(cw.children, (b, i) => b.className = 'chip' + (list[i].id === st[key] ? ' on' : ''));
      }
    }
  }
  /* a control the view ignores is HIDDEN, never left live and inert */
  function syncPanel(){
    const v = st.view;
    const live = (v === 'box' || v === 'levels');
    gModel.hidden = !(live || v === 'rates');
    gLight.hidden = !(live || v === 'series');
    rows.lam.row.hidden = !(v === 'series' || (live && st.light === 'mono'));
    lineBtns.hidden = !(v === 'series' || live);
    lampChecks.hidden = !live;
    lightChips.hidden = !live;
    gTime.hidden = !(live || v === 'wave');
    rows.seed.row.hidden = !(live || v === 'rates');
    gShow.hidden = !(live || v === 'wave' || v === 'orbitals');
    dbChips.hidden = !(v === 'wave' || (live && st.model === 'debroglie'));
    rows.nu.row.hidden = (v !== 'wave');
    rows.cb_showSpectro.row.hidden = (v !== 'box');
    rows.cb_logCount.row.hidden = (v !== 'box');
    rows.cb_showPhet.row.hidden = (v !== 'orbitals');
    gQ.hidden = (v !== 'orbitals');
    gSer.hidden = (v !== 'series');
    gEns.hidden = (v !== 'rates');
    /* l and m are bounded by n: clamp, then show the legal range */
    st.l = Math.min(st.l, st.n - 1);
    st.m = clamp(st.m, -st.l, st.l);
    if(rows.l.inp){ rows.l.inp.max = st.n - 1; }
    if(rows.m.inp){ rows.m.inp.min = -st.l; rows.m.inp.max = st.l; }
    for(const k in rows) rows[k].sync();
    const yr = MODEL_LIST.filter(o => o.id === st.model)[0].year;
    modelTag.innerHTML = MODEL_CLAIM[st.model] + (yr ? ' &nbsp;(' + yr + ')' : '')
      + '<br>switching the model restarts the run, as PhET&rsquo;s does';
    lightTag.innerHTML = 'PhET opens with the lamp <b>off</b> at 380 nm, which is not a transition of hydrogen; '
      + 'this file opens on at 122 nm so something happens. White light is 40 % aimed at the n = 1 lines '
      + '(PhET&rsquo;s bias) and uniform on 92&ndash;780 nm otherwise.';
    timeTag.innerHTML = 'space runs/pauses &nbsp; <b>.</b> steps &nbsp; <b>r</b> restarts &nbsp; 1&ndash;6 switch views'
      + '<br>one tick is 1/60 s of PhET&rsquo;s model; the seed makes the run reproducible';
    showTag.innerHTML = v === 'wave'
      ? 'slide &nu; off a whole number and the wave stops meeting itself'
      : (st.model === 'debroglie' ? 'PhET&rsquo;s three de Broglie pictures of the same standing wave'
        : 'green rings are where n&sup2;a<sub>0</sub> would put the orbits');
    qTag.innerHTML = 'l runs 0 to n&minus;1 and m runs &minus;l to +l, so the sliders clamp each other; '
      + 'the orbital is ' + st.n + '&thinsp;' + 'spdfgh'.charAt(Math.min(st.l, st.n - 1)) + '.';
    serTag.innerHTML = 'drag on the top panel to move the wavelength marker';
    ensTag.innerHTML = 'every |z| below 3 means the seeded run agrees with the distribution it draws from';
  }

  function refresh(){
    try{
      const M = S.model();
      roEl.innerHTML = readoutHTML(M);
      eqEl.innerHTML = eqbarHTML(M);
      tagEl.innerHTML = tagHTML(M);
      hintEl.textContent = st.view === 'box' ? 'click the box to switch the lamp · space pauses · 1–6 switch views'
        : st.view === 'series' ? 'drag across the spectrum to move the marker · 1–6 switch views'
        : st.view === 'wave' ? 'drag on the mismatch curve to set ν · space pauses · 1–6 switch views'
        : 'space pauses · 1–6 switch views';
      infoEl.innerHTML = INFO[st.view] || '';
      physEl.innerHTML = DERIV[st.view] || '';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown', e => {
    canvas.setPointerCapture(e.pointerId);
    const r = canvas.getBoundingClientRect();
    if(S.pointer('down', e.clientX - r.left, e.clientY - r.top)){ canvas.classList.add('dragging'); dirty = true; syncPanel(); }
  });
  canvas.addEventListener('pointermove', e => {
    if(!canvas.classList.contains('dragging') && e.buttons === 0) return;
    const r = canvas.getBoundingClientRect();
    if(S.pointer('move', e.clientX - r.left, e.clientY - r.top)){ dirty = true; syncPanel(); roEl.innerHTML = readoutHTML(S.model()); }
  });
  const up = () => { canvas.classList.remove('dragging'); if(S.pointer('up', 0, 0)){ dirty = true; refresh(); } };
  canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);

  window.addEventListener('keydown', e => {
    if(e.key === ' '){ e.preventDefault(); st.running = !st.running; syncPanel(); dirty = true; refresh(); }
    else if(e.key === 'r'){ atomReset(st); dirty = true; refresh(); }
    else if(e.key === '.'){ atomStepOnce(st); dirty = true; refresh(); }
    else if(e.key >= '1' && e.key <= String(TABS.length)) setView(TABS[+e.key - 1][0]);
  });

  function resize(){
    const r = canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(r.width * dpr); canvas.height = Math.round(r.height * dpr);
    canvas.getContext('2d').setTransform(dpr, 0, 0, dpr, 0, 0);
    S.W = r.width; S.H = r.height;
  }
  window.addEventListener('resize', () => { resize(); dirty = true; refresh(); });

  let frameN = 0, last = 0;
  function frameLoop(tm){
    frameN++;
    const dtw = last ? Math.min((tm - last) / 1000, 0.05) : 0; last = tm;
    const advanced = S.step(dtw);
    if(advanced || dirty){
      dirty = false;
      try{ S.draw(); if(advanced && frameN % 8 === 0) roEl.innerHTML = readoutHTML(S.model()); }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  atomReset(ST);
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO = {
  box: 'This is PhET&rsquo;s Spectra screen. A lamp below a box of hydrogen fires photons upward, one every '
    + '0.0792 s at 300 units a second, and you choose which picture of the atom sits in the middle. A <b>billiard '
    + 'ball</b> can only scatter light, so nothing ever changes colour. <b>Plum pudding</b> holds a photon, lets its '
    + 'electron oscillate, and gives back one wavelength, 150 nm &mdash; one line, always the same, whatever you '
    + 'shine in. A <b>classical solar system</b> radiates continuously because the electron is accelerating, so the '
    + 'orbit shrinks and the atom is destroyed in two thirds of a second; that is the disaster Bohr was answering. '
    + '<b>Bohr</b>, <b>de Broglie</b> and <b>Schr&ouml;dinger</b> absorb only when the photon&rsquo;s energy is '
    + 'exactly the gap between two levels, and give it back in the same currency. Switch to <b>experiment</b> and '
    + 'the atom is hidden: all you have is the spectrometer, which is all anyone ever had.',
  levels: 'This is PhET&rsquo;s Energy Levels screen, drawn twice. On the left is PhET&rsquo;s own ladder, whose '
    + 'six rungs sit at 0.025, 0.6, 0.73, 0.81, 0.86 and 0.9 of the axis &mdash; spread out so you can see them, not '
    + 'where they belong. On the right is the truth: E<sub>n</sub> = &minus;13.598287 eV / n&sup2;, which puts n = 2 '
    + 'three quarters of the way up and crushes everything from n = 3 into the last tenth. That crowding <i>is</i> '
    + 'the Balmer series converging at 364.7 nm. Watch the electron: every jump up is a photon swallowed and every '
    + 'jump down is one made, and the squiggle between the levels is drawn in the colour of the photon that carried '
    + 'the difference. For Schr&ouml;dinger the rungs split by l, and the selection rule &Delta;l = &plusmn;1 says '
    + 'the electron must step sideways as well as down.',
  wave: 'De Broglie&rsquo;s answer to &ldquo;why those orbits and no others&rdquo;. Give the electron a wavelength '
    + '&lambda; = h/mv and the orbit is allowed exactly when a whole number of them fits round it: n&lambda; = '
    + '2&pi;r. Put the Bohr speed v<sub>n</sub> = &alpha;c/n into that and out comes r<sub>n</sub> = n&sup2;a<sub>0</sub> '
    + '&mdash; the same ladder, from a wave instead of a postulate. Slide &nu; off a whole number and watch the wave '
    + 'fail to meet itself at the seam. The size of that failure has a closed form: matching both the height and the '
    + 'slope at the seam costs 2|sin &pi;&nu;|, which is zero only at the integers. The three pictures are '
    + 'PhET&rsquo;s own &mdash; the same standing wave drawn as a wobble in radius, as a height above the ring, or '
    + 'as brightness round it.',
  orbitals: 'Schr&ouml;dinger replaced the orbit with a cloud. The wavefunction &psi;<sub>nlm</sub> factorises into a '
    + 'radial part R<sub>nl</sub>(r) and an angular part Y<sub>l</sub><sup>m</sup>(&theta;,&phi;), and |&psi;|&sup2; '
    + 'is the probability of finding the electron there. The picture is that squared modulus integrated along the '
    + 'line of sight, which is what you would get if you could photograph one atom over and over. Three numbers set '
    + 'the shape: n fixes the energy and the size, l the number of angular nodes, m how the shape is oriented. The '
    + 'counting is exact &mdash; n &minus; l &minus; 1 spherical shells where the electron is never found, and '
    + 'l &minus; |m| cones. Nothing here is fitted: the polynomials are the analytic ones and the picture is what '
    + 'they say.',
  series: 'Every line hydrogen can make, on one logarithmic axis. They fall into series by where the electron lands: '
    + 'Lyman into n = 1, in the ultraviolet; Balmer into n = 2, four of them in the visible, which is why a hydrogen '
    + 'discharge looks pink; Paschen, Brackett and Pfund into n = 3, 4 and 5, in the infrared. Each series crowds '
    + 'toward its limit, the energy needed to tear the electron away from that level. The colours are real '
    + 'colorimetry, the CIE 1931 observer through the sRGB primaries. Underneath is the check that matters: this '
    + 'model against what NIST measured. It is right to one part in 10<sup>5</sup>, and the miss is not an error '
    + '&mdash; it is the relativistic correction a Schr&ouml;dinger atom does not contain, whose size is '
    + '&alpha;&sup2;/4 for the 1s level.',
  rates: 'A model of the hydrogen atom has to say not only which jumps are possible but how likely they are. Real '
    + 'hydrogen answers with the Einstein A coefficients, which come out of the dipole matrix element between the '
    + 'two wavefunctions &mdash; no free parameters at all. A(2p &rarr; 1s) is 6.27 &times; 10<sup>8</sup> per '
    + 'second, so a 2p atom lives 1.6 ns. A 2s atom lives forever, because &Delta;l = &plusmn;1 leaves it nowhere to '
    + 'go: that is the metastable state PhET has to nudge the atom out of with a spare photon. PhET uses a small '
    + 'table of weights instead, and its first column turns out to be twice the real A for np &rarr; 1s; the rest is '
    + 'its own. The bottom panel is the honesty check on the dice: run the cascade thousands of times with a fixed '
    + 'seed and the measured fractions have to sit on the distribution they were drawn from.',
};

function FR(t, b){ return '<span class="frac"><span class="t">' + t + '</span><span class="b">' + b + '</span></span>'; }
function EQ(n, body){ return '<div class="eq"><span class="n">[' + n + ']</span>' + body + '</div>'; }
const DERIV = {
  box: '<h4>absorption and emission</h4>'
    + EQ(1, 'E<sub>n</sub> = &minus;' + FR('R<sub>H</sub>hc', 'n&sup2;') + ', &nbsp; R<sub>H</sub> = '
      + FR('R<sub>&infin;</sub>', '1 + m<sub>e</sub>/m<sub>p</sub>') + ' = 10 967 758.340 m<sup>&minus;1</sup>')
    + EQ(2, '&lambda;(n<sub>1</sub>&rarr;n<sub>2</sub>) = ' + FR('1', 'R<sub>H</sub>(1/n<sub>1</sub>&sup2; &minus; 1/n<sub>2</sub>&sup2;)'))
    + EQ(3, '<span class="rm">PhET:</span> &lambda; = round(1240 / (13.6(1/n<sub>1</sub>&sup2; &minus; 1/n<sub>2</sub>&sup2;))) <span class="rm">nm</span>')
    + '<p>PhET&rsquo;s constants are round numbers and its wavelengths are integers, so its Lyman-&alpha; is 122 nm '
    + 'against the true 121.568 nm, and every absorption test in the box is an integer comparison. That is why the '
    + 'lamp does nothing at 121 nm and everything at 122.</p>'
    + '<h4>PhET&rsquo;s dynamics</h4>'
    + EQ(4, '<span class="rm">absorb if</span> t<sub>state</sub> &ge; 0.75 s <span class="rm">and</span> &lambda; '
      + '<span class="rm">is a transition of the current</span> n')
    + EQ(5, '<span class="rm">emit with probability</span> 0.5 <span class="rm">per frame once</span> t<sub>state</sub> &ge; 1 s')
    + '<div class="cite">pins: all 15 PhET integers against derive.py; the exact wavelengths to 1e&minus;12; '
    + 'the classical collapse time 0.67 s; the emitted-photon direction cone &mdash; derive.py</div>',
  levels: '<h4>the ladder</h4>'
    + EQ(1, 'E<sub>n</sub> = &minus;13.598287264 eV / n&sup2;, &nbsp; E<sub>&infin;</sub> = 0')
    + EQ(2, '<span class="rm">height on a true axis:</span> ' + FR('E<sub>n</sub> &minus; E<sub>1</sub>', '0 &minus; E<sub>1</sub>')
      + ' = 1 &minus; ' + FR('1', 'n&sup2;'))
    + EQ(3, '<span class="rm">PhET&rsquo;s heights:</span> 0.025, 0.6, 0.73, 0.81, 0.86, 0.9')
    + EQ(4, '<span class="rm">selection rule (Schr&ouml;dinger):</span> &Delta;l = &plusmn;1, &nbsp; |&Delta;m| &le; 1')
    + '<p>The true heights are 0, 0.75, 0.889, 0.938, 0.96, 0.972: five of the six levels live in the top quarter '
    + 'of the axis. PhET spreads them because a diagram you cannot click on is no use; the cost is that the picture '
    + 'no longer says what the spectrum says.</p>'
    + '<div class="cite">pins: both ladders; the reduced-mass R<sub>H</sub>; &Delta;E for every pair &mdash; derive.py</div>',
  wave: '<h4>the closure condition</h4>'
    + EQ(1, '&lambda;<sub>dB</sub> = ' + FR('h', 'm<sub>e</sub>v') + ', &nbsp; v<sub>n</sub> = ' + FR('&alpha;c', 'n'))
    + EQ(2, 'n&lambda;<sub>dB</sub> = 2&pi;r<sub>n</sub> &nbsp;&rArr;&nbsp; r<sub>n</sub> = n&sup2;a<sub>0</sub>, &nbsp; a<sub>0</sub> = '
      + FR('&hbar;', 'm<sub>e</sub>&alpha;c'))
    + EQ(3, '<span class="rm">seam mismatch at &nu; turns:</span> &radic;(sin&sup2;2&pi;&nu; + (1&minus;cos 2&pi;&nu;)&sup2;) = 2|sin &pi;&nu;|')
    + '<p>[2] is an identity, so the residual printed in the readout is not physics &mdash; it is how consistent '
    + 'CODATA&rsquo;s separately rounded a<sub>0</sub>, &alpha; and m<sub>e</sub> are with each other, 5.2 parts in '
    + '10<sup>12</sup>. [3] is worth writing out: the wave has to match in height <i>and</i> slope, and the two '
    + 'mismatches combine into one clean modulus.</p>'
    + '<div class="cite">pins: n&lambda;/2&pi;r &minus; 1 at six n; the closed form against the raw two-term '
    + 'expression at 400 &nu; &mdash; derive.py</div>',
  orbitals: '<h4>the wavefunction</h4>'
    + EQ(1, '&psi;<sub>nlm</sub> = R<sub>nl</sub>(r) Y<sub>l</sub><sup>m</sup>(&theta;,&phi;)')
    + EQ(2, 'R<sub>nl</sub> = &radic;((2/n)&sup3;' + FR('(n&minus;l&minus;1)!', '2n(n+l)!') + ') e<sup>&minus;&rho;/2</sup>&rho;<sup>l</sup>L<sub>n&minus;l&minus;1</sub><sup>2l+1</sup>(&rho;), &nbsp; &rho; = 2r/na<sub>0</sub>')
    + EQ(3, '&int;R&sup2;r&sup2;dr = 1, &nbsp; &lang;r&rang; = ' + FR('3n&sup2; &minus; l(l+1)', '2') + 'a<sub>0</sub>, &nbsp; &lang;1/r&rang; = 1/n&sup2;a<sub>0</sub>')
    + EQ(4, '<span class="rm">nodes:</span> n &minus; l &minus; 1 <span class="rm">radial,</span> l &minus; |m| <span class="rm">angular</span>')
    + EQ(5, '<span class="rm">drawn:</span> &int;|&psi;|&sup2; dy <span class="rm">(Simpson, step &prop; n)</span>')
    + '<p>The radial polynomial is built from exact coefficients rather than evaluated through a recurrence, and the '
    + 'two agree to 4&times;10<sup>&minus;17</sup>. The column integral needs a step that follows n, not the range: '
    + 'a fixed panel count tuned at n = 6 leaves the 1s column 10<sup>&minus;5</sup> low.</p>'
    + '<div class="cite">pins: normalisation, &lang;r&rang;, &lang;r&sup2;&rang;, &lang;1/r&rang;, node counts, 10 spot '
    + 'values of |&psi;|&sup2; and 7 of the column against scipy quad &mdash; derive.py</div>',
  series: '<h4>the spectrum</h4>'
    + EQ(1, FR('1', '&lambda;') + ' = R<sub>H</sub>(' + FR('1', 'n<sub>1</sub>&sup2;') + ' &minus; ' + FR('1', 'n<sub>2</sub>&sup2;') + ')')
    + EQ(2, '<span class="rm">series limit:</span> &lambda;<sub>&infin;</sub> = n<sub>1</sub>&sup2;/R<sub>H</sub> '
      + '&nbsp;&rArr;&nbsp; 91.18, 364.71, 820.59, 1458.8, 2279.4 nm')
    + EQ(3, '<span class="rm">air:</span> (n&minus;1)&times;10<sup>8</sup> = 8342.13 + ' + FR('2406030', '130 &minus; &sigma;&sup2;')
      + ' + ' + FR('15997', '38.9 &minus; &sigma;&sup2;') + ', &nbsp; &sigma; = 1/&lambda;<sub>vac</sub>[&micro;m]')
    + EQ(4, '<span class="rm">what is missing:</span> &Delta;E/E ~ &alpha;&sup2;(1/(j+&frac12;) &minus; 3/4n)/n&sup2;')
    + '<p>Every NIST line is reproduced to better than 3&times;10<sup>&minus;5</sup>; the eight Lyman lines miss by '
    + '1.10&ndash;1.33&times;10<sup>&minus;5</sup>, and &alpha;&sup2;/4 = 1.331&times;10<sup>&minus;5</sup> is the '
    + 'relativistic shift of the 1s level that every Lyman line carries. The residual is the physics that is not '
    + 'here, measured.</p>'
    + '<div class="cite">source: NIST, <i>Handbook of Basic Atomic Spectroscopic Data</i>, Strong Lines of Hydrogen '
    + '(H I), all 8 vacuum and 22 air rows; Edl&eacute;n 1966 &mdash; derive.py</div>',
  rates: '<h4>spontaneous emission</h4>'
    + EQ(1, 'A<sub>ul</sub> = ' + FR('4', '3') + '&alpha;&sup3;&omega;&sup3; ' + FR('l<sub>max</sub>', '2l<sub>u</sub>+1')
      + ' |&lang;n<sub>u</sub>l<sub>u</sub>|r|n<sub>l</sub>l<sub>l</sub>&rang;|&sup2; &nbsp; <span class="rm">(atomic units)</span>')
    + EQ(2, '&lang;u|r|l&rang; = &int;<sub>0</sub><sup>&infin;</sup> R<sub>u</sub>(r) r R<sub>l</sub>(r) r&sup2;dr = '
      + '&Sigma;<sub>k</sub> c<sub>k</sub> ' + FR('k!', 's<sup>k+1</sup>') + ', &nbsp; s = 1/n<sub>u</sub> + 1/n<sub>l</sub>')
    + EQ(3, '&tau;<sub>nl</sub> = 1/&Sigma;A, &nbsp; &tau;(2p) = 1.5953 ns, &nbsp; &tau;(2s) = &infin;')
    + EQ(4, '<span class="rm">PhET&rsquo;s weights:</span> 12.53 | 3.34, 0.87 | 1.36, 0.24, 0.07 | 0.69, 0.11, 0, 0.04 | 0.39, 0.06, 0.02, 0, 0')
    + '<p>[2] is exact: both radial functions are a polynomial times e<sup>&minus;r/n</sup>, so the integrand is a '
    + 'polynomial times e<sup>&minus;sr</sup> and every term integrates in closed form. It agrees with scipy quad to '
    + '2&times;10<sup>&minus;13</sup>. PhET&rsquo;s first column is 2A(np&rarr;1s)/10<sup>8</sup> to within 1.2 %; '
    + 'the other columns match nothing of the kind, and are PhET&rsquo;s own.</p>'
    + '<div class="cite">pins: 15 radial integrals and their A, 13 lifetimes, the l-averaged branching, and the '
    + 'seeded ensembles bit for bit &mdash; derive.py</div>',
};
