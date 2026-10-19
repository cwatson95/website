
/* ================================================================== *
 *  the orbit stage (shared by the first four views) and views 1-2     *
 * ================================================================== */
/* the ellipse sampled uniformly in the ECCENTRIC anomaly, which puts more points where the
   orbit turns fastest (near periapsis) instead of fewest */
function ellipsePts(el, n){
  const N = n || 256, cw = Math.cos(el.w), sw = Math.sin(el.w), d = el.dir, out = [];
  for(let i = 0; i <= N; i++){
    const E = TAU * i / N, X = el.a * (Math.cos(E) - el.e), Y = el.b * Math.sin(E);
    out.push([X * cw - d * Y * sw, X * sw + d * Y * cw]);
  }
  return out;
}
function orbitMap(b, R){ return worldFitUp(b, {xmin: -R, xmax: R, ymin: -R, ymax: R}, 0); }
function winOf(map, b){ return {x0: map.wx(b.x), x1: map.wx(b.x1), y0: map.wy(b.y1), y1: map.wy(b.y)}; }
function inWin(p, w){ return p[0] >= w.x0 && p[0] <= w.x1 && p[1] >= w.y0 && p[1] <= w.y1; }
/* the force on PhET's planet (its mass is 50e28 kg and does not enter the orbit), in units of
   the pull at 1 AU from our Sun -- so the arrow's scale can be stated exactly */
function gravRatio(el){ return (F_REF * F_REF) / (el.r * el.r) * el.M_sun; }

/* the whole orbit picture: grid, target, orbit, sectors, overlays, bodies, arrows.
   `show` selects the overlays; every view passes its own set. */
