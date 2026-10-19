#!/usr/bin/env python3
"""Write ui_drive_ph-scale-basics.js from build/ph-scale/ui_drive_ph-scale.js.

The two harnesses share every helper (the recording context, the DOM stub with its
plain()-decoding innerHTML setter, the whole-label slider finder, the arity-checked chip
finder, the proven-idle helper) and the whole beaker half of the drive: the clock, the two
volume sliders with their brim clamp, the probe drag, the twelve liquids and the two
dilution laws.  What this build changes is the counts that differ (four tabs, six panel
groups, six inputs), the op floors, the credit line it looks for, the readout rows PhET's
Basics does NOT have, and the section for its own view.  Generating it this way rather
than copying keeps the shared half from drifting; every substitution below is asserted to
match exactly once."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'ph-scale', 'ui_drive_ph-scale.js')
src = io.open(SRC, encoding='utf-8').read()

i = src.index('/* ---- the particles ---- */')
j = src.index('/* ---- the two analysis views ---- */')
head, tail = src[:i], src[j:]


# about 70 % of what each tab emits at 1400 x 820 on its first draw; measured with
# UI_DIAG (python3 jsrun.py ui_drive_ph-scale-basics.js osa diag)
FLOORS_B = [590, 78, 60, 780]


def sub(s, old, new, n=1):
    assert s.count(old) == n, 'pattern %r occurs %d times, wanted %d' % (old[:60], s.count(old), n)
    return s.replace(old, new)


head = sub(head, 'UI drive test for ph-scale.html',
           'UI drive test for ph-scale-basics.html')
head = sub(head,
           ' * DOM-stub pattern (lineage: projects/simulations/build_buoy/ui_drive_bu.js via\n'
           ' * build/greenhouse-effect/ui_drive_greenhouse-effect.js, which carries the',
           ' * GENERATED from build/ph-scale/ui_drive_ph-scale.js by make_ui.py, so the half\n'
           ' * the two sims share cannot drift.  DOM-stub pattern (lineage:\n'
           ' * projects/simulations/build_buoy/ui_drive_bu.js via\n'
           ' * build/greenhouse-effect/ui_drive_greenhouse-effect.js, which carries the')
head = sub(head,
           "uok(NODESU.panel.children.length===9,'the control panel has its nine groups ('+NODESU.panel.children.length+')');",
           "uok(NODESU.panel.children.length===6,'the control panel has its six groups ('+NODESU.panel.children.length+')');")
head = sub(head,
           "uok((NODESU.panel.textContent||'').indexOf('ph-scale_en.html 1.7.6')>=0,",
           "uok((NODESU.panel.textContent||'').indexOf('ph-scale-basics_en.html 1.7.5')>=0,")
head = sub(head,
           "const FLOORSU=(typeof UI_FLOORS!=='undefined')?UI_FLOORS:[590,870,32,320,60,780];",
           "const FLOORSU=(typeof UI_FLOORS!=='undefined')?UI_FLOORS:"+repr(FLOORS_B)+";")
# the eqbar of this build's first view is the same law, but the beaker readout is not
head = sub(head,
           "uok(RO().length>400,'the readout rendered ('+RO().length+' chars)');",
           "uok(RO().length>300,'the readout rendered ('+RO().length+' chars)');\n"
           "uok(RO().indexOf('mol/L')<0&&RO().indexOf('molecules')<0,\n"
           "    'and carries no concentration, as PhET\\u2019s Basics does not');")
# the chip row the law test switches to: this build has no particles view to return to
head = sub(head, "  chipU('exact (Kw)',2).fire('click');\n  chipU('orange juice',12).fire('click');",
           "  chipU('exact (Kw)',2).fire('click');\n  chipU('orange juice',12).fire('click');")

tail = sub(tail, "tab(4);\n{ RECU=makeRecU(); tab(4);", "tab(2);\n{ RECU=makeRecU(); tab(2);")
tail = sub(tail, "tab(5);\n{ RECU=makeRecU(); tab(5);", "tab(3);\n{ RECU=makeRecU(); tab(3);")
tail = sub(tail,
           "{ keyU('1'); uok(ST.view==='beaker','1 is the beaker');\n"
           "  keyU('4'); uok(ST.view==='my','4 is my solution');\n"
           "  keyU('6'); uok(ST.view==='scale','6 is the scale');\n"
           "  keyU('9'); uok(ST.view==='scale','9 is not a view');\n"
           "  keyU('2'); uok(ST.view==='particles','2 is the particles'); }",
           "{ keyU('1'); uok(ST.view==='beaker','1 is the beaker');\n"
           "  keyU('3'); uok(ST.view==='dilution','3 is dilution');\n"
           "  keyU('4'); uok(ST.view==='scale','4 is the scale');\n"
           "  keyU('9'); uok(ST.view==='scale','9 is not a view');\n"
           "  keyU('2'); uok(ST.view==='liquids','2 is the liquids'); }")
tail = sub(tail, "  uok(inputs.length>=11,'the panel has its sliders and checkboxes ('+inputs.length+')');",
           "  uok(inputs.length===6,'the panel has its two sliders and four checkboxes ('+inputs.length+')');")
tail = sub(tail,
           "{ const g=NODESU.panel.children;\n"
           "  tab(0); uok(g[0].hidden===false&&g[1].hidden===false&&g[3].hidden===true,\n"
           "    'the beaker shows the liquid and the beaker groups, not my solution');\n"
           "  tab(3); uok(g[1].hidden===true&&g[3].hidden===false,'my solution shows its own and hides the beaker');\n"
           "  tab(2); uok(g[4].hidden===false,'the graph shows the graph group');\n"
           "  tab(4); uok(g[0].hidden===false&&g[1].hidden===true&&g[2].hidden===false,\n"
           "    'dilution keeps the liquid and the law, and drops the beaker');\n"
           "  tab(5); uok(g[5].hidden===true,'the scale drops the particle boxes');\n"
           "  tab(0); }",
           "{ const g=NODESU.panel.children;\n"
           "  tab(0); uok(g[0].hidden===false&&g[1].hidden===false&&g[2].hidden===false,\n"
           "    'the beaker shows the liquid, the beaker and the law');\n"
           "  tab(1); uok(g[1].hidden===true&&g[2].hidden===false,\n"
           "    'the liquids table keeps the law and drops the beaker');\n"
           "  tab(2); uok(g[0].hidden===false&&g[1].hidden===true,'so does dilution');\n"
           "  tab(3); uok(g[1].hidden===true&&g[2].hidden===true,\n"
           "    'and the scale drops both');\n"
           "  tab(0); }")
tail = sub(tail, "  chipU('PhET’s rule',2).fire('click');\n"
                 "  ST.ph=2; ST.vMy=1.1; ST.units='moles'; ST.scaleKind='linear'; ST.linExp=-3;\n"
                 "  ST.ratio=true; ST.counts=true;\n",
           "  chipU('PhET’s rule',2).fire('click');\n")
tail = sub(tail, "  uok(ST.solute==='vomit'&&ST.law==='phet'&&ST.pourSolute&&ST.ratio,'the state is disturbed');",
           "  uok(ST.solute==='vomit'&&ST.law==='phet'&&ST.pourSolute,'the state is disturbed');")
tail = sub(tail, "  uok(findLabelledU('the dot ratio, in the beaker').checked===false,'the checkboxes follow');",
           "  uok(findLabelledU('the dropper pours (0.05 L/s)').checked===false,'the checkboxes follow');")

OWN = r'''
/* ---- this build's own view: the twelve liquids as a table ---- */
tab(1); quiet();
{ RECU=makeRecU(); tab(1);
  const tx=textsU(RECU);
  for(const s of SOLUTES) uok(tx.indexOf(s.name)>=0,'the table lists '+s.name);
  uok(tx.indexOf('4.58')>=0,'and prints orange juice’s diluted pH');
  uok(tx.indexOf('7.37–7.43')>=0,'and blood’s sourced range');
  uok(tx.filter(t=>t==='not sourced').length===8,
      'and says "not sourced" for exactly the eight that are not ('
      +tx.filter(t=>t==='not sourced').length+')');
  uok(tx.some(t=>t.indexOf('diluted 12x')>=0),'the diluted column is headed');
  assertCleanU(RECU,'the liquids table');
  /* the liquid chip highlights the row, so a different chip is a different picture.
     Compared on the GEOMETRY, not on sigU: length-plus-count is the same for two
     different rows of the same table, and the assertion passed on a view that had not
     changed at all. */
  const before=geomU(RECU);
  chipU('drain cleaner',12).fire('click');
  RECU=makeRecU(); tab(1);
  uok(geomU(RECU)!==before,'picking another liquid redraws the table');
  uok((NODESU.eqbar.innerHTML||'').indexOf('factor of ten')>=0,
      'and the equation bar carries this view’s own line');
  chipU('orange juice',12).fire('click'); }

'''

out = head + OWN + tail
io.open(os.path.join(HERE, 'ui_drive_ph-scale-basics.js'), 'w', encoding='utf-8').write(out)
print('ui_drive_ph-scale-basics.js: %d lines (%d shared with ph-scale)'
      % (len(out.splitlines()), len(head.splitlines()) + len(tail.splitlines())))
