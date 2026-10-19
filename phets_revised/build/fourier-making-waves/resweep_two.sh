#!/bin/sh
# Re-run ONLY the two mutants that survived the full sweep, after the two
# assertions that were missing were added.  Own scratch directory, as always.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
TOOLS="$HERE/../../../../projects/simulations/tools"
mkdir -p "$HERE/_out/sweep2"
cp "$HERE/../../fourier-making-waves.html" "$HERE/_out/sweep2/fourier-making-waves.html"
python3 - "$HERE" <<'PY'
import io, json, os, sys
here = sys.argv[1]
M = json.load(io.open(os.path.join(here, 'mutants.json'), encoding='utf-8'))
want = ["PhET's step button: 0.05 ms -> 0.1 ms", "the tab class never changes"]
sub = [m for m in M if m[0] in want]
assert len(sub) == len(want), sub
io.open(os.path.join(here, '_out', 'sweep2', 'mutants_two.json'), 'w', encoding='utf-8').write(
    json.dumps(sub, indent=1) + '\n')
print('re-sweeping %d mutants' % len(sub))
PY
python3 "$TOOLS/mutate.py" \
  "$HERE/_out/sweep2/fourier-making-waves.html" \
  "$HERE/_out/sweep2/mutants_two.json" \
  "$HERE/ui_drive_fourier-making-waves.js" \
  > "$HERE/_out/sweep2/mutation_log.txt" 2>&1
tail -10 "$HERE/_out/sweep2/mutation_log.txt"