function drawOrbitStage(ctx, W, H, M, b, show){
  const el = M.el, st = M.st, map = orbitMap(b, M.R), win = winOf(map, b);
  const now = M.now;
  frame(ctx, b, COL.edge);
  /* what the picture is, and its scale, BEFORE anything else is registered: drawn last, the
     title loses the label registry's shove and ends up outside the box (seen at 1400x820 with
     an eccentric orbit, where the velocity label sits where the title wants to be) */
  lab(ctx, W, H, b.x + 6, b.y + 8, (st.mass === 1 ? 'our Sun' : fmt(st.mass, 2) + ' M☉')
      + ' — a = ' + sigf(el.a, 4) + ' AU, e = ' + fmt(el.e, 3) + (el.allowed ? ', T = ' + fmt(el.T, 4) + ' yr' : ''),
      '#aeb6c6', 'italic 13px Georgia, serif', 'left', 'top');
  lab(ctx, W, H, b.x1 - 6, b.y + 8, plain(scaleNote(map)) + ' — true shape, both axes alike',
      COL.dim, SM_FONT, 'right', 'top');
  if(M.warn) lab(ctx, W, H, (b.x + b.x1) / 2, b.y + 30, plain(M.warn) + ' The clock will not run.', COL.warn,
                 'italic 15px Georgia, serif', 'center', 'top');
  if(show.grid) gridDraw(ctx, map, b, 1, '#141a27');
  /* the target orbit: PhET draws it only for our Sun */
  if(M.tgtOn && show.target){
    const t = M.tgt, tel = {a: t.a, b: t.a * Math.sqrt(1 - t.e * t.e), e: t.e, w: 0, dir: 1};
    worldPathClip(ctx, map, ellipsePts(tel, 192), COL.target, 1.6, [7, 5], win);
    const tip = conicPoint({p: t.a * (1 - t.e * t.e), e: t.e, w: 0, dir: 1}, PI);
    if(inWin(tip, win)) lab(ctx, W, H, map.X(tip[0]) - 6, map.Y(tip[1]) - 8, t.name + '&rsquo;s orbit', COL.target, SM_FONT, 'right', 'bottom');
  }
  /* the swept sectors, filled by how much of each has been swept */
  if(show.sectors && M.sec){
    const c = M.sec;
    withClip(ctx, b, () => {
      for(let k = 0; k < c.N; k++){
        if(c.frac[k] <= 0) continue;
        const nu0 = c.cuts[k];
        const nu1 = c.frac[k] >= 1 ? c.cuts[k + 1] : klSweepNu(el, c.N, k, c.frac[k]);
        const poly = klSectorPoly(el, nu0, nu1, 40);
        const shade1 = 0.13 + 0.30 * (k + 1) / c.N;
        worldFill(ctx, map, poly, rgba(c.frac[k] >= 1 ? COL.sector : COL.sectorOn, shade1));
      }
      for(let k = 0; k <= c.N; k++){
        const p = conicPoint(el, c.cuts[k]);
        seg(ctx, map, [0, 0], p, rgba(COL.sector, 0.5), 1, [3, 3]);
      }
    });
  }
  /* the orbit itself: dashed and orange when PhET would not allow it */
  const pts = ellipsePts(el, 256);
  worldPathClip(ctx, map, pts, el.allowed ? COL.orbit : COL.warn, el.allowed ? 2 : 1.6,
                el.allowed ? null : [6, 5], win);
  /* first-law furniture */
  const F = M.foci;
  if(show.axes){
    const cw = Math.cos(el.w), sw = Math.sin(el.w), d = el.dir;
    const P = [F.centre[0] + el.a * cw, F.centre[1] + el.a * sw];
    const Ap = [F.centre[0] - el.a * cw, F.centre[1] - el.a * sw];
    const B1 = [F.centre[0] - d * el.b * sw, F.centre[1] + d * el.b * cw];
    const B2 = [F.centre[0] + d * el.b * sw, F.centre[1] - d * el.b * cw];
    segClip(ctx, map, Ap, P, win, rgba(COL.struct, 0.75), 1.2, [5, 4]);
    segClip(ctx, map, B1, B2, win, rgba(COL.struct, 0.75), 1.2, [5, 4]);
    if(show.semiaxes){
      segClip(ctx, map, F.centre, P, win, COL.amaj, 2.4);
      segClip(ctx, map, F.centre, B1, win, COL.bmin, 2.4);
      /* two thirds out, not at the midpoint: the midpoint of a is inside the star's disc */
      const mid = [F.centre[0] + 0.66 * (P[0] - F.centre[0]), F.centre[1] + 0.66 * (P[1] - F.centre[1])];
      const midb = [F.centre[0] + 0.66 * (B1[0] - F.centre[0]), F.centre[1] + 0.66 * (B1[1] - F.centre[1])];
      if(inWin(mid, win)) lab(ctx, W, H, map.X(mid[0]), map.Y(mid[1]) - 9, 'a = ' + sigf(el.a, 4) + ' AU', COL.amaj, LAB_FONT, 'center', 'bottom');
      if(inWin(midb, win)) lab(ctx, W, H, map.X(midb[0]) + 7, map.Y(midb[1]), 'b = ' + sigf(el.b, 4) + ' AU', COL.bmin, LAB_FONT);
    }
  }
  if(show.foci){
    for(const f of [F.f1, F.f2]){
      if(!inWin(f, win)) continue;
      const X = map.X(f[0]), Y = map.Y(f[1]);
      ctx.strokeStyle = COL.foci; ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.moveTo(X - 5, Y - 5); ctx.lineTo(X + 5, Y + 5);
      ctx.moveTo(X - 5, Y + 5); ctx.lineTo(X + 5, Y - 5); ctx.stroke();
    }
    if(inWin(F.f2, win)) lab(ctx, W, H, map.X(F.f2[0]), map.Y(F.f2[1]) + 9, 'empty focus', COL.foci, SM_FONT, 'center', 'top');
    if(show.string){
      const d1 = Math.hypot(now.x, now.y), d2 = Math.hypot(now.x - F.f2[0], now.y - F.f2[1]);
      segClip(ctx, map, [0, 0], [now.x, now.y], win, COL.foci, 1.6);
      segClip(ctx, map, F.f2, [now.x, now.y], win, COL.foci, 1.6);
      /* both strings can lie along the same line (a planet at an apsis), so each label is
         pushed off its OWN segment, one up and one down, rather than both "above" */
      const off = (a, b2, sgn) => { const dx = b2[0] - a[0], dy = b2[1] - a[1], L = Math.hypot(dx, dy) || 1;
        const k = 0.10 * Math.max(el.a, 0.2) * sgn;
        return [(a[0] + b2[0]) / 2 - k * dy / L, (a[1] + b2[1]) / 2 + k * dx / L]; };
      const m1 = off([0, 0], [now.x, now.y], 1), m2 = off(F.f2, [now.x, now.y], -1);
      if(inWin(m1, win)) lab(ctx, W, H, map.X(m1[0]), map.Y(m1[1]), 'd&#8321; = ' + sigf(d1, 4), COL.foci, SM_FONT, 'center', 'middle');
      if(inWin(m2, win)) lab(ctx, W, H, map.X(m2[0]), map.Y(m2[1]), 'd&#8322; = ' + sigf(d2, 4), COL.foci, SM_FONT, 'center', 'middle');
    }
  }
  if(show.ecc){
    segClip(ctx, map, F.centre, [0, 0], win, COL.cfoc, 2.4);
    const mid = [F.centre[0] / 2, F.centre[1] / 2];
    /* the star's disc covers the midpoint of c at every mass, so the label clears its radius */
    if(inWin(mid, win)) lab(ctx, W, H, map.X(mid[0]), map.Y(mid[1]) + el.star * map.s + 10,
                            'c = ae = ' + sigf(el.c, 4), COL.cfoc, SM_FONT, 'center', 'top');
  }
  if(show.apsides){
    const P = conicPoint(el, 0), A = conicPoint(el, PI);
    const outward = (p, txt, col) => {
      const X = map.X(p[0]), Y = map.Y(p[1]), L = Math.hypot(X - map.X(0), Y - map.Y(0)) || 1;
      const ux = (X - map.X(0)) / L, uy = (Y - map.Y(0)) / L;
      diamond(ctx, X, Y, 5, col, '#fff');
      lab(ctx, W, H, X + 10 * ux, Y + 10 * uy, txt, col, SM_FONT, ux < -0.3 ? 'right' : (ux > 0.3 ? 'left' : 'center'),
          uy > 0.3 ? 'top' : (uy < -0.3 ? 'bottom' : 'middle'));
    };
    if(st.peri && inWin(P, win)) outward(P, 'periapsis ' + sigf(el.q, 4) + ' AU', '#ffd24a');
    if(st.apo && inWin(A, win)) outward(A, 'apoapsis ' + sigf(el.Q, 4) + ' AU', COL.struct);
  }
  /* the period trace (PhET's "Period (T)" checkbox): the arc drawn since play began */
  if(show.showT && SIM.periodTrace && el.allowed){
    const pt = SIM.periodTrace, n = 90, arc = [];
    for(let i = 0; i <= n; i++){ const s2 = klStateAt(el, pt.t0 + pt.t * i / n); arc.push([s2.x, s2.y]); }
    worldPathClip(ctx, map, arc, COL.struct, 4, null, win);
  }
  /* the semiaxes overlay already draws (and labels) a, so the third law's own
     "semi-major axis" line is skipped rather than drawn on top of it */
  if(show.showA && !(show.axes && show.semiaxes)){
    const cw = Math.cos(el.w), sw = Math.sin(el.w);
    const P = [F.centre[0] + el.a * cw, F.centre[1] + el.a * sw];
    segClip(ctx, map, F.centre, P, win, COL.amaj, 2.4);
    const mid = [F.centre[0] + 0.66 * (P[0] - F.centre[0]), F.centre[1] + 0.66 * (P[1] - F.centre[1])];
    if(inWin(mid, win)) lab(ctx, W, H, map.X(mid[0]), map.Y(mid[1]) - 9, 'a = ' + sigf(el.a, 4) + ' AU', COL.amaj, LAB_FONT, 'center', 'bottom');
  }
  /* the star, to scale (PhET's radius rule), and the planet */
  const starPx = bodyDraw(ctx, map, 0, 0, el.star, COL.star, 4);
  lab(ctx, W, H, starPx.X, starPx.Y + starPx.rp + 8, (st.mass === 1 ? 'our Sun' : fmt(st.mass, 2) + ' M☉'), COL.star, SM_FONT, 'center', 'top');
  const pl = bodyDraw(ctx, map, now.x, now.y, massToRadius(PHET.PLANET), COL.planet, 4);
  /* the arrows */
  if(show.velocity){
    const t = velArrow(ctx, map, now.x, now.y, now.vx, now.vy, VSCALE, COL.pos);
    dot(ctx, t.TX, t.TY, 4.5, COL.pos, '#fff', 1.2);       /* the handle you drag */
    /* off the shaft, not along it: the label was struck through by its own arrow */
    const L2 = Math.hypot(t.TX - t.X, t.TY - t.Y) || 1;
    lab(ctx, W, H, t.TX + 9 * (t.TX - t.X) / L2, t.TY + 9 * (t.TY - t.Y) / L2 - 8,
        'v = ' + fmt(Math.hypot(now.vx, now.vy), 2) + ' km/s', COL.pos, SM_FONT,
        t.TX < t.X ? 'right' : 'left', 'bottom');
  } else if(show.speedLab){
    lab(ctx, W, H, pl.X + pl.rp + 7, pl.Y, fmt(Math.hypot(now.vx, now.vy), 2) + ' km/s', COL.pos, SM_FONT);
  }
  if(show.gravity){
    const g = gravRatio(el), ux = -now.x / now.r, uy = -now.y / now.r;
    const maxPx = 0.42 * Math.min(b.w, b.h);
    const a1 = forceArrow(ctx, map, now.x, now.y, g * ux, g * uy, 1, st.fpow, COL.ref, maxPx);
    forceArrow(ctx, map, 0, 0, -g * ux, -g * uy, 1, st.fpow, COL.ref, maxPx);
    if(a1 && a1.capped) lab(ctx, W, H, b.x + 8, b.y1 - 10, 'the gravity arrow is longer than the view and is drawn cut \u2014 lower the power',
                            COL.warn, SM_FONT, 'left', 'bottom');
  }
  if(show.tape) tapeDraw(ctx, W, H, map, SIM.tape, COL.struct);
  if(show.stopwatch) swChip(ctx, W, H, b, 'stopwatch  ' + plain(yrStr(SIM.sw)), SIM.swRun);
  return {map, win, pl, starPx};
}

