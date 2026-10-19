#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-off patch: narrow-stage layouts for the wave, orbitals and rates views,
and the series axis label fixes.  Kept as a file (the shell guard refuses long
python heredocs) and run as `python3 _patch1.py`."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "p5_views.js")
s = io.open(p, encoding="utf-8").read()


def sub(old, new):
    global s
    assert s.count(old) == 1, ("pattern %r appears %d times" % (old[:60], s.count(old)))
    s = s.replace(old, new)


sub("""  const uw = usableW(W);
  const top = L.top + 24, bot = L.bot - 16;
  const side = Math.max(140, Math.min(bot - top, uw * 0.52));
  const a = box(30, top + (bot - top - side) / 2, side, side);
  const b = box(a.x1 + 56, top + 10, Math.max(150, uw - side - 80), Math.max(110, bot - top - 30));
  return {L, a, b, side};
}
function waveCaption(M){""",
    """  const uw = usableW(W);
  const top = L.top + 24, bot = L.bot - 16;
  if(narrowStage(W)){
    const side2 = Math.max(110, Math.min(uw - 24, (bot - top) * 0.50));
    const a2 = box(30 + (uw - 24 - side2) / 2, top, side2, side2);
    const b2 = box(56, a2.y1 + 44, uw - 78, Math.max(80, bot - a2.y1 - 60));
    return {L, a: a2, b: b2, side: side2, narrow: true};
  }
  const side = Math.max(140, Math.min(bot - top, uw * 0.52));
  const a = box(30, top + (bot - top - side) / 2, side, side);
  const b = box(a.x1 + 56, top + 10, Math.max(150, uw - side - 80), Math.max(110, bot - top - 30));
  return {L, a, b, side};
}
function waveCaption(M){""")

sub("""  const uw = usableW(W);
  const top = L.top + 24, bot = L.bot - 16;
  const side = Math.max(140, Math.min(bot - top, uw * 0.50));
  const a = box(30, top + (bot - top - side) / 2, side, side);
  const b = box(a.x1 + 60, top + 14, Math.max(160, uw - side - 86), Math.max(110, bot - top - 40));
  return {L, a, b, side};
}""",
    """  const uw = usableW(W);
  const top = L.top + 24, bot = L.bot - 16;
  if(narrowStage(W)){
    const side2 = Math.max(110, Math.min(uw - 24, (bot - top) * 0.50));
    const a2 = box(30 + (uw - 24 - side2) / 2, top, side2, side2);
    const b2 = box(64, a2.y1 + 46, uw - 86, Math.max(80, bot - a2.y1 - 62));
    return {L, a: a2, b: b2, side: side2, narrow: true};
  }
  const side = Math.max(140, Math.min(bot - top, uw * 0.50));
  const a = box(30, top + (bot - top - side) / 2, side, side);
  const b = box(a.x1 + 60, top + 14, Math.max(160, uw - side - 86), Math.max(110, bot - top - 40));
  return {L, a, b, side};
}""")

sub("""  const uw = usableW(W);
  const top = L.top + 26, bot = L.bot - 16;
  const hA = Math.max(110, (bot - top) * 0.54);
  const a = box(54, top, uw - 70, hA);
  const b = box(54, a.y1 + 58, uw - 70, Math.max(90, bot - a.y1 - 74));
  return {L, a, b};""",
    """  const uw = usableW(W);
  const top = L.top + 26, bot = L.bot - 16;
  const hA = Math.max(100, (bot - top) * 0.52);
  const a = box(54, top, uw - 70, hA);
  /* 80 px between the panels, not 58: panel a's x-axis title sits 33 px below
     its frame and panel b's own title 24 px above its own, and at 58 they
     overlapped by 3.6 px at every stage size */
  const b = box(64, a.y1 + 80, uw - 80, Math.max(80, bot - a.y1 - 96));
  return {L, a, b};""")

sub("""  axes(ctx, b, lo, hi, 0, yhi, {title: 'this model minus NIST, relative',
    xlab: 'wavelength (nm, log scale)', ylab: '(model − NIST)/NIST', nx: 6, ny: 5,
    xfmt: t => fmt(Math.pow(10, t), 0), yfmt: t => (t * 1e5).toFixed(1) + '×10⁻⁵'});""",
    """  /* the units go in the axis TITLE, not on every tick: '0.5x10^-5' is 49 px
     wide and ran into the rotated y-axis label at every stage size */
  axes(ctx, b, lo, hi, 0, yhi, {title: 'this model minus NIST, in parts per 100 000',
    xlab: 'wavelength (nm, log scale)', ylab: '(model − NIST)/NIST, ×10⁻⁵',
    nx: 6, ny: 5, xfmt: t => fmt(Math.pow(10, t), 0), yfmt: t => (t * 1e5).toFixed(1)});""")

