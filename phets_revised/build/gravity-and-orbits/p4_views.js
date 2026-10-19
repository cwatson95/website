
/* ================================================================== *
 *  the stage both PhET screens share, and views 1-2                   *
 * ================================================================== */
function sysMap(b, M){
  const c = M.centre || [0, 0], R = M.R;
  return worldFitUp(b, {xmin: c[0] - R, xmax: c[0] + R, ymin: c[1] - R, ymax: c[1] + R}, 0);
}
function winOf(map, b){ return {x0: map.wx(b.x), x1: map.wx(b.x1), y0: map.wy(b.y1), y1: map.wy(b.y)}; }
function inWin(p, w){ return p[0] >= w.x0 && p[0] <= w.x1 && p[1] >= w.y0 && p[1] <= w.y1; }
/* "1 px = 2.38 Mm": the scale is a measurement, so it is printed, not assumed */
function scaleNoteGo(map){ return '1 px = ' + lenStr(1 / map.s, 3); }
/* the measuring tape reads kilometres, as PhET's does */
function tapeDrawKm(ctx, W, H, map, tape, col){
  const AX = map.X(tape.ax), AY = map.Y(tape.ay), BX = map.X(tape.bx), BY = map.Y(tape.by);
  ctx.beginPath(); ctx.moveTo(AX, AY); ctx.lineTo(BX, BY);
  ctx.strokeStyle = col; ctx.lineWidth = 1.6; ctx.setLineDash([6, 4]); ctx.stroke(); ctx.setLineDash([]);
  POLY_SEGS.push(AX, AY, BX, BY);
  ctx.beginPath(); ctx.rect(AX - 5, AY - 5, 10, 10); ctx.fillStyle = col; ctx.fill();
  dot(ctx, BX, BY, 5, null, col, 2);
  const d = Math.hypot(tape.bx - tape.ax, tape.by - tape.ay);
  lab(ctx, W, H, (AX + BX) / 2, (AY + BY) / 2 - 10, kmStr(d, 5), col, LAB_FONT, 'center', 'bottom');
  return d;
}
/* A label that takes the SHORT form when the long one will not fit the width it is given.
   The estimate is the same one lab() and the layout sweep use (0.52 of the font size per
   character), so a string that passes here passes the audit's off-canvas rule too. */
function labFit(ctx, W, H, x, y, longT, shortT, maxW, col, font, al, ba){
  const fs = parseFloat((font || LAB_FONT).match(/([\d.]+)px/)[1]);
  const wide = plain(longT).length * fs * 0.52 > maxW;
  return lab(ctx, W, H, x, y, wide ? shortT : longT, col, font, al, ba);
}
/* A body drawn at its own radius.  PhET clamps the drawn diameter at 2 px and, when it is
   12 px or less, draws a line pointing at it with its name -- which is the entire content of
   the To Scale screen, so it is reproduced rather than tidied away. */
function bodyDrawGo(ctx, map, bd, col){
  const X = map.X(bd.x), Y = map.Y(bd.y);
  const dTrue = 2 * bd.r * map.s;                 /* the honest diameter, in pixels */
  const rp = Math.max(1, dTrue / 2);
  dot(ctx, X, Y, rp + 2.5, rgba(col, 0.18), null);
  dot(ctx, X, Y, rp, col, '#0b0f1a', rp > 3 ? 1 : 0.6);
  /* the spin, where the body has a rotation period: a radius line, so it can be seen turning */
  if(bd.rot && rp > 4){
    ctx.beginPath(); ctx.moveTo(X, Y);
    ctx.lineTo(X + rp * Math.cos(bd.rot), Y - rp * Math.sin(bd.rot));
    ctx.strokeStyle = '#0b0f1a'; ctx.lineWidth = 1.4; ctx.stroke();
  }
  return {X, Y, rp, dTrue, tiny: dTrue <= 12};
}
/* PhET's pointer for a body too small to see: a 60 px leader at -45 degrees with the name */
function bodyPointer(ctx, W, H, d, name, col){
  const ux = Math.cos(-Math.PI / 4), uy = Math.sin(-Math.PI / 4);
  const X0 = d.X + 10 * ux, Y0 = d.Y - 10 * uy, X1 = d.X + 62 * ux, Y1 = d.Y - 62 * uy;
  ctx.beginPath(); ctx.moveTo(X0, Y0); ctx.lineTo(X1, Y1);
  ctx.strokeStyle = rgba(col, 0.75); ctx.lineWidth = 1.2; ctx.stroke();
  POLY_SEGS.push(X0, Y0, X1, Y1);
  lab(ctx, W, H, X1 + 4, Y1 - 4, name, col, SM_FONT, 'left', 'bottom');
}

/* the bodies, their paths, their vectors and the furniture.  Returns the map so the drags and
   the tests can ask where things landed. */
