
/* ================================================================== *
 *  boot -- panel, tabs, handlers, frame loop                          *
 * ================================================================== */
function boot() {
  const canvas = document.getElementById('scene');
  const panel = document.getElementById('panel');
  const tabsEl = document.getElementById('tabs');
  const roEl = document.getElementById('readout');
  const eqEl = document.getElementById('eqbar');
  const tagEl = document.getElementById('tag');
  const hintEl = document.getElementById('hint');
  const errEl = document.getElementById('errbox');
  const S = makeScene(canvas), st = S.st;
  let dirty = false;      /* only the pointer and the wheel set it; everything else calls refresh() */

  function fail(e) { errEl.style.display = 'block'; errEl.textContent = String(e && e.stack || e); }
  window.addEventListener('error', ev => fail(ev.error || ev.message));

  function setView(k) {
    st.view = k;
    [].forEach.call(tabsEl.children, (bt, i) => { bt.className = TABS[i][0] === st.view ? 'active' : ''; });
    syncChips(); syncPanel(); refresh();
  }
  S.onView = setView;
  TABS.forEach(([k, lab2]) => {
    tabsEl.appendChild(h('button', {class: st.view === k ? 'active' : '', onclick: () => setView(k)}, lab2));
  });

  const rows = {};
  function slider(key, lab2, lo, hi, step2, fmtf, onchg) {
    const inp = h('input', {type: 'range', min: lo, max: hi, step: step2, value: st[key]});
    const val = h('span', {class: 'val'});
    const rowEl = h('div', {class: 'sliderrow'}, h('label', null, lab2), inp, val);
    const sync = () => { inp.value = st[key]; val.textContent = fmtf(st[key]); };
    inp.addEventListener('input', () => {
      st[key] = parseFloat(inp.value);
      if (onchg) onchg();
      val.textContent = fmtf(st[key]);
      syncPanel(); refresh();
    });
    rows[key] = {row: rowEl, sync};
    sync();
    return rowEl;
  }
  function checkbox(key, lab2, onchg) {
    const inp = h('input', {type: 'checkbox'});
    inp.checked = st[key];
    const el = h('label', null, inp, lab2);
    inp.addEventListener('change', () => {
      st[key] = inp.checked;
      if (onchg) onchg();
      syncPanel(); refresh();
    });
    rows['cb_' + key] = {row: el, sync: () => { inp.checked = st[key]; }};
    return el;
  }
  const CHIPROWS = [];
  function chipRow(list, key, onPick) {
    const wrapEl = h('div', {class: 'chips'});
    list.forEach(o => {
      const c = h('button', {
        class: 'chip' + (st[key] === o.id ? ' on' : ''),
        onclick: () => {
          const was = st[key];
          st[key] = o.id;
          if (onPick) onPick(o, was);
          [].forEach.call(wrapEl.children, (bt, i) => { bt.className = 'chip' + (list[i].id === st[key] ? ' on' : ''); });
          syncPanel(); refresh();
        }}, o.name);
      wrapEl.appendChild(c);
    });
    CHIPROWS.push([wrapEl, list, key]);
    return wrapEl;
  }
  const BTN = {};
  function btn(label, fn) {
    const bt = h('button', {onclick: () => { fn(); syncChips(); syncPanel(); refresh(); }}, label);
    BTN[label] = bt;
    return bt;
  }

  /* --- the light source: PhET's four radio buttons --- */
  const gSrc = h('div', {class: 'grp'}, h('h3', null, 'the light source'));
  gSrc.appendChild(chipRow(BANDS.map(b => ({id: b, name: BANDNAME[b]})), 'band', () => chamberRebuild()));
  gSrc.appendChild(h('div', {class: 'checks'}, checkbox('source', 'source on', () => chamberSync())));
  gSrc.appendChild(h('div', {class: 'btnrow'},
    btn('fire one photon', () => { chamberSync(); chamberFire(CH, 0); }),
    btn('reset molecule', () => chamberRebuild())));
  const srcTag = h('div', {class: 'tag'});
  gSrc.appendChild(srcTag);

  /* --- the molecule: PhET's eight --- */
  const gMol = h('div', {class: 'grp'}, h('h3', null, 'the molecule'));
  gMol.appendChild(chipRow(MOLORDER.map(m => ({id: m, name: m})), 'mol', () => {
    ST.modeIdx = 0; chamberRebuild();
  }));
  const molTag = h('div', {class: 'tag'});
  gMol.appendChild(molTag);

  /* --- time: PhET's play/pause, step and slow motion --- */
  const gTime = h('div', {class: 'grp'}, h('h3', null, 'time'));
  gTime.appendChild(h('div', {class: 'checks'},
    checkbox('running', 'running'),
    checkbox('slow', 'slow motion'),
    checkbox('showRadius', 'show the absorption radius')));
  gTime.appendChild(h('div', {class: 'btnrow'}, btn('step one frame', () => chamberManualStep())));
  const timeTag = h('div', {class: 'tag'});
  gTime.appendChild(timeTag);

  /* --- whose animation --- */
  const gAnim = h('div', {class: 'grp'}, h('h3', null, 'the vibration drawn'));
  gAnim.appendChild(chipRow([{id: 'mode', name: 'the normal mode'}, {id: 'phet', name: 'PhET’s animation'}], 'anim'));
  const animTag = h('div', {class: 'tag'});
  gAnim.appendChild(animTag);

  /* --- which mode (prev/next, because the count changes with the molecule) --- */
  const gMode = h('div', {class: 'grp'}, h('h3', null, 'the mode'));
  gMode.appendChild(h('div', {class: 'btnrow'},
    btn('previous mode', () => { const n = modeTable(ST.mol).length; ST.modeIdx = (ST.modeIdx + n - 1) % n; }),
    btn('next mode', () => { const n = modeTable(ST.mol).length; ST.modeIdx = (ST.modeIdx + 1) % n; })));
  const modeTag = h('div', {class: 'tag'});
  gMode.appendChild(modeTag);

  /* --- the ensemble --- */
  const gEns = h('div', {class: 'grp'}, h('h3', null, 'the ensemble'));
  gEns.appendChild(slider('nStat', 'photons drawn', 500, 40000, 500, v => fmt(v, 0)));
  gEns.appendChild(slider('statSeed', 'seed', 1, 200000, 1, v => fmt(v, 0)));
  const ensTag = h('div', {class: 'tag'});
  gEns.appendChild(ensTag);

  /* --- the atmosphere --- */
  const gAir = h('div', {class: 'grp'}, h('h3', null, 'the atmosphere'));
  gAir.appendChild(slider('tempK', 'surface T', 220, 330, 1, v => fmt(v, 0) + ' K'));
  gAir.appendChild(h('div', {class: 'checks'}, checkbox('showWindow', 'shade the 8–13 µm window')));
  const airTag = h('div', {class: 'tag'});
  gAir.appendChild(airTag);

  const gReset = h('div', {class: 'grp'}, h('h3', null, 'reset'));
  gReset.appendChild(h('div', {class: 'btnrow'},
    btn('reset view', () => S.resetCam()),
    btn('reset all', () => {
      const v = st.view;
      Object.assign(st, DEFAULTS);
      st.view = v;
      /* DEFAULTS carries camTheta, camPhi and zoom, so the Object.assign
         above has already reset the camera -- calling resetCam() here as well
         would give that state two owners and make a mutant on either one
         equivalent (Known-bad, buoyancy's two guards on one path) */
      chamberRebuild(); MODEPHASE = 0;
    })));

  const gInfo = h('div', {class: 'grp'}, h('h3', null, 'what you are looking at'),
    h('div', {id: 'info'}),
    h('div', {class: 'src', html: 'Remake of PhET Interactive Simulations&rsquo; Molecules and Light (University of '
      + 'Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values, read '
      + 'from its build 1.5.33: the four source wavelengths (0.2 m, 850 nm, 580 nm, 100 nm), the 50&thinsp;% absorption '
      + 'probability, the 1.1&ndash;1.3 s hold and the 0.2 s refusal window after an emission, the 100-unit absorption '
      + 'radius, photons at 3000 units/s from x = &minus;1350, the 0.8 s emission period, 5 Hz vibration, 1.1 Hz '
      + 'rotation, the break-apart speeds 990 and 0.67&thinsp;&times;&thinsp;3000, the whole molecule/band response '
      + 'table, every drawing offset and vibration amplitude, the atom radii and masses, and the seven band edges of '
      + 'its Light Spectrum Diagram. Measured spectroscopy: NIST CCCBDB (cccbdb.nist.gov) &mdash; experimental '
      + 'vibrational frequencies, experimental geometries and experimental dipole moments, retrieved 2026-09-22 to the '
      + 'precision it prints; diatomic constants from the NIST Chemistry WebBook (Huber &amp; Herzberg 1979); isotopic '
      + 'masses from NIST&rsquo;s Atomic Weights and Isotopic Compositions. Bond dissociation energies are QUOTED '
      + '(Active Thermochemical Tables) and were not re-derived here. Composition: NASA Earth Fact Sheet, with '
      + 'NOAA GML&rsquo;s June 2026 global mean CO&#8322; of 427.62 ppm, which that page calls preliminary. Every model '
      + 'number is pinned in selfTest to build/molecules-and-light/derive.py, the Python twin.'}));
  const gPhys = h('div', {class: 'grp'}, h('h3', null, 'the physics'), h('div', {id: 'phys'}));
  [gSrc, gMol, gTime, gAnim, gMode, gEns, gAir, gReset, gInfo, gPhys].forEach(g => panel.appendChild(g));
  const infoEl = gInfo.querySelector('#info'), physEl = gPhys.querySelector('#phys');

  function syncChips() {
    for (const [cw, list, key] of CHIPROWS)
      [].forEach.call(cw.children, (bt, i) => { bt.className = 'chip' + (list[i].id === st[key] ? ' on' : ''); });
  }
  function syncPanel() {
    const v = st.view;
    gSrc.hidden = !(v === 'chamber' || v === 'spectrum' || v === 'table');
    gMol.hidden = (v === 'stats');
    gTime.hidden = !(v === 'chamber' || v === 'modes');
    rows.cb_showRadius.row.hidden = (v !== 'chamber');
    gAnim.hidden = (v !== 'chamber');
    gMode.hidden = (v !== 'modes');
    gEns.hidden = (v !== 'stats');
    gAir.hidden = (v !== 'air');
    for (const k in rows) rows[k].sync();
    const p = PHOTON[st.band];
    srcTag.innerHTML = 'PhET&rsquo;s four are fixed wavelengths, not bands: <b>' + sigf(p.lam * 1e9, 4)
      + ' nm</b> here, which is <b>' + sigf(p.E_eV, 4) + ' eV</b> and <b>' + sigf(p.nubar, 4)
      + ' cm&#8315;&#185;</b>. Its own diagram puts that in <b>' + (bandOf(p.lam) || 'no band at all') + '</b>.';
    const R = realAnswer(st.mol, st.band);
    molTag.innerHTML = '<b>' + st.mol + '</b>, ' + MOLSHAPE[st.mol] + ', dipole moment <b>' + fmt(DIPOLE[st.mol], 3)
      + ' D</b> &mdash; so it ' + (R.rot ? 'does' : 'does not') + ' have a pure rotational spectrum, and <b>'
      + R.nActive + '</b> of its ' + modeTable(st.mol).length + ' vibrations change the dipole.';
    timeTag.innerHTML = 'PhET discards any frame longer than ' + PHET.DT_CEILING + ' s whole, and slow motion halves '
      + 'the step. The emission period is ' + PHET.EMIT_PERIOD + ' s and a photon takes ' + fmt(1350 / 3000, 2)
      + ' s to cross to the molecule.';
    animTag.innerHTML = st.anim === 'phet'
      ? 'PhET&rsquo;s molecules move on hand-picked offsets. Its CO&#8322; bend draws the carbon at <b>'
        + fmt(40 / CO2_SB, 2) + '&times;</b> the oxygens&rsquo; displacement, because its oxygen mass is '
        + PHET_ATOM.O.m + ' &mdash; carbon&rsquo;s. The true ratio is <b>' + fmt(2 * MASS.O / MASS.C, 3) + '</b>.'
      : 'The lowest infrared-active normal mode of this molecule, at its true displacement ratios.';
    const m = currentMode();
    modeTag.innerHTML = 'mode <b>' + (st.modeIdx + 1) + '</b> of ' + modeTable(st.mol).length + ': <b>'
      + fmt(m.nu, 0) + ' cm&#8315;&#185;</b>, ' + m.sym + ', ' + (m.active ? 'infrared-<b>active</b>'
      : 'infrared-<b>inactive</b> &mdash; &part;&mu;/&part;Q is exactly zero');
    ensTag.innerHTML = 'The 4&sigma; band at this sample size is &plusmn;<b>'
      + sigf(4 * Math.sqrt(0.25 / st.nStat), 3) + '</b>. An honest run fails it about 6 times in 100&thinsp;000.';
    airTag.innerHTML = 'The peak of B<sub>&nu;&#771;</sub> at ' + fmt(st.tempK, 0) + ' K is <b>'
      + fmt(planckPeakCm(st.tempK), 0) + ' cm&#8315;&#185;</b> = ' + fmt(1e4 / planckPeakCm(st.tempK), 1)
      + ' &micro;m, from the root of 3(1 &minus; e<sup>&minus;x</sup>) = x.';
  }

  function refresh() {
    try {
      const M = S.model();
      roEl.innerHTML = readoutHTML(M);
      eqEl.innerHTML = eqbarHTML(M);
      tagEl.innerHTML = tagHTML(M);
      const v = st.view;
      hintEl.textContent = v === 'modes' ? 'drag to orbit · wheel to zoom · 1–6 switch views'
        : v === 'chamber' ? 'space pauses · f fires one photon · 1–6 switch views'
        : '1–6 switch views';
      infoEl.innerHTML = INFO[v] || '';
      physEl.innerHTML = DERIV[v] || '';
      S.draw();
    } catch (e) { fail(e); }
  }

  canvas.addEventListener('pointerdown', e => {
    canvas.setPointerCapture(e.pointerId);
    const r = canvas.getBoundingClientRect();
    if (S.pointer('down', e.clientX - r.left, e.clientY - r.top)) { canvas.classList.add('dragging'); dirty = true; }
  });
  canvas.addEventListener('pointermove', e => {
    if (!canvas.classList.contains('dragging') && e.buttons === 0) return;
    const r = canvas.getBoundingClientRect();
    if (S.pointer('move', e.clientX - r.left, e.clientY - r.top)) dirty = true;
  });
  const up = () => { canvas.classList.remove('dragging'); if (S.pointer('up', 0, 0)) refresh(); };
  canvas.addEventListener('pointerup', up);
  canvas.addEventListener('pointercancel', up);
  canvas.addEventListener('wheel', e => { e.preventDefault(); if (S.wheel(e.deltaY)) dirty = true; }, {passive: false});

  window.addEventListener('keydown', e => {
    if (e.key === ' ') { e.preventDefault(); st.running = !st.running; syncPanel(); refresh(); }
    else if (e.key === 'f') { chamberSync(); chamberFire(CH, 0); refresh(); }
    else if (e.key === 'r') { S.resetCam(); refresh(); }
    else if (e.key >= '1' && e.key <= String(TABS.length)) setView(TABS[+e.key - 1][0]);
  });

  function resize() {
    const r = canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(r.width * dpr);
    canvas.height = Math.round(r.height * dpr);
    canvas.getContext('2d').setTransform(dpr, 0, 0, dpr, 0, 0);
    S.W = r.width; S.H = r.height;
  }
  window.addEventListener('resize', () => { resize(); refresh(); });

  let frameN = 0, last = 0, wasBusy = false;
  function frameLoop(tm) {
    frameN++;
    const dtw = last ? Math.min((tm - last) / 1000, 0.05) : 0;
    last = tm;
    const advanced = S.step(dtw);
    if (advanced || dirty) {
      dirty = false;
      try { S.draw(); if (advanced && frameN % 8 === 0) roEl.innerHTML = readoutHTML(S.model()); } catch (e) { fail(e); }
    }
    if (wasBusy && !advanced) { try { roEl.innerHTML = readoutHTML(S.model()); } catch (e) { fail(e); } }
    wasBusy = advanced;
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO = {
  chamber: 'PhET&rsquo;s one screen. A light source on the left, tuned to one of four fixed wavelengths, fires photons '
    + 'at a molecule in the middle, and one of five things happens: nothing, or the molecule rotates, vibrates, glows, '
    + 'or comes apart. The rules are PhET&rsquo;s own, exactly. A photon that comes within a hundred model units of the '
    + 'molecule gets one trial, and one only &mdash; a failed trial marks it to pass through for good &mdash; and that '
    + 'trial is a fair coin. If it wins, the molecule holds the photon for somewhere between 1.1 and 1.3 seconds and '
    + 'then throws it back out in a completely random direction, after which it refuses everything for a fifth of a '
    + 'second. Watch the strip under the chamber: with the source running the molecule spends about half its time '
    + 'excited, and roughly a third of the photons fired are absorbed rather than a half, because every photon that '
    + 'arrives while the molecule is busy is turned away without a trial at all.',
  spectrum: 'PhET&rsquo;s Light Spectrum Diagram, with the band edges its own accessibility text states, and its four '
    + 'source wavelengths marked on it. Two things are worth noticing before anything else. Its microwave photon is at '
    + '0.2 m, and its own diagram has radio ending at 0.5 m and microwave starting at 0.1 m &mdash; so the photon falls '
    + 'in a gap in the picture beside it. And its infrared photon is at 850 nm, which is at the very blue end of a band '
    + 'that runs to a millimetre. The zooms underneath show why that matters: the vibrations a molecule really has live '
    + 'between 2.6 and 15 micrometres, ten to twenty times further into the infrared, and the rotations are at '
    + 'millimetres. None of this is a mistake on PhET&rsquo;s part &mdash; four photons have to be visibly different '
    + 'colours on a screen, and a 15 micrometre photon and a 2.6 millimetre one are both black &mdash; but it is worth '
    + 'knowing that the photon you are firing is a token for its band rather than a member of it.',
  table: 'The whole simulation, in sixty-four cells. On the left is PhET&rsquo;s table, read straight out of the calls '
    + 'that register an absorption strategy; on the right is what a photon of that wavelength would really do. Two '
    + 'selection rules decide the right-hand table and both are exact. A molecule shows a pure rotational spectrum only '
    + 'if it has a permanent dipole moment for the field to grab, and a vibration absorbs infrared only if the dipole '
    + 'moment changes as the atoms move. PhET gets both columns structurally right, which is the remarkable thing: its '
    + 'microwave column is exactly the four molecules with a dipole, and its infrared column is exactly the six with an '
    + 'infrared-active mode. Where the two tables part company is the ultraviolet, where a 12.4 eV photon really does '
    + 'break every one of these molecules, including the two PhET draws as inert, and the visible, where ozone really '
    + 'does absorb &mdash; something PhET&rsquo;s own model notes say out loud.',
  modes: 'A molecule of N atoms has 3N &minus; 6 vibrations (3N &minus; 5 if it is straight), and they are the '
    + 'eigenvectors of the mass-weighted second derivative of its energy. That is what is diagonalised here, from a '
    + 'valence force field fitted to the measured wavenumbers, so the frequencies are the measured ones by construction '
    + 'and the shapes are what the calculation says. Some of those shapes need no calculation at all. In carbon dioxide '
    + 'the symmetric stretch has the carbon exactly at rest &mdash; it cannot move, because the mode is symmetric under '
    + 'the inversion that swaps the two oxygens &mdash; and the other two modes move the carbon in exactly the opposite '
    + 'direction to the oxygens, in the ratio 2m<sub>O</sub>/m<sub>C</sub> = 2.666, which is momentum and nothing else. '
    + 'The arrows are the eigenvector itself. Grey arrows mean the mode changes no dipole: carbon dioxide&rsquo;s '
    + 'symmetric stretch, methane&rsquo;s breathing mode and its two bending deformations, and both fundamentals of '
    + 'nitrogen and oxygen. Those are not weak. They are zero.',
  stats: 'Everything stochastic in PhET&rsquo;s model is here, measured rather than asserted. Three rules: the '
    + 'absorption is a fair coin, the hold time is uniform on 1.1 to 1.3 seconds, and the re-emission direction is '
    + 'uniform on the circle. Each is drawn from a seeded generator so the run reproduces exactly, and each is compared '
    + 'against the standard error a sample of that size is entitled to &mdash; a binomial one for the coin, '
    + '(b &minus; a)/&radic;12 for the uniform, and 1/&radic;2N for the direction &mdash; rather than against a '
    + 'tolerance chosen to make the test pass. The orange trace is the same experiment run on a generator biased to '
    + '0.52 instead of 0.5. It looks perfectly reasonable for the first few hundred photons and is comfortably rejected '
    + 'by twenty thousand, which is the only honest way to say that a statistical test has any teeth.',
  air: 'Why any of this matters. The Earth&rsquo;s surface is at about 288 K, so it radiates a Planck spectrum whose '
    + 'peak &mdash; in wavenumber, which is how infrared spectroscopists count &mdash; is at 565 per centimetre, about '
    + '18 micrometres. Every vertical line is a measured infrared-active fundamental of a gas the air actually carries. '
    + 'Carbon dioxide&rsquo;s bend is at 667, essentially on the peak. The composition bar underneath is the payoff: '
    + '99.97 per cent of dry air is nitrogen, oxygen and argon, and not one of them can absorb an infrared photon at '
    + 'all &mdash; the diatomics because a stretch of a homonuclear bond changes no dipole, argon because a single atom '
    + 'has nothing to stretch. The four hundredths of one per cent that is carbon dioxide and methane does all of it. '
    + 'The shaded band is the 8 to 13 micrometre window, about a third of the emission, and it is a window for exactly '
    + 'one reason: no strong fundamental of the major gases lands in it.',
};
function FR(t, b) { return '<span class="frac"><span class="t">' + t + '</span><span class="b">' + b + '</span></span>'; }
const DERIV = {
  chamber: '<h4>the photon, and PhET&rsquo;s coin</h4>'
    + EQ(1, 'E = hc/&lambda;, &nbsp; hc/e = 1239.841984332002 eV&#8239;nm <span class="rm">exactly</span>')
    + EQ(2, 'P(absorb) = &frac12; <span class="rm">per photon, once</span>; &nbsp; t<sub>hold</sub> ~ U(1.1, 1.3) s')
    + EQ(3, '&lang;busy&rang; = 1.2 + 0.2 = 1.4 s, &nbsp; T<sub>emit</sub> = 0.8 s')
    + '<p>[1] is exact arithmetic: the 2019 SI fixes h, c and e by definition, so hc carries no uncertainty at all. '
    + '[2] is PhET&rsquo;s, and the &ldquo;once&rdquo; is the subtle part &mdash; its pass-through list makes the first '
    + 'failed trial final, so a photon that spends four frames inside the absorption radius still gets one coin flip. '
    + 'A renewal estimate from [3] with a decorrelated phase gives the molecule excited 46.2&thinsp;% of the time; the '
    + 'simulation measures 49.1&thinsp;% over five 1200-second runs, and the gap is real: the source is exactly '
    + 'periodic and the busy time nearly deterministic, so the phase never decorrelates.</p>'
    + '<div class="cite">pins: the photon energies, PhET&rsquo;s constants, and a 60-second and a 600-second chamber run '
    + 'reproduced photon for photon by derive.py &mdash; same generator, same counts</div>',
  spectrum: '<h4>one axis, three labels</h4>'
    + EQ(1, 'E = hc/&lambda; = h&nu; = hc&nu;&#771;')
    + EQ(2, '&nu;&#771;(CO, J = 1 &larr; 0) = 2B&#8320; = 2(B<sub>e</sub> &minus; &alpha;<sub>e</sub>/2)')
    + EQ(3, '&lambda;<sub>threshold</sub> = hc/D&#8320;')
    + '<p>[2] is derived rather than quoted: B<sub>e</sub> comes out of the measured r<sub>e</sub> and the reduced mass '
    + 'to 3.5&times;10<sup>&minus;7</sup> of the tabulated value, and the line lands at 115.2719 GHz against the '
    + '115.2712 GHz radio astronomers use &mdash; the 6&times;10<sup>&minus;6</sup> residual is the centrifugal '
    + 'distortion &minus;4D&#8320;, not an error. Doing the same for oxygen is how a mislabelled column was caught: '
    + 'the WebBook prints its rotational constant in square brackets, which in Huber and Herzberg means B&#8320; and '
    + 'not B<sub>e</sub>, and reading it as B<sub>e</sub> disagrees with the same row&rsquo;s r<sub>e</sub> by 0.55&thinsp;% '
    + 'where reading it as B&#8320; agrees to 1.1&times;10<sup>&minus;5</sup>. [3] uses bond energies that are QUOTED, '
    + 'not re-derived.</p>'
    + '<div class="cite">pins: all five photon energies, B<sub>e</sub> from geometry for three diatomics, the bracket '
    + 'test both ways, the CO line, every threshold &mdash; derive.py</div>',
  table: '<h4>the two selection rules</h4>'
    + EQ(1, '<span class="rm">pure rotation:</span> &nbsp; &mu; &ne; 0')
    + EQ(2, '<span class="rm">infrared:</span> &nbsp; &part;&mu;/&part;Q<sub>k</sub> &ne; 0')
    + EQ(3, '<span class="rm">under an operation S with</span> S Q = &minus;Q <span class="rm">and</span> S &mu; = +&mu;: &nbsp; &part;&mu;/&part;Q &equiv; 0')
    + '<p>[3] is the whole content of [2]: if a symmetry of the molecule reverses the mode but not the dipole, the '
    + 'derivative must vanish identically. Computed here two independent ways &mdash; from rigid point charges, where '
    + 'every inactive mode returns zero to 4&times;10<sup>&minus;15</sup> and stays zero when the charges are '
    + 'rescaled, and from the inversion character of the centrosymmetric molecules, where gerade and ungerade decide '
    + 'it with no numbers at all. The two agree on every mode they both cover.</p>'
    + '<div class="cite">pins: 26 modes over nine molecules, the six exact zeros and the twenty non-zeros, both routes '
    + '&mdash; derive.py; dipole moments NIST CCCBDB</div>',
  modes: '<h4>the mass-weighted Hessian</h4>'
    + EQ(1, 'H&#771;<sub>ij</sub> = ' + FR('1', '&radic;(m<sub>i</sub>m<sub>j</sub>)') + ' '
            + FR('&part;&sup2;V', '&part;x<sub>i</sub>&part;x<sub>j</sub>') + ', &nbsp; H&#771; d = &omega;&sup2; d')
    + EQ(2, '<span class="rm">linear XY&#8322;:</span> (1, 0, &minus;1) <span class="rm">and</span> (1, &minus;2m<sub>Y</sub>/m<sub>X</sub>, 1)')
    + EQ(3, '<span class="rm">bent XY&#8322;, B&#8322;:</span> v/u = cot(&theta;/2)')
    + '<p>[2] and [3] are exact and need no force field: they follow from the symmetry operation plus zero linear and '
    + 'zero angular momentum. The eigenvectors this file computes reproduce them to 7&times;10<sup>&minus;15</sup>, '
    + 'which is what makes the diagonalisation a check rather than a claim. Two numerical details matter. The bend of a '
    + 'linear molecule is written as 1 + cos&theta;, not (&pi; &minus; &theta;)&sup2;, because arccos has infinite '
    + 'gradient at &pi; and the first form is smooth in the Cartesian coordinates. And the Hessian is Eckart-projected '
    + 'before diagonalisation: a finite-difference Hessian is only translationally invariant to O(h&sup2;), and the '
    + 'residual leaks into the eigenvectors as a drift of 2&times;10<sup>&minus;8</sup>, which projection removes '
    + 'entirely.</p>'
    + '<div class="cite">pins: every wavenumber against derive.py, the exact shapes for CO&#8322; and the three bent '
    + 'triatomics, momentum and angular momentum on all 26 modes, the CH&#8324; degeneracies 3,1,2,3</div>',
  stats: '<h4>the three rules, and what they are entitled to</h4>'
    + EQ(1, '&sigma;(p&#770;) = &radic;(p(1&minus;p)/N) = ' + FR('1', '2&radic;N') + ' <span class="rm">at p = &frac12;</span>')
    + EQ(2, '&sigma;(t&#772;) = ' + FR('b &minus; a', '&radic;(12N)') + ', &nbsp; &sigma;(&lang;cos&rang;) = ' + FR('1', '&radic;(2N)'))
    + EQ(3, '&chi;&sup2; = &Sigma;(O &minus; E)&sup2;/E <span class="rm">on 11 d.f.</span>')
    + '<p>Each measurement is compared against four times its own standard error, which an honest generator fails about '
    + 'six times in a hundred thousand. The generator is a seeded mulberry32, all 32-bit, which is why the Python twin '
    + 'reproduces every draw bit for bit rather than merely statistically. The test is shown to have teeth by running '
    + 'it on a generator biased to 0.52: at twenty thousand draws that is 5.7 standard errors out and is rejected.</p>'
    + '<div class="cite">pins: the first six draws, the mean and variance of 20&thinsp;000, and the absorbed count, '
    + 'hold mean and s.d., direction moments and &chi;&sup2; &mdash; all identical in derive.py</div>',
  air: '<h4>Planck, per wavenumber</h4>'
    + EQ(1, 'B<sub>&nu;&#771;</sub>(T) = ' + FR('2hc&sup2;&nu;&#771;&sup3;', 'e<sup>hc&nu;&#771;/kT</sup> &minus; 1'))
    + EQ(2, '&pi;&int;B<sub>&nu;&#771;</sub> d&nu;&#771; = &sigma;T&#8308;')
    + EQ(3, '<span class="rm">peak:</span> 3(1 &minus; e<sup>&minus;x</sup>) = x, &nbsp; x = hc&nu;&#771;/kT = 2.8214393721')
    + '<p>[2] is the check that [1] is normalised correctly: the quadrature reproduces &sigma;T&#8308; to 7 parts in '
    + '10<sup>9</sup>. [3] is Wien&rsquo;s displacement in the wavenumber form, which is a different root from the '
    + 'wavelength form&rsquo;s 4.965 and gives 565 cm&#8315;&#185; at 288 K, not the 10 &micro;m the wavelength form '
    + 'would give &mdash; the two peaks are different questions about the same spectrum. The band positions drawn on it '
    + 'are measured fundamentals; nothing here computes a cross-section, so this picture says where the absorption is, '
    + 'never how strong.</p>'
    + '<div class="cite">pins: the Stefan&ndash;Boltzmann check, the Wien root, the peak, the window fraction &mdash; '
    + 'derive.py; composition NASA Earth Fact Sheet and NOAA GML</div>',
};
