#!/bin/zsh
# Capture the display list at three stage sizes, audit and rasterise each (one osascript at a time).
# Usage: zsh capture_all.sh        (from anywhere; paths are absolute)
B=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build/blackbody-spectrum
TOOLS=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/projects/simulations/tools
for sz in 1400x820 1100x700 560x380; do
  w=${sz%x*}; h=${sz#*x}
  d=$B/_out/c$w
  mkdir -p $d
  rm -f $d/display.json $d/view_*.png
  { echo "var CAP_W=$w, CAP_H=$h;"; cat $B/_out/run.js $TOOLS/recorder.js $B/capture_tail_blackbody-spectrum.js; } > $d/cap_run.js
  (cd $d && osascript -l JavaScript cap_run.js > cap.log 2>&1)
  echo "== $sz: $(tail -1 $d/cap.log)"
  python3 $TOOLS/audit.py $d/display.json > $d/audit.log 2>&1
  grep -v "^OK" $d/audit.log
  python3 $TOOLS/raster.py $d/display.json $d > $d/raster.log 2>&1
done
