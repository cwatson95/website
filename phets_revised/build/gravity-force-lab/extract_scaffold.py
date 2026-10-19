#!/usr/bin/env python3
"""Extract the house scaffold (PLAYBOOK section 4 recipe) for the two
inverse-square remakes, and write each sim's p1_head.html and the shared
p1_utils.js.

  * CSS, body markup, the numeric and colour helpers and h() come from
    projects/simulations/diffraction.html (<style> ... end of project()),
    exactly as the recipe cuts them (252 lines).
  * The 3-D block (v3, makeCamera, camBasis, project) is DROPPED: neither sim
    has a 3-D view, and code no view calls is dead code that a mutation sweep
    can only report as survivors (Known-bad: "a no-op method nothing calls").
  * The 2-D plotting layer (plain/ENTS, wrapText, caption, box, frame,
    ticksFor, logTicks, axes, polyline, legendBox/legendAuto, the caption
    fitters) is taken from projects/simulations/build_buoy/p1_utils.js, the
    newest house copy, because the diffraction copy lacks four Known-bad fixes
    (plain() strips tags + wide entity regex with the numeric decode inside,
    axes() sorts its range, polyline() clips in data space in x AND y with
    Liang-Barsky, logTicks guards non-positive bounds).  selfTest re-asserts
    each fix so they cannot rot.
  * Edits, and only these: the <h1>, the .sub tagline, the :root accents, the
    site-nav hrefs (absolute URLs to the live site: the relative ../website/
    links are dead from docs/phets_revised/), and one Known-bad fix carried
    from buoyancy: #readout td.v gets overflow-wrap:anywhere (periodic_table).

Run from anywhere:  python3 extract_scaffold.py
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
SIMS = os.path.join(ROOT, 'projects', 'simulations')

src = io.open(os.path.join(SIMS, 'diffraction.html'), encoding='utf-8').read()
i = src.index('<style>')
k = src.index('function project(')
e = src.index('\n}\n', k) + 3
scaffold = src[i:e]
assert len(scaffold.splitlines()) == 252, len(scaffold.splitlines())
css_body, script = scaffold.split("'use strict';\n", 1)
utils_top = script[:script.index('/* ================================================================== *\n *  3-vector helpers')]
assert 'function h(tag,attrs)' in utils_top and 'makeCamera' not in utils_top

buoy = io.open(os.path.join(SIMS, 'build_buoy', 'p1_utils.js'), encoding='utf-8').read()
j = buoy.index('function fmt(x,n)')
layer2d = buoy[j:]
for fn in ('function plain(', 'function wrapText(', 'function caption(', 'function box(', 'function frame(',
           'function ticksFor(', 'function logTicks(', 'function axes(', 'function polyline(',
           'function legendBox(', 'function legendAuto(', 'function fitCaption(', 'function sigf('):
    assert fn in layer2d, fn

SITE = 'https://cooper-watson.net/'
NAV_OLD = ['../website/index.html', '../website/about.html', '../website/teaching.html',
           '../modules/teaching_modules.html', '../website/simulations.html', '../website/research.html',
           '../website/cv.html']
NAV_NEW = [SITE + 'index.html', SITE + 'about.html', SITE + 'teaching.html',
           SITE + 'modules/teaching_modules.html', SITE + 'simulations.html', SITE + 'research.html',
           SITE + 'cv.html']

ROOT_OLD = '    --plate:#39404f; --beam:#5ac8e0; --envelope:#e8843a;\n'
ROOT_NEW = ('    /* role colours: green = the computed force, orange = the reference or a\n'
            '       warning (the forbidden zone, a clipped arrow), magenta = the live marker,\n'
            '       cyan = structure (the track, the ruler, the axes). */\n'
            '    --pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --struct:#5ac8e0;\n')
TDV_OLD = '  #readout td.v{color:var(--text); text-align:right; font-variant-numeric:tabular-nums;}\n'
TDV_NEW = ('  #readout td.v{color:var(--text); text-align:right; font-variant-numeric:tabular-nums;\n'
           '                overflow-wrap:anywhere; white-space:normal;}\n')


def head(stem, title, h1, sub, comment):
    b = css_body
    for o, n in zip(NAV_OLD, NAV_NEW):
        assert b.count('href="%s"' % o) == 1, o
        b = b.replace('href="%s"' % o, 'href="%s"' % n)
    assert b.count(ROOT_OLD) == 1 and b.count(TDV_OLD) == 1
    b = b.replace(ROOT_OLD, ROOT_NEW).replace(TDV_OLD, TDV_NEW)
    b = b.replace('/* injected site header — palette & tabs match ../website/style.css */',
                  '/* injected site header — palette & tabs match the live site\'s style.css */')
    b = re.sub(r'<h1>[^<]*</h1>', '<h1>%s</h1>' % h1, b, count=1)
    b = re.sub(r'<span class="sub" id="sub">[^<]*</span>', '<span class="sub" id="sub">%s</span>' % sub, b, count=1)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<!--\n%s-->\n' % (title, comment) + b + "'use strict';\n")


if __name__ == '__main__':
    # the view-layer helpers (fonts, world maps, the label registry that shifts
    # or drops a label at the audit's half-pixel rule, titleFor/axesR, the
    # bottom-up stage layout, marker) — build_buoy/p4_views.js, whose lineage
    # is build_cycloid; cut before the first buoyancy-specific function
    bv = io.open(os.path.join(SIMS, 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
    a = bv.index('const CAP_FONT=')
    z = bv.index('/* the fluid: a translucent slab')
    helpers = bv[a:z]
    for fn in ('function stageLayout(', 'function lab(', 'function labFits(', 'function axesR(',
               'function titleFor(', 'function marker(', 'function dot(', 'function worldFitUp('):
        assert fn in helpers, fn
    io.open(os.path.join(HERE, 'p4_helpers.js'), 'w', encoding='utf-8').write(
        '\n/* ================================================================== *\n'
        ' *  drawing helpers shared by the views  (projects/simulations/       *\n'
        ' *  build_buoy/p4_views.js, lineage build_cycloid; unchanged)         *\n'
        ' * ================================================================== */\n' + helpers)
    print('wrote p4_helpers.js', len(helpers.splitlines()), 'lines')
    # selfTest's text-box recorder (tracks translate/rotate/scale, so a rotated
    # axis title is measured where it lands) — build_buoy/p7_test.js
    bt = io.open(os.path.join(SIMS, 'build_buoy', 'p7_test.js'), encoding='utf-8').read()
    a = bt.index('function makeShot(W,H){')
    z = bt.index('\nfunction selfTest(){')
    shot = bt[a:z]
    assert 'fillText(t,x,y)' in shot and 'rotate(r)' in shot
    io.open(os.path.join(HERE, 'p7_kit.js'), 'w', encoding='utf-8').write(
        '\n/* ================================================================== *\n'
        ' *  selfTest kit: the text-box recorder  (projects/simulations/        *\n'
        ' *  build_buoy/p7_test.js makeShot; unchanged)                        *\n'
        ' * ================================================================== */\n' + shot)
    print('wrote p7_kit.js', len(shot.splitlines()), 'lines')
    io.open(os.path.join(HERE, 'p1_utils.js'), 'w', encoding='utf-8').write(
        '/* ================================================================== *\n'
        ' *  small utilities, colour helpers and h()  (projects/simulations/   *\n'
        ' *  diffraction.html, the PLAYBOOK scaffold cut; camera dropped)      *\n'
        ' * ================================================================== */\n'
        + utils_top.split('\n', 3)[3] +
        '/* ================================================================== *\n'
        ' *  the 2-D plotting layer  (projects/simulations/build_buoy/          *\n'
        ' *  p1_utils.js: the copy carrying every Known-bad fix)               *\n'
        ' * ================================================================== */\n'
        + layer2d)
    for stem, cfile in (('gravity-force-lab', 'head_gfl.txt'), ('coulombs-law', 'head_cl.txt')):
        spec_path = os.path.join(HERE, '..', stem, cfile)
        if not os.path.exists(spec_path):
            print('skip', stem, '(no', cfile + ')')
            continue
        spec = io.open(spec_path, encoding='utf-8').read()
        meta, comment = spec.split('\n---\n', 1)
        kv = dict(line.split('=', 1) for line in meta.strip().splitlines())
        out = head(stem, kv['title'], kv['h1'], kv['sub'], comment)
        io.open(os.path.join(HERE, '..', stem, 'p1_head.html'), 'w', encoding='utf-8').write(out)
        print('wrote', stem, 'p1_head.html', len(out.splitlines()), 'lines')
    print('wrote p1_utils.js')
