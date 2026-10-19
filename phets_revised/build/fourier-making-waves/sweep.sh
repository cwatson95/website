#!/bin/sh
# Mutation sweep on a COPY inside _out/sweep: mutate.py writes its scratch
# _mutant.js next to the html it tests, so an in-place sweep would share one
# docs/phets_revised/_mutant.js with every other agent working in parallel and
# corrupt their kill counts (BRIEF, step 4).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
TOOLS="$HERE/../../../../projects/simulations/tools"
mkdir -p "$HERE/_out/sweep"
cp "$HERE/../../fourier-making-waves.html" "$HERE/_out/sweep/fourier-making-waves.html"
python3 "$TOOLS/mutate.py" \
  "$HERE/_out/sweep/fourier-making-waves.html" \
  "$HERE/mutants.json" \
  "$HERE/ui_drive_fourier-making-waves.js" \
  > "$HERE/_out/sweep/mutation_log.txt" 2>&1
echo "sweep finished"
tail -20 "$HERE/_out/sweep/mutation_log.txt"
