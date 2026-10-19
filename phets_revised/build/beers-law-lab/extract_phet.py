#!/usr/bin/env python3
"""Read PhET's own numbers out of the minified original docs/phets/beers-law-lab_en.html
(1.8.7) and write them to phet_values.json.  Nothing here is typed by hand: every solute,
every molar-absorptivity spectrum and every constant is parsed from the shipped build, so a
value in the sim can be traced to a byte range of the file it was read from.

Run:  python3 extract_phet.py
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'phets', 'beers-law-lab_en.html'))

s = io.open(ORIG, encoding='utf-8', errors='replace').read()

out = {'source': 'docs/phets/beers-law-lab_en.html', 'version': None}

m = re.search(r'"beers-law-lab"\s*:\s*"([\d.]+)"', s)
out['version'] = m.group(1) if m else '1.8.7'

# ---------------------------------------------------------------- constants
def grab(pat, cast=float):
    mm = re.search(pat, s)
    assert mm, 'not found: ' + pat
    return cast(mm.group(1))

out['BEAKER_VOLUME'] = grab(r'\.BEAKER_VOLUME=([\d.]+)')
mm = re.search(r'\.SOLUTE_AMOUNT_RANGE=new \w+\(([\d.]+),([\d.]+),([\d.]+)\)', s)
out['SOLUTE_AMOUNT_RANGE'] = [float(mm.group(i)) for i in (1, 2, 3)]
mm = re.search(r'\.SOLUTION_VOLUME_RANGE=new \w+\(([\d.]+),\w+\.BEAKER_VOLUME,([\d.]+)\)', s)
out['SOLUTION_VOLUME_RANGE'] = [float(mm.group(1)), out['BEAKER_VOLUME'], float(mm.group(2))]
mm = re.search(r'\.CUVETTE_WIDTH_RANGE=new \w+\(([\d.]+),([\d.]+),([\d.]+)\)', s)
out['CUVETTE_WIDTH_RANGE'] = [float(mm.group(i)) for i in (1, 2, 3)]
out['CUVETTE_SNAP_DEFAULT'] = grab(r'cuvetteSnapInterval:\{type:"number",defaultValue:([\d.]+)')
out['MIN_WAVELENGTH'] = grab(r'MIN_WAVELENGTH:(\d+)', int)
out['MAX_WAVELENGTH'] = grab(r'MAX_WAVELENGTH:(\d+)', int)
for key, pat in [('DECIMALS_CONC_MOL_PER_L', r'DECIMAL_PLACES_CONCENTRATION_MOLES_PER_LITER=(\d+)'),
                 ('DECIMALS_CONC_PERCENT', r'DECIMAL_PLACES_CONCENTRATION_PERCENT=(\d+)'),
                 ('DECIMALS_CONC_MOLAR', r'DECIMAL_PLACES_CONCENTRATION_MOLAR=(\d+)'),
                 ('DECIMALS_ABSORBANCE', r'DECIMAL_PLACES_ABSORBANCE=(\d+)'),
                 ('DECIMALS_TRANSMITTANCE', r'DECIMAL_PLACES_TRANSMITTANCE=(\d+)'),
                 ('DECIMALS_WAVELENGTH', r'DECIMAL_PLACES_WAVELENGTH=(\d+)'),
                 ('DECIMALS_SOLUTE_AMOUNT', r'DECIMAL_PLACES_SOLUTE_AMOUNT=(\d+)'),
                 ('DECIMALS_CUVETTE_WIDTH', r'DECIMAL_PLACES_CUVETTE_WIDTH=(\d+)'),
                 ('DECIMALS_VOLUME_LITERS', r'DECIMAL_PLACES_VOLUME_LITERS=(\d+)')]:
    out[key] = grab(r'\.' + pat, int)

# rates: dropper maxFlowRate, faucet maxFlowRate, evaporator maxEvaporationRate, shaker rate
out['DROPPER_FLOW'] = grab(r'dropper=new \w+\(this\.soluteProperty,this\.soluteFormProperty,'
                           r'\{position:new \w+\.\w+\([\d.]+,[\d.]+\),maxFlowRate:([\d.]+)')
out['FAUCET_FLOW'] = grab(r'pipeMinX:-100,spoutWidth:\d+,maxFlowRate:([\d.]+)')
out['EVAPORATION_MAX'] = grab(r'maxEvaporationRate:([\d.]+)')
out['SHAKER_RATE'] = grab(r'orientation:[\d.]*\*?Math\.PI,maxDispensingRate:([\d.]+)')
out['PARTICLES_PER_MOLE'] = grab(r'particlesPerMole:(\d+)', int)
out['PARTICLE_SIZE'] = grab(r'particleSize:(\d+)', int)
mm = re.search(r'\.WATER=new \w+\(224,255,255\)', s)
assert mm, 'water colour'
out['WATER_RGB'] = [224, 255, 255]
out['WATER_DENSITY'] = grab(r'WATER=new \w+\("water","H<sub>2</sub>O",(\de\d),')

# ---------------------------------------------------------------- the nine solutes
RGB = r'new \w+\((\d+),(\d+),(\d+)\)'
SOL = re.compile(
    r'\.([A-Z_0-9]+)=new \w+\(\{nameProperty:\w+\.(\w+)StringProperty,'
    r'(?:formula:"([^"]*)",)?'
    r'stockSolutionConcentration:([\d.]+),molarMass:([\d.]+),'
    r'colorScheme:new \w+\(([\d.]+),(?:\w+\.WATER\.colorProperty\.value|' + RGB + r'),'
    r'([\d.]+),' + RGB + r',([\d.]+),' + RGB + r'\)')
solutes = []
for m in SOL.finditer(s):
    g = m.groups()
    minc = [224, 255, 255] if g[6] is None else [int(g[6]), int(g[7]), int(g[8])]
    solutes.append({
        'const': g[0], 'nameKey': g[1], 'formula': g[2],
        'stock': float(g[3]), 'molarMass': float(g[4]),
        'minConcentration': float(g[5]), 'minColor': minc,
        'midConcentration': float(g[9]), 'midColor': [int(g[10]), int(g[11]), int(g[12])],
        'maxConcentration': float(g[13]), 'maxColor': [int(g[14]), int(g[15]), int(g[16])],
    })
assert len(solutes) == 9, len(solutes)
out['solutes'] = solutes

# ---------------------------------------------------------------- the eight Beer's Law solutions
BLS = re.compile(
    r'\.([A-Z_0-9]+)=new \w+\(\{nameProperty:\w+\.([A-Z_0-9]+)\.nameProperty,'
    r'formulaProperty:\w+\.[A-Z_0-9]+\.formulaProperty,'
    r'molarAbsorptivityData:\w+\.([A-Z_0-9]+),'
    r'concentrationRange:new \w+\(([\d.e-]+),([\d.e-]+),([\d.e-]+)\),'
    r'concentrationTransform:\w+\.(mM|uM),'
    r'colorRange:new \w+\(' + RGB + r',(?:\w+\.RED|' + RGB + r')\)'
    r'(?:,saturatedColor:' + RGB + r')?')
bls = []
for m in BLS.finditer(s):
    # groups: 0 const, 1 solute, 2 data, 3-5 range, 6 transform, 7-9 colorLo,
    #         10-12 colorHi (None => Color.RED), 13-15 saturatedColor (optional)
    g = m.groups()
    hi = [255, 0, 0] if g[10] is None else [int(g[10]), int(g[11]), int(g[12])]
    bls.append({'const': g[0], 'solute': g[1], 'data': g[2],
                'cMin': float(g[3]), 'cMax': float(g[4]), 'cDefault': float(g[5]),
                'transform': g[6],
                'colorLo': [int(g[7]), int(g[8]), int(g[9])],
                'colorHi': hi,
                'saturatedColor': None if g[13] is None else [int(g[13]), int(g[14]), int(g[15])]})
assert len(bls) == 8, len(bls)
out['beersLawSolutions'] = bls

# ---------------------------------------------------------------- the eight spectra
i = s.index('.DRINK_MIX=new ', s.index('getLambdaMax'))
blk = s[i - 40:i + 40000]
eps = {}
for m in re.finditer(r'\.([A-Z_0-9]+)=new \w+\(\[([-\d.,e]+)\]\)', blk):
    name = m.group(1)
    arr = [float(x) for x in m.group(2).split(',')]
    if len(arr) == 401:
        eps[name] = arr
assert len(eps) == 8, sorted(eps)
out['molarAbsorptivity'] = eps
out['lambdaMax'] = {k: out['MIN_WAVELENGTH'] + v.index(max(v)) for k, v in eps.items()}

io.open(os.path.join(HERE, 'phet_values.json'), 'w', encoding='utf-8').write(
    json.dumps(out, indent=1, sort_keys=True))
print('version', out['version'])
print('solutes:')
for d in solutes:
    print('  %-24s %-22s stock %-5s M  M=%-8s  sat %-5s M  colours %s %s(%s) %s(%s)' % (
        d['const'], d['formula'], d['stock'], d['molarMass'], d['maxConcentration'],
        d['minColor'], d['midColor'], d['midConcentration'], d['maxColor'], d['maxConcentration']))
print("Beer's Law solutions:")
for d in bls:
    print('  %-24s c 0..%-8s default %-8s %s  lo %s hi %s sat %s' % (
        d['const'], d['cMax'], d['cDefault'], d['transform'], d['colorLo'], d['colorHi'],
        d['saturatedColor']))
print('lambda_max (nm) and eps at it:')
for k in eps:
    lm = out['lambdaMax'][k]
    print('  %-24s %4d nm   eps = %-10s  eps(380) = %-10s eps(780) = %s' % (
        k, lm, max(eps[k]), eps[k][0], eps[k][-1]))
print('constants:', {k: v for k, v in out.items()
                     if k not in ('solutes', 'beersLawSolutions', 'molarAbsorptivity',
                                  'lambdaMax', 'source')})
