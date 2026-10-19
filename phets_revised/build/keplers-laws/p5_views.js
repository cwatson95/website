
/* ================================================================== *
 *  views 3-5, the dispatch and the scene (drags live here)            *
 * ================================================================== */
const CAP3_FULL = 'PhET’s Third Law screen. The chart plots T^p against a^q for every semi-major axis the planet has '
  + 'visited (drag it to visit more); only a³ with T² gives a straight line through the origin, and its slope is '
  + '4π²/GM — the same for every body about this star and for nothing else. The orange curve is the law itself. '
  + 'Switch to log–log and every power becomes a straight line: T against a has slope 3/2 exactly, with PhET’s five '
  + 'target planets sitting on it. The panel on the right is that constant against the star’s mass.';
const CAP3_SHORT = 'T^p against a^q: only a³ with T² is a straight line. On log–log, T against a has slope 3/2.';
function drawThird(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAP3_FULL, CAP3_SHORT, 2, 0.40, 1);
  const st = M.st, d = M.thd;
  drawOrbitStage(ctx, W, H, M, L.main, {grid: st.grid, target: true, foci: false, string: false,
    axes: false, semiaxes: false, ecc: false, apsides: false, velocity: st.velocity, speedLab: st.speedLab,
    gravity: st.gravity, tape: st.tape, stopwatch: st.stopwatch, sectors: false,
    showA: st.showA, showT: st.showT});
  if(!d){ drawCaption(ctx, L); return; }
  /* panel 1: the chart, linear in the chosen powers or log-log */
  const bb = L.bottom[0];
  if(!st.loglog){
    const xhi = Math.pow(d.aMax, st.pa), yhi = Math.pow(d.Tmax, st.pt);
    axesT(ctx, bb, 0, xhi, 0, yhi, {title: titleFor(bb, 'T' + (st.pt > 1 ? '^' + st.pt : '') + ' against a'
        + (st.pa > 1 ? '^' + st.pa : '') + (d.th.correct ? ' — a straight line' : ' — not a straight line'),
        'T^' + st.pt + ' vs a^' + st.pa), xlab: 'a^' + st.pa + ' (AU^' + st.pa + ')',
      ylab: 'T^' + st.pt + ' (yr^' + st.pt + ')', nx: 5, ny: 4});
    /* the law over the whole range (orange), then the visited trace (green) */
    const lx = [], ly = [];
    for(let i = 0; i <= 80; i++){
      const a = d.aMax * i / 80;
      lx.push(Math.pow(a, st.pa)); ly.push(Math.pow(periodOf(a, starMu(st.mass)), st.pt));
    }
    polyline(ctx, bb, lx, ly, 0, xhi, 0, yhi, COL.ref, 1.4, [5, 4]);
    if(d.pts.length) polyline(ctx, bb, d.pts.map(p => p[0]), d.pts.map(p => p[1]), 0, xhi, 0, yhi, COL.pos, 2.4);
    if(d.tgt) marker(ctx, bb, 0, xhi, 0, yhi, Math.pow(d.tgt.a, st.pa),
                     Math.pow(periodOf(d.tgt.a, starMu(1)), st.pt), COL.target);
    marker(ctx, bb, 0, xhi, 0, yhi, d.th.ap, d.th.Tp, COL.live);
    labIn(ctx, W, H, bb, bb.x + 8, bb.y + 10, 'T^' + st.pt + '/a^' + st.pa + ' = ' + fmt(d.th.ratio, 4)
          + (d.th.correct ? ' — constant' : ' — it drifts'), d.th.correct ? COL.pos : COL.warn, LAB_FONT, 'left', 'top');
    legendR(ctx, bb, [[COL.ref, 'the law'], [COL.pos, 'a visited'], [COL.live, 'now']]);
  } else {
    const xlo = Math.log10(0.2), xhi = Math.log10(Math.max(6, d.aMax));
    const ylo = Math.log10(periodOf(0.2, starMu(st.mass))), yhi = Math.log10(periodOf(Math.max(6, d.aMax), starMu(st.mass)));
    axesT(ctx, bb, xlo, xhi, ylo, yhi, {title: titleFor(bb, 'log T against log a — slope 3/2, whatever the star',
      'log T vs log a'), xlab: 'log₁₀ a (AU)', ylab: 'log₁₀ T (yr)', nx: 5, ny: 4});
    const lx = [], ly = [];
    for(let i = 0; i <= 60; i++){
      const la = xlo + (xhi - xlo) * i / 60;
      lx.push(la); ly.push(Math.log10(periodOf(Math.pow(10, la), starMu(st.mass))));
    }
    polyline(ctx, bb, lx, ly, xlo, xhi, ylo, yhi, COL.ref, 1.6);
    for(const p of d.planets){
      marker(ctx, bb, xlo, xhi, ylo, yhi, Math.log10(p.a), Math.log10(p.T), COL.struct);
      labIn(ctx, W, H, bb, bb.x + bb.w * (Math.log10(p.a) - xlo) / (xhi - xlo) + 6,
            bb.y1 - bb.h * (Math.log10(p.T) - ylo) / (yhi - ylo) - 6, p.name, COL.struct, SM_FONT, 'left', 'bottom');
    }
    marker(ctx, bb, xlo, xhi, ylo, yhi, Math.log10(M.el.a), Math.log10(M.el.T), COL.live);
    const slope = (Math.log10(periodOf(4, starMu(st.mass))) - Math.log10(periodOf(1, starMu(st.mass))))
                / (Math.log10(4) - Math.log10(1));
    labIn(ctx, W, H, bb, bb.x + 8, bb.y + 10, 'measured slope ' + fmt(slope, 4) + ' (3/2 = 1.5)', COL.pos, LAB_FONT, 'left', 'top');
    legendR(ctx, bb, [[COL.ref, 'T = a^(3/2)/√M'], [COL.struct, 'PhET’s planets'], [COL.live, 'this orbit']]);
  }
  /* panel 2: the constant belongs to the star */
  if(L.bottom.length > 1){
    const cb = L.bottom[1], mlo = 0.5, mhi = 2;
    const ylo = klConst(mhi) * 0.85, yhi = klConst(mlo) * 1.05;
    axesT(ctx, cb, mlo, mhi, ylo, yhi, {title: titleFor(cb, 'T²/a³ = 4π²/GM against the star’s mass',
      'T²/a³ vs mass'), xlab: 'star mass (M☉)', ylab: 'yr²/AU³', nx: 4, ny: 4});
    const mx = [], my = [];
    for(let i = 0; i <= 60; i++){ const m = mlo + (mhi - mlo) * i / 60; mx.push(m); my.push(klConst(m)); }
    polyline(ctx, cb, mx, my, mlo, mhi, ylo, yhi, COL.ref, 1.6);
    marker(ctx, cb, mlo, mhi, ylo, yhi, st.mass, M.el.T * M.el.T / Math.pow(M.el.a, 3), COL.live);
    labIn(ctx, W, H, cb, cb.x + 8, cb.y + 10, 'this orbit: T²/a³ = ' + fmt(M.el.T * M.el.T / Math.pow(M.el.a, 3), 5),
          COL.live, SM_FONT, 'left', 'top');
  }
  drawCaption(ctx, L);
}

