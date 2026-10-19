#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What looking at the PNGs found.  The audit is blind to all of it — it
inspects text only.

  1. The proton was drawn 12.5 px across, which swallows PhET's n = 1 orbit
     (14.7 px) whole and crowds n = 2.
  2. The classical spiral's trail was reconstructed with the CURRENT angular
     speed for the whole history, so it drew an arc of something that never
     happened.  The forward map is invertible; step it backwards exactly.
  3. "1 levels too close to label".
  4. The small Schrodinger cloud was drawn at a FIXED screen size whatever n
     was, so the one thing the ladder behind it is saying — that the atom grows
     with n — was contradicted by the cloud on top of it.  Scaled so <r> lands
     on PhET's drawn radius for that n, and said on the canvas.
  5. The de Broglie wave on the standing-wave view had an amplitude of 6 px on
     a 55 px ring, times a sin(phase) that a still frame can catch near zero —
     so the view's whole subject was invisible.  The amplitude is now a stated
     fraction of the ring, and the full-amplitude shape is drawn faintly behind
     the live wave so the nodes are visible at every phase.
  6. The ensemble panel's y axis ran 0 to 1 for bars of 0.2, and the mean-hops
     note sat behind the first bar.
  7. legendAuto dodges POLY_SEGS, and a scatter of fills is not in it, so the
     lifetime legend sat on two data points.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(fname, pairs):
    p = os.path.join(HERE, fname)
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        if s.count(old) == 0 and s.count(new) == 1:
            continue          # already applied by an aborted earlier run
        assert s.count(old) == 1, ("%s: %r appears %d times" % (fname, old[:70], s.count(old)))
        s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(s)
    print(fname, "patched")


patch("p4_views.js", [
    # 1. the proton
    ("""function drawAtomInBox(ctx, M, G, X, Y){
  const st = M.st, s = G.s;
  const px = X(0), py = Y(0);""",
     """/* PhET draws a fat proton; at 8 x 1.6 view units it covered its own n = 1
   orbit (15 units) completely.  7 units across is still generous and leaves
   the ground-state orbit visible. */
function protonR(s){ return Math.max(3, 7 * s); }
function drawAtomInBox(ctx, M, G, X, Y){
  const st = M.st, s = G.s;
  const px = X(0), py = Y(0);"""),
    ("""  if(st.model === 'classical'){
    disc(ctx, px, py, Math.max(4, 8 * s * 1.6), COL.proton);
    if(!M.dead){
      const [ex, ey] = electronXY(st);
      /* the spiral it has already run down */
      ctx.strokeStyle = rgba(COL.struct, 0.35); ctx.lineWidth = 1;
      ctx.beginPath();
      const a0 = ATOM.cls.a, r0 = ATOM.cls.r;
      for(let k = 0; k <= 160; k++){
        const rr = r0 + (PHET.classicalR0 - r0) * k / 160;
        const aa = a0 + (PHET.classicalR0 - rr) / PHET.classicalDrdt * ATOM.cls.w * 0.7;
        const xx = X(rr * Math.cos(aa)), yy = Y(rr * Math.sin(aa));
        if(k === 0) ctx.moveTo(xx, yy); else ctx.lineTo(xx, yy);
      }
      ctx.stroke();""",
     """  if(st.model === 'classical'){
    disc(ctx, px, py, protonR(s), COL.proton);
    if(!M.dead){
      const [ex, ey] = electronXY(st);
      /* the path it has already run down, integrated BACKWARDS through the
         exact inverse of the forward step (r += dr, a += w dt, w /= spin).
         Running it forwards from r_0 with today's angular speed drew an arc of
         something that never happened. */
      ctx.strokeStyle = rgba(COL.struct, 0.35); ctx.lineWidth = 1;
      ctx.beginPath();
      let br = ATOM.cls.r, ba = ATOM.cls.a, bw = ATOM.cls.w;
      for(let k = 0; k <= ATOM.ticks; k++){
        const xx = X(br * Math.cos(ba)), yy = Y(br * Math.sin(ba));
        if(k === 0) ctx.moveTo(xx, yy); else ctx.lineTo(xx, yy);
        bw /= PHET.classicalSpin;
        br += PHET.classicalDrdt * DT_TICK;
        ba += bw * DT_TICK;
        if(br > PHET.classicalR0) break;
      }
      ctx.stroke();"""),
    ("""  if(st.model === 'experiment'){
    disc(ctx, px, py, Math.max(4, 8 * s * 1.6), COL.proton);""",
     """  if(st.model === 'experiment'){
    disc(ctx, px, py, protonR(s), COL.proton);"""),
    ("""  disc(ctx, px, py, Math.max(4, 8 * s * 1.6), COL.proton);
  if(st.model === 'debroglie')""",
     """  disc(ctx, px, py, protonR(s), COL.proton);
  if(st.model === 'debroglie')"""),
    # the true-radius rings, a little more visible
    ("""    if(rr < G.side / 2) ring(ctx, px, py, rr, 'rgba(184,236,76,0.22)', 1, [1, 4]);""",
     """    if(rr < G.side / 2) ring(ctx, px, py, rr, 'rgba(184,236,76,0.34)', 1, [1, 4]);"""),
    # 3. the plural
    ("""  if(labelled < NMAX) labelIfClear(ctx, x0, b.y + 30, (NMAX - labelled) + ' levels too close to label',""",
     """  if(labelled < NMAX) labelIfClear(ctx, x0, b.y + 30,
    (NMAX - labelled) + (NMAX - labelled === 1 ? ' level' : ' levels') + ' too close to label',"""),
    # 4. the small cloud follows n
    ("""function drawCloudSmall(ctx, M, px, py, side){
  const n = M.n, l = M.l, m = M.m;
  const G = 34, rmax = cloudExtent(n, l);
  const cg = cloudGrid(n, l, m, G, rmax);
  const half = Math.min(side * 0.44, viewRadius(NMAX) * 0.9 * (side / PHET.boxSide));
  const cell = 2 * half / G;""",
     """function drawCloudSmall(ctx, M, px, py, side){
  const n = M.n, l = M.l, m = M.m;
  const G = 44, rmax = cloudExtent(n, l);
  const cg = cloudGrid(n, l, m, G, rmax);
  /* the cloud has to GROW with n, or it contradicts the orbit ladder drawn
     behind it: <r> is put on PhET's drawn radius for this n and the rest of
     the cloud follows that scale */
  const pxPerA0 = viewRadius(n) * (side / PHET.boxSide) / meanR(n, l);
  const half = Math.min(side * 0.47, rmax * pxPerA0);
  const cell = 2 * half / G;"""),
])

