#!/bin/zsh
# Assemble, then run the UI drive under osascript (after the selfTest, which run.js runs first).
# Usage: zsh run_ui.sh [diag]
B=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build/wave-interference
python3 $B/assemble.py
{ if [[ "$1" == "diag" ]]; then echo "var UI_DIAG=1;"; fi; cat $B/_out/run.js $B/ui_drive_wave-interference.js; } > $B/_out/ui_run.js
cd $B/_out && osascript -l JavaScript ui_run.js > ui.log 2>&1
echo "exit $?"
grep -c 'UI FAIL' ui.log
grep 'UI FAIL\|TABOPS\|^UI:\|passed' ui.log | cut -c1-240
