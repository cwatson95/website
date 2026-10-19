#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Layout round 4 — the 560x380 stage.

The root cause of the last batch: on a narrow stage the LONG caption still fit
(seven lines), which left the panels 224 px of stack to live in when they need
at least 224, and stackFit's floor then pushed the bottom axis onto the caption.
A narrow stage now demands far more headroom before it will take the long
caption, so the short one is chosen and the panels fit.

Second general fix: the caption is drawn FIRST in every view, so its rectangle
is in the registry and every optional label dodges it instead of landing on it.
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
    ("  const f = fitCaption(ctx, W, H - HINT_H, full, short, W - 40, stageTop() + 120);",
     "  /* a narrow stage has to keep 300 px for the picture, or the long caption\n"
     "     eats the stack and the bottom panel's axis title lands on it */\n"
     "  const f = fitCaption(ctx, W, H - HINT_H, full, short, W - 40,\n"
     "                       stageTop() + (narrowStage(W) ? 300 : 120));"),
    # the caption goes down FIRST so every optional label can dodge it
    ("""  /* the spectrometer */
  if(st.showSpectro) drawSpectrometer(ctx, G.spB, M);
  drawCaption(ctx, G.L);
}""",
     """  /* the spectrometer */
  if(st.showSpectro) drawSpectrometer(ctx, G.spB, M);
}"""),
    ("""function drawBox(ctx, W, H, M){
  const st = M.st, G = boxGeo(ctx, W, H, M), bb = G.bb, s = G.s;""",
     """function drawBox(ctx, W, H, M){
  const st = M.st, G = boxGeo(ctx, W, H, M), bb = G.bb, s = G.s;
  drawCaption(ctx, G.L);"""),
    ("""  label(ctx, G.cx + gw / 2 + 9, gy + gh / 2, st.lightOn""",
     """  labelIfClear(ctx, G.cx + gw / 2 + 9, gy + gh / 2, st.lightOn"""),
    ("""  label(ctx, bb.x + 10, bb.y + 28, MODEL_CLAIM[st.model], '#767e92',
    '11px -apple-system, sans-serif', 'left', 'top');""",
     """  labelIfClear(ctx, bb.x + 10, bb.y + 28, MODEL_CLAIM[st.model], '#767e92',
    '11px -apple-system, sans-serif', 'left', 'top');"""),
    ("  const gunH = 40;", "  const gunH = 48;"),
    # levels: caption first, and the energy values only where there is room
    ("""function drawLevels(ctx, W, H, M){
  const st = M.st, G = levelsGeo(ctx, W, H, M);""",
     """function drawLevels(ctx, W, H, M){
  const st = M.st, G = levelsGeo(ctx, W, H, M);
  drawCaption(ctx, G.L);"""),
    ("""  panelTitle(ctx, bb, 'the atom');
  drawCaption(ctx, G.L);
}""",
     """  panelTitle(ctx, bb, 'the atom');
}"""),
    ("""    if(trueAxis) labelIfClear(ctx, x0 - 5, y, fmt(energyEV(n), 2), '#6f7789',
      '9.5px -apple-system, sans-serif', 'right', 'middle');""",
     """    /* below 150 px of panel there is no room between the energy axis and the
       level lines for a value, and it lands on the rotated axis title */
    if(trueAxis && b.w >= 150) labelIfClear(ctx, x0 - 5, y, fmt(energyEV(n), 2), '#6f7789',
      '9.5px -apple-system, sans-serif', 'right', 'middle');"""),
    # the rotated axis title is drawn in a rotated frame, so its registry
    # rectangle would be computed in the wrong place — draw it raw
    ("""  ctx.save(); ctx.translate(b.x + 13, b.y + b.h / 2); ctx.rotate(-PI / 2);
  label(ctx, 0, 0, 'energy', '#8b93a6', '11px -apple-system, sans-serif', 'center', 'bottom');
  ctx.restore();""",
     """  ctx.save(); ctx.translate(b.x + 13, b.y + b.h / 2); ctx.rotate(-PI / 2);
  ctx.fillStyle = '#8b93a6'; ctx.font = '11px -apple-system, sans-serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
  ctx.fillText('energy', 0, 0);          /* rotated: not registered, see labelRect */
  ctx.restore();"""),
])

