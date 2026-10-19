#!/usr/bin/env python3
"""Write mutants.json for beers-law-lab.html (and, with an argument, concentration.html).

Every leading coefficient, every exponent, every unit conversion, every sign and every
clamp in the chemistry, plus the UI mutants the house list calls for (the dirty flag on
each pointer path, each dragged axis frozen one at a time, the snap on release, a slider's
repaint, the frame loop's flag, and a panel group that stops hiding).

Each `old` is checked to appear EXACTLY once in the assembled script before it is written,
because mutate.py skips a pattern that matches twice and a skipped mutant is one you think
you ran and did not.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEM = sys.argv[1] if len(sys.argv) > 1 else 'beers-law-lab'
BDIR = os.path.join(HERE, '..', STEM)
HTML = os.path.abspath(os.path.join(HERE, '..', '..', STEM + '.html'))

BEERS = (STEM == 'beers-law-lab')

M = [
    # ---------------- Beer-Lambert ----------------
    ['A drops the path length', 'function absorbance(eps,l,c){ return eps*l*c; }',
     'function absorbance(eps,l,c){ return eps*c; }', 'p'],
    ['A doubled', 'function absorbance(eps,l,c){ return eps*l*c; }',
     'function absorbance(eps,l,c){ return 2*eps*l*c; }', 'p'],
    ['T: sign of the exponent', 'function transmittance(A){ return Math.pow(10,-A); }',
     'function transmittance(A){ return Math.pow(10,A); }', 'p'],
    ['T: base e, not ten', 'function transmittance(A){ return Math.pow(10,-A); }',
     'function transmittance(A){ return Math.exp(-A); }', 'p'],
    ['A from T: sign', 'function absorbanceOfT(T){ return -Math.log10(T); }',
     'function absorbanceOfT(T){ return Math.log10(T); }', 'p'],
    ['A from T: natural log', 'function absorbanceOfT(T){ return -Math.log10(T); }',
     'function absorbanceOfT(T){ return -Math.log(T); }', 'p'],
    # ---------------- the spectra ----------------
    ['eps rounds instead of flooring', '  const i=Math.floor(lam-LAM0);',
     '  const i=Math.round(lam-LAM0);', 'p'],
    ['eps reads the next cell', '  const i=Math.floor(lam-LAM0);',
     '  const i=Math.floor(lam-LAM0)+1;', 'p'],
    ['lambda_max takes the LAST maximum', '  for(let i=0;i<t.length;i++) if(t[i]>best){ best=t[i]; k=i; }',
     '  for(let i=0;i<t.length;i++) if(t[i]>=best){ best=t[i]; k=i; }', 'p'],
    ['lambda_max off by a nanometre', '  return LAM0+k;\n}\nfunction epsMaxOf(id)',
     '  return LAM0+k+1;\n}\nfunction epsMaxOf(id)', 'p'],
    # ---------------- the beaker ----------------
    ['precipitate forgets the volume', '  const z=B.n-B.V*csatOf(B.solute);',
     '  const z=B.n-csatOf(B.solute);', 'p'],
    ['concentration is not capped at saturation', '  return q>cs?cs:q;', '  return q;', 'p'],
    ['saturated the wrong way round',
     'function bkSaturated(B){ return B.V>0 && B.n/B.V>csatOf(B.solute); }',
     'function bkSaturated(B){ return B.V>0 && B.n/B.V<csatOf(B.solute); }', 'p'],
    ['the brim clamp is twice the beaker',
     '  const v0=B.V; B.V=Math.min(PHET.VOL_MAX,B.V+d); return B.V-v0;',
     '  const v0=B.V; B.V=Math.min(2*PHET.VOL_MAX,B.V+d); return B.V-v0;', 'p'],
    ['the empty clamp lets the volume go negative',
     '  const v0=B.V; B.V=Math.max(PHET.VOL_MIN,B.V-d); return v0-B.V;',
     '  const v0=B.V; B.V=B.V-d; return v0-B.V;', 'p'],
    ['the 7 mol ceiling is gone',
     '  const n0=B.n; B.n=Math.min(PHET.SOLUTE_MOL_MAX,B.n+d); return B.n-n0;',
     '  const n0=B.n; B.n=B.n+d; return B.n-n0;', 'p'],
    ['the drain takes solute at n/V, not at the dissolved C',
     '    const c=bkConc(B);\n    const got=bkRemoveSolvent(B,dOut);',
     '    const c=B.V>0?B.n/B.V:0;\n    const got=bkRemoveSolvent(B,dOut);', 'p'],
    ['the drain uses the asked-for volume, not the moved one',
     '    B.led.drained+=bkRemoveSolute(B,c*got);',
     '    B.led.drained+=bkRemoveSolute(B,c*dOut);', 'p'],
    ['the dropper carries the saturation, not the stock',
     '    B.led.dropper+=bkAddSolute(B,soluteById(B.solute).stock*got);',
     '    B.led.dropper+=bkAddSolute(B,soluteById(B.solute).cSat*got);', 'p'],
    ['evaporation takes solute with the water',
     '  B.led.evaporated+=bkRemoveSolvent(B,ctl.evap*dt);',
     '  B.led.evaporated+=bkRemoveSolvent(B,ctl.evap*dt); bkRemoveSolute(B,ctl.evap*dt);', 'p'],
    ['a grain is a hundredth of a mole',
     'const MOLE_PER_PARTICLE=1/PHET.PARTICLES_PER_MOLE;',
     'const MOLE_PER_PARTICLE=1/100;', 'p'],
    ['a landing grain delivers twice its moles',
     '    if(p.y<=surf){ B.led.shaker+=bkAddSolute(B,MOLE_PER_PARTICLE); }',
     '    if(p.y<=surf){ B.led.shaker+=bkAddSolute(B,2*MOLE_PER_PARTICLE); }', 'p'],
    ["the shaker's max(1,...) floor is gone",
     '  return Math.round(Math.max(1,PHET.SHAKER_RATE*PHET.PARTICLES_PER_MOLE*dt));',
     '  return Math.round(PHET.SHAKER_RATE*PHET.PARTICLES_PER_MOLE*dt);', 'p'],
    ['the shaker dispenses twice as fast',
     '  return Math.round(Math.max(1,PHET.SHAKER_RATE*PHET.PARTICLES_PER_MOLE*dt));',
     '  return Math.round(Math.max(1,2*PHET.SHAKER_RATE*PHET.PARTICLES_PER_MOLE*dt));', 'p'],
    ['the clock runs at thirty frames a second', 'const FRAME_DT=1/60;', 'const FRAME_DT=1/30;', 'p'],
    # ---------------- grams, percent, saturation ----------------
    ['grams weigh the precipitate too',
     '  const p=Math.max(0,n-V*cs);\n  return M*Math.max(0,n-p);',
     '  const p=Math.max(0,n-V*cs);\n  return M*n;', 'p'],
    ['mass percent over the solvent alone',
     '  return V<=0?0:g/(g+V*PHET.WATER_DENSITY)*100;',
     '  return V<=0?0:g/(V*PHET.WATER_DENSITY)*100;', 'p'],
    ["the stock's mass percent drops the solute from the denominator",
     '  return sol.molarMass*sol.stock*100/(PHET.WATER_DENSITY+sol.molarMass*sol.stock);',
     '  return sol.molarMass*sol.stock*100/PHET.WATER_DENSITY;', 'p'],
    ['the saturation volume is inverted',
     'function saturationVolume(n,cs){ return cs>0?n/cs:Infinity; }',
     'function saturationVolume(n,cs){ return cs>0?cs/n:Infinity; }', 'p'],
    ['the time to saturate multiplies by the rate',
     '  return (rate>0&&V>vs)?(V-vs)/rate:null;',
     '  return (rate>0&&V>vs)?(V-vs)*rate:null;', 'p'],
    ['half as many grains of solid are drawn',
     '  let k=Math.round(PHET.PARTICLES_PER_MOLE*pm);',
     '  let k=Math.round(PHET.PARTICLES_PER_MOLE*pm/2);', 'p'],
    ['a trace of solid draws none',
     '  if(k===0&&pm>0) k=1;', '  if(false) k=1;', 'p'],
    # ---------------- PhET's colour laws ----------------
    ['interpolateRGBA rounds instead of flooring',
     '  return [Math.floor(a[0]+(b[0]-a[0])*t),\n          Math.floor(a[1]+(b[1]-a[1])*t),\n'
     '          Math.floor(a[2]+(b[2]-a[2])*t)];',
     '  return [Math.round(a[0]+(b[0]-a[0])*t),\n          Math.round(a[1]+(b[1]-a[1])*t),\n'
     '          Math.round(a[2]+(b[2]-a[2])*t)];', 'p'],
    ["the scheme's first segment runs to saturation",
     '  if(c<=d.cMid) return lerpRGBfloor(d.minRGB,d.midRGB,(c-d.cMin)/(d.cMid-d.cMin));',
     '  if(c<=d.cMid) return lerpRGBfloor(d.minRGB,d.midRGB,(c-d.cMin)/(d.cSat-d.cMin));', 'p'],
    # (the "scheme has no water at zero" mutant is EQUIVALENT for PhET's data -- every
    #  solute's minColor IS the water colour, so the branch cannot differ; the suite
    #  asserts that property instead, and the mutant is not run)
    # (and the c <= cMin branch is unreachable for the same reason: every cMin is 0, so
    #  the "c > 0" test above it has already fired.  Both properties are asserted instead.)
    ["the Beer's Law ramp has no step at zero",
     '  if(!(c>0)) return WATER_RGB.slice();\n  const t=clamp(c/d.cMax,0,1);',
     '  if(c<0) return WATER_RGB.slice();\n  const t=clamp(c/d.cMax,0,1);', 'p'],
    ['the ramp is not clamped at full scale', '  const t=clamp(c/d.cMax,0,1);',
     '  const t=c/d.cMax;', 'p'],
    # ---------------- colorimetry ----------------
    ["illuminant A's fifth power", '  return 100*Math.pow(560/lam,5)',
     '  return 100*Math.pow(560/lam,4)', 'p'],
    ['illuminant A at 2856 K', 'const C2_ILLUM_A=1.435e-2, T_ILLUM_A=2848;',
     'const C2_ILLUM_A=1.435e-2, T_ILLUM_A=2856;', 'p'],
    ["illuminant A's radiation constant", 'const C2_ILLUM_A=1.435e-2, T_ILLUM_A=2848;',
     'const C2_ILLUM_A=1.4388e-2, T_ILLUM_A=2848;', 'p'],
    ['sRGB gamma 2.2 instead of 2.4',
     '  return u<=0.0031308?12.92*u:1.055*Math.pow(u,1/2.4)-0.055;',
     '  return u<=0.0031308?12.92*u:1.055*Math.pow(u,1/2.2)-0.055;', 'p'],
    ["sRGB's linear segment slope",
     '  return u<=0.0031308?12.92*u:1.055*Math.pow(u,1/2.4)-0.055;',
     '  return u<=0.0031308?12*u:1.055*Math.pow(u,1/2.4)-0.055;', 'p'],
    ["the sRGB matrix's leading term", 'const SRGB_M=[[ 3.2406,-1.5372,-0.4986],',
     'const SRGB_M=[[ 3.4606,-1.5372,-0.4986],', 'p'],
    ['the transmitted spectrum forgets the path length',
     '    const T=Math.pow(10,-t[i]*l*c);', '    const T=Math.pow(10,-t[i]*c);', 'p'],
    ['the colour integral swaps x-bar and y-bar',
     '    const sx=S*CIE_X[i], sy=S*CIE_Y[i], sz=S*CIE_Z[i];',
     '    const sx=S*CIE_Y[i], sy=S*CIE_X[i], sz=S*CIE_Z[i];', 'p'],
    ['no adaptation to the illuminant',
     '  const v=[lin[0]/w[0],lin[1]/w[1],lin[2]/w[2]];',
     '  const v=[lin[0],lin[1],lin[2]];', 'p'],
    ["srgbGamma's clamp is gone (the ONE guard on that path)", '  u=clamp(u,0,1);',
     '  u=u*1;', 'p'],
    ["the luminance's red weight",
     '  return 0.2126*inv(v[0])+0.7152*inv(v[1])+0.0722*inv(v[2]);',
     '  return 0.3126*inv(v[0])+0.7152*inv(v[1])+0.0722*inv(v[2]);', 'p'],
    ["the beam colour's fade on the eye", '  const k=Math.sqrt(Math.min(1,4*CIE_Y[i]));',
     '  const k=Math.sqrt(Math.min(1,2*CIE_Y[i]));', 'p'],
    ['the beam colour is not normalised to its brightest channel',
     '  return v.map(u=>Math.round(255*srgbGamma(u/m*k)));',
     '  return v.map(u=>Math.round(255*srgbGamma(u*k)));', 'p'],
    # ---------------- the bench ----------------
    ['the linear limit is 50 mM', 'const LINEAR_LIMIT=0.01;', 'const LINEAR_LIMIT=0.05;', 'p'],
    ["the detector's beam is wider", 'const BEAM_HALF=0.225, SENSOR_HALF=0.5;',
     'const BEAM_HALF=0.28, SENSOR_HALF=0.5;', 'p'],
    ["the detector's sensor is bigger", 'const BEAM_HALF=0.225, SENSOR_HALF=0.5;',
     'const BEAM_HALF=0.225, SENSOR_HALF=0.7;', 'p'],
    ['the cuvette snaps down instead of to the nearest',
     '  return clamp(Math.round(w/s)*s,PHET.CUVETTE_MIN,PHET.CUVETTE_MAX);',
     '  return clamp(Math.floor(w/s)*s,PHET.CUVETTE_MIN,PHET.CUVETTE_MAX);', 'p'],
    ['the preset wavelength is not the peak',
     'function presetWavelength(){ return lambdaMaxOf(ST.blSolution); }',
     'function presetWavelength(){ return 550; }', 'p'],
    ['changing the solution keeps the old concentration',
     '  ST.blConc=blsById(id).cDefault;', '  ST.blConc=ST.blConc;', 'p'],
    ['changing the solute leaves the old one in the beaker',
     '  BK.solute=id; BK.n=0; BK.parts=[];', '  BK.solute=id; BK.parts=[];', 'p'],
    ['the evaporation curve is drawn uncapped',
     '    cc.push(V>0?Math.min(B.cs,B.n/V):NaN);', '    cc.push(V>0?B.n/V:NaN);', 'p'],
    # ---------------- the UI ----------------
    ['UI: pointer-down does not mark the canvas dirty',
     "    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; }",
     "    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); }", 'u'],
    ['UI: pointer-move does not mark it dirty',
     "    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }",
     "    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ roEl.innerHTML=readoutHTML(S.model()); }", 'u'],
    ["UI: the meter probe's x is frozen", '          PROBE.x=clamp(p.x,-0.25,1.25);',
     '          PROBE.x=PROBE.x;', 'u'],
    ["UI: the meter probe's y is frozen", '          PROBE.y=clamp(p.y,-0.20,1.30);',
     '          PROBE.y=PROBE.y;', 'u'],
    ["UI: the probe's grab box is the whole canvas",
     "          if(Math.abs(x-px)<=12&&y>=py-30&&y<=py+10){ DRAG.what='probe'; return true; }",
     "          if(Math.abs(x-px)<=400&&y>=py-300&&y<=py+300){ DRAG.what='probe'; return true; }", 'u'],
    ['UI: a slider does not repaint',
     '      if(setf) setf(v); else ST[key]=v;\n      syncPanel(); dirty=true; refresh(); });',
     '      if(setf) setf(v); else ST[key]=v;\n      syncPanel(); });', 'u'],
    ['UI: the frame loop ignores the dirty flag', '    if(advanced||dirty){', '    if(advanced){', 'u'],
    ['UI: reset all forgets the beaker',
     '      resetBeaker();\n      PROBE.x=PROBE0.x;', '      PROBE.x=PROBE0.x;', 'u'],
    ['UI: the meter group never hides', "    gMeter.hidden=(v!=='beaker');",
     '    gMeter.hidden=false;', 'u'],
]
if BEERS:
    M += [
        ["UI: the cuvette's wall does not move",
         '          ST.cuvette=clamp(DRAG.grabW+(x-DRAG.grabX)/L.px,PHET.CUVETTE_MIN,PHET.CUVETTE_MAX);',
         '          ST.cuvette=DRAG.grabW;', 'u'],
        ['UI: the cuvette does not snap on release',
         "        if(DRAG.what==='cuvette') ST.cuvette=snapCuvette(ST.cuvette);",
         "        if(false) ST.cuvette=snapCuvette(ST.cuvette);", 'u'],
        ["UI: the detector's x is frozen",
         '          DET.x=clamp(L.cmOf(x)-L.CUV0,-0.4,L.BENCH_CM-L.CUV0);',
         '          DET.x=DET.x;', 'u'],
        ["UI: the detector's y is frozen", '          DET.y=clamp((L.axis-y)/L.px,-2.4,2.4);',
         '          DET.y=DET.y;', 'u'],
        ['UI: the wavelength slider is always shown',
         "    if(rows.wavelength) rows.wavelength.row.hidden=(ST.lightMode!=='variable');",
         '    if(rows.wavelength) rows.wavelength.row.hidden=false;', 'u'],
    ]

# Five constants belong to the Beer's Law bench alone -- the beam's width, the sensor's,
# the cuvette's snap, the preset wavelength and the solution's default concentration.  The
# engine is shared, so concentration.html carries them, but it has no cuvette and no bench
# controls and never reaches them: they survive its sweep for the same reason a mutant in a
# view a sim does not build would.  They are swept in beers-law-lab, where they are live,
# and left out here with that as the reason rather than reported as survivors.
BENCH_ONLY = ("the detector's beam is wider", "the detector's sensor is bigger",
              'the cuvette snaps down instead of to the nearest',
              'the preset wavelength is not the peak',
              'changing the solution keeps the old concentration')
if not BEERS:
    M = [e for e in M if e[0] not in BENCH_ONLY]

s = io.open(HTML, encoding='utf-8').read()
js = s.split('<script>', 1)[1].rsplit('</script>', 1)[0]
bad = []
for e in M:
    n = js.count(e[1])
    if n != 1:
        bad.append((e[0], n))
print('%d mutants (%d physics, %d UI)' % (len(M), sum(1 for e in M if e[3] == 'p'),
                                          sum(1 for e in M if e[3] == 'u')))
for label, n in bad:
    print('  PATTERN APPEARS %d TIMES: %s' % (n, label))
io.open(os.path.join(BDIR, 'mutants.json'), 'w', encoding='utf-8').write(
    json.dumps(M, indent=1) + '\n')
print('wrote %s' % os.path.relpath(os.path.join(BDIR, 'mutants.json'), HERE))
if bad:
    raise SystemExit(1)