function drawSystem(ctx, W, H, M, b, show){
  const sys = M.sys, S = sys.S, map = sysMap(b, M), win = winOf(map, b);
  frame(ctx, b, COL.edge);
  lab(ctx, W, H, b.x + 6, b.y + 8, plain(M.sysName) + ' — PhET’s ' + M.screenName
      + ' screen, t = ' + plain(timeStr(sys.t, sys.cfg.minutes)),
      '#aeb6c6', 'italic 13px Georgia, serif', 'left', 'top');
  lab(ctx, W, H, b.x1 - 6, b.y + 8, plain(scaleNoteGo(map)) + ', both axes alike'
      + (show.velocity ? '; v arrows ' + sigf(M.vscale * 1000, 3) + ' px per km/s' : ''),
      COL.dim, SM_FONT, 'right', 'top');
  const marks = [], tinies = [], drawn = [];
  let small = false, capped = false;
  withClip(ctx, b, () => {
    if(show.grid) gridDraw(ctx, map, b, sys.cfg.grid, '#141a27');
    if(show.path) for(const bd of M.bodies){
      const p = sys.paths[bd.i];
      if(p && p.length > 1) worldPathClip(ctx, map, p, rgba(bd.col, 0.55), 1.4, null, win);
    }
    for(const bd of M.bodies){
      if(!inWin([bd.x, bd.y], win)) continue;
      const d = bodyDrawGo(ctx, map, bd, bd.col);
      drawn.push(d);
      if(d.tiny) tinies.push([d, bd]);
      if(show.mass) marks.push({x: d.X, y: d.Y + Math.max(d.rp, 6) + 12, col: bd.col, al: 'center',
                                t: plain(massReadout(S, bd.i, sys.cfg.id))});
    }
    if(show.velocity) for(const bd of M.bodies){
      if(!inWin([bd.x, bd.y], win)) continue;
      const t = velArrow(ctx, map, bd.x, bd.y, bd.vx, bd.vy, M.vscale, COL.pos);
      dot(ctx, t.TX, t.TY, 5, COL.pos, '#fff', 1.2);
      if(Math.hypot(t.TX - t.X, t.TY - t.Y) > 16)
        lab(ctx, W, H, t.TX, t.TY - 9, 'V', '#0b0f1a', 'bold 11px -apple-system, sans-serif', 'center', 'middle');
    }
    if(show.force){
      const maxPx = 0.42 * Math.min(b.w, b.h);
      for(const bd of M.bodies){
        if(!inWin([bd.x, bd.y], win)) continue;
        const f = M.forces[bd.i];
        const a = forceArrow(ctx, map, bd.x, bd.y, f[0], f[1], M.fref, ST.fpow, COL.ref, maxPx);
        if(a && a.small) small = true;
        if(a && a.capped) capped = true;
      }
    }
    if(show.com && inWin([M.com.x, M.com.y], win)){
      const X = map.X(M.com.x), Y = map.Y(M.com.y);
      ctx.strokeStyle = COL.com; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(X - 7, Y - 7); ctx.lineTo(X + 7, Y + 7);
      ctx.moveTo(X - 7, Y + 7); ctx.lineTo(X + 7, Y - 7); ctx.stroke();
      /* The centre of mass of a star and its planet sits INSIDE the star -- 450 km from the
         Sun's centre for the real pair, and on the Model screen the drawn Sun is 50 times too
         big -- so a label at its own height is written across a yellow disc in magenta and
         cannot be read.  Push it clear of whichever body is nearest, along the line between
         them (the same fix my-solar-system needed, for the same reason). */
      let near = null, best = Infinity;
      for(const d of drawn){ const q = Math.hypot(d.X - X, d.Y - Y); if(q < best){ best = q; near = d; } }
      let ux = 0, uy = 1, pad = 18;
      if(near){
        const dx = X - near.X, dy = Y - near.Y, L = Math.hypot(dx, dy);
        pad = near.rp + 13;
        if(L > 0.5){ ux = dx / L; uy = dy / L; }
      }
      marks.push({x: X + ux * pad, y: Y + uy * pad, t: 'centre of mass', col: COL.com,
                  al: ux < -0.2 ? 'right' : (ux > 0.2 ? 'left' : 'center')});
    }
    if(show.tape) tapeDrawKm(ctx, W, H, map, sys.tape, COL.struct);
  });
  /* the pointers and the labels go on AFTER the clip is lifted, so none of them is cut */
  for(const [d, bd] of tinies) bodyPointer(ctx, W, H, d, bd.name, bd.col);
  for(const m of marks) lab(ctx, W, H, m.x, m.y, m.t, m.col, SM_FONT, m.al || 'left', 'middle');
  if(small) lab(ctx, W, H, b.x + 8, b.y1 - 30, 'some gravity arrows are too small to draw — raise the power',
                COL.warn, SM_FONT, 'left', 'bottom');
  if(capped) lab(ctx, W, H, b.x + 8, b.y1 - 30, 'a gravity arrow is longer than the view and is drawn cut (hollow tip) — lower the power',
                 COL.warn, SM_FONT, 'left', 'bottom');
  if(!ST.gravity) lab(ctx, W, H, b.x + 6, b.y1 - 12, 'gravity is OFF: every body drifts in a straight line at constant speed',
                      COL.warn, SM_FONT, 'left', 'bottom');
  let off = 0;
  for(const bd of M.bodies) if(!inWin([bd.x, bd.y], win)) off++;
  if(off) lab(ctx, W, H, b.x + 6, b.y + 26, off + (off === 1 ? ' body is' : ' bodies are')
              + ' outside the view — zoom out, or restart', COL.warn, SM_FONT, 'left', 'top');
  return {map, win, off, tinies: tinies.length};
}
/* the legend both screens carry */
function systemLegend(ctx, b, M){
  const items = [];
  for(const bd of M.bodies) items.push([bd.col, bd.name + (bd.fixed ? ' (fixed)' : '')]);
  if(ST.velocity) items.push([COL.pos, 'velocity (drag the V)']);
  if(ST.force) items.push([COL.ref, 'gravity ×10^' + ST.fpow]);
  if(ST.com) items.push([COL.com, 'centre of mass']);
  legendR(ctx, b, items);
}

