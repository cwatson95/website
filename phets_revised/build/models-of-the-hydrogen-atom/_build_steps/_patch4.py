#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Layout round 3.

Two general fixes rather than another round of one-off nudges:

1.  A label REGISTRY.  label() records the rectangle it drew and labelIfClear()
    refuses to draw one that would land on top of an existing rectangle.  Every
    optional label (a transition name, a series limit, a level energy, a bar
    value, a z score) goes through it, so crowding drops labels instead of
    stacking them.  The mandatory text — panel titles, axis titles, the caption
    — is registered but never dropped.

2.  stackFit(): a two-panel stack whose bottom panel is GUARANTEED to leave
    AXIS_BOT under itself.  The previous version clamped the height with a
    Math.max floor, which silently pushed the x-axis title past the caption and
    into the #hint corner at 560x380.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(fname, pairs):
    p = os.path.join(HERE, fname)
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, ("%s: %r appears %d times" % (fname, old[:70], s.count(old)))
        s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(s)
    print(fname, "patched")


patch("p4_views.js", [
    ("""function label(ctx, x, y, t, col, font, align, base){
  ctx.fillStyle = col || '#8b93a6';
  ctx.font = font || '11px -apple-system, sans-serif';
  ctx.textAlign = align || 'left'; ctx.textBaseline = base || 'top';
  ctx.fillText(plain(t), x, y);
}""",
     """/* every label this file draws records its rectangle; labelIfClear() then
   refuses to draw one that would land on an existing rectangle, so a crowded
   picture DROPS labels instead of stacking them.  Cleared per draw. */
let LABEL_RECTS = [];
function labelRect(ctx, x, y, t, font, align, base){
  ctx.font = font || '11px -apple-system, sans-serif';
  const w = ctx.measureText(plain(t)).width;
  const mm = /([\\d.]+)px/.exec(ctx.font), fs = mm ? parseFloat(mm[1]) : 10, fh = fs * 1.15;
  const lx = align === 'center' ? x - w / 2 : (align === 'right' ? x - w : x);
  const ly = base === 'top' ? y : (base === 'middle' ? y - fh / 2
    : (base === 'bottom' ? y - fh : y - fh * 0.8));
  return {x: lx, y: ly, w, h: fh};
}
function rectsHit(a, b){
  return Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x) > 2
      && Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) > 2;
}
function label(ctx, x, y, t, col, font, align, base){
  LABEL_RECTS.push(labelRect(ctx, x, y, t, font, align, base));
  ctx.fillStyle = col || '#8b93a6';
  ctx.font = font || '11px -apple-system, sans-serif';
  ctx.textAlign = align || 'left'; ctx.textBaseline = base || 'top';
  ctx.fillText(plain(t), x, y);
}
function labelIfClear(ctx, x, y, t, col, font, align, base){
  const r = labelRect(ctx, x, y, t, font, align, base);
  for(const q of LABEL_RECTS) if(rectsHit(r, q)) return false;
  label(ctx, x, y, t, col, font, align, base);
  return true;
}"""),
    ("""function drawCaption(ctx, L){
  caption(ctx, 18, L.capY, L.txt, L.capW, '#767e92');
}""",
     """function drawCaption(ctx, L){
  const lines = wrapText(ctx, L.txt, L.capW, '11.5px -apple-system, sans-serif');
  LABEL_RECTS.push({x: 18, y: L.capY, w: L.capW, h: lines.length * 14});
  caption(ctx, 18, L.capY, L.txt, L.capW, '#767e92');
}
/* two stacked panels that ALWAYS leave AXIS_BOT under the lower one: the
   square shrinks until the plot below it fits, rather than the plot's height
   being clamped and its x-axis title pushed onto the caption */
function stackFit(top, bot, gap, share){
  let side = Math.max(90, Math.min((bot - top) * (share || 0.46), bot - top));
  let bh = bot - AXIS_BOT - (top + side + gap);
  if(bh < 72){ side = Math.max(70, side - (72 - bh)); bh = bot - AXIS_BOT - (top + side + gap); }
  return {side, bh: Math.max(46, bh)};
}"""),
    ("""function panelTitle(ctx, b, t){
  ctx.textAlign = 'left'; ctx.textBaseline = 'bottom'; ctx.fillStyle = '#aeb6c6';
  ctx.font = 'italic 13px Georgia, serif';
  ctx.fillText(plain(t), b.x, b.y - 9);
}""",
     """function panelTitle(ctx, b, t){
  LABEL_RECTS.push(labelRect(ctx, b.x, b.y - 9, t, 'italic 13px Georgia, serif', 'left', 'bottom'));
  ctx.textAlign = 'left'; ctx.textBaseline = 'bottom'; ctx.fillStyle = '#aeb6c6';
  ctx.font = 'italic 13px Georgia, serif';
  ctx.fillText(plain(t), b.x, b.y - 9);
}"""),
    # level energies and the crowding note now dodge instead of stacking
    ("""    if(trueAxis) label(ctx, x0 - 5, y, fmt(energyEV(n), 2), '#6f7789',
      '9.5px -apple-system, sans-serif', 'right', 'middle');""",
     """    if(trueAxis) labelIfClear(ctx, x0 - 5, y, fmt(energyEV(n), 2), '#6f7789',
      '9.5px -apple-system, sans-serif', 'right', 'middle');"""),
    ("""  if(labelled < NMAX) label(ctx, x0, b.y + 6, (NMAX - labelled) + ' levels too close to label',
    '#6f7789', '10px -apple-system, sans-serif', 'left', 'top');""",
     """  if(labelled < NMAX) labelIfClear(ctx, x0, b.y + 30, (NMAX - labelled) + ' levels too close to label',
    '#6f7789', '10px -apple-system, sans-serif', 'left', 'top');"""),
])

