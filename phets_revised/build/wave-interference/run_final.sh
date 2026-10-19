#!/bin/zsh
# The final verification of the finished file, one osascript job at a time:
# assemble -> selfTest (osascript) -> UI drive -> display-list capture, audit and raster at three sizes.
B=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build/wave-interference
python3 $B/assemble.py
cd $B/_out
osascript -l JavaScript run.js > osa_final.log 2>&1
echo "selfTest exit $?: $(grep 'passed' osa_final.log)"
grep -c 'FAIL' osa_final.log
zsh $B/run_ui.sh > ui_final.log 2>&1
echo "UI: $(grep '^UI:' ui.log)"
zsh $B/capture_all.sh 1400x820 1100x700 560x380 > cap_final.log 2>&1
grep '==\|layout problems' cap_final.log
