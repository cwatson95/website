#!/usr/bin/env python3
"""Write p2_data.js: PhET's nine solutes, its eight Beer's Law solutions, its eight
molar-absorptivity spectra, and the CIE 1931 2-degree colour-matching functions.

Every number is copied from phet_values.json (which extract_phet.py read out of the
minified original) or from the CIE's own published table; none is typed by hand.  The
literature column is the only hand-entered block, and each row carries its source.
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PV = json.load(io.open(os.path.join(HERE, 'phet_values.json'), encoding='utf-8'))
CIE_CSV = os.path.abspath(os.path.join(HERE, '..', 'blackbody-spectrum', 'CIE_xyz_1931_2deg.csv'))

LAM0, LAM1 = PV['MIN_WAVELENGTH'], PV['MAX_WAVELENGTH']
NLAM = LAM1 - LAM0 + 1

NAME = {
    'DRINK_MIX': ('drinkMix', 'drink mix', None),
    'COBALT_II_NITRATE': ('cobaltIINitrate', 'cobalt(II) nitrate', 'Co(NO3)2'),
    'COBALT_CHLORIDE': ('cobaltChloride', 'cobalt(II) chloride', 'CoCl2'),
    'POTASSIUM_DICHROMATE': ('potassiumDichromate', 'potassium dichromate', 'K2Cr2O7'),
    'POTASSIUM_CHROMATE': ('potassiumChromate', 'potassium chromate', 'K2CrO4'),
    'NICKEL_II_CHLORIDE': ('nickelIIChloride', 'nickel(II) chloride', 'NiCl2'),
    'COPPER_SULFATE': ('copperSulfate', 'copper(II) sulfate', 'CuSO4'),
    'POTASSIUM_PERMANGANATE': ('potassiumPermanganate', 'potassium permanganate', 'KMnO4'),
    'SODIUM_CHLORIDE': ('sodiumChloride', 'sodium chloride', 'NaCl'),
}
# HTML formulas with real subscripts, for the panel and the readout (the canvas gets the
# ASCII form above: plain() strips tags, and a letter subscript is tofu in the rasteriser)
HTML = {
    'COBALT_II_NITRATE': 'Co(NO<sub>3</sub>)<sub>2</sub>',
    'COBALT_CHLORIDE': 'CoCl<sub>2</sub>',
    'POTASSIUM_DICHROMATE': 'K<sub>2</sub>Cr<sub>2</sub>O<sub>7</sub>',
    'POTASSIUM_CHROMATE': 'K<sub>2</sub>CrO<sub>4</sub>',
    'NICKEL_II_CHLORIDE': 'NiCl<sub>2</sub>',
    'COPPER_SULFATE': 'CuSO<sub>4</sub>',
    'POTASSIUM_PERMANGANATE': 'KMnO<sub>4</sub>',
    'SODIUM_CHLORIDE': 'NaCl',
}
# literature, fetched from the Wikipedia chemical infoboxes on 2026-09-22 and quoted to the
# precision printed there: (molar mass g/mol, solubility, unit, temperature, note)
LIT = {
    'DRINK_MIX': (342.297, 2.01, 'g/mL', '20 &deg;C', 'sucrose &mdash; PhET&rsquo;s molar mass is sucrose&rsquo;s'),
    'COBALT_II_NITRATE': (182.943, 84.03, 'g/100 mL', '0 &deg;C', 'anhydrous; the only temperature the infobox gives below 90 &deg;C'),
    'COBALT_CHLORIDE': (129.839, 52.9, 'g/100 mL', '20 &deg;C', 'anhydrous'),
    'POTASSIUM_DICHROMATE': (294.182, 15.1, 'g/100 g', 'no temperature given', ''),
    'POTASSIUM_CHROMATE': (194.189, 65.0, 'g/100 mL', 'no temperature given', ''),
    'NICKEL_II_CHLORIDE': (129.5994, 67.5, 'g/100 mL', '25 &deg;C', 'anhydrous'),
    'COPPER_SULFATE': (159.60, 201.0, 'g/L', '20 &deg;C', 'anhydrous'),
    'POTASSIUM_PERMANGANATE': (158.032, 76.0, 'g/L', '25 &deg;C', ''),
    'SODIUM_CHLORIDE': (58.44, 360.0, 'g/L', '25 &deg;C', ''),
}
UNIT_GPL = {'g/mL': 1000.0, 'g/100 mL': 10.0, 'g/100 g': 10.0, 'g/L': 1.0}


def num(x):
    """shortest round-tripping spelling"""
    s = repr(float(x))
    return s[:-2] if s.endswith('.0') else s


def arr(vals, per=20, ind='  '):
    out, row = [], []
    for v in vals:
        row.append(num(v))
        if len(row) == per:
            out.append(ind + ','.join(row))
            row = []
    if row:
        out.append(ind + ','.join(row))
    return '[\n' + ',\n'.join(out) + ']'


L = []
L.append('''
/* ================================================================== *
 *  PhET's data.  Every number below was read out of the minified      *
 *  original docs/phets/beers-law-lab_en.html %s by                 *
 *  build/beers-law-lab/extract_phet.py, and written here by           *
 *  make_data.py -- nothing was typed by hand.  The CIE block is the   *
 *  CIE's own published table.                                         *
 * ================================================================== */
const PHET_VERSION=%s;
const LAM0=%d, LAM1=%d, NLAM=%d;                   /* PhET's visible band, 1 nm samples */
const PHET={
  BEAKER_VOLUME:%s,                    /* L */
  SOLUTE_MOL_MIN:%s, SOLUTE_MOL_MAX:%s, SOLUTE_MOL_DEFAULT:%s,
  VOL_MIN:%s, VOL_MAX:%s, VOL_DEFAULT:%s,
  CUVETTE_MIN:%s, CUVETTE_MAX:%s, CUVETTE_DEFAULT:%s, CUVETTE_SNAP:%s,
  DROPPER_FLOW:%s, FAUCET_FLOW:%s, EVAPORATION_MAX:%s, SHAKER_RATE:%s,
  PARTICLES_PER_MOLE:%d, PARTICLE_SIZE:%d, WATER_DENSITY:%s,
  DEC_CONC:%d, DEC_PERCENT:%d, DEC_MOLAR:%d, DEC_A:%d, DEC_T:%d,
  DEC_LAMBDA:%d, DEC_AMOUNT:%d, DEC_CUVETTE:%d, DEC_VOLUME:%d
};
const WATER_RGB=[%d,%d,%d];
''' % (PV['version'], json.dumps(PV['version']), LAM0, LAM1, NLAM,
       num(PV['BEAKER_VOLUME']),
       num(PV['SOLUTE_AMOUNT_RANGE'][0]), num(PV['SOLUTE_AMOUNT_RANGE'][1]),
       num(PV['SOLUTE_AMOUNT_RANGE'][2]),
       num(PV['SOLUTION_VOLUME_RANGE'][0]), num(PV['SOLUTION_VOLUME_RANGE'][1]),
       num(PV['SOLUTION_VOLUME_RANGE'][2]),
       num(PV['CUVETTE_WIDTH_RANGE'][0]), num(PV['CUVETTE_WIDTH_RANGE'][1]),
       num(PV['CUVETTE_WIDTH_RANGE'][2]), num(PV['CUVETTE_SNAP_DEFAULT']),
       num(PV['DROPPER_FLOW']), num(PV['FAUCET_FLOW']), num(PV['EVAPORATION_MAX']),
       num(PV['SHAKER_RATE']), PV['PARTICLES_PER_MOLE'], PV['PARTICLE_SIZE'],
       num(PV['WATER_DENSITY']),
       PV['DECIMALS_CONC_MOL_PER_L'], PV['DECIMALS_CONC_PERCENT'], PV['DECIMALS_CONC_MOLAR'],
       PV['DECIMALS_ABSORBANCE'], PV['DECIMALS_TRANSMITTANCE'], PV['DECIMALS_WAVELENGTH'],
       PV['DECIMALS_SOLUTE_AMOUNT'], PV['DECIMALS_CUVETTE_WIDTH'], PV['DECIMALS_VOLUME_LITERS'],
       PV['WATER_RGB'][0], PV['WATER_RGB'][1], PV['WATER_RGB'][2]))

# ---- the spectra ----
L.append('\n/* molar absorptivity, 1/(cm M), one value per nanometre from %d to %d nm.\n'
         '   PhET\'s own digitised spectra; no literature values for these could be sourced\n'
         '   offline, so they stand as PhET\'s data and the file says so. */\n'
         'const EPS={' % (LAM0, LAM1))
for const in [d['const'] for d in PV['beersLawSolutions']]:
    L.append('%s:%s,' % (NAME[const][0], arr(PV['molarAbsorptivity'][const], 20, '  ')))
L.append('};\n')

# ---- the solutes ----
rows = []
for d in PV['solutes']:
    c = d['const']
    key, label, ascii_f = NAME[c]
    M_lit, val, unit, temp, note = LIT[c]
    gpl = val * UNIT_GPL[unit]
    rows.append('  {id:%s,name:%s,formula:%s,html:%s,'
                'molarMass:%s,stock:%s,'
                'cMin:%s,minRGB:[%d,%d,%d],cMid:%s,midRGB:[%d,%d,%d],'
                'cSat:%s,maxRGB:[%d,%d,%d],'
                'lit:{M:%s,val:%s,unit:%s,temp:%s,note:%s,gPerL:%s}}'
                % (json.dumps(key), json.dumps(label),
                   json.dumps(ascii_f or label), json.dumps(HTML.get(c, label)),
                   num(d['molarMass']), num(d['stock']),
                   num(d['minConcentration']), d['minColor'][0], d['minColor'][1], d['minColor'][2],
                   num(d['midConcentration']), d['midColor'][0], d['midColor'][1], d['midColor'][2],
                   num(d['maxConcentration']), d['maxColor'][0], d['maxColor'][1], d['maxColor'][2],
                   num(M_lit), num(val), json.dumps(unit), json.dumps(temp), json.dumps(note),
                   num(gpl)))
L.append('/* the nine solutes of PhET\'s Concentration screen, in PhET\'s own order.\n'
         '   cSat is SoluteColorScheme.maxConcentration, which is what\n'
         '   Solute.getSaturatedConcentration() returns.  lit.* is the Wikipedia chemical\n'
         '   infobox, fetched 2026-09-22 and quoted to its own printed precision. */\n'
         'const SOLUTES=[\n' + ',\n'.join(rows) + '];\n')

# ---- the Beer's Law solutions ----
rows = []
for d in PV['beersLawSolutions']:
    c = d['const']
    key, label, ascii_f = NAME[c]
    sat = d['saturatedColor'] or d['colorHi']
    rows.append('  {id:%s,solute:%s,cMax:%s,cDefault:%s,transform:%s,scale:%s,'
                'loRGB:[%d,%d,%d],hiRGB:[%d,%d,%d],satRGB:[%d,%d,%d]}'
                % (json.dumps(key), json.dumps(key), num(d['cMax']), num(d['cDefault']),
                   json.dumps(d['transform'].replace('uM', 'µM')),
                   '1e3' if d['transform'] == 'mM' else '1e6',
                   d['colorLo'][0], d['colorLo'][1], d['colorLo'][2],
                   d['colorHi'][0], d['colorHi'][1], d['colorHi'][2],
                   sat[0], sat[1], sat[2]))
L.append('/* the eight solutions of PhET\'s Beer\'s Law screen (sodium chloride is not one:\n'
         '   it is colourless).  Each carries its own concentration range and display\n'
         '   transform, and a two-stop colour ramp that is NOT the Concentration screen\'s. */\n'
         'const BLSOLS=[\n' + ',\n'.join(rows) + '];\n')

# ---- CIE ----
cie = {}
for r in io.open(CIE_CSV, encoding='utf-8').read().splitlines():
    if not r.strip():
        continue
    p = r.split(',')
    cie[int(p[0])] = (float(p[1]), float(p[2]), float(p[3]))
XB = [cie[LAM0 + i][0] for i in range(NLAM)]
YB = [cie[LAM0 + i][1] for i in range(NLAM)]
ZB = [cie[LAM0 + i][2] for i in range(NLAM)]
L.append('''
/* CIE 1931 2-degree colour-matching functions, one row per nanometre from %d to %d --
   the SAME grid PhET's spectra live on, so the colour integral below interpolates
   nothing and resamples nothing.  Rows from CIE_xyz_1931_2deg.csv
   (DOI 10.25039/CIE.DS.xvudnb9b, ISO/CIE 11664-1:2019), the file
   build/blackbody-spectrum/ downloaded; written here by make_data.py. */
const CIE_X=%s;
const CIE_Y=%s;
const CIE_Z=%s;
''' % (LAM0, LAM1, arr(XB, 12), arr(YB, 12), arr(ZB, 12)))

L.append('/* PhET\'s own constant names, in file order -- the bridge between refvals.txt\'s\n'
         '   labels and the ids above, generated rather than typed */\n'
         'const SOLUTE_CONST=%s;\nconst BLS_CONST=%s;\n'
         % (json.dumps([d['const'] for d in PV['solutes']]),
            json.dumps([d['const'] for d in PV['beersLawSolutions']])))

js = '\n'.join(L)
io.open(os.path.join(HERE, 'p2_data.js'), 'w', encoding='utf-8').write(js)
print('p2_data.js: %d lines, %.1f KB' % (len(js.splitlines()), len(js.encode()) / 1024))
