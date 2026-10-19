#!/usr/bin/env python3
"""Copy in the parts this sim shares with the finished gas-properties remake.

The brief's rule is to build ON that work, not to re-derive it.  Four blocks
come across, each with a provenance banner and none of them edited:

  p1_utils.js    the shared house layer (throwing toRgb, plain() that strips
                 tags and decodes numeric entities inside the wide match,
                 Liang-Barsky polyline, guarded logTicks, recorded legends) —
                 build/gas-properties/p1_utils.js, itself verbatim from
                 projects/simulations/build_lagr/p1_utils.js.
  p2_engine.js   the event-driven hard-disk gas.  No DOM, no view state; its
                 API, step algorithm and invariants are in
                 build/gas-properties/ENGINE.md and its Python twin is
                 build/gas-properties/derive.py.
  p4a_helpers.js worldFitUp, lab/axesR and the label registry, stageLayout,
                 marker — build/gas-properties/p4a_helpers.js.
  p4s_scene.js   the container scene and the small-plot layer, sliced out of
                 build/gas-properties/p4_views.js: HINT_H and viewGeo (driven
                 entirely by this file's own SCENE table), drawContainer ..
                 sceneCaption, and niceRange/plotSeries/plotNote/tickFmt/
                 emptyNote.  The view-specific halves of that file (its SCENE,
                 captionFor and drawIdeal/drawExplore/drawEnergy) are NOT
                 taken; this sim writes its own.

Nothing in build/gas-properties/ is written to.
"""
import io, os

here = os.path.dirname(os.path.abspath(__file__))
gp = os.path.abspath(os.path.join(here, '..', 'gas-properties'))


def read(fn):
    return io.open(os.path.join(gp, fn), encoding='utf-8').read()


def banner(what, src):
    return ('/* ================================================================== *\n'
            ' *  %-64s*\n'
            ' *  Taken UNCHANGED from %-42s*\n'
            ' *  (the finished gas-properties remake).  Do not edit here.          *\n'
            ' * ================================================================== */\n'
            % (what, src))


# --- the three whole files -------------------------------------------------
utils = read('p1_utils.js')
assert 'function polyline(' in utils and 'function plain(' in utils and 'function axes(' in utils
io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

eng = read('p2_engine.js')
for want in ['const GAS={', 'function gasMake(', 'function gasStep(', 'function gasPredict(',
             'function pairResolve(', 'function gasSetHold(', 'const GAS_OOPS=']:
    assert want in eng, want
io.open(os.path.join(here, 'p2_engine.js'), 'w', encoding='utf-8').write(
    banner('the gas engine', 'build/gas-properties/p2_engine.js') + eng)

helpers = read('p4a_helpers.js')
assert 'function axesR(' in helpers and 'function lab(' in helpers and 'function worldFitUp(' in helpers
io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)

# --- the two generic slices of p4_views.js ---------------------------------
v = read('p4_views.js')
a0 = v.index('/* the house #hint is HTML')
a1 = v.index('function captionFor(')
blockA = v[a0:a1].rstrip() + '\n'
b0 = v.index('/* ---- the container ---')
b1 = v.index('/* ================================================================== *\n *  the gas law')
blockB = v[b0:b1].rstrip() + '\n'
for want in ['const HINT_H=18;', 'function viewGeo(']:
    assert want in blockA, want
for want in ['function drawContainer(', 'function drawParticles(', 'function drawHandles(',
             'function drawPump(', 'function drawThermometer(', 'function drawGauge(',
             'function drawHeater(', 'function drawRuler(', 'function drawTools(',
             'function oopsGeo(', 'function drawOops(', 'function drawScene(',
             'function sceneCaption(', 'function niceRange(', 'function plotSeries(',
             'function plotNote(', 'function tickFmt(', 'function emptyNote(']:
    assert want in blockB, want
assert 'function captionFor(' not in blockA + blockB
assert 'const SCENE=' not in blockA + blockB

# The one adaptation.  gas-properties asks its OWN view names ('ideal',
# 'explore', 'diffusion', 'energy') inside these generic routines; this sim has
# different ones.  Each such test becomes a named hook that this sim defines in
# p4_views.js, and every substitution must match exactly once or the build
# stops — so the block cannot silently drift out from under the rewrite.
SUBS = [
    ("const wDraw=(M.view==='ideal'&&M.w.dragW!==null)?M.w.dragW:g.W;",
     "const wDraw=(dragPauses(M)&&M.w.dragW!==null)?M.w.dragW:g.W;"),
    ("const wallOK=(v==='ideal'&&g.hold!=='volume'&&g.hold!=='pressureV')||v==='explore';",
     "const wallOK=wallDraggable(M);"),
    ("const lidOK=g.lid&&g.lid.on&&!(v==='ideal'&&g.hold==='temperature');",
     "const lidOK=lidDraggable(M);"),
    ("const locked=M.view==='ideal'&&(g.hold==='temperature'||g.hold==='pressureT');",
     "const locked=heaterLocked(M);"),
    ("if(g.divided||M.view==='diffusion'){",
     "if(g.divided||dividerShown(M)){"),
    ("const y=G.yB+(M.view==='diffusion'?22:14), g=M.g;",
     "const y=G.yB+(scaleBar(M)?22:14), g=M.g;"),
    ("  if(M.view==='diffusion'){\n    /* PhET's Scale: a bar with a tick every nanometre */",
     "  if(scaleBar(M)){\n    /* PhET's Scale: a bar with a tick every nanometre */"),
    ("if(o.ruler&&(M.view!=='diffusion'?M.st.showWidth:M.st.dScale)) drawRuler(ctx,G,M,W,H);",
     "if(o.ruler&&rulerOn(M)) drawRuler(ctx,G,M,W,H);"),
    ("if(M.view==='explore') drawWallVelocity(ctx,G,M);",
     "if(wallVelocity(M)) drawWallVelocity(ctx,G,M);"),
    ("if(st.showCounter&&M.view!=='energy'){",
     "if(st.showCounter&&counterOn(M)){"),
    ("drawParticles(ctx,G,M.g,M.view==='ideal'&&M.w.dragW!==null);",
     "drawParticles(ctx,G,M.g,dragPauses(M)&&M.w.dragW!==null);"),
]
scene = blockA + '\n' + blockB
for old, new in SUBS:
    assert scene.count(old) == 1, ('substitution not unique', old[:70], scene.count(old))
    scene = scene.replace(old, new)
assert "M.view==='ideal'" not in scene and "M.view==='explore'" not in scene
assert "M.view==='diffusion'" not in scene and "M.view==='energy'" not in scene
assert "v==='ideal'" not in scene and "v==='explore'" not in scene
io.open(os.path.join(here, 'p4s_scene.js'), 'w', encoding='utf-8').write(
    banner('the container scene and the small-plot layer',
           'build/gas-properties/p4_views.js')
    + '/*  The ONLY change: eleven tests on gas-properties own view names      *\n'
      ' *  became the hooks dragPauses / wallDraggable / lidDraggable /        *\n'
      ' *  heaterLocked / scaleBar / rulerOn / wallVelocity / counterOn /      *\n'
      ' *  dividerShown, which this sim defines in p4_views.js.                *\n'
      ' *  make_shared.py asserts each substitution matches exactly once.      */\n'
    + '\n' + scene)

print('shared: p1_utils.js %d, p2_engine.js %d, p4a_helpers.js %d, p4s_scene.js %d lines'
      % (len(utils.splitlines()), len(eng.splitlines()), len(helpers.splitlines()),
         len((blockA + blockB).splitlines())))
