#!/usr/bin/env python3
"""gen_mutants.py -- write mutants.json for gravity-and-orbits.html.

Every physics mutant breaks ONE leading coefficient, exponent, unit conversion
or sign; every UI mutant breaks one link between an interaction and the
drawing.  Each `old` is checked to appear EXACTLY ONCE in the extracted script
before it is written, because mutate.py skips a pattern that does not (and a
skipped mutant is one you think you ran and did not).

Nothing here changes a loop condition that has to converge: mutate.py has no
per-mutant timeout, so a non-terminating mutant stalls the whole sweep.
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.normpath(os.path.join(HERE, '..', '..', 'gravity-and-orbits.html'))

M = []


def p(label, old, new):
    M.append([label, old, new, 'p'])


def u(label, old, new):
    M.append([label, old, new, 'u'])


# ---- PhET's constants: every one of them is quoted on the page ---------------
p('G', 'const G_SI = 667408e-16;', 'const G_SI = 667408e-15;')
p('sun mass', 'SUN_MASS: 1.989e30,', 'SUN_MASS: 1.889e30,')
p('earth mass', 'EARTH_MASS: 59724e20,', 'EARTH_MASS: 59724e21,')
p('moon mass', 'MOON_MASS: 7346e19,', 'MOON_MASS: 7346e20,')
p('station mass', 'STATION_MASS: 419725,                  /* bp.SPACE_STATION_MASS */',
  'STATION_MASS: 519725,                  /* bp.SPACE_STATION_MASS */')
p('sun radius', 'SUN_RADIUS: 6957e5,', 'SUN_RADIUS: 6957e6,')
p('earth radius', 'EARTH_RADIUS: 6371e3,', 'EARTH_RADIUS: 6371e4,')
p("moon radius (PhET's 1727.4 km, not the measured 1737.4)",
  'MOON_RADIUS: 1727400,', 'MOON_RADIUS: 1737400,')
p('station radius', 'STATION_RADIUS: 45.5,', 'STATION_RADIUS: 91,')
# e3 -> e4, not e2: a ten-times-closer Earth needs 193 substeps a frame and the sweep crawls
p('earth-sun distance', 'EARTH_X: 147098074e3,', 'EARTH_X: 147098074e4,')
p('earth speed', 'EARTH_VY: 30300,', 'EARTH_VY: 30200,')
p('moon distance', 'MOON_Y: 3633e5,', 'MOON_Y: 3633e6,')
p('moon speed sign', 'MOON_VX: -1082,', 'MOON_VX: 1082,')
p('station orbit radius', 'STATION_X: 6718045.5,', 'STATION_X: 6818045.5,')
p('station speed', 'STATION_VY: 7706,', 'STATION_VY: 7606,')
p('the day', 'DAY: 86400,', 'DAY: 8640,')
# 36e3 -> 36e2, not 36e4: a ten-times-longer frame is ten times as many substeps
p('the base step', 'DEFAULT_DT: 36e3,', 'DEFAULT_DT: 36e2,')
p("PhET's substep fraction", 'SUBSTEP: 0.13125,', 'SUBSTEP: 0.0625,')
p('the speed steps', 'SPEED_STEPS: [1, 4, 7],', 'SPEED_STEPS: [1, 4, 8],')
p('the view scale', 'VIEW_SCALE: 1.5e-9,', 'VIEW_SCALE: 1.5e-8,')
p('the stage height', 'STAGE_W: 987.5, STAGE_H: 772.5,', 'STAGE_W: 987.5, STAGE_H: 672.5,')
p("the moon boost", 'MOON_BOOST: 10200,', 'MOON_BOOST: 10100,')
p('the planet exaggeration', 'MODEL_PLANET_R: 800,', 'MODEL_PLANET_R: 400,')
p("the model moon's speed factor", 'MODEL_MOON_VX: 21,', 'MODEL_MOON_VX: 20,')
p("the model moon's distance", 'MODEL_MOON_Y_R: 1.7,', 'MODEL_MOON_Y_R: 1.6,')
p('the station exaggeration', 'MODEL_SAT_R: 2e4', 'MODEL_SAT_R: 2e5')
p('the sun exaggeration', 'MODEL_SUN_R: 50,', 'MODEL_SUN_R: 25,')
p('the planet-moon exaggeration', 'MODEL_PM_R: 15,', 'MODEL_PM_R: 30,')
p('the model planet shrink', 'MODEL_SAT_PLANET_R: 0.8,', 'MODEL_SAT_PLANET_R: 1.0,')

# ---- the measured column ----------------------------------------------------
p('measured moon radius', 'MOON_RADIUS: 1737.4e3,', 'MOON_RADIUS: 1727.4e3,')
p('measured sun mass', 'SUN_MASS: 1988400e24,', 'SUN_MASS: 1998400e24,')
p('measured earth mass', 'EARTH_MASS: 5.9722e24,', 'EARTH_MASS: 5.9724e24,')

# ---- the force law ----------------------------------------------------------
p('the inverse-square exponent', 'const f = k * G_SI * S.m[j] / (r2 * r);',
  'const f = k * G_SI * S.m[j] / (r2 * r2);')
p('the mass in the force', 'const f = k * G_SI * S.m[j] / (r2 * r);',
  'const f = k * G_SI * S.m[i] / (r2 * r);')
p('the sign of gravity', 'S.ax[i] += f * dx; S.ay[i] += f * dy;', 'S.ax[i] -= f * dx; S.ay[i] -= f * dy;')
p('the boost is one-sided', "(S.boost !== 1 && S.kind[i] === 'moon' && S.kind[j] === 'planet') ? S.boost : 1",
  "(S.boost !== 1 && S.kind[j] === 'moon' && S.kind[i] === 'planet') ? S.boost : 1")
p('the force arrow is F = m a', 'out.push([S.ax[i] * S.m[i], S.ay[i] * S.m[i]]);',
  'out.push([S.ax[i], S.ay[i]]);')

# ---- the integrator ---------------------------------------------------------
p('the drift moves x by v_x', 'if(S.fix[i]) continue; S.x[i] += c * S.vx[i]; S.y[i] += c * S.vy[i];',
  'if(S.fix[i]) continue; S.x[i] += c * S.vy[i]; S.y[i] += c * S.vx[i];')
p('the kick sign', 'if(S.fix[i]) continue; S.vx[i] += c * S.ax[i]; S.vy[i] += c * S.ay[i];',
  'if(S.fix[i]) continue; S.vx[i] -= c * S.ax[i]; S.vy[i] -= c * S.ay[i];')
p('PEFRL xi', 'const PEFRL_XI = 0.1786178958448091', 'const PEFRL_XI = 0.1886178958448091')
p('PEFRL lambda', 'PEFRL_LAM = -0.2123418310626054', 'PEFRL_LAM = -0.2223418310626054')
p('PEFRL chi', 'PEFRL_CHI = -0.06626458266981849', 'PEFRL_CHI = -0.07626458266981849')
p('the middle drift', 'goKick(S, PEFRL_LAM * h);\n  goDrift(S, (1 - 2 * (PEFRL_CHI + PEFRL_XI)) * h);',
  'goKick(S, PEFRL_LAM * h);\n  goDrift(S, (1 - 1 * (PEFRL_CHI + PEFRL_XI)) * h);')
# NOT "call goAccel twice" -- that recomputes the same numbers and is an equivalent mutant.
# Making the kicks read the LIVE acceleration turns PhET's step into the real PEFRL, which the
# measured order (0.995) pins.
p("PhET's step reuses ONE acceleration",
  '  const kick = c => { for(let i = 0; i < n; i++){ if(S.fix[i]) continue; S.vx[i] += c * ax[i]; S.vy[i] += c * ay[i]; } };',
  '  const kick = c => goKick(S, c);')
# r^3 -> r^4, not r^3 -> r^2: the exponent has to move the limit UP.  Down, it asks for 74,000
# substeps a frame on the Sun-Earth scene, and the suite -- which does not abort on a failed
# assertion -- then grinds for the best part of an hour before reporting a mutant it had
# already caught in its third section.  mutate.py has no per-mutant timeout.
p('the step limit is a free-fall time', 'tau = Math.min(tau, Math.sqrt(r * r * r / (k * G_SI * (S.m[i] + S.m[j]))));',
  'tau = Math.min(tau, Math.sqrt(r * r * r * r / (k * G_SI * (S.m[i] + S.m[j]))));')
p('the crossing-time limit', 'if(dv > 0) tau = Math.min(tau, r / dv);\n  }\n  return isFinite(tau) ? GO_ETA * tau : Infinity;',
  'if(dv > 0) tau = Math.min(tau, r * dv);\n  }\n  return isFinite(tau) ? GO_ETA * tau : Infinity;')
p('eta', 'const GO_ETA = 0.02;', 'const GO_ETA = 0.2;')
p('the substep count', 'const n = Math.max(1, Math.ceil(Math.abs(dt) / lim));\n  const h = dt / n, step = stepFn || goPefrl;',
  'const n = Math.max(1, Math.ceil(Math.abs(dt) / lim / 4));\n  const h = dt / n, step = stepFn || goPefrl;')
p('gravity off is ONE drift', 'if(!gravity){ goDrift(S, dt); return 1; }',
  'if(!gravity){ goDrift(S, dt); goDrift(S, dt); return 1; }')
p('the order-sweep window', 'return T / 9;', 'return T / 3;')

# ---- the scene builders -----------------------------------------------------
p('the centre-of-momentum shift', 'b.vx -= px / M; b.vy -= py / M;', 'b.vx += px / M; b.vy += py / M;')
p('the planet-moon hand shift', "const vp = -PH.MOON_VX * PH.MOON_MASS / (PH.EARTH_MASS + PH.MOON_MASS)",
  "const vp = -PH.MOON_VX * PH.EARTH_MASS / (PH.EARTH_MASS + PH.MOON_MASS)")
p('the planet-moon grid step', 'grid: PH.MOON_Y / 2,', 'grid: PH.MOON_Y,')
p('the star-planet grid step', 'grid: PH.EARTH_X / 2, minutes: false,\n    bodies: [bodyCfg(\'Our Sun\', \'star\', PH.SUN_MASS, PH.SUN_RADIUS, 0, 0, 0, 0),\n             bodyCfg(\'Earth\', \'planet\', PH.EARTH_MASS, PH.EARTH_RADIUS, PH.EARTH_X, 0, 0, PH.EARTH_VY)]};',
  'grid: PH.EARTH_X / 4, minutes: false,\n    bodies: [bodyCfg(\'Our Sun\', \'star\', PH.SUN_MASS, PH.SUN_RADIUS, 0, 0, 0, 0),\n             bodyCfg(\'Earth\', \'planet\', PH.EARTH_MASS, PH.EARTH_RADIUS, PH.EARTH_X, 0, 0, PH.EARTH_VY)]};')
p('the planet-moon scene dt', "dt: PH.DEFAULT_DT / 3,", "dt: PH.DEFAULT_DT / 2,")
p('the station scene dt', "dt: 9e-4 * PH.DEFAULT_DT,", "dt: 9e-5 * PH.DEFAULT_DT,")
p('the planet-moon zoom', 'zoom: 400,', 'zoom: 200,')
p('the station zoom', 'zoom: 21600,', 'zoom: 10800,')
p('the star-planet zoom', "id: sid, zoom: 1.25, dt: PH.DEFAULT_DT, grid: PH.EARTH_X / 2, minutes: false,\n    bodies:", "id: sid, zoom: 2.5, dt: PH.DEFAULT_DT, grid: PH.EARTH_X / 2, minutes: false,\n    bodies:")
p('the star is nailed down', "b[0].fixed = true;\n      cfg.boost = PH.MOON_BOOST;",
  "b[0].fixed = false;\n      cfg.boost = PH.MOON_BOOST;")
p('a fixed body does not drift', 'for(let i = 0; i < S.n; i++){ if(S.fix[i]) continue; S.x[i] += c * S.vx[i]; S.y[i] += c * S.vy[i]; }',
  'for(let i = 0; i < S.n; i++){ S.x[i] += c * S.vx[i]; S.y[i] += c * S.vy[i]; }')
p('the view half-height', 'return PH.STAGE_H / (2 * PH.VIEW_SCALE * cfg.zoom * (level || 1));',
  'return PH.STAGE_H / (PH.VIEW_SCALE * cfg.zoom * (level || 1));')
p('the frame length', 'return PH.SUBSTEP * cfg.dt * steps;', 'return PH.SUBSTEP * cfg.dt;')

# ---- the closed forms -------------------------------------------------------
p('the circular speed', 'function circSpeed(M, r){ return Math.sqrt(G_SI * M / r); }',
  'function circSpeed(M, r){ return Math.sqrt(G_SI * M / (r * r)); }')
p('the circular period', 'function circPeriod(M, r){ return TAU * Math.sqrt(r * r * r / (G_SI * M)); }',
  'function circPeriod(M, r){ return TAU * Math.sqrt(r * r / (G_SI * M)); }')
p('the two-body mu', 'const mu = G_SI * (S.m[0] + S.m[1]);', 'const mu = G_SI * S.m[0];')
p('the fixed-centre mu', 'const mu = G_SI * S.m[0];\n    return {kind: ', 'const mu = G_SI * (S.m[0] + S.m[1]);\n    return {kind: ')
p('the mass split', "  return {kind: 'free', mu, el, cx: c.x, cy: c.y, cvx: c.vx, cvy: c.vy,\n"
  "          f1: S.m[1] / (S.m[0] + S.m[1]), f2: S.m[0] / (S.m[0] + S.m[1])};",
  "  return {kind: 'free', mu, el, cx: c.x, cy: c.y, cvx: c.vx, cvy: c.vy,\n"
  "          f1: S.m[0] / (S.m[0] + S.m[1]), f2: S.m[1] / (S.m[0] + S.m[1])};")
p('the sign of the mass split', 'return {x1: cx - ref.f1 * s.x, y1: cy - ref.f1 * s.y,',
  'return {x1: cx + ref.f1 * s.x, y1: cy + ref.f1 * s.y,')
p('the centre of mass drifts in a line', 'const cx = ref.cx + ref.cvx * t, cy = ref.cy + ref.cvy * t;',
  'const cx = ref.cx, cy = ref.cy;')

# ---- PhET's own readout rules ----------------------------------------------
p("the Earth-mass thousands rule", "if(e > 1000) return fmt(Math.round(e / 1000), 0)",
  "if(e > 100) return fmt(Math.round(e / 1000), 0)")
p("the 'one Earth mass' window", "if(Math.abs(e - 1) < 0.01) return '1 Earth mass';",
  "if(Math.abs(e - 1) < 0.1) return '1 Earth mass';")
p("the billion-billions rule", "if(e > 1e18) return fmt(e / 1e18, 0)", "if(e > 1e17) return fmt(e / 1e17, 0)")
p('the kilometre', "function kmStr(m, sig){ return sci(m / 1e3, sig || 4) + ' km'; }",
  "function kmStr(m, sig){ return sci(m / 1e2, sig || 4) + ' km'; }")
p('the megametre', "if(a >= 1e6) return sci(m / 1e6, s) + ' Mm';", "if(a >= 1e6) return sci(m / 1e5, s) + ' Mm';")
p('the digit superscripts', "let out = n < 0 ? '⁻' : '';", "let out = n < 0 ? '-' : '';")
p('Earth days', "return fmt(t / PH.DAY, 0) + ' Earth days';", "return fmt(t / PH.DAY / 2, 0) + ' Earth days';")
p('Earth minutes', "if(minutes) return fmt(t / 60, 0) + ' Earth minutes';",
  "if(minutes) return fmt(t / 3600, 0) + ' Earth minutes';")
p('the AU', 'const AU_M = 149597870.7e3;', 'const AU_M = 149597870.7e2;')

# ---- the state layer --------------------------------------------------------
p('the velocity-arrow scale', 'const VEL_PX = 90;', 'const VEL_PX = 45;')
p('the force-arrow scale', 'const FSCALE = 60;', 'const FSCALE = 30;')
p('the reference speed', 'v = Math.max(v, Math.hypot(sys.start[i][3] - sys.start[0][3], sys.start[i][4] - sys.start[0][4]));',
  'v = Math.max(v, Math.hypot(sys.start[i][3], sys.start[i][4]));')
p('the reference pull', 'return G_SI * s[0][0] * s[1][0] / (r * r);', 'return G_SI * s[0][0] * s[1][0] / (r * r * r);')
p('the mass slider is a multiple of the default', 'S.m[i] = defaultMass(sys, i) * mult;',
  'S.m[i] = defaultMass(sys, i) + mult;')

# ---- UI: the links between an action and the drawing ------------------------
u('the drag sets the dirty flag', "if(S.pointer('move', e.clientX - r.left, e.clientY - r.top)){ dirty = true;",
  "if(S.pointer('move', e.clientX - r.left, e.clientY - r.top)){ dirty = false;")
# the grab's own repaint comes from refresh(), not from a dirty flag -- there is no flag there
# to mutate any more (a redundant one survived a sweep).  What IS load-bearing on that path is
# the dragging class, which is what lets pointermove run with no button held.
u('the grab marks the canvas as dragging',
  "if(S.pointer('down', e.clientX - r.left, e.clientY - r.top)){ canvas.classList.add('dragging'); syncPanel(); refresh(); }",
  "if(S.pointer('down', e.clientX - r.left, e.clientY - r.top)){ syncPanel(); refresh(); }")
u('the body drag restarts the clock', """        st.x[DRAGM.i] = clamp(wx, c[0] - R, c[0] + R);
        st.y[DRAGM.i] = clamp(wy, c[1] - R, c[1] + R);
        sys.t = 0; sysClearPaths(sys);""",
  """        st.x[DRAGM.i] = clamp(wx, c[0] - R, c[0] + R);
        st.y[DRAGM.i] = clamp(wy, c[1] - R, c[1] + R);
        sysClearPaths(sys);""")
u('the velocity drag inverts the arrow scale',
  'st.vx[DRAGM.i] = (x - X) / M.vscale; st.vy[DRAGM.i] = -(y - Y) / M.vscale;',
  'st.vx[DRAGM.i] = (x - X) * M.vscale; st.vy[DRAGM.i] = -(y - Y) * M.vscale;')
u('the drag saves the new start', "if(had && (DRAGM.what === 'body' || DRAGM.what === 'vel')) sysSaveStart(curSys());",
  "if(false) sysSaveStart(curSys());")
u('a tab selects its screen', "if(k === 'model' || k === 'scale') st.screen = k;",
  "if(false) st.screen = k;")
u('the g key flips gravity', "else if(e.key === 'g'){ st.gravity = !st.gravity;",
  "else if(e.key === 'g'){ st.gravity = st.gravity;")
u('the slider redraws at once', "val.innerHTML = fmtf(st[key]); syncPanel(); dirty = true; refresh();",
  "val.innerHTML = fmtf(st[key]); syncPanel(); dirty = false;")
u('the checkbox redraws at once', "st[key] = inp.checked; if(onchg) onchg(); syncPanel(); dirty = true; refresh();",
  "st[key] = inp.checked; if(onchg) onchg(); syncPanel();")
u('the power slider is disabled until the arrows are on', "enable('fpow', st.force);", "enable('fpow', true);")
u('the screen chips are disabled on the two PhET screens',
  "[].forEach.call(scrChips.children, c => { c.disabled = (v === 'model' || v === 'scale'); });",
  "[].forEach.call(scrChips.children, c => { c.disabled = false; });")
u('the step button takes one frame', "const was = st.running; st.running = true; runStep(); st.running = was;",
  "const was = st.running; st.running = true; runStep(); runStep(); st.running = was;")
u('the tape end follows the pointer', "if(DRAGM.what === 'tapeB'){ sys.tape.bx = wx; sys.tape.by = wy; return true; }",
  "if(DRAGM.what === 'tapeB'){ sys.tape.bx = wx; return true; }")
u('a body too small to see gets a pointer', 'return {X, Y, rp, dTrue, tiny: dTrue <= 12};',
  'return {X, Y, rp, dTrue, tiny: false};')
u('the mass readout follows the scene',
  "return sid === 'planetSatellite' ? stationMassStr(S.m[i]) : earthMassStr(S.m[i]);",
  "return earthMassStr(S.m[i]);")


def main():
    s = io.open(HTML, encoding='utf-8').read().split('<script>', 1)[1].rsplit('</script>', 1)[0]
    bad = [(lab, s.count(old)) for lab, old, _, _ in M if s.count(old) != 1]
    for lab, n in bad:
        print('!! %-50s appears %d times' % (lab, n))
    io.open(os.path.join(HERE, 'mutants.json'), 'w', encoding='utf-8').write(
        json.dumps(M, indent=0))
    print('mutants.json: %d mutants (%d physics, %d UI), %d unusable'
          % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u'), len(bad)))
    return 1 if bad else 0


if __name__ == '__main__':
    raise SystemExit(main())
