#!/usr/bin/env python3
"""family.py -- builds the magnets-and-electromagnets family from one engine.

    python3 family.py [stem ...]     (default: all three)

The engine (e1_core.js ... e5_gen.js), the shared drawing primitives
(v_common.js, v_screens.js, v_analysis.js) and the house layers live here in
build/magnets-and-electromagnets/; each sim's own parts (header comment,
state, boot, tests, UI drive) live in its own build dir.  For each stem this:

  1. extracts the house scaffold from projects/simulations/build_buoy
     (p1_head.html -> the stem's p1_head.html with ONLY the title, the header
     comment, the :root accents, the <h1>, the .sub tagline and the site-nav
     hrefs changed; every replacement asserted to hit exactly once), and the
     house 2-D layer (p1_utils.js) and view helpers (p4_helpers.js) verbatim,
     every function carried asserted present;
  2. emits p7a_refs.js from refvals.txt (derive.py's printed output) as the
     literal table REF -- never retyped -- keeping the keys that sim uses;
  3. concatenates the parts into docs/phets_revised/<stem>.html and writes
     _out/run.js (osascript) and _out/run_jsc.js (jsc) beside it.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
OUTDIR = os.path.dirname(BUILD)                      # docs/phets_revised
ROOT = os.path.abspath(os.path.join(OUTDIR, '..', '..'))
SIM = os.path.join(ROOT, 'projects', 'simulations')

ACCENTS = """    /* role colours: green = the computed field (the needles' north halves, field
       lines, the exact curves) and a magnet's north pole; magenta = a south pole;
       orange = the reference/analytic curve (the dipole, the closed forms) or a
       warning; cyan = structure (the axis, mu0 H, the bound current); the live
       tools (compass, meter, cursors) are white. */
    --pos:#b8ec4c; --neg:#cd35c4; --ref:#e8843a; --live:#f2f4f8; --struct:#5ac8e0;"""

STEMS = {
    'magnets-and-electromagnets': dict(
        title='Magnets and Electromagnets &mdash; the bar magnet, the electromagnet and the field they share',
        h1='Magnets and Electromagnets',
        sub='a bar magnet and a coil, their exact fields, the compass and the meter that read them &mdash; field lines, the field on the axis, the far-field dipole, and the needle as a pendulum',
        feats=['bar', 'coil', 'emag', 'far'],
        parts=['@p1_head.html', 'p1_utils.js', 'e1_core.js', 'e2_coil.js', 'e3_lines.js', 'e4_far.js', '@p3_state.js',
               'p4_helpers.js', 'v_common.js', 'v_screens.js', 'v_analysis.js', '@p6_boot.js', '@p7a_refs.js',
               't_core.js', 't_coil.js', 't_lines.js', 't_far.js', 't_rotor.js', '@p7_test.js'],
        refs=lambda k: not k.startswith('gen.')),
    'magnet-and-compass': dict(
        title='Magnet and Compass &mdash; a bar magnet, its exact field, and the compass that reads it',
        h1='Magnet and Compass',
        sub='a bar magnet and its exact field, the compass and the meter that read it &mdash; field lines, the field on the axis, the far-field dipole, and the needle as a pendulum',
        feats=['bar', 'far'],
        parts=['@p1_head.html', 'p1_utils.js', 'e1_core.js', 'e3_lines.js', 'e4_far.js', '@p3_state.js',
               'p4_helpers.js', 'v_common.js', 'v_screens.js', 'v_analysis.js', '@p6_boot.js', '@p7a_refs.js',
               't_core.js', 't_lines.js', 't_far.js', 't_rotor.js', '@p7_test.js'],
        refs=lambda k: not (k.startswith('gen.') or k.startswith('coil.') or k.startswith('loop.')
                            or k.startswith('lines.coil.') or k.startswith('supply'))),
    'generator': dict(
        title='Generator &mdash; a turning magnet, a pickup coil, and Faraday&rsquo;s law',
        h1='Generator',
        sub='water turns a bar magnet beside a pickup coil: the flux through the coil, the EMF it induces, &minus;N d&Phi;/dt, and the bulb and voltmeter it drives',
        feats=['coil', 'gen'],
        parts=['@p1_head.html', 'p1_utils.js', 'e1_core.js', 'e3_lines.js', 'e5_gen.js', '@p3_state.js',
               'p4_helpers.js', 'v_common.js', 'v_screens.js', 'v_analysis.js', '@v_gen.js', '@p6_boot.js',
               '@p7a_refs.js', 't_core.js', 't_lines.js', 't_rotor.js', '@t_gen.js', '@p7_test.js'],
        refs=lambda k: not (k.startswith('coil.') or k.startswith('loop.') or k.startswith('lines.coil.')
                            or k.startswith('mag.far') or k.startswith('mag.dev') or k.startswith('mag.oct')
                            or k.startswith('supply'))),
}
# the symbols each feature owns: after stripping, a page that lacks the feature must not
#   mention any of them -- a mechanical check that the trim was complete.  #coil is the coil
#   DRAWING (shared by the electromagnet and the generator's pickup coil); #emag is the
#   electromagnet itself -- its field, its supplies, its screen.
FEATURE_SYMBOLS = {
    'coil': ['drawCoilHalf', 'drawElectrons', 'COIL_TILT', 'loopPts'],
    'emag': ['coilRU', 'coilPsi', 'coilLoopsX', 'coilField', 'coilGaussPerUnit', 'coilDip', 'I_MAX', 'supplyCurrent',
             'supplyVoltage', 'acFreq', 'emCoil', 'COIL_A', 'COIL_PITCH', 'WIRE_R', 'inWire', 'drawBattery',
             'drawACSupply', 'loopB', 'loopAxis', 'DC_VMAX', 'AC_VMAX', 'emSupply', 'hitCoil', 'drawEMScreen',
             'electronSpeed', 'COIL_NMAX', 'COIL_LINES', 'projectPsi', 'emParts', 'axisCoilPoint'],
    'bar': ['drawBarScreen', 'hitMagnet'],
    'far': ['drawFarView', 'farCurves', 'farGeo', 'FAR_CAP', 'FAR_SRC', 'farField', 'dipPred', 'farRatio',
            'richardson', 'dipoleLimit', 'octCoef', 'octMeasured', 'testFar'],
    'gen': ['drawBulb', 'drawVoltmeter', 'fluxSeries', 'flux1', 'fluxPhet1', 'genReadings', 'pickRadius', 'E_FULL',
            'TURB_X', 'PICK_X', 'seriesPhi', 'seriesDPhi'],
}