patch("p5_views.js", [
    ("""function drawWave(ctx, W, H, M){
  const st = M.st, G = waveGeo(ctx, W, H, M), a = G.a;""",
     """function drawWave(ctx, W, H, M){
  const st = M.st, G = waveGeo(ctx, W, H, M), a = G.a;
  drawCaption(ctx, G.L);"""),
    ("""  legendAuto(ctx, b, [[COL.pos, 'mismatch 2|sin πν|'], [COL.live, 'where you are'],
                      [COL.struct, 'the allowed orbits']]);
  drawCaption(ctx, G.L);
}""",
     """  legendAuto(ctx, b, [[COL.pos, 'mismatch 2|sin πν|'], [COL.live, 'where you are'],
                      [COL.struct, 'the allowed orbits']]);
}"""),
    ("""function drawOrbitals(ctx, W, H, M){
  const st = M.st, G = orbGeo(ctx, W, H, M), a = G.a, n = M.on, l = M.ol, m = M.om;""",
     """function drawOrbitals(ctx, W, H, M){
  const st = M.st, G = orbGeo(ctx, W, H, M), a = G.a, n = M.on, l = M.ol, m = M.om;
  drawCaption(ctx, G.L);"""),
    ("""  legendAuto(ctx, b, [[COL.pos, 'r²R²'], [COL.ref, 'radial nodes'],
                      [COL.live, '⟨r⟩ = ' + fmt(M.meanR, 2) + ' a₀']]);
  drawCaption(ctx, G.L);
}""",
     """  legendAuto(ctx, b, [[COL.pos, 'r²R²'], [COL.ref, 'radial nodes'],
                      [COL.live, '⟨r⟩ = ' + fmt(M.meanR, 2) + ' a₀']]);
}"""),
    ("""  const sLines = wrapText(ctx, scaleTxt, a.w - 16, '10.5px -apple-system, sans-serif');
  LABEL_RECTS.push({x: a.x + 8, y: a.y1 - 8 - sLines.length * 13, w: a.w - 16, h: sLines.length * 13});
  ctx.fillStyle = '#8d95a8'; ctx.textAlign = 'left'; ctx.textBaseline = 'top';
  ctx.font = '10.5px -apple-system, sans-serif';
  for(let i = 0; i < sLines.length; i++)
    ctx.fillText(sLines[i], a.x + 8, a.y1 - 8 - sLines.length * 13 + i * 13);""",
     """  const sLines = wrapText(ctx, scaleTxt, a.w - 16, '10.5px -apple-system, sans-serif');
  /* on a small panel the note would wrap to more lines than the panel is tall
     and climb into its own title; the readout carries the same numbers */
  if(sLines.length * 13 < a.h * 0.32){
    LABEL_RECTS.push({x: a.x + 8, y: a.y1 - 8 - sLines.length * 13, w: a.w - 16, h: sLines.length * 13});
    ctx.fillStyle = '#8d95a8'; ctx.textAlign = 'left'; ctx.textBaseline = 'top';
    ctx.font = '10.5px -apple-system, sans-serif';
    for(let i = 0; i < sLines.length; i++)
      ctx.fillText(sLines[i], a.x + 8, a.y1 - 8 - sLines.length * 13 + i * 13);
  }"""),
    ("""function drawSeries(ctx, W, H, M){
  const st = M.st, G = serGeo(ctx, W, H, M), a = G.a, b = G.b;""",
     """function drawSeries(ctx, W, H, M){
  const st = M.st, G = serGeo(ctx, W, H, M), a = G.a, b = G.b;
  drawCaption(ctx, G.L);"""),
    ("""  legendAuto(ctx, b, [[COL.pos, 'NIST vacuum (Lyman)'], [COL.ref, 'NIST air (Edlén 1966)']]);
  drawCaption(ctx, G.L);
}""",
     """  legendAuto(ctx, b, [[COL.pos, 'NIST vacuum (Lyman)'], [COL.ref, 'NIST air (Edlén 1966)']]);
}"""),
    # the marker label is mandatory, so it goes down BEFORE the series limits
    ("""  /* the lines */
  const rowOf = n1 => a.y + 16 + (n1 - 1) * (a.h - 42) / 5;""",
     """  /* the marker first: it is mandatory, so the optional limit and transition
     labels have to dodge IT, not the other way round */
  const rowOf = n1 => a.y + 16 + (n1 - 1) * (a.h - 42) / 5;
  if(st.lam >= 80 && st.lam <= 15000){
    const Xm2 = a.x + a.w * (Math.log10(st.lam) - lo) / (hi - lo);
    ctx.strokeStyle = COL.live; ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(Xm2, a.y); ctx.lineTo(Xm2, a.y1); ctx.stroke();
    label(ctx, Xm2 + 4, a.y1 - 13, fmt(st.lam, 0) + ' nm', COL.live,
      '10.5px -apple-system, sans-serif', 'left', 'bottom');
  }
  /* the lines */"""),
    ("""  /* the marker */
  if(st.lam >= 80 && st.lam <= 15000){
    const X = a.x + a.w * (Math.log10(st.lam) - lo) / (hi - lo);
    ctx.strokeStyle = COL.live; ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(X, a.y); ctx.lineTo(X, a.y1); ctx.stroke();
    label(ctx, X + 4, a.y1 - 13, fmt(st.lam, 0) + ' nm', COL.live,
      '10.5px -apple-system, sans-serif', 'left', 'bottom');
  }
  /* the residuals against NIST */""",
     """  /* the residuals against NIST */"""),
    ("""function drawRates(ctx, W, H, M){
  const st = M.st, G = ratesGeo(ctx, W, H, M);""",
     """function drawRates(ctx, W, H, M){
  const st = M.st, G = ratesGeo(ctx, W, H, M);
  drawCaption(ctx, G.L);"""),
    ("""  if(!c){ drawRatesEnsemble(ctx, M, b, cats, nF); drawCaption(ctx, G.L); return; }""",
     """  if(!c){ drawRatesEnsemble(ctx, M, b, cats, nF); return; }"""),
    ("""  drawRatesEnsemble(ctx, M, b, cats, nF);
  drawCaption(ctx, G.L);
}
function drawRatesEnsemble(ctx, M, b, cats, nF){""",
     """  drawRatesEnsemble(ctx, M, b, cats, nF);
}
function drawRatesEnsemble(ctx, M, b, cats, nF){"""),
])