/* ================================================================== *
 *  view 1: the model (PhET's Model screen)                            *
 * ================================================================== */
const CAPM_FULL = 'PhET’s Model screen. The physics is the real thing — Newton’s inverse square '
  + 'between every pair, with PhET’s own masses and speeds — but the bodies are drawn far bigger than '
  + 'they are so that there is something to look at, and PhET bends two more things to make the picture work: '
  + 'the star is nailed down, and in Sun-Planet-Moon the moon is moved out to 1.7 drawn planet radii and given '
  + '10,200 times the planet’s pull (one-sidedly) to keep it in orbit. Every factor is printed on the '
  + 'picture. '
  + 'Switch gravity off and everything flies straight; drag a body or the tip of its V arrow and the run '
  + 'starts again from what you built.';
const CAPM_SHORT = 'PhET’s Model screen: real physics, bodies drawn far too big, and two deliberate cheats.';
function exaggerationNote(M){
  const parts = [];
  for(const bd of M.bodies){
    const base = sceneCfg('scale', M.cfg.id).bodies[bd.i].r;
    const f = bd.r / base;
    if(Math.abs(f - 1) > 1e-9) parts.push(bd.name + ' ×' + sigf(f, 4));
  }
  return parts.length ? 'drawn sizes exaggerated: ' + parts.join(', ') : 'every body drawn true';
}
function drawModel(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAPM_FULL, CAPM_SHORT, 0, 0, 0);
  const b = L.main;
  drawSystem(ctx, W, H, M, b, {grid: ST.grid, path: ST.path, velocity: ST.velocity,
    force: ST.force, com: ST.com, tape: ST.tape, mass: ST.massOn});
  /* the notes go on BEFORE the legend: legendR rejects a corner that covers a registered
     label, so a note drawn afterwards is the one that gets dropped instead */
  labFit(ctx, W, H, b.x + 6, b.y + 26, plain(exaggerationNote(M)), 'sizes exaggerated \u2014 see the panel',
         b.w - 12, COL.warn, SM_FONT, 'left', 'top');
  if(M.broken.length)
    labFit(ctx, W, H, b.x + 6, b.y + 42, plain('and PhET bends the physics here: ' + M.broken.join('; ')),
           'PhET bends the physics here \u2014 see the readout', b.w - 12, COL.warn, SM_FONT, 'left', 'top');
  systemLegend(ctx, b, M);
  drawCaption(ctx, L);
}

/* ================================================================== *
 *  view 2: to scale (PhET's To Scale screen)                          *
 * ================================================================== */
const CAPS_FULL = 'PhET’s To Scale screen: the same four systems with every radius true, and nothing '
  + 'nailed down or boosted. This is the honest picture, and the reason the other screen exists — at '
  + 'PhET’s own zoom the Sun is about two and a half pixels across and the Earth is a fortieth of one, so '
  + 'PhET draws anything under twelve pixels with a line pointing at it and its name, and so does this. The '
  + 'panels below put the true sizes and the separations on one logarithmic axis, which is the only way they '
  + 'fit together.';
