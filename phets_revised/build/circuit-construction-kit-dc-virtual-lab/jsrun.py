#!/usr/bin/env python3
"""Development runner: concatenate part files (paths relative to this build
dir) into _out/<out>.js and run it under jsc (fast; console.log shimmed to
print) or osascript (the house's final judge).

    python3 jsrun.py jsc  quick  p1_utils.js p2_presets.js ... _dev/tail.js
    python3 jsrun.py osa  quick  ...
    python3 jsrun.py jsc  sim    (the assembled sim's script, see assemble.py) [tail.js]

Prints the combined stdout/stderr and the exit code.
"""
import io
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc'


def main():
    eng, name, files = sys.argv[1], sys.argv[2], sys.argv[3:]
    parts = []
    if files and files[0] == 'SIM':
        s = io.open(os.path.join(HERE, '_out', 'run.js'), encoding='utf-8').read()
        parts.append(s)
        files = files[1:]
    for f in files:
        parts.append(io.open(os.path.join(HERE, f), encoding='utf-8').read())
    body = '\n'.join(parts)
    out = os.path.join(HERE, '_out', name + '.js')
    if eng == 'jsc':
        body = 'var console={log:print};\n' + body
    io.open(out, 'w', encoding='utf-8').write(body)
    t0 = time.time()
    cmd = [JSC, out] if eng == 'jsc' else ['osascript', '-l', 'JavaScript', out]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3000)
    sys.stdout.write(r.stdout)
    sys.stdout.write(r.stderr)
    print('[exit %d, %.1f s]' % (r.returncode, time.time() - t0))
    sys.exit(r.returncode)


if __name__ == '__main__':
    main()
