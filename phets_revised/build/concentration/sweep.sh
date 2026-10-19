#!/bin/zsh
# Sweep a COPY of the html inside this build's own _out/, never the landed file: mutate.py
# writes its scratch _mutant.js next to the html it tests, so an in-place sweep would share
# one docs/phets_revised/_mutant.js with every other agent running at the same time and
# corrupt both kill counts.
#   zsh sweep.sh <stem> [p|u]        (p = physics only, u = the UI mutants only)
B=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build
T=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/projects/simulations/tools
STEM=${1:-beers-law-lab}
ONLY=$2
UI=$B/$STEM/ui_drive_$STEM.js
mkdir -p $B/$STEM/_out/sweep
cp $B/../$STEM.html $B/$STEM/_out/sweep/$STEM.html
cd $B/$STEM/_out/sweep
python3 $T/mutate.py $STEM.html $B/$STEM/mutants.json $UI $ONLY
