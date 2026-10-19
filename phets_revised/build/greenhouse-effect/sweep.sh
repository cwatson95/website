#!/bin/zsh
# Mutation sweep, run against a COPY of the html inside this build's own _out/: mutate.py
# writes its scratch _mutant.js next to the html it tests, so an in-place sweep on
# docs/phets_revised/greenhouse-effect.html would share one _mutant.js with every other
# agent's sweep and corrupt both kill counts (BRIEF.md).
B=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build/greenhouse-effect
TOOLS=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/projects/simulations/tools
cp $B/../../greenhouse-effect.html $B/_out/sweep_greenhouse-effect.html
python3 $TOOLS/mutate.py $B/_out/sweep_greenhouse-effect.html $B/mutants.json \
        $B/ui_drive_greenhouse-effect.js | tee $B/mutation_log.txt
