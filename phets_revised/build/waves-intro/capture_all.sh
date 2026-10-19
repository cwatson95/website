#!/bin/zsh
# Capture the display list at three stage sizes, audit and rasterise each (one osascript at a time).
# Usage: zsh capture_all.sh [sizes...]        (paths are absolute)
B=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build/waves-intro
TOOLS=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/projects/simulations/tools
# NOT SIZES=(${@:-a b c}): with no arguments zsh puts the whole default in ONE word, and the
# script then makes a single directory called "c1400x820 1100x700 560" and audits one size while
# looking like it audited three.  Set the default as its own array.
if (( $# )); then
  SIZES=("$@")
else
  SIZES=(1400x820 1100x700 560x380)
fi
for sz in $SIZES; do
  w=${sz%x*}; h=${sz#*x}
  d=$B/_out/c$w
  mkdir -p $d
  rm -f $d/display.json $d/view_*.png(N)
  { echo "var CAP_W=$w, CAP_H=$h;"; cat $B/_out/run.js $TOOLS/recorder.js $B/capture_tail_waves-intro.js; } > $d/cap_run.js
  (cd $d && osascript -l JavaScript cap_run.js > cap.log 2>&1)
  echo "== $sz: $(tail -1 $d/cap.log)"
  python3 $TOOLS/audit.py $d/display.json > $d/audit.log 2>&1
  grep -v "^OK" $d/audit.log
  python3 $TOOLS/raster.py $d/display.json $d > $d/raster.log 2>&1
  tail -1 $d/raster.log
done
