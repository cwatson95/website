
/* ================================================================== *
 *  selfTest -- headless verification.  REF is refvals.json, the       *
 *  printed output of build/molecules-and-light/derive.py (the Python  *
 *  twin of every formula here, with scipy beside it), copied in by    *
 *  gen_ref.py.  "(python)" marks a value from that output, "(scipy)"  *
 *  one scipy itself produced, "(exact)" a closed form, "(PhET)" a     *
 *  constant read out of PhET's own build, "(NIST)" a measured value.  *
 * ================================================================== */
function makeShot(W, H) {
  const ops = []; let Mx = [1, 0, 0, 1, 0, 0]; const stack = [];
  const st2 = {font: '10px x', align: 'left', base: 'alphabetic'};
  const mul = (A, B) => [A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1],
                         A[0] * B[2] + A[2] * B[3], A[1] * B[2] + A[3] * B[3],
                         A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5]];
  const app = (x, y) => [Mx[0] * x + Mx[2] * y + Mx[4], Mx[1] * x + Mx[3] * y + Mx[5]];
  const fsz = () => { const m = /([\d.]+)px/.exec(st2.font); return m ? parseFloat(m[1]) : 10; };
  let pend = null;
  const ctx = {ops,
    save() { stack.push({M: Mx.slice(), f: st2.font, a: st2.align, b: st2.base}); },
    restore() { const s = stack.pop(); if (s) { Mx = s.M; st2.font = s.f; st2.align = s.a; st2.base = s.b; } },
    translate(x, y) { Mx = mul(Mx, [1, 0, 0, 1, x, y]); },
    rotate(r) { const c = Math.cos(r), s3 = Math.sin(r); Mx = mul(Mx, [c, s3, -s3, c, 0, 0]); },
    scale(x, y) { Mx = mul(Mx, [x, 0, 0, y, 0, 0]); },
    setTransform() { Mx = [1, 0, 0, 1, 0, 0]; },
    beginPath() { pend = null; }, moveTo() { if (!pend) pend = {n: 0}; }, lineTo() { if (!pend) pend = {n: 0}; },
    closePath() {}, rect() { if (!pend) pend = {n: 0}; pend.n++; }, arc() { if (!pend) pend = {n: 0}; pend.n++; },
    fill() { if (pend) ops.push({op: 'fill', n: pend.n || 1, style: ctx.fillStyle}); },
    stroke() { ops.push({op: 'stroke', style: ctx.strokeStyle}); }, clip() {},
    fillRect(x, y, w, hh) {
      const c = app(x, y), d = app(x + w, y + hh);
      ops.push({op: 'fill', n: 1, bb: [Math.min(c[0], d[0]), Math.min(c[1], d[1]),
                                       Math.max(c[0], d[0]), Math.max(c[1], d[1])], style: ctx.fillStyle});
    },
    strokeRect() { ops.push({op: 'stroke', style: ctx.strokeStyle}); }, clearRect() {},
    fillText(t, x, y) {
      const w = ('' + t).length * fsz() * 0.52, fh = fsz() * 1.15;
      const lx = st2.align === 'center' ? x - w / 2 : (st2.align === 'right' ? x - w : x);
      const ly = st2.base === 'top' ? y : (st2.base === 'middle' ? y - fh / 2 : (st2.base === 'bottom' ? y - fh : y - fh * 0.8));
      const cs = [[lx, ly], [lx + w, ly], [lx, ly + fh], [lx + w, ly + fh]].map(c2 => app(c2[0], c2[1]));
      const xs = cs.map(c2 => c2[0]), ys = cs.map(c2 => c2[1]);
      ops.push({op: 'text', t: '' + t, bb: [Math.min.apply(0, xs), Math.min.apply(0, ys),
                                            Math.max.apply(0, xs), Math.max.apply(0, ys)]});
    },
    strokeText() {}, setLineDash() {},
    measureText(t) { return {width: ('' + t).length * fsz() * 0.52}; },
    createLinearGradient() { return {addColorStop() {}}; },
  };
  Object.defineProperty(ctx, 'font', {get: () => st2.font, set: v => { st2.font = v; }});
  Object.defineProperty(ctx, 'textAlign', {get: () => st2.align, set: v => { st2.align = v; }});
  Object.defineProperty(ctx, 'textBaseline', {get: () => st2.base, set: v => { st2.base = v; }});
  ctx.fillStyle = '#000'; ctx.strokeStyle = '#000'; ctx.lineWidth = 1;
  ctx.lineCap = 'butt'; ctx.lineJoin = 'miter'; ctx.globalAlpha = 1;
  return ctx;
}

