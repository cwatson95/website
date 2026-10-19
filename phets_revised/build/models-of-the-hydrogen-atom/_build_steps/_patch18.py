#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""legendAuto dodges CURVES, not labels (Known-bad) — and here it put its box
over the one marker on the lifetime panel that the box's own orange entry was
naming, so the legend said "no allowed drop" and nothing orange was visible.
Close it properly: legendAuto now rejects a corner that hits a recorded LABEL
rectangle as well as a recorded curve segment.  Then the 2s note goes down as
mandatory text before the legend, and the legend has to find somewhere else."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(fname, pairs):
    p = os.path.join(HERE, fname)
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        if s.count(old) == 0 and s.count(new) == 1:
            continue
        assert s.count(old) == 1, ("%s: %r appears %d times" % (fname, old[:70], s.count(old)))
        s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(s)
    print(fname, "patched")


patch("p1_utils.js", [
    ("""  for(const [cx,cy] of cands){
    let hit=false;
    for(let i=0;i<POLY_SEGS.length&&!hit;i+=4){
      const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
      if(Math.max(x0,x1)<cx||Math.min(x0,x1)>cx+bw||
         Math.max(y0,y1)<cy||Math.min(y0,y1)>cy+bh) continue;
      hit=true;
    }
    if(!hit) return legendBox(ctx,cx,cy,items);
  }""",
     """  for(const [cx,cy] of cands){
    let hit=false;
    for(let i=0;i<POLY_SEGS.length&&!hit;i+=4){
      const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
      if(Math.max(x0,x1)<cx||Math.min(x0,x1)>cx+bw||
         Math.max(y0,y1)<cy||Math.min(y0,y1)>cy+bh) continue;
      hit=true;
    }
    /* and LABELS, not only curves: the shipped helper dodged POLY_SEGS alone,
       so a legend could sit on the very marker its own entry was naming
       (Known-bad, models-of-the-hydrogen-atom).  LABEL_RECTS is this file's
       registry of every label already drawn. */
    if(!hit && typeof LABEL_RECTS !== 'undefined')
      for(const r of LABEL_RECTS){
        if(r.x+r.w<cx||r.x>cx+bw||r.y+r.h<cy||r.y>cy+bh) continue;
        hit=true; break;
      }
    if(!hit) return legendBox(ctx,cx,cy,items);
  }"""),
])

patch("p5_views.js", [
    ("""  for(const t of taus){
    const X = c.x + c.w * (t.n + (t.l - (t.n - 1) / 2) * 0.13 - 1.5) / (NMAX - 1);""",
     """  /* the 2s note is MANDATORY and goes down before the scatter and the legend,
     so both have to keep out of its way */
  label(ctx, c.x + 8, c.y + 5, '2s has no allowed drop: \\u03c4 = \\u221e, plotted on the top rule',
    COL.ref, '10px -apple-system, sans-serif', 'left', 'top');
  for(const t of taus){
    const X = c.x + c.w * (t.n + (t.l - (t.n - 1) / 2) * 0.13 - 1.5) / (NMAX - 1);"""),
    ("""      metaX = X;
      disc(ctx, X, c.y + 7, 3.4, COL.ref);
      POLY_SEGS.push(X - 4, c.y + 7, X + 4, c.y + 7);
      continue;""",
     """      metaX = X;
      disc(ctx, X, c.y + 22, 3.4, COL.ref);
      POLY_SEGS.push(X - 4, c.y + 22, X + 4, c.y + 22);
      continue;"""),
    ("""  if(metaX) labelIfClear(ctx, metaX + 7, c.y + 7, '2s: ∞', COL.ref,
    '10px -apple-system, sans-serif', 'left', 'middle');""",
     """  if(metaX){
    ctx.save(); ctx.strokeStyle = 'rgba(232,132,58,0.45)'; ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(c.x, c.y + 22); ctx.lineTo(c.x1, c.y + 22); ctx.stroke(); ctx.restore();
  }"""),
])