/* ================================================================== *
 *  view 1: the first law                                              *
 * ================================================================== */
const CAP1_FULL = 'PhET’s First Law screen. Drag the planet, or the tip of its green velocity arrow, and the orbit is '
  + 'recomputed in closed form: a from the vis-viva equation, e and the direction of periapsis from the eccentricity vector. '
  + 'The star sits at one focus; the other is empty. The two ticked-on "string" lengths d₁ + d₂ stay at 2a wherever the '
  + 'planet is — that is what an ellipse is. Both axes share one scale, so the shape on screen is the shape of the orbit.';
const CAP1_SHORT = 'Drag the planet or its velocity arrow: the ellipse follows, with the star at one focus and d₁ + d₂ = 2a.';
function drawFirst(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAP1_FULL, CAP1_SHORT, 0, 0, 0);
  const st = M.st;
  drawOrbitStage(ctx, W, H, M, L.main, {grid: st.grid, target: true, foci: st.foci, string: st.string && st.foci,
    axes: st.axes, semiaxes: st.semiaxes && st.axes, ecc: st.ecc, apsides: false, velocity: st.velocity,
    speedLab: st.speedLab, gravity: st.gravity, tape: st.tape, stopwatch: st.stopwatch, sectors: false,
    showA: false, showT: false});
  if(M.el.allowed){
    const items = [[COL.orbit, 'the orbit']];
    if(st.foci) items.push([COL.foci, 'foci' + (st.string ? ', d₁ + d₂ = 2a' : '')]);
    if(st.axes) items.push([COL.struct, 'axes']);
    if(st.semiaxes && st.axes){ items.push([COL.amaj, 'a']); items.push([COL.bmin, 'b']); }
    if(st.ecc) items.push([COL.cfoc, 'c = ae']);
    if(M.tgtOn) items.push([COL.target, M.tgt.name + '’s orbit']);
    if(st.velocity) items.push([COL.pos, 'v (drag the tip)']);
    if(st.gravity) items.push([COL.ref, 'gravity ×10^' + st.fpow]);
    legendR(ctx, L.main, items);
  }
  drawCaption(ctx, L);
}

