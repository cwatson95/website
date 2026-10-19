#!/usr/bin/env python3
"""Bring projectile-data-lab's changelog entry up to the shipped file's numbers.

Its entry was written before the agent's last fix round: it claims selfTest 457,
UI 180 and 87 caught of 89, while the shipped file measures 479 / 182 and the
definitive sweep (build/_tools/resweep.py, this orchestrator) read 95 caught of
97 with the same two survivors, both labelled equivalent in mutants.json.
"""
import io

P = ("/Users/cooper/coding/Agent/.claude/worktrees/phets-revised/docs/phets_revised/"
     "build/projectile-data-lab/changelog_entry.md")
SUBS = [("`selfTest` 457 assertions green", "`selfTest` 479 assertions green"),
        ("180 green (drag the interval", "182 green (drag the interval"),
        ("mutation sweep 87 caught of 89 with the", "mutation sweep 95 caught of 97 with the"),
        ("- Mutation sweep findings (87 caught of 89):", "- Mutation sweep findings (95 caught of 97):")]

s = io.open(P, encoding="utf-8").read()
for old, new in SUBS:
    assert s.count(old) == 1, (old, s.count(old))
    s = s.replace(old, new, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched", P)
