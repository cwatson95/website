#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three grazes that only the half-pixel rule sees.

  * labelIfClear checked the label registry but not LEGEND_RECTS, so a z score
    could sit on the legend the shared legendBox had already drawn.
  * The levels view put three panels side by side in 320 px of usable stage at
    560x380, and the two ladder titles overlapped.  It now drops the live box
    and shortens both titles when the panels are narrow.
  * The Schrodinger ladder's "l = 0 1 2 ..." legend sat 12 px above the frame,
    which is where the n = 1 level lands on PhET's compressed axis.  The ladder
    now starts 28 px up when the l columns are drawn.
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
    ("""function labelIfClear(ctx, x, y, t, col, font, align, base){
  const r = labelRect(ctx, x, y, t, font, align, base);
  for(const q of LABEL_RECTS) if(rectsHit(r, q)) return false;""",
     """function labelIfClear(ctx, x, y, t, col, font, align, base){
  const r = labelRect(ctx, x, y, t, font, align, base);
  for(const q of LABEL_RECTS) if(rectsHit(r, q)) return false;
  /* the shared legendBox() draws its own text and records it in LEGEND_RECTS,
     not in the label registry — check both, or a dodging label lands on a
     legend (a z score did exactly that at 820x520) */
  for(const q of LEGEND_RECTS) if(rectsHit(r, q)) return false;"""),
    # --- the levels view: three panels do not fit a narrow stage ------------
    ("""  const top = L.top + 26, bot = L.bot - 24;
  const uw = usableW(W);
  const pw = Math.max(120, (uw - 60) * 0.42);
  const a = box(56, top, pw, bot - top);
  const bx = box(a.x1 + 54, top, pw, bot - top);
  const side = Math.max(90, Math.min(bot - top, W - bx.x1 - 40));
  const c = box(Math.min(W - side - 20, bx.x1 + 28), bot - side, side, side);
  return {L, a, b: bx, c, side};""",
     """  const top = L.top + 26, bot = L.bot - 24;
  const uw = usableW(W);
  if(narrowStage(W)){
    /* no room for the live box as well as the two ladders: the box is the one
       the first view already shows, so it goes */
    const pw2 = Math.max(90, (uw - 70) / 2);
    const a2 = box(56, top, pw2, bot - top);
    const b2 = box(a2.x1 + 44, top, pw2, bot - top);
    return {L, a: a2, b: b2, c: null, side: 0, narrow: true};
  }
  const pw = Math.max(120, (uw - 60) * 0.42);
  const a = box(56, top, pw, bot - top);
  const bx = box(a.x1 + 54, top, pw, bot - top);
  const side = Math.max(90, Math.min(bot - top, W - bx.x1 - 40));
  const c = box(Math.min(W - side - 20, bx.x1 + 28), bot - side, side, side);
  return {L, a, b: bx, c, side};"""),
    ("""  drawLadder(ctx, G.a, M, false);
  drawLadder(ctx, G.b, M, true);
  /* the live box */
  const bb = G.c;""",
     """  drawLadder(ctx, G.a, M, false);
  drawLadder(ctx, G.b, M, true);
  if(!G.c) return;
  /* the live box */
  const bb = G.c;"""),
    ("""  panelTitle(ctx, b, trueAxis ? 'the true ladder' : 'PhET&rsquo;s ladder (compressed)');""",
     """  /* a 26-character title does not fit a 130 px panel, and the two ran into
     each other at 560x380 */
  panelTitle(ctx, b, b.w < 200 ? (trueAxis ? 'true' : 'PhET&rsquo;s')
                               : (trueAxis ? 'the true ladder' : 'PhET&rsquo;s ladder (compressed)'));"""),
    # --- room under the Schrodinger ladder for its l legend -----------------
    ("""  const yOf = n => trueAxis ? b.y1 - 16 - (b.h - 40) * (1 - 1 / (n * n))
                            : b.y1 - 16 - (b.h - 40) * PHET.levelY[n - 1];""",
     """  /* the Schrodinger diagram carries an "l = 0 1 2 ..." legend along the
     bottom, which is exactly where n = 1 lands on PhET's compressed axis */
  const foot = (st.model === 'schrodinger') ? 28 : 16;
  const yOf = n => trueAxis ? b.y1 - foot - (b.h - 24 - foot) * (1 - 1 / (n * n))
                            : b.y1 - foot - (b.h - 24 - foot) * PHET.levelY[n - 1];"""),
    ("""  const yInf = trueAxis ? b.y1 - 16 - (b.h - 40) : b.y + 16;""",
     """  const yInf = trueAxis ? b.y1 - foot - (b.h - 24 - foot) : b.y + 16;"""),
])
