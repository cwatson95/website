
/* ================================================================== *
 *  state, the live chamber, the per-view model, readout, equation     *
 *  bar and tag                                                        *
 * ================================================================== */
const COL = {pos: '#b8ec4c', ref: '#e8843a', live: '#cd35c4', struct: '#5ac8e0',
             dim: '#8b93a6', edge: '#242a3a', text: '#aeb6c6', bond: '#9aa2b4',
             glow: '#ffe066', off: '#3a4154'};
const RO_W = 300;
/* sigf() writes an exponent as "×10^-6"; on the canvas that should be a
   real superscript.  Digit superscripts are safe in the rasteriser's font;
   letter subscripts are not, which is why nothing here uses one. */
function eFmt(x, n) {
  const s = sigf(x, n);
  const i = s.indexOf('×10^');
  if (i < 0) return s;
  return s.slice(0, i) + '×10' + supDigits(s.slice(i + 4));
}
const TABS = [['chamber', 'the chamber'], ['spectrum', 'the spectrum'],
              ['table', 'what responds'], ['modes', 'the normal modes'],
              ['stats', 'the statistics'], ['air', 'the atmosphere']];
/* the photon colours: PhET ships four PNG sprites, which this file does not
   use.  Each band gets a house accent instead, and the same four colours are
   used on the spectrum, in the table and in the chamber so a reader can
   follow one band across the views. */
const BANDCOL = {microwave: '#7f8cff', infrared: '#e8843a',
                 visible: '#b8ec4c', ultraviolet: '#cd35c4'};
const RESPCOL = {'': '#3a4154', rotate: '#5ac8e0', vibrate: '#e8843a',
                 glow: '#ffe066', break: '#cd35c4'};
const RESPNAME = {'': 'passes through', rotate: 'rotates', vibrate: 'vibrates',
                  glow: 'glows', break: 'breaks apart'};

const DEFAULTS = {
  view: 'chamber',
  band: 'infrared',                 /* PhET's own default source */
  mol: 'CO2',
  source: true, running: true, slow: false,
  anim: 'mode',                     /* mode | phet -- whose animation to draw */
  modeIdx: 0,
  showRadius: false,
  seed: 4242,
  nStat: 20000,
  statSeed: 77003,
  specReal: true,                   /* draw the real transitions under PhET's bands */
  tempK: 288,
  showWindow: true,
  camTheta: -1.2, camPhi: 0.22, zoom: 1,
};
const ST = Object.assign({}, DEFAULTS);
const MEMO = {};
function memo(name, key, fn) {
  const m = MEMO[name];
  if (m && m.key === key) return m.val;
  const val = fn();
  MEMO[name] = {key, val};
  return val;
}

/* ---- the live chamber ------------------------------------------- */
let CH = newChamber(DEFAULTS.seed, DEFAULTS.mol, DEFAULTS.band);
function chamberRebuild() {
  CH = newChamber(ST.seed, ST.mol, ST.band);
  chamberSetSource(CH, ST.source);
  STATE_HIST = [];
}
function chamberSync() {
  if (CH.mol !== ST.mol || CH.band !== ST.band) chamberRebuild();
  chamberSetSource(CH, ST.source);
}
/* the molecule's state against time, recorded by the SIMULATION rather than
   by the drawing -- a quantity built inside a draw call cannot be tested */
let STATE_HIST = [];
function stateRecord() {
  STATE_HIST.push([CH.t, CH.state]);
  while (STATE_HIST.length > 1600) STATE_HIST.shift();
}
/* one frame.  Returns true if anything moved -- the frame loop draws on it. */
function sceneStep(dt) {
  let moved = false;
  if (ST.view === 'chamber') {
    if (!ST.running) return false;
    chamberSync();
    moved = chamberStep(CH, dt, ST.slow) &&
            (CH.photons.length > 0 || CH.state !== 'idle' || CH.source);
    stateRecord();
  } else if (ST.view === 'modes') {
    if (!ST.running) return false;
    MODEPHASE += dt * 2 * Math.PI * 0.55 * (ST.slow ? PHET.SLOW_FACTOR : 1);
    moved = true;
  }
  return moved;
}
let MODEPHASE = 0;
function chamberManualStep() {
  chamberSync();
  chamberStep(CH, 1 / 60, ST.slow);
  stateRecord();
}

