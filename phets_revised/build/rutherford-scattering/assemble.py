#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/rutherford-scattering.html
and extract _out/run.js (the <script> body) for the headless runs."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.normpath(os.path.join(HERE, "..", "..", "rutherford-scattering.html"))
PARTS = ["p1_head.html", "p1_utils.js", "p2_physics.js", "p2_elements.js", "p3_state.js",
         "p4_helpers.js", "p4_views.js", "p5_views.js", "p6_boot.js", "p7_refs.js",
         "p7_test.js"]
TAIL = """
/* ============================== entry ============================= */
if(typeof document === 'undefined'){
  selfTest();
} else {
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
}
</script>
</body>
</html>
"""


def main():
    body = ""
    for p in PARTS:
        path = os.path.join(HERE, p)
        if not os.path.isfile(path):
            print("missing", p, file=sys.stderr)
            return 1
        body += io.open(path, encoding="utf-8").read()
    body += TAIL
    io.open(OUT_HTML, "w", encoding="utf-8").write(body)
    js = body.split("<script>", 1)[1].rsplit("</script>", 1)[0]
    outdir = os.path.join(HERE, "_out")
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    io.open(os.path.join(outdir, "run.js"), "w", encoding="utf-8").write(js)
    print("%s  %d lines, %.1f KB" % (OUT_HTML, len(body.splitlines()),
                                     len(body.encode("utf-8")) / 1024))
    # a copy inside _out/ is what the mutation sweep is run against: mutate.py
    # writes its scratch _mutant.js next to the html it tests, and parallel
    # agents sweeping docs/phets_revised/ in place would share one scratch file
    # and corrupt each other's kill counts (BRIEF.md).
    io.open(os.path.join(outdir, "sweep_copy.html"), "w", encoding="utf-8").write(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
