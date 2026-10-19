#!/usr/bin/env python3
"""Pull makeShot() — the transform-aware recording context the inline layout
sweep draws into — verbatim out of the landed rutherford-scattering build.
It is shared, audited code (it tracks rotate(), which axes() needs, and it
measures text the way tools/audit.py does); retyping it is how a fix gets
lost."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "rutherford-scattering", "p7_test.js"))

s = io.open(SRC, encoding="utf-8").read()
i = s.index("function makeShot(")
j = s.index("\n}\n", s.index("return ctx;", i)) + 3
body = s[i:j]
assert "rotate(" in body and "fillText" in body and "measureText" in body
head = ("/* makeShot(): the transform-aware recording context, extracted verbatim from\n"
        "   build/rutherford-scattering/p7_test.js by extract_shot.py.  It tracks\n"
        "   rotate() (axes() draws its y title in a rotated frame, and treating those\n"
        "   coordinates as canvas coordinates makes correct code fail) and measures\n"
        "   text the way tools/audit.py does. */\n")
io.open(os.path.join(HERE, "p7_shot.js"), "w", encoding="utf-8").write(head + body)
print("p7_shot.js  %d lines" % len((head + body).splitlines()))