/* ---- derived quantities the views and the readout share ---------- */
/* PhET's response for the current molecule and band */
function phetResponse(mol, band) { return PHET_TABLE[mol][band]; }
/* the REAL answer, as far as this file can state it: does the molecule have a
   permanent dipole (so a pure rotational spectrum), an infrared-active
   fundamental, and is the photon above its lowest dissociation threshold? */
function realAnswer(mol, band) {
  const lam_nm = PHET.lam[band] * 1e9;
  const E = eVfromNm(lam_nm);
  const modes = normalModes(mol);
  const act = modes.filter(m => m.active);
  const out = {dipole: DIPOLE[mol], rot: DIPOLE[mol] > 0,
               irActive: act.length > 0, nActive: act.length,
               E, lam_nm, diss: D0_EV[mol] !== undefined && E > D0_EV[mol],
               thresh: D0_EV[mol] !== undefined ? threshNm(mol) : null,
               bands: act.map(m => m.nu)};
  /* is PhET's photon anywhere near a real transition of this molecule? */
  const nubar = PHOTON[band].nubar;
  let best = Infinity, at = null;
  for (const m of modes) { const r = Math.abs(Math.log(nubar / m.nu)); if (r < best) { best = r; at = m.nu; } }
  out.nearest = at;
  out.decades = best / Math.LN10;
  return out;
}
/* every molecule's modes, memoised, with the exact-shape checks attached */
function modeTable(mol) {
  return memo('modes' + mol, mol, () => {
    const M = normalModes(mol);
    return M.map((m, i) => Object.assign({i, um: nubarToUm(m.nu), eV: nubarToEv(m.nu),
                                          chi: inversionChi(mol, m.d)}, m));
  });
}
function currentMode() {
  const T = modeTable(ST.mol);
  return T[Math.min(ST.modeIdx, T.length - 1)];
}
/* the displacement the chamber draws: PhET's own offsets, or the normal mode */
function drawOffsets(mol, kind, phase, amp) {
  const G = PHET_GEOM[mol].atoms;
  if (kind === 'phet') return phetVibration(mol, phase);
  const T = modeTable(mol);
  if (!T.length) return G.map(() => [0, 0]);
  /* the lowest IR-active fundamental is what an infrared photon would excite */
  const act = T.filter(m => m.active);
  const m = (act.length ? act : T)[0];
  const s = Math.sin(phase) * (amp === undefined ? 55 : amp);
  return G.map((_, i) => [m.d[i] ? m.d[i][0] * s : 0, m.d[i] ? m.d[i][1] * s : 0]);
}

/* ---- the statistics view's measurements -------------------------- */
function statBlock() {
  return memo('stat', ST.statSeed + '|' + ST.nStat, () => {
    const n = ST.nStat, s = ST.statSeed;
    const k = ensembleAbsorb(s, n, PHET.P_ABSORB);
    const hold = ensembleHold(s + 1, n);
    const dir = ensembleDirection(s + 2, n, 12);
    const cw = ensembleAbsorb(s + 3, n, 0.5);
    const bias = ensembleAbsorb(s, n, 0.52);
    const seP = Math.sqrt(0.25 / n);
    const seH = ((PHET.HOLD_MAX - PHET.HOLD_MIN) / Math.sqrt(12)) / Math.sqrt(n);
    const seD = 1 / Math.sqrt(2 * n);
    /* the running absorbed fraction, for the convergence trace */
    const rng = mulberry32(s);
    const xs = [], ys = [], lo = [], hi = [];
    let acc = 0;
    const step = Math.max(1, Math.floor(n / 400));
    for (let i = 1; i <= n; i++) {
      if (rng() < PHET.P_ABSORB) acc++;
      if (i % step === 0 || i === n) {
        xs.push(i); ys.push(acc / i);
        const e = 2 * Math.sqrt(0.25 / i);
        lo.push(0.5 - e); hi.push(0.5 + e);
      }
    }
    return {n, k, f: k / n, hold, dir, cw: cw / n, bias: bias / n,
            seP, seH, seD, xs, ys, lo, hi,
            pass: Math.abs(k / n - 0.5) < 4 * seP,
            biasCaught: Math.abs(bias / n - 0.5) > 4 * seP};
  });
}