def strip_feats(text, keep, where):
    """remove /* #feat */ ... /* #endfeat */ blocks whose feature this page does not carry"""
    for feat in FEATURE_SYMBOLS:
        if feat in keep:
            continue
        a, b = '/* #%s */' % feat, '/* #end%s */' % feat
        n = text.count(a)
        assert n == text.count(b), 'unbalanced #%s markers in %s (%d vs %d)' % (feat, where, n, text.count(b))
        while a in text:
            i = text.index(a)
            j = text.index(b, i) + len(b)
            text = text[:i] + text[j:]
    return text


def extract_house():
    """p1_utils.js and p4_helpers.js, verbatim from build_buoy (the newest house layer carrying the
    Known-bad fixes), every function we use asserted present."""
    u = io.open(os.path.join(SIM, 'build_buoy', 'p1_utils.js'), encoding='utf-8').read()
    for fn in ['function toRgb(', 'function mix(', 'function rgba(', 'function shade(', 'function neon(', 'function h(',
               'function fmt(', 'function sigf(', 'const ENTS=', 'function plain(', 'function wrapText(', 'function caption(',
               'function box(', 'function frame(', 'function ticksFor(', 'function logTicks(', 'function axes(',
               'function polyline(', 'function legendBox(', 'function legendAuto(', 'function fitCaption(', 'function stageTop(']:
        assert u.count(fn) == 1, fn
    io.open(os.path.join(HERE, 'p1_utils.js'), 'w', encoding='utf-8').write(u)
    src = io.open(os.path.join(SIM, 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
    k = src.index('/* the fluid: a translucent slab')
    out = src[:k].rstrip('\n') + '\n'
    out = out.replace(' *  — extracted from build_cycloid/p4_views.js, unchanged              *',
                      ' *  — verbatim from build_buoy/p4_views.js (build_cycloid lineage)     *')
    for fn in ['const CAP_FONT=', 'const LAB_FONT=', 'const SM_FONT=', 'function isNarrow(', 'const DRAG=', 'function worldFitUp(',
               'function worldPoly(', 'function seg(', 'function circleW(', 'function dot(', 'function arrowW(', 'let LABELS=',
               'function labFits(', 'function lab(', 'function titleFor(', 'function axesR(', 'function stageLayout(',
               'function drawCaption(', 'function marker(']:
        assert out.count(fn) == 1, fn
    assert 'fluidRect' not in out
    io.open(os.path.join(HERE, 'p4_helpers.js'), 'w', encoding='utf-8').write(out)


def make_head(stem, cfg, sdir):
    s = io.open(os.path.join(SIM, 'build_buoy', 'p1_head.html'), encoding='utf-8').read()

    def rep(old, new):
        nonlocal s
        assert s.count(old) == 1, (old[:60], s.count(old))
        s = s.replace(old, new)
    rep('<title>Buoyancy &mdash; Archimedes&rsquo; principle, from the spring scale to the metacentre</title>',
        '<title>%s</title>' % cfg['title'])
    i = s.index('<!--')
    j = s.index('-->', i) + 3
    header = io.open(os.path.join(sdir, 'header_comment.txt'), encoding='utf-8').read().rstrip('\n')
    assert '-->' not in header and '--!>' not in header, 'the header would end the HTML comment early'
    s = s[:i] + '<!--\n' + header + '\n-->' + s[j:]
    rep("""    /* role colours: green = the quantity computed (the upthrust, the submerged
       polygon), orange = the reference/analytic value or a warning,
       magenta = the live marker (the centre of buoyancy, the live state),
       cyan = structure (the fluid, the waterline, the vessel). */
    --pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --wplus:#5ac8e0; --wminus:#e8843a;""", ACCENTS)
    for a, b in [('../website/index.html', 'index.html'), ('../website/about.html', 'about.html'),
                 ('../website/teaching.html', 'teaching.html'), ('../modules/teaching_modules.html', 'modules/teaching_modules.html'),
                 ('../website/research.html', 'research.html'), ('../website/cv.html', 'cv.html')]:
        rep('<a href="%s">' % a, '<a href="https://cooper-watson.net/%s">' % b)
    rep('<a href="../website/simulations.html" aria-current="page">',
        '<a href="https://cooper-watson.net/simulations.html" aria-current="page">')
    rep('/* injected site header — palette & tabs match ../website/style.css */',
        '/* injected site header — palette & tabs match the site stylesheet (links absolute: this page lives outside the site tree) */')
    rep('<h1>Buoyancy</h1>', '<h1>%s</h1>' % cfg['h1'])
    i = s.index('<span class="sub" id="sub">')
    j = s.index('</span>', i) + len('</span>')
    s = s[:i] + '<span class="sub" id="sub">%s</span>' % cfg['sub'] + s[j:]
    assert '../website/' not in s and '../modules/' not in s
    io.open(os.path.join(sdir, 'p1_head.html'), 'w', encoding='utf-8').write(s)


def make_refs(stem, cfg, sdir):
    lines = io.open(os.path.join(HERE, 'refvals.txt'), encoding='utf-8').read().splitlines()
    R = {}
    for ln in lines:
        if not ln.strip() or ln.startswith('#'):
            continue
        assert ln.startswith('REF '), 'refvals.txt: unexpected line %r' % ln[:60]
        key, _, vals = ln[4:].partition(' = ')
        key = key.strip()
        assert key and vals, 'refvals.txt: malformed %r' % ln[:60]
        assert key not in R, 'duplicate REF key ' + key
        v = [float(x) for x in vals.split()]
        if cfg['refs'](key):
            R[key] = v[0] if len(v) == 1 else v
    out = ('\n/* ================================================================== *\n'
           ' *  REF: derive.py\'s printed reference values (refvals.txt), emitted  *\n'
           ' *  as literals by family.py -- never retyped                        *\n'
           ' * ================================================================== */\n'
           'const REF=' + json.dumps(R, separators=(',', ':')) + ';\n')
    io.open(os.path.join(sdir, 'p7a_refs.js'), 'w', encoding='utf-8').write(out)
    return len(R)


def assemble(stem):
    cfg = STEMS[stem]
    sdir = os.path.join(BUILD, stem)
    make_head(stem, cfg, sdir)
    n = make_refs(stem, cfg, sdir)
    html = ''
    for p in cfg['parts']:
        path = os.path.join(sdir, p[1:]) if p.startswith('@') else os.path.join(HERE, p)
        html += strip_feats(io.open(path, encoding='utf-8').read(), cfg['feats'], p)
    html += '</script>\n</body>\n</html>\n'
    for feat, syms in FEATURE_SYMBOLS.items():
        if feat in cfg['feats']:
            continue
        left = [sym for sym in syms if sym in html]
        assert not left, '%s carries no %s, yet the page still mentions %s' % (stem, feat, ', '.join(left))
    out_html = os.path.join(OUTDIR, stem + '.html')
    io.open(out_html, 'w', encoding='utf-8').write(html)
    js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
    os.makedirs(os.path.join(sdir, '_out'), exist_ok=True)
    io.open(os.path.join(sdir, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
    io.open(os.path.join(sdir, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
    print('%-28s %5d lines, %6.1f KB, %d REF keys' % (stem + '.html', len(html.splitlines()), len(html.encode()) / 1024, n))


if __name__ == '__main__':
    extract_house()
    for stem in (sys.argv[1:] or list(STEMS)):
        assemble(stem)
