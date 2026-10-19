#!/usr/bin/env python3
"""Extract the house scaffold (CSS, site-nav block, body markup) from
projects/simulations/build_buoy/p1_head.html and write p1_head.html for
charges-and-fields with ONLY the title, the header comment, the :root accent
comment and values, the <h1>, the .sub tagline and the site-nav hrefs changed
(the hrefs made absolute, BRIEF.md).  Every replacement is asserted to hit
exactly once, so a drifted source fails loudly instead of silently."""
import io
import os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
src = os.path.join(root, 'projects', 'simulations', 'build_buoy', 'p1_head.html')
s = io.open(src, encoding='utf-8').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:60], s.count(old))
    s = s.replace(old, new)


# the title
rep('<title>Buoyancy &mdash; Archimedes&rsquo; principle, from the spring scale to the metacentre</title>',
    '<title>Charges and Fields &mdash; point charges, their field and potential</title>')

# the header comment: everything between '<!--' and '-->'
i = s.index('<!--')
j = s.index('-->', i) + 3
HEADER = io.open(os.path.join(here, 'header_comment.txt'), encoding='utf-8').read().rstrip('\n')
s = s[:i] + '<!--\n' + HEADER + '\n-->' + s[j:]

# the :root accents and their role comment
rep("""    /* role colours: green = the quantity computed (the upthrust, the submerged
       polygon), orange = the reference/analytic value or a warning,
       magenta = the live marker (the centre of buoyancy, the live state),
       cyan = structure (the fluid, the waterline, the vessel). */
    --pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --wplus:#5ac8e0; --wminus:#e8843a;""",
    """    /* role colours: green = a positive charge, V > 0 and the computed field
       lines; magenta = a negative charge and V < 0 (the house charge pair, as
       in dipole_radiation.html); orange = the reference/analytic curve, the
       null points, a warning; cyan = structure (equipotentials, the tape, the
       grid, the axes); the live probes and sensors are white. */
    --pos:#b8ec4c; --neg:#cd35c4; --ref:#e8843a; --live:#f2f4f8; --struct:#5ac8e0;""")

# the site nav: absolute links (the relative ../website/ ones are dead from docs/phets_revised/)
rep('<a href="../website/index.html">Home</a>', '<a href="https://cooper-watson.net/index.html">Home</a>')
rep('<a href="../website/about.html">About</a>', '<a href="https://cooper-watson.net/about.html">About</a>')
rep('<a href="../website/teaching.html">Teaching</a>', '<a href="https://cooper-watson.net/teaching.html">Teaching</a>')
rep('<a href="../modules/teaching_modules.html">Modules</a>',
    '<a href="https://cooper-watson.net/modules/teaching_modules.html">Modules</a>')
rep('<a href="../website/simulations.html" aria-current="page">Simulations</a>',
    '<a href="https://cooper-watson.net/simulations.html" aria-current="page">Simulations</a>')
rep('<a href="../website/research.html">Research</a>', '<a href="https://cooper-watson.net/research.html">Research</a>')
rep('<a href="../website/cv.html">CV</a>', '<a href="https://cooper-watson.net/cv.html">CV</a>')
rep('/* injected site header — palette & tabs match ../website/style.css */',
    '/* injected site header — palette & tabs match the site stylesheet (links absolute: this page lives outside the site tree) */')

# the h1 and the tagline
rep('<h1>Buoyancy</h1>', '<h1>Charges and Fields</h1>')
i = s.index('<span class="sub" id="sub">')
j = s.index('</span>', i) + len('</span>')
s = (s[:i] + '<span class="sub" id="sub">point charges on a plane and their exact field and potential &mdash; '
     'the voltage map, equipotentials, field lines, the potential as a landscape, superposition and the multipole far field</span>'
     + s[j:])

assert '../website/' not in s and '../modules/' not in s
io.open(os.path.join(here, 'p1_head.html'), 'w', encoding='utf-8').write(s)
print('p1_head.html: %d lines' % len(s.splitlines()))