patch("p5_views.js", [
    # 5. the standing wave
    ("""  const amp = 0.45 * ((st.showExact ? trueViewRadius(1) : viewRadius(1)) * sc) * 2.2;
  const ph = ATOM.angle;""",
     """  /* a fraction of the RING, not of the n = 1 radius: on the true ladder the
     n = 1 radius is 1/36 of n = 6 and the wave came out 2 px tall */
  const amp = 0.24 * R;
  const ph = ATOM.angle;"""),
    ("""  } else {
    ctx.strokeStyle = COL.electron; ctx.lineWidth = 2;
    ctx.beginPath();
    for(let k = 0; k <= 240; k++){
      const t = TAU * k / 240, rr = R + amp * Math.sin(nu * t) * Math.sin(ph);
      const x = cx + rr * Math.cos(t), y = cy - rr * Math.sin(t);
      if(k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }""",
     """  } else {
    /* the full-amplitude shape, faint, so the nodes are visible at every phase:
       the live wave breathes as sin(phase) and a still frame can catch it flat */
    for(const [fac, col, lw] of [[1, 'rgba(90,200,224,0.28)', 1], [Math.sin(ph), COL.electron, 2]]){
      ctx.strokeStyle = col; ctx.lineWidth = lw;
      ctx.beginPath();
      for(let k = 0; k <= 240; k++){
        const t = TAU * k / 240, rr = R + amp * Math.sin(nu * t) * fac;
        const x = cx + rr * Math.cos(t), y = cy - rr * Math.sin(t);
        if(k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
  }"""),
    ("""      const x = cx + R * Math.cos(t), y = cy - ys * R * Math.sin(t) - amp * 0.42 / 0.45 * Math.sin(nu * t) * Math.sin(ph);""",
     """      const x = cx + R * Math.cos(t), y = cy - ys * R * Math.sin(t) - amp * Math.sin(nu * t) * Math.sin(ph);"""),
    ("""    + 'zero only at the integers. The radial and 3-D-height pictures exaggerate the amplitude — the wave is a '
    + 'phase, not a displacement — and the exaggeration is 0.45 and 0.42 of the n = 1 radius, PhET’s own.';""",
     """    + 'zero only at the integers. The radial and 3-D-height pictures exaggerate the amplitude — the wave is a '
    + 'phase, not a displacement — at 0.24 of the ring radius, and the faint outline behind the live wave is the '
    + 'full amplitude it reaches, drawn so the nodes stay visible while it breathes.';"""),
    # 6. the ensemble panel
    ("""  axes(ctx, b, 0.5, Math.max(1.5, nF - 0.5), 0, 1, {title: st.trials + ' seeded cascades: measured against exact',
    xlab: 'lower level n′', ylab: 'fraction of first hops', nx: Math.max(2, nF - 1), ny: nyFor(b.h),
    xticks: cats, xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 1)});
  /* the note is mandatory: it goes down before the optional z labels */
  label(ctx, b.x + 8, b.y1 - 16, 'mean hops per cascade ' + fmt(M.ens.mean, 3)""",
     """  /* auto-range: five channels share 1.0, so a fixed 0-1 axis left the bars in
     the bottom fifth of the panel */
  let yTop = 0.25;
  for(const r of rows) yTop = Math.max(yTop, r.f, r.p);
  yTop = Math.min(1, yTop * 1.35);
  axes(ctx, b, 0.5, Math.max(1.5, nF - 0.5), 0, yTop, {title: st.trials + ' seeded cascades: measured against exact',
    xlab: 'lower level n′', ylab: 'fraction of first hops', nx: Math.max(2, nF - 1), ny: nyFor(b.h),
    xticks: cats, xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 2)});
  /* the note is mandatory: it goes down before the optional z labels, and at
     the TOP of the panel, where the bars are not */
  label(ctx, b.x + 8, b.y + 5, 'mean hops per cascade ' + fmt(M.ens.mean, 3)"""),
    ("""    '#767e92', '10.5px -apple-system, sans-serif', 'left', 'top');
  /* the legend goes down before the z labels""",
     """    '#767e92', '10.5px -apple-system, sans-serif', 'left', 'top');
  /* the legend goes down before the z labels"""),
    ("""    ctx.fillStyle = COL.live;
    ctx.fillRect(X - bw2 / 2, b.y1 - b.h * r.f, bw2, b.h * r.f);
    const se = Math.sqrt(r.p * (1 - r.p) / st.trials);
    ctx.strokeStyle = COL.ref; ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(X - bw2, b.y1 - b.h * r.p); ctx.lineTo(X + bw2, b.y1 - b.h * r.p); ctx.stroke();
    ctx.strokeStyle = 'rgba(232,132,58,0.55)'; ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(X, b.y1 - b.h * (r.p - 2 * se)); ctx.lineTo(X, b.y1 - b.h * (r.p + 2 * se)); ctx.stroke();
    const zy = b.y1 - b.h * Math.max(r.f, r.p) - 4;""",
     """    const hf = b.h * clamp(r.f / yTop, 0, 1), hp = b.h * clamp(r.p / yTop, 0, 1);
    ctx.fillStyle = COL.live;
    ctx.fillRect(X - bw2 / 2, b.y1 - hf, bw2, hf);
    const se = Math.sqrt(r.p * (1 - r.p) / st.trials);
    ctx.strokeStyle = COL.ref; ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(X - bw2, b.y1 - hp); ctx.lineTo(X + bw2, b.y1 - hp); ctx.stroke();
    ctx.strokeStyle = 'rgba(232,132,58,0.55)'; ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(X, b.y1 - b.h * clamp((r.p - 2 * se) / yTop, 0, 1));
    ctx.lineTo(X, b.y1 - b.h * clamp((r.p + 2 * se) / yTop, 0, 1)); ctx.stroke();
    const zy = b.y1 - Math.max(hf, hp) - 4;"""),
    ("""    labelIfClear(ctx, X, zy > b.y + 16 ? zy : b.y1 - b.h * Math.max(r.f, r.p) + 14,""",
     """    labelIfClear(ctx, X, zy > b.y + 22 ? zy : b.y1 - Math.max(hf, hp) + 14,"""),
    ("""      'z = ' + fmt(r.z, 2), Math.abs(r.z) < 3 ? COL.pos : COL.ref,
      '10px -apple-system, sans-serif', 'center', zy > b.y + 16 ? 'bottom' : 'top');""",
     """      'z = ' + fmt(r.z, 2), Math.abs(r.z) < 3 ? COL.pos : COL.ref,
      '10px -apple-system, sans-serif', 'center', zy > b.y + 22 ? 'bottom' : 'top');"""),
    # 7. the lifetime scatter goes into POLY_SEGS so legendAuto dodges it
    ("""    const Y = c.y1 - c.h * (Math.log10(t.tau) - tlo) / (thi - tlo);
    disc(ctx, X, Y, 3.4, mix(COL.pos, COL.live, t.l / Math.max(1, NMAX - 1)));""",
     """    const Y = c.y1 - c.h * (Math.log10(t.tau) - tlo) / (thi - tlo);
    disc(ctx, X, Y, 3.4, mix(COL.pos, COL.live, t.l / Math.max(1, NMAX - 1)));
    /* a scatter of fills is invisible to legendAuto, which dodges POLY_SEGS;
       record each point as a short segment (never zero length, Known-bad) so
       the legend does not land on the data */
    POLY_SEGS.push(X - 4, Y, X + 4, Y);"""),
    # the orbital cloud, a little finer
    ("""  const GRID = 74;""",
     """  const GRID = 92;"""),
])

patch("p3_state.js", [
    ("""        const v = columnDensity(n, l, m, x, z, 96);""",
     """        const v = columnDensity(n, l, m, x, z, 72);"""),
])
