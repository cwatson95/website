#!/usr/bin/env python3
"""Write mutants.json for tools/mutate.py.

This build shares its chemistry, its state and three of its four views with ph-scale, so
its mutant list starts from build/ph-scale/mutants.json — every entry whose pattern occurs
EXACTLY once in this build's own _out/run.js is carried over, and any that does not is
reported rather than silently dropped (a pattern that matches none is a mutant you think
you ran and did not).  Then the mutants for what this build does NOT share: its identity,
its trimmed readout and its own view.

Every mutant is a changed CONSTANT, SIGN, EXPONENT or INDEX.  None of them touches a loop
condition: tools/mutate.py has no per-mutant timeout, so a mutant that fails to terminate
stalls the whole sweep (BRIEF.md)."""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
js = io.open(os.path.join(HERE, '_out', 'run.js'), encoding='utf-8').read()
parent = json.load(io.open(os.path.join(HERE, '..', 'ph-scale', 'mutants.json'),
                           encoding='utf-8'))

M, dropped = [], []
for label, old, new, suite in parent:
    n = js.count(old)
    if n == 1:
        M.append((label, old, new, suite))
    else:
        dropped.append((label, n))

OWN = [
    # ---- this build's identity: PhET's Basics is one screen and prints no concentrations ----
    ("the four tabs", "['dilution','dilution'],['scale','the scale']];",
     "['dilution','dilution']];", 'p'),
    ("the tab order", "const TABS=[['beaker','the beaker'],['liquids','the liquids'],",
     "const TABS=[['liquids','the liquids'],['beaker','the beaker'],", 'p'),
    ("PhET's Basics prints no concentrations", "const SHOW_CONC=false;",
     "const SHOW_CONC=true;", 'p'),
    ("the version it was built against", "const SIM_VER='1.7.5';", "const SIM_VER='1.7.6';", 'p'),
    # ---- the liquids table ----
    ("the table's dilution is 0.1 L into 1.2 L",
     "const ex=mixExact(r.s.pH,0.1,PHET.WATER_PH,1.1), ph=mixPhet(r.s.pH,0.1,1.1);",
     "const ex=mixExact(r.s.pH,0.2,PHET.WATER_PH,1.0), ph=mixPhet(r.s.pH,0.1,1.1);", 'p'),
    ("the table's two columns are the two different laws",
     "const ex=mixExact(r.s.pH,0.1,PHET.WATER_PH,1.1), ph=mixPhet(r.s.pH,0.1,1.1);",
     "const ex=mixExact(r.s.pH,0.1,PHET.WATER_PH,1.1), ph=mixExact(r.s.pH,0.1,PHET.WATER_PH,1.1);",
     'p'),
    ("a liquid with no range says so rather than printing one",
     "      : 'not sourced';", "      : fmt(r.s.pH,2);", 'p'),
    ("the table is sorted by pH",
     "  const rows=L.rows.slice().sort((a,b)=>a.s.pH-b.s.pH);",
     "  const rows=L.rows.slice().sort((a,b)=>b.s.pH-a.s.pH);", 'p'),
    ("the measured range is printed low-to-high",
     "         :fmt(r.s.range[0],2)+'–'+fmt(r.s.range[1],2))",
     "         :fmt(r.s.range[1],2)+'–'+fmt(r.s.range[0],2))", 'p'),
    # ---- the UI: the selected row, and this build's own equation bar ----
    ("the selected row is banded", "    if(on){\n      rc.fillStyle='rgba(184,236,76,.10)';",
     "    if(false){\n      rc.fillStyle='rgba(184,236,76,.10)';", 'u'),
    ("this build's own equation-bar line",
     "function eqbarFor(M){ return M.view==='liquids'?EQ_LIQUIDS:eqbarHTML(M); }",
     "function eqbarFor(M){ return eqbarHTML(M); }", 'u'),
]
for label, old, new, suite in OWN:
    n = js.count(old)
    assert n == 1, 'own pattern %r occurs %d times, wanted 1' % (label, n)
    M.append((label, old, new, suite))

io.open(os.path.join(HERE, 'mutants.json'), 'w', encoding='utf-8').write(
    json.dumps([list(m) for m in M], indent=0))
print('mutants.json: %d mutants (%d physics, %d ui) — %d carried from ph-scale, %d own'
      % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u'),
         len(M) - len(OWN), len(OWN)))
if dropped:
    print('%d of ph-scale\'s %d did not apply to this build:' % (len(dropped), len(parent)))
    for label, n in dropped:
        print('   %-52s (%d matches)' % (label, n))
