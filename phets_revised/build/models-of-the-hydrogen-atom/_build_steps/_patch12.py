#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The rest of the first sweep's survivors.

Three shapes, all on the Known-bad list:
  * a pin that recomputes the constant it is pinning, so it moves WITH the
    mutant instead of failing on it (the classical spiral, three constants);
  * a guard written twice, so either copy's mutant is equivalent (the l/m
    clamp, in the slider handler and again in syncPanel);
  * a repaint asserted against a FORCED draw rather than through the frame
    loop, so the dirty flag is not actually tested (the slider, and the
    pointerdown-only action).
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(fname, pairs):
    p = os.path.join(HERE, fname)
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, ("%s: %r appears %d times" % (fname, old[:70], s.count(old)))
        s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(s)
    print(fname, "patched")


patch("p7_test.js", [
    # --- the classical spiral, against PhET's literal values ---------------
    ("""  rel(tDead, (PHET.classicalR0 - PHET.classicalRmin) / PHET.classicalDrdt, 0.02,
    'it collapses in (150-5)/220 = 0.659 s');""",
     """  rel(tDead, (150 - 5) / 220, 0.02, 'it collapses in (150 - 5)/220 = 0.6591 s (PhET)');
  eq(PHET.classicalR0, 150, 'the classical electron starts 150 units out (PhET)');
  eq(PHET.classicalDrdt, 220, 'and loses 220 units of radius a second (PhET)');
  eq(PHET.classicalRmin, 5, 'and is destroyed at 5 units (PhET)');
  eq(PHET.classicalOmega0, 600, 'starting at 600 deg/s (PhET)');
  /* the radius really is linear in time, which is what makes 0.659 s the answer */
  {
    Object.assign(ST, DEFAULTS, {model: 'classical', lightOn: false});
    atomReset(ST);
    for(let k = 0; k < 20; k++) atomTick(ST);
    rel(ATOM.cls.r, 150 - 220 * 20 * DT_TICK, 1e-9, 'the radius falls linearly, 220 units a second');
    for(let k = 0; k < 10; k++) atomTick(ST);
    rel(ATOM.cls.r, 150 - 220 * 30 * DT_TICK, 1e-9, 'and keeps falling at the same rate');
  }"""),
    # --- the metastable handler runs ONLY in white light -------------------
    ("""  for(let k = 0; k < 400; k++) atomTick(ST);
  eq(ATOM.metaT, 0, 'the metastable handler does not run in monochromatic light (PhET)');""",
     """  let metaInMono = false;
  for(let k = 0; k < 400; k++){
    atomTick(ST);
    for(const p of ATOM.photons) if(p.meta) metaInMono = true;
  }
  ok(!metaInMono, 'the metastable handler fires NO photon in monochromatic light (PhET)');
  eq(ATOM.n, 2, 'so a 2s atom stays stuck at n = 2 under a 122 nm lamp');
  eq(ATOM.metaT, 0, 'and its timer never starts');"""),
])

patch("p3_state.js", [
    # --- the atom's tick length, stated once ------------------------------
    ("const DT_TICK = 1 / 60;", "const DT_TICK = 1 / 60;                 /* PhET's own frame on a 60 Hz display */"),
])

patch("p6_boot.js", [
    # --- one clamp, in syncPanel, which runs after every change ------------
    ("""  gQ.appendChild(slider('n', 'n', 1, NMAX, 1, v => fmt(v, 0), () => {
    st.l = Math.min(st.l, st.n - 1); st.m = clamp(st.m, -st.l, st.l);
  }));
  gQ.appendChild(slider('l', 'l', 0, NMAX - 1, 1, v => fmt(v, 0), () => {
    st.l = Math.min(st.l, st.n - 1); st.m = clamp(st.m, -st.l, st.l);
  }));
  gQ.appendChild(slider('m', 'm', -(NMAX - 1), NMAX - 1, 1, v => fmt(v, 0), () => {
    st.m = clamp(st.m, -Math.min(st.l, st.n - 1), Math.min(st.l, st.n - 1));
  }));""",
     """  /* l <= n-1 and |m| <= l are clamped in ONE place, syncPanel, which runs
     after every control change.  Clamping here as well made either copy's
     mutant equivalent and the sweep reported it as a survivor (Known-bad). */
  gQ.appendChild(slider('n', 'n', 1, NMAX, 1, v => fmt(v, 0)));
  gQ.appendChild(slider('l', 'l', 0, NMAX - 1, 1, v => fmt(v, 0)));
  gQ.appendChild(slider('m', 'm', -(NMAX - 1), NMAX - 1, 1, v => fmt(v, 0)));"""),
])

