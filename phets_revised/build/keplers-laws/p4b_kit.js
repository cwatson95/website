
/* ================================================================== *
 *  the shared view kit for this family: the hint-safe layout, axes    *
 *  that register what they draw, and the pieces both sims paint (the  *
 *  grid, the bodies, the velocity and gravity arrows, the measuring   *
 *  tape, the trail, the stopwatch).  my-solar-system reads this file  *
 *  from ../keplers-laws/, so the two sims draw the same furniture.    *
 * ================================================================== */
/* The house #hint sits at bottom:11px in 11px type, ON TOP of the last line of a caption
   anchored at H - 12, and the canvas capture cannot see it because the hint is HTML
   (wave-on-a-string's finding).  Every layout here is built for H - HINT_H, and the layout
   sweep asserts no canvas text reaches the hint's corner. */
const HINT_H = 18;
function stageLayoutH(ctx, W, H, capFull, capShort, nBottom, bottomFrac, nBottomNarrow){
  return stageLayout(ctx, W, H - HINT_H, capFull, capShort, nBottom, bottomFrac, nBottomNarrow);
}
/* tick labels follow the tick SPACING, not a fixed decimal count (Known-bad: fmt(t,2) prints
   "318.00" whatever the range and six of those do not fit a narrow panel) */
function tickFmt(ticks){
  let g = Infinity;
  for(let i = 1; i < ticks.length; i++) g = Math.min(g, Math.abs(ticks[i] - ticks[i - 1]));
  if(!isFinite(g) || g <= 0) return v => sigf(v, 3);
  let d = 0;
  while(d < 6 && Math.abs(Math.round(g * Math.pow(10, d)) - g * Math.pow(10, d)) > 1e-6 * Math.max(1, g * Math.pow(10, d))) d++;
  return v => fmt(Math.abs(v) < 1e-12 ? 0 : v, d);
}
/* axes() registers nothing, so a label placed later can land on a tick number (the
   standard_model trap).  axesT registers every tick label and both axis titles. */
function axesT(ctx, b, xlo, xhi, ylo, yhi, opt){
  const o = Object.assign({}, opt || {});
  if(o.xticks === undefined) o.xticks = ticksFor(Math.min(xlo, xhi), Math.max(xlo, xhi), o.nx || 6);
  if(o.yticks === undefined) o.yticks = ticksFor(Math.min(ylo, yhi), Math.max(ylo, yhi), o.ny || 5);
  if(!o.xfmt) o.xfmt = tickFmt(o.xticks);
  if(!o.yfmt) o.yfmt = tickFmt(o.yticks);
  axesR(ctx, b, xlo, xhi, ylo, yhi, o);
  const fs = 10.5;
  for(const t of o.xticks){
    const X = b.x + b.w * (t - xlo) / (xhi - xlo || 1);
    if(X < b.x - 0.5 || X > b.x1 + 0.5) continue;
    const w = plain(o.xfmt(t)).length * fs * 0.52;
    LABELS.push([X - w / 2, b.y1 + 5, X + w / 2, b.y1 + 5 + fs * 1.15]);
  }
  for(const t of o.yticks){
    const Y = b.y1 - b.h * (t - ylo) / (yhi - ylo || 1);
    if(Y < b.y - 0.5 || Y > b.y1 + 0.5) continue;
    const w = plain(o.yfmt(t)).length * fs * 0.52;
    LABELS.push([b.x - 6 - w, Y - fs * 0.6, b.x - 6, Y + fs * 0.6]);
  }
  if(o.xlab){ const w = plain(o.xlab).length * 11 * 0.52;
    LABELS.push([b.x + b.w / 2 - w / 2, b.y1 + 21, b.x + b.w / 2 + w / 2, b.y1 + 21 + 13]); }
  if(o.ylab) LABELS.push([b.x - 47, b.y, b.x - 33, b.y1]);
}
/* a label that is kept inside a box as well as on the canvas */
function labIn(ctx, W, H, b, x, y, txt, col, font, align, base){
  const fs = parseFloat((font || LAB_FONT).match(/([\d.]+)px/)[1]);
  const w = plain(txt).length * fs * 0.52;
  let X = clamp(x, b.x + (align === 'right' ? w + 3 : align === 'center' ? w / 2 + 3 : 3),
                b.x1 - (align === 'right' ? 3 : align === 'center' ? w / 2 + 3 : w + 3));
  const Y = clamp(y, b.y + fs, b.y1 - fs * 0.6);
  return lab(ctx, W, H, X, Y, txt, col, font, align, base);
}

