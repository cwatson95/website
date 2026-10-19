#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write mutants.json: break one constant, exponent, sign or unit at a time and
check the suite goes red.  Every pattern is verified to appear EXACTLY ONCE in
the extracted script first — a pattern that matches twice mutates two places
and one that matches zero times is a mutant you think you ran and did not."""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.normpath(os.path.join(HERE, "..", "..", "models-of-the-hydrogen-atom.html"))
SRC = io.open(HTML, encoding="utf-8").read().split("<script>", 1)[1].rsplit("</script>", 1)[0]

M = []


def m(label, old, new, suite="p"):
    M.append([label, old, new, suite])


# ---- the constants -----------------------------------------------------
m("R_inf", "const R_INF   = 10973731.568157;", "const R_INF   = 10973731.568157 * 1.000001;")
m("Rydberg energy", "const RYD_EV  = 13.60569312299;", "const RYD_EV  = 13.60569312299 * 1.0001;")
m("Bohr radius", "const A0      = 5.29177210544e-11;", "const A0      = 5.29177210544e-11 * 1.001;")
m("fine-structure constant", "const ALPHA   = 0.0072973525643;", "const ALPHA   = 0.0072973525643 * 1.001;")
m("electron mass", "const M_E      = 9.1093837139e-31;", "const M_E      = 9.1093837139e-31 * 1.001;")
m("Planck constant", "const H_PLANCK = 6.62607015e-34;", "const H_PLANCK = 6.62607015e-34 * 1.001;")
m("electron/proton mass ratio", "const ME_MP   = 0.00054461702149015;", "const ME_MP   = 0.00054461702149015 * 2;")
m("the reduced mass is dropped", "const MU_ME   = 1 / (1 + ME_MP);", "const MU_ME   = 1;")
m("the reduced mass sign", "const MU_ME   = 1 / (1 + ME_MP);", "const MU_ME   = 1 / (1 - ME_MP);")
m("atomic unit of time", "const T_AU = 2.4188843265863e-17;", "const T_AU = 2.4188843265863e-17 * 1.001;")
m("DEG converts the wrong way", "const DEG = PI / 180, RAD = 180 / PI;", "const DEG = 180 / PI, RAD = PI / 180;")

# ---- the Bohr ladder ---------------------------------------------------
m("E_n exponent", "function energyEV(n){ return -RH_EV / (n * n); }",
  "function energyEV(n){ return -RH_EV / (n * n * n); }")
m("E_n sign", "function energyEV(n){ return -RH_EV / (n * n); }",
  "function energyEV(n){ return RH_EV / (n * n); }")
m("r_n exponent", "function orbitRadius(n){ return n * n * A0; }",
  "function orbitRadius(n){ return n * A0; }")
m("v_n exponent", "function orbitSpeed(n){ return ALPHA * C_LIGHT / n; }",
  "function orbitSpeed(n){ return ALPHA * C_LIGHT / (n * n); }")
m("nm conversion in lamVac", "function lamVac(n1, n2){ return 1e9 / (R_H",
  "function lamVac(n1, n2){ return 1e10 / (R_H")
m("lamVac exponent", "1e9 / (R_H * (1 / (n1 * n1) - 1 / (n2 * n2)))",
  "1e9 / (R_H * (1 / n1 - 1 / n2))")
m("series limit exponent", "function seriesLimit(n1){ return 1e9 / (R_H / (n1 * n1)); }",
  "function seriesLimit(n1){ return 1e9 / (R_H / n1); }")

# ---- PhET's own table --------------------------------------------------
m("PhET hc", "const PHET_HC = 1240, PHET_RYD = 13.6;", "const PHET_HC = 1230, PHET_RYD = 13.6;")
m("PhET Rydberg", "const PHET_HC = 1240, PHET_RYD = 13.6;", "const PHET_HC = 1240, PHET_RYD = 13.7;")
m("PhET rounds down", "return Math.round(PHET_HC / (PHET_RYD", "return Math.floor(PHET_HC / (PHET_RYD")
m("PhET white-light bias", "whiteGroundFraction: 0.4,", "whiteGroundFraction: 0.7,", "p")

# ---- the wavefunctions -------------------------------------------------
m("factorial starts at 3", "function factorial(k){ let f = 1; for(let i = 2; i <= k; i++) f *= i; return f; }",
  "function factorial(k){ let f = 1; for(let i = 3; i <= k; i++) f *= i; return f; }")
m("binomial coefficient", "for(let i = 0; i < k; i++) r = r * (n - i) / (i + 1);",
  "for(let i = 0; i < k; i++) r = r * (n - i) / (i + 2);")
m("R_nl normalisation exponent", "factorial(n + l)));\n  const co = new Array(n).fill(0);",
  "factorial(n + l) * 2));\n  const co = new Array(n).fill(0);")
m("R_nl normalisation, the Laguerre route", "factorial(n + l)));\n  return norm * Math.exp(-rho / 2)",
  "factorial(n + l) * 2));\n  return norm * Math.exp(-rho / 2)")
m("R_nl rho in the Laguerre route", "const rho = 2 * r / n;\n  const norm", "const rho = r / n;\n  const norm")
m("R_nl series sign", "const term = (k % 2 ? -1 : 1) * binom(n + l, n - l - 1 - k)",
  "const term = 1 * binom(n + l, n - l - 1 - k)")
m("R_nl rho scale in the series", "/ factorial(k) * Math.pow(2 / n, k);",
  "/ factorial(k) * Math.pow(1 / n, k);")
m("R_nl rho^l factor", "co[l + k] += norm * Math.pow(2 / n, l) * term;",
  "co[l + k] += norm * term;")
m("R_nl exponential decay", "return s * Math.exp(-r / n);", "return s * Math.exp(-2 * r / n);")
m("Laguerre recurrence", "const p2 = ((2 * i + 1 + a - x) * p1 - (i + a) * p0) / (i + 1);",
  "const p2 = ((2 * i + 1 + a - x) * p1 - (i + a) * p0) / (i + 2);")
m("Legendre double factorial step", "for(let i = 1; i <= m; i++){ pmm *= -f * somx2; f += 2; }",
  "for(let i = 1; i <= m; i++){ pmm *= -f * somx2; f += 1; }")
m("Legendre P_{m+1}^m", "let pmmp1 = x * (2 * m + 1) * pmm;", "let pmmp1 = x * (2 * m + 3) * pmm;")
m("Legendre recurrence", "pll = ((2 * ll - 1) * x * pmmp1 - (ll + m - 1) * pmm) / (ll - m);",
  "pll = ((2 * ll - 1) * x * pmmp1 - (ll + m) * pmm) / (ll - m);")
m("|Y_lm|^2 normalisation", "return (2 * l + 1) / (4 * PI) * factorial(l - am) / factorial(l + am) * p * p;",
  "return (2 * l + 1) / (2 * PI) * factorial(l - am) / factorial(l + am) * p * p;")
m("|Y_lm|^2 factorial ratio", "return (2 * l + 1) / (4 * PI) * factorial(l - am) / factorial(l + am) * p * p;",
  "return (2 * l + 1) / (4 * PI) * factorial(l + am) / factorial(l - am) * p * p;")
m("|psi|^2 polar axis", "const cth = r > 0 ? clamp(z / r, -1, 1) : 1;",
  "const cth = r > 0 ? clamp(x / r, -1, 1) : 1;")
m("<r> closed form", "function meanR(n, l){ return (3 * n * n - l * (l + 1)) / 2; }",
  "function meanR(n, l){ return (3 * n * n - l * (l + 1)) / 3; }")
m("<r> l term", "function meanR(n, l){ return (3 * n * n - l * (l + 1)) / 2; }",
  "function meanR(n, l){ return (3 * n * n - l * l) / 2; }")
m("<r^2> closed form", "return n * n * (5 * n * n + 1 - 3 * l * (l + 1)) / 2;",
  "return n * n * (5 * n * n + 1 - 3 * l * (l + 1)) / 3;")
m("<1/r> exponent", "function meanInvR(n){ return 1 / (n * n); }", "function meanInvR(n){ return 1 / n; }")
m("radial node count", "function radialNodes(n, l){ return n - l - 1; }",
  "function radialNodes(n, l){ return n - l; }")
m("angular node count", "function angularNodes(l, m){ return l - Math.abs(m); }",
  "function angularNodes(l, m){ return l + Math.abs(m); }")
m("column density symmetry factor", "return 2 * s * hstep / 3;", "return s * hstep / 3;")
m("column Simpson weights", "for(let i = 1; i < N; i++) s += (i % 2 ? 4 : 2) * psiSq(n, l, m, x, i * hstep, z);",
  "for(let i = 1; i < N; i++) s += (i % 2 ? 2 : 4) * psiSq(n, l, m, x, i * hstep, z);")
m("column panel count ignores n", "const N = panels || 2 * Math.ceil(ymax / (0.1 * n));",
  "const N = panels || 240;")

# ---- the Einstein coefficients ----------------------------------------
m("dipole integral power of r", "const k = i + j + 3;", "const k = i + j + 2;")
m("dipole integral exponent", "tot += c1[i] * c2[j] * factorial(k) / Math.pow(s, k + 1);",
  "tot += c1[i] * c2[j] * factorial(k) / Math.pow(s, k);")
m("dipole integral decay", "const c1 = rnlPoly(n1, l1), c2 = rnlPoly(n2, l2), s = 1 / n1 + 1 / n2;",
  "const c1 = rnlPoly(n1, l1), c2 = rnlPoly(n2, l2), s = 1 / n1 - 1 / n2;")
m("Einstein A leading 4/3", "return (4 / 3) * Math.pow(ALPHA, 3) * w * w * w",
  "return (2 / 3) * Math.pow(ALPHA, 3) * w * w * w")
m("Einstein A alpha^3", "return (4 / 3) * Math.pow(ALPHA, 3) * w * w * w",
  "return (4 / 3) * Math.pow(ALPHA, 2) * w * w * w")
m("Einstein A omega^3", "return (4 / 3) * Math.pow(ALPHA, 3) * w * w * w",
  "return (4 / 3) * Math.pow(ALPHA, 3) * w * w")
m("Einstein A omega", "const w = 0.5 / (nl * nl) - 0.5 / (nu * nu);",
  "const w = 1.0 / (nl * nl) - 1.0 / (nu * nu);")
m("Einstein A degeneracy", "const lmax = Math.max(lu, ll);", "const lmax = Math.min(lu, ll);")
m("Einstein A statistical weight", "* (lmax / (2 * lu + 1)) * R * R / T_AU;",
  "* (lmax / (2 * lu + 3)) * R * R / T_AU;")
m("Einstein A time unit", "* (lmax / (2 * lu + 1)) * R * R / T_AU;",
  "* (lmax / (2 * lu + 1)) * R * R * T_AU;")
m("selection rule delta l", "if(Math.abs(lu - ll) !== 1 || nu <= nl", "if(Math.abs(lu - ll) > 1 || nu <= nl")
m("lifetime unit", "function lifetimeNS(n, l){ const g = decayRate(n, l); return g > 0 ? 1e9 / g : Infinity; }",
  "function lifetimeNS(n, l){ const g = decayRate(n, l); return g > 0 ? 1e6 / g : Infinity; }")
m("l-average statistical weight", "const g = 2 * l + 1;\n    den += g;", "const g = 1;\n    den += g;")

# ---- the de Broglie closure -------------------------------------------
m("lambda_dB", "function lamDeBroglie(n){ return H_PLANCK / (M_E * orbitSpeed(n)); }",
  "function lamDeBroglie(n){ return H_PLANCK / (2 * M_E * orbitSpeed(n)); }")
m("closure leading 2", "function closureMismatch(nu){ return 2 * Math.abs(Math.sin(PI * nu)); }",
  "function closureMismatch(nu){ return Math.abs(Math.sin(PI * nu)); }")
m("closure argument", "function closureMismatch(nu){ return 2 * Math.abs(Math.sin(PI * nu)); }",
  "function closureMismatch(nu){ return 2 * Math.abs(Math.sin(TAU * nu)); }")
m("closure slope term", "const ds = 1 - Math.cos(TAU * nu);", "const ds = 1 + Math.cos(TAU * nu);")

# ---- air ---------------------------------------------------------------
m("Edlen leading term", "return 1 + 1e-8 * (8342.13 + 2406030 / (130 - s2) + 15997 / (38.9 - s2));",
  "return 1 + 1e-8 * (8000.00 + 2406030 / (130 - s2) + 15997 / (38.9 - s2));")
m("Edlen scale", "return 1 + 1e-8 * (8342.13 + 2406030 / (130 - s2) + 15997 / (38.9 - s2));",
  "return 1 + 1e-7 * (8342.13 + 2406030 / (130 - s2) + 15997 / (38.9 - s2));")
m("Edlen dispersion pole", "return 1 + 1e-8 * (8342.13 + 2406030 / (130 - s2) + 15997 / (38.9 - s2));",
  "return 1 + 1e-8 * (8342.13 + 2406030 / (140 - s2) + 15997 / (38.9 - s2));")
m("Edlen wavenumber unit", "const s2 = Math.pow(1000 / lamNm, 2);", "const s2 = Math.pow(1 / lamNm, 2);")
m("air divides the wrong way", "function lamAir(n1, n2){ const lv = lamVac(n1, n2); return lv / nAirEdlen(lv); }",
  "function lamAir(n1, n2){ const lv = lamVac(n1, n2); return lv * nAirEdlen(lv); }")

# ---- the seeded dice ---------------------------------------------------
m("mulberry32 increment", "a = (a + 0x6D2B79F5) | 0;", "a = (a + 0x6D2B79F6) | 0;")
m("mulberry32 first shift", "let t = Math.imul(a ^ (a >>> 15), 1 | a);", "let t = Math.imul(a ^ (a >>> 14), 1 | a);")
m("mulberry32 second mask", "t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;",
  "t = (t + Math.imul(t ^ (t >>> 7), 63 | t)) ^ t;")
m("mulberry32 the dropped addend", "t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;",
  "t = Math.imul(t ^ (t >>> 7), 61 | t) ^ t;")
m("mulberry32 divisor", "return ((t ^ (t >>> 14)) >>> 0) / 4294967296;",
  "return ((t ^ (t >>> 14)) >>> 0) / 4294967295;")
m("rng.int rounds up", "int: k => Math.min(k - 1, Math.floor(f() * k)),",
  "int: k => Math.min(k - 1, Math.ceil(f() * k)),")
m("weighted choice normalisation", "for(const it of items){ acc += it[1] / tot; if(r <= acc) return it[0]; }",
  "for(const it of items){ acc += it[1]; if(r <= acc) return it[0]; }")

# ---- PhET's stochastic model ------------------------------------------
m("PhET weight table", "const PHET_W = [[], [12.53], [3.34, 0.87], [1.36, 0.24, 0.07],",
  "const PHET_W = [[], [12.53], [3.34, 0.87], [1.36, 0.24, 0.70],")
m("PhET 2s dead end", "if(n === 2) return l === 0 ? out : [[1, 1]];",
  "if(n === 2) return [[1, 1]];")
m("PhET lower-n floor", "const lo = (l === 0) ? 2 : l;", "const lo = (l === 0) ? 2 : 1;")
m("PhET s-state floor", "const lo = (l === 0) ? 2 : l;", "const lo = (l === 0) ? 1 : l;")
m("PhET choose_l at l = 0", "if(l === 0) return [[1, 1]];", "if(l === 0) return [[0, 1]];")
m("PhET choose_l boundary", "if(l === nNew || l === nNew - 1) return [[l - 1, 1]];",
  "if(l === nNew) return [[l - 1, 1]];")
m("PhET choose_m thirds", "return [[m + 1, 1 / 3], [m - 1, 1 / 3], [m, 1 / 3]];",
  "return [[m + 1, 1 / 2], [m - 1, 1 / 4], [m, 1 / 4]];")
m("PhET selection rule delta l", "&& Math.abs(l - l2) === 1 && Math.abs(m - m2) <= 1;",
  "&& Math.abs(l - l2) <= 1 && Math.abs(m - m2) <= 1;")
m("PhET selection rule delta m", "&& Math.abs(l - l2) === 1 && Math.abs(m - m2) <= 1;",
  "&& Math.abs(l - l2) === 1 && Math.abs(m - m2) <= 2;")
m("PhET state validity", "return n >= 1 && n <= NMAX && l >= 0 && l <= n - 1 && m >= -l && m <= l;",
  "return n >= 1 && n <= NMAX && l >= 0 && l <= n && m >= -l && m <= l;")
m("Bohr picks the lower n", "while(n > 1){ const nl = 1 + rng.int(n - 1); hops.push([n, nl]); n = nl; }",
  "while(n > 1){ const nl = 1 + rng.int(n); hops.push([n, nl]); n = nl; }")

# ---- PhET's dynamics ---------------------------------------------------
m("photon speed", "photonSpeed: 300,", "photonSpeed: 280,")
m("photons across the box", "photonsAcrossBox: 20,", "photonsAcrossBox: 25,")
m("box side", "boxSide: 475,", "boxSide: 500,")
m("photon radius", "photonRadius: 15,", "photonRadius: 25,")
m("electron radius", "electronRadius: 5,", "electronRadius: 9,")
m("the absorb wait", "tAbsorb: 0.75,", "tAbsorb: 0.05,")
m("the emit wait", "tEmit: 1.0,", "tEmit: 0.05,")
m("the emission chance", "pEmit: 0.5,", "pEmit: 0.02,")
m("the plum-pudding line", "puddingLam: 150,", "puddingLam: 160,")
m("the plum-pudding absorb chance", "puddingPAbsorb: 0.5,", "puddingPAbsorb: 0.0,")
m("the classical collapse rate", "classicalDrdt: 220,", "classicalDrdt: 120,")
m("the classical spin-up", "classicalSpin: 1.008, classicalRmin: 5,", "classicalSpin: 1.0, classicalRmin: 5,")
m("the classical start radius", "classicalR0: 150, classicalOmega0: 600,", "classicalR0: 100, classicalOmega0: 600,")
m("the emission cone", "const w = PI / 8, up = PI / 2;", "const w = PI / 16, up = PI / 2;")
m("the emission direction at n >= 5", "return angle + PI + 0.1 * rng.sign() * PI;",
  "return angle + PI + 0.4 * rng.sign() * PI;")
m("the emission direction below n = 5", "if(n < 5) return rng.angle();", "if(n < 4) return rng.angle();")
m("the tick length", "const DT_TICK = 1 / 60;", "const DT_TICK = 1 / 30;")
m("PhET's drawn radii", "orbitR: [15, 44, 81, 124, 174, 233],", "orbitR: [15, 60, 135, 240, 375, 540],")
m("PhET's level heights", "levelY: [0.025, 0.6, 0.73, 0.81, 0.86, 0.9],",
  "levelY: [0, 0.75, 0.889, 0.9375, 0.96, 0.972],")
m("the true drawn radii", "function trueViewRadius(n){ return PHET.orbitR[0] * n * n; }",
  "function trueViewRadius(n){ return PHET.orbitR[0] * n; }")
m("the UV axis compression", "const UV_MAP = [[94, 94], [95, 95], [97, 97], [103, 100], [122, 105], [150, 112]];",
  "const UV_MAP = [[94, 94], [95, 95], [97, 97], [103, 103], [122, 122], [150, 150]];")
m("the visible axis is not compressed", "if(lam <= 780) return [1, (lam - 380) / (780 - 380)];",
  "if(lam <= 780) return [1, (lam - 380) / (780 - 300)];")
m("the quantum collision radius", "return Math.abs(Math.hypot(p.x, p.y) - r) <= PHET.photonRadius + 8;\n  }",
  "return Math.abs(Math.hypot(p.x, p.y) - r) <= PHET.photonRadius + 80;\n  }")
m("the metastable interval", "metastableWait: 2.0,", "metastableWait: 60.0,")
m("the metastable light mode", "if(ATOM.n === 2 && ATOM.l === 0 && st.lightOn && st.light === 'white'){",
  "if(ATOM.n === 2 && ATOM.l === 0 && st.lightOn){")

# ---- the UI (suite 'u') ------------------------------------------------
m("the pointer never marks the canvas dirty",
  "if(S.pointer('down', e.clientX - r.left, e.clientY - r.top)){ canvas.classList.add('dragging'); dirty = true; syncPanel(); }",
  "if(S.pointer('down', e.clientX - r.left, e.clientY - r.top)){ canvas.classList.add('dragging'); syncPanel(); }", "u")
m("the series drag stops moving the marker",
  "        ST.lam = Math.round(clamp(Math.pow(10, lo + (hi - lo) * f), PHET.lamMin, PHET.lamMax));",
  "        ST.lam = ST.lam;", "u")
m("the series drag stops clamping",
  "        ST.lam = Math.round(clamp(Math.pow(10, lo + (hi - lo) * f), PHET.lamMin, PHET.lamMax));",
  "        ST.lam = Math.round(Math.pow(10, lo + (hi - lo) * f));", "u")
m("the wave drag stops moving nu",
  "        ST.nu = Math.round(clamp(0.5 + (7.2 - 0.5) * (x - b.x) / b.w, 0.5, 7.2) * 20) / 20;",
  "        ST.nu = ST.nu;", "u")
m("clicking the box stops toggling the lamp",
  "        DRAG.what = 'light'; ST.lightOn = !ST.lightOn; return true;",
  "        DRAG.what = 'light'; return true;", "u")
m("a slider stops repainting",
  "      if(onchg) onchg();\n      syncPanel(); dirty = true; refresh();\n    });\n    rows[key] = {row: rowEl, sync, inp}; sync(); return rowEl;",
  "      if(onchg) onchg();\n      syncPanel(); refresh();\n    });\n    rows[key] = {row: rowEl, sync, inp}; sync(); return rowEl;", "u")
m("l is no longer clamped to n - 1", "    st.l = Math.min(st.l, st.n - 1);\n    st.m = clamp(st.m, -st.l, st.l);",
  "    st.m = clamp(st.m, -st.l, st.l);", "u")
m("m is no longer clamped to l", "    st.l = Math.min(st.l, st.n - 1);\n    st.m = clamp(st.m, -st.l, st.l);",
  "    st.l = Math.min(st.l, st.n - 1);", "u")
m("the step button steps twice", "    btn('step', () => { atomStepOnce(st); }),",
  "    btn('step', () => { atomStepOnce(st); atomStepOnce(st); }),", "u")
m("reset all forgets the atom",
  "    btn('reset all', () => { const v = st.view; Object.assign(st, DEFAULTS); st.view = v; atomReset(st); syncChips(); })));",
  "    btn('reset all', () => { const v = st.view; Object.assign(st, DEFAULTS); st.view = v; syncChips(); })));", "u")
m("the seed slider does not restart the run",
  "gTime.appendChild(slider('seed', 'random seed', 1, 999999, 1, v => fmt(v, 0), () => atomReset(st)));",
  "gTime.appendChild(slider('seed', 'random seed', 1, 999999, 1, v => fmt(v, 0)));", "u")
m("the quantum-number group is never hidden", "    gQ.hidden = (v !== 'orbitals');", "    gQ.hidden = false;", "u")
m("a paused clock still advances", "  S.step = function(dtWall){\n    if(!ST.running) return false;",
  "  S.step = function(dtWall){\n    if(false) return false;", "u")

# ---- verify each pattern is unique -------------------------------------
bad = []
for label, old, new, suite in M:
    n = SRC.count(old)
    if n != 1:
        bad.append((label, n))
for label, n in bad:
    print("PATTERN %-50s appears %d times" % (label, n), file=sys.stderr)
io.open(os.path.join(HERE, "mutants.json"), "w", encoding="utf-8").write(
    json.dumps(M, indent=1, ensure_ascii=False))
print("%d mutants (%d physics, %d ui); %d bad patterns"
      % (len(M), sum(1 for x in M if x[3] == "p"), sum(1 for x in M if x[3] == "u"), len(bad)))
sys.exit(1 if bad else 0)
