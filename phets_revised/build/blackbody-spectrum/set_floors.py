#!/usr/bin/env python3
"""Derive the layout sweep's substance floors from what each configuration actually emits (the SUB lines
of a diagnostic selfTest run, _out/diag.log): floor = 80 % of the minimum over the four canvas sizes of
[fills + strokes, curve segments, texts].  Writes them into CONFIGS as a fourth element."""
import io, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
mins = collections.defaultdict(lambda: [10**9] * 3)
for l in io.open(os.path.join(HERE, '_out', 'diag.log'), encoding='utf-8'):
    m = re.match(r'SUB (.+) (\d+)x(\d+) marks (\d+) segs ([\d.]+) texts (\d+)', l)
    if m:
        k = m.group(1)
        v = [int(m.group(4)), float(m.group(5)), int(m.group(6))]
        mins[k] = [min(a, b) for a, b in zip(mins[k], v)]
p = os.path.join(HERE, 'p7_test.js')
s = io.open(p, encoding='utf-8').read()
i = s.index('  const CONFIGS=['); j = s.index('];', i) + 2
block = s[i:j]
n = 0
def repl(m):
    global n
    name = m.group(1)
    f = [int(0.8 * x) for x in mins[name]]
    n += 1
    return "['%s',%s,%s,[%d,%d,%d]]" % (name, m.group(2), m.group(3), f[0], f[1], f[2])
# re-runnable: an entry may already carry a floor triple, which is replaced
block2 = re.sub(r"\['([^']+)',(\{[^}]*\}),(null|\[[0-9,]+\])(?:,\[\d+,\d+,\d+\])?\]", repl, block)
assert n == len(mins), (n, len(mins))
s = s[:i] + block2 + s[j:]
s = s.replace("for(const [nm,over,saved] of CONFIGS) for(const [W,H] of SIZES){ const minFills=FLOOR[over.view];",
              "for(const [nm,over,saved,minFills] of CONFIGS) for(const [W,H] of SIZES){")
if '  /* substance floors per view' in s:
    k0 = s.index('  /* substance floors per view'); k1 = s.index('\n', s.index('const FLOOR=')) + 1
    s = s[:k0] + ("  /* substance floors per configuration, [fills + strokes, curve segments, texts]: 80 % of the least that\n"
                  "     configuration emits at any of the four sizes (set_floors.py from a SUB diagnostic run) — derived,\n"
                  "     not copied; a view that legitimately draws little (a curve off the top of the axis) has a low floor */\n") + s[k1:]
io.open(p, 'w', encoding='utf-8').write(s)
print('floors written for %d configurations' % n)
for k, v in mins.items(): print('  %-24s %s' % (k, [int(0.8 * x) for x in v]))