/* ================================================================== *
 *  view 4: all laws                                                   *
 * ================================================================== */
const CAP4_FULL = 'PhET’s All Laws screen: the shape, the pace and the scale on one orbit. Every overlay of the three '
  + 'screens is available at once — the foci and the string, the equal-area sectors, the semi-major axis and the period '
  + 'trace — with the swept-area bars and the T–a chart under the stage.';
const CAP4_SHORT = 'All three laws on one orbit: foci and string, equal-area sectors, and the T–a chart.';
function drawAll(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAP4_FULL, CAP4_SHORT, 2, 0.36, 1);
  const st = M.st;
  drawOrbitStage(ctx, W, H, M, L.main, {grid: st.grid, target: true, foci: st.foci, string: st.string && st.foci,
    axes: st.axes, semiaxes: st.semiaxes && st.axes, ecc: st.ecc, apsides: true, velocity: st.velocity,
    speedLab: st.speedLab, gravity: st.gravity, tape: st.tape, stopwatch: st.stopwatch,
    sectors: st.swept, showA: st.showA, showT: st.showT});
  const c = M.sec, d = M.thd;
  if(c && L.bottom.length){
    const bb = L.bottom[0], ymax = 1.3 * c.full;
    axesT(ctx, bb, -0.5, c.N - 0.5, 0, ymax, {title: titleFor(bb, 'swept area of each sector', 'swept area'),
      xlab: 'period division', ylab: 'area (AU²)', ny: 4,
      xticks: Array.from({length: c.N}, (_, i) => i), xfmt: v => String(Math.round(v) + 1)});
    const wbar = Math.min(40, bb.w / (c.N + 1) * 0.7);
    for(let k = 0; k < c.N; k++){
      const X = bb.x + bb.w * (k + 0.5) / c.N, hgt = bb.h * c.areas[k] / ymax;
      ctx.fillStyle = rgba(c.frac[k] >= 1 ? COL.sector : COL.sectorOn, 0.55);
      ctx.fillRect(X - wbar / 2, bb.y1 - hgt, wbar, hgt);
    }
    polyline(ctx, bb, [-0.5, c.N - 0.5], [c.full, c.full], -0.5, c.N - 0.5, 0, ymax, COL.ref, 1.4, [5, 4]);
  }
  if(d && L.bottom.length > 1){
    const cb = L.bottom[1], xhi = Math.pow(d.aMax, st.pa), yhi = Math.pow(d.Tmax, st.pt);
    axesT(ctx, cb, 0, xhi, 0, yhi, {title: titleFor(cb, 'T^' + st.pt + ' against a^' + st.pa, 'T^' + st.pt + ' vs a^' + st.pa),
      xlab: 'a^' + st.pa, ylab: 'T^' + st.pt, nx: 4, ny: 4});
    const lx = [], ly = [];
    for(let i = 0; i <= 60; i++){ const a = d.aMax * i / 60;
      lx.push(Math.pow(a, st.pa)); ly.push(Math.pow(periodOf(a, starMu(st.mass)), st.pt)); }
    polyline(ctx, cb, lx, ly, 0, xhi, 0, yhi, COL.ref, 1.4, [5, 4]);
    if(d.pts.length) polyline(ctx, cb, d.pts.map(p => p[0]), d.pts.map(p => p[1]), 0, xhi, 0, yhi, COL.pos, 2.2);
    marker(ctx, cb, 0, xhi, 0, yhi, d.th.ap, d.th.Tp, COL.live);
    labIn(ctx, W, H, cb, cb.x + 8, cb.y + 10, 'T^' + st.pt + '/a^' + st.pa + ' = ' + fmt(d.th.ratio, 4),
          d.th.correct ? COL.pos : COL.warn, SM_FONT, 'left', 'top');
  }
  drawCaption(ctx, L);
}