function selfTest() {
  const T0 = Date.now();
  let pass = 0, fail = 0;
  function ok(c, n) { if (c) pass++; else { fail++; console.log('FAIL — ' + n); } }
  function close(a, b, tol, n) {
    const d = Math.abs(a - b);
    ok(isFinite(d) && d <= tol, n + '  (' + a + ' vs ' + b + ', |d| ' + d + ' > ' + tol + ')');
  }
  function rel(a, b, rt, n) {
    const d = Math.abs(a - b) / Math.max(1e-300, Math.abs(b));
    ok(isFinite(d) && d <= rt, n + '  (' + a + ' vs ' + b + ', rel ' + d + ' > ' + rt + ')');
  }
  const stSave = Object.assign({}, ST);
  function withState(o, fn) {
    const s = Object.assign({}, ST);
    Object.assign(ST, o);
    try { fn(); } finally { Object.assign(ST, s); }
  }
  function resetAll() {
    Object.assign(ST, DEFAULTS);
    for (const k in MEMO) delete MEMO[k];
    chamberRebuild();
    MODEPHASE = 0;
  }
  resetAll();

  /* ================= 1. the exact photon arithmetic ================= */
  close(PLANCK_H, 6.62607015e-34, 0, '(exact) h is the 2019 SI value, exactly');
  close(LIGHT_C, 299792458, 0, '(exact) c is the 2019 SI value, exactly');
  close(ELEM_Q, 1.602176634e-19, 0, '(exact) e is the 2019 SI value, exactly');
  close(BOLTZ_K, 1.380649e-23, 0, '(exact) k is the 2019 SI value, exactly');
  rel(HC_JM, REF.HC_Jm, 1e-15, '(python) hc');
  rel(HC_EV_NM, REF.HC_eV_nm, 1e-15, '(python) hc/e in eV nm');
  rel(HC_EV_NM, 1239.841984332002, 1e-15, '(exact) hc/e = 1239.841984332002 eV nm');
  rel(U_KG, REF.U_KG, 1e-11, '(scipy) the atomic mass constant');
  for (const bd of BANDS) {
    const p = PHOTON[bd], r = REF_PHOTONS[bd];
    rel(p.lam, r.lam_m, 1e-15, '(PhET) ' + bd + ' wavelength');
    rel(p.nu, r.nu_Hz, 1e-15, '(python) ' + bd + ' frequency');
    rel(p.E_eV, r.E_eV, 1e-14, '(python) ' + bd + ' energy in eV');
    rel(p.nubar, r.nubar_cm, 1e-14, '(python) ' + bd + ' wavenumber');
    /* the same energy by the identity the file prints -- a second route */
    rel(eVfromNm(p.lam * 1e9), p.E_eV, 1e-14, '(exact) ' + bd + ': hc/e / lambda reaches the same energy');
    rel(nubarToEv(p.nubar), p.E_eV, 1e-13, '(exact) ' + bd + ': hc nubar reaches the same energy');
  }
  rel(PHOTON.ultraviolet.E_eV, 12.39841984332, 1e-12, '(exact) 100 nm is 12.398 eV');
  /* the micrometre conversion: 1e4 / nubar.  Only the readout and the canvas
     print it, so pin it by ROUND-TRIPPING through photonOf, which reaches a
     wavenumber from a wavelength in metres by a different route entirely. */
  rel(nubarToUm(667), 14.99250374812594, 1e-13, '(exact) the CO2 bend is at 14.99 um');
  for (const nub of [667, 1595, 2349, 3756, 0.05]) {
    rel(photonOf(nubarToUm(nub) * 1e-6).nubar, nub, 1e-12,
        '(exact) um and cm-1 round-trip at ' + nub + ' cm-1');
    rel(nubarToUm(nub) * 1e-4, 1 / nub, 1e-13, 'and um x 1e-4 is the wavelength in cm');
  }
  rel(PHOTON.microwave.E_eV, REF['phet_micro_eV'], 1e-13, '(python) the microwave photon is 6.2 micro-eV');
  rel(PHOTON.infrared.E_eV / nubarToEv(667), REF['phet_ir_over_CO2bend'], 1e-12,
      "(python) PhET's IR photon is 17.6x the CO2 bend quantum");
  ok(PHOTON.infrared.E_eV > 17 * nubarToEv(667),
     "PhET's 850 nm photon carries more than seventeen CO2 bend quanta");

  /* ================= 2. PhET's own band diagram ===================== */
  ok(PHET_BANDS.length === 7, '(PhET) the Light Spectrum Diagram has seven bands');
  ok(bandOf(PHET.lam.infrared) === 'infrared', "(PhET) the 850 nm photon is in PhET's infrared band");
  ok(bandOf(PHET.lam.visible) === 'visible', "(PhET) the 580 nm photon is in PhET's visible band");
  ok(bandOf(PHET.lam.ultraviolet) === 'ultraviolet', "(PhET) the 100 nm photon is in PhET's ultraviolet band");
  ok(bandOf(PHET.lam.microwave) === null,
     "(PhET) the 0.2 m photon is in NO band of PhET's own diagram -- it falls in the 0.5-0.1 m gap");
  ok(bandOf(0.05) === 'microwave' && bandOf(1.0) === 'radio',
     'the band finder still works either side of that gap');
  ok(bandOf(1e-20) === null, 'a wavelength off the end of the diagram belongs to no band');

  /* ================= 3. PhET's model constants ====================== */
  close(PHET.P_ABSORB, 0.5, 0, '(PhET) the absorption probability is one half');
  close(PHET.HOLD_MIN, 1.1, 0, '(PhET) the hold time starts at 1.1 s');
  close(PHET.HOLD_MAX, 1.3, 0, '(PhET) the hold time ends at 1.3 s');
  close(PHET.HYSTERESIS, 0.2, 0, '(PhET) the refusal window after an emission is 0.2 s');
  close(PHET.ABSORB_RADIUS, 100, 0, '(PhET) the absorption radius is 100 model units');
  close(PHET.PHOTON_SPEED, 3000, 0, '(PhET) photons travel at 3000 units per second');
  close(PHET.EMITTER_X, -1350, 0, '(PhET) the emitter sits at x = -1350');
  close(PHET.EMIT_PERIOD, 0.8, 0, '(PhET) the continuous emission period is 0.8 s');
  close(PHET.VIB_HZ, 5, 0, '(PhET) the vibration runs at 5 Hz');
  close(PHET.ROT_HZ, 1.1, 0, '(PhET) the rotation runs at 1.1 Hz');
  close(PHET.SLOW_FACTOR, 0.5, 0, '(PhET) slow motion halves the step');
  close(PHET.DT_CEILING, 0.2, 0, '(PhET) a frame longer than 0.2 s is discarded whole');
  close(PHET.FRAG_A, 990, 0, '(PhET) the heavy fragment leaves at 990');
  close(PHET.FRAG_B, 2010, 1e-12, '(PhET) the light fragment leaves at 0.67 x 3000');
  close(PHET_ATOM.O.m, 12.011, 0, "(PhET) PhET's oxygen mass is 12.011 -- carbon's, a copy-paste in its source");
  close(PHET_ATOM.C.m, 12.011, 0, '(PhET) and its carbon mass is the same number');
  close(CO2_SB, 20, 1e-12, "(PhET) so its CO2 bend amplitude ratio comes out exactly 20");
  rel(40 / CO2_SB, REF['PHET.CO2_bend_ratio'], 1e-12, "(python) PhET draws the bend at |C|/|O| = 2");
  rel(2 * MASS.O / MASS.C, REF.CO2_bend_ratio_true, 1e-14, '(python) the true ratio is 2 m_O/m_C = 2.6658');
  ok(Math.abs(2 * MASS.O / MASS.C - 40 / CO2_SB) > 0.6,
     "PhET's drawn ratio and the true one differ by more than 0.6 -- not a rounding");
  close(REF['flight_time_s'], 0.45, 1e-12, '(python) a photon takes 0.45 s to reach the molecule');
  close(Math.abs(PHET.EMITTER_X) / PHET.PHOTON_SPEED, REF['flight_time_s'], 1e-15, 'and this file agrees');

  /* ================= 4. PhET's response table ======================= */
  { let n = 0;
    for (const m of MOLORDER) for (const b of BANDS) if (PHET_TABLE[m][b]) n++;
    ok(n === REF['PHET.table_responses'], '(python) PhET registers ' + REF['PHET.table_responses']
       + ' responses in 32 cells (' + n + ')');
  }
  ok(MOLORDER.length === 8, '(PhET) eight molecules');
  ok(PHET_TABLE.N2.microwave === '' && PHET_TABLE.N2.infrared === '' &&
     PHET_TABLE.N2.visible === '' && PHET_TABLE.N2.ultraviolet === '',
     '(PhET) nitrogen answers nothing at all');
  ok(PHET_TABLE.O2.ultraviolet === '', '(PhET) and neither does oxygen, even in the ultraviolet');
  ok(PHET_TABLE.NO2.visible === 'glow' && PHET_TABLE.NO2.ultraviolet === 'break',
     '(PhET) NO2 glows in the visible and breaks in the ultraviolet');
  ok(PHET_TABLE.O3.visible === '' && PHET_TABLE.O3.ultraviolet === 'break',
     '(PhET) O3 passes the visible and breaks in the ultraviolet');
  ok(PHET_TABLE.CO2.microwave === '' && PHET_TABLE.CO.microwave === 'rotate',
     '(PhET) CO2 has no microwave response and CO does');

  /* ================= 5. the measured spectroscopy =================== */
  close(VIB.CO2[1][0], 667, 0, '(NIST) the CO2 bend is at 667 cm-1');
  close(VIB.CO2[2][0], 2349, 0, '(NIST) the CO2 antisymmetric stretch is at 2349 cm-1');
  close(VIB.H2O[1][0], 1595, 0, '(NIST) the water bend is at 1595 cm-1');
  close(GEOM.H2O.ang, 104.4776, 0, '(NIST) the water bond angle is 104.4776 degrees');
  close(GEOM.CO2.ang, 180, 0, '(NIST) CO2 is linear');
  /* Every measured bond length, pinned ABSOLUTELY.  A mutation sweep flagged
     CO2's as a survivor, and it is right to: with the force field fitted in
     the coordinates r*dtheta and (|r| - r_e), the bond LENGTH cancels out of
     every wavenumber and every mode shape this file computes, so no amount of
     spectroscopy can see it.  A parameter that cancels out of everything you
     check needs an absolute pin AND a deliberate statement of the invariance
     (Known-bad, drum_head's radius and areal density). */
  close(GEOM.CO2.r, 1.162, 0, '(NIST) the measured C=O bond length is 1.162 A');
  close(GEOM.H2O.r, 0.958, 0, '(NIST) the measured O-H bond length is 0.958 A');
  close(GEOM.O3.r, 1.278, 0, '(NIST) the measured O-O bond length in ozone is 1.278 A');
  close(GEOM.NO2.r, 1.193, 0, '(NIST) the measured N-O bond length is 1.193 A');
  close(GEOM.CH4.r, 1.087, 0, '(NIST) the measured C-H bond length is 1.087 A');
  close(GEOM.O3.ang, 116.8, 0, '(NIST) the ozone bond angle is 116.8 degrees');
  close(GEOM.NO2.ang, 134.1, 0, '(NIST) the NO2 bond angle is 134.1 degrees');
  close(GEOM.CH4.ang, 109.471, 0, '(NIST) the methane bond angle is 109.471 degrees');
  { /* and the invariance itself, stated rather than left as a blind spot */
    const r0 = GEOM.CO2.r, nu0 = normalModes('CO2').map(m => m.nu);
    GEOM.CO2.r = r0 * 1.03;
    delete MODE_CACHE.CO2;
    const nu1 = normalModes('CO2').map(m => m.nu);
    GEOM.CO2.r = r0;
    delete MODE_CACHE.CO2;
    let worst = 0;
    for (let i = 0; i < nu0.length; i++) worst = Math.max(worst, Math.abs(nu1[i] - nu0[i]) / nu0[i]);
    /* the residual is the finite-difference step, which is ABSOLUTE (2e-4 A)
       while the geometry was rescaled, so h/r moved by 3 % and the O(h^2)
       truncation with it: (2e-4/1.162)^2 = 3e-8, which is the size seen. */
    ok(worst < 5e-8, '(exact) CO2\u2019s wavenumbers are invariant to its bond length by construction, to '
       + worst.toExponential(2) + ' -- the fitted field lives in r*dtheta and |r| - r_e, and the '
       + 'residual is the fixed finite-difference step against a rescaled geometry');
    ok(normalModes('CO2').map(m => m.nu).join() === nu0.join(),
       'and the cache is back where it started');
  }
  close(DIPOLE.H2O, 1.857, 0, '(NIST) water has a dipole moment of 1.857 D');
  close(DIPOLE.CO2, 0, 0, '(NIST) CO2 has none');
  close(MASS.C, 12, 0, '(NIST) carbon-12 is 12 exactly, by definition of the scale');
  rel(MASS.O, 15.99491461957, 1e-15, '(NIST) oxygen-16');
  for (const m of ['CO', 'N2', 'O2']) {
    const d = DIATOMIC[m];
    rel(BeFromGeometry(m), REF['Be_from_geometry.' + m], 1e-12, '(python) B_e from the geometry of ' + m);
    const asBe = Math.abs(BeFromGeometry(m) - d.Bprint) / d.Bprint;
    const asB0 = Math.abs(BeFromGeometry(m) - d.ae / 2 - d.Bprint) / d.Bprint;
    rel(asBe, REF['Be_rel_if_read_as_Be.' + m], 1e-9, '(python) ' + m + ': the residual reading it as B_e');
    rel(asB0, REF['Be_rel_if_read_as_B0.' + m], 1e-9, '(python) ' + m + ': the residual reading it as B_0');
    if (d.bracketed) ok(asB0 < 3e-5 && asBe > 100 * asB0,
      '(NIST) O2’s bracketed constant is B_0, not B_e -- reading it as B_0 is '
      + Math.round(asBe / asB0) + 'x better');
    else ok(asBe < 1e-6 && asB0 > 100 * asBe,
      '(NIST) ' + m + '’s unbracketed constant is B_e -- reading it as B_e is '
      + Math.round(asB0 / asBe) + 'x better');
  }
  { const B0 = DIATOMIC.CO.Bprint - DIATOMIC.CO.ae / 2;
    rel(B0, REF.CO_B0_cm, 1e-9, '(python) CO B_0');
    rel(2 * B0 * C_CM / 1e9, REF.CO_J10_GHz, 1e-9, '(python) the CO J = 1 <- 0 line in GHz');
    rel(2 * B0 * C_CM / 1e9, 115.2712018, 3e-5,
        '(NIST) it lands on the 115.2712018 GHz rest frequency to 6e-6 -- the residual is -4 D_0');
    ok(2 * B0 * C_CM / 1e9 > 115.2712018,
       'and it lands ABOVE it, which is the sign centrifugal distortion must have');
  }
  for (const m of ['CO', 'N2', 'O2']) {
    const d = DIATOMIC[m];
    close(d.we - 2 * d.wexe, VIB[m][0][0], 4,
          '(NIST) ' + m + ': we - 2 wexe reproduces the printed fundamental');
  }
  rel(diatomicK('CO'), REF['k_Nm.CO'], 1e-11, '(python) the CO force constant, N/m');
  rel(diatomicK('N2'), REF['k_Nm.N2'], 1e-11, '(python) the N2 force constant, N/m');
  ok(diatomicK('N2') > diatomicK('CO') && diatomicK('CO') > diatomicK('O2'),
     'the triple bonds are stiffer than the double one');
  for (const m in D0_EV) rel(threshNm(m), REF_THRESH[m], 1e-11, '(python) the ' + m + ' threshold in nm');
  rel(threshNm('NO2'), 397.857069067, 1e-9, '(python) NO2 dissociates below 398 nm');
  ok(PHOTON.ultraviolet.E_eV > Math.max.apply(null, MOLORDER.map(m => D0_EV[m] || 0)),
     "PhET's 100 nm photon is above EVERY bond energy here, N2's 9.75 eV included");

  /* ================= 6. the normal modes ============================ */
  ok(Math.abs(CONV_S2 - REF.CONV_s2) / REF.CONV_s2 < 1e-11, '(python) the aJ/(A^2 u) -> s^-2 conversion');
  for (const mol of MOLORDER) {
    const T = modeTable(mol);
    const nat = geomXY(mol).sym.length;
    const want = 3 * nat - ((GEOM[mol].ang === null || Math.abs(GEOM[mol].ang - 180) < 1e-9) ? 5 : 6);
    ok(T.length === want, mol + ' has 3N - ' + (3 * nat - want) + ' = ' + want + ' vibrations (' + T.length + ')');
    /* every wavenumber is the measured one */
    for (const row of VIB[mol]) {
      const got = T.filter(o => Math.abs(o.nu - row[0]) < 0.02);
      ok(got.length === row[3], '(NIST) ' + mol + ': ' + row[0] + ' cm-1 appears with multiplicity '
         + row[3] + ' (' + got.length + ')');
    }
    /* momentum and angular momentum, on every mode */
    const g = geomXY(mol);
    let wp = 0, wl = 0;
    for (const o of T) {
      const p = [0, 0, 0];
      for (let i = 0; i < g.m.length; i++) for (let k = 0; k < 3; k++) p[k] += g.m[i] * o.d[i][k];
      for (const c of p) wp = Math.max(wp, Math.abs(c));
      const L = [0, 0, 0];
      for (let i = 0; i < g.m.length; i++) {
        const r = g.X[i], dd = o.d[i], mm = g.m[i];
        L[0] += mm * (r[1] * dd[2] - r[2] * dd[1]);
        L[1] += mm * (r[2] * dd[0] - r[0] * dd[2]);
        L[2] += mm * (r[0] * dd[1] - r[1] * dd[0]);
      }
      for (const c of L) wl = Math.max(wl, Math.abs(c));
    }
    ok(wp < 1e-9, mol + ': every mode conserves linear momentum (' + wp.toExponential(2) + ')');
    ok(wl < 1e-8, mol + ': every mode conserves angular momentum (' + wl.toExponential(2) + ')');
  }
  /* the JS eigenvectors against the Python twin's, mode for mode */
  for (const mol in REF_MODES) {
    const T = modeTable(mol), R = REF_MODES[mol];
    ok(T.length === R.nu.length, '(python) ' + mol + ' has the twin’s mode count');
    let worst = 0;
    for (let i = 0; i < T.length; i++) worst = Math.max(worst, Math.abs(T[i].nu - R.nu[i]));
    ok(worst < 2e-3, '(python) ' + mol + ' wavenumbers match the twin to ' + worst.toExponential(2) + ' cm-1');
  }
  /* the shapes symmetry alone fixes */
  { const T = modeTable('CO2'), ex = 2 * MASS.O / MASS.C;
    const sym = T.filter(o => Math.abs(o.d[1][0]) < 1e-7 && Math.abs(o.d[0][0]) > 0.5)[0];
    const asy = T.filter(o => Math.abs(o.d[1][0]) > 0.1)[0];
    const bnd = T.filter(o => Math.abs(o.d[0][1]) > 0.1)[0];
    ok(!!sym && !!asy && !!bnd, 'CO2’s three distinct modes are all identifiable by their shape');
    close(sym.nu, 1333, 0.02, '(NIST) the symmetric stretch is 1333 cm-1');
    close(asy.nu, 2349, 0.02, '(NIST) the antisymmetric stretch is 2349 cm-1');
    close(bnd.nu, 667, 0.02, '(NIST) the bend is 667 cm-1');
    close(Math.abs(sym.d[1][0]), 0, 1e-12,
          '(exact) in the symmetric stretch the carbon is EXACTLY at rest');
    close(Math.abs(sym.d[1][1]) + Math.abs(sym.d[1][2]), 0, 1e-12, 'and it does not move sideways either');
    close(Math.abs(sym.d[0][0]) - Math.abs(sym.d[2][0]), 0, 1e-12, 'and the two oxygens move equally');
    rel(asy.d[1][0] / asy.d[0][0], -ex, 1e-9,
        '(exact) the antisymmetric stretch is (1, -2 m_O/m_C, 1)');
    rel(bnd.d[1][1] / bnd.d[0][1], -ex, 1e-9, '(exact) and so is the bend, in the perpendicular direction');
    rel(asy.d[1][0] / asy.d[0][0], REF.CO2_asym_ratio, 1e-9, '(python) the same ratio as the twin');
    /* the closed forms this file writes down, against the eigenvectors */
    /* ALL THREE branches of linearExact, against the three eigenvectors.  The
       'sym' and 'bend' branches were reached by no assertion at all until a
       mutant on the symmetric stretch survived a sweep. */
    for (const [which, mode, comp] of [['asym', asy, 0], ['sym', sym, 0], ['bend', bnd, 1]]) {
      const le = linearExact('CO2', which);
      let w2 = 0;
      const ref = mode.d[0][comp] || mode.d[2][comp];
      const s2 = Math.sign(ref) * Math.sign(le[0][comp] || le[2][comp]);
      for (let i = 0; i < 3; i++) w2 = Math.max(w2, Math.abs(s2 * mode.d[i][comp] - le[i][comp]));
      ok(w2 < 1e-9, "(exact) linearExact('" + which + "') reproduces the computed mode ("
         + w2.toExponential(2) + ')');
    }
    ok(Math.abs(linearExact('CO2', 'sym')[0][0] + linearExact('CO2', 'sym')[2][0]) < 1e-15,
       '(exact) and its symmetric stretch really is antisymmetric in the two oxygens');
  }
  for (const mol of ['H2O', 'O3', 'NO2']) {
    const T = modeTable(mol), ex = bentB2Exact(mol);
    const b2 = T.filter(o => Math.abs(o.d[1][1]) < 1e-7 && Math.abs(o.d[1][0]) > 1e-3)[0];
    ok(!!b2, mol + ': the B2 antisymmetric stretch is identifiable (central atom moves only along x)');
    if (b2) {
      const sg = Math.sign(b2.d[0][0]);
      let e = 0;
      for (let i = 0; i < 3; i++) for (let k = 0; k < 3; k++) e = Math.max(e, Math.abs(sg * b2.d[i][k] - ex[i][k]));
      ok(e < 1e-8, '(exact) ' + mol + ': the B2 shape is cot(theta/2) and -2m_Y/m_X, to '
         + e.toExponential(2));
      ok(e < REF['B2_exact_vs_numeric.' + mol] * 1e7 + 1e-8,
         '(python) ' + mol + ': the same agreement the twin found');
      close(b2.nu, VIB[mol][2][0], 0.02, '(NIST) ' + mol + ': and it is the measured nu3');
    }
    /* the exact shape must DEPEND on the bond angle -- otherwise nothing pins it */
    const cotA = 1 / Math.tan(GEOM[mol].ang * Math.PI / 360);
    rel(Math.abs(ex[0][1] / ex[0][0]) * (Math.abs(ex[0][0]) > 0.5 ? 1 : 0) + (Math.abs(ex[0][0]) > 0.5 ? 0 : cotA),
        cotA, 1e-12, '(exact) ' + mol + ': the perpendicular/parallel ratio is cot(theta/2) = ' + fmt(cotA, 6));
  }
  { const T = modeTable('CH4');
    const mult = [];
    for (let i = 0; i < T.length; i++) if (i === 0 || Math.abs(T[i - 1].nu - T[i].nu) > 0.5) mult.push(T[i].mult);
    ok(mult.join(',') === '3,1,2,3',
       '(exact) CH4’s degeneracies in descending wavenumber are T2, A1, E, T2 = 3,1,2,3 (' + mult.join(',') + ')');
  }
  /* the numerical machinery itself */
  { const A = [[2, 1, 0], [1, 3, 1], [0, 1, 4]];
    const {val} = jacobiEig(A);
    const sv = val.slice().sort((a, b) => a - b);
    const tr = A[0][0] + A[1][1] + A[2][2];
    close(sv[0] + sv[1] + sv[2], tr, 1e-12, 'jacobiEig conserves the trace');
    close(sv[0] * sv[1] * sv[2], 2 * (3 * 4 - 1) - 1 * (1 * 4 - 0), 1e-11, 'and the determinant');
    ok(sv[0] > 1.2 && sv[0] < 1.4, 'and its smallest eigenvalue is where it should be (' + sv[0] + ')');
  }
  { /* the Eckart basis really does span the rigid motions */
    const {sym, X} = geomXY('H2O');
    const B = eckartBasis(sym, X);
    ok(B.length === 6, 'a bent triatomic has six rigid motions (' + B.length + ')');
    ok(eckartBasis(geomXY('CO2').sym, geomXY('CO2').X).length === 5,
       'and a linear one has five -- the rotation about the axis is identically zero');
    let worst = 0;
    for (let i = 0; i < B.length; i++) for (let j = 0; j < B.length; j++) {
      let d = 0;
      for (let k = 0; k < B[i].length; k++) d += B[i][k] * B[j][k];
      worst = Math.max(worst, Math.abs(d - (i === j ? 1 : 0)));
    }
    ok(worst < 1e-12, 'the Eckart basis is orthonormal (' + worst.toExponential(2) + ')');
  }
  { /* the linear bend coordinate: 2(1+cos) must be the harmonic form */
    const f = FIELDS.CO2, g = geomXY('CO2');
    const V0 = potentialV('CO2', g.X, f);
    close(V0, 0, 1e-16, 'the equilibrium geometry is a stationary point of zero energy');
    const bend = e => {
      const X = g.X.map(p => p.slice());
      X[1][1] += e; X[0][1] -= e * MASS.C / (2 * MASS.O); X[2][1] -= e * MASS.C / (2 * MASS.O);
      return potentialV('CO2', X, f);
    };
    rel(bend(2e-3) / bend(1e-3), 4, 2e-3, 'the bend potential is quadratic in the displacement');
    const str = e => {
      const X = g.X.map(p => p.slice());
      X[0][0] -= e; X[2][0] += e;
      return potentialV('CO2', X, f);
    };
    rel(str(2e-3) / str(1e-3), 4, 1e-6, 'and so is the stretch');
  }

  /* ================= 7. the infrared selection rule ================== */
  { let nz = 0, nact = 0, worstZero = 0, weakest = Infinity;
    for (const mol of ['CO', 'N2', 'O2', 'NO', 'CO2', 'H2O', 'O3', 'NO2', 'CH4']) {
      for (const m of normalModes(mol)) {
        if (m.active) { nact++; weakest = Math.min(weakest, m.dmu); }
        else { nz++; worstZero = Math.max(worstZero, m.dmu, m.dmu2); }
      }
    }
    ok(nz === REF.n_inactive_modes, '(python) ' + REF.n_inactive_modes + ' inactive modes over nine molecules (' + nz + ')');
    ok(nact === REF.n_active_modes, '(python) ' + REF.n_active_modes + ' active ones (' + nact + ')');
    ok(worstZero < 1e-12, '(exact) every inactive mode gives |dmu/dQ| = 0 to ' + worstZero.toExponential(2)
       + ', at BOTH charge scales -- the zero is the shape, not the charge');
    ok(weakest > 0.1, 'and no active mode is anywhere near zero (weakest ' + weakest.toExponential(3) + ')');
  }
  { /* the inversion character, an independent route, on every centrosymmetric mode */
    let checked = 0, bad = null;
    for (const mol of ['N2', 'O2', 'CO2']) {
      for (const m of normalModes(mol)) {
        const chi = inversionChi(mol, m.d);
        if (!chi) { bad = mol + ' mode ' + m.nu + ' has no definite character'; continue; }
        checked++;
        if ((chi < 0) !== m.active) bad = mol + ' ' + m.nu + ': chi=' + chi + ' but active=' + m.active;
      }
    }
    ok(checked === 6, 'six centrosymmetric modes carry a definite inversion character (' + checked + ')');
    ok(!bad, '(exact) gerade means infrared-inactive and ungerade means active, on every one (' + (bad || 'ok') + ')');
    ok(inversionChi('CO', normalModes('CO')[0].d) === 0,
       'and a heteronuclear diatomic has no inversion centre to test');
  }
  { /* PhET's two columns ARE the two selection rules */
    let rotOk = true, irOk = true;
    for (const mol of MOLORDER) {
      const hasMu = DIPOLE[mol] > 0;
      const hasIR = normalModes(mol).some(m => m.active);
      if ((PHET_TABLE[mol].microwave === 'rotate') !== hasMu) rotOk = false;
      if ((PHET_TABLE[mol].infrared === 'vibrate') !== hasIR) irOk = false;
    }
    ok(rotOk, "(exact) PhET's microwave column is exactly the permanent-dipole column");
    ok(irOk, "(exact) PhET's infrared column is exactly the infrared-active column");
    ok(REF.n_IR_active_molecules === 6, '(python) six of the eight have an IR-active mode');
    ok(REF.n_microwave_active === 4, '(python) four of the eight have a permanent dipole');
  }

  /* ================= 8. the seeded generator ======================== */
  { const r = mulberry32(20260922);
    for (let i = 0; i < REF_RNG_FIRST.length; i++)
      rel(r(), REF_RNG_FIRST[i], 1e-15, '(python) mulberry32 draw ' + i + ' matches the twin bit for bit');
  }
  { const r = mulberry32(20260922);
    let s = 0, s2 = 0, lo = 1, hi = 0;
    for (let i = 0; i < REF_N_STAT; i++) { const v = r(); s += v; s2 += v * v; lo = Math.min(lo, v); hi = Math.max(hi, v); }
    rel(s / REF_N_STAT, REF.mulberry_mean, 1e-13, '(python) the mean of 20000 draws');
    rel(s2 / REF_N_STAT - (s / REF_N_STAT) * (s / REF_N_STAT), REF.mulberry_var, 1e-11, '(python) and the variance');
    ok(lo >= 0 && hi < 1, 'every draw is in [0, 1)');
    close(REF.mulberry_var, 1 / 12, 3e-4, 'which is 1/12 to 3e-4, as a uniform must be');
  }
  { const k = ensembleAbsorb(77003, REF_N_STAT, PHET.P_ABSORB);
    ok(k === REF_STAT.absorbed_count, '(python) the absorbed count is identical to the twin’s ('
       + k + ' vs ' + REF_STAT.absorbed_count + ')');
    ok(Math.abs(k / REF_N_STAT - 0.5) < 4 * Math.sqrt(0.25 / REF_N_STAT),
       '(scipy) and it is inside the 4-sigma binomial band');
    const bad = ensembleAbsorb(77003, REF_N_STAT, 0.52);
    rel(bad / REF_N_STAT, REF_STAT.biased_fraction, 1e-15, '(python) a p = 0.52 generator reads 0.52025');
    ok(Math.abs(bad / REF_N_STAT - 0.5) > 4 * Math.sqrt(0.25 / REF_N_STAT),
       '(scipy) and the SAME test rejects it -- the test has teeth');
  }
  { const hRes = ensembleHold(77004, REF_N_STAT);
    rel(hRes.mean, REF_STAT.hold_mean, 1e-14, '(python) the mean hold time');
    /* the twin uses numpy's two-pass variance and this file the one-pass form,
       so the two agree to the cancellation floor, not to machine precision */
    rel(hRes.sd, REF_STAT.hold_sd, 1e-10, '(python) and its standard deviation');
    const se = ((PHET.HOLD_MAX - PHET.HOLD_MIN) / Math.sqrt(12)) / Math.sqrt(REF_N_STAT);
    ok(Math.abs(hRes.mean - 1.2) < 4 * se, '(scipy) the mean is inside 4 standard errors of 1.2');
    rel(hRes.sd, (PHET.HOLD_MAX - PHET.HOLD_MIN) / Math.sqrt(12), 3e-3,
        'and the spread is (b - a)/sqrt(12), which is what uniform means');
  }
  { const d = ensembleDirection(77005, REF_N_STAT, 12);
    rel(d.cos, REF_STAT.emission_mean_cos, 1e-13, '(python) <cos> over 20000 emission directions');
    rel(d.sin, REF_STAT.emission_mean_sin, 1e-13, '(python) and <sin>');
    rel(d.chi2, REF_STAT.emission_chi2, 1e-11, '(python) and the 12-sector chi-square');
    const se = 1 / Math.sqrt(2 * REF_N_STAT);
    ok(Math.abs(d.cos) < 4 * se && Math.abs(d.sin) < 4 * se, '(scipy) both moments are inside 4 standard errors of 0');
    ok(d.chi2 < REF.emission_chi2_crit, '(scipy) and chi-square is under the 99.9 % point ' + fmt(REF.emission_chi2_crit, 2));
    ok(d.bins.reduce((a, b) => a + b, 0) === REF_N_STAT, 'every direction landed in a sector');
  }
  { /* a generator with structure must FAIL the chi-square, or it tests nothing */
    const bins = new Array(12).fill(REF_N_STAT / 12);
    bins[0] += 400; bins[6] -= 400;
    let c2 = 0;
    for (const b of bins) c2 += (b - REF_N_STAT / 12) * (b - REF_N_STAT / 12) / (REF_N_STAT / 12);
    ok(c2 > REF.emission_chi2_crit, 'a 2 % excess in one sector is rejected by the same chi-square (' + fmt(c2, 1) + ')');
  }

  /* ================= 9. the chamber, by PhET's rules ================= */
  { /* one trial per photon, and exactly one half */
    let nTrial = 0;
    const ch = newChamber(5, 'CO2', 'infrared');
    const p = {x: -60, y: 0, vx: 0, vy: 0, band: 'infrared', pass: false};
    const r0 = ch.rng;
    ch.rng = () => { nTrial++; return r0(); };
    for (let i = 0; i < 8; i++) chamberQuery(ch, p);
    ok(nTrial <= 2, 'a photon inside the radius draws the generator at most twice, however many frames it is there ('
       + nTrial + ')');
    ok(p.pass || ch.state !== 'idle', 'and it ends either absorbed or marked to pass through');
  }
  { /* a busy molecule refuses without a trial at all */
    const ch = newChamber(7, 'CO2', 'infrared');
    ch.state = 'vib'; ch.hold = 1;
    let drew = 0;
    const r0 = ch.rng;
    ch.rng = () => { drew++; return r0(); };
    const p = {x: 0, y: 0, vx: 0, vy: 0, band: 'infrared', pass: false};
    chamberQuery(ch, p);
    ok(drew === 0 && p.pass, 'a busy molecule marks the photon to pass through and never flips the coin');
  }
  { /* a molecule with no strategy for that band does the same */
    const ch = newChamber(7, 'N2', 'infrared');
    let drew = 0;
    const r0 = ch.rng;
    ch.rng = () => { drew++; return r0(); };
    const p = {x: 0, y: 0, vx: 0, vy: 0, band: 'infrared', pass: false};
    chamberQuery(ch, p);
    ok(drew === 0 && p.pass, 'nitrogen never even flips the coin in the infrared');
  }
  { /* a photon OUTSIDE the radius is not touched at all */
    const ch = newChamber(7, 'CO2', 'infrared');
    const p = {x: -PHET.ABSORB_RADIUS - 1, y: 0, vx: 0, vy: 0, band: 'infrared', pass: false};
    chamberQuery(ch, p);
    ok(!p.pass && ch.state === 'idle', 'a photon just outside the 100-unit radius is left alone');
    const q = {x: -PHET.ABSORB_RADIUS + 1, y: 0, vx: 0, vy: 0, band: 'infrared', pass: false};
    chamberQuery(ch, q);
    ok(q.pass || ch.state !== 'idle', 'and one just inside it is not');
  }
  { /* the chamber's OWN emission direction, not ensembleDirection's: they are
       different code paths, and only the second one was ever measured */
    let up = 0, down = 0, left = 0, right = 0, n = 0;
    let sc = 0, ss = 0;
    for (let k = 0; k < 400; k++) {
      const ch = newChamber(1000 + k, 'CO2', 'infrared');
      ch.state = 'vib'; ch.hold = 1e-6;
      chamberStep(ch, 1 / 60, false);
      const p = ch.photons[ch.photons.length - 1];
      if (!p) continue;
      n++;
      const a = Math.atan2(p.vy, p.vx);
      sc += Math.cos(a); ss += Math.sin(a);
      if (p.vy > 0) up++; else down++;
      if (p.vx > 0) right++; else left++;
    }
    ok(n === 400, 'four hundred re-emissions, one per seeded chamber (' + n + ')');
    ok(up > 120 && down > 120, 'the emitted photon goes up about as often as down ('
       + up + ' / ' + down + ')');
    ok(left > 120 && right > 120, 'and left about as often as right (' + left + ' / ' + right + ')');
    const se = 1 / Math.sqrt(2 * n);
    ok(Math.abs(sc / n) < 4 * se && Math.abs(ss / n) < 4 * se,
       '(scipy) both moments of the chamber\u2019s own emissions are inside 4 standard errors of 0 ('
       + fmt(sc / n, 4) + ', ' + fmt(ss / n, 4) + ')');
    rel(Math.hypot(400 * 0 + 1, 0), 1, 1e-15, 'a sanity anchor for the moment test');
  }
  { /* the 0.2 s hysteresis is what stops a molecule swallowing the photon it
       has just emitted -- the emitted photon starts AT the molecule, inside
       the absorption radius, and is an ordinary photon like any other */
    const ch = newChamber(31, 'CO2', 'infrared');
    ch.state = 'vib'; ch.hold = 1e-6;
    chamberStep(ch, 1 / 60, false);
    ok(ch.reemitted === 1, 'the molecule re-emits when its hold runs out');
    ok(ch.hyst > 0, "(PhET) and starts its 0.2 s refusal window (" + fmt(ch.hyst, 3) + ' s)');
    const p0 = ch.photons[ch.photons.length - 1];
    ok(p0 && Math.hypot(p0.x, p0.y) < PHET.ABSORB_RADIUS && !p0.pass,
       'the emitted photon is an ordinary photon, starting INSIDE the absorption radius');
    const abs0 = ch.absorbed;
    for (let i = 0; i < 3; i++) chamberStep(ch, 1 / 60, false);
    ok(ch.absorbed === abs0,
       'and the molecule does not swallow it again -- the hysteresis is the only thing stopping it');
    ok(Math.hypot(ch.photons[0].x, ch.photons[0].y) > PHET.ABSORB_RADIUS ||
       ch.hyst > 0, 'by the time the window closes the photon has left the radius');
  }
  { /* the whole 60 s run, photon for photon, against the Python twin */
    const ch = newChamber(4242, 'CO2', 'infrared');
    chamberSetSource(ch, true);
    for (let i = 0; i < 3600; i++) chamberStep(ch, 1 / 60, false);
    ok(ch.fired === REF.sim_fired, '(python) 60 s: photons fired (' + ch.fired + ' vs ' + REF.sim_fired + ')');
    ok(ch.absorbed === REF.sim_absorbed, '(python) 60 s: absorbed (' + ch.absorbed + ' vs ' + REF.sim_absorbed + ')');
    ok(ch.passed === REF.sim_passed, '(python) 60 s: passed through (' + ch.passed + ' vs ' + REF.sim_passed + ')');
    ok(ch.reemitted === REF.sim_reemit, '(python) 60 s: re-emitted (' + ch.reemitted + ' vs ' + REF.sim_reemit + ')');
    rel(ch.busyTime / ch.liveTime, REF.sim_duty, 1e-9, '(python) 60 s: the excited fraction');
    rel(ch.absorbed / (ch.absorbed + ch.passed), REF.sim_absorbed_fraction, 1e-12,
        '(python) 60 s: the absorbed fraction, well under a half');
    ok(ch.absorbed / (ch.absorbed + ch.passed) < 0.45,
       'a continuously lit molecule absorbs far fewer than half the photons, because a busy one refuses them all');
  }
  { /* and the 600 s run */
    const ch = newChamber(4242, 'CO2', 'infrared');
    chamberSetSource(ch, true);
    for (let i = 0; i < 36000; i++) chamberStep(ch, 1 / 60, false);
    ok(ch.fired === REF.sim600_fired, '(python) 600 s: photons fired (' + ch.fired + ' vs ' + REF.sim600_fired + ')');
    ok(ch.absorbed === REF.sim600_absorbed, '(python) 600 s: absorbed (' + ch.absorbed + ')');
    ok(ch.passed === REF.sim600_passed, '(python) 600 s: passed (' + ch.passed + ')');
    rel(ch.busyTime / ch.liveTime, REF.sim600_duty, 1e-9, '(python) 600 s: the excited fraction');
  }
  { /* the renewal estimate is LOW, and the gap is not the seed */
    const d = dutyCycle();
    rel(d.busy, REF.mean_busy_s, 1e-12, '(python) the mean busy time is 1.4 s');
    rel(d.cycle, REF.renewal_cycle_s, 1e-12, '(python) the renewal cycle is 2.6 s');
    rel(d.duty, REF.renewal_duty, 1e-12, '(python) which predicts a 46.2 % duty');
    ok(REF.renewal_duty < REF.sim1200_duty_mean,
       '(python) and the measured 49.1 % is HIGHER -- the phase of an exactly periodic source does not decorrelate');
    ok(REF.sim1200_duty_spread < 0.03, '(python) the spread over five 1200 s seeds is under 0.03, so the gap is real');
  }
  { /* slow motion halves the clock, and a long frame is discarded whole */
    const a = newChamber(3, 'CO2', 'infrared');
    const b = newChamber(3, 'CO2', 'infrared');
    chamberStep(a, 0.1, false);
    chamberStep(b, 0.1, true);
    rel(a.t, 2 * b.t, 1e-12, '(PhET) slow motion advances the clock at half speed');
    const c = newChamber(3, 'CO2', 'infrared');
    ok(chamberStep(c, 0.25, false) === false && c.t === 0,
       '(PhET) a frame longer than 0.2 s is discarded whole, not clamped');
    ok(chamberStep(c, 0.19, false) === true && c.t > 0, 'and one just under it is taken');
  }
  { /* breaking apart: the products, and the speeds */
    const ch = newChamber(99, 'O3', 'ultraviolet');
    chamberSetSource(ch, true);
    let n = 0;
    while (ch.state !== 'broken' && n < 4000) { chamberStep(ch, 1 / 60, false); n++; }
    ok(ch.state === 'broken', 'ozone in the ultraviolet does break apart');
    ok(ch.frags && ch.frags.map(f => f.mol).join('+') === 'O2+O',
       '(PhET) into O2 and O, which is what PhET builds');
    if (ch.frags) {
      rel(Math.hypot(ch.frags[0].vx, ch.frags[0].vy), PHET.FRAG_A, 1e-12, '(PhET) the O2 leaves at 990');
      rel(Math.hypot(ch.frags[1].vx, ch.frags[1].vy), PHET.FRAG_B, 1e-12, '(PhET) the O leaves at 0.67 x 3000');
      const dot = ch.frags[0].vx * ch.frags[1].vx + ch.frags[0].vy * ch.frags[1].vy;
      ok(dot < 0, 'and they leave in opposite directions');
    }
    const ch2 = newChamber(99, 'N2', 'ultraviolet');
    chamberSetSource(ch2, true);
    for (let i = 0; i < 2000; i++) chamberStep(ch2, 1 / 60, false);
    ok(ch2.state === 'idle' && ch2.absorbed === 0,
       '(PhET) while nitrogen, which really would be destroyed at 12.4 eV, is left completely alone');
  }
  { /* PhET's own vibration offsets: the CO2 bend conserves ITS centre of mass */
    const off = phetVibration('CO2', Math.PI / 2);
    const mC = PHET_ATOM.C.m, mO = PHET_ATOM.O.m;
    close(mC * off[0][1] + mO * off[1][1] + mO * off[2][1], 0, 1e-12,
          "(PhET) PhET's CO2 bend conserves the centre of mass -- with ITS oxygen mass of 12.011");
    const bad = mC * off[0][1] + MASS.O * off[1][1] + MASS.O * off[2][1];
    ok(Math.abs(bad) > 100, 'and with the real oxygen mass it does not, by ' + fmt(bad, 0) + ' units');
    close(off[0][1], 40, 1e-12, "(PhET) the carbon moves 40 at the top of the swing");
    close(off[1][1], -20, 1e-12, 'and each oxygen 20 the other way');
  }
  { /* the normal-mode animation really follows the eigenvector */
    const off = drawOffsets('CO2', 'mode', Math.PI / 2, 55);
    const T = modeTable('CO2');
    const first = T.filter(m => m.active)[0];
    let w = 0;
    for (let i = 0; i < 3; i++) w = Math.max(w, Math.abs(off[i][0] - first.d[i][0] * 55),
                                             Math.abs(off[i][1] - first.d[i][1] * 55));
    ok(w < 1e-9, 'the drawn normal-mode offsets ARE the eigenvector, times the amplitude (' + w.toExponential(2) + ')');
    const ph = drawOffsets('CO2', 'phet', Math.PI / 2, 55);
    ok(Math.abs(ph[0][1] - 40) < 1e-12, "and the PhET chip draws PhET's own offsets instead");
  }

  /* ================= 10. Planck and the atmosphere ================== */
  rel(planckBand(1, 6000, 288, 24000), REF.sigma_T4, 3e-4,
      '(scipy) pi times the integral of B over wavenumber is sigma T^4');
  rel(REF.integrated_emittance, REF.sigma_T4, 1e-7, '(python) and the twin agrees to 7e-9');
  rel(wienXWavenumber(), REF.wien_x_wavenumber, 1e-12, '(scipy) the root of 3(1 - e^-x) = x');
  rel(wienXWavenumber(), 2.821439372122079, 1e-12, '(exact) x = 2.8214393721');
  ok(Math.abs(3 * (1 - Math.exp(-wienXWavenumber())) - wienXWavenumber()) < 1e-12,
     'and it really solves its own equation');
  rel(planckPeakCm(288), REF.planck_peak_cm, 1e-11, '(python) the peak of B at 288 K, per wavenumber');
  ok(Math.abs(1e4 / planckPeakCm(288) - 10) > 5,
     'the wavenumber peak (17.7 um) is NOT the wavelength peak (10.1 um) -- different questions');
  { /* the peak really is a maximum */
    const p = planckPeakCm(288);
    ok(planckNubar(p, 288) > planckNubar(p * 0.98, 288) && planckNubar(p, 288) > planckNubar(p * 1.02, 288),
       'and B is larger there than on either side of it');
  }
  rel(planckNubar(667, 288), REF.planck_288_at_667, 1e-10, '(python) B at the CO2 bend');
  rel(planckBand(1e4 / 13, 1e4 / 8, 288, 4000) / planckBand(1, 6000, 288, 24000), REF.window_fraction, 2e-5,
      '(python) the 8-13 um window carries 31.2 % of the 288 K emission');
  { let a = 0, i = 0;
    for (const r of AIR) { if (r[3]) a += r[1]; else i += r[1]; }
    rel(i, REF.dry_air_transparent_pct, 1e-12, '(python) 99.966 % of dry air absorbs no infrared');
    rel(a, REF.dry_air_IRactive_pct, 1e-12, '(python) and 0.043 % does all of it');
    ok(i / a > 2000, 'the transparent part outnumbers the absorbing part by more than 2000 to 1');
  }
  close(CO2_PPM, 427.62, 0, '(NOAA) the June 2026 global mean CO2, which NOAA itself calls preliminary');
  { /* the bands drawn on the Planck curve are the IR-ACTIVE ones only */
    const a = airBlock();
    ok(a.lines.length > 0 && a.lines.every(l => modeTable(l.mol).some(m => m.active && Math.abs(m.nu - l.nu) < 0.5)),
       'every band drawn on the Planck curve is an infrared-active fundamental');
    ok(!a.lines.some(l => l.mol === 'N2' || l.mol === 'O2'),
       'and neither nitrogen nor oxygen contributes one');
    const co2 = a.lines.filter(l => l.mol === 'CO2').map(l => l.nu);
    const near = v => co2.some(x => Math.abs(x - v) < 0.5);
    ok(near(667) && near(2349) && !near(1333),
       'CO2 contributes its bend and its antisymmetric stretch, and NOT its symmetric stretch');
  }

  /* ================= 11. the real-vs-PhET comparison ================ */
  { let dis = 0;
    for (const m of MOLORDER) for (const b of BANDS)
      if ((PHET_TABLE[m][b] !== '') !== (realCell(m, b).kind !== '')) dis++;
    ok(dis > 0 && dis < 32, 'the two tables disagree in ' + dis + ' of the 32 cells');
    ok(realCell('N2', 'ultraviolet').kind === 'break' && PHET_TABLE.N2.ultraviolet === '',
       'nitrogen at 100 nm is the clearest of them: 12.4 eV against a 9.75 eV bond');
    ok(realCell('O3', 'visible').kind === 'glow' && PHET_TABLE.O3.visible === '',
       'and ozone in the visible is the one PhET’s own model notes admit');
    ok(realCell('N2', 'infrared').kind === '' && realCell('O2', 'microwave').kind === '',
       'the two tables agree that N2 and O2 do nothing in the infrared and microwave');
  }
  { const R = realAnswer('CO2', 'infrared');
    ok(R.nActive === 3, 'CO2 has three IR-active fundamentals (the bend is doubly degenerate)');
    ok(R.decades > 0.65, "PhET's IR photon is a factor of five from CO2's nearest band ("
       + fmt(R.decades, 2) + ' decades)');
    rel(Math.pow(10, R.decades), PHOTON.infrared.nubar / 2349, 1e-12,
        'which is 11765 over 2349, the antisymmetric stretch');
    const Rm = realAnswer('CO', 'microwave');
    ok(Rm.rot, 'CO does have a rotational spectrum');
  }

  /* ================= 12. the panels and the layout =================== */
  { let bad = null;
    for (const [v] of TABS) for (const mol of MOLORDER) for (const band of BANDS) {
      withState({view: v, mol, band, nStat: 2000}, () => {
        for (const k in MEMO) delete MEMO[k];
        const M = buildModel();
        for (const s of [readoutHTML(M), eqbarHTML(M), tagHTML(M)])
          if (/NaN|undefined|Infinity/.test(s)) bad = bad || (v + '/' + mol + '/' + band + ': ' + s.slice(0, 80));
      });
    }
    ok(!bad, 'every view x molecule x band builds a clean readout, eqbar and tag (' + (bad || 'ok') + ')');
  }
  { /* the readout must carry a number no other row can supply -- a formatter
       that prints NaN as an em-dash makes the NaN scan vacuous */
    withState({view: 'modes', mol: 'CO2', modeIdx: 0}, () => {
      for (const k in MEMO) delete MEMO[k];
      const s = readoutHTML(buildModel());
      ok(s.indexOf('12.398') >= 0 || s.indexOf('1.4586') >= 0, 'the readout prints a real photon energy');
      ok(s.indexOf('0 exactly') >= 0 || s.indexOf('active') >= 0, 'and a real selection-rule verdict');
    });
  }
  { let bad = null;
    for (const mol of MOLORDER) for (let i = 0; i < 12; i++) {
      withState({mol, modeIdx: i}, () => {
        for (const k in MEMO) delete MEMO[k];
        const m = currentMode();
        if (!m || !isFinite(m.nu) || !isFinite(m.dmu)) bad = bad || (mol + '/' + i);
      });
    }
    ok(!bad, 'no molecule and mode index gives a non-finite mode (' + (bad || 'ok') + ')');
  }
  { let bad = null;
    for (let T = 220; T <= 330; T += 5) {
      const a = (function () { const s = Object.assign({}, ST); ST.tempK = T; delete MEMO.air;
        const r = airBlock(); Object.assign(ST, s); delete MEMO.air; return r; })();
      if (!isFinite(a.tot) || !isFinite(a.peak) || !(a.wfrac > 0 && a.wfrac < 1)) bad = '' + T;
    }
    ok(!bad, 'no surface temperature gives a non-finite atmosphere block (' + (bad || 'ok') + ')');
  }
  { let bad = null;
    for (const n of [500, 2000, 8000, 40000]) for (const sd of [1, 77003, 199999]) {
      const s = Object.assign({}, ST);
      ST.nStat = n; ST.statSeed = sd; delete MEMO.stat;
      const t = statBlock();
      if (!isFinite(t.f) || !isFinite(t.hold.mean) || !isFinite(t.dir.chi2)) bad = n + '/' + sd;
      if (t.xs.length !== t.ys.length) bad = 'trace length ' + n + '/' + sd;
      Object.assign(ST, s); delete MEMO.stat;
    }
    ok(!bad, 'no ensemble size and seed gives a non-finite statistic (' + (bad || 'ok') + ')');
  }
  const SIZES = [[1400, 820], [1100, 712], [820, 560], [560, 380]];
  const CONFIGS = [
    ['chamber CO2 IR', {view: 'chamber', mol: 'CO2', band: 'infrared'}, 40],
    ['chamber N2 UV', {view: 'chamber', mol: 'N2', band: 'ultraviolet', showRadius: true}, 40],
    ['chamber O3 UV', {view: 'chamber', mol: 'O3', band: 'ultraviolet'}, 40],
    ['chamber CH4 micro', {view: 'chamber', mol: 'CH4', band: 'microwave', anim: 'phet'}, 40],
    ['chamber source off', {view: 'chamber', mol: 'CO', band: 'visible', source: false}, 30],
    /* the floor is derived from what the configuration draws: with the
       bottom row dropped on a short stage the spectrum view legitimately
       emits about sixty ops, and a floor of 80 would punish it for that */
    ['spectrum IR', {view: 'spectrum', band: 'infrared', mol: 'CO2'}, 50],
    ['spectrum micro', {view: 'spectrum', band: 'microwave', mol: 'H2O'}, 50],
    ['table', {view: 'table', mol: 'NO2', band: 'visible'}, 80],
    ['table N2 UV', {view: 'table', mol: 'N2', band: 'ultraviolet'}, 80],
    ['modes CO2', {view: 'modes', mol: 'CO2', modeIdx: 1}, 30],
    ['modes CH4', {view: 'modes', mol: 'CH4', modeIdx: 3}, 30],
    ['modes H2O', {view: 'modes', mol: 'H2O', modeIdx: 0}, 30],
    ['modes N2', {view: 'modes', mol: 'N2', modeIdx: 0}, 20],
    ['stats', {view: 'stats', nStat: 2000}, 60],
    ['stats big', {view: 'stats', nStat: 20000, statSeed: 5}, 60],
    ['air', {view: 'air'}, 60],
    ['air cold', {view: 'air', tempK: 220, showWindow: false}, 60],
  ];
  const entRe = /&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for (const [nm, over, minOps] of CONFIGS) for (const [W, H] of SIZES) {
    withState(over, () => {
      for (const k in MEMO) delete MEMO[k];
      const c = makeShot(W, H);
      let err = null;
      try { drawView(c, W, H, buildModel()); } catch (e) { err = e; }
      ok(!err, nm + ' ' + W + 'x' + H + ' draws without throwing' + (err ? ': ' + (err.stack || err) : ''));
      if (err) return;
      const texts = c.ops.filter(o => o.op === 'text'), fills = c.ops.filter(o => o.op === 'fill');
      ok(c.ops.length >= minOps && texts.length >= 1 && fills.length >= 1,
         nm + ' ' + W + 'x' + H + ' draws substance (' + c.ops.length + ' ops, ' + fills.length
         + ' fills, ' + texts.length + ' texts; floor ' + minOps + ')');
      let bad = null;
      for (const t of texts) {
        if (entRe.test(t.t)) { bad = 'entity/tag: "' + t.t.slice(0, 40) + '"'; break; }
        if (/undefined|NaN/.test(t.t)) { bad = 'NaN/undefined: "' + t.t.slice(0, 40) + '"'; break; }
        if (t.bb[0] < -1 || t.bb[2] > W + 1 || t.bb[1] < -1 || t.bb[3] > H + 1) {
          bad = 'off-canvas: "' + t.t.slice(0, 30) + '" [' + t.bb.map(v => fmt(v, 0)) + ']'; break;
        }
      }
      ok(!bad, nm + ' ' + W + 'x' + H + ' text clean (' + (bad || 'ok') + ')');
      const inHint = texts.filter(t => t.bb[0] < 340 && t.bb[3] > H - 27);
      ok(!inHint.length, nm + ' ' + W + 'x' + H + ' no canvas text under the #hint line'
         + (inHint.length ? ' ("' + inHint[0].t.slice(0, 30) + '" to y ' + fmt(inHint[0].bb[3], 0) + ')' : ''));
      let hit = null;
      for (let i2 = 0; i2 < texts.length && !hit; i2++) for (let j2 = i2 + 1; j2 < texts.length; j2++) {
        const a = texts[i2].bb, b2 = texts[j2].bb;
        const ox = Math.min(a[2], b2[2]) - Math.max(a[0], b2[0]);
        const oy = Math.min(a[3], b2[3]) - Math.max(a[1], b2[1]);
        if (ox > 3 && oy > 3) { hit = '"' + texts[i2].t.slice(0, 22) + '" vs "' + texts[j2].t.slice(0, 22) + '"'; break; }
      }
      ok(!hit, nm + ' ' + W + 'x' + H + ' no text collisions (' + (hit || 'ok') + ')');
      const nanc = fills.filter(f => f.style && /NaN/.test(f.style));
      ok(!nanc.length, nm + ' ' + W + 'x' + H + ' no NaN colours');
    });
  }

  Object.assign(ST, stSave);
  resetAll();
  const dt = (Date.now() - T0) / 1000;
  console.log(pass + ' passed, ' + fail + ' failed  (' + fmt(dt, 1) + ' s)');
  if (fail > 0) throw new Error(fail + ' self-test failure(s)');
  return fail;
}

/* ============================== entry ============================= */
if (typeof document === 'undefined') {
  selfTest();
} else {
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
}