patch("p5_views.js", [
    # --- the narrow stacks -------------------------------------------------
    ("""  if(narrowStage(W)){
    const side2 = Math.max(110, Math.min(uw - 24, (bot - top) * 0.50));
    const a2 = box(30 + (uw - 24 - side2) / 2, top, side2, side2);
    const b2 = box(56, a2.y1 + 44, uw - 78, Math.max(70, bot - a2.y1 - 60 - AXIS_BOT));
    return {L, a: a2, b: b2, side: side2, narrow: true};
  }""",
     """  if(narrowStage(W)){
    const f = stackFit(top, bot, 44, 0.46);
    const side2 = Math.min(f.side, uw - 24);
    const a2 = box(30 + (uw - 24 - side2) / 2, top, side2, side2);
    const b2 = box(56, a2.y1 + 44, uw - 78, f.bh);
    return {L, a: a2, b: b2, side: side2, narrow: true};
  }"""),
    ("""  if(narrowStage(W)){
    const side2 = Math.max(110, Math.min(uw - 24, (bot - top) * 0.50));
    const a2 = box(30 + (uw - 24 - side2) / 2, top, side2, side2);
    const b2 = box(64, a2.y1 + 46, uw - 86, Math.max(70, bot - a2.y1 - 62 - AXIS_BOT));
    return {L, a: a2, b: b2, side: side2, narrow: true};
  }""",
     """  if(narrowStage(W)){
    const f = stackFit(top, bot, 46, 0.46);
    const side2 = Math.min(f.side, uw - 24);
    const a2 = box(30 + (uw - 24 - side2) / 2, top, side2, side2);
    const b2 = box(64, a2.y1 + 46, uw - 86, f.bh);
    return {L, a: a2, b: b2, side: side2, narrow: true};
  }"""),
    # --- series: the bottom panel must leave room for its own axis ---------
    ("""  const hA = Math.max(100, (bot - top) * 0.52);
  const a = box(54, top, uw - 70, hA);""",
     """  const f = stackFit(top, bot, 80, 0.50);
  const hA = f.side;
  const a = box(54, top, uw - 70, hA);"""),
    ("  const b = box(64, a.y1 + 80, uw - 80, Math.max(70, bot - a.y1 - 96 - AXIS_BOT));",
     "  const b = box(64, a.y1 + 80, uw - 80, f.bh);"),
    # --- rates: same, both modes ------------------------------------------
    ("""    const hTop2 = Math.max(70, (bot - top) * 0.40);
    const a2 = box(58, top, uw - 76, hTop2);
    const b2 = box(58, a2.y1 + 80, uw - 76, Math.max(60, bot - a2.y1 - 96 - AXIS_BOT));
    return {L, a: a2, b: b2, c: null, narrow: true};""",
     """    const f2 = stackFit(top, bot, 80, 0.40);
    const a2 = box(58, top, uw - 76, f2.side);
    const b2 = box(58, a2.y1 + 80, uw - 76, f2.bh);
    return {L, a: a2, b: b2, c: null, narrow: true};"""),
    ("""  const hTop = Math.max(100, (bot - top) * 0.46);
  const wHalf = (uw - 100) / 2;""",
     """  const f = stackFit(top, bot, 80, 0.46);
  const hTop = f.side;
  const wHalf = (uw - 100) / 2;"""),
    ("  const b = box(54, a.y1 + 80, uw - 70, Math.max(70, bot - a.y1 - 96 - AXIS_BOT));",
     "  const b = box(54, a.y1 + 80, uw - 70, f.bh);"),
    # --- optional labels dodge --------------------------------------------
    ("""    if(t.n2 <= t.n1 + 2) label(ctx, X, y0 - 2, t.n2 + '→' + t.n1, lamColour(t.lam),
      '9.5px -apple-system, sans-serif', 'center', 'bottom');""",
     """    if(t.n2 <= t.n1 + 2) labelIfClear(ctx, X, y0 - 2, t.n2 + '→' + t.n1, lamColour(t.lam),
      '9.5px -apple-system, sans-serif', 'center', 'bottom');"""),
    ("""    if(X - 5 - tw >= a.x + 2)
      label(ctx, X - 5, rowOf(n1) + 5, txt, COL.ref, '10px -apple-system, sans-serif', 'right', 'top');
    else if(X + 5 + tw <= a.x1 - 2)
      label(ctx, X + 5, rowOf(n1) + 5, txt, COL.ref, '10px -apple-system, sans-serif', 'left', 'top');""",
     """    if(X - 5 - tw >= a.x + 2)
      labelIfClear(ctx, X - 5, rowOf(n1) + 5, txt, COL.ref, '10px -apple-system, sans-serif', 'right', 'top');
    else if(X + 5 + tw <= a.x1 - 2)
      labelIfClear(ctx, X + 5, rowOf(n1) + 5, txt, COL.ref, '10px -apple-system, sans-serif', 'left', 'top');"""),
    ("""    if(t.n <= 3) label(ctx, X + 5, Y - 5, t.n + 'spdfgh'.charAt(t.l), '#8b93a6',
      '9.5px -apple-system, sans-serif', 'left', 'bottom');""",
     """    if(t.n <= 3) labelIfClear(ctx, X + 5, Y - 5, t.n + 'spdfgh'.charAt(t.l), '#8b93a6',
      '9.5px -apple-system, sans-serif', 'left', 'bottom');"""),
    ("""    label(ctx, X, b.y1 - b.h * Math.max(r.f, r.p) - 4, 'z = ' + fmt(r.z, 2),
      Math.abs(r.z) < 3 ? COL.pos : COL.ref, '10px -apple-system, sans-serif', 'center', 'bottom');""",
     """    const zy = b.y1 - b.h * Math.max(r.f, r.p) - 4;
    labelIfClear(ctx, X, zy > b.y + 16 ? zy : b.y1 - b.h * Math.max(r.f, r.p) + 14,
      'z = ' + fmt(r.z, 2), Math.abs(r.z) < 3 ? COL.pos : COL.ref,
      '10px -apple-system, sans-serif', 'center', zy > b.y + 16 ? 'bottom' : 'top');"""),
    # --- the orbital scale note wraps inside its own panel -----------------
    ("""  const scaleTxt = 'the frame is ' + fmt(2 * rmax, 0) + ' a₀ across (' + sigf(2 * rmax * A0 * 1e12, 3)
    + ' pm) — it holds 99 % of the probability';
  label(ctx, a.x + 8, a.y1 - 16, scaleTxt, '#767e92', '10.5px -apple-system, sans-serif', 'left', 'top');""",
     """  /* the note is WRAPPED to the panel: a single label ran 382 px across a
     350 px panel and met the neighbouring plot's tick labels */
  const scaleTxt = 'frame ' + fmt(2 * rmax, 0) + ' a₀ (' + sigf(2 * rmax * A0 * 1e12, 3)
    + ' pm) wide — 99 % of |ψ|² is inside it';
  const sLines = wrapText(ctx, scaleTxt, a.w - 16, '10.5px -apple-system, sans-serif');
  LABEL_RECTS.push({x: a.x + 8, y: a.y1 - 8 - sLines.length * 13, w: a.w - 16, h: sLines.length * 13});
  ctx.fillStyle = '#8d95a8'; ctx.textAlign = 'left'; ctx.textBaseline = 'top';
  ctx.font = '10.5px -apple-system, sans-serif';
  for(let i = 0; i < sLines.length; i++)
    ctx.fillText(sLines[i], a.x + 8, a.y1 - 8 - sLines.length * 13 + i * 13);"""),
    # --- clear the registry each draw --------------------------------------
    ("  POLY_SEGS = []; LEGEND_RECTS = [];",
     "  POLY_SEGS = []; LEGEND_RECTS = []; LABEL_RECTS = [];"),
])

patch("p4_views.js", [
    ("""    label(ctx, X, a.y1 - hgt - 12, lam + ' nm', lamColour(lam),
        '10px -apple-system, sans-serif', 'center', 'top');""",
     """    labelIfClear(ctx, X, a.y1 - hgt - 12, lam + ' nm', lamColour(lam),
        '10px -apple-system, sans-serif', 'center', 'top');"""),
])