sub("""  for(let e = 2; e <= 4; e++) for(const mnt of [1, 2, 3, 5, 7]){
    const v = mnt * Math.pow(10, e);
    if(v < 80 || v > 15000) continue;
    const X = a.x + a.w * (Math.log10(v) - lo) / (hi - lo);
    ctx.strokeStyle = 'rgba(30,38,54,1)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(X, a.y); ctx.lineTo(X, a.y1); ctx.stroke();
    label(ctx, X, a.y1 + 5, v >= 1000 ? fmt(v / 1000, 1) + ' µm' : fmt(v, 0), '#6f7789',
      '10px -apple-system, sans-serif', 'center', 'top');
  }""",
    """  /* thin the decade labels by MEASURED width: at 560 px '5.0 um' and '7.0 um'
     are 14 px apart and overlap (Known-bad: tick label width follows the tick
     spacing, not a fixed decimal count) */
  let lastLabX = -1e9;
  for(let e = 2; e <= 4; e++) for(const mnt of [1, 2, 3, 5, 7]){
    const v = mnt * Math.pow(10, e);
    if(v < 80 || v > 15000) continue;
    const X = a.x + a.w * (Math.log10(v) - lo) / (hi - lo);
    ctx.strokeStyle = 'rgba(30,38,54,1)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(X, a.y); ctx.lineTo(X, a.y1); ctx.stroke();
    const txt = v >= 1000 ? fmt(v / 1000, 1) + ' µm' : fmt(v, 0);
    ctx.font = '10px -apple-system, sans-serif';
    const need = ctx.measureText(plain(txt)).width / 2 + 6;
    if(X - need < lastLabX) continue;
    label(ctx, X, a.y1 + 5, txt, '#6f7789', '10px -apple-system, sans-serif', 'center', 'top');
    lastLabX = X + need;
  }""")

sub("""  const uw = usableW(W);
  const top = L.top + 26, bot = L.bot - 16;
  const hTop = Math.max(100, (bot - top) * 0.46);
  const wHalf = (uw - 100) / 2;
  const a = box(54, top, wHalf, hTop);
  const c = box(54 + wHalf + 46, top, wHalf, hTop);
  const b = box(54, a.y1 + 54, uw - 70, Math.max(90, bot - a.y1 - 70));
  return {L, a, b, c};""",
    """  const uw = usableW(W);
  const top = L.top + 26, bot = L.bot - 16;
  if(narrowStage(W)){
    /* no room for two columns: the branching bars on top, the ensemble below,
       and the lifetime scatter is dropped (the caption says so) */
    const hTop2 = Math.max(70, (bot - top) * 0.40);
    const a2 = box(58, top, uw - 76, hTop2);
    const b2 = box(58, a2.y1 + 80, uw - 76, Math.max(70, bot - a2.y1 - 96));
    return {L, a: a2, b: b2, c: null, narrow: true};
  }
  const hTop = Math.max(100, (bot - top) * 0.46);
  const wHalf = (uw - 100) / 2;
  const a = box(54, top, wHalf, hTop);
  const c = box(54 + wHalf + 46, top, wHalf, hTop);
  /* 80 px between the rows: a's x-axis title and b's panel title overlapped by
     3.6 px at 54 */
  const b = box(54, a.y1 + 80, uw - 70, Math.max(80, bot - a.y1 - 96));
  return {L, a, b, c};""")

sub("""  /* --- lifetimes --- */
  const taus = [];""",
    """  /* --- lifetimes (dropped on a narrow stage) --- */
  if(!c){ drawRatesEnsemble(ctx, M, b, cats, nF); drawCaption(ctx, G.L); return; }
  const taus = [];""")

sub("""  /* --- the seeded ensemble --- */
  const rows = M.ens.rows;""",
    """  drawRatesEnsemble(ctx, M, b, cats, nF);
  drawCaption(ctx, G.L);
}
function drawRatesEnsemble(ctx, M, b, cats, nF){
  const st = M.st;
  const rows = M.ens.rows;""")

sub("""  legendAuto(ctx, b, [[COL.live, 'measured'], [COL.ref, 'exact, ±2σ']]);
  drawCaption(ctx, G.L);
}""",
    """  legendAuto(ctx, b, [[COL.live, 'measured'], [COL.ref, 'exact, ±2σ']]);
}""")

io.open(p, "w", encoding="utf-8").write(s)
print("p5_views.js patched")
