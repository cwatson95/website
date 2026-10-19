#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/sound-waves.html and extract
_out/run.js (osascript) and _out/run_jsc.js (jsc, which has no console.log).

Four parts are COPIES of build/wave-interference/ files, taken verbatim when this build
started (the house utilities, the 2-D drawing layer, the selfTest recording context) plus
p2_engine.js, which is that build's lattice engine WITH the two changes named in its own
header (a 231-cell lattice and a new run layer for Sound Waves).  They are copies and not
references on purpose: build/waves-intro/assemble.py pins those files by SHA-256, so nothing
here may touch them.  The three that are unchanged are checked against that pin on every
assembly, in both directions."""
import hashlib
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WI = os.path.join(HERE, '..', 'wave-interference')
OUT = os.path.dirname(os.path.dirname(HERE))                # docs/phets_revised
UNCHANGED = {                                               # must equal wave-interference's
    'p1_utils.js': 'bff73f3eb6aa92c4485808f7b5ee4f8da0973353ecb44c137ec945ac4741ae96',
    'p4_helpers.js': '863bca754db41b8237306153edf4dba8dd4f9a97af41a96443d7d960a315c7dc',
    'p7_shot.js': 'e10d16351fd35beecf22f7fb39bc6890019353178034f0336d8aff4c865f8262',
}
PARTS = ['p1_head.html', 'p1_utils.js', 'p2_engine.js', 'p2_sound.js', 'p3_state.js',
         'p4_helpers.js', 'p4_draw.js', 'p4_views.js', 'p6_boot.js', 'p7_refs.js',
         'p7_shot.js', 'p7_test.js']


def sha(path):
    return hashlib.sha256(io.open(path, encoding='utf-8').read().encode('utf-8')).hexdigest()


for fn, want in UNCHANGED.items():
    mine = sha(os.path.join(HERE, fn))
    theirs = sha(os.path.join(WI, fn))
    assert mine == want, '%s has been edited here (%s)' % (fn, mine)
    assert theirs == want, 'build/wave-interference/%s has changed upstream (%s)' % (fn, theirs)

html = ''.join(io.open(os.path.join(HERE, fn), encoding='utf-8').read() for fn in PARTS)
html += '</script>\n</body>\n</html>\n'
io.open(os.path.join(OUT, 'sound-waves.html'), 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(HERE, '_out'), exist_ok=True)
io.open(os.path.join(HERE, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(HERE, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write(
    'var console={log:print};\n' + js)
print('sound-waves.html: %d lines, %.1f KB; run.js: %d lines' %
      (len(html.splitlines()), len(html.encode('utf-8')) / 1024, len(js.splitlines())))
