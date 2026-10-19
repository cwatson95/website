
/* ================================================================== *
 *  views 3-4 (the analysis pair), the dispatch and the scene          *
 * ================================================================== */
const CAPE_FULL = 'Not a PhET screen. Two bodies are the one case Newton could solve in closed form: the separation '
  + 'r = r₂ − r₁ moves as a single body about μ = G(m₁+m₂), so each body traces a similar conic about the '
  + 'centre of mass while that centre drifts in a straight line for ever. The orange curves are that exact solution, '
  + 'drawn from the state the run started at; the coloured trails are what the integrator has actually done. The panel '
  + 'below is the distance between them — the integrator’s error — as it grows.';
const CAPE_SHORT = 'The exact two-body solution (orange) against the integrated path: their difference is below.';
function drawExact(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAPE_FULL, CAPE_SHORT, 2, 0.34, 1);
  const st = M.st, b = L.main, ex = M.ex;
  if(!ex){
    frame(ctx, b, COL.edge);
    lab(ctx, W, H, (b.x + b.x1) / 2, (b.y + b.y1) / 2,
        M.sys.S.n === 1 ? 'one body has nowhere to fall: add a second on the lab view'
                        : 'the exact solution is for two bodies; this system has ' + M.sys.S.n,
        COL.warn, 'italic 15px Georgia, serif', 'center', 'middle');
    drawCaption(ctx, L);
    return;
  }
  const S = drawSystem(ctx, W, H, M, b, {grid: st.grid, path: st.path, velocity: st.velocity,
    speedLab: st.speedLab, gravity: false, com: true, tape: st.tape});
  /* the exact orbits of both bodies, and where each one should be now (clipped to the stage,
     as the scene itself is: a ring whose centre is one pixel inside still draws 7 px out) */
  withClip(ctx, b, () => {
    worldPathClip(ctx, S.map, ex.pts1, COL.ref, 1.6, [6, 4], S.win);
    worldPathClip(ctx, S.map, ex.pts2, COL.ref, 1.6, [6, 4], S.win);
    for(const [x, y] of [[ex.now.x1, ex.now.y1], [ex.now.x2, ex.now.y2]])
      if(inWin([x, y], S.win)) dot(ctx, S.map.X(x), S.map.Y(y), 7, null, COL.ref, 1.6);
  });
  lab(ctx, W, H, b.x + 6, b.y + 26, 'orange: Kepler’s own answer from the start state — rings are where it puts the bodies now',
      COL.ref, SM_FONT, 'left', 'top');
  legendR(ctx, b, [[COL.ref, 'the exact orbits'], [M.bodies[0].col, 'body 1'], [M.bodies[1].col, 'body 2'],
                   [COL.com, 'centre of mass']]);
  /* panel 1: the error against time */
  const bb = L.bottom[0], h = SIM.ehist;
  const xs = h.map(s => yrOf(s.t)), ys = h.map(s => Math.max(1e-16, s.err));
  const thi = Math.max(1e-3, yrOf(M.sys.t));
  const lo = -14, hi = Math.max(-6, Math.log10(Math.max(1e-14, Math.max.apply(null, ys.concat([1e-14])))) + 0.5);
  axesT(ctx, bb, 0, thi, lo, hi, {title: titleFor(bb, 'how far the integration has drifted from the exact orbit',
    'error vs exact'), xlab: 'years', ylab: 'log₁₀ |Δr| (AU)', nx: 4, ny: 4});
  if(xs.length > 1) polyline(ctx, bb, xs, ys.map(v => Math.log10(v)), 0, thi, lo, hi, COL.pos, 1.8);
  labIn(ctx, W, H, bb, bb.x + 8, bb.y + 10, 'now: ' + (ex.err === 0 ? '0' : ex.err.toExponential(2) + ' AU'),
        COL.pos, SM_FONT, 'left', 'top');
  /* panel 2: the separation, exact and numerical */
  if(L.bottom.length > 1){
    const cb = L.bottom[1];
    const rn = h.map(s => s.rn), re = h.map(s => s.re);
    const all = rn.concat(re);
    const rlo = all.length ? Math.min.apply(null, all) * 0.95 : 0, rhi = all.length ? Math.max.apply(null, all) * 1.05 : 1;
    axesT(ctx, cb, 0, thi, rlo, rhi, {title: titleFor(cb, 'the separation of the two bodies', 'separation'),
      xlab: 'years', ylab: '|r| (AU)', nx: 4, ny: 4});
    if(xs.length > 1){
      polyline(ctx, cb, xs, re, 0, thi, rlo, rhi, COL.ref, 2.2, [6, 4]);
      polyline(ctx, cb, xs, rn, 0, thi, rlo, rhi, COL.pos, 1.4);
    }
    if(ex.el.kind === 'ellipse'){
      labIn(ctx, W, H, cb, cb.x + 8, cb.y + 10, 'T = ' + fmt(yrOf(ex.el.T), 4) + ' yr, e = ' + fmt(ex.el.e, 4),
            COL.dim, SM_FONT, 'left', 'top');
    }
    legendR(ctx, cb, [[COL.ref, 'Kepler'], [COL.pos, 'integrated']]);
  }
  drawCaption(ctx, L);
}