/* ================================================================== *
 *  view 5: Kepler's equation (analysis)                               *
 * ================================================================== */
const CAP5_FULL = 'Not a PhET screen: where the motion in time comes from. Draw the auxiliary circle of radius a about the '
  + 'centre of the ellipse and project the planet up onto it; the angle at the centre is the ECCENTRIC anomaly E, the angle '
  + 'at the star is the TRUE anomaly ν, and the MEAN anomaly M = nt is where a body going round at constant rate would '
  + 'be. Kepler’s equation M = E − e sin E ties them together and cannot be solved for E in elementary functions, so '
  + 'Newton does it: the panel on the right shows f(E) = E − e sin E − M with the tangent steps from PhET’s own '
  + 'starting guess E = M, and where PhET stops (a step under 0.01 rad) against where this file stops (1e-15).';
const CAP5_SHORT = 'The auxiliary circle, the three anomalies, and Newton solving M = E − e sin E in front of you.';
function drawAnom(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAP5_FULL, CAP5_SHORT, 2, 0.42, 1);
  const el = M.el, A = M.an, b = L.main;
  const map = orbitMap(b, M.R * 0.78), win = winOf(map, b);
  frame(ctx, b, COL.edge);
  if(!A){ lab(ctx, W, H, (b.x + b.x1) / 2, (b.y + b.y1) / 2, plain(M.warn || 'no orbit'), COL.warn,
              'italic 15px Georgia, serif', 'center', 'middle'); drawCaption(ctx, L); return; }
  const cw = Math.cos(el.w), sw = Math.sin(el.w), d = el.dir;
  const toW = (X, Y) => [X * cw - d * Y * sw, X * sw + d * Y * cw];          /* perifocal -> world */
  const C = toW(-el.c, 0);                                                    /* the ellipse centre */
  /* the auxiliary circle and the ellipse */
  const circ = [], ell = [];
  for(let i = 0; i <= 180; i++){
    const th = TAU * i / 180;
    circ.push(toW(-el.c + el.a * Math.cos(th), el.a * Math.sin(th)));
    ell.push(toW(-el.c + el.a * Math.cos(th), el.b * Math.sin(th)));
  }
  worldPathClip(ctx, map, circ, rgba(COL.struct, 0.55), 1.4, [5, 4], win);
  worldPathClip(ctx, map, ell, COL.orbit, 2, null, win);
  /* the three points: P on the ellipse, Q above it on the circle, and the mean point */
  const P = toW(-el.c + el.a * Math.cos(A.E), el.b * Math.sin(A.E));
  const Q = toW(-el.c + el.a * Math.cos(A.E), el.a * Math.sin(A.E));
  const Mp = toW(-el.c + el.a * Math.cos(A.M), el.a * Math.sin(A.M));
  seg(ctx, map, C, Q, COL.struct, 1.4);
  seg(ctx, map, P, Q, rgba(COL.struct, 0.6), 1.2, [3, 3]);
  seg(ctx, map, C, Mp, COL.ref, 1.4, [6, 4]);
  seg(ctx, map, [0, 0], P, COL.live, 1.6);
  /* the periapsis direction, from which all three angles are measured */
  const Pp = toW(el.a * (1 - el.e), 0);
  seg(ctx, map, C, toW(-el.c + el.a * 1.06, 0), rgba(COL.dim, 0.7), 1, [2, 3]);
  bodyDraw(ctx, map, 0, 0, el.star, COL.star, 4);
  dot(ctx, map.X(C[0]), map.Y(C[1]), 3.5, null, COL.struct, 1.4);
  dot(ctx, map.X(Q[0]), map.Y(Q[1]), 5, COL.struct, '#fff', 1.2);
  dot(ctx, map.X(Mp[0]), map.Y(Mp[1]), 5, COL.ref, '#fff', 1.2);
  bodyDraw(ctx, map, P[0], P[1], massToRadius(PHET.PLANET), COL.planet, 4);
  lab(ctx, W, H, map.X(Q[0]) + 8, map.Y(Q[1]) - 6, 'E = ' + plain(degStr(A.E)), COL.struct, LAB_FONT);
  lab(ctx, W, H, map.X(Mp[0]) + 8, map.Y(Mp[1]) + 8, 'M = ' + plain(degStr(A.M)), COL.ref, LAB_FONT);
  lab(ctx, W, H, map.X(P[0]) + 8, map.Y(P[1]) + 10, 'ν = ' + plain(degStr(A.nu)), COL.live, LAB_FONT);
  lab(ctx, W, H, map.X(Pp[0]), map.Y(Pp[1]) - 8, 'periapsis', '#ffd24a', SM_FONT, 'center', 'bottom');
  lab(ctx, W, H, b.x + 6, b.y + 8, titleFor(b, 'the auxiliary circle: the planet on the ellipse, projected to the circle of radius a',
      'the auxiliary circle'), '#aeb6c6', 'italic 13px Georgia, serif', 'left', 'top');
  lab(ctx, W, H, b.x1 - 6, b.y + 8, plain(scaleNote(map)) + ' — e = ' + fmt(el.e, 3) + ', t = ' + plain(yrStr(A.t)),
      COL.dim, SM_FONT, 'right', 'top');
  legendR(ctx, b, [[COL.orbit, 'the orbit'], [COL.struct, 'auxiliary circle, E'], [COL.ref, 'the mean point, M'],
                   [COL.live, 'the planet, ν']]);
  /* panel 1: the three anomalies over one period */
  const bb = L.bottom[0];
  axesT(ctx, bb, 0, 1, 0, 360, {title: titleFor(bb, 'the three anomalies over one period', 'anomalies over a period'),
    xlab: 't / T', ylab: 'degrees', nx: 5, ny: 4});
  const fx = A.curve.map(c2 => c2[0] / TAU);
  polyline(ctx, bb, fx, A.curve.map(c2 => c2[0] / DEG), 0, 1, 0, 360, COL.ref, 1.6);
  polyline(ctx, bb, fx, A.curve.map(c2 => c2[1] / DEG), 0, 1, 0, 360, COL.struct, 1.6);
  /* nu runs 0 -> 360 over one period and needs no wrap; taking it mod 360 put a false
     vertical line down the right-hand edge of the panel */
  polyline(ctx, bb, fx, A.curve.map(c2 => c2[2] / DEG), 0, 1, 0, 360, COL.live, 1.6);
  marker(ctx, bb, 0, 1, 0, 360, A.M / TAU, A.M / DEG, COL.ref);
  marker(ctx, bb, 0, 1, 0, 360, A.M / TAU, A.E / DEG, COL.struct);
  marker(ctx, bb, 0, 1, 0, 360, A.M / TAU, A.nu / DEG, COL.live);
  legendR(ctx, bb, [[COL.ref, 'M (uniform)'], [COL.struct, 'E'], [COL.live, 'ν']]);
  /* panel 2: Newton on f(E) */
  if(L.bottom.length > 1){
    const cb = L.bottom[1];
    const Elo = Math.max(0, Math.min(A.E, A.M) - 0.9), Ehi = Math.max(A.E, A.M) + 0.9;
    const fs = [], xs = [];
    let fmin = 0, fmax = 0;
    for(let i = 0; i <= 80; i++){
      const E2 = Elo + (Ehi - Elo) * i / 80, f = E2 - el.e * Math.sin(E2) - A.M;
      xs.push(E2); fs.push(f); fmin = Math.min(fmin, f); fmax = Math.max(fmax, f);
    }
    const pad = 0.12 * (fmax - fmin || 1);
    axesT(ctx, cb, Elo, Ehi, fmin - pad, fmax + pad, {title: titleFor(cb, 'Newton on f(E) = E − e sin E − M',
      'Newton on f(E)'), xlab: 'E (rad)', ylab: 'f(E)', nx: 4, ny: 4});
    polyline(ctx, cb, [Elo, Ehi], [0, 0], Elo, Ehi, fmin - pad, fmax + pad, '#3a4152', 1, [3, 3]);
    polyline(ctx, cb, xs, fs, Elo, Ehi, fmin - pad, fmax + pad, COL.pos, 2);
    for(let k = 0; k < A.trace.length - 1; k++){
      const E0 = A.trace[k], f0 = E0 - el.e * Math.sin(E0) - A.M, E1 = A.trace[k + 1];
      /* the tangent to the axis, then the drop to the curve: the staircase Newton walks */
      polyline(ctx, cb, [E0, E1], [f0, 0], Elo, Ehi, fmin - pad, fmax + pad, rgba(COL.ref, 0.8), 1.1);
      polyline(ctx, cb, [E1, E1], [0, E1 - el.e * Math.sin(E1) - A.M], Elo, Ehi, fmin - pad, fmax + pad, rgba(COL.ref, 0.45), 1, [3, 3]);
      marker(ctx, cb, Elo, Ehi, fmin - pad, fmax + pad, E0, f0, k === A.stop + 1 ? COL.warn : COL.ref);
    }
    marker(ctx, cb, Elo, Ehi, fmin - pad, fmax + pad, A.E, 0, COL.live);
    labIn(ctx, W, H, cb, cb.x + 8, cb.y + 10, 'from E₀ = M: ' + (A.stop + 1) + ' steps to PhET’s 0.01 rad, '
          + A.it + ' to 1e-15', COL.dim, SM_FONT, 'left', 'top');
  }
  drawCaption(ctx, L);
}

