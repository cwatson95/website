#!/usr/bin/env python3
"""p1_head.html = p0_top.html (the header comment) + the scaffold taken
verbatim from build/fourier-making-waves/p1_head.html, with only the <h1>, the
.sub tagline and the :root role colours edited.  The scaffold's SHA is pinned
in both directions so neither side can drift silently."""
import hashlib
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'fourier-making-waves', 'p1_head.html')
SCAFFOLD_SHA = '0d1b28bfcf17c2d8538c2312db005aa267204cb702d826580def5c0e797874d8'

src = io.open(SRC, encoding='utf-8').read()
i = src.index('<style>')
scaffold = src[i:]
got = hashlib.sha256(scaffold.encode('utf-8')).hexdigest()
if SCAFFOLD_SHA != 'PRINT':
    assert got == SCAFFOLD_SHA, 'fourier scaffold changed upstream: %s' % got
else:
    print(got)

# the only edits: the role colours, the h1 and the tagline
scaffold = scaffold.replace(
    "    --pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --wplus:#5ac8e0; --wminus:#e8843a;",
    "    --pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --integ:#5ac8e0; --deriv:#cd35c4;")
scaffold = scaffold.replace(
    "       partial sum, the discrete packet), orange = the reference/analytic curve\n"
    "       (the waveform the series converges to, the continuous packet, the exact\n"
    "       envelope) or a warning, magenta = the live marker (the selected harmonic,\n"
    "       the caliper, the Gibbs peak), cyan = structure (axes, the zero line, the\n"
    "       component stems).  The eleven harmonics themselves use the house NEON\n"
    "       ramp, which is a scale, not a role. */",
    "       curve you draw and everything computed from it), orange = the exact\n"
    "       closed form, the one-sided limits and the second derivative (which is a\n"
    "       warning as much as a curve), magenta = the live marker and the first\n"
    "       derivative, cyan = structure and the integral.  No scalar ramp is used:\n"
    "       nothing here is a magnitude map. */")
assert '--integ:#5ac8e0' in scaffold and 'closed form, the one-sided limits' in scaffold

scaffold = scaffold.replace(
    '<h1>Fourier: making waves</h1>', '<h1>Calculus grapher</h1>')
old_sub = re.search(r'<span class="sub" id="sub">.*?</span>', scaffold, re.S)
assert old_sub, 'tagline not found'
scaffold = scaffold.replace(old_sub.group(0),
    '<span class="sub" id="sub">A remake of PhET&rsquo;s Calculus Grapher &mdash; draw a function by hand '
    'and watch its slope, its running area and its curvature follow, with the fundamental theorem holding '
    'to the last bit and the corners where the derivative stops existing shown as what they are</span>')

top = io.open(os.path.join(HERE, 'p0_top.html'), encoding='utf-8').read()
io.open(os.path.join(HERE, 'p1_head.html'), 'w', encoding='utf-8').write(top + scaffold)
print('p1_head.html: %d lines (%d of header comment)'
      % (len((top + scaffold).splitlines()), len(top.splitlines())))
