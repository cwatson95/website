#!/usr/bin/env python3
"""Independent check of one remake, run FROM A GIVEN CHECKOUT.

    python3 verify_one.py <root> <stem> [<stem> ...]

<root> is a checkout root (the worktree or the main checkout); the sim is
<root>/docs/phets_revised/<stem>.html and its UI drive
<root>/docs/phets_revised/build/<stem>/ui_drive_<stem>.js.

Checks: selfTest() green under osascript; the UI drive green; the PhET credit
line; all six site-nav links absolute and no relative ../website/ or
../modules/ href left; nothing fetched from the network. Exit 0 only if all
pass for every stem.
"""
import io
import os
import re
import subprocess
import sys
import tempfile
import time

NAV = ["https://cooper-watson.net/index.html", "https://cooper-watson.net/about.html",
       "https://cooper-watson.net/teaching.html",
       "https://cooper-watson.net/modules/teaching_modules.html",
       "https://cooper-watson.net/simulations.html", "https://cooper-watson.net/research.html"]
NETWORK = re.compile(r"""(<script[^>]+src\s*=\s*["']?https?:|<link[^>]+href\s*=\s*["']?https?:[^>]*stylesheet|"""
                     r"""<link[^>]+stylesheet[^>]*href\s*=\s*["']?https?:|@import\s+url\(\s*["']?https?:|"""
                     r"""\bfetch\s*\(|XMLHttpRequest|<img[^>]+src\s*=\s*["']?https?:|new\s+WebSocket)""", re.I)


def run_js(body, tail="", timeout=1800):
    fd, tmp = tempfile.mkstemp(suffix=".js")
    os.close(fd)
    with io.open(tmp, "w", encoding="utf-8") as f:
        f.write(body + "\n" + tail)
    t0 = time.time()
    try:
        r = subprocess.run(["osascript", "-l", "JavaScript", tmp], capture_output=True,
                           text=True, timeout=timeout)
    finally:
        os.remove(tmp)
    return r, time.time() - t0


def counts(lines, ui):
    pat = re.compile(r"(\d+)\s+passed,\s+(\d+)\s+failed")
    for line in reversed(lines):
        if ("UI" in line) != ui:
            continue
        m = pat.search(line)
        if m:
            return int(m.group(1)), int(m.group(2)), line.strip()
    return None, None, "?"


def find_ui(bdir, stem):
    """ui_drive_<stem>.js, else the build dir's single ui_drive*.js (some builds
    abbreviate the stem, e.g. ui_drive_gfl.js)."""
    exact = os.path.join(bdir, "ui_drive_%s.js" % stem)
    if os.path.isfile(exact):
        return exact
    cands = sorted(f for f in os.listdir(bdir) if f.startswith("ui_drive") and f.endswith(".js")) \
        if os.path.isdir(bdir) else []
    return os.path.join(bdir, cands[0]) if len(cands) == 1 else exact


def check(root, stem):
    html = os.path.join(root, "docs", "phets_revised", stem + ".html")
    ui = find_ui(os.path.join(root, "docs", "phets_revised", "build", stem), stem)
    probs = []
    if not os.path.isfile(html):
        return False, ["missing " + html]
    s = io.open(html, encoding="utf-8").read()
    body = s.split("<script>", 1)[1].rsplit("</script>", 1)[0]
    r, dt = run_js(body)
    p, f, line = counts((r.stdout + r.stderr).splitlines(), ui=False)
    if r.returncode != 0 or not p or f != 0:
        probs.append("selfTest: %s (exit %d)" % (line, r.returncode))
    st = "selfTest %s/%s %.0fs" % (p, f, dt)
    if os.path.isfile(ui):
        r2, dt2 = run_js(body, io.open(ui, encoding="utf-8").read())
        p2, f2, line2 = counts((r2.stdout + r2.stderr).splitlines(), ui=True)
        if r2.returncode != 0 or not p2 or f2 != 0:
            probs.append("UI drive: %s (exit %d)" % (line2, r2.returncode))
        st += ", UI %s/%s %.0fs" % (p2, f2, dt2)
    else:
        probs.append("no UI drive at " + ui)
    if "Remake of PhET Interactive Simulations" not in s or "CC-BY 4.0" not in s:
        probs.append("PhET credit line missing")
    for u in NAV:
        if 'href="%s"' % u not in s:
            probs.append("nav link missing: " + u)
    if 'href="../website/' in s or 'href="../modules/' in s or 'href="../../modules/' in s:
        probs.append("relative site-nav href left")
    m = NETWORK.search(s)
    if m:
        probs.append("network use: " + m.group(0)[:60])
    print("%-40s %7.1f KB  %s  %s" % (stem, len(s.encode()) / 1024, st, "OK" if not probs else "PROBLEMS"))
    for pr in probs:
        print("    - " + pr)
    return not probs, probs


def main():
    root = os.path.abspath(sys.argv[1])
    ok = True
    for stem in sys.argv[2:]:
        good, _ = check(root, stem)
        ok = ok and good
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
