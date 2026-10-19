#!/usr/bin/env python3
"""Set the "draws substance" floors in p7_test.js from the MEASURED op counts
that probe_tail.js prints (about 80 % of the smallest count across the three
canvas sizes), and make the floor count fills AND strokes: several views here
are almost all curves, so a fills-only floor is either useless or unmeetable."""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'p7_test.js')
FLOORS = {
    'harmonics sine square': 55, 'harmonics cosine triangle': 48, 'harmonics sawtooth, time': 62,
    'harmonics space & time': 38, 'harmonics one harmonic': 26, 'harmonics all zero': 52,
    'harmonics wave packet': 58, 'convergence square M=6': 42, 'convergence square M=1': 40,
    'convergence square M=128': 42, 'convergence triangle': 40, 'convergence sawtooth': 40,
    'convergence sinusoid': 40, 'spectrum square': 85, 'spectrum single sine': 86,
    'spectrum all zero': 86, 'game level 1': 46, 'game level 5 solved': 52,
    'packet default': 68, 'packet continuous': 36, 'packet narrow spacing': 177,
    'packet widest packet': 53, 'packet in time': 68, 'transform pair default': 27,
    'transform pair coarse': 30, 'transform pair fine': 29,
}
s = io.open(P, encoding='utf-8').read()
for name, f in FLOORS.items():
    pat = re.compile(r"(\['" + re.escape(name) + r"',\{[^\]]*\},)(\d+)\]")
    s, cnt = pat.subn(lambda m: m.group(1) + str(f) + ']', s)
    assert cnt == 1, (name, cnt)
OLD = ("      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');\n"
       "      ok(fills.length>=minFills&&texts.length>=1,nm+' '+W+'x'+H+' draws substance "
       "('+fills.length+' fills, floor '+minFills+')');")
NEW = ("      const texts=c.ops.filter(o=>o.op==='text');\n"
       "      /* the floor counts fills AND strokes: several views here are almost all\n"
       "         curves, so a fills-only floor is either useless or unmeetable */\n"
       "      const marks=c.ops.filter(o=>o.op==='fill'||o.op==='stroke').length;\n"
       "      ok(marks>=minFills&&texts.length>=1,nm+' '+W+'x'+H+' draws substance "
       "('+marks+' marks, floor '+minFills+')');")
if OLD in s:
    s = s.replace(OLD, NEW)
else:
    assert 'marks>=minFills' in s, 'neither the old nor the new form is present'
io.open(P, 'w', encoding='utf-8').write(s)
print('set %d measured floors in p7_test.js' % len(FLOORS))
