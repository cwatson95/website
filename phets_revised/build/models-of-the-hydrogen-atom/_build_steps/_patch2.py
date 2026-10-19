#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Layout round 2: reserve the axis-label band under every bottom plot box, move
the labels that collided, and floor 'draws substance' on the total op count
rather than on fills alone."""
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


# ---------------------------------------------------------------- p4_views
patch("p4_views.js", [
    # a plot box needs 38 px under it for its own tick labels and axis title;
    # without that reserve the x-axis title of a bottom panel lands on the
    # caption and inside the #hint corner
    ("function narrowStage(W){ return usableW(W) < 430; }",
     "function narrowStage(W){ return usableW(W) < 430; }\n"
     "/* axes() puts tick labels at +5 and the x-axis title at +21 below the\n"
     "   frame, in 11 px type: 38 px of clearance under every plot box. */\n"
     "const AXIS_BOT = 38;"),
    # the gun label went UNDER the gun and met the spectrometer title 3 px
    # later; it goes beside the gun instead
    ("""  label(ctx, G.cx, gy + gh + 4, st.lightOn
    ? (st.light === 'white' ? 'white light' : fmt(st.lam, 0) + ' nm, ' + bandOf(st.lam))
    : 'light source off', '#8b93a6', '11px -apple-system, sans-serif', 'center', 'top');""",
     """  label(ctx, G.cx + gw / 2 + 9, gy + gh / 2, st.lightOn
    ? (st.light === 'white' ? 'white light' : fmt(st.lam, 0) + ' nm, ' + bandOf(st.lam))
    : 'light source off', '#8b93a6', '11px -apple-system, sans-serif', 'left', 'middle');"""),
    # the true ladder really does crowd n = 4, 5, 6 into the top 3 % of the
    # axis; label what fits and say what could not be labelled, rather than
    # stacking three labels on top of each other
    ("""    label(ctx, x1 + 1, y, 'n=' + n, n === M.n ? COL.pos : '#6f7789',
      '10.5px -apple-system, sans-serif', 'right', 'middle');""",
     """    if(Math.abs(y - lastLabY) >= 12 || n === M.n){
      label(ctx, x1 + 1, y, 'n=' + n, n === M.n ? COL.pos : '#6f7789',
        '10.5px -apple-system, sans-serif', 'right', 'middle');
      lastLabY = y; labelled++;
    }"""),
    ("""  const x0 = b.x + 36, x1 = b.x1 - 14;""",
     """  const x0 = b.x + 36, x1 = b.x1 - 14;
  let lastLabY = -1e9, labelled = 0;"""),
    ("""  /* the ionisation line */""",
     """  if(labelled < NMAX) label(ctx, x0, b.y + 6, (NMAX - labelled) + ' levels too close to label',
    '#6f7789', '10px -apple-system, sans-serif', 'left', 'top');
  /* the ionisation line */"""),
    # the long title of the true ladder ran into the live box's title
    ("""  panelTitle(ctx, b, trueAxis ? 'the true ladder, E = &minus;13.598 eV / n&sup2;'
                              : 'PhET&rsquo;s ladder (compressed)');""",
     """  panelTitle(ctx, b, trueAxis ? 'the true ladder' : 'PhET&rsquo;s ladder (compressed)');"""),
])

# ---------------------------------------------------------------- p5_views
patch("p5_views.js", [
    ("    const b2 = box(56, a2.y1 + 44, uw - 78, Math.max(80, bot - a2.y1 - 60));\n"
     "    return {L, a: a2, b: b2, side: side2, narrow: true};\n"
     "  }\n"
     "  const side = Math.max(140, Math.min(bot - top, uw * 0.52));",
     "    const b2 = box(56, a2.y1 + 44, uw - 78, Math.max(70, bot - a2.y1 - 60 - AXIS_BOT));\n"
     "    return {L, a: a2, b: b2, side: side2, narrow: true};\n"
     "  }\n"
     "  const side = Math.max(140, Math.min(bot - top, uw * 0.52));"),
    ("  const b = box(a.x1 + 56, top + 10, Math.max(150, uw - side - 80), Math.max(110, bot - top - 30));",
     "  const b = box(a.x1 + 56, top + 10, Math.max(150, uw - side - 80),\n"
     "                Math.max(100, bot - top - 30 - AXIS_BOT));"),
    ("    const b2 = box(64, a2.y1 + 46, uw - 86, Math.max(80, bot - a2.y1 - 62));",
     "    const b2 = box(64, a2.y1 + 46, uw - 86, Math.max(70, bot - a2.y1 - 62 - AXIS_BOT));"),
    ("  const b = box(a.x1 + 60, top + 14, Math.max(160, uw - side - 86), Math.max(110, bot - top - 40));",
     "  const b = box(a.x1 + 60, top + 14, Math.max(160, uw - side - 86),\n"
     "                Math.max(100, bot - top - 40 - AXIS_BOT));"),
    ("  const b = box(64, a.y1 + 80, uw - 80, Math.max(80, bot - a.y1 - 96));",
     "  const b = box(64, a.y1 + 80, uw - 80, Math.max(70, bot - a.y1 - 96 - AXIS_BOT));"),
    ("    const b2 = box(58, a2.y1 + 80, uw - 76, Math.max(70, bot - a2.y1 - 96));",
     "    const b2 = box(58, a2.y1 + 80, uw - 76, Math.max(60, bot - a2.y1 - 96 - AXIS_BOT));"),
    ("  const b = box(54, a.y1 + 80, uw - 70, Math.max(80, bot - a.y1 - 96));",
     "  const b = box(54, a.y1 + 80, uw - 70, Math.max(70, bot - a.y1 - 96 - AXIS_BOT));"),
    ("  const c = box(54 + wHalf + 46, top, wHalf, hTop);",
     "  const c = box(54 + wHalf + 62, top, wHalf - 16, hTop);"),
    # the marker label sat at the top of the spectrum panel, on top of the
    # '2->1' line label of whichever line the marker was parked on
    ("""    label(ctx, X + 4, a.y + 4, fmt(st.lam, 0) + ' nm', COL.live,
      '10.5px -apple-system, sans-serif', 'left', 'top');""",
     """    label(ctx, X + 4, a.y1 - 13, fmt(st.lam, 0) + ' nm', COL.live,
      '10.5px -apple-system, sans-serif', 'left', 'bottom');"""),
    # <r> goes in the legend instead of floating over it
    ("""  const Xm = b.x + b.w * clamp(M.meanR, 0, rmax * 1.15) / (rmax * 1.15);
  ctx.strokeStyle = COL.live; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(Xm, b.y); ctx.lineTo(Xm, b.y1); ctx.stroke();
  label(ctx, Xm + 4, b.y + 4, '⟨r⟩ = ' + fmt(M.meanR, 2) + ' a₀', COL.live,
    '10.5px -apple-system, sans-serif', 'left', 'top');
  legendAuto(ctx, b, [[COL.pos, 'r²R²'], [COL.ref, 'radial nodes'], [COL.live, '⟨r⟩']]);""",
     """  const Xm = b.x + b.w * clamp(M.meanR, 0, rmax * 1.15) / (rmax * 1.15);
  ctx.strokeStyle = COL.live; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(Xm, b.y); ctx.lineTo(Xm, b.y1); ctx.stroke();
  /* the value goes in the legend, not in a floating label beside the rule:
     legendAuto dodges CURVES, not labels (Known-bad), so the two met */
  legendAuto(ctx, b, [[COL.pos, 'r²R²'], [COL.ref, 'radial nodes'],
                      [COL.live, '⟨r⟩ = ' + fmt(M.meanR, 2) + ' a₀']]);"""),
    # bar value labels: inside the bar when it is tall, skipped when the bar is
    # empty, and never on top of the legend
    ("""    label(ctx, X - bw / 2 - 2, a.y1 - a.h * f1 - 3, fmt(f1, 2), COL.pos,
      '9.5px -apple-system, sans-serif', 'center', 'bottom');
    label(ctx, X + bw / 2 + 2, a.y1 - a.h * f2 - 3, fmt(f2, 2), COL.ref,
      '9.5px -apple-system, sans-serif', 'center', 'bottom');""",
     """    barLabel(ctx, a, X - bw / 2 - 2, f1, COL.pos);
    barLabel(ctx, a, X + bw / 2 + 2, f2, COL.ref);"""),
    ("""  legendAuto(ctx, a, [[COL.pos, 'real hydrogen (Einstein A)'], [COL.ref, 'PhET’s weights']]);""",
     """  legendAuto(ctx, a, [[COL.pos, 'real hydrogen'], [COL.ref, 'PhET’s weights']]);"""),
    ("""function drawRates(ctx, W, H, M){""",
     """/* a bar's value: above the bar when there is room, just inside its top when
   the bar reaches the frame, and not at all when the bar is empty or the spot
   is already taken by the legend */
function barLabel(ctx, b, X, f, col){
  if(!(f > 0.005)) return;
  const top = b.y1 - b.h * f;
  const above = top - 3 > b.y + 16;
  const y = above ? top - 3 : top + 13;
  ctx.font = '9.5px -apple-system, sans-serif';
  const w = ctx.measureText(fmt(f, 2)).width;
  for(const r of LEGEND_RECTS){
    if(X + w / 2 < r.x || X - w / 2 > r.x + r.w) continue;
    if(y < r.y || y - 11 > r.y + r.h) continue;
    return;
  }
  label(ctx, X, y, fmt(f, 2), col, '9.5px -apple-system, sans-serif', 'center',
    above ? 'bottom' : 'top');
}
function drawRates(ctx, W, H, M){"""),
])
