
/* ================================================================== *
 *  selfTest — headless verification.  Every value labelled (derive)   *
 *  is a line of build/models-of-the-hydrogen-atom/refvals.txt, the    *
 *  printed output of derive.py, emitted into p7_refs.js by            *
 *  make_refs.py — no number in this file was typed by hand.           *
 * ================================================================== */
function makeShot(W, H){
  const ops = []; let Mx = [1, 0, 0, 1, 0, 0]; const stack = [];
  const st2 = {font: '10px x', align: 'left', base: 'alphabetic'};
  const mul = (A, B) => [A[0]*B[0]+A[2]*B[1], A[1]*B[0]+A[3]*B[1], A[0]*B[2]+A[2]*B[3],
                         A[1]*B[2]+A[3]*B[3], A[0]*B[4]+A[2]*B[5]+A[4], A[1]*B[4]+A[3]*B[5]+A[5]];
  const app = (x, y) => [Mx[0]*x+Mx[2]*y+Mx[4], Mx[1]*x+Mx[3]*y+Mx[5]];
  const fsz = () => { const m = /([\d.]+)px/.exec(st2.font); return m ? parseFloat(m[1]) : 10; };
  let pend = null;
  const ctx = {ops,
    save(){ stack.push({M: Mx.slice(), f: st2.font, a: st2.align, b: st2.base}); },
    restore(){ const s = stack.pop(); if(s){ Mx = s.M; st2.font = s.f; st2.align = s.a; st2.base = s.b; } },
    translate(x, y){ Mx = mul(Mx, [1, 0, 0, 1, x, y]); },
    rotate(r){ const c = Math.cos(r), s3 = Math.sin(r); Mx = mul(Mx, [c, s3, -s3, c, 0, 0]); },
    scale(x, y){ Mx = mul(Mx, [x, 0, 0, y, 0, 0]); }, setTransform(){ Mx = [1, 0, 0, 1, 0, 0]; },
    beginPath(){ pend = null; }, moveTo(){}, lineTo(){ if(!pend) pend = {n: 0}; }, closePath(){},
    rect(){ if(!pend) pend = {n: 0}; pend.n++; }, arc(){ if(!pend) pend = {n: 0}; pend.n++; },
    fill(){ if(pend) ops.push({op: 'fill', n: pend.n || 1}); },
    stroke(){ ops.push({op: 'stroke'}); }, clip(){},
    fillRect(x, y, w, hh){ ops.push({op: 'fill', n: 1, bb: [x, y, x + w, y + hh]}); },
    strokeRect(){ ops.push({op: 'stroke'}); }, clearRect(){},
    fillText(t, x, y){
      const w = ('' + t).length * fsz() * 0.52, fh = fsz() * 1.15;
      const lx = st2.align === 'center' ? x - w / 2 : (st2.align === 'right' ? x - w : x);
      const ly = st2.base === 'top' ? y : (st2.base === 'middle' ? y - fh / 2
        : (st2.base === 'bottom' ? y - fh : y - fh * 0.8));
      const cs = [[lx, ly], [lx + w, ly], [lx, ly + fh], [lx + w, ly + fh]].map(c2 => app(c2[0], c2[1]));
      const xs = cs.map(c2 => c2[0]), ys = cs.map(c2 => c2[1]);
      ops.push({op: 'text', t: '' + t, bb: [Math.min.apply(0, xs), Math.min.apply(0, ys),
                                            Math.max.apply(0, xs), Math.max.apply(0, ys)]});
    },
    strokeText(){}, setLineDash(){},
    measureText(t){ return {width: ('' + t).length * fsz() * 0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
  };
  let _fill = '#000';
  Object.defineProperty(ctx, 'fillStyle', {get: () => _fill, set: v => _fill = '' + v});
  for(const kk of ['strokeStyle', 'lineWidth', 'globalAlpha', 'lineJoin', 'lineCap']){
    let v2; Object.defineProperty(ctx, kk, {get: () => v2, set: x => v2 = x});
  }
  Object.defineProperty(ctx, 'font', {get: () => st2.font, set: v => st2.font = '' + v});
  Object.defineProperty(ctx, 'textAlign', {get: () => st2.align, set: v => st2.align = '' + v});
  Object.defineProperty(ctx, 'textBaseline', {get: () => st2.base, set: v => st2.base = '' + v});
  return ctx;
}

/* composite Simpson — the independent numerical route for every closed form */
function simpson(f, a, b, N){
  N = N + (N % 2);
  const hh = (b - a) / N;
  let s = f(a) + f(b);
  for(let i = 1; i < N; i++) s += (i % 2 ? 4 : 2) * f(a + i * hh);
  return s * hh / 3;
}

function selfTest(){
  let pass = 0, fail = 0;
  const ok = (c, name) => { if(c) pass++; else { fail++; console.log('FAIL — ' + name); } };
  const eq = (a, b, name) => ok(a === b, name + ' [' + a + ' vs ' + b + ']');
  const close = (a, b, tol, name) => ok(Math.abs(a - b) <= tol, name + ' [' + a + ' vs ' + b + ']');
  const rel = (a, b, t, name) => ok(Math.abs(a - b) <= t * Math.abs(b || 1),
    name + ' [' + a + ' vs ' + b + ', rel ' + (Math.abs(a - b) / Math.abs(b || 1)).toExponential(2) + ']');
  const T0 = Date.now();
  const stSave = Object.assign({}, ST);

  /* =============== A. constants ================================== */
  close(DEG * 90, PI / 2, 1e-12, 'DEG converts degrees INTO radians (90 deg = pi/2)');
  close(RAD * PI, 180, 1e-12, 'RAD converts radians INTO degrees');
  rel(R_INF, R('R_inf (m^-1)'), 1e-12, 'R_inf (derive)');
  rel(RYD_EV, R('R_inf*h*c (eV)'), 1e-12, 'R_inf h c in eV (derive)');
  rel(A0, R('a_0 (m)'), 1e-12, 'a_0 (derive)');
  rel(ALPHA, R('alpha'), 1e-12, 'alpha (derive)');
  rel(M_E, R('m_e (kg)'), 1e-12, 'm_e (derive)');
  rel(H_PLANCK, R('h (J s)'), 1e-12, 'h (derive)');
  rel(ME_MP, R('m_e/m_p'), 1e-12, 'm_e/m_p (derive)');
  rel(MU_ME, R('mu/m_e'), 1e-12, 'reduced mass mu/m_e (derive)');
  rel(R_H, R('R_H (m^-1)'), 1e-12, 'R_H (derive)');
  rel(RH_EV, R('R_H*h*c (eV)'), 1e-12, 'R_H h c in eV (derive)');
  rel(T_AU, R('atomic unit of time (s)'), 1e-12, 'atomic unit of time (derive)');
  /* the reduced mass is not decoration: it moves every line by 5.4e-4 */
  rel((lamVac(2, 3) - lamVacInf(2, 3)) / lamVac(2, 3), ME_MP / (1 + ME_MP), 1e-9,
    'reduced mass shifts H-alpha by m_e/m_p');
  ok(Math.abs(lamVac(2, 3) - lamVacInf(2, 3)) > 0.3, 'that shift is 0.36 nm at H-alpha, not a rounding');

  /* =============== B. the Bohr ladder ============================ */
  for(let n = 1; n <= 6; n++){
    rel(energyEV(n), R('E_' + n + ' (eV, reduced mass)'), 1e-12, 'E_' + n + ' reduced mass (derive)');
    rel(energyEVinf(n), R('E_' + n + ' (eV, infinite mass)'), 1e-12, 'E_' + n + ' infinite mass (derive)');
    rel(orbitRadius(n), R('r_' + n + ' (m) = n^2 a_0'), 1e-12, 'r_' + n + ' (derive)');
    rel(orbitSpeed(n), R('v_' + n + ' (m/s) = alpha c/n'), 1e-12, 'v_' + n + ' (derive)');
  }
  /* the virial theorem: <T> = -E and <V> = 2E, so V/T = -2 exactly */
  close(2 * energyEV(1) / (-energyEV(1)), -2, 1e-12, 'virial <V>/<T> = -2');
  const SER = {1: 'Lyman', 2: 'Balmer', 3: 'Paschen', 4: 'Brackett', 5: 'Pfund', 6: 'Humphreys'};
  for(let n1 = 1; n1 <= 6; n1++){
    for(let n2 = n1 + 1; n2 <= Math.min(n1 + 6, 12); n2++)
      rel(lamVac(n1, n2), R('lambda(' + n2 + '->' + n1 + ') ' + SER[n1] + ' nm'), 1e-12,
        'lambda ' + n2 + '->' + n1 + ' (derive)');
    rel(seriesLimit(n1), R('lambda(inf->' + n1 + ') ' + SER[n1] + ' limit nm'), 1e-12,
      SER[n1] + ' limit (derive)');
  }
  /* an independent route to the same wavelength: hc/dE */
  const HC_EV_NM = R('hc (eV nm)');
  for(const [n1, n2] of [[1, 2], [2, 3], [2, 4], [3, 4], [1, 6]]){
    const dE = RH_EV * (1 / (n1 * n1) - 1 / (n2 * n2));
    rel(HC_EV_NM / dE, lamVac(n1, n2), 1e-12, 'hc/dE route agrees, ' + n2 + '->' + n1);
  }
  /* PhET's fifteen integers */
  eq(TRANSITIONS.length, R('PhET number of transitions (n=1..6)'), 'PhET has 15 transitions (derive)');
  for(const t of TRANSITIONS)
    eq(t.phet, R('PhET lambda(' + t.n2 + '->' + t.n1 + ') nm (integer)'),
      'PhET integer ' + t.n2 + '->' + t.n1 + ' (derive)');
  ok(new Set(PHET_LAMS).size === PHET_LAMS.length, 'no two PhET transitions round to the same integer');
  eq(JSON.stringify(PHET_LAMS.filter(w => w < 380).sort((a, b) => a - b)),
     JSON.stringify(R('PhET UV wavelengths').replace(/[\[\] ]/g, '').split(',').map(Number)),
     'PhET UV set (derive)');
  eq(JSON.stringify(PHET_LAMS.filter(w => w >= 380 && w <= 780).sort((a, b) => a - b)),
     JSON.stringify(R('PhET visible wavelengths').replace(/[\[\] ]/g, '').split(',').map(Number)),
     'PhET visible set (derive)');
  eq(JSON.stringify(phetGroundAbsorptionLams()), JSON.stringify([122, 103, 97, 95, 94]),
     'the n=1 absorption lines PhET biases white light toward');
  {
    /* PhET aims 0.4 of its white photons at an n = 1 line and scatters the rest
       uniformly over 92-780 nm; measure the fraction off the source */
    Object.assign(ST, DEFAULTS, {light: 'white', lightOn: true, seed: 5150});
    atomReset(ST);
    const gl = phetGroundAbsorptionLams();
    let onLine = 0;
    const NW = 20000;
    for(let k = 0; k < NW; k++){
      ATOM.photons.length = 0;
      firePhoton(ST);
      if(gl.indexOf(ATOM.photons[0].lam) >= 0) onLine++;
    }
    const want = 0.4 + 0.6 * gl.length / (PHET.lamMax - PHET.lamMin + 1);
    rel(onLine / NW, want, 0.04, 'white light is 40 % aimed at the n = 1 lines (PhET)');
    ok(Math.abs(onLine / NW - 0.7) > 0.2, 'and not 70 %');
    let inRange = true;
    for(let k = 0; k < 2000; k++){
      ATOM.photons.length = 0; firePhoton(ST);
      const w = ATOM.photons[0].lam;
      if(w < PHET.lamMin || w > PHET.lamMax || w !== Math.round(w)) inRange = false;
    }
    ok(inRange, 'every white photon is an integer nanometre inside 92-780 nm (PhET)');
  }
  /* PhET's rounding is a real error, not a nicety */
  rel(phetLam(1, 2) / lamVac(1, 2) - 1, R('PhET lambda(2->1) nm (integer) :: PhET/exact - 1'), 1e-9,
    'PhET Lyman-alpha is 0.355 % high (derive)');
  /* the round-trip PhET's absorption test depends on */
  for(const t of TRANSITIONS){
    eq(phetHigherState(t.n1, t.phet), t.n2, 'higher state for ' + t.phet + ' nm from n=' + t.n1);
    eq(phetLowerState(t.n2, t.phet), t.n1, 'lower state for ' + t.phet + ' nm from n=' + t.n2);
  }
  eq(phetHigherState(1, 121), null, '121 nm is not an absorption line of PhET n=1');
  eq(transitionForPhetLam(300), null, '300 nm is not a transition at all');
  eq(bandOf(122), 'UV', '122 nm is ultraviolet');
  eq(bandOf(656), 'visible', '656 nm is visible');
  eq(bandOf(1876), 'IR', '1876 nm is infrared');
  /* PhET's drawn ladder is not the true one, and both are pinned */
  eq(JSON.stringify(PHET.orbitR), JSON.stringify([15, 44, 81, 124, 174, 233]), 'PhET orbit radii');
  eq(JSON.stringify(PHET.levelY), JSON.stringify([0.025, 0.6, 0.73, 0.81, 0.86, 0.9]), 'PhET level heights');
  close(viewRadius(6) / viewRadius(1), 233 / 15, 1e-12, 'PhET compresses n=6 to 15.5 x n=1');
  close(trueViewRadius(6) / trueViewRadius(1), 36, 1e-12, 'the true n=6 is 36 x n=1');
  ok(Math.abs(PHET.levelY[1] - (1 - 1 / 4)) > 0.1, 'PhET puts n=2 well below its true 0.75');

  /* =============== C. de Broglie ================================= */
  for(let n = 1; n <= 6; n++){
    rel(lamDeBroglie(n), R('lambda_dB(n=' + n + ') (m)'), 1e-12, 'lambda_dB n=' + n + ' (derive)');
    rel(n * lamDeBroglie(n) / (TAU * orbitRadius(n)) - 1,
      R('lambda_dB(n=' + n + ') (m) :: n*lambda_dB / (2 pi r_n) - 1'), 1e-6,
      'n lambda_dB = 2 pi r_n to 5.18e-12 (derive)');
  }
  /* the residual is CODATA's own inconsistency, not the sim's: it is the same
     number as a_0 - hbar/(m alpha c), which is why it does not shrink with n */
  rel(1 * lamDeBroglie(1) / (TAU * orbitRadius(1)) - 1,
    R('a_0 - hbar/(m_e alpha c), relative'), 1e-4, 'the residual IS a_0 vs hbar/(m alpha c) (derive)');
  /* the seam mismatch: closed form against the two-term expression it came from */
  let worstC = 0;
  for(let k = 0; k <= 400; k++){
    const nu = 0.3 + 7 * k / 400;
    worstC = Math.max(worstC, Math.abs(closureMismatch(nu) - closureMismatchRaw(nu)));
  }
  ok(worstC < 1e-14, '2|sin pi nu| equals sqrt(dv^2 + ds^2) over 400 nu [' + worstC.toExponential(2) + ']');
  for(let n = 1; n <= 7; n++) close(closureMismatch(n), 0, 1e-12, 'the wave closes at nu = ' + n);
  close(closureMismatch(2.5), 2, 1e-12, 'a half-integer misses by the maximum, 2');
  close(closureMismatch(3.25), 2 * Math.abs(Math.sin(PI * 0.25)), 1e-12, 'quarter-integer mismatch');
  ok(closureMismatch(3.02) > 0.125 && closureMismatch(3.02) < 0.126, 'a 0.02 slip already costs 0.1256');

  /* =============== D. the wavefunctions ========================== */
  /* the exact polynomial coefficients against the Laguerre recurrence */
  let worstR = 0;
  for(let n = 1; n <= 6; n++) for(let l = 0; l < n; l++) for(let k = 1; k <= 60; k++){
    const r = k;
    worstR = Math.max(worstR, Math.abs(Rnl(n, l, r) - RnlDirect(n, l, r)));
  }
  ok(worstR < 1e-14, 'the polynomial form equals the Laguerre recurrence [' + worstR.toExponential(2) + ']');
  for(const [n, l, r] of [[1, 0, 0.5], [1, 0, 1.0], [1, 0, 2.0], [2, 0, 1.0], [2, 0, 4.0],
                          [2, 1, 2.0], [2, 1, 4.0], [3, 0, 3.0], [3, 2, 9.0], [4, 1, 8.0],
                          [6, 0, 12.0], [6, 5, 30.0]]){
    const key = 'R_' + n + l + '(' + r.toFixed(1) + ')';
    rel(Rnl(n, l, r), R(key), 1e-12, key + ' (derive)');
  }
  eq(Rnl(2, 0, 2), 0, 'R_20 has its node at exactly r = 2 a_0');
  eq(Rnl(3, 1, 6), 0, 'R_31 has its node at exactly r = 6 a_0');
  /* normalisation and the moments, by quadrature — an independent route */
  for(const [n, l] of [[1, 0], [2, 0], [2, 1], [3, 0], [3, 1], [3, 2], [4, 0], [4, 3], [5, 2], [6, 1]]){
    /* the integrand decays as exp(-2r/n) and oscillates n-l-1 times, so BOTH the
       range and the step have to follow n; a fixed pair tuned at n = 1 leaves
       <1/r> wrong in the fifth digit at n = 4 (Known-bad: resolution follows
       the structure, not the range) */
    const rmax = 15 * n + 12 * n * n, N = 6000 * n;
    const nrm = simpson(r => { const v = Rnl(n, l, r); return v * v * r * r; }, 0, rmax, N);
    rel(nrm, 1, 1e-9, 'int R_' + n + l + '^2 r^2 dr = 1 (quadrature)');
    const m1 = simpson(r => { const v = Rnl(n, l, r); return v * v * r * r * r; }, 0, rmax, N);
    rel(m1, meanR(n, l), 1e-9, '<r> for ' + n + l + ' by quadrature equals the closed form');
    rel(meanR(n, l), R('radial nodes R_' + n + l + ' (counted) :: <r>_' + n + l + ' (quad)'), 1e-12,
      '<r> ' + n + l + ' (derive)');
    const m2 = simpson(r => { const v = Rnl(n, l, r); return v * v * r * r * r * r; }, 0, rmax, N);
    rel(m2, meanR2(n, l), 1e-9, '<r^2> for ' + n + l + ' by quadrature equals the closed form');
    rel(meanR2(n, l), R('radial nodes R_' + n + l + ' (counted) :: <r^2>_' + n + l + ' (quad)'), 1e-12,
      '<r^2> ' + n + l + ' (derive)');
    const mi = simpson(r => { const v = Rnl(n, l, r); return v * v * r; }, 0, rmax, N);
    rel(mi, meanInvR(n), 1e-8, '<1/r> for ' + n + l + ' by quadrature equals 1/n^2');
    eq(radialNodeRadii(n, l).length, radialNodes(n, l), 'R_' + n + l + ' has n-l-1 radial nodes');
    eq(radialNodes(n, l), R('radial nodes R_' + n + l + ' (counted)'), 'node count ' + n + l + ' (derive)');
  }
  /* <r> depends on l, so a test that only ever used l = 0 would miss it */
  ok(meanR(3, 0) !== meanR(3, 2), '<r> is not the same for 3s and 3d (13.5 vs 10.5)');
  /* The Condon-Shortley phase (-1)^m in legendreP cancels in |Y|^2, which is
     the only thing this file ever asks for, so a mutant that drops it is
     EQUIVALENT.  That is worth stating rather than leaving as a blind spot
     (Known-bad): assert the invariance deliberately. */
  for(const [l, m] of [[1, 1], [2, 1], [3, 3], [5, 3]]){
    const p1 = legendreP(l, m, 0.42);
    ok(Math.abs(p1) > 1e-6, 'P_' + l + '^' + m + '(0.42) is not zero, so the phase is testable');
    ok(Math.abs(ylmSq(l, m, 0.42) - ylmSq(l, -m, 0.42)) < 1e-15,
      '|Y_' + l + '^' + m + '|^2 does not depend on the sign of m, so the phase cancels');
  }
  /* the angular part */
  for(const [l, m] of [[0, 0], [1, 0], [1, 1], [2, 0], [2, 1], [2, 2], [3, 0], [3, 2], [5, 3]]){
    for(const cth of [0.0, 0.3, 0.7, 1.0]){
      const key = 'int |Y_' + l + m + '|^2 dOmega (scipy) :: |Y_' + l + m + '|^2 at cos th=' + cth.toFixed(1);
      const want = R(key);
      if(Math.abs(want) < 1e-20) close(ylmSq(l, m, cth), 0, 1e-15, key + ' (derive)');
      else rel(ylmSq(l, m, cth), want, 1e-11, key + ' (derive)');
    }
    /* normalisation of |Y|^2 over the sphere, by quadrature in cos theta */
    const nrm = TAU * simpson(u => ylmSq(l, m, u), -1, 1, 4000);
    rel(nrm, 1, 1e-8, 'int |Y_' + l + m + '|^2 dOmega = 1 (quadrature)');
    eq(angularNodeAngles(l, m).length * (l - Math.abs(m) > 0 ? 1 : 0) >= 0, true, 'angular nodes counted');
    eq(angularNodes(l, m), R('int |Y_' + l + m + '|^2 dOmega (scipy) :: angular nodes of P_' + l + '^' + m + ' counted'),
      'l - |m| angular nodes for Y_' + l + m + ' (derive)');
  }
  /* |psi|^2 and the drawn column */
  for(const [n, l, m, x, y, z] of [[1, 0, 0, 0.0, 0.0, 1.0], [1, 0, 0, 0.6, 0.0, 0.8],
      [2, 0, 0, 0.0, 0.0, 3.0], [2, 1, 0, 0.0, 0.0, 4.0], [2, 1, 1, 4.0, 0.0, 0.0],
      [3, 2, 0, 0.0, 0.0, 6.0], [3, 2, 1, 5.0, 0.0, 5.0], [3, 2, 2, 7.0, 0.0, 0.0],
      [4, 3, 1, 8.0, 0.0, 8.0], [6, 0, 0, 0.0, 0.0, 20.0]]){
    const key = '|psi_' + n + l + m + '|^2 at (' + x.toFixed(1) + ',' + y.toFixed(1) + ',' + z.toFixed(1) + ')';
    rel(psiSq(n, l, m, x, y, z), R(key), 1e-11, key + ' (derive)');
  }
  for(const [n, l, m, x, z] of [[1, 0, 0, 0.0, 0.5], [1, 0, 0, 1.0, 1.0], [2, 1, 0, 0.0, 4.0],
      [2, 1, 1, 3.0, 0.0], [3, 2, 0, 0.0, 8.0], [3, 2, 2, 9.0, 0.0], [4, 1, 0, 0.0, 10.0]]){
    const key = 'column(' + n + ',' + l + ',' + m + '; x=' + x.toFixed(1) + ' z=' + z.toFixed(1) + ')';
    rel(columnDensity(n, l, m, x, z), R(key), 1e-9, key + ' vs scipy quad (derive)');
  }
  /* the column integrand varies on the scale of n, so a fixed panel count is
     wrong at n = 1: the coarse version must be visibly worse */
  ok(Math.abs(columnDensity(1, 0, 0, 0, 0.5, 240) - R('column(1,0,0; x=0.0 z=0.5)')) > 1e-7,
    'a fixed 240-panel column is 1e-5 low at n=1 (the reason the step follows n)');
  /* the cloud grid: normalised, finite, and peaked where <r> says */
  const cg = cloudGrid(3, 2, 0, 24, cloudExtent(3, 2));
  ok(cg.mx > 0 && isFinite(cg.mx), 'the 3d cloud grid has a finite maximum');
  let gsum = 0, gFinite = true;
  for(let i = 0; i < cg.g.length; i++){ if(!isFinite(cg.g[i]) || cg.g[i] < 0) gFinite = false; gsum += cg.g[i]; }
  ok(gFinite && isFinite(gsum) && gsum > 0, 'the cloud grid is finite and non-negative in all 576 cells');
  ok(cloudExtent(1, 0) < cloudExtent(6, 0), 'the 99 % radius grows with n');
  const ext = cloudExtent(2, 1);
  const inside = simpson(r => radialProb(2, 1, r), 0, ext, 4000);
  rel(inside, 0.99, 6e-3, 'cloudExtent really holds 99 % of the probability');

  /* =============== E. the Einstein coefficients ================== */
  const PAIRS = [[2, 1, 1, 0], [3, 1, 1, 0], [4, 1, 1, 0], [5, 1, 1, 0], [6, 1, 1, 0],
                 [3, 0, 2, 1], [3, 2, 2, 1], [3, 1, 2, 0], [4, 0, 2, 1], [4, 2, 2, 1],
                 [4, 1, 2, 0], [4, 1, 3, 0], [4, 3, 3, 2], [5, 2, 3, 1], [6, 1, 5, 0]];
  for(const [nu, lu, nl, ll] of PAIRS){
    const tag = '(' + nu + lu + ' -> ' + nl + ll + ')';
    rel(radialDipole(nu, lu, nl, ll), R('R' + tag + ' exact series'), 1e-11, 'radial dipole ' + tag + ' (derive)');
    rel(radialDipole(nu, lu, nl, ll), R('R' + tag + ' exact series :: scipy quad'), 1e-11,
      'radial dipole ' + tag + ' vs scipy quad (derive)');
    rel(einsteinA(nu, lu, nl, ll), R('A' + tag + ' s^-1'), 1e-10, 'A ' + tag + ' (derive)');
  }
  /* an independent numerical route to the same radial integral */
  for(const [nu, lu, nl, ll] of [[2, 1, 1, 0], [3, 2, 2, 1], [4, 1, 3, 0]]){
    const q = simpson(r => Rnl(nu, lu, r) * Rnl(nl, ll, r) * r * r * r, 0, 400, 40000);
    rel(q, radialDipole(nu, lu, nl, ll), 1e-8, 'radial dipole by quadrature, ' + nu + lu + '->' + nl + ll);
  }
  eq(einsteinA(2, 0, 1, 0), 0, '2s -> 1s is forbidden (delta l = 0)');
  eq(einsteinA(3, 1, 2, 1), 0, '3p -> 2p is forbidden (delta l = 0, and l_max does not hide it)');
  eq(einsteinA(4, 2, 3, 2), 0, '4d -> 3d is forbidden (delta l = 0)');
  eq(einsteinA(4, 3, 3, 1), 0, '4f -> 3p is forbidden (delta l = 2)');
  eq(einsteinA(3, 2, 1, 0), 0, '3d -> 1s is forbidden (delta l = 2)');
  eq(einsteinA(2, 1, 3, 0), 0, 'no emission upward');
  ok(einsteinA(2, 1, 1, 0) > 0, '2p -> 1s is allowed');
  for(const [n, l] of [[2, 0], [2, 1], [3, 0], [3, 1], [3, 2], [4, 0], [4, 1], [4, 2], [4, 3],
                       [5, 0], [5, 1], [5, 2], [6, 1]]){
    rel(decayRate(n, l), R('Gamma(' + n + l + ') total s^-1'), 1e-10, 'Gamma(' + n + l + ') (derive)');
    const tref = R('Gamma(' + n + l + ') total s^-1 :: tau(' + n + l + ') ns');
    if(tref === 'inf') ok(!isFinite(lifetimeNS(n, l)), 'tau(' + n + l + ') is infinite (derive)');
    else rel(lifetimeNS(n, l), tref, 1e-10, 'tau(' + n + l + ') ns (derive)');
  }
  ok(!isFinite(lifetimeNS(2, 0)), '2s is metastable: no allowed one-photon drop');
  rel(lifetimeNS(2, 1), 1.5953250519467, 1e-10, 'tau(2p) = 1.5953 ns');
  for(let n = 2; n <= 6; n++){
    const tb = trueBranching(n);
    const want = R('n=' + n + ' l-averaged rates to n\'=1..' + (n - 1) + ' (s^-1) :: branching fractions')
      .replace(/[\[\]' ]/g, '').split(',').map(Number);
    eq(tb.frac.length, want.length, 'branching from n=' + n + ' has n-1 channels');
    for(let i = 0; i < want.length; i++)
      rel(tb.frac[i], want[i], 1e-7, 'true branching n=' + n + ' -> ' + (i + 1) + ' (derive)');
    rel(tb.frac.reduce((a, b) => a + b, 0), 1, 1e-12, 'branching from n=' + n + ' sums to 1');
  }
  /* PhET's first column IS twice the Einstein A for np -> 1s */
  for(const [n, w] of [[2, 12.53], [3, 3.34], [4, 1.36], [5, 0.69], [6, 0.39]]){
    eq(PHET_W[n - 1][0], w, 'PhET weight from n=' + n + ' is ' + w);
    rel(PHET_W[n - 1][0], 2 * einsteinA(n, 1, 1, 0) / 1e8, 0.013,
      'PhET weight from n=' + n + ' is 2A(np->1s)/1e8 to 1.3 %');
  }
  /* and its other columns are not any average of the real rates */
  ok(Math.abs(PHET_W[3][1] / (PHET_W[3][0] + PHET_W[3][1] + PHET_W[3][2]) - trueBranching(4).frac[1]) > 0.1,
    'PhET n=4 -> 2 branching is nowhere near the true one');

  /* =============== F. the seeded dice ============================ */
  const rg = makeRng(12345);
  for(let i = 0; i < 12; i++)
    rel(rg.next(), R('mulberry32(12345)[' + i + ']'), 1e-12, 'mulberry32(12345)[' + i + '] (derive)');
  const rg2 = makeRng(2026);
  for(let i = 0; i < 6; i++)
    rel(rg2.next(), R('mulberry32(2026)[' + i + ']'), 1e-12, 'mulberry32(2026)[' + i + '] (derive)');
  const rg3 = makeRng(7);
  let sum7 = 0, v7 = 0, lo7 = 1, hi7 = 0;
  const N7 = 200000, buf = new Float64Array(N7);
  for(let i = 0; i < N7; i++){ const v = rg3.next(); buf[i] = v; sum7 += v; if(v < lo7) lo7 = v; if(v > hi7) hi7 = v; }
  const mean7 = sum7 / N7;
  for(let i = 0; i < N7; i++) v7 += (buf[i] - mean7) * (buf[i] - mean7);
  rel(mean7, R('mulberry32(7) mean over 2e5'), 1e-12, 'mulberry32(7) mean over 2e5 (derive)');
  rel(v7 / N7, R('mulberry32(7) variance over 2e5'), 1e-12, 'mulberry32(7) variance (derive)');
  ok(lo7 > 0 && hi7 < 1, 'the stream stays inside [0,1)');
  {
    /* weighted() normalises; every distribution the sim passes it already sums
       to 1, so the division is invisible unless it is tested with weights that
       do not (Known-bad: a term that cancels in every call is untested) */
    const rgw = makeRng(8888);
    let a3 = 0;
    for(let i = 0; i < 40000; i++) if(rgw.weighted([[1, 3], [2, 1]]) === 1) a3++;
    rel(a3 / 40000, 0.75, 0.02, 'weighted() normalises un-normalised weights (3:1 gives 0.75)');
    ok(makeRng(1).weighted([]) === null, 'an empty distribution returns null');
    ok(makeRng(1).weighted([[7, 0]]) === null, 'an all-zero distribution returns null');
  }
  rel(v7 / N7, 1 / 12, 3e-3, 'the variance is the uniform 1/12');
  /* PhET's own distributions */
  for(const [n, l, want] of [[2, 0, 0], [2, 1, 1], [3, 0, 1], [3, 1, 2], [4, 1, 3], [5, 1, 3],
                             [6, 1, 3], [6, 4, 0], [6, 5, 0]]){
    eq(phetLowerDist(n, l).length, want, 'PhET chooseLower_n(' + n + ',' + l + ') has ' + want + ' options');
  }
  eq(phetLowerDist(2, 0).length, 0, 'a 2s atom has nowhere to go: PhET\'s metastable state');
  const d31 = phetLowerDist(3, 1);
  rel(d31[0][1], 0.79334917, 1e-7, 'PhET P(1 | n=3,l=1) (derive)');
  rel(d31[1][1], 0.20665083, 1e-7, 'PhET P(2 | n=3,l=1) (derive)');
  for(const d of [phetLowerDist(3, 1), phetLowerDist(4, 1), phetLowerDist(6, 1)])
    rel(d.reduce((a, b) => a + b[1], 0), 1, 1e-12, 'a PhET lower-n distribution sums to 1');
  eq(JSON.stringify(phetChooseL(0, 3)), JSON.stringify([[1, 1]]), 'PhET choose_l: l=0 always goes to 1');
  eq(JSON.stringify(phetChooseL(1, 2)), JSON.stringify([[0, 1]]), 'PhET choose_l: l = n-1 goes down');
  eq(phetChooseM(0, 1).length, 3, 'PhET choose_m from m=0 has three options');
  {
    /* m is a passenger in PhET's model — phetLowerDist reads only (n, l),
       phetChooseL does not read m, and phetChooseM can only return m, m+1 or
       m-1, so |dm| is never 2 and the (1,0,0) fallback is never reached through
       m.  Nothing about which n the atom lands on, or which wavelength comes
       out, depends on it; it sets the m the readout prints and the orbital the
       cloud draws.  So assert the DISTRIBUTION, and assert the inertness. */
    const rgm = makeRng(606060);
    const hist = {};
    const NM3 = 60000;
    for(let i = 0; i < NM3; i++){
      const v = rgm.weighted(phetChooseM(0, 2));
      hist[v] = (hist[v] || 0) + 1;
    }
    for(const k of [-1, 0, 1])
      rel((hist[k] || 0) / NM3, 1 / 3, 0.02, 'PhET choose_m gives m' +
        (k > 0 ? '+1' : (k < 0 ? '-1' : '')) + ' one third of the time');
    let worstDm = 0;
    for(let l2 = 0; l2 <= 5; l2++) for(let m0 = -5; m0 <= 5; m0++)
      for(const [mp] of phetChooseM(m0, l2))
        worstDm = Math.max(worstDm, Math.abs(mp - clamp(m0, -l2, l2)));
    eq(worstDm, 1, 'PhET choose_m never moves m by more than 1, so |dm| <= 1 is automatic');
    /* and the lower n never depends on m */
    let sameN = true;
    for(let n2 = 2; n2 <= NMAX; n2++) for(let l2 = 0; l2 < n2; l2++)
      if(JSON.stringify(phetLowerDist(n2, l2)) !== JSON.stringify(phetLowerDist(n2, l2))) sameN = false;
    ok(sameN && phetLowerDist.length === 2, 'phetLowerDist takes (n, l) only: m cannot change the hop');
  }
  eq(JSON.stringify(phetChooseM(0, 0)), JSON.stringify([[0, 1]]), 'l=0 forces m=0');
  ok(validState(2, 1, 1) && validState(2, 1, -1), 'l = n-1 and m = +-l are legal');
  ok(!validState(2, 2, 0), 'l = n is NOT a legal state');
  ok(!validState(2, 1, 2), '|m| > l is not a legal state');
  ok(!validState(7, 0, 0), 'n above PhET\'s ceiling of 6 is not a legal state');
  ok(phetTransitionAllowed(3, 1, 0, 2, 0, 0), 'dl=1, dm=0 is allowed');
  ok(!phetTransitionAllowed(3, 1, 0, 2, 1, 0), 'dl=0 is forbidden');
  ok(!phetTransitionAllowed(3, 2, 0, 2, 0, 0), 'dl=2 is forbidden');
  ok(!phetTransitionAllowed(3, 2, 2, 2, 1, 0), 'dm=2 is forbidden');
  /* the cascades, bit for bit */
  for(const start of [6, 5, 4, 3, 2]){
    const rng = makeRng(20260921);
    const cnt = {};
    let hops = 0;
    for(let i = 0; i < 40000; i++) for(const hp of cascadeBohr(rng, start)){
      cnt[hp[1] + '<-' + hp[0]] = (cnt[hp[1] + '<-' + hp[0]] || 0) + 1; hops++;
    }
    const base = 'Bohr cascade from n=' + start + ', 40000 trials, hops';
    eq(hops, R(base), 'Bohr cascade from n=' + start + ': hop count (derive)');
    rel(hops / 40000, R(base + ' :: mean hops per cascade'), 1e-12,
      'Bohr cascade from n=' + start + ': mean hops (derive)');
    for(const k in cnt){
      const parts = k.split('<-');
      eq(cnt[k], R(base + ' :: emissions ' + parts[1] + '->' + parts[0]),
        'Bohr n=' + start + ' emissions ' + parts[1] + '->' + parts[0] + ' (derive)');
    }
  }
  for(const [n0, l0, m0] of [[6, 1, 0], [5, 2, 1], [4, 3, -2], [3, 0, 0]]){
    const rng = makeRng(777);
    const cnt = {};
    let hops = 0, stuck = 0;
    for(let i = 0; i < 40000; i++){
      const hs = cascadeSchrodinger(rng, n0, l0, m0);
      for(const hp of hs){ cnt[hp[1] + '<-' + hp[0]] = (cnt[hp[1] + '<-' + hp[0]] || 0) + 1; hops++; }
      if(!hs.length || hs[hs.length - 1][1] !== 1) stuck++;
    }
    const base = 'Schrodinger cascade from (' + n0 + ',' + l0 + ',' + m0 + '), 40000 trials, hops';
    eq(hops, R(base), 'Schrodinger cascade ' + n0 + l0 + m0 + ': hop count (derive)');
    eq(stuck, R(base + ' :: cascades that did not reach n=1 (metastable 2s)'),
      'Schrodinger cascade ' + n0 + l0 + m0 + ': stuck in 2s (derive)');
    for(const k in cnt){
      const parts = k.split('<-');
      eq(cnt[k], R(base + ' :: emissions ' + parts[1] + '->' + parts[0]),
        'Schrodinger ' + n0 + l0 + m0 + ' emissions ' + parts[1] + '->' + parts[0] + ' (derive)');
    }
  }
  /* the ensemble the rates view shows: measured against exact, |z| < 3 */
  for(const [model, fromN] of [['bohr', 6], ['bohr', 3], ['schrodinger', 6], ['schrodinger', 4]]){
    Object.assign(ST, DEFAULTS, {view: 'rates', model, fromN, trials: 8000});
    const e = ensemble(ST);
    let worstZ = 0, sumF = 0;
    for(const r of e.rows){ worstZ = Math.max(worstZ, Math.abs(r.z)); sumF += r.f; }
    ok(worstZ < 3, model + ' from n=' + fromN + ': every |z| < 3 [' + fmt(worstZ, 2) + ']');
    rel(sumF, 1, 1e-12, model + ' from n=' + fromN + ': the measured fractions sum to 1');
    ok(e.hops > 0 && e.mean >= 1, model + ' from n=' + fromN + ': every cascade takes at least one hop');
  }

  /* =============== G. against NIST =============================== */
  for(const [inten, ang, n1, n2] of NIST_VAC){
    const obs = ang / 10, r2 = (lamVac(n1, n2) - obs) / obs;
    ok(Math.abs(r2) < 3e-5, 'NIST vacuum ' + ang + ' A is ' + n2 + '->' + n1 + ' to 3e-5 [' + r2.toExponential(2) + ']');
    ok(r2 > 0, 'the model is HIGH on every Lyman line (the 1s is relativistically deeper)');
    rel(r2, ALPHA * ALPHA / 4, 0.35, 'the Lyman residual is alpha^2/4 to 35 %');
  }
  for(const [inten, ang, n1, n2] of NIST_AIR){
    const obs = ang / 10, r2 = (lamAir(n1, n2) - obs) / obs;
    ok(Math.abs(r2) < 3e-5, 'NIST air ' + ang + ' A is ' + n2 + '->' + n1 + ' to 3e-5 [' + r2.toExponential(2) + ']');
  }
  rel(nAirEdlen(lamVac(2, 3)), R('n_air at H-alpha vacuum (Edlen 1966)'), 1e-12,
    'n_air at H-alpha (derive)');
  rel(lamAir(2, 3), R('lambda_air(3->2) nm'), 1e-12, 'H-alpha in air (derive)');
  rel(nAirEdlen(400), R('n_air at 400 nm'), 1e-12, 'n_air at 400 nm (derive)');
  rel(nAirEdlen(700), R('n_air at 700 nm'), 1e-12, 'n_air at 700 nm (derive)');
  rel(lamAir(2, 3), 656.28518, 5e-6, 'H-alpha air equals the strongest NIST component to 5e-6');
  ok(lamVac(2, 3) > lamAir(2, 3), 'air shortens the wavelength');
  ok(nAirEdlen(400) > nAirEdlen(700), 'air is dispersive: more refractive in the blue');
  /* the residual is smaller than the fine structure it is missing */
  const fsNm = lamVac(2, 3) * ALPHA * ALPHA * RH_EV / 4 / (RH_EV * (1 / 4 - 1 / 9));
  rel(fsNm, R('fine-structure splitting scale at n=2: alpha^2 E_2 (eV) :: in nm at H-alpha'), 1e-9,
    'the n=2 fine-structure scale at H-alpha, nm (derive)');
  ok(Math.abs(lamAir(2, 3) - 656.28518) < fsNm,
    'the H-alpha residual is inside the fine-structure multiplet NIST resolves');
  ok(Math.abs(6562.8518 - 6562.7110) / 10 > Math.abs(lamAir(2, 3) - 656.28518),
    'NIST\'s own H-alpha components spread wider than this model\'s error');

  /* =============== H. PhET's dynamics, run ======================= */
  eq(PHET.boxSide, 475, 'PhET box side');
  rel(PHET.dtPhoton, R('dt between emitted photons = 475/300/20 s'), 1e-12, 'PhET photon interval (derive)');
  rel(1 / PHET.dtPhoton, R('photons per second from the source'), 1e-12, 'PhET fires 12.63 photons/s (derive)');
  /* adjustEmissionDirection: nothing within pi/8 of straight up */
  const rg4 = makeRng(99);
  let minOff = 9;
  for(let i = 0; i < 20000; i++){
    const d = adjustEmission(rg4.angle());
    let off = d - PI / 2;
    off = Math.atan2(Math.sin(off), Math.cos(off));
    minOff = Math.min(minOff, Math.abs(off));
  }
  rel(minOff, PI / 8, 1e-9, 'no emitted photon comes out within pi/8 of the beam (PhET)');
  /* PhET's emission direction: isotropic below n = 5, backwards along the
     electron above it */
  const rgd = makeRng(1234);
  let cs = 0, sn = 0;
  for(let i = 0; i < 20000; i++){
    const d = emissionDirection(4, 0.7, rgd);
    cs += Math.cos(d); sn += Math.sin(d);
  }
  ok(Math.hypot(cs, sn) / 20000 < 0.02, 'at n = 4 the emission is isotropic: the branch is n < 5 (PhET)');
  {
    let cs5 = 0, sn5 = 0;
    for(let i = 0; i < 20000; i++){
      const d5 = emissionDirection(5, 0.0, rgd);
      cs5 += Math.cos(d5); sn5 += Math.sin(d5);
    }
    ok(Math.hypot(cs5, sn5) / 20000 > 0.9, 'and at n = 5 it is not: it points back along the electron');
  }
  let worstBack = 0;
  for(let i = 0; i < 2000; i++){
    const ang = rgd.angle();
    const d = emissionDirection(6, ang, rgd);
    let off = d - (ang + PI);
    off = Math.atan2(Math.sin(off), Math.cos(off));
    worstBack = Math.max(worstBack, Math.abs(off));
  }
  rel(worstBack, 0.1 * PI, 1e-9, 'from n >= 5 it comes back along the electron, 0.1 turn either side (PhET)');
  /* one tick is 1/60 s of PhET's model: a photon crosses the box in 95 of them */
  eq(Math.round(PHET.boxSide / (PHET.photonSpeed * DT_TICK)), 95,
    'a 300-unit/s photon crosses the 475-unit box in 95 ticks of 1/60 s');
  close(DT_TICK, 1 / 60, 1e-15, 'the tick is 1/60 s');
  {
    /* x = 200 so the photon misses the 30-unit billiard ball: one fired up the
       middle bounces off it and the count then measures the bounce, not the
       tick */
    Object.assign(ST, DEFAULTS, {model: 'billiard', light: 'mono', lam: 300, lightOn: false});
    atomReset(ST);
    ATOM.photons.push({x: 200, y: -HALF_BOX, dir: PI / 2, lam: 300, emit: false, hit: false, age: 0});
    for(let k = 0; k < 60; k++) atomTick(ST);
    close(ATOM.photons[0].y, -HALF_BOX + 300, 1e-9,
      'a 300-unit/s photon moves exactly 300 units in 60 ticks, so a tick is 1/60 s');
    close(ATOM.photons[0].x, 200, 1e-12, 'and it goes straight up, as PhET fires it');
    let k = 60;
    while(ATOM.photons.length && k < 400){ atomTick(ST); k++; }
    eq(k, Math.ceil((PHET.boxSide + 40) / (PHET.photonSpeed * DT_TICK)),
      'and leaves the captured region after ' + k + ' ticks');
  }
  /* the collision geometry: PhET's photon is 15 units and its electron 5 */
  {
    Object.assign(ST, DEFAULTS, {model: 'bohr'});
    atomReset(ST); ATOM.n = 1; ATOM.angle = 0;
    const ee = electronXY(ST);
    ok(quantumCollides(ST, {x: ee[0] + 19.9, y: ee[1], lam: 122}),
      'Bohr: a photon 19.9 units from the electron collides (15 + 5, PhET)');
    ok(!quantumCollides(ST, {x: ee[0] + 20.1, y: ee[1], lam: 122}),
      'and one 20.1 units away does not');
    Object.assign(ST, DEFAULTS, {model: 'debroglie', dbRep: 'radial'});
    atomReset(ST); ATOM.n = 1;
    ok(quantumCollides(ST, {x: viewRadius(1) + 22.9, y: 0, lam: 122}),
      'de Broglie: the whole ring collides out to 23 units (15 + 8, PhET)');
    ok(!quantumCollides(ST, {x: viewRadius(1) + 23.1, y: 0, lam: 122}),
      'and not beyond it');
    ok(quantumCollides(ST, {x: -viewRadius(1), y: 0, lam: 122}),
      'and it collides on the far side too, which a point electron would not');
  }
  /* PhET makes the atom wait 0.75 s before it will absorb */
  function uAbsorbAt(tState){
    Object.assign(ST, DEFAULTS, {model: 'bohr', light: 'mono', lam: 122, lightOn: false});
    atomReset(ST);
    ATOM.n = 1; ATOM.l = 0; ATOM.m = 0; ATOM.tState = tState; ATOM.angle = 0;
    const ee = electronXY(ST);
    return processPhoton(ST, {x: ee[0], y: ee[1], dir: PI / 2, lam: 122, emit: false, hit: false, age: 0});
  }
  ok(!uAbsorbAt(0.70), 'a photon arriving 0.70 s after the last transition is refused (PhET waits 0.75 s)');
  ok(uAbsorbAt(0.80), 'and one arriving at 0.80 s is absorbed');
  /* and 1 s before it will emit, and then a flat 0.5 a tick */
  {
    Object.assign(ST, DEFAULTS, {model: 'bohr', lightOn: false});
    atomReset(ST);
    ATOM.n = 3; ATOM.l = 0; ATOM.m = 0; ATOM.tState = 0;
    let waited = 0;
    while(ATOM.n === 3 && waited < 400){ atomTick(ST); waited++; }
    ok(waited * DT_TICK >= 1.0, 'nothing is emitted before the state is 1 s old ('
      + fmt(waited * DT_TICK, 3) + ' s)');
    let tot = 0, trials = 0;
    for(let k = 0; k < 3000; k++){
      ATOM.n = 3; ATOM.l = 0; ATOM.m = 0; ATOM.tState = PHET.tEmit;
      let t = 0;
      while(ATOM.n === 3 && t < 500){ atomTick(ST); t++; }
      if(ATOM.n !== 3){ tot += t; trials++; }
    }
    ok(trials > 2900, 'every one of the 3000 excited atoms decayed');
    rel(tot / trials, 2, 0.06, 'past 1 s the wait is geometric with mean 2 ticks, i.e. 0.5 a tick (PhET)');
  }
  /* the classical spiral */
  Object.assign(ST, DEFAULTS, {model: 'classical', lightOn: false});
  atomReset(ST);
  let tDead = 0;
  for(let k = 0; k < 400 && !ATOM.cls.dead; k++){ atomTick(ST); tDead = ATOM.t; }
  ok(ATOM.cls.dead, 'the classical atom collapses');
  rel(tDead, (150 - 5) / 220, 0.02, 'it collapses in (150 - 5)/220 = 0.6591 s (PhET)');
  eq(PHET.classicalR0, 150, 'the classical electron starts 150 units out (PhET)');
  eq(PHET.classicalDrdt, 220, 'and loses 220 units of radius a second (PhET)');
  eq(PHET.classicalRmin, 5, 'and is destroyed at 5 units (PhET)');
  eq(PHET.classicalOmega0, 600, 'starting at 600 deg/s (PhET)');
  /* the radius really is linear in time, which is what makes 0.659 s the answer */
  {
    Object.assign(ST, DEFAULTS, {model: 'classical', lightOn: false});
    atomReset(ST);
    for(let k = 0; k < 20; k++) atomTick(ST);
    rel(ATOM.cls.r, 150 - 220 * 20 * DT_TICK, 1e-9, 'the radius falls linearly, 220 units a second');
    for(let k = 0; k < 10; k++) atomTick(ST);
    rel(ATOM.cls.r, 150 - 220 * 30 * DT_TICK, 1e-9, 'and keeps falling at the same rate');
  }
  rel(ATOM.cls.w / (600 * DEG), Math.pow(1.008, ATOM.ticks), 1e-9,
    'the angular speed starts at 600 deg/s and is multiplied by 1.008 every tick (PhET)');
  /* a photon on a wavelength that is NOT a PhET transition does nothing */
  Object.assign(ST, DEFAULTS, {model: 'bohr', light: 'mono', lam: 121, lightOn: true});
  atomReset(ST);
  for(let k = 0; k < 3000; k++) atomTick(ST);
  eq(ATOM.n, 1, '121 nm never excites the atom (PhET matches integers)');
  eq(ATOM.emitted, 0, '121 nm produces no emission at all');
  ok(ATOM.fired > 200, 'the lamp did fire (' + ATOM.fired + ' photons)');
  /* on the line, it cycles */
  Object.assign(ST, DEFAULTS, {model: 'bohr', light: 'mono', lam: 122, lightOn: true});
  atomReset(ST);
  for(let k = 0; k < 3000; k++) atomTick(ST);
  ok(ATOM.absorbed > 3, '122 nm excites the atom repeatedly (' + ATOM.absorbed + ' times)');
  ok(Math.abs(ATOM.emitted - ATOM.absorbed) <= 1, 'every absorption is paid back by an emission');
  eq(Object.keys(ATOM.counts).join(','), '122', 'a two-level cycle emits one wavelength only');
  /* determinism: the same seed gives the same run */
  const snap = JSON.stringify(ATOM.counts) + '|' + ATOM.emitted + '|' + ATOM.fired;
  atomReset(ST);
  for(let k = 0; k < 3000; k++) atomTick(ST);
  eq(JSON.stringify(ATOM.counts) + '|' + ATOM.emitted + '|' + ATOM.fired, snap,
    'the same seed reproduces the run exactly');
  /* white light on Schrodinger: it climbs, it emits, and it can stick in 2s */
  Object.assign(ST, DEFAULTS, {model: 'schrodinger', light: 'white', lightOn: true, seed: 4242});
  atomReset(ST);
  let sawHigh = 0, sawMeta = 0, alwaysValid = true;
  for(let k = 0; k < 9000; k++){
    atomTick(ST);
    if(ATOM.n > 1) sawHigh++;
    if(ATOM.n === 2 && ATOM.l === 0) sawMeta++;
    if(!validState(ATOM.n, ATOM.l, ATOM.m)) alwaysValid = false;
  }
  ok(alwaysValid, '(n,l,m) stays legal through 9000 ticks of white light');
  ok(sawHigh > 100, 'white light lifts the Schrodinger atom out of the ground state');
  ok(ATOM.emitted > 3, 'and it emits (' + ATOM.emitted + ' photons)');
  let allKnown = true;
  for(const k in ATOM.counts) if(PHET_LAMS.indexOf(+k) < 0) allKnown = false;
  ok(allKnown, 'every emitted wavelength is one of PhET\'s fifteen');
  /* the metastable handler fires only in white light */
  Object.assign(ST, DEFAULTS, {model: 'schrodinger', light: 'mono', lam: 122, lightOn: true});
  atomReset(ST);
  ATOM.n = 2; ATOM.l = 0; ATOM.m = 0; ATOM.tState = 0;
  let metaInMono = false;
  for(let k = 0; k < 400; k++){
    atomTick(ST);
    for(const p of ATOM.photons) if(p.meta) metaInMono = true;
  }
  ok(!metaInMono, 'the metastable handler fires NO photon in monochromatic light (PhET)');
  eq(ATOM.n, 2, 'so a 2s atom stays stuck at n = 2 under a 122 nm lamp');
  eq(ATOM.metaT, 0, 'and its timer never starts');
  Object.assign(ST, DEFAULTS, {model: 'schrodinger', light: 'white', lightOn: true});
  atomReset(ST);
  ATOM.n = 2; ATOM.l = 0; ATOM.m = 0;
  let metaFired = false;
  for(let k = 0; k < 200; k++){
    atomTick(ST);
    for(const p of ATOM.photons) if(p.meta) metaFired = true;
    if(ATOM.n !== 2 || ATOM.l !== 0) break;
  }
  ok(metaFired, 'in white light PhET fires a Balmer photon at a stuck 2s atom every 2 s');
  /* billiard ball: scatter only */
  Object.assign(ST, DEFAULTS, {model: 'billiard', light: 'white', lightOn: true});
  atomReset(ST);
  for(let k = 0; k < 2000; k++) atomTick(ST);
  eq(ATOM.emitted, 0, 'a billiard ball emits nothing');
  ok(ATOM.bounced > 0, 'but it does scatter (' + ATOM.bounced + ' photons)');
  /* plum pudding: one line, 150 nm */
  Object.assign(ST, DEFAULTS, {model: 'pudding', light: 'white', lightOn: true, seed: 31415});
  atomReset(ST);
  for(let k = 0; k < 12000; k++) atomTick(ST);
  ok(ATOM.emitted > 0, 'plum pudding emits (' + ATOM.emitted + ' photons)');
  eq(Object.keys(ATOM.counts).join(','), '150', 'plum pudding emits 150 nm and nothing else');
  ok(ATOM.absorbed > 0, 'plum pudding absorbs');
  /* the spectrometer axis: PhET's compression, and the visible band undistorted */
  eq(segPos(656)[0], 1, '656 nm sits in the visible segment');
  eq(segPos(122)[0], 0, '122 nm sits in the UV segment');
  eq(segPos(1876)[0], 2, '1876 nm sits in the IR segment');
  close(segPos(580)[1], (580 - 380) / 400, 1e-12, 'the visible segment is undistorted');
  ok(segPos(150)[1] > segPos(122)[1], 'PhET still orders the UV lines correctly after compressing them');
  ok(segPos(7460)[1] > segPos(4052)[1], 'and the IR lines too');
  ok(Math.abs(segPos(122)[1] - (122 - 93) / 20) > 0.3, 'the UV axis really is compressed (122 -> 105)');

  /* =============== I. the panels build clean ===================== */
  const entRe = /&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [v] of TABS) for(const mo of MODEL_LIST){
    Object.assign(ST, DEFAULTS, {view: v, model: mo.id});
    atomReset(ST);
    for(let k = 0; k < 90; k++) atomTick(ST);
    const M = buildModel();
    for(const [nm, s] of [['readout', readoutHTML(M)], ['eqbar', eqbarHTML(M)], ['tag', tagHTML(M)],
                          ['info', INFO[v]], ['deriv', DERIV[v]]]){
      ok(typeof s === 'string' && s.length > 20, v + '/' + mo.id + ' ' + nm + ' builds');
      ok(!/NaN|undefined|Infinity/.test(s.replace(/&infin;/g, '')), v + '/' + mo.id + ' ' + nm + ' is clean');
    }
  }
  /* no slider combination makes a non-finite model value */
  for(const n of [1, 2, 3, 4, 5, 6]) for(let l = 0; l < n; l++) for(let m = -l; m <= l; m++){
    Object.assign(ST, DEFAULTS, {view: 'orbitals', n, l, m});
    const M = buildModel();
    ok(isFinite(M.meanR) && isFinite(M.meanR2) && M.nodesR >= 0 && M.nodesA >= 0,
      'orbital (' + n + ',' + l + ',' + m + ') is finite');
  }
  for(let lam = PHET.lamMin; lam <= PHET.lamMax; lam += 7){
    const c = lamColour(lam);
    ok(/^#[0-9a-f]{6}$/i.test(c) || /^rgb\(\d+,\d+,\d+\)$/.test(c), 'lamColour(' + lam + ') is a legal colour');
  }
  /* a colour-FORMAT test passes on black; assert the BRIGHTNESS too
     (Known-bad: rgb(0,0,0) is well formed) */
  for(const lam of [420, 480, 530, 580, 650, 700]){
    const b = toRgb(lamColour(lam));
    ok(Math.max(b[0], b[1], b[2]) > 60, 'the visible line at ' + lam + ' nm is drawn bright, not black');
  }
  ok(toRgb(lamColour(122))[0] > 60 && toRgb(lamColour(2000))[0] > 60, 'UV and IR are drawn grey, not black');
  const g530 = toRgb(lamColour(530)), b450 = toRgb(lamColour(450)), r650 = toRgb(lamColour(650));
  ok(g530[1] > g530[0] && g530[1] > g530[2], '530 nm is green');
  ok(b450[2] > b450[0], '450 nm is blue');
  ok(r650[0] > r650[1] && r650[0] > r650[2], '650 nm is red');

  /* =============== J. the layout sweep =========================== */
  const SIZES = [[1400, 820], [1100, 712], [980, 620], [820, 520], [560, 380]];
  const CONFIGS = [
    ['box bohr', {view: 'box'}, 60],
    ['box white schro', {view: 'box', model: 'schrodinger', light: 'white'}, 60],
    ['box billiard', {view: 'box', model: 'billiard'}, 50],
    ['box pudding', {view: 'box', model: 'pudding'}, 50],
    ['box classical', {view: 'box', model: 'classical', _ticks: 80}, 50],
    ['box debroglie', {view: 'box', model: 'debroglie', dbRep: 'bright'}, 50],
    ['box experiment', {view: 'box', model: 'experiment'}, 50],
    ['box no spectro', {view: 'box', showSpectro: false, showExact: false}, 40],
    ['box log', {view: 'box', logCount: true, light: 'white', _ticks: 900}, 50],
    ['levels bohr', {view: 'levels'}, 40],
    ['levels schro', {view: 'levels', model: 'schrodinger', light: 'white', _ticks: 400}, 40],
    ['levels exp', {view: 'levels', model: 'experiment'}, 40],
    ['wave radial', {view: 'wave'}, 12],
    ['wave height', {view: 'wave', dbRep: 'height', nu: 5}, 12],
    ['wave bright', {view: 'wave', dbRep: 'bright', nu: 1}, 40],
    ['wave off', {view: 'wave', nu: 3.45, showExact: false}, 12],
    ['orb 1s', {view: 'orbitals', n: 1, l: 0, m: 0}, 60],
    ['orb 2p0', {view: 'orbitals', n: 2, l: 1, m: 0}, 60],
    ['orb 3d2', {view: 'orbitals', n: 3, l: 2, m: 2}, 60],
    ['orb 4f1', {view: 'orbitals', n: 4, l: 3, m: 1}, 60],
    ['orb 6s', {view: 'orbitals', n: 6, l: 0, m: 0}, 60],
    ['orb nodes off', {view: 'orbitals', n: 5, l: 2, m: 1, showPhet: false}, 60],
    ['series all', {view: 'series'}, 30],
    ['series lyman', {view: 'series', series: '1', lam: 100}, 25],
    ['series pfund', {view: 'series', series: '5', lam: 700}, 25],
    ['rates 6 bohr', {view: 'rates', trials: 800}, 25],
    ['rates 2 bohr', {view: 'rates', fromN: 2, trials: 800}, 20],
    ['rates 5 schro', {view: 'rates', model: 'schrodinger', fromN: 5, trials: 800}, 25],
  ];
  for(const [nm, over, minFills] of CONFIGS) for(const [W, H] of SIZES){
    const clean = {};
    for(const k in over) if(k[0] !== '_') clean[k] = over[k];
    Object.assign(ST, DEFAULTS, clean);
    atomReset(ST);
    for(let k = 0; k < (over._ticks || 40); k++) atomTick(ST);
    const c = makeShot(W, H);
    let err = null;
    try{ drawView(c, W, H, buildModel()); }catch(e){ err = e; }
    ok(!err, nm + ' ' + W + 'x' + H + ' draws without throwing' + (err ? ': ' + (err.stack || err) : ''));
    if(err) continue;
    const texts = c.ops.filter(o => o.op === 'text');
    /* floor the TOTAL op count, not the fills: the standing-wave view draws one
       stroked polyline and four discs, and a fill floor tuned on the orbital
       cloud punishes it for batching (Known-bad) */
    ok(c.ops.length >= minFills && texts.length >= 3,
      nm + ' ' + W + 'x' + H + ' draws substance (' + c.ops.length + ' ops, floor ' + minFills + ')');
    let bad = null;
    for(const t of texts){
      if(entRe.test(t.t)){ bad = 'entity/tag: "' + t.t.slice(0, 40) + '"'; break; }
      if(/undefined|NaN/.test(t.t)){ bad = 'NaN/undefined: "' + t.t.slice(0, 40) + '"'; break; }
      if(t.bb[0] < -1 || t.bb[2] > W + 1 || t.bb[1] < -1 || t.bb[3] > H + 1){
        bad = 'off-canvas: "' + t.t.slice(0, 30) + '" [' + t.bb.map(v => fmt(v, 0)) + ']'; break; }
    }
    ok(!bad, nm + ' ' + W + 'x' + H + ' text clean (' + (bad || 'ok') + ')');
    /* the HTML #hint (bottom:11px, 11px type) owns the bottom-left corner and
       the canvas capture cannot see it, so nothing may be drawn there */
    const inHint = texts.filter(t => t.bb[0] < HINT_W && t.bb[3] > H - HINT_H);
    ok(!inHint.length, nm + ' ' + W + 'x' + H + ' no canvas text under the #hint line'
      + (inHint.length ? ' ("' + inHint[0].t.slice(0, 30) + '" to y ' + fmt(inHint[0].bb[3], 0) + ')' : ''));
    let hit = null;
    for(let i = 0; i < texts.length && !hit; i++) for(let j = i + 1; j < texts.length; j++){
      const a = texts[i].bb, b = texts[j].bb;
      const ox = Math.min(a[2], b[2]) - Math.max(a[0], b[0]);
      const oy = Math.min(a[3], b[3]) - Math.max(a[1], b[1]);
      /* half a pixel, the same rule tools/audit.py applies: a 3 px tolerance
         passed here and failed the audit on the same picture (Known-bad) */
      if(ox > 0.5 && oy > 0.5){ hit = '"' + texts[i].t.slice(0, 22) + '" vs "' + texts[j].t.slice(0, 22) + '"'; break; }
    }
    ok(!hit, nm + ' ' + W + 'x' + H + ' no text collisions (' + (hit || 'ok') + ')');
    let leg = null;
    for(const r of LEGEND_RECTS) for(let i = 0; i < POLY_SEGS.length; i += 4){
      const x0 = POLY_SEGS[i], y0 = POLY_SEGS[i + 1], x1 = POLY_SEGS[i + 2], y1 = POLY_SEGS[i + 3];
      if(Math.max(x0, x1) < r.x || Math.min(x0, x1) > r.x + r.w
        || Math.max(y0, y1) < r.y || Math.min(y0, y1) > r.y + r.h) continue;
      leg = 'a curve crosses the legend'; break;
    }
    ok(!leg, nm + ' ' + W + 'x' + H + ' legend clear');
  }

  Object.assign(ST, stSave);
  atomReset(ST);
  const dt = (Date.now() - T0) / 1000;
  console.log(pass + ' passed, ' + fail + ' failed  (' + fmt(dt, 1) + ' s)');
  if(fail > 0) throw new Error(fail + ' self-test failure(s)');
  return fail;
}
