
/* ================================================================== *
 *  the stage both PhET screens share, and views 1-2                   *
 * ================================================================== */
function sysMap(b, R){ return worldFitUp(b, {xmin: -R, xmax: R, ymin: -R, ymax: R}, 0); }
function winOf(map, b){ return {x0: map.wx(b.x), x1: map.wx(b.x1), y0: map.wy(b.y1), y1: map.wy(b.y)}; }
function inWin(p, w){ return p[0] >= w.x0 && p[0] <= w.x1 && p[1] >= w.y0 && p[1] <= w.y1; }

/* the bodies, their paths, their vectors, and the furniture.  Returns the map so the drags
   and the tests can ask where things landed. */
function drawSystem(ctx, W, H, M, b, show){
  const st = M.st, sys = M.sys, map = sysMap(b, M.R), win = winOf(map, b);
  frame(ctx, b, COL.edge);
  /* the title and the scale claim their place first: drawn last, the label registry pushes them
     out of the box when something else has taken that corner */
  lab(ctx, W, H, b.x + 6, b.y + 8, (M.key === 'lab' ? plain(M.preset.name) : 'a star and a planet')
      + ' — ' + sys.S.n + (sys.S.n === 1 ? ' body' : ' bodies') + ', t = ' + plain(yrStr(sys.t)),
      '#aeb6c6', 'italic 13px Georgia, serif', 'left', 'top');
  lab(ctx, W, H, b.x1 - 6, b.y + 8, plain(scaleNote(map)) + ' — true shape, both axes alike'
      + (show.velocity ? '; v arrows ' + fmt(VSCALE, 1) + ' px per km/s' : ''), COL.dim, SM_FONT, 'right', 'top');
  /* everything in world coordinates is CLIPPED to the stage: a body sitting one pixel inside
     the window still draws a disc and a velocity arrow that reach past the frame, and the
     capture of "hyperbolic" had both of them out on the page background.  Labels that ride on
     a body are collected here and written once the clip is lifted, so none of them is cut. */
  const marks = [], drawn = [];
  let small = false, capped = false;
  withClip(ctx, b, () => {
    if(show.grid) gridDraw(ctx, map, b, 1, '#141a27');
    /* the paths, oldest first, in each body's own colour */
    if(show.path) for(const bd of M.bodies){
      const p = sys.paths[bd.i];
      if(p && p.length > 1) worldPathClip(ctx, map, p, rgba(bd.col, 0.5), 1.4, null, win);
    }
    /* where a merge happened */
    for(const mg of sys.merged){
      if(!inWin([mg.x, mg.y], win)) continue;
      const X = map.X(mg.x), Y = map.Y(mg.y);
      ctx.strokeStyle = COL.warn; ctx.lineWidth = 1.4;
      ctx.beginPath(); ctx.moveTo(X - 6, Y - 6); ctx.lineTo(X + 6, Y + 6);
      ctx.moveTo(X - 6, Y + 6); ctx.lineTo(X + 6, Y - 6); ctx.stroke();
    }
    /* the bodies */
    for(const bd of M.bodies){
      if(!inWin([bd.x, bd.y], win)) continue;
      const d = bodyDraw(ctx, map, bd.x, bd.y, bd.r, bd.col, 3);
      drawn.push(d);
      if(show.speedLab) marks.push({x: d.X + d.rp + 6, y: d.Y + 10, col: bd.col,
                                    t: '|v| = ' + fmt(Math.hypot(bd.vx, bd.vy), 2) + ' km/s'});
    }
    /* the velocity arrows, with the handle each one is dragged by */
    if(show.velocity) for(const bd of M.bodies){
      if(!inWin([bd.x, bd.y], win)) continue;
      const t = velArrow(ctx, map, bd.x, bd.y, bd.vx, bd.vy, VSCALE, COL.pos);
      dot(ctx, t.TX, t.TY, 4.5, COL.pos, '#fff', 1.2);
    }
    /* the gravity arrows: the net pull on each body, at a scale the canvas states */
    if(show.gravity){
      const maxPx = 0.42 * Math.min(b.w, b.h);
      for(const bd of M.bodies){
        if(!inWin([bd.x, bd.y], win)) continue;
        const f = M.forces[bd.i];
        const a = forceArrow(ctx, map, bd.x, bd.y, f[0], f[1], F_REF, st.fpow, COL.ref, maxPx);
        if(a && a.small) small = true;
        if(a && a.capped) capped = true;
      }
    }
    /* the centre of mass (PhET's red cross) */
    if(show.com && inWin([M.com.x, M.com.y], win)){
      const X = map.X(M.com.x), Y = map.Y(M.com.y);
      ctx.strokeStyle = COL.com; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(X - 7, Y - 7); ctx.lineTo(X + 7, Y + 7);
      ctx.moveTo(X - 7, Y + 7); ctx.lineTo(X + 7, Y - 7); ctx.stroke();
      /* pushed clear of whichever body is nearest, along the line between them: the centre of
         mass of a star and its planet sits INSIDE the star, and a label at its own height is
         written across it -- it was, in three captures */
      let near = null, best = Infinity;
      for(const d of drawn){ const q = Math.hypot(d.X - X, d.Y - Y); if(q < best){ best = q; near = d; } }
      let ux = 0, uy = 1, pad = 18;
      if(near){
        const dx = X - near.X, dy = Y - near.Y, L = Math.hypot(dx, dy);
        pad = near.rp + 13;
        if(L > 0.5){ ux = dx / L; uy = dy / L; }
      }
      marks.push({x: X + ux * pad, y: Y + uy * pad, t: 'centre of mass', col: COL.com,
                  al: ux < -0.2 ? 'right' : (ux > 0.2 ? 'left' : 'center'),
                  ba: uy < -0.2 ? 'bottom' : (uy > 0.2 ? 'top' : 'middle')});
    }
    if(show.tape) tapeDraw(ctx, W, H, map, SIM.tape, COL.struct);
  });
  for(const m of marks) lab(ctx, W, H, m.x, m.y, m.t, m.col, SM_FONT, m.al || 'left', m.ba || 'alphabetic');
  if(small) lab(ctx, W, H, b.x + 8, b.y1 - 28, 'some gravity arrows are too small to draw — raise the power',
                COL.warn, SM_FONT, 'left', 'bottom');
  if(capped) lab(ctx, W, H, b.x + 8, b.y1 - 28, 'a gravity arrow is longer than the view and is drawn cut (hollow tip) — lower the power',
                 COL.warn, SM_FONT, 'left', 'bottom');
  /* anything that has left the view */
  let off = 0;
  for(const bd of M.bodies) if(!inWin([bd.x, bd.y], win)) off++;
  if(off) lab(ctx, W, H, b.x + 6, b.y + 26, off + (off === 1 ? ' body is' : ' bodies are') + ' outside the view — zoom out, or return them',
              COL.warn, SM_FONT, 'left', 'top');
  return {map, win, off};
}

