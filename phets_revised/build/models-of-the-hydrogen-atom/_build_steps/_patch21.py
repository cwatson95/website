#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Small-stage polish, all found by looking at the PNGs:

  * the model's one-line claim is 55 characters and the box is 130 px wide at
    560x380, so it ran three times the width of the thing it labels (the audit
    cannot see it: the text is inside the canvas, just not inside the box);
  * the light source's rectangle is a FILL, so the audit is blind to it, and it
    sat on the spectrometer's title;
  * the caption promised "faint green rings" in configurations that do not draw
    them;
  * the short fallback captions were written in ASCII (|psi|^2) while the long
    ones use the glyphs.
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
    ("  const availH = (st.showSpectro ? spB.y - 16 : L.bot) - L.top - gunH - 16;",
     "  const availH = (st.showSpectro ? spB.y - 16 : L.bot) - L.top - gunH - 26;"),
    ("""  labelIfClear(ctx, bb.x + 10, bb.y + 28, MODEL_CLAIM[st.model], '#767e92',
    '11px -apple-system, sans-serif', 'left', 'top');""",
     """  /* the claim is 55 characters: below 280 px of box it is three times as wide
     as the thing it labels, and the control panel carries it anyway */
  if(bb.w >= 280) labelIfClear(ctx, bb.x + 10, bb.y + 28, MODEL_CLAIM[st.model], '#767e92',
    '11px -apple-system, sans-serif', 'left', 'top');"""),
    ("""  label(ctx, b.x, b.y - 13, 'spectrometer &mdash; photons emitted per wavelength'
    + (st.logCount ? ' (log counts)' : '') + '; ' + M.emitted + ' so far',
    '#aeb6c6', 'italic 12.5px Georgia, serif', 'left', 'bottom');""",
     """  label(ctx, b.x, b.y - 13, b.w < 620
    ? 'spectrometer' + (st.logCount ? ', log counts' : '') + ': ' + M.emitted + ' photons'
    : 'spectrometer &mdash; photons emitted per wavelength'
      + (st.logCount ? ' (log counts)' : '') + '; ' + M.emitted + ' so far',
    '#aeb6c6', 'italic 12.5px Georgia, serif', 'left', 'bottom');"""),
    ("""    + 'orbit is 36 times n = 1, not 15.5 times, and a photon has no size at all. The faint green rings are where '
    + 'n&sup2;a&#8320; would put the orbits.';""",
     """    + 'orbit is 36 times n = 1, not 15.5 times, and a photon has no size at all.'
    + (st.showExact ? ' The faint green rings are where n&sup2;a&#8320; would put the orbits.' : '');"""),
])

patch("p5_views.js", [
    ("    'The cloud is |psi|^2 integrated along the line of sight; the nodes are surfaces.');",
     "    'The cloud is ∫|ψ|² dy through the orbital: the dark rings and cones are its nodes.');"),
    ("    'PhET’s weight table against the Einstein A coefficients of real hydrogen.');",
     "    'PhET’s weight table against the Einstein A coefficients of real hydrogen, and the dice checked.');"),
])