/* ---- the atmosphere view's numbers -------------------------------- */
function airBlock() {
  return memo('air', ST.tempK, () => {
    const T = ST.tempK;
    const lo = 200, hi = 2600, n = 480;
    const xs = [], ys = [];
    for (let i = 0; i <= n; i++) { const v = lo + (hi - lo) * i / n; xs.push(v); ys.push(planckNubar(v, T)); }
    const tot = planckBand(1, 6000, T, 24000);
    const win = planckBand(1e4 / WINDOW_UM[1], 1e4 / WINDOW_UM[0], T, 4000);
    /* every IR-active fundamental of the molecules the air actually carries */
    const lines = [];
    for (const mol of ['CO2', 'H2O', 'CH4', 'O3', 'N2', 'O2']) {
      for (const m of modeTable(mol)) {
        if (!m.active) continue;
        if (lines.some(l => l.mol === mol && Math.abs(l.nu - m.nu) < 0.5)) continue;
        lines.push({mol, nu: m.nu, um: nubarToUm(m.nu), sym: m.sym, what: m.what});
      }
    }
    lines.sort((a, b) => a.nu - b.nu);
    return {T, xs, ys, tot, win, wfrac: win / tot, lines,
            peak: planckPeakCm(T), peakUm: 1e4 / planckPeakCm(T),
            sb: 5.670374419e-8 * Math.pow(T, 4)};
  });
}

/* ---- the model the views draw ------------------------------------ */
function buildModel() {
  const v = ST.view, mol = ST.mol, band = ST.band;
  const M = {view: v, mol, band, ph: PHOTON[band], resp: phetResponse(mol, band),
             real: realAnswer(mol, band), modes: modeTable(mol),
             mode: currentMode(), ch: CH, phase: MODEPHASE};
  if (v === 'stats') M.stat = statBlock();
  if (v === 'air') M.air = airBlock();
  M.duty = dutyCycle();
  M.chDuty = CH.liveTime > 0 ? CH.busyTime / CH.liveTime : 0;
  M.chFrac = (CH.absorbed + CH.passed) > 0 ? CH.absorbed / (CH.absorbed + CH.passed) : 0;
  return M;
}

