
/* ================================================================== *
 *  views 3-5 (the analysis three), the dispatch and the scene         *
 * ================================================================== */

/* ---- view 3: the circular orbit ----------------------------------------------------------- */
const CAPC_FULL = 'Not a PhET screen. Set a body going sideways at exactly √(GM/r) and the pull needed '
  + 'to bend it round the circle is exactly the pull gravity supplies — that is the whole of the circular '
  + 'orbit, and it is the only speed at which the two match. Slower and the orbit falls inside, with the start '
  + 'point at apoapsis; faster and it swings out, with the start point at periapsis; at √2 times it never '
  + 'comes back. The slider is that ratio, and the conic under it is computed in closed form, not integrated. '
  + 'The panels below put the law on a log axis with PhET’s three real orbits on it, and then the '
  + 'third law that follows from it.';
const CAPC_SHORT = 'v = √(GM/r): the one speed that balances, and what the others do.';
function drawCirc(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAPC_FULL, CAPC_SHORT, 2, 0.36, 1);
  const b = L.main, ci = M.ci, el = ci.el;
  /* the drawn arc: the whole ellipse, or the hyperbola between its asymptotes, capped at 6r
     so that a near-escape orbit does not shrink everything else to a dot */
  const CAP = 6 * ci.r;
  const pts = [];
  if(el.kind === 'ellipse'){
    for(let k = 0; k <= 400; k++) pts.push(conicPoint(el, TAU * k / 400));
  } else {
    const nuMax = (el.nuInf !== undefined ? el.nuInf : Math.PI) * 0.995;
    for(let k = 0; k <= 400; k++){
      const p = conicPoint(el, -nuMax + 2 * nuMax * k / 400);
      if(Math.hypot(p[0], p[1]) <= CAP) pts.push(p);
    }
  }
  let ext = ci.r * 1.4;
  for(const p of pts) ext = Math.max(ext, Math.abs(p[0]), Math.abs(p[1]));
  ext = Math.min(ext, CAP) * 1.08;
  const map = worldFitUp(b, {xmin: -ext, xmax: ext, ymin: -ext, ymax: ext}, 0);
  const win = winOf(map, b);
  frame(ctx, b, COL.edge);
  lab(ctx, W, H, b.x + 6, b.y + 8, 'the conic a start of ' + fmt(ST.vfrac, 3) + ' × v_c makes at r = '
      + plain(lenStr(ci.r, 4)), '#aeb6c6', 'italic 13px Georgia, serif', 'left', 'top');
  lab(ctx, W, H, b.x1 - 6, b.y + 8, plain(scaleNoteGo(map)) + '; the arrow is '
      + fmt(VEL_PX, 0) + ' px at the escape speed', COL.dim, SM_FONT, 'right', 'top');
  /* the central body at its TRUE radius, floored at 1.4 % of the VIEW (not of the orbit: a
     near-escape conic widens the view six-fold and a floor tied to the orbit then shrinks the
     star to one pixel).  The factor that floor amounts to is printed, not assumed. */
  const rTrue = sceneCfg('scale', M.cfg.id).bodies[0].r;
  const rc = Math.max(rTrue, 0.028 * ext);
  withClip(ctx, b, () => {
    /* the circle the balance makes, always drawn, as the thing to compare against */
    circleW(ctx, map, [0, 0], ci.r, COL.struct, 1.4, [5, 4]);
    worldPathClip(ctx, map, pts, COL.pos, 2, null, win);
    circleW(ctx, map, [0, 0], rc, null, 0, null, rgba(BODY_COL[M.sys.S.kind[0]], 0.9));
    /* the apsides FIRST, then the start point: above v_c periapsis sits exactly on the start,
       and drawn last it covers the live marker the view is about */
    if(el.kind === 'ellipse'){
      const q = conicPoint(el, 0), Q = conicPoint(el, Math.PI);
      diamond(ctx, map.X(q[0]), map.Y(q[1]), 6, COL.ref, '#fff');
      diamond(ctx, map.X(Q[0]), map.Y(Q[1]), 6, null, COL.ref);
    }
    const X = map.X(ci.r), Y = map.Y(0);
    arrowPx(ctx, X, Y, X, Y - VEL_PX * ci.v / ci.vesc, COL.live, 2);
    dot(ctx, X, Y, 4.5, COL.live, '#fff', 1.2);
  });
  lab(ctx, W, H, map.X(ci.r), map.Y(0) - VEL_PX * ci.v / ci.vesc - 8, fmt(ci.v, 0) + ' m/s',
      COL.live, SM_FONT, 'center', 'bottom');
  lab(ctx, W, H, b.x + 6, b.y + 26, el.kind === 'ellipse'
      ? plain('an ellipse: e = ' + fmt(el.e, 6) + ', a = ' + lenStr(el.a, 5) + ', T = '
              + timeStr(el.T, M.cfg.minutes))
      : plain('unbound: ' + el.kind + ', e = ' + fmt(el.e, 6) + ' — it never comes back'),
      el.kind === 'ellipse' ? COL.pos : COL.warn, SM_FONT, 'left', 'top');
  labFit(ctx, W, H, b.x + 6, b.y + 42, plain('the central body is drawn at ×' + sigf(rc / rTrue, 3)
         + ' its true radius (' + lenStr(rTrue, 3) + ') so that it can be seen'),
         plain('central body ×' + sigf(rc / rTrue, 3) + ' its true size'),
         b.w - 12, COL.dim, SM_FONT, 'left', 'top');
  /* an orbit whose periapsis is inside the body is not an orbit: PhET flags the same thing on
     its own Kepler screen, and the picture alone only shows the curve going behind the disc */
  if(el.q < rTrue)
    labFit(ctx, W, H, b.x + 6, b.y + 58, plain('periapsis is ' + lenStr(el.q, 3) + ', inside the '
           + lenStr(rTrue, 3) + ' body — this orbit hits it'),
           'periapsis is inside the body — it hits', b.w - 12, COL.warn, SM_FONT, 'left', 'top');
  /* at exactly v_c the orbit IS the circle and is drawn over it, so the legend says so rather
     than naming a colour that is not on the screen */
  legendR(ctx, b, [[COL.struct, 'the circle at v_c = ' + fmt(ci.vc, 0) + ' m/s'
                    + (el.e < 1e-9 ? ' (the orbit is on it)' : '')], [COL.pos, 'the orbit'],
                   [COL.live, 'the start, and v'], [COL.ref, 'periapsis (filled), apoapsis']]);
  /* panel 1: the law itself, with the real orbits on it */
  const bb = L.bottom[0];
  const rlo = Math.log10(PH.EARTH_RADIUS), rhi = Math.log10(3 * PH.EARTH_X);
  const vlo = Math.log10(200), vhi = Math.log10(6e4);
  axesT(ctx, bb, rlo, rhi, vlo, vhi, {title: titleFor(bb, 'the circular speed against the radius, for both central masses',
    'v_c against r'), xlab: 'log₁₀ r (m)', ylab: 'log₁₀ v_c (m/s)', nx: 4, ny: 4});
  for(const [Mc, col, nm] of [[PH.SUN_MASS, COL.ref, 'about the Sun'], [PH.EARTH_MASS, COL.struct, 'about the Earth']]){
    const xs = [], ys = [];
    for(let k = 0; k <= 80; k++){
      const lr = rlo + (rhi - rlo) * k / 80;
      xs.push(lr); ys.push(Math.log10(circSpeed(Mc, Math.pow(10, lr))));
    }
    polyline(ctx, bb, xs, ys, rlo, rhi, vlo, vhi, col, 1.8);
  }
  /* the marker labels go BELOW and right of their marker: both v_c lines descend to the right,
     so a label above one lands on it (it did, in the first capture) */
  for(const k of ci.marks){
    marker(ctx, bb, rlo, rhi, vlo, vhi, Math.log10(k.r), Math.log10(k.vc), k.col);
    labIn(ctx, W, H, bb, bb.x + bb.w * (Math.log10(k.r) - rlo) / (rhi - rlo) + 7,
          bb.y1 - bb.h * (Math.log10(k.vc) - vlo) / (vhi - vlo) + 6,
          plain(k.short) + ' ' + fmt(k.vc, 0) + ' m/s', k.col, SM_FONT, 'left', 'top');
  }
  legendR(ctx, bb, [[COL.ref, 'GM of the Sun'], [COL.struct, 'GM of the Earth']]);
  /* panel 2: the third law */
  if(L.bottom.length > 1){
    const cb = L.bottom[1];
    const alo = Math.log10(PH.EARTH_RADIUS), ahi = Math.log10(3 * PH.EARTH_X);
    const tlo = Math.log10(3e3), thi = Math.log10(1e9);
    axesT(ctx, cb, alo, ahi, tlo, thi, {title: titleFor(cb, 'T² ∝ a³: the period against the radius, slope 3/2',
      'T against a, slope 3/2'), xlab: 'log₁₀ a (m)', ylab: 'log₁₀ T (s)', nx: 4, ny: 4});
    for(const [Mc, col] of [[PH.SUN_MASS, COL.ref], [PH.EARTH_MASS, COL.struct]]){
      const xs = [], ys = [];
      for(let k = 0; k <= 80; k++){
        const la = alo + (ahi - alo) * k / 80;
        xs.push(la); ys.push(Math.log10(circPeriod(Mc, Math.pow(10, la))));
      }
      polyline(ctx, cb, xs, ys, alo, ahi, tlo, thi, col, 1.8);
    }
    /* below and right again: both lines rise to the right, so the free space is underneath */
    for(const k of ci.marks){
      marker(ctx, cb, alo, ahi, tlo, thi, Math.log10(k.r), Math.log10(k.T), k.col);
      labIn(ctx, W, H, cb, cb.x + cb.w * (Math.log10(k.r) - alo) / (ahi - alo) + 7,
            cb.y1 - cb.h * (Math.log10(k.T) - tlo) / (thi - tlo) + 6,
            plain(k.short) + ' ' + plain(timeStrFine(k.T, k.T < 2 * PH.DAY)), k.col, SM_FONT, 'left', 'top');
    }
  }
  drawCaption(ctx, L);
}

