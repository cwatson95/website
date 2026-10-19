#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).
Same three cuts as build/molecule-shapes/make_head.py; only the <h1>, the .sub
tagline, the role-colour comment and the seven absolute site-nav hrefs differ."""
import io, os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
SIM = os.path.join(root, 'projects', 'simulations')

src = io.open(os.path.join(SIM, 'build_lagr', 'p1_head.html'), encoding='utf-8').read()
i = src.index('<style>')
k = src.index("<script>\n'use strict';\n") + len("<script>\n'use strict';\n")
body = src[i:k]


def sub1(s, old, new):
    assert s.count(old) == 1, (old[:60], s.count(old))
    return s.replace(old, new)


body = sub1(body, """    /* role colours: green = the computed orbit or curve, orange = a reference
       value, a warning or the unstable branch, magenta = the live particle or
       spacecraft, cyan = structure (the primaries, the frame, the axes). */""",
            """    /* role colours: green = the computed thing (the bond dipoles, the model
       curves), orange = the reference (the measured dipole moment, the ideal
       or limiting case) or a warning, magenta = the live marker (the molecular
       dipole, the current angle), cyan = structure (the atoms' frame, the
       plates, the axes). */""")
body = sub1(body, '<h1>Lagrange points</h1>', '<h1>Molecule polarity</h1>')
tagline = ('Two electronegativities set a bond dipole, partial charges and the surface that shows them; a bond angle '
           'you drag adds two bond dipoles into a molecular one that cancels exactly at 180&deg;; a field turns the '
           'molecule until the dipole lines up; and nineteen real molecules carry their measured dipole moments')
j0 = body.index('<span class="sub" id="sub">')
j1 = body.index('</span>', j0) + len('</span>')
body = body[:j0] + '<span class="sub" id="sub">' + tagline + '</span>' + body[j1:]
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

top = io.open(os.path.join(here, 'p0_top.html'), encoding='utf-8').read()
io.open(os.path.join(here, 'p1_head.html'), 'w', encoding='utf-8').write(top + body)

utils = io.open(os.path.join(SIM, 'build_lagr', 'p1_utils.js'), encoding='utf-8').read()
assert 'function plain(' in utils and 'function polyline(' in utils and 'function legendAuto(' in utils
# ENTS extension (the Known-bad rule: extend the table rather than let an
# unknown entity reach fillText verbatim).  psi and zeta are the field view's
# angle and damping ratio; Aring is the angstrom the real molecules are in.
OLD_ENT = "'&theta;':'\u03b8',"
NEW_ENT = "'&theta;':'\u03b8','&psi;':'\u03c8','&zeta;':'\u03b6','&Aring;':'\u212b','&xi;':'\u03be',"
assert utils.count(OLD_ENT) == 1, utils.count(OLD_ENT)
utils = utils.replace(OLD_ENT, NEW_ENT)
io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

buoy = io.open(os.path.join(SIM, 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
hcut = buoy.index('/* the fluid: a translucent slab')
helpers = buoy[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                              'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
assert 'function axesR(' in helpers and 'function lab(' in helpers and 'function stageLayout(' in helpers
lagr = io.open(os.path.join(SIM, 'build_lagr', 'p4_views.js'), encoding='utf-8').read()
c0 = lagr.index('/* ---- 3-vector helpers, orbit camera, perspective projection')
c1 = lagr.index('function seg3(')
c1 = lagr.index('\n', c1) + 1
cam = lagr[c0:c1]
assert 'function makeCamera(' in cam and 'function camBasis(' in cam and 'function project(' in cam and 'function poly3(' in cam
helpers = helpers + '\n/* ---- the 3-D block, from build_lagr/p4_views.js ---- */\n' + cam
io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)
print('p1_head.html: %d lines   p1_utils.js: %d lines   p4a_helpers.js: %d lines (camera %d)'
      % (len((top + body).splitlines()), len(utils.splitlines()), len(helpers.splitlines()), len(cam.splitlines())))