const CAPS_SHORT = 'Drawn true: at PhET’s zoom the Sun is 2.5 px across and the Earth a fortieth of one.';
function drawScale(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAPS_FULL, CAPS_SHORT, 2, 0.34, 1);
  const b = L.main;
  const S = drawSystem(ctx, W, H, M, b, {grid: ST.grid, path: ST.path, velocity: ST.velocity,
    force: ST.force, com: ST.com, tape: ST.tape, mass: ST.massOn});
  const px = M.bodies.map(bd => bd.name + ' ' + sigf(2 * bd.r * S.map.s, 3) + ' px');
  labFit(ctx, W, H, b.x + 6, b.y + 26, 'true sizes at this zoom: ' + plain(px.join(', ')),
         'true sizes: ' + plain(px[px.length - 1]), b.w - 12, COL.dim, SM_FONT, 'left', 'top');
  systemLegend(ctx, b, M);
  /* panel 1: every length in the system on one log axis */
  const bb = L.bottom[0];
  const rows = M.bodies.map(bd => ({t: bd.name + ' diameter', v: 2 * bd.r, col: bd.col}));
  rows.push({t: 'their separation', v: M.sep, col: COL.ref});
  const lo = Math.floor(Math.log10(Math.min.apply(null, rows.map(r => r.v)))) - 0.4;
  const hi = Math.ceil(Math.log10(Math.max.apply(null, rows.map(r => r.v)))) + 0.4;
  axesT(ctx, bb, lo, hi, 0, rows.length, {title: titleFor(bb, 'the lengths in this system, on a log axis',
    'the lengths'), xlab: 'log₁₀ metres', ny: 1, yticks: [], nx: 5});
  /* The label goes ABOVE its own bar, left-aligned at the frame, never after the bar's end: a
     bar that reaches 90 % of the axis leaves no room to the right, and a label clamped back
     inside the box is then written across the bar it names (found in the first capture). */
  rows.forEach((r, i) => {
    const slot = bb.h / rows.length, top = bb.y + slot * i;
    const X = bb.x + bb.w * (Math.log10(r.v) - lo) / (hi - lo);
    ctx.fillStyle = r.col; ctx.fillRect(bb.x, top + slot - 14, Math.max(1, X - bb.x), 9);
    lab(ctx, W, H, bb.x + 3, top + slot - 20, plain(r.t) + ' — ' + plain(lenStr(r.v, 3)),
        r.col, SM_FONT, 'left', 'bottom');
  });
  /* panel 2: what those lengths come to in pixels, here and on the Model screen */
  if(L.bottom.length > 1){
    const cb = L.bottom[1];
    const mcfg = sceneCfg('model', M.cfg.id);
    const pxs = M.bodies.map(bd => ({t: bd.name, col: bd.col,
      here: 2 * sceneCfg('scale', M.cfg.id).bodies[bd.i].r * S.map.s,
      model: 2 * mcfg.bodies[bd.i].r * S.map.s}));
    const all = pxs.map(p => p.here).concat(pxs.map(p => p.model)).concat([1]);
    const plo = Math.floor(Math.log10(Math.min.apply(null, all))) - 0.3;
    const phi = Math.ceil(Math.log10(Math.max.apply(null, all))) + 0.3;
    axesT(ctx, cb, plo, phi, 0, pxs.length, {title: titleFor(cb,
      'pixels across: true (filled) against PhET’s Model screen (hollow)', 'true vs Model, in pixels'),
      xlab: 'log₁₀ pixels', ny: 1, yticks: [], nx: 5});
    pxs.forEach((p, i) => {
      const slot = cb.h / pxs.length, top = cb.y + slot * i, y0 = top + slot - 12;
      const X = cb.x + cb.w * (Math.log10(p.here) - plo) / (phi - plo);
      const XM = cb.x + cb.w * (Math.log10(p.model) - plo) / (phi - plo);
      ctx.fillStyle = p.col; ctx.fillRect(cb.x, y0 - 4, Math.max(1, X - cb.x), 8);
      ctx.strokeStyle = COL.warn; ctx.lineWidth = 1.4; ctx.strokeRect(cb.x, y0 - 7, Math.max(1, XM - cb.x), 14);
      lab(ctx, W, H, cb.x + 3, y0 - 11, plain(p.t) + ': ' + sigf(p.here, 3) + ' true, ' + sigf(p.model, 3) + ' on Model',
          p.col, SM_FONT, 'left', 'bottom');
    });
    /* the one-pixel line: below it, nothing can be drawn honestly */
    const X1 = cb.x + cb.w * (0 - plo) / (phi - plo);
    if(X1 > cb.x && X1 < cb.x1){
      ctx.beginPath(); ctx.moveTo(X1, cb.y); ctx.lineTo(X1, cb.y1);
      ctx.strokeStyle = COL.dim; ctx.lineWidth = 1; ctx.setLineDash([4, 3]); ctx.stroke(); ctx.setLineDash([]);
      labIn(ctx, W, H, cb, X1 + 4, cb.y + 10, 'one pixel', COL.dim, SM_FONT, 'left', 'top');
    }
  }
  drawCaption(ctx, L);
}