/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx, W, H, M){
  LEGEND_RECTS = []; POLY_SEGS = []; LABELS = [];
  ctx.fillStyle = '#070b18'; ctx.fillRect(0, 0, W, H);
  if(M.view === 'first') drawFirst(ctx, W, H, M);
  else if(M.view === 'second') drawSecond(ctx, W, H, M);
  else if(M.view === 'third') drawThird(ctx, W, H, M);
  else if(M.view === 'all') drawAll(ctx, W, H, M);
  else drawAnom(ctx, W, H, M);
}
/* the stage box each view drags in (the same layout the view used) */
function mainBox(ctx, W, H, view){
  if(view === 'first') return stageLayoutH(ctx, W, H, CAP1_FULL, CAP1_SHORT, 0, 0, 0).main;
  if(view === 'second') return stageLayoutH(ctx, W, H, CAP2_FULL, CAP2_SHORT, 1, 0.34, 1).main;
  if(view === 'third') return stageLayoutH(ctx, W, H, CAP3_FULL, CAP3_SHORT, 2, 0.40, 1).main;
  if(view === 'all') return stageLayoutH(ctx, W, H, CAP4_FULL, CAP4_SHORT, 2, 0.36, 1).main;
  return stageLayoutH(ctx, W, H, CAP5_FULL, CAP5_SHORT, 2, 0.42, 1).main;
}
function dragsHere(view){ return view !== 'anom'; }
function makeScene(canvas){
  const S = {st: ST, W: 1100, H: 712};
  S.model = buildModel;
  S.draw = function(){ const ctx = canvas.getContext('2d'); drawView(ctx, S.W, S.H, buildModel()); };
  S.step = function(){ const moved = runStep(); if(moved && ST.view === 'anom'){
      const el = klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular);
      if(el.allowed) ST.mfrac = ((SIM.t / el.T) % 1 + 1) % 1; }
    return moved; };
  /* the drags: the planet, the tip of its velocity arrow, and the two ends of the tape */
  S.pointer = function(type, x, y){
    if(type === 'up'){ const had = DRAGK.what !== null; DRAGK.what = null; return had; }
    if(!dragsHere(ST.view)) return false;
    const ctx = canvas.getContext('2d');
    const b = mainBox(ctx, S.W, S.H, ST.view), map = orbitMap(b, viewRadius());
    const M = buildModel(), now = M.now;
    if(type === 'down'){
      const PX = map.X(now.x), PY = map.Y(now.y);
      if(ST.velocity){
        const TX = PX + now.vx * VSCALE, TY = PY - now.vy * VSCALE;
        if(Math.hypot(TX - x, TY - y) <= 14){ DRAGK.what = 'vel'; ST.running = false; return true; }
      }
      if(Math.hypot(PX - x, PY - y) <= 16){ DRAGK.what = 'planet'; ST.running = false; return true; }
      if(ST.tape){ const t = tapeHit(map, SIM.tape, x, y); if(t){ DRAGK.what = t; return true; } }
      return false;
    }
    if(type === 'move' && DRAGK.what){
      const wx = map.wx(x), wy = map.wy(y);
      if(DRAGK.what === 'planet'){
        const R = viewRadius(), rmin = starRadius(ST.mass) * 1.4;
        let px = clamp(wx, -R, R), py = clamp(wy, -R, R);
        const r = Math.hypot(px, py);
        /* dropped exactly on the star there is no direction to push along: keep the one the
           planet already had (PhET nudges it to (0.01, 0) instead) */
        if(r < rmin){
          if(r > 1e-12){ const s = rmin / r; px *= s; py *= s; }
          else { const r0 = Math.hypot(ST.px, ST.py) || 1; px = rmin * ST.px / r0; py = rmin * ST.py / r0; }
        }
        ST.px = px; ST.py = py; SIM.t = 0; SIM.sweep = {erased: false, tErase: 0}; SIM.periodTrace = null;
        traceNote(klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular));
        return true;
      }
      if(DRAGK.what === 'vel'){
        if(ST.circular) return false;                 /* held circular: the arrow is not free */
        const PX = map.X(ST.px), PY = map.Y(ST.py);
        ST.vx = (x - PX) / VSCALE; ST.vy = -(y - PY) / VSCALE;
        SIM.t = 0; SIM.sweep = {erased: false, tErase: 0}; SIM.periodTrace = null;
        traceNote(klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular));
        return true;
      }
      if(DRAGK.what === 'tapeA'){ SIM.tape.ax = wx; SIM.tape.ay = wy; return true; }
      if(DRAGK.what === 'tapeB'){ SIM.tape.bx = wx; SIM.tape.by = wy; return true; }
    }
    return false;
  };
  return S;
}
