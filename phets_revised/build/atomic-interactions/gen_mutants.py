#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write mutants.json for atomic-interactions.html.

Every `old` pattern is checked for being present EXACTLY ONCE in the extracted
script before the file is written: a pattern that matches twice mutates two
places silently, and one that matches zero times is a mutant you believe you
ran and did not (mutate.py reports these as SKIP, which is easy to skim past).

Suite 'p' runs selfTest alone; 'u' appends the UI drive.  Nothing here can make
a loop non-terminating: every mutated value is a constant, a sign, an exponent
or a statement order, and every loop in the file is bounded by a count (the
integrator's MAX_STEPS, the quadrature's panel count, the Newton iteration's
100).  A mutant that turns a correction loop into an infinite one outlives the
sweep and burns a core for days (BRIEF.md), so keep it that way.
"""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.normpath(os.path.join(HERE, '..', '..', 'atomic-interactions.html'))

M = []


def m(label, old, new, suite='p'):
    M.append([label, old, new, suite])


# ---------------------------------------------------------- the potential
m('V leading 4 -> 3',
  'return 4 * eps * (x6 * x6 - x6);', 'return 3 * eps * (x6 * x6 - x6);')
m('V attraction sign',
  'return 4 * eps * (x6 * x6 - x6);', 'return 4 * eps * (x6 * x6 + x6);')
m('V repulsion dropped',
  'return 4 * eps * (x6 * x6 - x6);', 'return 4 * eps * (x6 - x6 * x6);')
m('V exponent 6 -> 5',
  '  const x6 = Math.pow(sig / r, 6);\n  return 4 * eps * (x6 * x6 - x6);',
  '  const x6 = Math.pow(sig / r, 5);\n  return 4 * eps * (x6 * x6 - x6);')
m('V exponent 12 -> 11 (x6*x6 -> x6*x6/ (sig/r))',
  'return 4 * eps * (x6 * x6 - x6);',
  'return 4 * eps * (x6 * x6 * r / sig - x6);')

# ---------------------------------------------------------- the force
m('F leading 24 -> 12',
  'return 24 * eps / r * (2 * x6 * x6 - x6);', 'return 12 * eps / r * (2 * x6 * x6 - x6);')
m('F drops the factor 2',
  'return 24 * eps / r * (2 * x6 * x6 - x6);', 'return 24 * eps / r * (x6 * x6 - x6);')
m('F sign of the attraction',
  'return 24 * eps / r * (2 * x6 * x6 - x6);', 'return 24 * eps / r * (2 * x6 * x6 + x6);')
m('F overall sign',
  'return 24 * eps / r * (2 * x6 * x6 - x6);', 'return -24 * eps / r * (2 * x6 * x6 - x6);')
m('F exponent 6 -> 7',
  '  const x6 = Math.pow(sig / r, 6);\n  return 24 * eps / r * (2 * x6 * x6 - x6);',
  '  const x6 = Math.pow(sig / r, 7);\n  return 24 * eps / r * (2 * x6 * x6 - x6);')
m('F 1/r dropped',
  'return 24 * eps / r * (2 * x6 * x6 - x6);', 'return 24 * eps * (2 * x6 * x6 - x6);')

# ---------------------------------------------------------- the curvature
m("V'' leading 24 -> 25",
  'return 24 * eps / (r * r) * (26 * x6 * x6 - 7 * x6);',
  'return 25 * eps / (r * r) * (26 * x6 * x6 - 7 * x6);')
m("V'' 26 -> 25",
  'return 24 * eps / (r * r) * (26 * x6 * x6 - 7 * x6);',
  'return 24 * eps / (r * r) * (25 * x6 * x6 - 7 * x6);')
m("V'' 7 -> 8",
  'return 24 * eps / (r * r) * (26 * x6 * x6 - 7 * x6);',
  'return 24 * eps / (r * r) * (26 * x6 * x6 - 8 * x6);')
m("V'' 1/r^2 -> 1/r",
  'return 24 * eps / (r * r) * (26 * x6 * x6 - 7 * x6);',
  'return 24 * eps / r * (26 * x6 * x6 - 7 * x6);')

# ------------------------------------------------- PhET's own two halves
m("PhET repulsive 48 -> 24", 'return 48 * eps / r * x6 * x6;', 'return 24 * eps / r * x6 * x6;')
m("PhET attractive 24 -> 12", 'return 24 * eps / r * x6;', 'return 12 * eps / r * x6;')

# ---------------------------------------------------------- the landmarks
m('r_min uses 2^(1/3)', 'function rMin(sig){ return sig * SIXRT2; }',
  'function rMin(sig){ return sig * CBRT2; }')
m('the spring constant 72 -> 71',
  'function ljK(sig, eps){ return 72 * eps / (CBRT2 * sig * sig); }',
  'function ljK(sig, eps){ return 71 * eps / (CBRT2 * sig * sig); }')
m('the spring drops 2^(1/3)',
  'function ljK(sig, eps){ return 72 * eps / (CBRT2 * sig * sig); }',
  'function ljK(sig, eps){ return 72 * eps / (sig * sig); }')
m('the spring is 1/sigma, not 1/sigma^2',
  'function ljK(sig, eps){ return 72 * eps / (CBRT2 * sig * sig); }',
  'function ljK(sig, eps){ return 72 * eps / (CBRT2 * sig); }')
m('omega multiplies by mu instead of dividing',
  'function ljOmega(sig, eps, mu){ return Math.sqrt(ljK(sig, eps) / mu); }',
  'function ljOmega(sig, eps, mu){ return Math.sqrt(ljK(sig, eps) * mu); }')
m('the period drops the 2 of 2 pi',
  'function ljPeriod(sig, eps, mu){ return 2 * Math.PI / ljOmega(sig, eps, mu); }',
  'function ljPeriod(sig, eps, mu){ return Math.PI / ljOmega(sig, eps, mu); }')
m('the deepest pull at (25/7)^(1/6)', 'rF:sig*Math.pow(26/7,1/6)', 'rF:sig*Math.pow(25/7,1/6)')

# ---------------------------------------------------------- the masses
m('the reduced mass is the SUM',
  'return pinned ? mb : ma * mb / (ma + mb);', 'return pinned ? mb : ma + mb;')
m('pinned uses the FIXED atom',
  'return pinned ? mb : ma * mb / (ma + mb);', 'return pinned ? ma : ma * mb / (ma + mb);')
m('the reduced mass is not reduced at all',
  'return pinned ? mb : ma * mb / (ma + mb);', 'return mb;')
m('kinetic energy loses its half',
  'return 0.5 * mu * s.v * s.v + ljV(s.r, sig, eps);',
  'return mu * s.v * s.v + ljV(s.r, sig, eps);')
m('the readout kinetic energy loses its half',
  'const K=0.5*P.mu*st.v*st.v, E=K+V;', 'const K=P.mu*st.v*st.v, E=K+V;')

# ---------------------------------------------------------- the units
m('k_B / m_u doubled', 'const K_TO_E = KBOLTZ / MU_KG;', 'const K_TO_E = 2 * KBOLTZ / MU_KG;')
m('the pN conversion off by ten', 'const F_TO_PN = MU_KG * 1e24;', 'const F_TO_PN = MU_KG * 1e23;')
m('the meV conversion off by ten', 'const E_TO_MEV = MU_KG / QE * 1e3;',
  'const E_TO_MEV = MU_KG / QE * 1e2;')
m('the zJ conversion off by ten', 'const E_TO_ZJ = MU_KG * 1e21;', 'const E_TO_ZJ = MU_KG * 1e20;')
m('2^(1/3) -> 2^(1/4)', 'const CBRT2 = Math.pow(2, 1 / 3);', 'const CBRT2 = Math.pow(2, 1 / 4);')
m('2^(1/6) -> 2^(1/5)', 'const SIXRT2 = Math.pow(2, 1 / 6);', 'const SIXRT2 = Math.pow(2, 1 / 5);')

# ---------------------------------------------------------- turning points
m('the discriminant sign', 'const d = 1 + E / eps;', 'const d = 1 - E / eps;')
m('the roots lose their half',
  'const uIn = 0.5 * (1 + s), uOut = 0.5 * (1 - s);',
  'const uIn = (1 + s), uOut = 0.5 * (1 - s);')
m('the roots are swapped',
  'const uIn = 0.5 * (1 + s), uOut = 0.5 * (1 - s);',
  'const uIn = 0.5 * (1 - s), uOut = 0.5 * (1 + s);')
m('u -> r uses the wrong root',
  "return {rIn: sig * Math.pow(uIn, -1 / 6),", "return {rIn: sig * Math.pow(uIn, -1 / 5),")

# ---------------------------------------------------------- the quadrature
m('the regularised integrand loses r^6', 'const r6 = Math.pow(r, 6);', 'const r6 = Math.pow(r, 5);')
m('the quadrature 8 eps -> 4 eps',
  's += ww * pre * r6 * Math.sqrt(mu / (8 * eps * Sin * Sout));',
  's += ww * pre * r6 * Math.sqrt(mu / (4 * eps * Sin * Sout));')
m('the quadrature prefactor r1^3 -> r1^2',
  'const pre = Math.pow(r1, 3) * Math.pow(r2, 3) / sig6;',
  'const pre = Math.pow(r1, 2) * Math.pow(r2, 3) / sig6;')
m('the substitution loses its half-width',
  'const a = 0.5 * (r1 + r2), b = 0.5 * (r2 - r1);\n  const gl = gaussLegendre(n);',
  'const a = 0.5 * (r1 + r2), b = (r2 - r1);\n  const gl = gaussLegendre(n);')
m('the period loses its factor 2', 'return 2 * s;\n}\n\n/* The same integral',
  'return s;\n}\n\n/* The same integral')
m('powSum6 loses a term',
  'return y2 * y2 * y + x * y2 * y2 + x2 * y2 * y + x2 * x * y2 + x2 * x2 * y\n       + x2 * x2 * x;',
  'return y2 * y2 * y + x * y2 * y2 + x2 * y2 * y + x2 * x * y2\n       + x2 * x2 * x;')

# ---------------------------------------------------------- the integrators
m('velocity Verlet loses its first half-kick',
  's.v += 0.5 * s.a * dt;\n  s.r += s.v * dt;', 's.v += s.a * dt;\n  s.r += s.v * dt;')
m('velocity Verlet loses its second half-kick',
  's.v += 0.5 * s.a * dt;\n  s.t += dt;', 's.v += s.a * dt;\n  s.t += dt;')
m('symplectic Euler becomes forward Euler',
  's.v += s.a * dt;\n  s.r += s.v * dt;\n  s.t += dt;',
  's.r += s.v * dt;\n  s.v += s.a * dt;\n  s.t += dt;')
m('the step ceiling is computed and not applied',
  'n = isFinite(n) && n > 0 ? Math.min(n, MAX_STEPS) : 0;',
  'n = isFinite(n) && n > 0 ? n : 0;')
m('the escape speed loses its 2',
  'return v >= 0 ? 0 : Math.sqrt(-2 * v / mu);', 'return v >= 0 ? 0 : Math.sqrt(-v / mu);')
m("Landau's coefficient 91/4 -> 90/4", 'const ANHARM_C=91/4;', 'const ANHARM_C=90/4;')

# ---------------------------------------------------------- the tables
m("PhET's neon sigma 308 -> 310",
  "{key: 'NeNe', label: 'neon-neon', a: 'Ne', b: 'Ne', sig: 308, eps: 35.8}",
  "{key: 'NeNe', label: 'neon-neon', a: 'Ne', b: 'Ne', sig: 310, eps: 35.8}")
m("PhET's argon eps 111.84 -> 111",
  "{key: 'ArAr', label: 'argon-argon', a: 'Ar', b: 'Ar', sig: 376, eps: 111.84}",
  "{key: 'ArAr', label: 'argon-argon', a: 'Ar', b: 'Ar', sig: 376, eps: 111}")
m("PhET's oxygen eps 1000 -> 113 (the literature value)",
  "{key: 'OO', label: 'oxygen-oxygen', a: 'O', b: 'O', sig: 200, eps: 1000}",
  "{key: 'OO', label: 'oxygen-oxygen', a: 'O', b: 'O', sig: 200, eps: 113}")
m("PhET's neon radius 154 -> 150",
  "Ne: {sym: 'Ne', name: 'neon', r: 154, m: 20.1797, col: '#5ac8e0'}",
  "Ne: {sym: 'Ne', name: 'neon', r: 150, m: 20.1797, col: '#5ac8e0'}")
m("PhET's neon mass",
  "Ne: {sym: 'Ne', name: 'neon', r: 154, m: 20.1797, col: '#5ac8e0'}",
  "Ne: {sym: 'Ne', name: 'neon', r: 154, m: 20.18, col: '#5ac8e0'}")
m('the literature neon r_min',
  "Ne: {sig: 278.9, eps: 35.7, rmin: 313.1, src: 'van Sciver 2012'}",
  "Ne: {sig: 278.9, eps: 35.7, rmin: 311.0, src: 'van Sciver 2012'}")
m('the literature argon eps',
  "Ar: {sig: 341.8, eps: 124.0, rmin: 383.7, src: 'van Sciver 2012'}",
  "Ar: {sig: 341.8, eps: 122.4, rmin: 383.7, src: 'van Sciver 2012'}")
m("PhET's own O2 constant", 'const PHET_SOM = {epsO2: 113, sigO2: 365};',
  'const PHET_SOM = {epsO2: 112, sigO2: 365};')
m("PhET's argon critical point", 'const PHET_CRIT = {Ne: 45, Ar: 151, O: 155};',
  'const PHET_CRIT = {Ne: 45, Ar: 150, O: 155};')
m('the Lorentz rule loses its half',
  'return {sig: 0.5 * (pa.sig + pb.sig), eps: Math.sqrt(pa.eps * pb.eps)};',
  'return {sig: (pa.sig + pb.sig), eps: Math.sqrt(pa.eps * pb.eps)};')
m('Berthelot becomes an arithmetic mean',
  'return {sig: 0.5 * (pa.sig + pb.sig), eps: Math.sqrt(pa.eps * pb.eps)};',
  'return {sig: 0.5 * (pa.sig + pb.sig), eps: 0.5 * (pa.eps + pb.eps)};')
m("PhET's slider floor 75 -> 70",
  'const PHET_MIN_SIGMA = 75, PHET_MAX_SIGMA = 500;',
  'const PHET_MIN_SIGMA = 70, PHET_MAX_SIGMA = 500;')
m("PhET's epsilon ceiling 450 -> 400",
  'const PHET_MIN_EPSILON = 20, PHET_MAX_EPSILON = 450;',
  'const PHET_MIN_EPSILON = 20, PHET_MAX_EPSILON = 400;')
m("PhET's 5-pm snap becomes 10",
  'st.adjSig=clamp(Math.round(s/5)*5,PHET_MIN_SIGMA,PHET_MAX_SIGMA);',
  'st.adjSig=clamp(Math.round(s/10)*10,PHET_MIN_SIGMA,PHET_MAX_SIGMA);')
m("PhET's 5-K snap becomes 10",
  'st.adjEps=clamp(Math.round(e/5)*5,PHET_MIN_EPSILON,PHET_MAX_EPSILON);',
  'st.adjEps=clamp(Math.round(e/10)*10,PHET_MIN_EPSILON,PHET_MAX_EPSILON);')
# The window floor SURVIVED the first full sweep, because every assertion that
# touched it was written as `R_LO_FAC * sigma` — in terms of the constant under
# test.  It is not an equivalent mutant: it moves the inward end of a drag from
# 221.76 pm to 154.00 pm for neon, where the wall goes from 177 eps to 16128.
# It is invisible to the PICTURE only because the curve is clipped above
# 0.943 sigma.  Both ends are now mutated, and both are pinned in absolute
# picometres off the built model (selfTest section J2).
m('the drawn r window floor', 'const R_LO_FAC=0.72, R_HI_FAC=3.2;',
  'const R_LO_FAC=0.50, R_HI_FAC=3.2;')
m('the drawn r window ceiling', 'const R_LO_FAC=0.72, R_HI_FAC=3.2;',
  'const R_LO_FAC=0.72, R_HI_FAC=2.6;')
# the same class, everywhere else a constant appeared in its own assertion
m("the integrator's step ceiling", 'const MAX_STEPS=6e5;',
  'const MAX_STEPS=6e4;')
m('the clock speed', 'const PS_PER_SEC=2.0, SLOW_FACTOR=0.35, DT_INT=1.5e-3;',
  'const PS_PER_SEC=3.0, SLOW_FACTOR=0.35, DT_INT=1.5e-3;', 'u')
m("PhET's slow factor", 'const PS_PER_SEC=2.0, SLOW_FACTOR=0.35, DT_INT=1.5e-3;',
  'const PS_PER_SEC=2.0, SLOW_FACTOR=0.50, DT_INT=1.5e-3;', 'u')
m('the integrator substep', 'const PS_PER_SEC=2.0, SLOW_FACTOR=0.35, DT_INT=1.5e-3;',
  'const PS_PER_SEC=2.0, SLOW_FACTOR=0.35, DT_INT=6.0e-3;', 'u')
m('the trail cap', 'const TRAIL_MAX=900;', 'const TRAIL_MAX=600;')

# ---------------------------------------------------------------- the UI
m('the pointer-move dirty flag',
  "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){\n      dirty=true;",
  "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){\n      dirty=false;", 'u')
m('the drag reads the y coordinate',
  "if(type==='move'&&DRAG.what==='atom'){ setSep(ST,G.wx(x)-DRAG.off); return true; }",
  "if(type==='move'&&DRAG.what==='atom'){ setSep(ST,G.wx(y)-DRAG.off); return true; }", 'u')
m('the drag is not clamped to the axis',
  'function setSep(st,r){ const b=rBounds(st); st.r=clamp(r,b[0],b[1]); st.v=0; TRAIL=[]; }',
  'function setSep(st,r){ st.r=r; st.v=0; TRAIL=[]; }', 'u')
m('the drag does not pause the motion',
  "if(hit){ DRAG.what='atom'; DRAG.off=G.wx(x)-ST.r; ST.running=false; return true; }",
  "if(hit){ DRAG.what='atom'; DRAG.off=G.wx(x)-ST.r; return true; }", 'u')
m('Return Atom leaves the clock running',
  'function returnAtom(st){ st.r=rMin(pairOf(st).sig); st.v=0; st.t=0; st.running=false; TRAIL=[]; }',
  'function returnAtom(st){ st.r=rMin(pairOf(st).sig); st.v=0; st.t=0; TRAIL=[]; }', 'u')
m('changing the pair leaves the atom where it was',
  'function setPair(st,key){ st.pair=key; returnAtom(st); }',
  'function setPair(st,key){ st.pair=key; }', 'u')
m('a slider does not redraw',
  "inp.addEventListener('input',()=>{ set(parseFloat(inp.value)); syncPanel(); dirty=true; refresh(); });",
  "inp.addEventListener('input',()=>{ set(parseFloat(inp.value)); syncPanel(); dirty=true; });", 'u')
m('the literature switch is left live on the adjustable pair',
  'rows.cb_lit.inp.disabled=!litOn;', 'rows.cb_lit.inp.disabled=false;', 'u')
m('the adjustable sliders are never hidden',
  "gAdj.hidden=!(st.pair==='Adj');", 'gAdj.hidden=false;', 'u')
m('the frame loop runs while paused', 'if(!ST.running) return false;',
  'if(false) return false;', 'u')
m('the slow switch does nothing',
  'S.advance(PS_PER_SEC*(ST.slow?SLOW_FACTOR:1)/60);', 'S.advance(PS_PER_SEC/60);', 'u')
m('space does not toggle the clock',
  "if(e.key===' '){ st.running=!st.running; dirty=true; refresh(); }",
  "if(e.key===' '){ dirty=true; refresh(); }", 'u')
m('the trail records twice a frame', 'TRAIL.push([s.t,s.r,K,V]);',
  'TRAIL.push([s.t,s.r,K,V]); TRAIL.push([s.t,s.r,K,V]);', 'u')
m('the tab keys are off by one',
  "if(e.key>='1'&&e.key<=String(TABS.length)){ setView(TABS[+e.key-1][0]); return; }",
  "if(e.key>='1'&&e.key<=String(TABS.length)){ setView(TABS[+e.key%TABS.length][0]); return; }", 'u')
m('reset all keeps the clock', "Object.assign(st,DEFAULTS); st.view=v; simReset();",
  "Object.assign(st,DEFAULTS); st.view=v;", 'u')

# ------------------------------------------------------------------ check
src = io.open(HTML, encoding='utf-8').read()
js = src.split('<script>', 1)[1].rsplit('</script>', 1)[0]
bad = [(lab, js.count(old)) for lab, old, new, s in M if js.count(old) != 1]
for lab, n in bad:
    print('PATTERN %-50s appears %d times' % (lab, n))
if bad:
    raise SystemExit('%d patterns are not unique — fix them before writing' % len(bad))
dupes = [x for x in set((a[1], a[2]) for a in M)
         if sum(1 for b in M if (b[1], b[2]) == x) > 1]
if dupes:
    raise SystemExit('%d identical mutations listed twice' % len(dupes))
io.open(os.path.join(HERE, 'mutants.json'), 'w', encoding='utf-8').write(
    json.dumps(M, ensure_ascii=False, indent=0))
print('mutants.json: %d mutants (%d physics, %d UI)'
      % (len(M), sum(1 for x in M if x[3] == 'p'), sum(1 for x in M if x[3] == 'u')))