const CAPC_FULL = 'Not a PhET screen either. Every kick this integrator takes is an equal and opposite pair and every '
  + 'drift leaves r × v alone, so momentum and angular momentum are conserved to rounding — whatever the step. '
  + 'The energy is not: it is conserved only to the order of the method, and the top panel shows all three drifting (or '
  + 'not) as the run goes on. PhET’s own step is run beside ours on the same system, and the panel below halves the '
  + 'step four times to measure both orders: four for PEFRL with its forces re-evaluated, one for PhET’s as shipped.';
const CAPC_SHORT = 'Energy, momentum and angular momentum along the run, PhET’s integrator beside ours, and both orders.';
function drawConserve(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAPC_FULL, CAPC_SHORT, 2, 0.42, 1);
  const c = M.cn, b = L.main;
  frame(ctx, b, COL.edge);
  if(!c){ lab(ctx, W, H, (b.x + b.x1) / 2, (b.y + b.y1) / 2, 'no run yet', COL.dim, LAB_FONT, 'center', 'middle');
          drawCaption(ctx, L); return; }
  /* the drifts, on a log axis */
  const h = c.hist, thi = Math.max(1e-3, yrOf(M.sys.t));
  const lo = -17, hi = -3;
  axesT(ctx, b, 0, thi, lo, hi, {title: titleFor(b, 'the constants of the motion, as the run goes on',
    'the constants of the motion'), xlab: 'years', ylab: 'log₁₀ of the relative drift', nx: 5, ny: 5});
  const xs = h.map(s => yrOf(s.t));
  const put = (key, col, lw, dash) => {
    if(h.length < 2) return;
    const ys = h.map(s => Math.log10(Math.max(1e-17, s[key] || 1e-17)));
    polyline(ctx, b, xs, ys, 0, thi, lo, hi, col, lw, dash);
  };
  put('dE', COL.pos, 2);
  put('dL', COL.struct, 1.6);
  put('dP', COL.live, 1.6);
  if(M.st.shadow) put('dPhet', COL.phet, 1.8, [6, 4]);
  const items = [[COL.pos, '|ΔE/E| (ours)'], [COL.struct, '|ΔL/L|'], [COL.live, '|Δp|/p']];
  if(M.st.shadow) items.push([COL.phet, '|ΔE/E| (PhET’s step)']);
  legendR(ctx, b, items);
  labIn(ctx, W, H, b, b.x + 8, b.y + 10, 'now: |ΔE/E| = ' + (c.dE === 0 ? '0' : c.dE.toExponential(1))
        + ', |ΔL/L| = ' + (c.dL === 0 ? '0' : c.dL.toExponential(1))
        + ', |Δp|/p = ' + (c.dP === 0 ? '0' : c.dP.toExponential(1)), COL.dim, SM_FONT, 'left', 'top');
  if(c.merged) labIn(ctx, W, H, b, b.x + 8, b.y + 26, 'a collision has merged two bodies: the energy dropped for a '
    + 'physical reason and the sampling stopped there', COL.warn, SM_FONT, 'left', 'top');
  /* panel 1: the order of both methods */
  const bb = L.bottom[0], o = c.order;
  const lx = o.N.map(n => Math.log10(n));
  const ally = o.pefrl.concat(o.phet).map(v => Math.log10(Math.max(1e-16, v)));
  const ylo = Math.min.apply(null, ally) - 0.5, yhi = Math.max.apply(null, ally) + 0.5;
  /* the measured orders go in the TITLE: a floating label in this panel lands on PhET's own
     curve, which runs across the top of it at every step count */
  axesT(ctx, bb, lx[0] - 0.1, lx[lx.length - 1] + 0.1, ylo, yhi,
    {title: titleFor(bb, 'error against steps: PEFRL ' + fmt(o.slope('pefrl'), 2) + ', PhET’s '
       + fmt(o.slope('phet'), 2) + ' (the orders)', 'order: ' + fmt(o.slope('pefrl'), 2) + ' vs ' + fmt(o.slope('phet'), 2)),
     xlab: 'log₁₀ steps', ylab: 'log₁₀ error (AU)', nx: 4, ny: 4});
  polyline(ctx, bb, lx, o.pefrl.map(v => Math.log10(Math.max(1e-16, v))), lx[0] - 0.1, lx[lx.length - 1] + 0.1, ylo, yhi, COL.pos, 2);
  polyline(ctx, bb, lx, o.phet.map(v => Math.log10(Math.max(1e-16, v))), lx[0] - 0.1, lx[lx.length - 1] + 0.1, ylo, yhi, COL.phet, 2, [6, 4]);
  for(let i = 0; i < lx.length; i++){
    marker(ctx, bb, lx[0] - 0.1, lx[lx.length - 1] + 0.1, ylo, yhi, lx[i], Math.log10(Math.max(1e-16, o.pefrl[i])), COL.pos);
    marker(ctx, bb, lx[0] - 0.1, lx[lx.length - 1] + 0.1, ylo, yhi, lx[i], Math.log10(Math.max(1e-16, o.phet[i])), COL.phet);
  }
  legendR(ctx, bb, [[COL.pos, 'PEFRL (4 forces a step)'], [COL.phet, 'PhET’s (1 force a step)']]);
  /* panel 2: where the energy sits */
  if(L.bottom.length > 1){
    const cb = L.bottom[1];
    /* a five-digit tick label reaches the rotated axis title 40 px left of the frame, so the
       energies are drawn in whatever power of ten keeps the numbers short, and the axis says so */
    let big = 0;
    for(const s2 of h) big = Math.max(big, Math.abs(s2.K), Math.abs(s2.U), Math.abs(s2.K + s2.U));
    const pw = big > 0 ? Math.max(0, 3 * Math.floor(Math.log10(big) / 3)) : 0, sc = Math.pow(10, pw);
    const Ks = h.map(s2 => s2.K / sc), Us = h.map(s2 => s2.U / sc), Es = h.map(s2 => (s2.K + s2.U) / sc);
    const all = Ks.concat(Us).concat(Es);
    const elo = all.length ? Math.min.apply(null, all) : -1, ehi = all.length ? Math.max.apply(null, all) : 1;
    const pad = 0.08 * (ehi - elo || 1);
    axesT(ctx, cb, 0, thi, elo - pad, ehi + pad, {title: titleFor(cb, 'kinetic, potential and total energy', 'the energy'),
      xlab: 'years', ylab: 'energy' + (pw ? ' (10' + (pw === 3 ? '\u00b3' : '\u2078') + ')' : ''), nx: 4, ny: 4});
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
  if(M.view === 'intro') drawIntro(ctx, W, H, M);
  else if(M.view === 'lab') drawLab(ctx, W, H, M);
  else if(M.view === 'exact') drawExact(ctx, W, H, M);
  else drawConserve(ctx, W, H, M);
}
function mainBox(ctx, W, H, view){
  if(view === 'intro') return stageLayoutH(ctx, W, H, CAPI_FULL, CAPI_SHORT, 0, 0, 0).main;
  if(view === 'lab') return stageLayoutH(ctx, W, H, CAPL_FULL, CAPL_SHORT, 0, 0, 0).main;
  if(view === 'exact') return stageLayoutH(ctx, W, H, CAPE_FULL, CAPE_SHORT, 2, 0.34, 1).main;
  return stageLayoutH(ctx, W, H, CAPC_FULL, CAPC_SHORT, 2, 0.42, 1).main;
}
function dragsHere(view){ return view === 'intro' || view === 'lab' || view === 'exact'; }
function makeScene(canvas){
  const S = {st: ST, W: 1100, H: 712};
  S.model = buildModel;
  S.draw = function(){ const ctx = canvas.getContext('2d'); drawView(ctx, S.W, S.H, buildModel()); };
  S.step = function(){ return runStep(); };
  /* the drags: any body, the tip of any velocity arrow, and the two ends of the tape.  A drag
     pauses the clock and re-saves the starting state, as PhET does when the user takes hold. */
  S.pointer = function(type, x, y){
    if(type === 'up'){
      const had = DRAGM.what !== null;
      if(had){ const sys = curSys(); sysSaveStart(sys); if(sysKey(ST.view) === 'lab') histReset(); }
      DRAGM.what = null; DRAGM.i = -1;
      return had;
    }
    if(!dragsHere(ST.view)) return false;
    const ctx = canvas.getContext('2d');
    const b = mainBox(ctx, S.W, S.H, ST.view), map = sysMap(b, viewRadius());
    const sys = curSys();
    if(type === 'down'){
      for(let i = 0; i < sys.S.n; i++){
        if(ST.velocity){
          const TX = map.X(sys.S.x[i]) + sys.S.vx[i] * VSCALE, TY = map.Y(sys.S.y[i]) - sys.S.vy[i] * VSCALE;
          if(Math.hypot(TX - x, TY - y) <= 13){ DRAGM.what = 'vel'; DRAGM.i = i; ST.running = false; return true; }
        }
      }
      for(let i = 0; i < sys.S.n; i++){
        const X = map.X(sys.S.x[i]), Y = map.Y(sys.S.y[i]);
        const rp = Math.max(9, massToRadius(sys.S.m[i]) * map.s);
        if(Math.hypot(X - x, Y - y) <= rp + 4){ DRAGM.what = 'body'; DRAGM.i = i; ST.running = false; return true; }
      }
      if(ST.tape){ const t = tapeHit(map, SIM.tape, x, y); if(t){ DRAGM.what = t; return true; } }
      return false;
    }
    if(type === 'move' && DRAGM.what){
      const wx = map.wx(x), wy = map.wy(y);
      if(DRAGM.what === 'body'){
        const R = viewRadius();
        sys.S.x[DRAGM.i] = clamp(wx, -R, R); sys.S.y[DRAGM.i] = clamp(wy, -R, R);
        sys.t = 0; sysClearPaths(sys);
        if(sysKey(ST.view) === 'lab') ST.preset = 'custom';
        return true;
      }
      if(DRAGM.what === 'vel'){
        const X = map.X(sys.S.x[DRAGM.i]), Y = map.Y(sys.S.y[DRAGM.i]);
        sys.S.vx[DRAGM.i] = (x - X) / VSCALE; sys.S.vy[DRAGM.i] = -(y - Y) / VSCALE;
        sys.t = 0; sysClearPaths(sys);
        if(sysKey(ST.view) === 'lab') ST.preset = 'custom';
        return true;
      }
      if(DRAGM.what === 'tapeA'){ SIM.tape.ax = wx; SIM.tape.ay = wy; return true; }
      if(DRAGM.what === 'tapeB'){ SIM.tape.bx = wx; SIM.tape.by = wy; return true; }
    }
    return false;
  };
  return S;
}
