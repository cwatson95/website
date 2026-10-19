#!/bin/zsh
# Capture the display list at three stage sizes, audit and rasterise each (one osascript at
# a time).  Usage: zsh capture_all.sh [build-dir-name] [sizes...]   (paths are absolute)
ROOT=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build
TOOLS=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/projects/simulations/tools
STEM=${1:-beers-law-lab}
shift 2>/dev/null
B=$ROOT/$STEM
TAIL=$ROOT/beers-law-lab/capture_tail_beers-law-lab.js
if (( $# )); then SIZES=($@); else SIZES=(1400x820 1100x700 560x380); fi
# (zsh expands ${@:-a b c} as ONE word when $@ is empty, which makes a directory called
#  'c1400x820 1100x700 560' and an audit of a file that is not there)
for sz in $SIZES; do
  w=${sz%x*}; h=${sz#*x}
  d=$B/_out/c$w
  mkdir -p $d
  rm -f $d/display.json $d/view_*.png(N)
  { echo "var CAP_W=$w, CAP_H=$h;"; cat $B/_out/run.js $TOOLS/recorder.js $TAIL; } > $d/cap_run.js
  (cd $d && osascript -l JavaScript cap_run.js > cap.log 2>&1)
  echo "== $STEM $sz: $(tail -1 $d/cap.log)"
  python3 $TOOLS/audit.py $d/display.json > $d/audit.log 2>&1
  grep -v "^OK" $d/audit.log
  python3 $TOOLS/raster.py $d/display.json $d > $d/raster.log 2>&1
  tail -1 $d/raster.log
done
