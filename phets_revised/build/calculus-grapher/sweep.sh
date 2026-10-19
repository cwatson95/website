#!/bin/sh
# Mutation sweep on a PRIVATE COPY of the html inside _out/: mutate.py writes
# its scratch _mutant.js next to the file it tests, so sweeping
# docs/phets_revised/calculus-grapher.html in place would share one scratch
# file with every other agent's sweep (BRIEF).
set -e
D=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build/calculus-grapher
T=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/projects/simulations/tools
cp "$D/../../calculus-grapher.html" "$D/_out/cg_copy.html"
exec python3 "$T/mutate.py" "$D/_out/cg_copy.html" "$D/mutants.json" \
     "$D/ui_drive_calculus-grapher.js"