/* ---- readout / equation bar / tag --------------------------------- */
function hd(t) { return '<tr class="hd"><td colspan="2">' + t + '</td></tr>'; }
function row(a, b, cls) {
  return '<tr><td>' + a + '</td><td class="v' + (cls ? ' ' + cls : '') + '">' + b + '</td></tr>';
}
function readoutHTML(M) {
  const p = M.ph;
  let s = '<div class="rname">' + MOLNAME[M.mol] + ' &middot; ' + BANDNAME[M.band] + '</div><table>';
  s += hd('the photon (PhET&rsquo;s value)');
  s += row('&lambda;', sigf(p.lam * 1e9, 5) + ' nm');
  s += row('&nu;', sigf(p.nu, 5) + ' Hz');
  s += row('E', sigf(p.E_eV, 5) + ' eV');
  s += row('&nu;&#771;', sigf(p.nubar, 5) + ' cm&#8315;&#185;');
  s += row('PhET&rsquo;s own band', bandOf(p.lam) || 'in no band it draws',
           bandOf(p.lam) ? '' : 'bad');
  if (M.view === 'chamber' || M.view === 'table') {
    s += hd('PhET says');
    s += row('response', RESPNAME[M.resp], M.resp ? 'good' : '');
    s += hd('the real molecule');
    s += row('dipole moment', fmt(M.real.dipole, 3) + ' D', M.real.rot ? 'good' : '');
    s += row('rotational spectrum', M.real.rot ? 'yes' : 'no', M.real.rot ? 'good' : 'bad');
    s += row('IR-active modes', M.real.nActive + ' of ' + M.modes.length,
             M.real.irActive ? 'good' : 'bad');
    if (M.real.thresh !== null) s += row('breaks below', fmt(M.real.thresh, 1) + ' nm');
    s += row('this photon dissociates', M.real.diss ? 'yes' : 'no', M.real.diss ? 'good' : '');
    s += row('nearest real band', M.real.nearest ? fmt(M.real.nearest, 0) + ' cm&#8315;&#185;' : '&mdash;');
    s += row('decades away', M.real.nearest ? fmt(M.real.decades, 2) : '&mdash;',
             M.real.decades > 0.5 ? 'bad' : 'good');
  }
  if (M.view === 'chamber') {
    s += hd('the chamber');
    s += row('photons fired', CH.fired);
    s += row('absorbed', CH.absorbed, 'good');
    s += row('passed through', CH.passed);
    s += row('re-emitted', CH.reemitted);
    s += row('absorbed fraction', fmt(M.chFrac, 3));
    s += row('excited fraction of time', fmt(M.chDuty, 3));
    s += row('molecule now', CH.state === 'idle' ? 'waiting'
             : CH.state === 'rot' ? 'rotating' : CH.state === 'vib' ? 'vibrating'
             : CH.state === 'glow' ? 'glowing' : 'in pieces',
             CH.state === 'idle' ? '' : 'good');
  }
  if (M.view === 'modes') {
    const m = M.mode;
    s += hd('this mode (measured)');
    s += row('&nu;&#771;', fmt(m.nu, 1) + ' cm&#8315;&#185;');
    s += row('&lambda;', sigf(m.um, 4) + ' &micro;m');
    s += row('E', sigf(m.eV, 4) + ' eV');
    s += row('species', m.sym + (m.mult > 1 ? ' (&times;' + m.mult + ')' : ''));
    s += row('motion', m.what || '&mdash;');
    s += row('|&part;&mu;/&part;Q|', m.active ? sigf(m.dmu, 4) : '0 exactly',
             m.active ? 'good' : 'bad');
    s += row('infrared', m.active ? 'active' : 'inactive', m.active ? 'good' : 'bad');
    if (m.chi) s += row('character under i', (m.chi > 0 ? '+1 gerade' : '&minus;1 ungerade'));
  }
  if (M.view === 'stats') {
    const t = M.stat;
    s += hd('measured over ' + t.n + ' draws');
    s += row('absorbed fraction', fmt(t.f, 5), t.pass ? 'good' : 'bad');
    s += row('intended', fmt(PHET.P_ABSORB, 5));
    s += row('4&sigma; band', '&plusmn;' + sigf(4 * t.seP, 3));
    s += row('mean hold', fmt(t.hold.mean, 5) + ' s');
    s += row('intended', fmt(0.5 * (PHET.HOLD_MIN + PHET.HOLD_MAX), 5) + ' s');
    s += row('hold s.d.', fmt(t.hold.sd, 5) + ' s');
    s += row('&lt;cos&gt;', fmt(t.dir.cos, 5));
    s += row('&lt;sin&gt;', fmt(t.dir.sin, 5));
    s += row('&chi;&sup2; over 12 sectors', fmt(t.dir.chi2, 2));
    s += row('a p = 0.52 generator', fmt(t.bias, 5), t.biasCaught ? 'bad' : '');
  }
  if (M.view === 'air') {
    const a = M.air;
    s += hd('the surface');
    s += row('T', fmt(a.T, 0) + ' K');
    s += row('&sigma;T&#8308;', sigf(a.sb, 5) + ' W/m&sup2;');
    s += row('&pi;&int;B d&nu;&#771;', sigf(a.tot, 5) + ' W/m&sup2;');
    s += row('peak', fmt(a.peak, 1) + ' cm&#8315;&#185; = ' + fmt(a.peakUm, 2) + ' &micro;m');
    s += hd('the 8&ndash;13 &micro;m window');
    s += row('fraction of the emission', fmt(a.wfrac, 4));
    s += row('IR-active air', fmt(AIR.filter(r => r[3]).reduce((s2, r) => s2 + r[1], 0), 4) + ' %');
    s += row('transparent air', fmt(AIR.filter(r => !r[3]).reduce((s2, r) => s2 + r[1], 0), 4) + ' %');
  }
  s += '</table>';
  s += '<p class="note">PhET&rsquo;s four source wavelengths and its response table are read out of '
    + 'its build 1.5.33. Measured wavenumbers, geometries and dipole moments are NIST CCCBDB.</p>';
  return s;
}
function EQ(n, body) { return '<div class="eq"><span class="n">[' + n + ']</span>' + body + '</div>'; }
function eqbarHTML(M) {
  const v = M.view, p = M.ph;
  if (v === 'chamber')
    return '<b>E = hc/&lambda;</b> &nbsp;=&nbsp; ' + sigf(p.E_eV, 6) + ' eV at ' + sigf(p.lam * 1e9, 5)
      + ' nm<span class="sm">h and c are exact by definition, so hc/e = 1239.841984332002 eV&#8239;nm is an exact number. '
      + 'PhET absorbs a photon with probability exactly one half, holds it 1.1&ndash;1.3 s, and re-emits it in a random direction.</span>';
  if (v === 'spectrum')
    return '<b>E = hc/&lambda; = h&nu; = hc&nu;&#771;</b><span class="sm">One axis, three labels. '
      + 'PhET&rsquo;s four photons are marked on its own band diagram; the real transitions of these molecules are marked underneath.</span>';
  if (v === 'table')
    return '<b>&mu; &ne; 0 &rArr; pure rotational spectrum &nbsp;&middot;&nbsp; &part;&mu;/&part;Q &ne; 0 &rArr; infrared-active</b>'
      + '<span class="sm">Two selection rules decide the whole table. A molecule with no permanent dipole has no microwave spectrum; '
      + 'a vibration that does not change the dipole cannot absorb infrared.</span>';
  if (v === 'modes')
    return '<b>(1/&radic;(m<sub>i</sub>m<sub>j</sub>)) &part;&sup2;V/&part;x<sub>i</sub>&part;x<sub>j</sub> &middot; d = &omega;&sup2; d, '
      + '&nbsp; &nu;&#771; = &omega;/2&pi;c</b><span class="sm">The mass-weighted Hessian of a valence force field fitted to the measured '
      + 'wavenumbers. Where symmetry fixes the shape, it is written down exactly and the eigenvector is asserted against it.</span>';
  if (v === 'stats')
    return '<b>P(absorb) = &frac12; &nbsp;&middot;&nbsp; t<sub>hold</sub> ~ U(1.1, 1.3) s &nbsp;&middot;&nbsp; &theta; ~ U(0, 2&pi;)</b>'
      + '<span class="sm">PhET&rsquo;s three random rules. Measured here over ' + M.stat.n
      + ' draws of a seeded generator, against the standard error each is entitled to.</span>';
  return '<b>B<sub>&nu;&#771;</sub>(T) = 2hc&sup2;&nu;&#771;&sup3; / (e<sup>hc&nu;&#771;/kT</sup> &minus; 1)</b>'
    + '<span class="sm">Earth&rsquo;s surface at ' + fmt(M.air.T, 0) + ' K radiates here. The bands drawn on it are the measured '
    + 'infrared-active fundamentals of the gases the air carries &mdash; positions only, never strengths.</span>';
}
function tagHTML(M) {
  const v = M.view;
  if (v === 'chamber')
    return 'PhET&rsquo;s screen, rule for rule: one absorption trial per photon at p = &frac12;, a 100-unit absorption radius, '
      + 'photons at 3000 units/s from x = &minus;1350, a 0.8 s emission period, 5 Hz vibration and 1.1 Hz rotation, '
      + 'and a 0.2 s refusal window after every emission. The generator is seeded, so the run is reproducible.';
  if (v === 'spectrum')
    return 'Band edges from PhET&rsquo;s own Light Spectrum Diagram (its accessibility text states them). '
      + 'Real transition positions: NIST CCCBDB fundamentals, the CO J = 1 &larr; 0 line derived from B<sub>e</sub> and &alpha;<sub>e</sub>, '
      + 'and dissociation thresholds from QUOTED bond energies.';
  if (v === 'table')
    return 'PhET&rsquo;s table is read from its setPhotonAbsorptionStrategy calls. The real column is computed here: '
      + 'the dipole moment decides the microwave answer and &part;&mu;/&part;Q the infrared one.';
  if (v === 'modes')
    return 'Force constants fitted to the measured fundamentals in derive.py; the eigenvectors are recomputed here from '
      + 'the fitted field and asserted against the shapes symmetry alone fixes.';
  if (v === 'stats')
    return 'A seeded mulberry32, reproduced bit for bit by the Python twin. The bands are the standard errors, not fitted tolerances.';
  return 'Planck from the exact SI constants; the band positions are measured fundamentals. '
    + 'Composition: NASA Earth Fact Sheet, with NOAA GML&rsquo;s June 2026 CO&#8322; (' + fmt(CO2_PPM, 2) + ' ppm, preliminary).';
}