patch("ui_drive_models-of-the-hydrogen-atom.js", [
    # --- a slider's repaint has to be taken through the FRAME LOOP ---------
    ("""  const sl = uFindSlider('n');
  UREC = uMakeRec();
  sl.value = '5'; sl.fire('input');
  uok(UREC.ops.length > 50, 'moving n repaints at once (' + UREC.ops.length + ' ops)');
  uok(ST.n === 5, 'and the model followed the slider');""",
     """  const sl = uFindSlider('n');
  UREC = uMakeRec();
  sl.value = '5'; sl.fire('input');
  uok(UREC.ops.length > 50, 'moving n repaints at once (' + UREC.ops.length + ' ops)');
  uok(ST.n === 5, 'and the model followed the slider');
  /* refresh() draws unconditionally, so the draw above says nothing about the
     dirty flag.  The frame loop is the only path on which it matters, and the
     next pumped frame has to repaint too (Known-bad, three times). */
  UREC = uMakeRec(); upump(3);
  uok(UREC.ops.length > 50, 'and the frame loop repaints it as well (the dirty flag is set)');
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC) === '[]', 'then it goes quiet again');"""),
    # --- a pointerdown-ONLY action: pointermove sets dirty by itself, so a
    #     down-move-up sequence cannot test the pointerdown handler's flag
    ("""uClickTab('box');
{
  const on0 = ST.lightOn;
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  uok(ST.lightOn !== on0, 'clicking inside the box toggles the lamp');
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  uok(ST.lightOn === on0, 'and clicking again puts it back');
}""",
     """uClickTab('box');
{
  /* stop the clock, or the box view repaints every frame and no dirty-flag
     test on it can mean anything */
  const cb0 = uFindLabelled('time runs');
  if(cb0 && cb0.checked){ cb0.checked = false; cb0.fire('change'); }
  upump(4);
  uok(uFrameGeom(3) === '[]', 'with the clock stopped the box view is idle');
  const on0 = ST.lightOn;
  UREC = uMakeRec();
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  upump(3);
  uok(uGeom(UREC).length > 50, 'a pointerdown ALONE repaints (only that handler sets dirty)');
  uok(ST.lightOn !== on0, 'clicking inside the box toggles the lamp');
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  uok(ST.lightOn === on0, 'and clicking again puts it back');
  if(cb0){ cb0.checked = true; cb0.fire('change'); }
}"""),
    # --- the seed slider restarts the atom AT ONCE, not lazily -------------
    ("""  const sd = uFindSlider('random seed');
  sd.value = '777'; sd.fire('input');
  upump(240);""",
     """  const sd = uFindSlider('random seed');
  uok(ATOM.t > 0, 'the clock has run before the seed is changed');
  sd.value = '777'; sd.fire('input');
  uok(ATOM.t === 0 && ATOM.emitted === 0,
    'changing the seed restarts the atom immediately, not on the next frame');
  upump(240);"""),
    # --- the l/m clamp now lives only in syncPanel, so assert it there ------
    ("""  const sll = uFindSlider('l'), slm = uFindSlider('m');
  sll.value = '5'; sll.fire('input');
  uok(ST.l === 4, 'l is clamped to n - 1 (' + ST.l + ')');""",
     """  const sll = uFindSlider('l'), slm = uFindSlider('m');
  sll.value = '5'; sll.fire('input');
  uok(ST.l === 4, 'l is clamped to n - 1 by syncPanel (' + ST.l + ')');"""),
])

patch("gen_mutants.py", [
    # the l/m clamp is now a single statement in syncPanel
    ("""m("l is no longer clamped to n - 1", "    st.l = Math.min(st.l, st.n - 1);\\n    st.m = clamp(st.m, -st.l, st.l);\\n    if(rows.l.inp)",
  "    st.m = clamp(st.m, -st.l, st.l);\\n    if(rows.l.inp)", "u")""",
     """m("l is no longer clamped to n - 1", "    st.l = Math.min(st.l, st.n - 1);\\n    st.m = clamp(st.m, -st.l, st.l);",
  "    st.m = clamp(st.m, -st.l, st.l);", "u")
m("m is no longer clamped to l", "    st.l = Math.min(st.l, st.n - 1);\\n    st.m = clamp(st.m, -st.l, st.l);",
  "    st.l = Math.min(st.l, st.n - 1);", "u")"""),
    # the Condon-Shortley phase is provably invisible: keep it out of the sweep
    # and assert the invariance instead (see p7_test.js)
    ("""m("Legendre P_m^m sign", "for(let i = 1; i <= m; i++){ pmm *= -f * somx2; f += 2; }",
  "for(let i = 1; i <= m; i++){ pmm *= f * somx2; f += 2; }")
""", ""),
])