/* A panel with nothing in it yet.  Drawing axes for a run of length zero gives a degenerate
   range whose every tick formats as "0" -- six identical labels along the bottom, which is
   what the first capture of the exact view showed.  Say what is missing instead. */
function emptyPanel(ctx, W, H, b, msg){
  frame(ctx, b, COL.edge);
  lab(ctx, W, H, (b.x + b.x1) / 2, (b.y + b.y1) / 2, msg, COL.dim, 'italic 13px Georgia, serif',
      'center', 'middle');
}

/* ---- view 4: the exact orbit -------------------------------------------------------------- */
const CAPE_FULL = 'Not a PhET screen. Two bodies are the case that can be solved, and Kepler solved it: get '
  + 'the elements from the state vector, then the position at any later time follows from '
  + 'M = E − e sin E with no integration at all. The orange curve is that answer, drawn from the state '
  + 'this run started at; the coloured trails are what the integrator has actually done. The first panel '
  + 'below is the distance between them, which is the integrator’s error and nothing else — it grows, '
  + 'slowly. '
  + 'With the star nailed down (the Model screen) the exact problem is one body about μ = GM; with both '
  + 'free it is the relative orbit about μ = G(M+m).';
const CAPE_SHORT = 'The closed-form Kepler solution (orange) against the integrated path, and their difference.';
function drawExact(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAPE_FULL, CAPE_SHORT, 2, 0.34, 1);
  const b = L.main, ex = M.ex;
  if(!ex){
    /* No closed form for three bodies -- but the system is still drawn, both because the view
       has to say WHY it cannot compare and because the drag mapping is taken from this same
       box.  An early return left two empty panels and a stage with nothing in it. */
    drawSystem(ctx, W, H, M, b, {grid: ST.grid, path: ST.path, velocity: ST.velocity,
      force: false, com: true, tape: ST.tape, mass: ST.massOn});
    lab(ctx, W, H, b.x + 6, b.y + 26, 'no orange curve here: the closed form is for two bodies',
        COL.warn, SM_FONT, 'left', 'top');
    systemLegend(ctx, b, M);
    /* ONE box across where the two panels would be, with one sentence in two lines: the same
       sentence in each panel says it twice, and a single long line measured 694 px and ran off
       a 560 px canvas (the layout sweep caught that) */
    if(L.bottom.length){
      const b0 = L.bottom[0], b1 = L.bottom[L.bottom.length - 1];
      const wide = box(b0.x, b0.y, b1.x1 - b0.x, b0.h);
      frame(ctx, wide, COL.edge);
      lab(ctx, W, H, (wide.x + wide.x1) / 2, (wide.y + wide.y1) / 2 - 12, 'the closed form is for two bodies',
          COL.warn, 'italic 15px Georgia, serif', 'center', 'middle');
      lab(ctx, W, H, (wide.x + wide.x1) / 2, (wide.y + wide.y1) / 2 + 12,
          'this system has ' + M.sys.S.n + ' — choose another on the right',
          COL.warn, 'italic 14px Georgia, serif', 'center', 'middle');
    }
    drawCaption(ctx, L);
    return;
  }
  const S = drawSystem(ctx, W, H, M, b, {grid: ST.grid, path: ST.path, velocity: ST.velocity,
    force: false, com: true, tape: ST.tape, mass: ST.massOn});
  withClip(ctx, b, () => {
    worldPathClip(ctx, S.map, ex.pts1, COL.ref, 1.6, [6, 4], S.win);
    worldPathClip(ctx, S.map, ex.pts2, COL.ref, 1.6, [6, 4], S.win);
    for(const [x, y] of [[ex.now.x1, ex.now.y1], [ex.now.x2, ex.now.y2]])
      if(inWin([x, y], S.win)) dot(ctx, S.map.X(x), S.map.Y(y), 8, null, COL.ref, 1.8);
  });
  lab(ctx, W, H, b.x + 6, b.y + 26,
      'orange: Kepler’s own answer from the start state — the rings are where it puts the bodies now',
      COL.ref, SM_FONT, 'left', 'top');
  legendR(ctx, b, [[COL.ref, 'the exact orbit'], [M.bodies[0].col, M.bodies[0].name],
                   [M.bodies[1].col, M.bodies[1].name], [COL.com, 'centre of mass']]);
  /* panel 1: the error against time */
  const bb = L.bottom[0], h = ex.hist;
  const min = M.cfg.minutes, tf = min ? 60 : PH.DAY;
  if(h.length < 2){
    emptyPanel(ctx, W, H, bb, 'nothing to compare yet — press space to start the clock');
    if(L.bottom.length > 1) emptyPanel(ctx, W, H, L.bottom[1], 'the separation will be drawn here');
    drawCaption(ctx, L);
    return;
  }
  const xs = h.map(s => s.t / tf), ys = h.map(s => Math.max(1e-9, s.err));
  const thi = Math.max(1e-6, M.t / tf);
  const lo = -9, hi = Math.max(-3, Math.log10(Math.max.apply(null, ys.concat([1e-9]))) + 0.5);
  axesT(ctx, bb, 0, thi, lo, hi, {title: titleFor(bb, 'how far the integration has drifted from the exact orbit',
    'error against the exact orbit'), xlab: min ? 'minutes' : 'Earth days', ylab: 'log₁₀ |Δr| (m)',
    nx: 4, ny: 4});
  if(xs.length > 1) polyline(ctx, bb, xs, ys.map(v => Math.log10(v)), 0, thi, lo, hi, COL.pos, 1.8);
  labIn(ctx, W, H, bb, bb.x + 8, bb.y + 10, 'now: ' + (ex.err === 0 ? '0' : ex.err.toExponential(2) + ' m')
        + ' = ' + (ex.err / M.sep).toExponential(1) + ' of r', COL.pos, SM_FONT, 'left', 'top');
  /* panel 2: the separation, exact and numerical */
  if(L.bottom.length > 1){
    const cb = L.bottom[1];
    const rn = h.map(s => s.rn / 1e6), re = h.map(s => s.re / 1e6);
    const all = rn.concat(re);
    const rlo = all.length ? Math.min.apply(null, all) * 0.98 : 0;
    const rhi = all.length ? Math.max.apply(null, all) * 1.02 : 1;
    axesT(ctx, cb, 0, thi, rlo, rhi === rlo ? rlo + 1 : rhi,
      {title: titleFor(cb, 'the separation of the two bodies', 'separation'),
       xlab: min ? 'minutes' : 'Earth days', ylab: 'r (Mm)', nx: 4, ny: 4});
    if(xs.length > 1){
      polyline(ctx, cb, xs, re, 0, thi, rlo, rhi, COL.ref, 2.4, [6, 4]);
      polyline(ctx, cb, xs, rn, 0, thi, rlo, rhi, COL.pos, 1.4);
    }
    if(ex.el.kind === 'ellipse')
      labIn(ctx, W, H, cb, cb.x + 8, cb.y + 10, 'T = ' + plain(timeStr(ex.el.T, min)) + ', e = ' + fmt(ex.el.e, 5),
            COL.dim, SM_FONT, 'left', 'top');
    legendR(ctx, cb, [[COL.ref, 'Kepler'], [COL.pos, 'integrated']]);
  }
  drawCaption(ctx, L);
}