/* ---- the furniture ----------------------------------------------------------------------- */
/* a grid of `step` world units, clipped to the box, with the axes through the origin bolder */
function gridDraw(ctx, map, b, step, col){
  const x0 = map.wx(b.x), x1 = map.wx(b.x1), y0 = map.wy(b.y1), y1 = map.wy(b.y);
  const i0 = Math.ceil(x0 / step), i1 = Math.floor(x1 / step);
  const j0 = Math.ceil(y0 / step), j1 = Math.floor(y1 / step);
  if(i1 - i0 > 400 || j1 - j0 > 400) return 0;       /* far out, a grid is a grey wash */
  let n = 0;
  ctx.beginPath();
  for(let i = i0; i <= i1; i++){ const X = map.X(i * step); ctx.moveTo(X, b.y); ctx.lineTo(X, b.y1); n++; }
  for(let j = j0; j <= j1; j++){ const Y = map.Y(j * step); ctx.moveTo(b.x, Y); ctx.lineTo(b.x1, Y); n++; }
  ctx.strokeStyle = col || '#161b28'; ctx.lineWidth = 1; ctx.stroke();
  ctx.beginPath();
  if(0 >= x0 && 0 <= x1){ const X = map.X(0); ctx.moveTo(X, b.y); ctx.lineTo(X, b.y1); }
  if(0 >= y0 && 0 <= y1){ const Y = map.Y(0); ctx.moveTo(b.x, Y); ctx.lineTo(b.x1, Y); }
  ctx.strokeStyle = '#222a3c'; ctx.lineWidth = 1.2; ctx.stroke();
  return n;
}
/* a body: drawn to scale when that is more than minPx, else at minPx, with a halo */
function bodyDraw(ctx, map, x, y, rWorld, col, minPx){
  const X = map.X(x), Y = map.Y(y), rp = Math.max(minPx || 3.5, rWorld * map.s);
  dot(ctx, X, Y, rp + 2.5, rgba(col, 0.18), null);
  dot(ctx, X, Y, rp, col, '#0b0f1a', 1);
  return {X, Y, rp};
}
/* the velocity arrow: px per km/s is fixed and printed on the canvas, so the arrow is a
   measurement rather than a decoration */
function velArrow(ctx, map, x, y, vxk, vyk, scale, col){
  const X = map.X(x), Y = map.Y(y), TX = X + vxk * scale, TY = Y - vyk * scale;
  arrowPx(ctx, X, Y, TX, TY, col, 2);
  return {X, Y, TX, TY};
}
/* the gravity arrow: 60 px at the reference pull, times 10^pow, and CAPPED to the box.  An
   inverse-square force grows without bound as two bodies close, so an uncapped arrow leaves
   the stage entirely (seen in the first capture of my-solar-system, 418 px of arrow off both
   ends of the view).  A capped arrow is drawn hollow-tipped and reported, never silently. */
