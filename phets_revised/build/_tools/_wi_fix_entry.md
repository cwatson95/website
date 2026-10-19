## 2026-09-21 — wave-interference: captions clear the HTML hint (re-landed)
### Fixed
- Its captions were fitted to the full canvas height, so the bottom-left caption
  line shared pixels with the HTML hint (`#hint{bottom:11px}`) — the trap the
  `wave-on-a-string` build found and `waves-intro` confirmed against this file.
  Neither the capture nor the audit can see it, because the hint is HTML, not
  canvas. The four call sites now fit to `H − HINT_H` (18 px) and the layout
  sweep asserts the bottom-left corner is clear, exactly as the sibling builds
  do. The assertion was run against the unfixed file first and failed all 148
  configuration × size cases; after the fix the lowest canvas text clears by
  4 px at every size.
- Two narrow-stage consequences of the reservation, fixed rather than left to
  collide (11 collisions at 560×380 on the first rebuild): below 300 px of tank
  the far field's cut plot is dropped with a note and its two squares take the
  height, and the tank's "needs a taller window" notes take short forms.
### Verified
- Rebuilt file 209.2 KB: selfTest 1453/0 (was 1305; the 148 new checks are the
  corner assertion), UI drive 257/0, mutation sweep 81/81 in one pass on a copy
  `cmp`-equal to the shipped file, audit 0 problems at 1400×820, 1100×700 and
  560×380, affected PNGs looked at again at all three sizes.
- The five part files `build/waves-intro/assemble.py` pins are byte-identical
  (SHA-256 re-checked), so `waves-intro` is unaffected: re-verified 968/0, 164/0.
