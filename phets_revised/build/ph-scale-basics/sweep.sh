#!/bin/zsh
# Mutation sweep, run against a COPY of the html inside this build's own _out/: mutate.py
# writes its scratch _mutant.js next to the html it tests, so an in-place sweep on
# docs/phets_revised/ph-scale-basics.html would share one _mutant.js with every other
# agent's sweep and corrupt both kill counts (BRIEF.md).
B=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build/ph-scale-basics
TOOLS=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/projects/simulations/tools
cp $B/../../ph-scale-basics.html $B/_out/sweep_ph-scale-basics.html
python3 $TOOLS/mutate.py $B/_out/sweep_ph-scale-basics.html $B/mutants.json \
        $B/ui_drive_ph-scale-basics.js | tee $B/mutation_log.txt
