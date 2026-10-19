#!/usr/bin/env python3
"""Build p1_head.html by EXTRACTION from the house sims (PLAYBOOK section 4:
the aesthetic is extracted, not restyled).

  scaffold : projects/simulations/build_lagr/p1_head.html, from <style> to
             'use strict'; (the CSS, the site-nav block, the body markup) —
             the same cut build/gas-properties/make_head.py takes.  Edited:
             the :root role-colour comment, <h1>, .sub, and the seven site-nav
             hrefs (absolute: the relative ../website/ links are dead from
             docs/phets_revised/).  Everything else is byte-identical.

p1_utils.js, p2_engine.js and p4a_helpers.js are NOT copied: assemble.py reads
them straight out of build/gas-properties/, which owns them.
"""
import io, os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
lagr = os.path.join(root, 'projects', 'simulations', 'build_lagr')

src = io.open(os.path.join(lagr, 'p1_head.html'), encoding='utf-8').read()
i = src.index('<style>')
k = src.index("<script>\n'use strict';\n") + len("<script>\n'use strict';\n")
body = src[i:k]


def sub1(s, old, new):
    assert s.count(old) == 1, (old[:60], s.count(old))
    return s.replace(old, new)


body = sub1(body, """    /* role colours: green = the computed orbit or curve, orange = a reference
       value, a warning or the unstable branch, magenta = the live particle or
       spacecraft, cyan = structure (the primaries, the frame, the axes). */""",
            """    /* role colours: green = the computed thing (the measured trace, the
       simulated sweep point), orange = the reference/analytic law (the ideal
       gas law, the isotherms, kinetic theory) or a warning, magenta = the live
       marker (the state now, the handle being dragged), cyan = structure (the
       box, the walls, the axes).  The two species have their own colour slots
       (COL.heavy, COL.light) rather than borrowing a role colour. */""")
body = sub1(body, '<h1>Lagrange points</h1>', '<h1>Gases intro</h1>')
j0 = body.index('<span class="sub" id="sub">')
j1 = body.index('</span>', j0) + len('</span>')
body = body[:j0] + ('<span class="sub" id="sub">A box of hard disks, PhET&rsquo;s two intro screens &mdash; pump, '
                    'heat and squeeze, then hold one of P, V and T still and watch the other two answer, with '
                    'the gas laws measured off the simulation rather than assumed</span>') + body[j1:]
NAV = [('../website/index.html', 'https://cooper-watson.net/index.html'),
       ('../website/about.html', 'https://cooper-watson.net/about.html'),
       ('../website/teaching.html', 'https://cooper-watson.net/teaching.html'),
       ('../modules/teaching_modules.html', 'https://cooper-watson.net/modules/teaching_modules.html'),
       ('../website/simulations.html', 'https://cooper-watson.net/simulations.html'),
       ('../website/research.html', 'https://cooper-watson.net/research.html'),
       ('../website/cv.html', 'https://cooper-watson.net/cv.html')]
for old, new in NAV:
    body = sub1(body, 'href="%s"' % old, 'href="%s"' % new)
assert 'href="../' not in body
assert 'aria-current="page"' in body
for want in ['id="scene"', 'id="panel"', 'id="tabs"', 'id="readout"', 'id="eqbar"',
             'id="tag"', 'id="hint"', 'id="errbox"', 'site-nav']:
    assert want in body, want

top = io.open(os.path.join(here, 'p0_top.html'), encoding='utf-8').read()
io.open(os.path.join(here, 'p1_head.html'), 'w', encoding='utf-8').write(top + body)
print('p1_head.html: %d lines (scaffold %d from build_lagr)'
      % (len((top + body).splitlines()), len(body.splitlines())))
