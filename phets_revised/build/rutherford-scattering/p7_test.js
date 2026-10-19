
/* ================================================================== *
 *  selfTest — headless verification.  Every value labelled (derive)   *
 *  is a line of build/rutherford-scattering/refvals.txt, the printed   *
 *  output of derive.py, emitted into p7_refs.js by make_refs.py —      *
 *  no number in this file was typed by hand.                           *
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
  const close = (a, b, tol, name) => ok(Math.abs(a - b) <= tol, name + ' [' + a + ' vs ' + b + ']');
  const rel = (a, b, t, name) => ok(Math.abs(a - b) <= t * Math.abs(b || 1),
    name + ' [' + a + ' vs ' + b + ', rel ' + (Math.abs(a - b) / Math.abs(b || 1)).toExponential(2) + ']');
  const T0 = Date.now();
  const stSave = Object.assign({}, ST);
  Object.assign(ST, DEFAULTS);

  /* =============== A. constants ================================== */
  close(DEG * 90, PI / 2, 1e-12, 'DEG converts degrees INTO radians (90 deg = pi/2)');
  rel(E_Q, R('e (C)'), 1e-14, 'e (derive)');
  rel(EPS0, R('eps0 (F/m)'), 1e-14, 'eps0 (derive)');
  rel(KE, R('k = 1/(4 pi eps0) (N m^2/C^2)'), 1e-12, 'Coulomb constant, derived (derive)');
  rel(M_E, R('m_e (kg)'), 1e-14, 'm_e (derive)');
  rel(M_ALPHA, R('m_alpha (kg)'), 1e-14, 'alpha particle mass (derive)');
  rel(N_AVO, R('N_A (1/mol)'), 1e-14, 'N_A (derive)');
  /* k e^2 = 1.44 MeV fm is DERIVED here, not typed */
  rel(KE2_MEVFM, R('k e^2 (MeV fm)'), 1e-12, 'k e^2 in MeV fm, derived (derive)');
  rel(electronMaxDeflection(), R('max lab deflection off a free electron, rad (asin m_e/m_alpha)'),
    1e-12, 'asin(m_e/m_alpha), the free-electron bound (derive)');
  ok(electronMaxDeflection() < 2e-4, 'a free electron cannot turn an alpha by more than 1.4e-4 rad');

  /* =============== B. the closed forms ============================ */
  const D3 = 3;
  for(const b of [0.25, 0.5, 1, 2, 5, 20]){
    rel(thetaOfB(b, D3), R('theta(b=' + b + ', D=3) closed form, rad'), 1e-13,
      'theta(b=' + b + ') (derive)');
    /* the deflection integral has never been told tan(theta/2) = D/2b */
    /* the deflection integral returns pi MINUS something almost pi, so its
       error is absolute, not relative: at b = 20 the answer is 0.1497 and a
       5e-12 absolute residual reads as 3.4e-11 relative. */
    close(thetaQuad(b, r => D3 / r, 14), R('theta(b=' + b + ', D=3) closed form, rad'), 2e-11,
      'theta(b=' + b + ') by quadrature, an independent route');
  }
  rel(rminOfB(1, D3), R('rmin(b=1, D=3)'), 1e-13, 'r min at b = 1 (derive)');
  rel(rminOfB(3, D3), R('rmin(b=3, D=3)'), 1e-13, 'r min at b = 3 (derive)');
  /* r_min written the other way: (D/2)(1 + cosec(theta/2)) */
  for(const b of [0.5, 1, 3])
    rel(rminOfB(b, D3), 0.5 * D3 * (1 + 1 / Math.sin(thetaOfB(b, D3) / 2)), 1e-13,
      'r min = (D/2)(1 + cosec(theta/2)) at b = ' + b);
  rel(bOfTheta(PI / 2, D3), R('b(theta=90deg, D=3) = D/2'), 1e-14, 'b at 90 degrees is D/2 (derive)');
  rel(eccOfTheta(thetaOfB(1, D3)), R('eccentricity at b=1, D=3 (1/sin(theta/2))'), 1e-13,
    'eccentricity 1/sin(theta/2) (derive)');
  /* b(theta) inverts theta(b) */
  for(const b of [0.3, 2, 17]) rel(bOfTheta(thetaOfB(b, D3), D3), b, 1e-12, 'b(theta(b)) round trip at b = ' + b);
  /* the conic */
  for(const b of [0.5, 1, 4]){
    rel(phiInfOf(b, D3), R('phi_inf(b=' + b + ', D=3), rad'), 1e-13, 'phi_inf at b = ' + b + ' (derive)');
    rel(phiInfOf(b, D3), PI - thetaOfB(b, D3), 1e-13, 'phi_inf = pi - theta at b = ' + b);
    rel(rOfPhi(phiInfOf(b, D3) / 2, b, D3), rminOfB(b, D3), 1e-12,
      'the conic is smallest half way along, at b = ' + b);
    close(rOfPhi(1e-9, b, D3) * Math.sin(1e-9), b, 1e-6,
      'the incoming asymptote of the conic stands off by exactly b, at b = ' + b);
  }
  /* PhET's entry quadratic recovers the impact parameter of a point on the orbit */
  for(const [b, ph] of [[1, 0.3], [4, 0.1], [0.5, 0.8]]){
    const r0 = rOfPhi(ph, b, D3);
    const X0 = r0 * Math.sin(ph), Y0 = -r0 * Math.cos(ph);
    const brec = 0.5 * (X0 + Math.sqrt(X0 * X0 - 2 * D3 * (Y0 + r0)));
    rel(brec, R('b recovered at b=' + b + ' phi=' + ph), 1e-12, 'entry quadratic at b = ' + b + ' (derive)');
  }
  /* phiAtRadius inverts the conic on both branches */
  for(const b of [1, 8]) for(const r of [4, 20, 300]){
    if(r < rminOfB(b, D3)) continue;
    rel(rOfPhi(phiAtRadius(r, b, D3, false), b, D3), r, 1e-10, 'phiAtRadius in, b=' + b + ' r=' + r);
    rel(rOfPhi(phiAtRadius(r, b, D3, true), b, D3), r, 1e-10, 'phiAtRadius out, b=' + b + ' r=' + r);
  }
  /* the velocity angle runs from 0 on the way in to theta on the way out */
  for(const b of [0.5, 3, 30]){
    const th = thetaOfB(b, D3);
    close(velAngle(1e-7, b, D3), 0, 1e-5, 'the velocity starts along the incoming asymptote, b = ' + b);
    close(velAngle(phiInfOf(b, D3) * (1 - 1e-9), b, D3), th, 1e-5,
      'and ends along the outgoing one, b = ' + b);
    /* so a full tracked arc delivers exactly theta */
    rel(drawnTurn(b, D3, 1e11, 1e11), th, 1e-7, 'a tracked arc from infinity to infinity turns by theta, b = ' + b);
    ok(drawnTurn(b, D3, 40, 40) < th, 'and a finite box delivers less than theta, b = ' + b);
  }

  /* =============== C. the cross section =========================== */
  for(const d of [1, 5, 15, 30, 60, 90, 135, 179]){
    const th = d * PI / 180;
    rel(dsdoOf(th, D3), R('dsdo(' + d + ' deg, D=3) closed form'), 1e-12, 'dsdo at ' + d + ' deg (derive)');
    /* the Jacobian route: this is what catches a missing constant factor, and
       nothing about scaling, limits or monotonicity ever could */
    rel(dsdoNumeric(th, D3), dsdoOf(th, D3), 1e-7, 'dsdo at ' + d + ' deg from (b/sin theta)|db/dtheta|');
  }
  rel(dsdoOf(PI / 36, D3) / dsdoOf(PI / 2, D3), R('dsdo(5 deg)/dsdo(90 deg)'), 1e-12,
    '5 deg is 69059 times 90 deg (derive)');
  /* the 4 in (D/4)^2 is the constant a scaling test cannot see: pin it */
  /* sin^4(45 deg) is 1/4 exactly, so dsdo(90 deg) is D^2/4 and nothing else:
     an identity that moves if the 4 in (D/4)^2 does.  A ratio test cannot see
     that constant at all (Known-bad: a missing constant factor is invisible to
     every scaling, limiting and monotonicity assertion there is). */
  rel(dsdoOf(PI / 2, 4), 4, 1e-14, 'dsdo(90 deg, D=4) is exactly D^2/4 = 4, which pins the (D/4)^2');
  rel(dsdoOf(PI / 2, 7), 49 / 4, 1e-14, 'and D^2/4 again at D = 7');
  rel(dsdoOf(2 * PI / 3, 6), 4, 1e-13, 'dsdo(120 deg, D=6) is D^2/9 = 4, which pins it a second way');
  for(const d of [10, 90, 150])
    rel(sigmaBeyond(d * PI / 180, D3), R('sigma(>' + d + ' deg) quadrature'), 1e-12,
      'sigma beyond ' + d + ' deg = pi b^2 (derive)');
  /* and against a quadrature of dsdo dOmega taken here */
  const sig90 = simpson(t => dsdoOf(t, D3) * TAU * Math.sin(t), PI / 2, PI * (1 - 1e-9), 4000);
  rel(sig90, sigmaBeyond(PI / 2, D3), 2e-7, 'integrating dsdo over solid angle gives pi b(90)^2');
  ok(!isFinite(dsdoOf(0, D3)) || dsdoOf(1e-6, D3) > 1e20,
    'the total cross section diverges: dsdo blows up as theta goes to zero');

  /* =============== D. Newton's equations ========================== */
  {
    const io = integrateOrbit(2, 3, 400, 20000);
    ok(io.dE < 1e-9, 'energy is conserved along the integrated orbit [' + io.dE + ']');
    ok(io.dL < 1e-10, 'angular momentum is conserved [' + io.dL + ']');
    rel(io.L0, 2, 1e-12, 'L0 is b, with v_inf = 1');
    rel(io.E0, 0.5, 1e-12, 'E0 is half v_inf squared');
    rel(io.theta, thetaOfB(2, 3), 1e-4, 'RK4 reproduces 2 atan(D/2b)');
    /* the residual is a TRUNCATION whose rate is 1/r^2, measured not assumed */
    const c2 = Math.abs(io.theta - thetaOfB(2, 3)) * io.rEnd * io.rEnd;
    rel(c2, R('b=2, start y0=-400: final r :: residual * r_final^2 (constant => the rate is 1/r^2)'), 0.05,
      'residual x r_final^2 matches derive');
    const io2 = integrateOrbit(2, 3, 200, 20000);
    const c1 = Math.abs(io2.theta - thetaOfB(2, 3)) * io2.rEnd * io2.rEnd;
    rel(c1 / c2, 1, 0.05, 'and it is the same constant at half the distance, so the rate really is 1/r^2');
    ok(io.pts.length > 40, 'the integrated path is a usable polyline [' + io.pts.length / 2 + ' points]');
  }
  /* head-on: b = 0 exactly */
  close(thetaOfB(0, D3), PI, 1e-15, 'b = 0 gives exactly 180 degrees');
  rel(rminOfB(0, D3), D3, 1e-15, 'and r min is exactly D');
  rel(rminOfB(0, D3), R('rmin(b=0, D=3) = D'), 1e-15, 'r min at b = 0 (derive)');
  for(const b of [1e-2, 1e-3, 1e-4]){
    rel(rminOfB(b, D3) - D3, R('rmin(b=' + b + ') - D'), 2e-6, 'the b -> 0 rate of r min (derive)');
    rel(rminOfB(b, D3) - D3, b * b / D3, 1e-4, 'r min - D goes as b^2/D, at b = ' + b);
    rel(PI - thetaOfB(b, D3), 4 * b / D3, 1e-4, 'pi - theta goes as 4b/D, at b = ' + b);
  }
  /* the radial problem has a closed parametric solution; it must satisfy
     v^2 = 1 - D/r, which pins both halves of the parametrisation together */
  for(const eta of [0, 0.5, 2]){
    const r = 0.5 * D3 * (Math.cosh(eta) + 1);
    rel(r, R('radial parametric: eta=' + eta + ' -> r'), 1e-13, 'radial r(eta) (derive)');
    rel(0.5 * D3 * (Math.sinh(eta) + eta), R('radial parametric: eta=' + eta + ' -> r :: t'), 1e-13,
      'radial t(eta) (derive)');
    const drdt = Math.sinh(eta) / (Math.cosh(eta) + 1);
    close(drdt, Math.sqrt(Math.max(0, 1 - D3 / r)), 1e-13, 'dr/dt from the parametrisation is sqrt(1 - D/r)');
  }

  /* =============== E. PhET's stepper identity ===================== */
  {
    const Dn = phetD(PHET.boxW, 79, 80);
    for(const b of [10, 40, 120]) for(const ph of [0.05, 0.4, 1]){
      const r = rOfPhi(ph, b, Dn);
      if(!(r > 0)) continue;
      const sp = Math.sqrt(1 - Dn / r);
      const t3 = b * Math.cos(ph) - 0.5 * Dn * Math.sin(ph);
      const arc = b * b * sp / (r * Math.sqrt(Math.pow(b, 4) + r * r * t3 * t3));
      rel(arc, b / (r * r), 1e-13, 'the arc-length and angular-momentum forms of dphi/dt agree, b='
        + b + ' phi=' + ph);
      rel(arc, R('dphi/dt at b=' + b + ' phi=' + ph + ': arc-length form'), 1e-12,
        'dphi/dt at b=' + b + ' phi=' + ph + ' (derive)');
    }
  }

  /* =============== F. the seeded beam ============================= */
  {
    const mb = mulberry32(12345);
    for(let i = 0; i < 6; i++)
      rel(mb(), R('mulberry32(12345) draw ' + i), 4e-15, 'mulberry32 draw ' + i + ' (derive)');
    const th = sampleBeam(200000, 30, 3, 20260922);
    /* bit for bit: the JS and Python streams give the SAME sample, so the
       fractions have to agree exactly, not statistically */
    for(const d of [6, 8, 12, 20, 45, 90])
      rel(fractionBeyond(th, d * PI / 180), R('fraction scattered beyond ' + d + ' deg (sample)'), 1e-12,
        'the sampled fraction beyond ' + d + ' deg is the same sample as Python’s (derive)');
    /* and the sample agrees with the closed form to the SAMPLING LAW, whose
       tolerance comes from the binomial sigma derive.py printed */
    for(const d of [6, 8, 12, 20, 45, 90]){
      const z = R('fraction scattered beyond ' + d + ' deg (sample) :: z = (sample - exact)/sigma');
      ok(Math.abs(z) < 3, 'beyond ' + d + ' deg the sample is within 3 sigma of the closed form [z = ' + z + ']');
      const f = fractionBeyond(th, d * PI / 180);
      const ex = sigmaBeyond(d * PI / 180, 3) / (PI * 30 * 30);
      const sg = Math.sqrt(ex * (1 - ex) / 200000);
      rel((f - ex) / sg, z, 1e-6, 'and this file computes the same z at ' + d + ' deg');
    }
    const edges = [6, 8, 13, 21, 34, 55, 89, 144].map(d => d * PI / 180);
    const bins = binBeam(th, edges, 30, 3);
    const names = ['6-8', '8-13', '13-21', '21-34', '34-55', '55-89', '89-144'];
    for(let i = 0; i < bins.length; i++){
      rel(bins[i].n, R('bin ' + names[i] + ' deg: sampled dsdo :: count'), 1e-12,
        'bin ' + names[i] + ' deg holds the same particles as Python (derive)');
      rel(bins[i].dens, R('bin ' + names[i] + ' deg: sampled dsdo'), 1e-9,
        'bin ' + names[i] + ' deg sampled dsdo (derive)');
      rel(bins[i].exact, R('bin ' + names[i] + ' deg: sampled dsdo :: exact bin average'), 1e-12,
        'bin ' + names[i] + ' deg exact solid-angle average (derive)');
      /* the tolerance is the sampling law, 1/sqrt(N), not a number chosen to
         make the test pass -- three sigma of it */
      const s = 1 / Math.sqrt(bins[i].n);
      ok(Math.abs(bins[i].dens / bins[i].exact - 1) < 3 * s,
        'bin ' + names[i] + ' deg lands on 1/sin^4 within 3/sqrt(N) [' + (bins[i].dens / bins[i].exact)
        + ', 3 sigma = ' + (3 * s) + ']');
    }
    /* the beam really does span decades: if it did not, the test above would
       be measuring nothing */
    ok(bins[0].exact / bins[6].exact > 3e4, 'the binned cross section spans four decades');
  }

  /* =============== G. Thomson's atom ============================== */
  {
    const Dt = 1, Rt = 500;
    rel(thomsonThetaMax(Dt, Rt), R('Thomson theta_max = D/(2R) (D=1, R=500)'), 1e-14,
      'theta_max = D/2R (derive)');
    rel(thomsonTheta(Rt / Math.sqrt(2), Dt, Rt), thomsonThetaMax(Dt, Rt), 1e-14,
      'and it is reached at b = R/sqrt(2)');
    for(const f of [0.1, 0.3, 0.9]){
      const b = f * Rt;
      const key = 'Thomson theta(b=' + f.toFixed(4) + ' R) impulse, rad';
      const ti = thomsonTheta(b, Dt, Rt);
      const te = thomsonThetaExact(b, Dt, Rt, 20);
      rel(ti, R(key), 1e-13, 'the impulse deflection at b = ' + f + ' R (derive)');
      /* the deflection integral here is pi minus something almost pi, so it
         has lost four digits to cancellation before it is even returned: the
         agreement with scipy's own quadrature is 1e-5 relative and that is
         the arithmetic, not the physics. */
      rel(te, R(key + ' :: exact deflection integral'), 1e-4,
        'and the deflection integral agrees with scipy at b = ' + f + ' R (derive)');
      /* the impulse form is NOT exact, and saying so is the point: its error
         is O(theta) relative, which at these angles is a part in a thousand */
      const err = Math.abs(ti - te) / te;
      ok(err < 3e-3 && err > 1e-5, 'the impulse error at b = ' + f
        + ' R is a real O(theta) departure, not zero and not large [' + err + ']');
    }
    /* O(theta): halving D must halve the relative error of the impulse form */
    const e1 = R('impulse error at b=0.3R, D=1 (relative)');
    const e2 = R('impulse error at b=0.3R, D=0.5 (relative)');
    const e4 = R('impulse error at b=0.3R, D=0.25 (relative)');
    rel(e1 / e2, 2, 0.02, 'the impulse error is O(theta): it halves with D (derive)');
    rel(e2 / e4, 2, 0.02, 'and again (derive)');
    rel(thomsonTheta2Mean(Dt, Rt), R('closed form D^2/(6 R^2)'), 1e-14, '<theta^2> = D^2/6R^2 (derive)');
    /* <theta^2> by brute force over the disc, an independent route */
    const mean = simpson(b => thomsonTheta(b, Dt, Rt) * thomsonTheta(b, Dt, Rt) * 2 * b / (Rt * Rt),
      0, Rt, 20000);
    rel(mean, thomsonTheta2Mean(Dt, Rt), 2e-5, '<theta^2> by quadrature over the disc');
    ok(thomsonTheta(Rt * 1.01, Dt, Rt) === 0, 'a neutral Thomson atom does nothing outside its own radius');
  }

  /* =============== H. gold, for real ============================== */
  {
    const Dg = coulombD(2, 79, 7.7 * MEV);
    rel(Dg, R('D = k Z1 Z2 e^2 / E (m)'), 1e-12, 'D for 7.7 MeV alpha on gold (derive)');
    rel(Dg / FM, R('D (fm)'), 1e-12, 'D in fm (derive)');
    rel(bOfTheta(PI / 2, Dg) / FM, R('b at 90 deg (fm)'), 1e-12, 'b at 90 degrees, in fm (derive)');
    rel(nuclearRadius(197) / FM, R('nuclear radius 1.2 A^(1/3) fm, gold (fm)'), 1e-12,
      'the gold nuclear radius (derive)');
    rel(nuclearRadius(4) / FM, R('nuclear radius, alpha (fm)'), 1e-12, 'the alpha radius (derive)');
    const Et = KE * 2 * 79 * E_Q * E_Q / (nuclearRadius(197) + nuclearRadius(4));
    rel(Et / MEV, R('energy at which a head-on alpha touches gold (MeV)'), 1e-12,
      'the touching energy (derive)');
    ok(Dg > 3 * (nuclearRadius(197) + nuclearRadius(4)),
      'at 7.7 MeV the alpha stops three times too far out to touch the nucleus');
    rel(numberDensity(GOLD.rho, GOLD.molar), R('gold number density (1/m^3)'), 1e-12,
      'the gold number density (derive)');
    rel(Math.pow(numberDensity(GOLD.rho, GOLD.molar), -1 / 3), R('gold atomic spacing n^(-1/3) (m)'),
      1e-12, 'the gold atomic spacing (derive)');
    rel(GOLD.rAtom / nuclearRadius(197), R('atom / nucleus diameter ratio'), 1e-12,
      'a gold atom is 20623 nuclear diameters across (derive)');
    rel(dsdoOf(PI / 2, Dg) / BARN, R('dsdo at 90 deg (barn/sr)'), 1e-12, 'dsdo at 90 deg in barn/sr (derive)');
    const nt = numberDensity(GOLD.rho, GOLD.molar) * 400e-9;
    rel(nt, R('n t (1/m^2)'), 1e-12, 'n t for a 400 nm leaf (derive)');
    rel(nt * sigmaBeyond(PI / 2, Dg), R('Rutherford fraction beyond 90 deg'), 1e-12,
      'the Rutherford fraction beyond 90 degrees (derive)');
    rel(thomsonThetaMax(Dg, GOLD.rAtom), R('Thomson theta_max, single atom (rad)'), 1e-12,
      'the Thomson single-atom maximum for gold (derive)');
    rel(thomsonFoilTheta2(Dg, nt), R('Thomson <theta^2> through the foil (rad^2)'), 1e-12,
      'Thomson <theta^2> through a 400 nm leaf (derive)');
    rel(thomsonLog10P(PI / 2, thomsonFoilTheta2(Dg, nt)),
      R('log10 P(theta > 90 deg) under Thomson multiple scattering'), 1e-12,
      'log10 P(theta > 90) under Thomson (derive)');
    /* the whole historical argument, as one number */
    const gap = thomsonLog10P(PI / 2, thomsonFoilTheta2(Dg, nt))
              - Math.log10(nt * sigmaBeyond(PI / 2, Dg));
    rel(gap, R('ratio of exponents (how many decades apart)'), 1e-9,
      'the two models are 99310 decades apart at 90 degrees (derive)');
    ok(gap < -5e4, 'and that gap is what killed the plum pudding');
  }

  /* =============== I. PhET's scaled model ========================= */
  rel(phetD(PHET.boxW, 79, 80), R('PhET D, nuclear scene, defaults'), 1e-14, 'PhET D, nuclear scene (derive)');
  rel(phetD(PHET.atomW, 79, 80), R('PhET D, atomic scene, defaults'), 1e-14, 'PhET D, atomic scene (derive)');
  rel(phetD(PHET.boxW, 100, 50), R('PhET D, nuclear, 100 protons, energy 50'), 1e-14,
    'PhET D at the extreme corner (derive)');
  rel(phetD(PHET.boxW, 20, 100), R('PhET D, nuclear, 20 protons, energy 100'), 1e-14,
    'PhET D at the other corner (derive)');
  /* D written as 2 alpha / v^2 and D written PhET's way are the same number,
     over the whole slider space */
  for(const L of [PHET.atomW, PHET.boxW]) for(const p of [20, 47, 79, 100]) for(const s of [50, 65, 80, 100])
    rel(phetD(L, p, s), phetDDirect(L, p, s), 1e-13, 'D = 2 alpha/s^2 is PhET’s (L/8)(p/79)(80/s)^2, '
      + L + '/' + p + '/' + s);
  /* and alpha, the Coulomb strength, does NOT depend on the gun setting */
  for(const s of [50, 65, 80, 100])
    rel(phetD(PHET.boxW, 79, s) * s * s / 2, phetAlpha(PHET.boxW, 79), 1e-13,
      'D s^2/2 is the same alpha at every gun setting: the field does not know the projectile speed (s = '
      + s + ')');
  rel(phetD(PHET.boxW, 79, 80) / PHET.boxW, R('PhET D / L (both scenes)'), 1e-14,
    'D/L is one eighth at the defaults (derive)');
  rel(phetD(PHET.atomW, 79, 80) / PHET.atomW, 0.125, 1e-14, 'and one eighth in the atomic scene too');
  rel(phetGunPeriod(80), R('PhET gun period at energy 80 (s)'), 1e-14, 'the gun period (derive)');
  rel(phetGunPeriod(50), R('PhET gun period at energy 50 (s)'), 1e-14, 'the gun period at 50 (derive)');
  rel(phetNudge(PHET.atomW), R('PhET gun nudge for atom width 30'), 1e-13, 'the gun nudge, atomic (derive)');
  rel(phetNudge(PHET.boxW), R('PhET gun nudge for atom width 255'), 1e-13, 'the gun nudge, nuclear (derive)');
  rel(thetaOfB(10, phetD(PHET.boxW, 79, 80)) * 180 / PI, R('theta at that b, defaults (deg)'), 1e-12,
    'the largest angle PhET’s nuclear gun can produce (derive)');
  rel(PHET.atomicScaleM / PHET.nuclearScaleM, R('PhET caption scale ratio'), 1e-12,
    'PhET’s two captions are 4000x apart (derive)');
  rel(PHET.boxW / PHET.atomW, R('PhET geometric zoom ratio (atom box 30 -> 255)'), 1e-14,
    'while its geometry is 8.5x (derive)');
  ok(PHET.atomicScaleM / PHET.nuclearScaleM < GOLD.rAtom / nuclearRadius(197),
    'and both are well short of the real 20623');

  /* =============== J. the engine ================================== */
  {
    /* one particle from the gun in the nuclear scene: its drawn turn must be
       exactly the conic's own drawn turn between the radii it was tracked
       across -- asserted off the BUILT path, not off a retyped formula */
    Object.assign(ST, DEFAULTS); ST.view = 'nucleus'; ST.gunOn = false; engineReset(ST);
    const atoms = atomsFor('nucleus');
    for(const x0 of [12, 30, 60, 100]){
      RUN.ps = [newParticle(x0, -HALF_BOX, 0, ST.energy)];
      const p = RUN.ps[0];
      let guard = 0;
      while(RUN.ps.length && guard++ < 20000) stepOne(ST, DT_TICK);
      const D = phetD(PHET.boxW, ST.protons, ST.energy);
      const measured = Math.abs(Math.atan2(p.vx, p.vy));
      /* the gun fires straight up and the orbit is chosen so that its
         ASYMPTOTE is straight up, so the particle's own direction kinks by
         chi(phi_in) the moment it is picked up -- PhET's algorithm does the
         same -- and the angle it finally leaves at is chi(phi_out), measured
         from the asymptote and not from the launch tangent. */
      const phiOut = phiAtRadius(p.rOut, p.b0, D, true);
      rel(measured, velAngle(phiOut, p.b0, D), 3e-4,
        'the drawn turn at x = ' + x0 + ' is the conic’s own velocity angle at r_out');
      rel(measured - drawnTurn(p.b0, D, p.rIn, p.rOut), p.chi0, 3e-4,
        'and the difference from the tracked turn is exactly the pick-up kink, x = ' + x0);
      ok(p.chi0 > 0 && p.chi0 <= pickupKink(PHET.boxW, D) + 1e-9,
        'that kink is positive and no bigger than the worst case the model prints, x = '
        + x0 + ' [' + p.chi0 + ' vs ' + pickupKink(PHET.boxW, D) + ']');
      ok(measured < thetaOfB(p.b0, D) + 1e-9,
        'and it never exceeds the full 2 atan(D/2b) at x = ' + x0);
      ok(p.b0 > 0 && p.b0 < x0 + 1e-9, 'the recovered b is positive and at most the launch offset, x = ' + x0);
      ok(RUN.clamps === 0, 'the entry quadratic never had to be clamped at x = ' + x0);
    }
    /* the gun's nudge really keeps particles off the axis */
    Object.assign(ST, DEFAULTS); ST.view = 'nucleus'; engineReset(ST);
    let minx = 1e9;
    for(let i = 0; i < 4000; i++){
      RUN.ps.length = 0;
      const p = gunFire(ST, atoms);
      minx = Math.min(minx, Math.abs(p.x));
    }
    ok(pickupKink(PHET.boxW, phetD(PHET.boxW, 79, 80)) < 0.06,
      'the worst pick-up kink at the defaults is under 3.5 degrees ['
      + pickupKink(PHET.boxW, phetD(PHET.boxW, 79, 80)) + ']');
    ok(minx >= phetNudge(PHET.boxW) - 1e-9,
      'PhET’s nudge keeps every fired particle at least ' + phetNudge(PHET.boxW)
      + ' off the axis [' + minx + ']');
  }
  /* a full run in every live view stays finite, and the foil really does send
     most of the beam almost straight through */
  for(const v of ['nucleus', 'foil', 'pudding']){
    Object.assign(ST, DEFAULTS); ST.view = v; engineReset(ST);
    for(let i = 0; i < 900; i++) stepOne(ST, DT_TICK);
    let bad = 0;
    for(const p of RUN.ps) if(!isFinite(p.x) || !isFinite(p.y) || !isFinite(p.vx) || !isFinite(p.vy)) bad++;
    ok(bad === 0, v + ': no particle went non-finite in 900 ticks');
    ok(RUN.left > 20, v + ': particles reach the edge of the frame [' + RUN.left + ']');
    ok(RUN.clamps === 0, v + ': the entry quadratic never clamped');
  }
  {
    Object.assign(ST, DEFAULTS); ST.view = 'foil'; engineReset(ST);
    for(let i = 0; i < 2500; i++) stepOne(ST, DT_TICK);
    let straight = 0, back = 0, tot = 0;
    for(let i = 0; i < NHIST; i++){
      tot += RUN.hist[i];
      if(i * 180 / NHIST < 5) straight += RUN.hist[i];
      if(i * 180 / NHIST >= 90) back += RUN.hist[i];
    }
    ok(straight / tot > 0.4, 'the foil sends most of the beam through nearly undeflected ['
      + (straight / tot) + ']');
    ok(back > 0 && back / tot < 0.08, 'and a few of them back past 90 degrees [' + back + ' of ' + tot + ']');
  }
  /* the plum pudding is the contrast, and it must be invisible at x1 */
  {
    Object.assign(ST, DEFAULTS); ST.view = 'pudding'; engineReset(ST);
    for(let i = 0; i < 900; i++) stepOne(ST, DT_TICK);
    ok(RUN.maxTheta < 1e-3, 'at x1 the plum pudding deflects nothing visible [' + RUN.maxTheta + ' rad]');
    const shift = RUN.maxTheta * PHET.boxW;
    ok(shift < 0.05, 'the largest sideways shift across the whole box is ' + shift + ' model units');
    Object.assign(ST, DEFAULTS); ST.view = 'pudding'; ST.exagg = 2001; engineReset(ST);
    for(let i = 0; i < 900; i++) stepOne(ST, DT_TICK);
    ok(RUN.maxTheta > 0.05, 'and the exaggeration slider makes it visible [' + RUN.maxTheta + ' rad]');
  }
  /* the engine resets itself when a control that changes the physics moves */
  {
    Object.assign(ST, DEFAULTS); ST.view = 'nucleus'; engineReset(ST);
    for(let i = 0; i < 300; i++) stepOne(ST, DT_TICK);
    const n0 = RUN.fired;
    ok(n0 > 0, 'the gun fired before the control moved');
    ST.protons = 40;
    engineAdvance(ST, DT_TICK);
    ok(RUN.fired < n0, 'changing the proton count restarts the run');
  }
  /* the same seed replays the same run, a different one does not */
  {
    Object.assign(ST, DEFAULTS); ST.view = 'nucleus'; engineReset(ST);
    for(let i = 0; i < 600; i++) stepOne(ST, DT_TICK);
    const a1 = RUN.fired + '|' + RUN.left + '|' + fmt(RUN.maxTheta, 9);
    engineReset(ST);
    for(let i = 0; i < 600; i++) stepOne(ST, DT_TICK);
    const a2 = RUN.fired + '|' + RUN.left + '|' + fmt(RUN.maxTheta, 9);
    ok(a1 === a2, 'the same seed replays the same run');
    ST.seed = 424242; engineReset(ST);
    for(let i = 0; i < 600; i++) stepOne(ST, DT_TICK);
    const a3 = RUN.fired + '|' + RUN.left + '|' + fmt(RUN.maxTheta, 9);
    ok(a1 !== a3, 'a different seed gives a different run');
  }


  /* =============== J2. what the mutation sweep found untested ====== */
  /* Every block below exists because a mutant survived: the list is in
     build/rutherford-scattering/changelog_entry.md.  They are not padding --
     each one pins a quantity that nothing in the first 925 assertions
     touched. */
  {
    /* (1) the Poisson sigma: the bin test recomputed 3/sqrt(n) locally
       instead of reading the one the model returns, so the model's own could
       be anything (Known-bad: assert values off a BUILT model). */
    const th = sampleBeam(200000, 30, 3, 20260922);
    const edges = [6, 8, 13, 21, 34, 55, 89, 144].map(d => d * PI / 180);
    const bins = binBeam(th, edges, 30, 3);
    rel(bins[0].sigma, R('bin 6-8 deg: sampled dsdo :: Poisson relative sigma 1/sqrt(count)'),
      1e-12, 'the model’s own Poisson sigma for the first bin (derive)');
    rel(bins[6].sigma, R('bin 89-144 deg: sampled dsdo :: Poisson relative sigma 1/sqrt(count)'),
      1e-12, 'and for the last one (derive)');
    for(let i = 0; i < bins.length; i++)
      ok(Math.abs(bins[i].dens / bins[i].exact - 1) < 3 * bins[i].sigma,
        'bin ' + i + ' is inside 3 of the model’s OWN sigma');
    ok(binBeam(th, edges, 30, 3)[0].sigma < 0.01,
      'and that sigma is small enough for the comparison to mean something');
  }
  {
    /* (2) PhET's 4% nudge window.  Its effect on the smallest reachable |x|
       is nil -- doubling the window leaves the minimum at the nudge itself --
       so the only thing that sees it is the DENSITY it doubles.  With a
       window w and a nudge c, the band (c, w + c) receives both the particles
       that were already there and the ones pushed in from (0, w). */
    Object.assign(ST, DEFAULTS); ST.view = 'nucleus'; engineReset(ST);
    const atoms = atomsFor('nucleus');
    const N = 40000, c = phetNudge(PHET.boxW), w = PHET.nudgeWindow * PHET.boxW;
    let inBand = 0, sum = 0, mx = 0, mn = 1e9, neg = 0;
    for(let i = 0; i < N; i++){
      RUN.ps.length = 0;
      const p = gunFire(ST, atoms);
      const ax = Math.abs(p.x);
      if(ax > c + 0.5 && ax < w - 0.2 + c) inBand++;
      sum += p.x; mx = Math.max(mx, ax); mn = Math.min(mn, ax);
      if(p.x < 0) neg++;
    }
    /* the doubled band is (10.5, 20.0): both the un-nudged and the nudged
       particles land in it, so its share is twice 9.5/127.5 */
    const lo2 = c + 0.5, hi2 = w - 0.2 + c;
    const pExp = 2 * (hi2 - lo2) / HALF_BOX;
    const sg = Math.sqrt(pExp * (1 - pExp) / N);
    rel(inBand / N, pExp, 5 * sg / pExp, 'the nudge window doubles the density just outside it ['
      + (inBand / N) + ' vs ' + pExp + ', 5 sigma = ' + (5 * sg) + ']');
    ok(mn >= c - 1e-9, 'no particle is fired closer than the nudge to the axis [' + mn + ']');
    /* (3) the beam is a BEAM: symmetric about the axis and as wide as the box */
    ok(Math.abs(sum / N) < 5 * HALF_BOX / Math.sqrt(3 * N),
      'the beam is symmetric about the axis (mean x = ' + (sum / N) + ')');
    ok(Math.abs(neg / N - 0.5) < 0.02, 'and half of it is on each side (' + (neg / N) + ')');
    ok(mx > HALF_BOX * 0.999, 'and it spans the whole box (' + mx + ' of ' + HALF_BOX + ')');
  }
  {
    /* (4) dphi/dt is the TIMING along the conic, and every earlier assertion
       measured a DIRECTION, which the timing cannot change.  Pin the time:
       derive.py integrates dt = r^2 dphi / (v b) with scipy quad and prints
       how long the orbit takes to run from phi = 0.05 to phi = 0.9. */
    const a = {x: 0, y: 0, L: PHET.boxW};
    for(const bb of [10, 60]){
      const p = newParticle(0, 0, 0, 1);
      p.b = bb; p.D = phetD(PHET.boxW, 79, 80); p.vinf = 1; p.phi = 0.05;
      p.ix = 1; p.iy = 0; p.jx = 0; p.jy = 1;
      const T = R('elapsed time from phi=0.05 to 0.9, b=' + bb);
      for(let k = 0; k < 60; k++) advanceOrbit(p, a, T / 60);
      close(p.phi, 0.9, 1e-4, 'the engine reaches phi = 0.9 in the time the quadrature says, b = '
        + bb + ' [' + p.phi + ']');
      /* and the engine is at least as accurate as derive's plain 60-step
         RK4, because it sub-steps where the angle is turning fastest */
      const ref60 = Math.abs(
        R('elapsed time from phi=0.05 to 0.9, b=' + bb + ' :: RK4 phi after T, 60 steps') - 0.9);
      ok(Math.abs(p.phi - 0.9) <= ref60 + 1e-12,
        'and it is at least as accurate as the 60-step RK4 derive.py printed, b = ' + bb
        + ' [' + Math.abs(p.phi - 0.9) + ' vs ' + ref60 + ']');
    }
  }
  {
    /* (5) the speed law: v(r) = v_inf sqrt(1 - D/r) appears nowhere in any
       angle, so pin the ENERGY of every particle the engine is carrying.
       alpha = D v_inf^2 / 2, so 1/2 v^2 + alpha/r must be 1/2 v_inf^2. */
    for(const v of ['nucleus', 'foil']){
      Object.assign(ST, DEFAULTS); ST.view = v; engineReset(ST);
      const atoms = atomsFor(v);
      let worst = 0, n = 0;
      for(let i = 0; i < 1200; i++){
        stepOne(ST, DT_TICK);
        for(const p of RUN.ps){
          if(p.ai < 0) continue;
          const a2 = atoms[p.ai];
          const r = Math.hypot(p.x - a2.x, p.y - a2.y);
          const E = 0.5 * (p.vx * p.vx + p.vy * p.vy) + 0.5 * p.D * p.vinf * p.vinf / r;
          worst = Math.max(worst, Math.abs(E - 0.5 * p.vinf * p.vinf) / (0.5 * p.vinf * p.vinf));
          n++;
        }
      }
      ok(n > 200, v + ': there were particles on orbits to check (' + n + ')');
      ok(worst < 1e-12, v + ': every particle on an orbit has exactly its launch energy ['
        + worst + ']');
    }
  }
  {
    /* (6) the orbit frame.  In the nuclear scene j is (0, 1) and i is (+-1, 0),
       so the j component of x is identically zero and no straight-up launch
       can see it.  Build a frame that is rotated and check the placement
       against its own definition. */
    const psi = 0.7, a = {x: 5, y: -3};
    const p = newParticle(0, 0, 0, 1);
    p.b = 18; p.D = 31.875; p.vinf = 80; p.phi = 0.42;
    p.ix = Math.cos(psi); p.iy = Math.sin(psi);
    p.jx = -Math.sin(psi); p.jy = Math.cos(psi);
    placeOnOrbit(p, a);
    const r = rOfPhi(p.phi, p.b, p.D);
    const rx = p.x - a.x, ry = p.y - a.y;
    rel(Math.hypot(rx, ry), r, 1e-12, 'a rotated frame still places the particle at r(phi)');
    rel(rx * p.ix + ry * p.iy, r * Math.sin(p.phi), 1e-12, 'its i component is r sin(phi)');
    rel(rx * p.jx + ry * p.jy, -r * Math.cos(p.phi), 1e-12, 'and its j component is -r cos(phi)');
    rel(Math.hypot(p.vx, p.vy), p.vinf * Math.sqrt(1 - p.D / r), 1e-12,
      'and its speed is v_inf sqrt(1 - D/r)');
    const chi = Math.atan2(p.vx * p.ix + p.vy * p.iy, p.vx * p.jx + p.vy * p.jy);
    rel(chi, velAngle(p.phi, p.b, p.D), 1e-12, 'and its direction is chi(phi) in that frame');
  }
  {
    /* (7) PhET's own geometry: five atoms, where PhET puts them */
    const A = atomsFor('foil'), n = PHET.boxW / 2, s = n / 2;
    ok(A.length === 5, 'the atomic scene has PhET’s five atoms');
    const want = [[-s, s], [s, s], [0, -s], [-n, -s], [n, -s]];
    let bad = 0;
    for(let i = 0; i < 5; i++){
      if(Math.abs(A[i].x - want[i][0]) > 1e-12 || Math.abs(A[i].y - want[i][1]) > 1e-12) bad++;
      if(A[i].L !== PHET.atomW) bad++;
    }
    ok(bad === 0, 'and each one is where RutherfordAtomSpace puts it, 30 units wide');
    rel(s, 63.75, 1e-12, 'the row offset is a quarter of the bounds width');
    ok(atomsFor('nucleus').length === 1 && atomsFor('nucleus')[0].L === PHET.boxW,
      'the nuclear scene has one atom whose box is the whole bounds');
    ok(atomsFor('pudding').length === 0,
      'and PhET’s plum-pudding space has no atoms in its model at all');
  }
  /* (8) PhET's manual step is 1/60 s and nothing else */
  rel(DT_TICK, 1 / 60, 1e-15, 'the model tick is PhET’s own 1/60 s manualStep');
  {
    Object.assign(ST, DEFAULTS); ST.view = 'nucleus'; engineReset(ST);
    const t0 = RUN.t;
    engineStepOnce(ST);
    rel(RUN.t - t0, 1 / 60, 1e-15, 'and one step advances the clock by exactly that');
  }
  {
    /* (9) the plum-pudding kick is thomsonTheta, not a second copy of it, and
       its D and its R are the real ones */
    Object.assign(ST, DEFAULTS);
    rel(realD(ST), R('D = k Z1 Z2 e^2 / E (m)'), 1e-12,
      'the pudding uses the real D for a 7.7 MeV alpha on gold (derive)');
    rel(realDoverR(ST), 2 * R('Thomson theta_max, single atom (rad)'), 1e-12,
      'and D/R is twice the single-atom maximum (derive)');
    const R2 = HALF_BOX, Dm = realDoverR(ST) * R2;
    for(const bb of [0.2, 0.5, 1 / Math.SQRT2, 0.95]){
      const p = newParticle(bb * R2, -1, 0, 80);
      puddingKick(p, ST);
      const got = Math.abs(Math.atan2(p.vx, p.vy));
      rel(got, thomsonTheta(bb * R2, Dm, R2), 1e-12,
        'the kick at b = ' + bb + ' R is thomsonTheta itself');
      rel(got, realDoverR(ST) * bb * Math.sqrt(1 - bb * bb), 1e-12,
        'which is (D/R)(b/R)sqrt(1 - (b/R)^2), at b = ' + bb + ' R');
    }
    /* the exaggeration multiplies it and nothing else */
    const p1 = newParticle(0.5 * R2, -1, 0, 80);
    puddingKick(p1, ST);
    const a1 = Math.abs(Math.atan2(p1.vx, p1.vy));
    ST.exagg = 1000;
    const p2 = newParticle(0.5 * R2, -1, 0, 80);
    puddingKick(p2, ST);
    rel(Math.abs(Math.atan2(p2.vx, p2.vy)) / a1, 1000, 1e-9,
      'and the exaggeration slider is a pure multiplier');
    ST.exagg = 1;
    /* a particle on the far side is kicked the other way */
    const p3 = newParticle(-0.5 * R2, -1, 0, 80);
    puddingKick(p3, ST);
    ok(p3.vx < 0 && p1.vx > 0, 'and the ball pushes each side outwards, not all one way');
    ok(Math.abs(p3.vx) === Math.abs(p1.vx), 'symmetrically');
  }

  /* =============== K. panels build clean ========================== */
  Object.assign(ST, DEFAULTS);
  const PRESETS = [
    {}, {energy: 50}, {energy: 100}, {protons: 20}, {protons: 100},
    {neutrons: 20}, {neutrons: 150}, {protons: 100, energy: 50}, {protons: 20, energy: 100},
    {bModel: 0}, {bModel: 120}, {nPaths: 1}, {nPaths: 19},
    {nSample: 2000}, {nSample: 60000}, {bMax: 20}, {bMax: 160},
    {EMeV: 0.5}, {EMeV: 30}, {foilNm: 50}, {foilNm: 4000}, {exagg: 4001},
    {traces: false}, {gunOn: false}, {showClosed: false}, {showInt: false},
    {showAsym: false}, {showSample: false}, {showJac: false},
  ];
  {
    let bad = 0, nonfinite = 0, first = '';
    for(const v of TABS.map(t => t[0])) for(const pr of PRESETS){
      Object.assign(ST, DEFAULTS, pr); ST.view = v;
      const M = buildModel();
      const s = readoutHTML(M) + eqbarHTML(M) + tagHTML(M) + INFO[v];
      if(/NaN|undefined|Infinity/.test(s)){ bad++; if(!first) first = v + ' ' + JSON.stringify(pr); }
      for(const k of ['D', 'alpha', 'thMaxPhet', 'bAt90', 'thSel', 'rminSel', 'eccSel', 'turnSel'])
        if(!isFinite(M[k])) nonfinite++;
      for(const k of ['D', 'a', 'Rnuc', 'Etouch', 'f90', 'thMax', 'th2', 'log10P'])
        if(!isFinite(M.gold[k])) nonfinite++;
    }
    ok(bad === 0, 'every view x preset builds clean panels [' + bad + ' bad, first ' + first + ']');
    ok(nonfinite === 0, 'and no model value is non-finite [' + nonfinite + ']');
  }
  /* every slider corner, on every view, leaves the model finite */
  {
    const RANGES = {energy: [50, 100], protons: [20, 100], neutrons: [20, 150],
                    bModel: [0, 120], nPaths: [1, 19], nSample: [2000, 60000],
                    bMax: [20, 160], EMeV: [0.5, 30], foilNm: [50, 4000], exagg: [1, 4001],
                    rate: [0.25, 3], seed: [1, 999999]};
    let bad = 0;
    for(const k in RANGES) for(const val of RANGES[k]) for(const v of TABS.map(t => t[0])){
      Object.assign(ST, DEFAULTS); ST[k] = val; ST.view = v;
      const M = buildModel();
      if(!isFinite(M.D) || !isFinite(M.thSel) || !isFinite(M.gold.D)) bad++;
    }
    ok(bad === 0, 'every slider corner on every view leaves the model finite [' + bad + ']');
  }

  /* =============== L. the drawing ================================ */
  Object.assign(ST, DEFAULTS);
  const SIZES = [[1400, 820], [1100, 700], [820, 520], [560, 380]];
  const entRe = /&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [W, H] of SIZES) for(const v of TABS.map(t => t[0])) for(const pr of
      [{}, {traces: false, showClosed: false}, {bModel: 0, nPaths: 1}, {showSample: false, showJac: false},
       {protons: 100, energy: 50, exagg: 4001}]){
    Object.assign(ST, DEFAULTS, pr); ST.view = v;
    if(liveView(v)){ engineReset(ST); for(let i = 0; i < 240; i++) stepOne(ST, DT_TICK); }
    const ctx = makeShot(W, H);
    drawView(ctx, W, H, buildModel());
    const nm = v + ' ' + JSON.stringify(pr);
    const texts = ctx.ops.filter(o => o.op === 'text');
    ok(ctx.ops.length > 20, nm + ' ' + W + 'x' + H + ' drew content [' + ctx.ops.length + ' ops]');
    let bad = null;
    for(const t of texts){
      if(entRe.test(t.t)){ bad = 'entity/tag: "' + t.t.slice(0, 40) + '"'; break; }
      if(/undefined|NaN/.test(t.t)){ bad = 'NaN/undefined: "' + t.t.slice(0, 40) + '"'; break; }
      if(t.bb[0] < -1 || t.bb[2] > W + 1 || t.bb[1] < -1 || t.bb[3] > H + 1){
        bad = 'off-canvas: "' + t.t.slice(0, 30) + '" [' + t.bb.map(q => fmt(q, 0)) + ']'; break; }
    }
    ok(!bad, nm + ' ' + W + 'x' + H + ' text clean (' + (bad || 'ok') + ')');
    /* the HTML #hint sits at bottom:11px in 11px type and the canvas capture
       cannot see it, so nothing may be drawn in that corner (Known-bad) */
    const inHint = texts.filter(t => t.bb[0] < HINT_W && t.bb[3] > H - HINT_H);
    ok(!inHint.length, nm + ' ' + W + 'x' + H + ' nothing under the #hint line'
      + (inHint.length ? ' ("' + inHint[0].t.slice(0, 30) + '" to y ' + fmt(inHint[0].bb[3], 0) + ')' : ''));
    let hit = null;
    for(let i = 0; i < texts.length && !hit; i++) for(let j = i + 1; j < texts.length; j++){
      const a = texts[i].bb, b = texts[j].bb;
      const ox = Math.min(a[2], b[2]) - Math.max(a[0], b[0]);
      const oy = Math.min(a[3], b[3]) - Math.max(a[1], b[1]);
      /* half a pixel, the threshold tools/audit.py applies (Known-bad) */
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
  engineReset(ST);
  const dt = (Date.now() - T0) / 1000;
  console.log(pass + ' passed, ' + fail + ' failed  (' + fmt(dt, 1) + ' s)');
  if(fail > 0) throw new Error(fail + ' self-test failure(s)');
  return fail;
}