/* ================================================================== *
 *  view 2: the second law                                             *
 * ================================================================== */
const CAP2_FULL = 'PhET’s Second Law screen. The orbit is cut into N pieces that take equal times — equal steps of the '
  + 'MEAN anomaly M, not of the angle you see — and each piece has exactly the same area, πab/N. Press play and the '
  + 'sectors are erased and fill again as the planet sweeps them: slowly near apoapsis, in a rush past the star. The bars '
  + 'below are PhET’s swept-area chart; the dashed line is πab/N, which every finished sector reaches.';
const CAP2_SHORT = 'N sectors of equal time have equal area πab/N; press play and watch them fill. The bars are the areas.';
function drawSecond(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAP2_FULL, CAP2_SHORT, 1, 0.34, 1);
  const st = M.st;
  const S = drawOrbitStage(ctx, W, H, M, L.main, {grid: st.grid, target: false, foci: false, string: false,
    axes: false, semiaxes: false, ecc: false, apsides: true, velocity: st.velocity, speedLab: st.speedLab,
    gravity: st.gravity, tape: st.tape, stopwatch: st.stopwatch, sectors: true, showA: false, showT: false});
  const c = M.sec;
  if(c){
    /* the area and time written on each sector */
    if(st.areaVals || st.timeVals){
      for(let k = 0; k < c.N; k++){
        if(c.frac[k] <= 1e-9) continue;          /* an empty sector has nothing to say */
        const nu = klSweepNu(M.el, c.N, k, 0.5), p = conicPoint(M.el, nu);
        const q = [p[0] * 0.62, p[1] * 0.62];
        if(!inWin(q, S.win)) continue;
        const txt = (st.areaVals ? sigf(c.areas[k], 3) + ' AU&sup2;' : '') + (st.areaVals && st.timeVals ? '  ' : '')
                  + (st.timeVals ? plain(yrStr(c.frac[k] * c.dt)) : '');
        lab(ctx, W, H, S.map.X(q[0]), S.map.Y(q[1]), txt, '#e8dcff', SM_FONT, 'center', 'middle');
      }
    }
    legendR(ctx, L.main, [[COL.orbit, 'the orbit'], [rgba(COL.sector, 0.35), 'a finished sector, πab/N'],
                          [rgba(COL.sectorOn, 0.35), 'the one being swept'], [COL.planet, 'the planet']]);
    /* the bars */
    const bb = L.bottom[0];
    const ymax = 1.3 * c.full;
    axesT(ctx, bb, -0.5, c.N - 0.5, 0, ymax, {title: titleFor(bb, 'swept area of each sector (PhET’s chart)', 'swept area'),
      xlab: 'period division', ylab: 'area (AU²)', nx: Math.min(c.N, 6), ny: 4,
      xticks: Array.from({length: c.N}, (_, i) => i), xfmt: v => String(Math.round(v) + 1)});
    const wbar = Math.min(46, bb.w / (c.N + 1) * 0.72);
    for(let k = 0; k < c.N; k++){
      const X = bb.x + bb.w * (k + 0.5) / c.N, hgt = bb.h * c.areas[k] / ymax;
      ctx.fillStyle = rgba(c.frac[k] >= 1 ? COL.sector : COL.sectorOn, 0.55);
      ctx.fillRect(X - wbar / 2, bb.y1 - hgt, wbar, hgt);
      ctx.strokeStyle = rgba('#ffffff', 0.25); ctx.lineWidth = 1;
      ctx.strokeRect(X - wbar / 2, bb.y1 - hgt, wbar, hgt);
    }
    polyline(ctx, bb, [-0.5, c.N - 0.5], [c.full, c.full], -0.5, c.N - 0.5, 0, ymax, COL.ref, 1.4, [5, 4]);
    labIn(ctx, W, H, bb, bb.x1 - 6, bb.y1 - bb.h * c.full / ymax - 7, 'πab/N = ' + sigf(c.full, 4) + ' AU²',
          COL.ref, SM_FONT, 'right', 'bottom');
  }
  drawCaption(ctx, L);
}
