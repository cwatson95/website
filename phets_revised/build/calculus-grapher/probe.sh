#!/bin/sh
# scratch: run _out/probe.js against the sim WITHOUT running selfTest first
set -e
D=/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/build/calculus-grapher
python3 "$D/assemble.py" > /dev/null
python3 - "$D" <<'PY'
import io, os, sys
d = sys.argv[1]
s = io.open(os.path.join(d, '_out', 'run.js'), encoding='utf-8').read()
i = s.index("/* ============================== entry ============================= */")
s = s[:i]
io.open(os.path.join(d, '_out', 'noentry.js'), 'w', encoding='utf-8').write(s)
PY
cat "$D/_out/jsc_head.js" "$D/_out/noentry.js" "$D/_out/probe.js" > "$D/_out/probe_run.js"
/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc "$D/_out/probe_run.js"
