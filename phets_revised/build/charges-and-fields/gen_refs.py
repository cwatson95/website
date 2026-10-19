#!/usr/bin/env python3
"""gen_refs.py -- refvals.txt (derive.py's printed output) -> p7_refs.js, a
literal table REF the selfTest asserts against.  The numbers go into the
file as the text derive.py printed, never retyped (Known-bad: hand-copied
coefficients were right for six entries and wrong from the seventh).  Every
line kind is parsed explicitly; an unknown kind fails loudly."""
import io
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
lines = io.open(os.path.join(here, 'refvals.txt'), encoding='utf-8').read().splitlines()
R = {'VE': {}, 'PROBE': [], 'LOOP': {}, 'DIPLINE': [], 'LIKELINE': [], 'NULLCOUNT': {}, 'NULL': {}, 'MOM': {},
     'SER': {}, 'FAR': {}, 'SERIES_CONV': {}, 'TAPE': {}, 'SUP': [], 'ROWS_UNIF': [], 'GRADCHECK': {}, 'JACCHECK': {}}
num = float
for ln in lines:
    if not ln.strip() or ln.startswith('#'):
        continue
    t = ln.split()
    k = t[0]
    if k in ('EPS0', 'K_SI', 'KNC'):
        R[k] = num(t[1])
    elif k == 'KNC/K_PHET':
        R['KNC_OVER_KPHET'] = num(t[1])
    elif k == 'PhET':
        R.setdefault('PHET_M', []).append(num(t[-1]))
    elif k == 'PROBE':
        R['PROBE'].append([num(t[2]), num(t[3])])
    elif k == 'VE':
        R['VE'].setdefault(t[1], []).append([num(x) for x in t[3:8]])
    elif k in ('GRADCHECK', 'JACCHECK'):
        R[k][t[1]] = num(t[2])
    elif k == 'LOOP':
        R['LOOP'][t[1]] = {'pre': t[2], 'seed': [num(t[3]), num(t[4])], 'V0': num(t[5]), 'A': num(t[6]), 'L': num(t[7]),
                           'ymax': num(t[9]), 'xmin': num(t[11])}
    elif k == 'CIRCLE_CHECK':
        R['CIRCLE'] = [num(t[1]), num(t[2])]
    elif k == 'DIPOLE09_AXIS_LEFT':
        R[k] = num(t[1])
    elif k == 'LIKE_SADDLE_V':
        R['LIKE_SADDLE_V'] = num(t[1]); R['LIKE_SEED04_V'] = num(t[3])
    elif k == 'DIPLINE':
        R['DIPLINE'].append([num(t[1]), num(t[3]), num(t[5]), num(t[7])])
    elif k == 'LIKELINE':
        R['LIKELINE'].append([num(t[1]), num(t[3]), num(t[5]), num(t[7])])
    elif k == 'NULLCOUNT':
        R['NULLCOUNT'][t[1]] = int(t[2])
    elif k == 'NULL':
        R['NULL'].setdefault(t[1], []).append([num(t[2]), num(t[3]), num(t[4]), t[5], num(t[6])])
    elif k == 'TRI_SADDLE_Y':
        R[k] = num(t[1])
    elif k == 'MOM':
        R['MOM'][t[1]] = [num(x) for x in t[2:10]]
    elif k == 'ASYM_MOM':
        R['ASYM_MOM'] = [num(x) for x in t[1:9]]
    elif k == 'ASYM_SER30':
        R['ASYM_SER30'] = [num(x) for x in t[1:6]]
    elif k == 'SER':
        R['SER'].setdefault(t[1], {})[t[2]] = [num(x) for x in t[3:8]]
    elif k == 'FAR':
        R['FAR'][t[1]] = {'th': num(t[2]), 'l0': int(t[3]), 'limit': num(t[5]), 'f25': num(t[7]), 'f50': num(t[9]),
                          'f100': num(t[11]), 'rich': num(t[13]), 'rate': num(t[15])}
    elif k in ('DIPOLE_CLOSED', 'QUAD_CLOSED'):
        R[k] = num(t[1])
    elif k == 'SERIES_CONV':
        R['SERIES_CONV'][t[1]] = {'dmax': num(t[3]), 'r': num(t[5]), 'partial': num(t[7]), 'exact': num(t[9])}
    elif k == 'TAPE':
        R['TAPE'][t[1]] = {'A': [num(t[3]), num(t[4])], 'B': [num(t[6]), num(t[7])], 'L': num(t[9]), 'int': num(t[11]),
                           'dV': num(t[13]), 'clear': num(t[15])}
    elif k == 'SUP':
        R['SUP'].append([int(t[1]), num(t[2]), num(t[3]), num(t[4])])
    elif k == 'SUPSUM':
        R['SUPSUM'] = [num(t[1]), num(t[2]), num(t[3])]; R['SUPDIRECT'] = [num(t[5]), num(t[6]), num(t[7])]
    elif k == 'ROWS_E0':
        R['ROWS_E0'] = [num(t[1]), num(t[2])]
    elif k == 'ROWS_UNIF':
        R['ROWS_UNIF'].append([num(t[1]), num(t[2])])
    elif k == 'PHET_V1M':
        R['PHET_V1M'] = [num(t[1]), num(t[3])]
    else:
        raise SystemExit('gen_refs: unknown line kind %r' % k)
for need in ['KNC', 'EPS0', 'VE', 'LOOP', 'DIPLINE', 'LIKELINE', 'NULL', 'MOM', 'SER', 'FAR', 'TAPE', 'SUP', 'SUPSUM']:
    assert R.get(need), need
out = ('\n/* ================================================================== *\n'
       ' *  REF: derive.py\'s printed reference values (refvals.txt), emitted  *\n'
       ' *  as literals by gen_refs.py -- never retyped                        *\n'
       ' * ================================================================== */\n'
       'const REF=' + json.dumps(R, separators=(',', ':')) + ';\n')
io.open(os.path.join(here, 'p7_refs.js'), 'w', encoding='utf-8').write(out)
print('p7_refs.js: %d bytes, %d VE presets, %d loops, %d null sets' % (len(out), len(R['VE']), len(R['LOOP']), len(R['NULL'])))