function forceArrow(ctx, map, x, y, fx, fy, fref, pow, col, maxPx){
  const X = map.X(x), Y = map.Y(y), f = Math.hypot(fx, fy);
  if(!(f > 0)) return null;
  const want = FSCALE * Math.pow(10, pow) * f / fref;
  if(want < 2) return {small: true, X, Y};
  const cap = maxPx || 1e9, L = Math.min(want, cap), capped = want > cap;
  const TX = X + L * fx / f, TY = Y - L * fy / f;
  arrowPx(ctx, X, Y, TX, TY, col, 2);
  if(capped) dot(ctx, TX, TY, 4, null, col, 1.4);
  return {X, Y, TX, TY, L, want, capped};
}
/* the measuring tape: two ends and the distance between them */
function tapeDraw(ctx, W, H, map, tape, col){
  const AX = map.X(tape.ax), AY = map.Y(tape.ay), BX = map.X(tape.bx), BY = map.Y(tape.by);
  ctx.beginPath(); ctx.moveTo(AX, AY); ctx.lineTo(BX, BY);
  ctx.strokeStyle = col; ctx.lineWidth = 1.6; ctx.setLineDash([6, 4]); ctx.stroke(); ctx.setLineDash([]);
  POLY_SEGS.push(AX, AY, BX, BY);
  ctx.beginPath(); ctx.rect(AX - 5, AY - 5, 10, 10); ctx.fillStyle = col; ctx.fill();
  dot(ctx, BX, BY, 5, null, col, 2);
  const d = Math.hypot(tape.bx - tape.ax, tape.by - tape.ay);
  lab(ctx, W, H, (AX + BX) / 2, (AY + BY) / 2 - 10, sigf(d, 4) + ' AU', col, LAB_FONT, 'center', 'bottom');
  return d;
}
function tapeHit(map, tape, px, py, tol){
  const t = tol || 12;
  if(Math.hypot(map.X(tape.bx) - px, map.Y(tape.by) - py) <= t) return 'tapeB';
  if(Math.hypot(map.X(tape.ax) - px, map.Y(tape.ay) - py) <= t) return 'tapeA';
  return null;
}
/* a world polyline, every segment CLIPPED IN WORLD SPACE (Liang-Barsky) to the window: the
   siblings' worldPath drops a segment whose two ends are both outside even when it crosses
   the box, which cuts a big orbit short at the frame (Known-bad, pupil_plane). */
function worldPathClip(ctx, map, pts, col, lw, dash, win){
  ctx.beginPath();
  let n = 0, prevIn = false, px = 0, py = 0;
  for(let i = 0; i + 1 < pts.length; i++){
    const c = win ? clipToWin(pts[i], pts[i + 1], win) : [pts[i], pts[i + 1]];
    if(!c){ prevIn = false; continue; }
    const X0 = map.X(c[0][0]), Y0 = map.Y(c[0][1]), X1 = map.X(c[1][0]), Y1 = map.Y(c[1][1]);
    if(!prevIn || Math.abs(X0 - px) > 0.01 || Math.abs(Y0 - py) > 0.01) ctx.moveTo(X0, Y0);
    ctx.lineTo(X1, Y1);
    POLY_SEGS.push(X0, Y0, X1, Y1);
    px = X1; py = Y1; prevIn = true; n++;
  }
  ctx.strokeStyle = col; ctx.lineWidth = lw || 1.5; ctx.lineJoin = 'round';
  if(dash) ctx.setLineDash(dash);
  ctx.stroke(); ctx.setLineDash([]);
  return n;
}
/* a clip to a box for FILLS (a polyline is clipped in data space instead; the display-list
   recorder does record this rectangle, so the rasterised PNG shows what a browser shows) */
function withClip(ctx, b, fn){
  ctx.save(); ctx.beginPath(); ctx.rect(b.x, b.y, b.w, b.h); ctx.clip();
  try{ fn(); } finally{ ctx.restore(); }
}
/* a trail of world points, clipped to the window */
function trailDraw(ctx, map, pts, col, win, lw){
  return worldPath(ctx, map, pts, col, lw || 1.3, null, win);
}
/* the stopwatch, drawn as a chip inside a box and registered so nothing lands on it */
function swChip(ctx, W, H, b, txt, running){
  const w = 116, hh = 30, x = b.x + 10, y = b.y1 - hh - 10;
  ctx.fillStyle = 'rgba(10,12,18,.82)'; ctx.fillRect(x, y, w, hh);
  frame(ctx, box(x, y, w, hh), running ? COL.pos : COL.edge);
  LABELS.push([x, y, x + w, y + hh]);
  ctx.fillStyle = running ? COL.pos : '#9aa2b4';
  ctx.font = '12.5px "SF Mono", Menlo, monospace'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
  ctx.fillText(plain(txt), x + 9, y + hh / 2);
  return box(x, y, w, hh);
}
/* "1 AU = 84 px": every scale distortion (and every scale) is printed on the canvas */
function scaleNote(map){ return '1 AU = ' + fmt(map.s, 1) + ' px'; }
