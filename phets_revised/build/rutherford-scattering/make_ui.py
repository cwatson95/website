#!/usr/bin/env python3
"""Build ui_drive_rutherford-scattering.js: the DOM-stub harness head is taken
VERBATIM from the landed models-of-the-hydrogen-atom build (it carries this
collection's fixes -- innerHTML as a setter that strips tags into textContent,
the recorder kept across frames, the real frame pump), and this file appends
the checks that are specific to this sim."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "models-of-the-hydrogen-atom",
                   "ui_drive_models-of-the-hydrogen-atom.js")
s = io.open(SRC, encoding="utf-8").read()
i = s.index("/* ============ UI drive")
k = s.index("/* ---- boot ---- */")
head = s[i:k]
for want in ["uMakeRec", "uEl", "globalThis.document", "upump", "uFrameGeom", "uSig", "uGeom"]:
    assert want in head, want
body = io.open(os.path.join(HERE, "_ui_body.js"), encoding="utf-8").read()
out = os.path.join(HERE, "ui_drive_rutherford-scattering.js")
io.open(out, "w", encoding="utf-8").write(head + body)
print("%d head + %d body = %d lines"
      % (len(head.splitlines()), len(body.splitlines()),
         len((head + body).splitlines())))