/* ---- view 5: what is conserved ------------------------------------------------------------ */
const CAPN_FULL = 'Not a PhET screen either. An isolated system keeps its energy, its momentum and its '
  + 'angular momentum. This integrator applies every force as an equal and opposite pair and every drift '
  + 'leaves r × v alone, so momentum and angular momentum survive to the last bit whatever the step, '
  + 'while the energy only wobbles by the order of the method and returns. That is the To Scale screen. The '
  + 'Model screen is different, and deliberately: its star is nailed down (so it absorbs momentum from '
  + 'nowhere) and its moon feels 10,200 times the planet’s pull with no reaction (so the third law does '
  + 'not hold), and this view measures both. Switch gravity off and the bodies leave on straight lines at '
  + 'exactly constant speed: the measured residual is printed, and from a scene’s start it reads a flat '
  + 'zero.';
const CAPN_SHORT = 'Energy, momentum and angular momentum along the run — exact to scale, bent on the Model screen.';
/* the order panel: a sweep over step counts, which needs no run at all */
function drawOrderPanel(ctx, W, H, bb, c){
  const o = c.order;
  const lx = o.N.map(n => Math.log10(n));
  const ally = o.pefrl.concat(o.phet).map(v => Math.log10(Math.max(1e-6, v)));
  const ylo = Math.min.apply(null, ally) - 0.5, yhi = Math.max.apply(null, ally) + 0.5;
  const X0 = lx[0] - 0.1, X1 = lx[lx.length - 1] + 0.1;
  axesT(ctx, bb, X0, X1, ylo, yhi,
    {title: titleFor(bb, 'error against steps over ' + fmt(o.T / PH.DAY, 1) + ' days: PEFRL '
       + fmt(o.slope('pefrl'), 2) + ', PhET\u2019s ' + fmt(o.slope('phet'), 2) + ' (the orders)',
       'order: ' + fmt(o.slope('pefrl'), 2) + ' vs ' + fmt(o.slope('phet'), 2)),
     xlab: 'log\u2081\u2080 steps', ylab: 'log\u2081\u2080 error (m)', nx: 4, ny: 4});
  polyline(ctx, bb, lx, o.pefrl.map(v => Math.log10(Math.max(1e-6, v))), X0, X1, ylo, yhi, COL.pos, 2);
  polyline(ctx, bb, lx, o.phet.map(v => Math.log10(Math.max(1e-6, v))), X0, X1, ylo, yhi, COL.phet, 2, [6, 4]);
  for(let i = 0; i < lx.length; i++){
    marker(ctx, bb, X0, X1, ylo, yhi, lx[i], Math.log10(Math.max(1e-6, o.pefrl[i])), COL.pos);
    marker(ctx, bb, X0, X1, ylo, yhi, lx[i], Math.log10(Math.max(1e-6, o.phet[i])), COL.phet);
  }
  legendR(ctx, bb, [[COL.pos, 'PEFRL (4 forces a step)'], [COL.phet, 'PhET\u2019s (1 force a step)']]);
}
function drawCons(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAPN_FULL, CAPN_SHORT, 2, 0.42, 1);
  const c = M.cn, b = L.main;
  const min = M.cfg.minutes, tf = min ? 60 : PH.DAY;
  const h = c.hist, thi = Math.max(1e-6, M.t / tf);
  const lo = -17, hi = 1;
  /* a run of length zero has a degenerate time axis whose every tick formats as "0" */
  if(h.length < 2){
    emptyPanel(ctx, W, H, b, 'nothing has drifted yet — press space to start the clock');
    drawOrderPanel(ctx, W, H, L.bottom[0], c);
    if(L.bottom.length > 1) emptyPanel(ctx, W, H, L.bottom[1], 'the energy will be drawn here');
    drawCaption(ctx, L);
    return;
  }
  frame(ctx, b, COL.edge);
  axesT(ctx, b, 0, thi, lo, hi, {title: titleFor(b, 'the constants of the motion, as the run goes on',
    'the constants of the motion'), xlab: min ? 'minutes' : 'Earth days',
    ylab: 'log₁₀ of the relative drift', nx: 5, ny: 6});
  const xs = h.map(s => s.t / tf);
  const put = (key, col, lw, dash) => {
    if(h.length < 2) return;
    const ys = h.map(s => Math.log10(Math.max(1e-17, s[key] || 1e-17)));
    polyline(ctx, b, xs, ys, 0, thi, lo, hi, col, lw, dash);
  };
  put('dE', COL.pos, 2);
  put('dL', COL.struct, 1.6);
  put('dP', COL.live, 1.6);
  if(ST.shadow && ST.gravity) put('dPhet', COL.phet, 1.8, [6, 4]);
  const items = [[COL.pos, '|ΔE/E|'], [COL.struct, '|ΔL/L|'], [COL.live, '|Δp|/p']];
  if(ST.shadow && ST.gravity) items.push([COL.phet, '|ΔE/E| with PhET’s step']);
  /* The notes go on whichever half of the box the curves are NOT in.  On the To Scale screen
     the drifts sit at 1e-14 and the top is empty; on the Model screen they run along the top
     and a note there is written across all three (it was). */
  const lvl = Math.log10(Math.max(1e-17, c.dE, c.dL, c.dP));
  const atTop = lvl < (lo + hi) / 2;
  const ny = n => atTop ? b.y + 10 + 16 * n : b.y1 - 10 - 16 * n;
  const nba = atTop ? 'top' : 'bottom';
  labIn(ctx, W, H, b, b.x + 8, ny(0), 'now: |ΔE/E| = ' + (c.dE === 0 ? '0' : c.dE.toExponential(1))
        + ', |ΔL/L| = ' + (c.dL === 0 ? '0' : c.dL.toExponential(1))
        + ', |Δp|/p = ' + (c.dP === 0 ? '0' : c.dP.toExponential(1)), COL.dim, SM_FONT, 'left', nba);
  if(c.broken.length)
    labFit(ctx, W, H, b.x + 8, ny(1), plain('PhET’s Model screen: ' + c.broken.join('; ')
           + ' — so these are not expected to hold'),
           'PhET’s Model screen bends the physics — these are not expected to hold',
           b.w - 16, COL.warn, SM_FONT, 'left', nba);
  if(!ST.gravity)
    labFit(ctx, W, H, b.x + 8, ny(2), 'gravity off: off the straight line by '
           + (c.coast.dev === 0 ? '0 m, exactly' : c.coast.dev.toExponential(2) + ' m')
           + ' over ' + plain(lenStr(c.coast.travel, 3)) + ', and |v| by '
           + (c.coast.dspeed === 0 ? '0 m/s, exactly' : c.coast.dspeed.toExponential(2) + ' m/s'),
           'gravity off: a straight line, to '
           + (c.coast.dev === 0 ? '0 m exactly' : c.coast.dev.toExponential(1) + ' m'),
           b.w - 16, COL.pos, SM_FONT, 'left', nba);
  /* with the force switched off the ledger still counts a potential the bodies no longer
     feel, so |dE/E| climbs.  That is the bookkeeping, not a defect, and it needs saying
     next to a curve that otherwise reads as one. */
  if(!ST.gravity)
    labFit(ctx, W, H, b.x + 8, ny(3), 'the energy still counts a potential the bodies no longer feel, '
           + 'so it is not conserved with the force off — p and L are, exactly',
           'E counts a potential nothing feels; p and L stay exact',
           b.w - 16, COL.dim, SM_FONT, 'left', nba);
  /* the legend goes on LAST: legendR rejects a corner that covers a registered label, so
     drawing it first is what makes the notes above get dropped instead (they were, on the
     Model screen, where the legend and the free space are both at the bottom) */
  legendR(ctx, b, items);
  /* panel 1: the order of both methods (it does not need a run, so it is drawn either way) */
  drawOrderPanel(ctx, W, H, L.bottom[0], c);
  /* panel 2: where the energy sits */
  if(L.bottom.length > 1){
    const cb = L.bottom[1];
    let big = 0;
    for(const s2 of h) big = Math.max(big, Math.abs(s2.K), Math.abs(s2.U), Math.abs(s2.K + s2.U));
    const pw = big > 0 ? 3 * Math.floor(Math.log10(big) / 3) : 0, sc = Math.pow(10, pw);
    const Ks = h.map(s2 => s2.K / sc), Us = h.map(s2 => s2.U / sc), Es = h.map(s2 => (s2.K + s2.U) / sc);
    const all = Ks.concat(Us).concat(Es);
    const elo = all.length ? Math.min.apply(null, all) : -1, ehi = all.length ? Math.max.apply(null, all) : 1;
    const pad = 0.08 * (ehi - elo || 1);
    axesT(ctx, cb, 0, thi, elo - pad, ehi + pad,
      {title: titleFor(cb, 'kinetic, potential and total energy', 'the energy'),
       xlab: min ? 'minutes' : 'Earth days',
       ylab: pw === 0 ? 'energy (J)' : 'energy (10' + supNum(pw) + ' J)', nx: 4, ny: 4});
    if(h.length > 1){
      polyline(ctx, cb, xs, Ks, 0, thi, elo - pad, ehi + pad, COL.struct, 1.6);
      polyline(ctx, cb, xs, Us, 0, thi, elo - pad, ehi + pad, COL.live, 1.6);
      polyline(ctx, cb, xs, Es, 0, thi, elo - pad, ehi + pad, COL.pos, 2.2);
    }
    legendR(ctx, cb, [[COL.struct, 'K'], [COL.live, 'U'], [COL.pos, 'E = K + U']]);
  }
  drawCaption(ctx, L);
}
/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx, W, H, M){
  LEGEND_RECTS = []; POLY_SEGS = []; LABELS = [];
  ctx.fillStyle = '#070b18'; ctx.fillRect(0, 0, W, H);
  if(M.view === 'model') drawModel(ctx, W, H, M);
  else if(M.view === 'scale') drawScale(ctx, W, H, M);
  else if(M.view === 'circ') drawCirc(ctx, W, H, M);
  else if(M.view === 'exact') drawExact(ctx, W, H, M);
  else drawCons(ctx, W, H, M);
}
function mainBox(ctx, W, H, view){
  if(view === 'model') return stageLayoutH(ctx, W, H, CAPM_FULL, CAPM_SHORT, 0, 0, 0).main;
  if(view === 'scale') return stageLayoutH(ctx, W, H, CAPS_FULL, CAPS_SHORT, 2, 0.34, 1).main;
  if(view === 'circ') return stageLayoutH(ctx, W, H, CAPC_FULL, CAPC_SHORT, 2, 0.36, 1).main;
  if(view === 'exact') return stageLayoutH(ctx, W, H, CAPE_FULL, CAPE_SHORT, 2, 0.34, 1).main;
  return stageLayoutH(ctx, W, H, CAPN_FULL, CAPN_SHORT, 2, 0.42, 1).main;
}
function dragsHere(view){ return view === 'model' || view === 'scale' || view === 'exact'; }
function makeScene(canvas){
  const S = {st: ST, W: 1100, H: 712};
  S.model = buildModel;
  S.draw = function(){ const ctx = canvas.getContext('2d'); drawView(ctx, S.W, S.H, buildModel()); };
  S.step = function(){ return runStep(); };
  /* the drags: any body, the tip of any velocity arrow (PhET's DraggableVectorNode, the one
     labelled V), and the two ends of the measuring tape.  Taking hold pauses the clock and
     re-saves the starting state, as PhET does. */
  S.pointer = function(type, x, y){
    if(type === 'up'){
      const had = DRAGM.what !== null;
      if(had && (DRAGM.what === 'body' || DRAGM.what === 'vel')) sysSaveStart(curSys());
      DRAGM.what = null; DRAGM.i = -1;
      return had;
    }
    if(!dragsHere(ST.view)) return false;
    const ctx = canvas.getContext('2d');
    const M = buildModel(), b = mainBox(ctx, S.W, S.H, ST.view), map = sysMap(b, M);
    const sys = curSys(), st = sys.S;
    if(type === 'down'){
      if(ST.velocity) for(let i = 0; i < st.n; i++){
        const TX = map.X(st.x[i]) + st.vx[i] * M.vscale, TY = map.Y(st.y[i]) - st.vy[i] * M.vscale;
        if(Math.hypot(TX - x, TY - y) <= 13){ DRAGM.what = 'vel'; DRAGM.i = i; ST.running = false; return true; }
      }
      for(let i = 0; i < st.n; i++){
        const X = map.X(st.x[i]), Y = map.Y(st.y[i]);
        const rp = Math.max(10, st.r[i] * map.s);
        if(Math.hypot(X - x, Y - y) <= rp + 4){ DRAGM.what = 'body'; DRAGM.i = i; ST.running = false; return true; }
      }
      if(ST.tape){ const t = tapeHit(map, sys.tape, x, y); if(t){ DRAGM.what = t; return true; } }
      return false;
    }
    if(type === 'move' && DRAGM.what){
      const wx = map.wx(x), wy = map.wy(y), c = M.centre, R = M.R;
      if(DRAGM.what === 'body'){
        st.x[DRAGM.i] = clamp(wx, c[0] - R, c[0] + R);
        st.y[DRAGM.i] = clamp(wy, c[1] - R, c[1] + R);
        sys.t = 0; sysClearPaths(sys);
        return true;
      }
      if(DRAGM.what === 'vel'){
        const X = map.X(st.x[DRAGM.i]), Y = map.Y(st.y[DRAGM.i]);
        st.vx[DRAGM.i] = (x - X) / M.vscale; st.vy[DRAGM.i] = -(y - Y) / M.vscale;
        sys.t = 0; sysClearPaths(sys);
        return true;
      }
      if(DRAGM.what === 'tapeA'){ sys.tape.ax = wx; sys.tape.ay = wy; return true; }
      if(DRAGM.what === 'tapeB'){ sys.tape.bx = wx; sys.tape.by = wy; return true; }
    }
    return false;
  };
  return S;
}
