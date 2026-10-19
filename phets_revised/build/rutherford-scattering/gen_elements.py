#!/usr/bin/env python3
"""Emit p2_elements.js from build/_survey/inventory.json -- PhET's own SHRED
element names for Z = 20..100, the range of its proton slider.  Generated, so
that no element name in the sim was typed by hand."""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
inv = json.load(io.open(os.path.join(HERE, "..", "_survey", "inventory.json"), encoding="utf-8"))
names = list(inv["rutherford-scattering"]["ui_by_repo"]["SHRED"].values())
assert names[0] == "Hydrogen" and names[78] == "Gold", (names[0], names[78])
out = ["/* p2_elements.js -- the element names PhET ships (its SHRED strings, read",
       "   out of the minified build) for Z = 20..100, the range of its proton",
       "   slider.  Emitted by gen_elements.py from build/_survey/inventory.json:",
       "   not one of them was typed by hand. */",
       "const ELEMENTS = {"]
for z in range(20, 101):
    out.append("  %d: %s," % (z, json.dumps(names[z - 1])))
out.append("};")
out.append("function elementName(z){ return ELEMENTS[z] || null; }")
out.append("")
io.open(os.path.join(HERE, "p2_elements.js"), "w", encoding="utf-8").write("\n".join(out))
print("%d element names, Z=20 %s, Z=79 %s, Z=100 %s"
      % (101 - 20, names[19], names[78], names[99]))
