# build/concentration/

PhET ships **Concentration** as the Concentration screen of **Beer's Law Lab** on its own,
so this sim is that one engine trimmed to that one screen. This directory holds only the
two files that are its own:

| file | what it is |
|---|---|
| `p1_head.html` | its `<title>`, header comment, `<h1>` and tagline (written by `../beers-law-lab/make_head.py basics`) |
| `p2b_id.js` | its identity and its four tabs, and the `SHOW_BEERS = false` that switches the cuvette, the spectrum and the law views off |

Everything else is read from `../beers-law-lab/` **by path** at assemble time and is never
written to here: `p2_data.js` (PhET's values), `p2_chem.js` (the chemistry), `p3_state.js`,
`p4_views.js` (the beaker), `p5_views.js` (the ledger and the colour view),
`p5c_solutes.js` (this sim's extra view, which `beers-law-lab` does not build),
`p6_boot.js`, `p7_refs.js` and `p7_test.js` (the same suite, `SHOW_BEERS`-guarded). The
Python twin, the reference values and the display-list capture tail live there too:

    ../beers-law-lab/derive.py                      the twin; writes refvals.txt
    ../beers-law-lab/refvals.txt                    every asserted reference value
    ../beers-law-lab/capture_tail_beers-law-lab.js  the capture tail for BOTH sims

`ui_drive_concentration.js` is the same harness as `ui_drive_beers-law-lab.js`, copied
rather than shared by path only because `_tools/verify_one.py` runs it by the name
`ui_drive_<stem>.js`; `assemble.py` rewrites the copy every time, so the two cannot drift
apart unnoticed.

    python3 assemble.py                       -> docs/phets_revised/concentration.html
    python3 jsrun.py "" jsc                   the physics suite (fast)
    python3 jsrun.py ui_drive_concentration.js osa
    zsh ../beers-law-lab/capture_all.sh concentration
    zsh sweep.sh concentration [p|u]          the mutation sweep, on a copy in _out/
