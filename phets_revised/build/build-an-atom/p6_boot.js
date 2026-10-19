
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
    tabsEl.appendChild(h('button', {class: st.view === k ? 'active' : '',
                                    onclick: () => setView(k)}, lab2));
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
    rows[key] = {row: rowEl, sync: sync, inp: inp}; sync(); return rowEl;
  }
  /* the game's answer controls write into GAME.given, not into ST: they are
     the answer, not a setting, and the reset button must not touch them */
  function gslider(field, lab2){
    const r = FIELD_RANGE[field];
    const inp = h('input', {type: 'range', min: r[0], max: r[1], step: 1, value: r[0]});
    const val = h('span', {class: 'val'});
    const rowEl = h('div', {class: 'sliderrow'}, h('label', null, lab2), inp, val);
    const show = v => field === 'element'
      ? (v >= 1 ? SYMBOL[v] + ' (' + v + ')' : '—')
      : (field === 'charge' ? chargeString(v, st.notation === 'first') : String(v));
    const sync = () => {
      const v = GAME.given[field];
      inp.value = (v === undefined ? r[0] : v);
      val.textContent = show(v === undefined ? r[0] : v);
    };
    inp.addEventListener('input', () => {
      GAME.given[field] = parseInt(inp.value, 10);
      val.textContent = show(GAME.given[field]);
      dirty = true; refresh();
    });
    rows['g_' + field] = {row: rowEl, sync: sync, inp: inp}; sync(); return rowEl;
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
      const c = h('button', {class: 'chip' + (st[key] === o.id ? ' on' : ''), html: o.name,
        onclick: () => {
          const was = st[key]; st[key] = o.id; if(onPick) onPick(o, was);
          [].forEach.call(wrapEl.children, (b, i) =>
            b.className = 'chip' + (list[i].id === st[key] ? ' on' : ''));
          syncPanel(); dirty = true; refresh();
        }});
      wrapEl.appendChild(c);
    });
    rows['chips_' + key] = {row: wrapEl, sync: () => {
      [].forEach.call(wrapEl.children, (b, i) =>
        b.className = 'chip' + (list[i].id === st[key] ? ' on' : ''));
    }};
    return wrapEl;
  }
  function btn(label2, fn){
    return h('button', {onclick: () => { fn(); syncPanel(); dirty = true; refresh(); }}, label2);
  }

  /* ---- the three counts: PhET's buckets, as numbers ---- */
  const gCounts = h('div', {class: 'grp'}, h('h3', null, 'the atom'));
  gCounts.appendChild(slider('p', 'protons', 0, PHET.numProtons, 1, v => fmt(v, 0)
    + (v ? ' — ' + elementSymbol(v) : '')));
  gCounts.appendChild(slider('n', 'neutrons', 0, PHET.numNeutrons, 1, v => fmt(v, 0)));
  gCounts.appendChild(slider('e', 'electrons', 0, PHET.numElectrons, 1, v => fmt(v, 0)));
  gCounts.appendChild(h('div', {class: 'btnrow'},
    btn('neutral', () => { st.e = st.p; }),
    btn('most common', () => { if(st.p) st.n = Math.min(MOSTN[st.p], PHET.numNeutrons); }),
    btn('empty', () => { st.p = 0; st.n = 0; st.e = 0; })));
  gCounts.appendChild(h('div', {class: 'btnrow'},
    btn('carbon-12', () => setNuclide(6, 6, 6)),
    btn('reset all', () => {
      const v = st.view; Object.assign(st, DEFAULTS); st.view = v;
      gameReset(st); FRAME.jig = 0; dragClear();
    })));
  const countTag = h('div', {class: 'tag'}); gCounts.appendChild(countTag);

  /* ---- the picture ---- */
  const gPic = h('div', {class: 'grp'}, h('h3', null, 'the picture'));
  gPic.appendChild(chipRow(MODELS, 'model'));
  gPic.appendChild(h('div', {class: 'checks'},
    checkbox('showName', 'element name'),
    checkbox('showIon', 'neutral atom or ion'),
    checkbox('showStab', 'nuclear stability'),
    checkbox('showTable', 'periodic table'),
    checkbox('jiggle', 'an unstable nucleus jiggles')));
  const picTag = h('div', {class: 'tag'}); gPic.appendChild(picTag);

  /* ---- the symbol ---- */
  const gSym = h('div', {class: 'grp'}, h('h3', null, 'charge notation'));
  gSym.appendChild(chipRow(NOTATIONS, 'notation'));
  const symTag = h('div', {class: 'tag'}); gSym.appendChild(symTag);

  /* ---- the game ---- */
  const gGame = h('div', {class: 'grp'}, h('h3', null, 'the game'));
  gGame.appendChild(slider('level', 'level', 1, PHET.numLevels, 1, v => fmt(v, 0)));
  gGame.appendChild(slider('gseed', 'seed', 1, 999999, 1, v => fmt(v, 0)));
  gGame.appendChild(h('div', {class: 'btnrow'},
    btn('start level', () => gameStart(st)),
    btn('new game', () => gameReset(st))));
  const gAns = h('div', {class: 'grp'}, h('h3', null, 'your answer'));
  /* "answer: protons" and not "protons": the atom group already owns a slider
     called protons, and a harness finder that matches a word rather than the
     whole label drives the wrong one (Known-bad, lagrange_points) */
  for(const f of ['element', 'protons', 'neutrons', 'electrons', 'mass', 'charge'])
    gAns.appendChild(gslider(f, 'answer: ' + FIELD_NAME[f]));
  gAns.appendChild(h('div', {class: 'btnrow'},
    btn('check', () => { gameCheck(); }),
    btn('try again', () => { gameRetry(); }),
    btn('next', () => { gameNext(); })));
  const gameTag = h('div', {class: 'tag'}); gGame.appendChild(gameTag);

  /* ---- the counting ---- */
  const gCount = h('div', {class: 'grp'}, h('h3', null, 'colour the grid by'));
  gCount.appendChild(chipRow(COUNT_MODES, 'countMode'));
  const cntTag = h('div', {class: 'tag'}); gCount.appendChild(cntTag);

  /* ---- the chart ---- */
  const gChart = h('div', {class: 'grp'}, h('h3', null, 'the chart'));
  gChart.appendChild(slider('chartZmax', 'Z up to', 12, 84, 2, v => fmt(v, 0)));
  gChart.appendChild(h('div', {class: 'checks'},
    checkbox('chartCompare', 'mark where the two tables differ'),
    checkbox('chartMagic', 'the magic numbers')));
  const chartTag = h('div', {class: 'tag'}); gChart.appendChild(chartTag);

  /* ---- mass and binding ---- */
  const gMass = h('div', {class: 'grp'}, h('h3', null, 'mass and binding'));
  gMass.appendChild(h('div', {class: 'checks'},
    checkbox('bindAll', 'the whole stable valley, not only Z ≤ 18'),
    checkbox('showAbund', 'show the trace isotopes')));
  const massTag = h('div', {class: 'tag'}); gMass.appendChild(massTag);

  const gInfo = h('div', {class: 'grp'}, h('h3', null, 'what you are looking at'),
    h('div', {id: 'info'}),
    h('div', {class: 'src', html: 'Remake of PhET Interactive Simulations&rsquo; Build an Atom '
      + '(University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or '
      + 'assets. PhET&rsquo;s values &mdash; the three screens, the 10/13/10 buckets, the 85 and 130 '
      + 'shell radii, the ten electron slots, the cloud law r = 42.5 + 8.75&thinsp;e, the 100 and 143 '
      + 'capture radii, the stableElementTable of 244 nuclides, the isotope and standard-weight '
      + 'tables, the element names and symbols, the four AtomValuePool challenge pools and the '
      + '5 challenges / 2 / 1 scoring &mdash; are read out of its minified build 1.9.3 in docs/phets/. '
      + 'The independent nuclide table (NUBASE half-lives, NIST Atomic Weights and Isotopic '
      + 'Compositions) and the periodic-table layout come from projects/simulations/periodic_table.html. '
      + 'm<sub>n</sub> and the u&rarr;MeV conversion are CODATA 2022 via scipy.constants. Every '
      + 'reference number selfTest asserts is a line of build/build-an-atom/_out/refvals.txt, written '
      + 'by derive.py.'}));
  [gCounts, gPic, gSym, gGame, gAns, gCount, gChart, gMass, gInfo]
    .forEach(g => panel.appendChild(g));
  const infoEl = gInfo.querySelector('#info');

  /* a control a view ignores is HIDDEN, never left live and inert */
  function syncPanel(){
    const v = st.view;
    gCounts.hidden = (v === 'game');
    gPic.hidden = !(v === 'atom' || v === 'symbol');
    rows.cb_showTable.row.hidden = (v !== 'atom');
    rows.cb_jiggle.row.hidden = (v !== 'atom');
    rows.cb_showName.row.hidden = (v !== 'atom');
    rows.cb_showIon.row.hidden = (v !== 'atom');
    rows.cb_showStab.row.hidden = (v !== 'atom');
    gSym.hidden = (v !== 'symbol');
    gGame.hidden = (v !== 'game');
    gAns.hidden = !(v === 'game' && (GAME.phase === 'ask' || GAME.phase === 'wrong'));
    const c = gameCurrent();
    const fields = c ? answerFields(c.type) : [];
    for(const f of ['element', 'protons', 'neutrons', 'electrons', 'mass', 'charge'])
      rows['g_' + f].row.hidden = (fields.indexOf(f) < 0);
    gCount.hidden = (v !== 'counting');
    gChart.hidden = (v !== 'chart');
    gMass.hidden = (v !== 'mass');
    for(const k in rows) rows[k].sync();
    const M = buildModel(st);
    countTag.innerHTML = 'the buckets hold <b>' + PHET.numProtons + '</b> protons, <b>'
      + PHET.numNeutrons + '</b> neutrons and <b>' + PHET.numElectrons + '</b> electrons, which are '
      + 'PhET&rsquo;s own, so the elements stop at neon and the charge runs &minus;'
      + PHET.numElectrons + ' to +' + PHET.numProtons + '. On the atom view you can drag them '
      + 'instead, or click a lit periodic-table cell.';
    picTag.innerHTML = 'PhET&rsquo;s two models. <b>Orbits</b> fills 2 then 8 in ten fixed slots; '
      + '<b>cloud</b> is one disc whose radius is r = 42.5 + 8.75&thinsp;e model units, so ten '
      + 'electrons put it exactly on the outer shell at 130. Neither is an orbital calculation.';
    symTag.innerHTML = 'PhET ships both sign conventions as a preference and defaults to <b>sign '
      + 'last</b> (2+), which is what chemistry writes; <b>sign first</b> (+2) is what physics '
      + 'writes. The charge here is ' + M.chargeStr + '.';
    gameTag.innerHTML = 'four levels &times; ' + PHET.challengesPerLevel + ' challenges, '
      + PHET.pointsFirst + ' points first try and ' + PHET.pointsSecond + ' second. The seed fixes '
      + 'the whole level: seed ' + st.gseed + ' on level ' + st.level + ' always gives the same five. '
      + (GAME.phase === 'idle' ? 'Press <b>start level</b>, or click a card.'
        : (GAME.phase === 'ask' ? 'Set the answer, then <b>check</b>.'
          : (GAME.phase === 'wrong' ? 'One more try, worth ' + PHET.pointsSecond + '.'
            : (GAME.phase === 'done' ? 'Level over.' : 'Press <b>next</b>.'))));
    cntTag.innerHTML = 'every one of the <b>' + M.census.total + '</b> configurations is checked in '
      + 'selfTest against an independently written expression for the element, the mass number, the '
      + 'charge and the stability. The magenta cell is the nucleus you have built.';
    chartTag.innerHTML = 'PhET&rsquo;s table has <b>' + M.nStable + '</b> nuclides; an independent '
      + 'one (NUBASE + NIST) has <b>253</b>; they agree on <b>243</b>. Below Z = 24 they are '
      + 'identical. The magic numbers are 2, 8, 20, 28, 50, 82, 126.';
    massTag.innerHTML = 'the bars are <b>measured</b> natural abundances and atomic masses; their '
      + 'mean is the standard atomic weight. The binding curve is computed from the masses, not '
      + 'from a mass formula, and peaks at <b>nickel-62</b>.';
  }

  /* the HTML panels only.  A pointer handler must update them — a stale
     readout during a drag is a bug — but it must NOT draw, or the frame
     loop's dirty flag is masked and the drag tests test nothing
     (Known-bad, three times). */
  function panels(){
    try{
      const M = S.model();
      roEl.innerHTML = readoutHTML(M);
      eqEl.innerHTML = eqbarHTML(M);
      tagEl.innerHTML = tagHTML(M);
      hintEl.textContent = HINT[st.view] || '1–6 switch views';
      infoEl.innerHTML = INFO[st.view] || '';
    }catch(e){ fail(e); }
  }
  function refresh(){
    panels();
    try{ S.draw(); }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown', e => {
    canvas.setPointerCapture(e.pointerId);
    const r = canvas.getBoundingClientRect();
    if(S.pointer('down', e.clientX - r.left, e.clientY - r.top)){
      canvas.classList.add('dragging'); dirty = true; syncPanel(); panels();
    }
  });
  canvas.addEventListener('pointermove', e => {
    if(!canvas.classList.contains('dragging') && e.buttons === 0) return;
    const r = canvas.getBoundingClientRect();
    if(S.pointer('move', e.clientX - r.left, e.clientY - r.top)){ dirty = true; panels(); }
  });
  const up = e => {
    canvas.classList.remove('dragging');
    const r = canvas.getBoundingClientRect();
    const x = e && e.clientX !== undefined ? e.clientX - r.left : DRAG.x;
    const y = e && e.clientY !== undefined ? e.clientY - r.top : DRAG.y;
    if(S.pointer('up', x, y)){ dirty = true; syncPanel(); panels(); }
  };
  canvas.addEventListener('pointerup', up);
  canvas.addEventListener('pointercancel', up);

  window.addEventListener('keydown', e => {
    if(e.key >= '1' && e.key <= String(TABS.length)){ setView(TABS[+e.key - 1][0]); return; }
    if(e.key === '0'){ st.p = 0; st.n = 0; st.e = 0; }
    else if(e.key === 'n'){ st.e = st.p; }
    else if(e.key === 'm'){ if(st.p) st.n = Math.min(MOSTN[st.p], PHET.numNeutrons); }
    else if(e.key === 'c'){ if(GAME.phase === 'idle') gameStart(st); else gameCheck(); }
    else if(e.key === '.'){ if(GAME.phase === 'wrong') gameRetry(); else gameNext(); }
    else return;
    e.preventDefault(); syncPanel(); dirty = true; refresh();
  });

  function resize(){
    const r = canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(r.width * dpr); canvas.height = Math.round(r.height * dpr);
    canvas.getContext('2d').setTransform(dpr, 0, 0, dpr, 0, 0);
    S.W = r.width; S.H = r.height;
  }
  window.addEventListener('resize', () => { resize(); dirty = true; refresh(); });

  let frameN = 0;
  function frameLoop(tm){
    frameN++;
    const advanced = S.step();
    if(advanced || dirty){
      dirty = false;
      try{ S.draw(); }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  gameReset(st);
  resize(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const HINT = {
  atom: 'drag particles between the buckets and the atom · click a lit table cell · 1–6 switch views',
  symbol: 'n makes it neutral · m takes the most common isotope · 1–6 switch views',
  game: 'click a level card · c checks · . goes on · 1–6 switch views',
  counting: '0 empties the atom · n makes it neutral · 1–6 switch views',
  chart: 'the magenta box is what the buckets can reach · 1–6 switch views',
  mass: 'm takes the most common isotope · 1–6 switch views',
};

const INFO = {
  atom: 'PhET&rsquo;s <b>Atom</b> screen. Drag protons, neutrons and electrons out of the buckets '
    + 'and drop them on the atom, and four things follow at once. The <b>element</b> is the proton '
    + 'count and nothing else &mdash; add a neutron and you still have carbon, add an electron and '
    + 'you still have carbon. The <b>mass number</b> is protons plus neutrons. The <b>charge</b> is '
    + 'protons minus electrons. The fourth, whether the nucleus is <b>stable</b>, is the odd one '
    + 'out: it is not arithmetic at all, it is a lookup in a measured table, and the chart-of-'
    + 'nuclides view is that table. The two models are PhET&rsquo;s: fixed orbits filling 2 then 8, '
    + 'or a cloud whose radius grows linearly with the electron count.',
  symbol: 'PhET&rsquo;s <b>Symbol</b> screen. The same three integers, written the way a chemist '
    + 'writes them: the mass number above the atomic number on the left of the symbol, the charge '
    + 'on the right shoulder. Two things are worth noticing. The symbol is <i>redundant</i> &mdash; '
    + 'the element letter and the atomic number say the same thing, which is why Z is often left '
    + 'off. And the neutron count never appears: you recover it as A &minus; Z, so a symbol '
    + 'identifies the nuclide but does not name what does the identifying. PhET ships both charge '
    + 'conventions; the chips switch between them.',
  game: 'PhET&rsquo;s <b>Game</b> screen, with its own four levels, its own challenge types and its '
    + 'own scoring: five challenges a level, two points for a right answer first time and one for a '
    + 'right answer second time. The challenge names say exactly what happens &mdash; '
    + '<i>schematic-to-charge</i> shows you a drawing and asks for the charge, '
    + '<i>symbol-to-counts</i> shows you a symbol and asks how many of each particle. The generator '
    + 'is seeded, so a level can be replayed exactly; that is what lets selfTest check 16 000 '
    + 'generated levels for solvability rather than trusting one.',
  counting: 'Every nucleus the buckets can build, laid out with the neutron count across and the '
    + 'proton count up: ten elements, fourteen neutron numbers, and eleven electron counts on top '
    + 'of that, which is ' + '1694' + ' configurations in all. The point of the view is that three '
    + 'of the four answers are pure arithmetic and are therefore checkable everywhere at once &mdash; '
    + 'selfTest walks all of them &mdash; while the fourth, stability, has to be looked up cell by '
    + 'cell. The twenty green cells are every stable nuclide with Z &le; 10 that exists. Four of '
    + 'them have an odd proton count AND an odd neutron count, and those four are the only odd-odd '
    + 'stable nuclides in the whole chart of nuclides.',
  chart: 'The table behind the word &ldquo;stable&rdquo;. Each square is a nuclide PhET calls '
    + 'stable; there are 244 of them and they stop at lead. Two things are drawn beside them. The '
    + 'first is N = Z: light nuclei sit on it and heavy ones leave it, because the Coulomb energy '
    + 'grows as Z&sup2; while the nuclear force is short-ranged and saturates, so a big nucleus '
    + 'needs extra neutrons to dilute the repulsion. The second is an <b>independent</b> stability '
    + 'table, built from NUBASE half-lives and NIST abundances, which disagrees with PhET&rsquo;s '
    + 'in eleven places &mdash; every one of them a nuclide that is predicted to decay but has '
    + 'never been caught doing it. Below Z = 24 the two are identical.',
  mass: 'The measured half of the sim. Isotope atomic masses and natural abundances are data, with '
    + 'a source and a precision, and two things fall out of them. First, the <b>standard atomic '
    + 'weight</b> is nothing but their mean: multiply each isotope&rsquo;s mass by how much of it '
    + 'there is and add up. Second, the <b>mass defect</b>. A nucleus weighs less than its parts, '
    + 'and the difference, times c&sup2;, is the energy holding it together. Plotted per nucleon '
    + 'against A it rises steeply through the light elements, peaks at nickel-62, and falls slowly '
    + 'after &mdash; which is the whole of why fusion releases energy at one end and fission at the '
    + 'other. Nothing here is fitted: the curve is arithmetic on measured masses.',
};