/* ================================================================== *
 *  view 1: two bodies (PhET's Intro screen)                           *
 * ================================================================== */
const CAPI_FULL = 'PhET’s Intro screen: a star and a planet, and nothing but Newton’s law between them. Drag either '
  + 'body, or the tip of its green velocity arrow, and set the masses on the right — the clock stops while you do, as '
  + 'PhET’s does, and the run starts again from what you built. Two bodies are the one case with a closed-form answer, '
  + 'so the third view draws this same orbit exactly and measures how far the integration has drifted from it.';
const CAPI_SHORT = 'A star and a planet: drag them, drag their velocity arrows, set their masses, and let them go.';
function drawIntro(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAPI_FULL, CAPI_SHORT, 0, 0, 0);
  const st = M.st;
  const S = drawSystem(ctx, W, H, M, L.main, {grid: st.grid, path: st.path, velocity: st.velocity,
    speedLab: st.speedLab, gravity: st.gravity, com: st.com, tape: st.tape});
  const items = [];
  for(const bd of M.bodies) items.push([bd.col, 'body ' + (bd.i + 1) + ', ' + plain(massStr(bd.m)) + ' × 10²⁸ kg']);
  if(st.velocity) items.push([COL.pos, 'v (drag the tip)']);
  if(st.gravity) items.push([COL.ref, 'gravity ×10^' + st.fpow]);
  if(st.com) items.push([COL.com, 'centre of mass']);
  legendR(ctx, L.main, items);
  drawCaption(ctx, L);
}

/* ================================================================== *
 *  view 2: the lab (PhET's Lab screen)                                *
 * ================================================================== */
const CAPL_FULL = 'PhET’s Lab screen: one to four bodies, and its eleven orbital systems. Every system is loaded with '
  + 'the centre of mass brought to rest, as PhET loads them. Touching anything makes the system “custom” and saves '
  + 'the new start, which is where restart returns to. Bodies that touch merge — here keeping mass, momentum and the '
  + 'centre of mass, where PhET keeps the heavier body’s mass and hands it the lighter one’s momentum.';
const CAPL_SHORT = 'One to four bodies and PhET’s eleven orbital systems; anything you touch becomes a custom system.';
function drawLab(ctx, W, H, M){
  const L = stageLayoutH(ctx, W, H, CAPL_FULL, CAPL_SHORT, 0, 0, 0);
  const st = M.st;
  drawSystem(ctx, W, H, M, L.main, {grid: st.grid, path: st.path, velocity: st.velocity,
    speedLab: st.speedLab, gravity: st.gravity, com: st.com, tape: st.tape});
  const items = [];
  for(const bd of M.bodies) items.push([bd.col, 'body ' + (bd.i + 1) + ', ' + plain(massStr(bd.m))]);
  if(st.com) items.push([COL.com, 'centre of mass']);
  if(M.merged.length) items.push([COL.warn, 'a collision']);
  legendR(ctx, L.main, items);
  /* the warning PhET's own presets earn: three bodies and more are chaotic.  It goes under
     the title, not at the foot of the stage: down there the label registry shifts it out
     of the box and into the caption (the audit caught that in nine captures). */
  if(M.chaotic) lab(ctx, W, H, L.main.x + 6, L.main.y + 26,
    'three bodies and more are chaotic: this is one possible history, not the history',
    COL.dim, SM_FONT, 'left', 'top');
  drawCaption(ctx, L);
}
