#!/usr/bin/env python3
"""Turn refvals.txt (derive.py's output, read in full) into p7_refs.js.

Every value the suite asserts against comes through this file, so a reference value can only
be one derive.py actually printed — never one recalled or typed by hand."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for line in io.open(os.path.join(HERE, 'refvals.txt'), encoding='utf-8').read().splitlines():
    if not line.strip():
        continue
    parts = line.split('\t')
    label, vals = parts[0], parts[1:]
    assert '"' not in label and '\\' not in label, label
    rows.append('  "%s":[%s]' % (label, ','.join(vals)))
js = ('\n/* ================================================================== *\n'
      ' *  reference values — every line of build/greenhouse-effect/refvals.txt,\n'
      ' *  which derive.py wrote.  Labels are verbatim; the suite looks them up by\n'
      ' *  name and fails loudly on a missing one (a typo must not pass silently). *\n'
      ' * ================================================================== */\n'
      'const REF={\n' + ',\n'.join(rows) + '\n};\n')
io.open(os.path.join(HERE, 'p7_refs.js'), 'w', encoding='utf-8').write(js)
print('p7_refs.js: %d reference lines' % len(rows))
