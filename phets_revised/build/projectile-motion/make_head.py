#!/usr/bin/env python3
"""Build p1_head.html: the house scaffold extracted from diffraction.html by the
PLAYBOOK recipe (everything from <style> to the end of project()), with ONLY the
<h1>, the .sub tagline, the :root accents and the site-nav hrefs changed, and
the doctype / <title> / header comment prepended."""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
W = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
SRC = os.path.join(W, 'projects', 'simulations', 'diffraction.html')
src = io.open(SRC, encoding='utf-8').read()
i = src.index('<style>')
k = src.index('function project(')
e = src.index('\n}\n', k) + 3
body = src[i:e]
n0 = len(body.splitlines())

def swap(s, old, new):
    assert s.count(old) == 1, (old, s.count(old))
    return s.replace(old, new)

body = swap(body, '--plate:#39404f; --beam:#5ac8e0; --envelope:#e8843a;',
            '--pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --struct:#5ac8e0; --tape:#d9b44a;')
body = swap(body, '<h1>Diffraction</h1>', '<h1>Projectile Motion</h1>')
body = swap(body, '<span class="sub" id="sub">a slit does not cast a shadow &mdash; it casts a spectrum of directions</span>',
            '<span class="sub" id="sub">a cannon, a projectile and the air &mdash; the parabola in closed form, '
            'quadratic drag integrated and checked three ways, the envelope of every shot, and the hodograph '
            'that ends at terminal velocity</span>')
# the house sims' relative ../website/ links are dead from docs/phets_revised/:
# point every link at the live site (BRIEF; phets_revised Known-bad)
for old, new in [('../website/index.html', 'https://cooper-watson.net/index.html'),
                 ('../website/about.html', 'https://cooper-watson.net/about.html'),
                 ('../website/teaching.html', 'https://cooper-watson.net/teaching.html'),
                 ('../modules/teaching_modules.html', 'https://cooper-watson.net/modules/teaching_modules.html'),
                 ('../website/simulations.html', 'https://cooper-watson.net/simulations.html'),
                 ('../website/research.html', 'https://cooper-watson.net/research.html'),
                 ('../website/cv.html', 'https://cooper-watson.net/cv.html')]:
    body = swap(body, 'href="' + old + '"', 'href="' + new + '"')
assert 'aria-current="page"' in body

head = io.open(os.path.join(here, 'p0_comment.html'), encoding='utf-8').read()
out = head + body
io.open(os.path.join(here, 'p1_head.html'), 'w', encoding='utf-8').write(out)
print('scaffold: %d lines from %s; p1_head.html: %d lines' % (n0, SRC, len(out.splitlines())))
