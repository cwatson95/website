
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
    syncPanel(); dirty = true; refresh();
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
  function btn(label2, fn){
    return h('button', {onclick: () => { fn(); syncPanel(); dirty = true; refresh(); }}, label2);
  }

  /* ---- the scene: PhET's two Rutherford scenes are its own radio pair ---- */
  const gScene = h('div', {class: 'grp'}, h('h3', null, 'the scene'));
  const sceneChips = chipRow(SCENES, 'sceneSel', o => setView(o.id === 'nucleus' ? 'nucleus' : 'foil'));
  gScene.appendChild(sceneChips);
  const sceneTag = h('div', {class: 'tag'}); gScene.appendChild(sceneTag);

  /* ---- the alpha particles (PhET's own panel) ---- */
  const gAlpha = h('div', {class: 'grp'}, h('h3', null, 'alpha particles'));
  gAlpha.appendChild(slider('energy', 'energy', PHET.minEnergy, PHET.maxEnergy, 1,
    v => fmt(v, 0) + (v === PHET.minEnergy ? ' min' : (v === PHET.maxEnergy ? ' max' : ''))));
  gAlpha.appendChild(h('div', {class: 'checks'},
    checkbox('traces', 'traces'), checkbox('gunOn', 'the gun is firing'),
    checkbox('showClosed', 'the closed form over the live particle')));
  const alphaTag = h('div', {class: 'tag'}); gAlpha.appendChild(alphaTag);

  /* ---- the atom (PhET's own panel) ---- */
  const gAtom = h('div', {class: 'grp'}, h('h3', null, 'the atom'));
  gAtom.appendChild(slider('protons', 'protons', PHET.minProtons, PHET.maxProtons, 1, v => fmt(v, 0)));
  gAtom.appendChild(slider('neutrons', 'neutrons', PHET.minNeutrons, PHET.maxNeutrons, 1, v => fmt(v, 0)));
  const atomTag = h('div', {class: 'tag'}); gAtom.appendChild(atomTag);

  /* ---- time ---- */
  const gTime = h('div', {class: 'grp'}, h('h3', null, 'time'));
  gTime.appendChild(h('div', {class: 'checks'}, checkbox('running', 'time runs')));
  gTime.appendChild(slider('rate', 'speed', 0.25, 3, 0.25, v => '×' + fmt(v, 2)));
  gTime.appendChild(slider('seed', 'random seed', 1, 999999, 1, v => fmt(v, 0), () => engineReset(st)));
  gTime.appendChild(h('div', {class: 'btnrow'},
    btn('step', () => { engineStepOnce(st); }),
    btn('clear', () => { engineReset(st); }),
    btn('reset all', () => { const v = st.view; Object.assign(st, DEFAULTS); st.view = v; engineReset(st); })));
  const timeTag = h('div', {class: 'tag'}); gTime.appendChild(timeTag);

  /* ---- the closed form ---- */
  const gHyp = h('div', {class: 'grp'}, h('h3', null, 'the trajectory'));
  gHyp.appendChild(slider('bModel', 'impact parameter b', 0, 120, 0.5, v => fmt(v, 1) + ' u'));
  gHyp.appendChild(slider('nPaths', 'how many orbits', 1, 19, 1, v => fmt(v, 0)));
  gHyp.appendChild(h('div', {class: 'checks'},
    checkbox('showInt', 'the RK4 integration over it'),
    checkbox('showAsym', 'asymptotes, b and r min')));
  gHyp.appendChild(h('div', {class: 'btnrow'},
    btn('head on, b = 0', () => { st.bModel = 0; }),
    btn('b = D/2 (90°)', () => { st.bModel = phetD(PHET.boxW, st.protons, st.energy) / 2; })));
  const hypTag = h('div', {class: 'tag'}); gHyp.appendChild(hypTag);

  /* ---- the beam ---- */
  const gBeam = h('div', {class: 'grp'}, h('h3', null, 'the sampled beam'));
  gBeam.appendChild(slider('nSample', 'particles', 2000, 60000, 1000, v => fmt(v, 0)));
  gBeam.appendChild(slider('bMax', 'beam radius bmax', 20, 400, 10, v => fmt(v, 0) + ' u'));
  gBeam.appendChild(h('div', {class: 'checks'},
    checkbox('showSample', 'the sampled points'),
    checkbox('showJac', 'the Jacobian route')));
  const beamTag = h('div', {class: 'tag'}); gBeam.appendChild(beamTag);

  /* ---- real units ---- */
  const gReal = h('div', {class: 'grp'}, h('h3', null, 'in metres'));
  gReal.appendChild(slider('EMeV', 'alpha energy', 0.5, 30, 0.1, v => fmt(v, 1) + ' MeV'));
  gReal.appendChild(slider('foilNm', 'gold leaf', 50, 4000, 50, v => fmt(v, 0) + ' nm'));
  gReal.appendChild(slider('exagg', 'draw Thomson ×', 1, 4001, 500, v => '×' + fmt(v, 0)));
  gReal.appendChild(h('div', {class: 'btnrow'},
    btn('RaC′ 7.7 MeV', () => { st.EMeV = 7.7; }),
    btn('touching energy', () => { st.EMeV = clamp(goldNumbers(st).Etouch / MEV, 0.5, 30); })));
  const realTag = h('div', {class: 'tag'}); gReal.appendChild(realTag);

  const gInfo = h('div', {class: 'grp'}, h('h3', null, 'what you are looking at'),
    h('div', {id: 'info'}),
    h('div', {class: 'src', html: 'Remake of PhET Interactive Simulations&rsquo; Rutherford Scattering '
      + '(University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      + 'PhET&rsquo;s values &mdash; both screens, both scenes, the 255-unit box, the five atoms of width 30, '
      + 'D = (L/8)(protons/79)(80/energy)&sup2;, the 50&ndash;100 energy and 20&ndash;100 / 20&ndash;150 proton and '
      + 'neutron ranges, the one-every-width/energy/20 gun, its 4% nudge away from an atom, its traces-off default '
      + 'and its two scale captions (6.0&times;10&minus;&sup1;&#8304; m and 1.5&times;10&minus;&sup1;&sup3; m) &mdash; '
      + 'are read out of its minified build 1.1.29, and the element names are its own SHRED strings. '
      + 'Everything in metres is exact and pinned in selfTest to build/rutherford-scattering/derive.py: '
      + 'scipy.constants (CODATA 2022), scipy.integrate.quad and solve_ivp, scipy.optimize.brentq and '
      + 'minimize_scalar, and a bit-for-bit Python mulberry32. Gold: Z = 79, A = 197 (monoisotopic), molar mass '
      + '196.96657 g/mol, density 19&thinsp;300 kg/m&sup3;, nuclear radius 1.2 A&#8531; fm, metallic radius '
      + '1.44&times;10&minus;&sup1;&#8304; m.'}));
  [gScene, gAlpha, gAtom, gTime, gHyp, gBeam, gReal, gInfo].forEach(g => panel.appendChild(g));
  const infoEl = gInfo.querySelector('#info');

  /* a control a view ignores is HIDDEN, never left live and inert */
  function syncPanel(){
    const v = st.view;
    st.sceneSel = v === 'foil' ? 'atom' : 'nucleus';
    [].forEach.call(sceneChips.children, (b, i) =>
      b.className = 'chip' + (SCENES[i].id === st.sceneSel ? ' on' : ''));
    gScene.hidden = !(v === 'nucleus' || v === 'foil');
    gAlpha.hidden = !liveView(v);
    rows.cb_showClosed.row.hidden = (v === 'pudding');
    gAtom.hidden = (v === 'sigma');
    rows.neutrons.row.hidden = !liveView(v) && v !== 'hyperbola';
    gTime.hidden = !liveView(v);
    gHyp.hidden = (v !== 'hyperbola');
    gBeam.hidden = (v !== 'sigma');
    gReal.hidden = !(v === 'pudding' || v === 'gold');
    rows.exagg.row.hidden = (v !== 'pudding');
    for(const k in rows) rows[k].sync();
    const M = buildModel();
    sceneTag.innerHTML = 'PhET&rsquo;s own radio pair. The two scenes carry the SAME D/L = 1/8, so they look alike '
      + 'although their captions are 4000&times; apart and the geometry is only '
      + fmt(PHET.boxW / PHET.atomW, 1) + '&times;.';
    alphaTag.innerHTML = 'PhET labels this slider <b>Energy</b> and uses it as the <b>speed</b>, so D &prop; 1/energy&sup2; '
      + '&mdash; which is the right 1/E scaling. D = ' + fmt(M.D, 3) + ' units, &alpha; = ' + sigf(M.alpha, 4)
      + ' units&sup3;/s&sup2; and &alpha; does not depend on the slider at all.';
    atomTag.innerHTML = 'Z = ' + fmt(st.protons, 0) + (M.element ? ' is <b>' + M.element + '</b>' : '')
      + '. Neutrons change the drawn nucleus and <b>nothing else</b> &mdash; PhET&rsquo;s model notes say the same. '
      + 'Gold-197 is 79 + 118, which is what PhET opens with.';
    timeTag.innerHTML = 'space runs/pauses &nbsp; <b>.</b> steps one 1/60 s tick &nbsp; <b>g</b> works the gun '
      + '&nbsp; <b>c</b> clears &nbsp; 1&ndash;6 switch views<br>the seed makes the run reproducible; '
      + 'click the stage to start or stop the gun.';
    hypTag.innerHTML = 'drag on the picture to set b. At b = 0 the alpha goes straight in, stops at r = D and comes '
      + 'straight back: &theta; = 180&deg; exactly. b = D/2 = ' + fmt(M.D / 2, 2) + ' gives 90&deg;.';
    beamTag.innerHTML = 'b uniform on a <b>disc</b>, which is what a beam is. The gun in the live views fires along a '
      + '<b>line</b> instead, whose fraction beyond &theta; is b(&theta;)/X rather than (b(&theta;)/bmax)&sup2;.';
    realTag.innerHTML = 'the touching energy is where a head-on alpha reaches the nuclear surface and the 1/sin&#8308; '
      + 'law stops: ' + fmt(M.gold.Etouch / MEV, 1) + ' MeV for Z = ' + fmt(st.protons, 0) + '.';
  }

  function refresh(){
    try{
      const M = S.model();
      roEl.innerHTML = readoutHTML(M);
      eqEl.innerHTML = eqbarHTML(M);
      tagEl.innerHTML = tagHTML(M);
      hintEl.textContent = liveView(st.view)
        ? 'click the stage to work the gun · space pauses · 1–6 switch views'
        : (st.view === 'hyperbola'
          ? 'drag across the picture to set the impact parameter · 1–6 switch views'
          : '1–6 switch views');
      infoEl.innerHTML = INFO[st.view] || '';
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
    else if(e.key === '.'){ engineStepOnce(st); dirty = true; refresh(); }
    else if(e.key === 'g'){ st.gunOn = !st.gunOn; syncPanel(); dirty = true; refresh(); }
    else if(e.key === 'c'){ engineReset(st); dirty = true; refresh(); }
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
  engineReset(ST);
  resize(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO = {
  nucleus: 'PhET&rsquo;s <b>nuclear-scale scene</b>: one nucleus, a gun below it, and alpha particles that curve away '
    + 'from it. Every curve on screen is the exact hyperbola of the Coulomb problem &mdash; the sim solves for the '
    + 'asymptotic impact parameter of the orbit through the launch point and then advances the polar angle along '
    + 'that conic, so the particle is <i>on</i> the hyperbola at every step and only its timing is integrated. '
    + 'Turn the energy down or the protons up and the deflections grow, because both of them grow <b>D</b>, the '
    + 'distance a head-on alpha would get to. Turn the neutrons and nothing happens: they change the picture of '
    + 'the nucleus and not the field.',
  foil: 'PhET&rsquo;s <b>atomic-scale scene</b>: five atoms instead of one, each tracked inside a box of its own '
    + 'width. This is Geiger and Marsden&rsquo;s experiment in miniature, and the census under the stage is the '
    + 'result: nearly everything goes almost straight through, and once in a while one comes back. The reason is '
    + 'the impact parameter. Almost all of the beam area is at large b, where the deflection is tiny; the tiny '
    + 'fraction that arrives within D of the nucleus is thrown through a large angle.',
  pudding: 'PhET&rsquo;s <b>Plum Pudding Atom</b> screen. Its model has no atoms in it at all &mdash; the particles '
    + 'fly straight &mdash; and that is not a simplification, it is the physics. Spread the positive charge through '
    + 'the whole atom and the largest deflection any single atom can give is D/2R, which for a 7.7 MeV alpha on gold '
    + 'is about a ten-thousandth of a radian. The strip under the stage puts that number, the multiple-scattering '
    + 'width of a real foil, and Rutherford&rsquo;s angles on one logarithmic axis. They are five decades apart, '
    + 'and the exaggeration slider is the only reason you can see the wiggle at all.',
  hyperbola: 'The closed form on its own. A repulsive inverse-square force gives an exact hyperbola, and everything '
    + 'about the scattering is in one relation: <b>tan(&theta;/2) = D/2b</b>. Small b, big angle. The orange curves '
    + 'are that closed form for a family of impact parameters; the green dashes are an independent RK4 integration '
    + 'of Newton&rsquo;s equations started on the conic, which conserves energy and angular momentum to a part in '
    + '10<sup>11</sup> and reproduces the same deflection. Two routes agreeing is the only reason either can be '
    + 'believed. Drag across the picture to move b; at b = 0 the alpha goes straight in and comes straight back.',
  sigma: 'The cross section is a <b>Jacobian</b>: a ring of beam area 2&pi;b db lands in a ring of solid angle '
    + '2&pi; sin&theta; d&theta;, so d&sigma;/d&Omega; = (b/sin&theta;)|db/d&theta;|. Put b = (D/2)cot(&theta;/2) '
    + 'into it and the famous 1/sin&#8308;(&theta;/2) falls out, with the constant (D/4)&sup2; &mdash; and that '
    + 'constant is exactly what no amount of checking scaling and limits can pin, which is why it is computed here '
    + 'three separate ways. The magenta points are a seeded beam, binned in solid angle; their error bars are '
    + '1/&radic;N, the sampling law, and nothing has been fitted.',
  gold: 'The same problem in metres, for the experiment that was actually done. A 7.7 MeV alpha on gold has '
    + 'D = 29.5 fm, and the gold nucleus and the alpha together are 8.9 fm &mdash; so even a head-on alpha stops '
    + 'three times too far out to feel the nuclear force, and the Coulomb law is exact. Push the energy past '
    + '25.6 MeV and that stops being true. The plot at the bottom is the whole argument: a gold leaf a few '
    + 'thousand atoms thick sends about one alpha in sixty thousand past 90&deg; if the charge is in a nucleus, '
    + 'and 10<sup>&minus;99000</sup> of them if it is spread through the atom.',
};
