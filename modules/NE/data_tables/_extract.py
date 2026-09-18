#!/usr/bin/env python3
"""
Extract the appendix data tables (Appendices A, B, C, D) from

  J.K. Shultis & R.E. Faw, *Fundamentals of Nuclear Science and Engineering*,
  3rd ed., CRC Press, 2017
  (books/library/NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf)

and emit, into this directory:

  A1_physical_constants.csv          Table A.1  fundamental constants
  A3_element_properties.csv          Table A.3  atomic weights, densities, MP/BP, abundances
  A4_isotopic_abundances.csv         Table A.4  isotopic abundances + decay data (T_1/2 > 1 h)
  B1_atomic_masses.csv               Table B.1  neutral atomic masses (Audi-Wapstra 1995)
  C1_thermal_neutron_cross_sections.csv  Table C.1  2200 m/s cross sections
  C2_activation_radionuclides.csv    Table C.2  thermal-neutron activation products
  C3_photon_coefficients_<mat>.csv   Table C.3  mass coefficients, 5 materials
  D1_decay_radiation.csv             Appendix D  individual emitted radiations
  D2_decay_group_totals.csv          Appendix D  keV/decay per radiation group
  data_tables.md                     human-readable rendering
  (README.md is hand-written, not generated)

Page geometry.  The PDF's printed page numbers run 23 behind the PDF page
index: **PDF page = printed page + 23** (verified: printed 54 = Ch. 3 opening
= PDF 77; printed 555 = Appendix A = PDF 578).  All page constants below are
PDF pages.

Method.  Text is pulled with poppler's `pdftotext -bbox-layout`, which gives a
bounding box per word.  Words are clustered into visual rows by baseline, and
into columns by x -- the book prints Appendices A.4, B.1, C.2 and D in two or
three side-by-side column groups per page, which a naive line-oriented read
would interleave.  Superscripts (mass numbers, temperature annotations) are
detected by glyph height and re-attached to the token they belong to.

Nothing is written until every table passes its validators: row counts, anchor
values checked against independently-known physical data (12C = 12 u exactly,
235U abundance = 0.7204%, ...), and internal identities (A = N+Z for every
nuclide; mu = mu_c + mu_ph + mu_pp for every photon-coefficient row).

Run:  python3 _extract.py            (from anywhere)
      python3 _extract.py --check    (validate only, write nothing)
"""

import argparse
import csv
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- locating the book
# data_tables/ -> NE/ -> modules/ -> projects/ -> <repo root>
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
BOOK_REL = os.path.join("books", "library", "NE_Nuclear_Engineering",
                        "nuclear_science_shultis_faw.pdf")


def find_pdf():
    """Locate the textbook PDF: $NE_BOOK_PDF, else <repo>/books/..., else the
    main checkout when we are running inside a .claude/worktrees/ copy."""
    env = os.environ.get("NE_BOOK_PDF")
    if env and os.path.exists(env):
        return env
    cand = [os.path.join(REPO, BOOK_REL)]
    # a git worktree lives at <main>/.claude/worktrees/<name>; books/ is untracked
    # and therefore only present in the main checkout
    marker = os.path.join(".claude", "worktrees")
    if marker in REPO:
        main = REPO.split(marker)[0].rstrip(os.sep)
        cand.append(os.path.join(main, BOOK_REL))
    for p in cand:
        if os.path.exists(p):
            return p
    sys.exit("cannot find nuclear_science_shultis_faw.pdf; tried:\n  " +
             "\n  ".join(cand) + "\nSet $NE_BOOK_PDF to override.")


PDF = None  # set in main()

PRINTED_TO_PDF = 23          # PDF page = printed page + 23

# PDF page spans (inclusive)
PAGES = {
    "A":  (578, 592),
    "B":  (593, 610),
    "C":  (611, 618),
    "D":  (619, 647),          # printed 596-624; the Index starts on PDF 648
}


# ---------------------------------------------------------------- pdftotext helpers
def raw_text(first, last, layout=True):
    cmd = ["pdftotext", "-f", str(first), "-l", str(last)]
    if layout:
        cmd.append("-layout")
    cmd += [PDF, "-"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("pdftotext failed: " + out.stderr[:400])
    return out.stdout


class Word:
    __slots__ = ("t", "x0", "x1", "y0", "y1", "page")

    def __init__(self, t, x0, y0, x1, y1, page):
        self.t, self.x0, self.y0, self.x1, self.y1, self.page = t, x0, y0, x1, y1, page

    @property
    def h(self):
        return self.y1 - self.y0

    @property
    def yc(self):
        return (self.y0 + self.y1) / 2.0

    def __repr__(self):
        return "Word(%r,%.0f,%.0f)" % (self.t, self.x0, self.y0)


def words_of(first, last):
    """[[Word,...] per page] via `pdftotext -bbox-layout`."""
    cmd = ["pdftotext", "-f", str(first), "-l", str(last), "-bbox-layout", PDF, "-"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("pdftotext -bbox-layout failed: " + out.stderr[:400])
    xml = out.stdout
    # strip the XHTML doctype/namespace so ElementTree is happy
    xml = re.sub(r"<!DOCTYPE[^>]*>", "", xml, count=1)
    xml = xml.replace(' xmlns="http://www.w3.org/1999/xhtml"', "")
    root = ET.fromstring(xml)
    pages = []
    for pi, page in enumerate(root.iter("page")):
        ws = []
        for w in page.iter("word"):
            t = (w.text or "").strip()
            if not t:
                continue
            ws.append(Word(t, float(w.get("xMin")), float(w.get("yMin")),
                           float(w.get("xMax")), float(w.get("yMax")), first + pi))
        pages.append(ws)
    return pages


def rows_of(words, y_tol=3.0):
    """Cluster words into visual rows by vertical centre; each row sorted by x."""
    ws = sorted(words, key=lambda w: (w.yc, w.x0))
    rows, cur, cy = [], [], None
    for w in ws:
        if cy is None or abs(w.yc - cy) <= y_tol:
            cur.append(w)
            cy = w.yc if cy is None else cy
        else:
            rows.append(sorted(cur, key=lambda z: z.x0))
            cur, cy = [w], w.yc
    if cur:
        rows.append(sorted(cur, key=lambda z: z.x0))
    return rows


def split_columns(row, boundaries):
    """Split one row's words into column groups at the given x boundaries."""
    groups = [[] for _ in range(len(boundaries) + 1)]
    for w in row:
        i = 0
        while i < len(boundaries) and w.x0 >= boundaries[i]:
            i += 1
        groups[i].append(w)
    return groups


def banded_rows(words, big_h=7.0):
    """Row-cluster that is robust to superscripts.

    Body glyphs (height > `big_h`) define the row baselines; small glyphs --
    exponents, footnote markers, degree signs -- are then attached to whichever
    baseline is vertically nearest.  A plain centre-of-mass clustering puts a
    superscript in the row *above* its own as often as not, because a raised
    glyph's centre sits between two baselines.
    """
    big = [w for w in words if w.h > big_h]
    small = [w for w in words if w.h <= big_h]
    bands = rows_of(big, y_tol=3.0)
    if not bands:
        return []
    centres = [sum(w.yc for w in b) / len(b) for b in bands]
    for w in small:
        i = min(range(len(centres)), key=lambda j: abs(centres[j] - w.yc))
        bands[i].append(w)
    return [sorted(b, key=lambda w: w.x0) for b in bands]


def by_columns(band, anchors, big_h=7.0, edge="x1"):
    """Bucket a band's words into named columns by x, splitting body text from
    superscripts.  `anchors` is [(name, x_lo, x_hi), ...].  Returns
    {name: (body_text, [superscript_tokens])}.

    `edge` selects which side of the glyph box decides the column.  Numeric
    tables in this book are *right*-aligned, and the right edge is far more
    stable across pages than the left, so 'x1' is the default."""
    out = {name: ["", []] for name, _, _ in anchors}
    for w in band:
        x = w.x1 if edge == "x1" else w.x0
        for name, lo, hi in anchors:
            if lo <= x < hi:
                if w.h > big_h:
                    out[name][0] += norm(w.t)
                else:
                    out[name][1].append(norm(w.t))
                break
    return {k: (v[0], v[1]) for k, v in out.items()}


def join_exponent(body, sups):
    """Re-attach a scientific-notation exponent that was typeset as a superscript.

    '1.08x10' + ['5']  -> 1.08e5 ;  '7x10' + ['-6'] -> 7e-6.
    Superscripts that are not exponents (footnote letters, degree signs,
    annotation temperatures) are returned separately as markers."""
    body = norm(body)
    exp, marks = None, []
    for s in sups:
        s = norm(s)
        if body.endswith("x10") and exp is None and re.fullmatch(r"-?\d{1,2}", s):
            exp = s
        else:
            marks.append(s)
    if body.endswith("x10"):
        if exp is None:
            exp = "0"           # '...x10' with the exponent lost: treat as x10^0
        return "%se%s" % (body[:-3], exp), marks
    return body, marks


# compact exponent notation used throughout Appendix C:  1.234-5 == 1.234e-5
SUP = {"−": "-", "–": "-", "‐": "-", "×": "x"}


def norm(s):
    for k, v in SUP.items():
        s = s.replace(k, v)
    return s


def cnum(tok):
    """Parse Appendix-C compact notation '1.234-5' / '3.605+3' -> float."""
    t = norm(tok).strip()
    m = re.fullmatch(r"([0-9]*\.?[0-9]+)([+-])([0-9]{1,2})", t)
    if m:
        return float(m.group(1)) * 10.0 ** (int(m.group(3)) * (1 if m.group(2) == "+" else -1))
    return float(t)


def sci(tok):
    """Parse '2.7x10-6' / '1.08x105' style numbers from Table A.3."""
    t = norm(tok).replace(" ", "")
    m = re.fullmatch(r"([0-9]*\.?[0-9]+)x10(-?[0-9]+)", t)
    if m:
        return float(m.group(1)) * 10.0 ** int(m.group(2))
    return float(t)


class Problem(Exception):
    pass


def check(cond, msg):
    if not cond:
        raise Problem(msg)


def close(a, b, rel=1e-6, abs_=0.0):
    return abs(a - b) <= max(abs_, rel * max(abs(a), abs(b)))


# ==================================================================== Table A.1
# Table A.1 is a short, typographically fussy table (values split over lines with
# parenthetical alternate units).  It is transcribed here and then *verified*
# against the page text: every numeric string below must occur on printed p. 555.
A1_CONSTANTS = [
    # name, symbol, value, unit, verify-string (as printed, spaces included)
    ("Speed of light (in vacuum)", "c", 2.99792458e8, "m/s", "2.997 924 58"),
    ("Electron charge", "e", 1.60217653e-19, "C", "1.602 176 53"),
    ("Atomic mass unit", "u", 1.6605389e-27, "kg", "1.660 538 9"),
    ("Atomic mass unit (energy)", "u c^2", 931.494043, "MeV", "931.494 043"),
    ("Electron rest mass", "m_e", 9.1093826e-31, "kg", "9.109 382 6"),
    ("Electron rest mass (energy)", "m_e c^2", 0.51099892, "MeV", "0.510 998 92"),
    ("Electron rest mass (u)", "m_e", 5.48579909e-4, "u", "5.485 799 09"),
    ("Proton rest mass", "m_p", 1.67262171e-27, "kg", "1.672 621 71"),
    ("Proton rest mass (energy)", "m_p c^2", 938.27203, "MeV", "938.272 03"),
    ("Proton rest mass (u)", "m_p", 1.0072764669, "u", "1.007 276 466 9"),
    ("Neutron rest mass", "m_n", 1.6749273e-27, "kg", "1.674 927 3"),
    ("Neutron rest mass (energy)", "m_n c^2", 939.56536, "MeV", "939.565 36"),
    ("Neutron rest mass (u)", "m_n", 1.0086649156, "u", "1.008 664 915 6"),
    ("Planck's constant", "h", 6.6260693e-34, "J s", "6.626 069 3"),
    ("Planck's constant (eV)", "h", 4.1356674e-15, "eV s", "4.135 667 4"),
    ("Avogadro's constant", "N_a", 6.0221415e23, "1/mol", "6.022 141 5"),
    ("Boltzmann constant", "k", 1.3806505e-23, "J/K", "1.380 650 5"),
    ("Boltzmann constant (eV)", "k", 8.617343e-5, "eV/K", "8.617 343"),
    ("Ideal gas constant (STP)", "R", 8.314472, "J/(mol K)", "8.314 472"),
    ("Electric constant", "eps_0", 8.854187817e-12, "F/m", "8.854 187 817"),
]


def table_A1():
    page = 555 + PRINTED_TO_PDF
    txt = raw_text(page, page)
    missing = [v for *_, v in A1_CONSTANTS if v not in txt]
    check(not missing, "Table A.1: transcribed values not found on printed p.555: %r" % missing[:4])
    rows = [{"constant": n, "symbol": s, "value": repr(v), "unit": u}
            for n, s, v, u, _ in A1_CONSTANTS]
    # sanity: E = mc^2 consistency between the kg and MeV entries of the neutron
    u_kg, u_mev = 1.6605389e-27, 931.494043
    mn_kg, mn_mev = 1.6749273e-27, 939.56536
    check(close(mn_kg / u_kg, mn_mev / u_mev, rel=2e-6),
          "Table A.1: neutron mass kg/MeV entries inconsistent")
    return rows


# ==================================================================== Table A.3
A3_PAGES = (560 + PRINTED_TO_PDF, 561 + PRINTED_TO_PDF)   # printed 560-561

# Column bands, given as *right-edge* (x1) ranges: the table is right-aligned,
# and the two printed pages differ by several points in their left margins.
A3_COLS = [
    ("Z", 120.0, 145.0),
    ("symbol", 145.0, 170.0),
    ("atomic_weight", 170.0, 228.0),
    ("density_g_cm3", 228.0, 268.0),
    ("melting_C", 268.0, 312.0),
    ("boiling_C", 312.0, 350.0),
    ("solar_system_pct", 350.0, 398.0),
    ("crustal_mg_per_kg", 398.0, 440.0),
    ("ocean_mg_per_L", 440.0, 530.0),
]
# superscript markers the book uses on melting/boiling points and densities
A3_MARKS = {"t": "critical temperature", "s": "sublimation temperature",
            "a": "footnote a", "◦": "degC annotation", "°": "degC annotation"}


def table_A3():
    out = []
    for page in range(A3_PAGES[0], A3_PAGES[1] + 1):
        ws = words_of(page, page)[0]
        for band in banded_rows(ws):
            cols = by_columns(band, A3_COLS)
            zb, _ = cols["Z"]
            sb, smarks = cols["symbol"]
            if not re.fullmatch(r"\d{1,3}", zb) or not re.fullmatch(r"[A-Z][a-z]?", sb):
                continue
            Z = int(zb)
            if not (1 <= Z <= 92) or sb not in Z_OF or Z_OF[sb] != Z:
                continue
            rec = {"Z": Z, "symbol": sb}
            notes = []
            if smarks:
                notes.append("symbol marker %s" % "".join(smarks))
            for name in ("atomic_weight", "density_g_cm3", "melting_C", "boiling_C",
                         "solar_system_pct", "crustal_mg_per_kg", "ocean_mg_per_L"):
                body, sups = cols[name]
                val, marks = join_exponent(body, sups)
                # trailing t/s markers are printed inline on some MP/BP entries
                tail = re.search(r"([ts]+)$", val)
                if tail and name in ("melting_C", "boiling_C"):
                    marks = list(marks) + list(tail.group(1))
                    val = val[: tail.start()]
                rec[name] = val
                if marks:
                    notes.append("%s:%s" % (name.split("_")[0], "".join(marks)))
            rec["note"] = "; ".join(notes)
            out.append(rec)
    out.sort(key=lambda r: r["Z"])
    # ---- validation
    Zs = [r["Z"] for r in out]
    check(Zs == list(range(1, 93)),
          "Table A.3: expected Z=1..92, got %d rows (%s)" % (len(out), Zs[:5]))
    aw = {}
    for r in out:
        aw[r["Z"]] = float(re.sub(r"[^0-9.]", "", r["atomic_weight"]))
    anchors = {1: 1.00794, 2: 4.002602, 6: 12.0107, 8: 15.9994, 26: 55.845,
               92: 238.0289, 43: 98.0, 61: 145.0}
    for Z, w in anchors.items():
        check(close(aw[Z], w, rel=1e-4), "Table A.3: atomic weight Z=%d got %s want %s" % (Z, aw[Z], w))
    # atomic weight rises with Z except the four classic inversions
    inversions = {(18, 19), (27, 28), (52, 53), (90, 91)}
    for Z in range(1, 92):
        if aw[Z] > aw[Z + 1]:
            check((Z, Z + 1) in inversions,
                  "Table A.3: unexpected mass inversion at Z=%d->%d" % (Z, Z + 1))
    # every numeric field must parse (blank allowed -- Tc, Pm, At, Fr have no
    # natural abundance, and several synthetics have no measured density)
    for r in out:
        for k in ("density_g_cm3", "melting_C", "boiling_C", "solar_system_pct",
                  "crustal_mg_per_kg", "ocean_mg_per_L"):
            if r[k]:
                try:
                    float(r[k])
                except ValueError:
                    raise Problem("Table A.3: Z=%d %s=%r not numeric" % (r["Z"], k, r[k]))
    # spot-check a scientific-notation cell whose exponent is a superscript
    h = next(r for r in out if r["Z"] == 1)
    check(close(float(h["ocean_mg_per_L"]), 1.08e5, rel=1e-9),
          "Table A.3: H ocean concentration %r (superscript exponent lost?)" % h["ocean_mg_per_L"])
    he = next(r for r in out if r["Z"] == 2)
    check(close(float(he["ocean_mg_per_L"]), 7e-6, rel=1e-9),
          "Table A.3: He ocean concentration %r" % he["ocean_mg_per_L"])
    return out


# ==================================================================== Table A.4
A4_PAGES = (562 + PRINTED_TO_PDF, 569 + PRINTED_TO_PDF)   # printed 562-569

# Modern IUPAC symbols indexed by Z (position 0 is the free neutron).
ELEMENTS = (
    "n H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni "
    "Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe "
    "Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg "
    "Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg "
    "Bh Hs Mt Ds Rg"
).split()
Z_OF = {el: i for i, el in enumerate(ELEMENTS)}

# The book predates the settled IUPAC names for the transactinides and is not
# even self-consistent: Table A.2 prints Ha(105) and Ns(107), while Appendix B
# (Audi-Wapstra 1995) prints Db(104), Jl(105), Rf(106), Hn(108).  Note that
# "Db" and "Rf" mean *different elements* in Appendix B than they do today, so
# a symbol alone cannot be trusted above Z=103 -- the Z column decides.
LEGACY_SYMBOLS = {"Ha": 105, "Ns": 107, "Jl": 105, "Hn": 108, "Uun": 110, "Uuu": 111}
FIRST_TRANSACTINIDE = 104


def z_of(sym):
    """Atomic number for a printed symbol, honouring the book's legacy names.
    Returns None when the symbol is ambiguous or unknown."""
    if sym in LEGACY_SYMBOLS:
        return LEGACY_SYMBOLS[sym]
    return Z_OF.get(sym)

# Table A.4 prints two records side by side, and the left margin of the pair
# drifts by several points from page to page.  Rather than pin absolute columns,
# records are located structurally: a record begins wherever a superscript
# (small-face) mass number is immediately followed by a body-face element
# symbol.  Everything up to the next such position belongs to that record.
#
# The abundance is set in a smaller face (h~5.7) than the decay modes (h~8.0);
# that is what separates "0.250 b+(83) b-(17)" into its two fields.
A4_ABUND_H = 7.0
A4_META = r"(\d{1,3})([mn]\d?)?"
# time units used in the half-life column (SI prefixes on the year)
A4_UNITS = {"ys", "zs", "as", "fs", "ps", "ns", "us", "µs", "ms", "s", "min",
            "h", "d", "y", "ky", "My", "Gy", "Ty", "Py", "Ey", "Zy", "Yy"}


def _a4_record_starts(band):
    """Indices in `band` where a new nuclide record begins."""
    out = []
    for i, w in enumerate(band[:-1]):
        nxt = band[i + 1]
        if (w.h < A4_ABUND_H and re.fullmatch(A4_META, norm(w.t))
                and nxt.h >= A4_ABUND_H and z_of(norm(nxt.t)) is not None):
            out.append(i)
    return out


def table_A4():
    recs = []
    for page in range(A4_PAGES[0], A4_PAGES[1] + 1):
        ws = words_of(page, page)[0]
        for band in rows_of(ws, y_tol=3.0):
            starts = _a4_record_starts(band)
            for k, i0 in enumerate(starts):
                i1 = starts[k + 1] if k + 1 < len(starts) else len(band)
                rec = band[i0:i1]
                m = re.fullmatch(A4_META, norm(rec[0].t))
                A, meta = int(m.group(1)), m.group(2) or ""
                sym = norm(rec[1].t)
                if not (1 <= A <= 300) or A < z_of(sym):
                    continue
                # --- half-life: 'stable', or a number optionally followed by a
                # unit.  Limits are printed relationally ("123Te  >600 Ty"), and
                # the relational sign may be its own token.
                j, half = 2, ""
                rel = ""
                if j < len(rec) and norm(rec[j].t) in (">", "<", "≥", "≤", "~", "≃"):
                    rel, j = norm(rec[j].t), j + 1
                if j < len(rec) and norm(rec[j].t) == "stable":
                    half, j = "stable", j + 1
                elif j < len(rec) and re.fullmatch(r"[<>≥≤~≃]?[0-9]*\.?[0-9]+", norm(rec[j].t)):
                    half, j = rel + norm(rec[j].t), j + 1
                    if j < len(rec) and norm(rec[j].t) in A4_UNITS:
                        half, j = half + " " + norm(rec[j].t), j + 1
                if not half:
                    continue
                # --- remainder: bold abundance and/or decay modes
                abundance, modes = [], []
                for w in rec[j:]:
                    t = norm(w.t)
                    if w.h < A4_ABUND_H and re.fullmatch(r"[0-9]*\.?[0-9]+\.?", t):
                        abundance.append(t)
                    else:
                        modes.append(t)
                recs.append({
                    "nuclide": "%d%s%s" % (A, meta, sym),
                    "Z": z_of(sym),
                    "A": A,
                    "symbol": ELEMENTS[z_of(sym)],
                    "metastable": meta,
                    "half_life": half,
                    "abundance_pct": "".join(abundance).rstrip("."),
                    "decay_modes": re.sub(r"\s+", "", "".join(modes)),
                })
    # ---- validation against independently-known abundances
    by = {}
    for r in recs:
        by.setdefault(r["nuclide"], r)
    anchors = {"1H": 99.9885, "12C": 98.93, "16O": 99.757, "235U": 0.7204,
               "238U": 99.2742, "40K": 0.0117, "56Fe": 91.754}
    for nuc, want in anchors.items():
        check(nuc in by, "Table A.4: missing %s" % nuc)
        got = by[nuc]["abundance_pct"]
        check(got != "" and close(float(got), want, rel=2e-3),
              "Table A.4: %s abundance got %r want %s" % (nuc, got, want))
    check(len(recs) > 900, "Table A.4: only %d records parsed" % len(recs))
    # every element symbol seen must be a real one, and A >= Z
    for r in recs:
        check(r["A"] >= r["Z"], "Table A.4: A<Z for %s" % r["nuclide"])
    recs.sort(key=lambda r: (r["Z"], r["A"], r["metastable"]))
    return recs


# ==================================================================== Table B.1
B_PAGES = PAGES["B"]

# mass digit-groups are separated by single spaces; one PDF text-layer artifact
# renders a group separator as '.', so allow that and normalise below
B_REC = re.compile(
    r"(\d{1,3})\s+(\d{1,3})\s+(?:(\d{1,3})\s+)?([A-Z][a-z]?|n)\s+(\d+\.\d+(?:[ .]\d+)*)")


def _b_mass(s):
    """'1.008 664 923 3' -> 1.0086649233 ; '211.991 887.5' -> 211.9918875"""
    head, _, tail = s.partition(".")
    return float(head + "." + re.sub(r"[ .]", "", tail))


def table_B1():
    txt = raw_text(B_PAGES[0], B_PAGES[1])
    rows, rejected = [], []
    for line in txt.splitlines():
        for m in B_REC.finditer(line):
            N, Z, A, el, mass = m.groups()
            N, Z = int(N), int(Z)
            try:
                mass = _b_mass(mass)
            except ValueError:
                rejected.append(line)
                continue
            if A is not None and int(A) != N + Z:
                rejected.append(line)
                continue
            if abs(mass - (N + Z)) > 0.35:      # atomic mass must sit within ~0.35 u of A
                rejected.append(line)
                continue
            if Z >= len(ELEMENTS):
                rejected.append(line)
                continue
            # Below the transactinides the printed symbol must agree with Z;
            # at and above Z=104 the book's symbol set conflicts with today's,
            # so Z governs and the printed symbol is kept for the record.
            if Z < FIRST_TRANSACTINIDE and el != ELEMENTS[Z]:
                rejected.append(line)
                continue
            rows.append({"N": N, "Z": Z, "A": N + Z, "symbol": ELEMENTS[Z],
                         "book_symbol": el if el != ELEMENTS[Z] else "",
                         "atomic_mass_u": "%.12g" % mass})
    # ---- validation
    check(len(rows) > 2800, "Table B.1: only %d nuclides parsed" % len(rows))
    seen = {}
    for r in rows:
        key = (r["N"], r["Z"])
        check(key not in seen, "Table B.1: duplicate nuclide N=%d Z=%d" % key)
        seen[key] = r
    anchors = {
        (1, 0): ("n", 1.0086649233), (0, 1): ("H", 1.0078250321),
        (1, 1): ("H", 2.0141017780), (1, 2): ("He", 3.0160293097),
        (2, 2): ("He", 4.0026032497), (6, 6): ("C", 12.0),
        (143, 92): ("U", 235.0439231), (146, 92): ("U", 238.0507826),
    }
    for (N, Z), (sym, want) in anchors.items():
        check((N, Z) in seen, "Table B.1: missing N=%d Z=%d" % (N, Z))
        got = seen[(N, Z)]
        check(got["symbol"] == sym, "Table B.1: N=%d Z=%d symbol %s != %s" % (N, Z, got["symbol"], sym))
        check(close(float(got["atomic_mass_u"]), want, rel=1e-9, abs_=1e-9),
              "Table B.1: N=%d Z=%d mass %s != %s" % (N, Z, got["atomic_mass_u"], want))
    # 12C is the definition of the scale -- must be exact
    check(float(seen[(6, 6)]["atomic_mass_u"]) == 12.0, "Table B.1: 12C is not exactly 12 u")
    rows.sort(key=lambda r: (r["Z"], r["A"]))
    return rows


# ==================================================================== Table C.1
C1_PAGES = (589 + PRINTED_TO_PDF, 590 + PRINTED_TO_PDF)


C1_SUB = {"γ": "gamma", "α": "alpha", "s": "s", "t": "t", "f": "f", "p": "p", "n": "n"}
BARN = {"mb": 1e-3, "ub": 1e-6, "µb": 1e-6, "b": 1.0, "kb": 1e3}
C1_UNITS = {"y", "d", "h", "m", "s", "min", "ky", "My", "Gy", "Ty", "Py", "Ey"}


def table_C1():
    """Table C.1 sets the reaction subscript (gamma, s, t, alpha, f, p) as a
    small glyph that pdftotext often drops into the neighbouring line, so rows
    are rebuilt with `banded_rows` and then read as a token sequence:
        <A> <El> [abundance] [half-life unit] ( sigma <sub> = <value> [unit] )+
    """
    recs = []
    for page in range(C1_PAGES[0], C1_PAGES[1] + 1):
        ws = words_of(page, page)[0]
        for band in banded_rows(ws, big_h=6.0):
            toks = [(norm(w.t), w.h) for w in band]
            if len(toks) < 5:
                continue
            if not (re.fullmatch(r"\d{1,3}", toks[0][0]) and toks[0][1] < 6.0):
                continue
            if not (re.fullmatch(r"[A-Z][a-z]?", toks[1][0]) and z_of(toks[1][0]) is not None):
                continue
            A, sym = int(toks[0][0]), toks[1][0]
            if A < z_of(sym):
                continue
            # everything before the first sigma is abundance and/or half-life
            try:
                first = next(i for i, (t, _) in enumerate(toks) if t == "σ")
            except StopIteration:
                continue
            head = toks[2:first]
            abundance, half = "", ""
            i = 0
            while i < len(head):
                t, _h = head[i]
                if re.fullmatch(r"[0-9]*\.?[0-9]+", t):
                    # scientific half-life:  1.405 x 10 ^10  y  (exponent is a superscript)
                    if (i + 2 < len(head) and head[i + 1][0] == "x" and head[i + 2][0] == "10"):
                        j, exp = i + 3, "0"
                        if j < len(head) and re.fullmatch(r"-?\d{1,2}", head[j][0]) and head[j][1] < 6.0:
                            exp, j = head[j][0], j + 1
                        val = "%se%s" % (t, exp)
                        if j < len(head) and head[j][0] in C1_UNITS:
                            half, i = val + " " + head[j][0], j + 1
                            continue
                        i = j
                        continue
                    if i + 1 < len(head) and head[i + 1][0] in C1_UNITS:
                        half, i = t + " " + head[i + 1][0], i + 2
                        continue
                    abundance = t
                i += 1
            # then repeated  sigma <sub> = <value> [unit]
            i = first
            while i < len(toks):
                if toks[i][0] != "σ":
                    i += 1
                    continue
                sub = toks[i + 1][0] if i + 1 < len(toks) and toks[i + 1][1] < 6.0 else ""
                j = i + (2 if sub else 1)
                if j >= len(toks) or toks[j][0] != "=":
                    i += 1
                    continue
                if j + 1 >= len(toks) or not re.fullmatch(r"[0-9]*\.?[0-9]+", toks[j + 1][0]):
                    i += 1
                    continue
                val = float(toks[j + 1][0])
                unit = toks[j + 2][0] if j + 2 < len(toks) and toks[j + 2][0] in BARN else "b"
                if sub in C1_SUB:
                    recs.append({
                        "nuclide": "%d%s" % (A, sym), "Z": z_of(sym), "A": A,
                        "symbol": sym, "abundance_pct": abundance, "half_life": half,
                        "reaction": C1_SUB[sub], "sigma_b": "%.6g" % (val * BARN[unit]),
                    })
                i = j + 2
    # the printed table covers 27 isotopes (1H..18O, then 232Th..242Pu)
    nuc = {r["nuclide"] for r in recs}
    check(len(nuc) == 27, "Table C.1: %d isotopes (expected 27)" % len(nuc))
    check(len(recs) >= 70, "Table C.1: only %d rows" % len(recs))
    idx = {(r["nuclide"], r["reaction"]): float(r["sigma_b"]) for r in recs}
    for key, want in [(("10B", "alpha"), 3840.0), (("6Li", "alpha"), 941.0),
                      (("1H", "gamma"), 0.333), (("1H", "s"), 30.5),
                      (("235U", "f"), 587.0), (("239Pu", "f"), 749.0),
                      (("238U", "gamma"), 2.73)]:
        check(key in idx, "Table C.1: missing %r" % (key,))
        check(close(idx[key], want, rel=1e-3), "Table C.1: %r got %s want %s" % (key, idx[key], want))
    # sigma_t must be >= each partial cross section of the same nuclide
    part = {}
    for r in recs:
        part.setdefault(r["nuclide"], {})[r["reaction"]] = float(r["sigma_b"])
    for n, d in part.items():
        if "t" in d:
            for k, v in d.items():
                check(k == "t" or v <= d["t"] * 1.001,
                      "Table C.1: %s sigma_%s=%g exceeds sigma_t=%g" % (n, k, v, d["t"]))
    # scientific-notation half-lives must have survived the superscript exponent
    half = {r["nuclide"]: r["half_life"] for r in recs}
    check(half.get("235U", "").startswith("7.038e8"),
          "Table C.1: 235U half-life %r" % half.get("235U"))
    check(half.get("232Th", "").startswith("1.405e10"),
          "Table C.1: 232Th half-life %r" % half.get("232Th"))
    return recs


# ==================================================================== Table C.2
C2_PAGES = (590 + PRINTED_TO_PDF, 590 + PRINTED_TO_PDF)


def _pairs(toks):
    """Indices where a superscript mass number is followed by an element symbol."""
    out = []
    for i in range(len(toks) - 1):
        (t, h), (t2, h2) = toks[i], toks[i + 1]
        if h < 6.0 and re.fullmatch(r"\d{1,3}[mn]?", t) and h2 >= 6.0 and z_of(t2) is not None:
            out.append(i)
    return out


def _time(toks, i):
    """Read '<number> <unit>' at position i; return (text, next_index) or (None, i)."""
    if i + 1 < len(toks) and re.fullmatch(r"[0-9]*\.?[0-9]+", toks[i][0]) \
            and toks[i + 1][0] in C1_UNITS:
        return toks[i][0] + " " + toks[i + 1][0], i + 2
    return None, i


def table_C2():
    recs = []
    ws = words_of(C2_PAGES[0], C2_PAGES[1])[0]
    for band in banded_rows(ws, big_h=6.0):
        toks = [(norm(w.t), w.h) for w in band]
        ps = _pairs(toks)
        if len(ps) != 2:                       # data rows carry exactly two nuclides
            continue
        i0, i1 = ps
        aA, aS = toks[i0][0], toks[i0 + 1][0]
        pA, pS = toks[i1][0], toks[i1 + 1][0]
        a_half, j = _time(toks, i0 + 2)
        if a_half is None or j > i1:
            continue
        k = i1 + 2
        p_half, k2 = _time(toks, k)
        p_abund = ""
        if p_half is not None:
            k = k2
        elif k < len(toks) and re.fullmatch(r"[0-9]*\.?[0-9]+", toks[k][0]):
            p_abund, k = toks[k][0], k + 1
        sigma = ""
        if k < len(toks) and re.fullmatch(r"[0-9]*\.?[0-9]+", toks[k][0]):
            val = float(toks[k][0])
            unit = toks[k + 1][0] if k + 1 < len(toks) and toks[k + 1][0] in BARN else "b"
            sigma = "%.6g" % (val * BARN[unit])
        recs.append({
            "activated_nuclide": "%s%s" % (aA, aS), "activated_half_life": a_half,
            "parent_nuclide": "%s%s" % (pA, pS),
            "parent_abundance_pct": p_abund, "parent_half_life": p_half or "",
            "activation_sigma_b": sigma,
        })
    check(len(recs) >= 25, "Table C.2: only %d rows" % len(recs))
    idx = {r["activated_nuclide"]: r for r in recs}
    for nuc, sig in [("24Na", 0.530), ("60Co", 16.8), ("56Mn", 13.3), ("198Au", 98.65)]:
        check(nuc in idx, "Table C.2: missing %s" % nuc)
        check(close(float(idx[nuc]["activation_sigma_b"]), sig, rel=1e-3),
              "Table C.2: %s sigma %s want %s" % (nuc, idx[nuc]["activation_sigma_b"], sig))
    # the activated nuclide is the parent plus one neutron
    for r in recs:
        a = int(re.match(r"(\d+)", r["activated_nuclide"]).group(1))
        p = int(re.match(r"(\d+)", r["parent_nuclide"]).group(1))
        check(a in (p + 1, p), "Table C.2: %s is not %s + n" %
              (r["activated_nuclide"], r["parent_nuclide"]))
    return recs


# ==================================================================== Table C.3
# printed 591-595: air, water, concrete, iron, lead (one material per ~1 page)
C3_PAGES = (591 + PRINTED_TO_PDF, 595 + PRINTED_TO_PDF)
C3_MATERIALS = [
    ("air", "dry air near sea level", 1.205e-3),
    ("water", "water", 1.0),
    ("concrete", "ANSI/ANS-6.4.3 standard concrete", 2.30),
    ("iron", "natural iron", 7.874),
    ("lead", "natural lead", 11.35),
]


def table_C3():
    """Returns {material: [row,...]}. Rows carry an 'edge' flag for the
    duplicated absorption-edge energies (e.g. 0.00320 and 0.00320K)."""
    txt = raw_text(C3_PAGES[0], C3_PAGES[1])
    # Split the stream at each caption; the caption names the material.  The
    # caption text is matched loosely -- "ANSI/ANS-6.4.3 standard concrete"
    # contains periods, so anything anchored on sentence punctuation misses it.
    marks = []
    for m in re.finditer(r"Mass coefficients \(cm2\s*/g\)\s+for\b", txt):
        marks.append((m.start(), txt[m.start():m.start() + 160].lower()))
    check(len(marks) >= 5, "Table C.3: found %d captions" % len(marks))

    def material_of(desc):
        for key, _, _ in C3_MATERIALS:
            if key in desc:
                return key
        return None

    segs = []
    for i, (pos, desc) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(txt)
        mat = material_of(desc)
        if mat:
            segs.append((mat, txt[pos:end]))

    data = {k: [] for k, _, _ in C3_MATERIALS}
    # Edge suffixes: lead carries M1..M5 as well as K and L1..L3.  A bare "M"
    # here silently dropped all five lead M-edge rows, because the trailing digit
    # then broke the \s+ that follows.
    row_re = re.compile(r"^\s*([0-9]*\.?[0-9]+)(K|L[123]|M[12345])?\s+(.*)$")
    # The exponent is OPTIONAL.  Appendix C prints coefficients of order unity
    # with no exponent at all (lead's photoelectric column reads "7.291", not
    # "7.291+0"), and requiring one dropped every row containing such a value --
    # including lead's K edge at 88 keV and the whole 0.05-0.15 MeV decade.
    numtok = re.compile(r"[0-9]*\.?[0-9]+(?:[+-][0-9]{1,2})?")
    for mat, seg in segs:
        for line in seg.splitlines():
            line = norm(line.rstrip())
            m = row_re.match(line)
            if not m:
                continue
            E, edge, rest = m.groups()
            # A data row is pure numbers.  The caption lines carry a density and
            # a composition ("2.3 g/cm3 . Composition by weight fraction: H
            # 0.005599, O 0.498250, ...") which the row pattern otherwise reads
            # as an energy followed by six coefficients.  The old strict-exponent
            # token regex rejected those by accident; reject them on purpose.
            if re.search(r"[A-Za-z]", rest):
                continue
            vals = numtok.findall(rest)
            if len(vals) not in (5, 6):
                continue
            v = [cnum(x) for x in vals]
            if len(v) == 5:                      # below pair-production threshold
                mu_c, mu_ph, mu, mu_tr, mu_en = v
                mu_pp = 0.0
            else:
                mu_c, mu_ph, mu_pp, mu, mu_tr, mu_en = v
            data[mat].append({
                "E_MeV": E, "edge": edge or "",
                "mu_c_cm2_g": "%.4g" % mu_c, "mu_ph_cm2_g": "%.4g" % mu_ph,
                "mu_pp_cm2_g": "%.4g" % mu_pp, "mu_cm2_g": "%.4g" % mu,
                "mu_tr_cm2_g": "%.4g" % mu_tr, "mu_en_cm2_g": "%.4g" % mu_en,
            })
    # ---- validation
    # Every absorption edge printed in the table must survive parsing.  An
    # earlier regex dropped lead's K edge and all five M edges without tripping
    # the row-count check, because enough other rows remained.
    C3_REQUIRED_EDGES = {
        "iron": {"K"},
        "lead": {"K", "L1", "L2", "L3", "M1", "M2", "M3", "M4", "M5"},
    }
    for mat, want in C3_REQUIRED_EDGES.items():
        got = {r["edge"] for r in data[mat] if r["edge"]}
        check(want <= got, "Table C.3 (%s): missing edge rows %s"
              % (mat, sorted(want - got)))
    # and the energy decade around lead's K edge must not be a hole
    lead_E = sorted(float(r["E_MeV"]) for r in data["lead"])
    in_gap = [e for e in lead_E if 0.04 < e < 0.20]
    check(len(in_gap) >= 5, "Table C.3 (lead): only %d rows between 0.04 and "
          "0.20 MeV -- the K edge region looks truncated" % len(in_gap))

    for mat, rows in data.items():
        check(len(rows) >= 40, "Table C.3 (%s): only %d rows" % (mat, len(rows)))
        for r in rows:
            tot = float(r["mu_c_cm2_g"]) + float(r["mu_ph_cm2_g"]) + float(r["mu_pp_cm2_g"])
            check(close(tot, float(r["mu_cm2_g"]), rel=2e-3),
                  "Table C.3 (%s) E=%s: mu_c+mu_ph+mu_pp=%.5g != mu=%s"
                  % (mat, r["E_MeV"], tot, r["mu_cm2_g"]))
            check(float(r["mu_en_cm2_g"]) <= float(r["mu_tr_cm2_g"]) * 1.001 + 1e-12,
                  "Table C.3 (%s) E=%s: mu_en > mu_tr" % (mat, r["E_MeV"]))
            # pair production is impossible below 1.022 MeV
            if float(r["E_MeV"]) < 1.022:
                check(float(r["mu_pp_cm2_g"]) == 0.0,
                      "Table C.3 (%s) E=%s: nonzero mu_pp below threshold" % (mat, r["E_MeV"]))
        E = [float(r["E_MeV"]) for r in rows]
        check(all(b >= a for a, b in zip(E, E[1:])), "Table C.3 (%s): energies not sorted" % mat)
    # anchors: NIST/Seltzer values the book reproduces
    def at(mat, e):
        for r in data[mat]:
            if abs(float(r["E_MeV"]) - e) < 1e-9 and not r["edge"]:
                return r
        raise Problem("Table C.3 (%s): no row at E=%s" % (mat, e))
    check(close(float(at("air", 1.0)["mu_cm2_g"]), 6.353e-2, rel=2e-3), "C.3 air mu@1MeV")
    check(close(float(at("water", 1.0)["mu_cm2_g"]), 7.072e-2, rel=5e-3), "C.3 water mu@1MeV")
    check(close(float(at("lead", 1.0)["mu_cm2_g"]), 7.102e-2, rel=5e-2), "C.3 lead mu@1MeV")
    return data


# ==================================================================== Appendix D
D_PAGES = PAGES["D"]
D_GROUP_BY_TEXT = {
    "Principal Beta Particles": "beta",
    "Positrons": "positron",
    "Conversion/Auger Electrons": "conversion_auger_electron",
    "Principal Gamma and X Rays": "gamma_xray",
    "Alpha Particles": "alpha",
    "Principal Alpha Particles": "alpha",
    "Principal X Rays": "xray",
    "Principal Gamma Rays": "gamma",
    "Neutrinos": "neutrino",
}
D_GUTTER = 306.0        # x that separates the two record columns
D_BIG_H = 6.5           # above this is body text; below it is a true superscript
D_SYM_H = 9.0           # the element symbol is set noticeably larger


def table_D():
    """Parse Appendix D's two-column, per-nuclide radiation records.

    Each record opens with a nuclide header (mass number typeset above the
    atomic number, then the symbol, then '(half-life)'), followed by one or
    more radiation groups.  Each group is a small table whose last line is
    'keV/decay <total>', optionally flagged '*' when the listed lines account
    for < 95% of the group total.
    """
    detail, totals = [], []
    for page in range(D_PAGES[0], D_PAGES[1] + 1):
        pages = words_of(page, page)
        if not pages:
            continue
        ws = pages[0]
        if not ws:
            continue
        # two record columns; find the gutter as the page mid-line
        for col_words in split_columns_page(ws, D_GUTTER):
            _parse_D_column(col_words, detail, totals)
    # ---- validation
    check(len(totals) > 300, "Appendix D: only %d group totals" % len(totals))
    nucs = {t["nuclide"] for t in totals}
    for want in ("60Co", "137Cs", "137mBa", "131I", "3H", "222Rn", "40K"):
        check(want in nucs, "Appendix D: missing %s" % want)

    def has_line(nuc, group, e):
        return any(d["nuclide"] == nuc and d["group"] == group
                   and close(float(d["E_keV"]), e, rel=1e-4)
                   for d in detail if d["E_keV"])

    # gamma lines every health physicist knows by heart
    check(has_line("60Co", "gamma_xray", 1173.2), "Appendix D: 60Co 1173.2 keV missing")
    check(has_line("60Co", "gamma_xray", 1332.5), "Appendix D: 60Co 1332.5 keV missing")
    # the 661.6 keV photon is emitted by the daughter 137mBa, not by 137Cs itself
    check(has_line("137mBa", "gamma_xray", 661.6), "Appendix D: 137mBa 661.6 keV missing")
    check(has_line("131I", "gamma_xray", 364.5), "Appendix D: 131I 364.5 keV missing")
    check(has_line("222Rn", "alpha", 5489.7), "Appendix D: 222Rn 5489.7 keV alpha missing")
    # 3H's beta spectrum: <E> = 5.67 keV, endpoint 18.6 keV
    tri = [d for d in detail if d["nuclide"] == "3H" and d["group"] == "beta"]
    check(len(tri) == 1 and close(float(tri[0]["E_avg_keV"]), 5.67, rel=1e-3)
          and close(float(tri[0]["E_max_keV"]), 18.6, rel=1e-3),
          "Appendix D: 3H beta line wrong: %r" % tri)
    # a beta group's mean energy can never exceed its endpoint
    for d in detail:
        if d["E_avg_keV"] and d["E_max_keV"]:
            check(float(d["E_avg_keV"]) <= float(d["E_max_keV"]) * 1.0001,
                  "Appendix D: %s Eav > Emax" % d["nuclide"])
    # frequencies are percentages (annihilation pairs legitimately exceed 100)
    for d in detail:
        check(0.0 < float(d["freq_pct"]) <= 210.0,
              "Appendix D: %s implausible frequency %s" % (d["nuclide"], d["freq_pct"]))
    return detail, totals


def split_columns_page(ws, boundary):
    return [[w for w in ws if w.x0 < boundary], [w for w in ws if w.x0 >= boundary]]


def _d_value(toks, i):
    """Read a number at toks[i], absorbing a 'x 10 ^e' scientific tail and a
    trailing '*' completeness flag.  Returns (value, incomplete, next_index)."""
    if i >= len(toks) or not re.fullmatch(r"[0-9]*\.?[0-9]+", toks[i][0]):
        return None, False, i
    v, i = float(toks[i][0]), i + 1
    if i + 1 < len(toks) and toks[i][0] in ("x", "*x") and toks[i + 1][0] == "10":
        i += 2
        if i < len(toks) and re.fullmatch(r"-?\d{1,3}", toks[i][0]) and toks[i][1] < D_BIG_H:
            v *= 10.0 ** int(toks[i][0])
            i += 1
    inc = False
    while i < len(toks) and toks[i][0] in ("∗", "*", "†", "a", "b"):
        inc = inc or toks[i][0] in ("∗", "*")
        i += 1
    return v, inc, i


def _parse_D_column(ws, detail, totals):
    """One record column of Appendix D.

    A nuclide header is typeset as a stack -- mass number on the line above,
    element symbol (in a larger face) with the half-life in parentheses, then
    the atomic number on the line below:

            3
           1H  (12.33 y)
    """
    bands = banded_rows(ws, big_h=D_BIG_H)
    lines = [[(norm(w.t), w.h, w.x0) for w in b] for b in bands]
    nuclide = half = group = None
    pending_A = None
    for k, toks in enumerate(lines):
        if not toks:
            continue
        text = " ".join(t for t, _, _ in toks)
        # --- lone mass number: remember it for the symbol line that follows
        if len(toks) == 1 and re.fullmatch(r"\d{1,3}[mn]?", toks[0][0]):
            pending_A = toks[0][0]
            continue
        # --- symbol + (half-life)
        if toks[0][1] >= D_SYM_H and z_of(toks[0][0]) is not None and pending_A:
            sym = toks[0][0]
            m = re.search(r"\((.+)\)", text)
            if not m:
                continue
            meta = "m" if pending_A.endswith(("m", "n")) else ""
            A = re.sub(r"[^0-9]", "", pending_A)
            # the atomic number on the next line confirms the element
            if k + 1 < len(lines) and len(lines[k + 1]) == 1:
                zt = lines[k + 1][0][0]
                if re.fullmatch(r"\d{1,3}", zt) and int(zt) != z_of(sym):
                    pending_A = None
                    continue
            nuclide, half, group = "%s%s%s" % (A, meta, sym), m.group(1).strip(), None
            pending_A = None
            continue
        # --- group heading
        if text in D_GROUP_BY_TEXT:
            group = D_GROUP_BY_TEXT[text]
            continue
        if text.startswith("Freq.") or text.startswith("keV/decay") is False and \
                re.match(r"^[A-Za-z(]", text) and "keV/decay" not in text:
            # column headings and prose: ignore, but do not clear the group
            if not re.match(r"^[0-9]", text):
                continue
        # --- group total
        if toks[0][0] == "keV/decay" and nuclide and group:
            v, inc, _ = _d_value(toks, 1)
            if v is None:
                continue
            totals.append({"nuclide": nuclide, "half_life": half, "group": group,
                           "keV_per_decay": "%.6g" % v, "incomplete": "yes" if inc else ""})
            continue
        # --- an individual radiation: freq then one or two energies
        if nuclide and group and re.fullmatch(r"[0-9]*\.?[0-9]+", toks[0][0]):
            vals, i = [], 0
            while i < len(toks) and len(vals) < 3:
                v, _inc, j = _d_value(toks, i)
                if v is None:
                    break
                vals.append(v)
                i = j
            if len(vals) == 2:
                detail.append({"nuclide": nuclide, "half_life": half, "group": group,
                               "freq_pct": "%.6g" % vals[0], "E_avg_keV": "",
                               "E_max_keV": "", "E_keV": "%.6g" % vals[1]})
            elif len(vals) == 3:
                detail.append({"nuclide": nuclide, "half_life": half, "group": group,
                               "freq_pct": "%.6g" % vals[0], "E_avg_keV": "%.6g" % vals[1],
                               "E_max_keV": "%.6g" % vals[2], "E_keV": ""})


# ==================================================================== errata
# Typographic errors in Table A.4, each caught by the cross-check below and each
# confirmed two ways: the corrected value makes the element's abundances sum to
# exactly 100%, *and* it reproduces the standard atomic weight printed in Table
# A.3.  The CSV keeps the printed value and flags it; only the cross-check uses
# the correction.
A4_ERRATA = {
    "32S":   ("95.02", "94.93"),    # sum 100.09 -> 100.00 ; weight -> 32.066
    "194Pt": ("32.67", "32.967"),   # sum  99.70 -> 100.00 ; weight -> 195.078
}

# Elements where the book's own Table A.3 and Table A.4 disagree by more than
# 3e-4 for reasons we could not resolve to a single typo -- the abundances are
# from a different evaluation than the standard atomic weights.  Listed so the
# validator fails if the set ever *grows*.
A3_A4_KNOWN_DISAGREEMENT = {
    70: "Yb: printed abundances sum to 99.94%, so the rebuilt weight runs 6e-4 low",
    76: "Os: printed abundances sum to 100.14%, so the rebuilt weight runs 1.4e-3 high",
}


# Table C.1 quotes ENDF/B-VI-era isotopic abundances while Table A.4 quotes
# NuBase; six light nuclides differ between the two.  Deuterium is the big one
# (0.015% vs 0.0115%).  Listed so the validator fails if the set ever grows --
# a genuinely misparsed digit would show up here as a new entry.
C1_A4_KNOWN_DISAGREEMENT = {"2H", "6Li", "10B", "13C", "15N", "17O"}


def cross_checks(built):
    """Falsification tests that span tables -- the ones a per-table parser
    cannot fake.  The headline test rebuilds each element's standard atomic
    weight from the isotopic abundances of Table A.4 and the nuclidic masses of
    Table B.1, and compares it with the value printed in Table A.3:

        M(Z)  ==  sum_i  (abundance_i / 100) * M(N_i, Z)

    Agreement to a few parts in 10^4 for ~80 elements can only happen if all
    three tables were read correctly."""
    mass = {(int(r["Z"]), int(r["A"])): float(r["atomic_mass_u"]) for r in built["B1"]}
    a3 = {r["Z"]: float(re.sub(r"[^0-9.]", "", r["atomic_weight"])) for r in built["A3"]}

    # (1) every nuclide named in Table A.4 must exist in the Table B.1 mass table
    missing = [r["nuclide"] for r in built["A4"]
               if r["metastable"] == "" and (r["Z"], r["A"]) not in mass]
    check(not missing, "cross-check: %d A.4 nuclides absent from B.1 (%s)"
          % (len(missing), missing[:6]))

    # (2) rebuild the standard atomic weights
    by_z = {}
    for r in built["A4"]:
        if r["abundance_pct"] and r["metastable"] == "":
            a = float(A4_ERRATA.get(r["nuclide"], (None, r["abundance_pct"]))[1]
                      if r["nuclide"] in A4_ERRATA else r["abundance_pct"])
            by_z.setdefault(r["Z"], []).append((r["A"], a))
    tested, worst, worst_z, outliers = 0, 0.0, None, {}
    for Z, iso in sorted(by_z.items()):
        if Z not in a3:
            continue
        try:
            m = sum((a / 100.0) * mass[(Z, A)] for A, a in iso)
        except KeyError:
            continue
        total = sum(a for _, a in iso)
        rel = abs(m - a3[Z]) / a3[Z]
        if rel >= 3e-4 or abs(total - 100.0) > 0.05:
            outliers[Z] = (total, m, a3[Z], rel)
            continue
        if rel > worst:
            worst, worst_z = rel, Z
        tested += 1
    unexpected = {Z: v for Z, v in outliers.items() if Z not in A3_A4_KNOWN_DISAGREEMENT}
    check(not unexpected,
          "cross-check: unexplained A.3/A.4 mismatch for Z=%s "
          "(sum%%, rebuilt, printed, rel) = %s"
          % (sorted(unexpected), [tuple(round(x, 5) for x in v) for v in unexpected.values()]))
    # the errata must actually be present as printed -- otherwise the correction
    # is silently patching something that is no longer there
    printed = {r["nuclide"]: r["abundance_pct"] for r in built["A4"]}
    for nuc, (was, _now) in A4_ERRATA.items():
        check(printed.get(nuc) == was,
              "cross-check: erratum for %s expects printed %r, found %r"
              % (nuc, was, printed.get(nuc)))
    check(tested >= 70, "cross-check: only %d elements reconstructed" % tested)

    # (3) Table C.1's abundances should track Table A.4's.  They are not from
    # the same evaluation -- C.1 is ENDF/B-VI (1995), A.4 is NuBase -- so the
    # tolerance here is only wide enough to catch a misparsed digit, not tight
    # enough to police the two vintages against each other (13C, for instance,
    # is 1.11% in C.1 and 1.07% in A.4).
    a4ab = {r["nuclide"]: r["abundance_pct"] for r in built["A4"]}
    c1_worst, c1_worst_n, c1_diff = 0.0, None, {}
    for r in built["C1"]:
        if not r["abundance_pct"] or r["nuclide"] not in a4ab or not a4ab[r["nuclide"]]:
            continue
        x, y = float(r["abundance_pct"]), float(a4ab[r["nuclide"]])
        rel = abs(x - y) / max(y, 1e-9)
        if rel > c1_worst:
            c1_worst, c1_worst_n = rel, r["nuclide"]
        if rel > 0.005:
            c1_diff[r["nuclide"]] = (x, y, rel)
    stray = set(c1_diff) - set(C1_A4_KNOWN_DISAGREEMENT)
    check(not stray, "cross-check: undocumented C.1/A.4 abundance disagreement for %s"
          % sorted(stray))

    # (4) every C.3 material must share one energy grid away from absorption edges
    # compare numerically: the book prints the same energy as "0.10" in one
    # table and "0.1" in another
    grids = {m: set(round(float(r["E_MeV"]), 9) for r in rows if not r["edge"])
             for m, rows in built["C3"].items()}
    common = set.intersection(*grids.values())
    check(len(common) >= 30,
          "cross-check: C.3 materials share only %d common energies" % len(common))
    for m, g in grids.items():
        extra = len(g - common)
        check(extra <= 20, "cross-check: C.3 %s has %d energies off the common grid" % (m, extra))
    return {"elements_reconstructed": tested, "worst_rel": worst, "worst_Z": worst_z,
            "outliers": outliers, "c1_worst": c1_worst, "c1_worst_nuclide": c1_worst_n}


# ==================================================================== output
def write_csv(name, rows, fields):
    path = os.path.join(HERE, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path, len(rows)


def _md_table(head, rows):
    out = ["| " + " | ".join(head) + " |",
           "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join("" if c is None else str(c) for c in r) + " |")
    return "\n".join(out)


def write_markdown(built, x):
    """A readable rendering of the small tables plus summaries of the big ones."""
    L = []
    L.append("# Shultis & Faw — Appendix data tables\n")
    L.append("Generated by `_extract.py` from *Fundamentals of Nuclear Science and\n"
             "Engineering*, 3rd ed. (Appendices A–D). The CSVs beside this file are the\n"
             "canonical data; this rendering is for reading. See `README.md` for units,\n"
             "provenance and the errata list.\n")

    L.append("\n## Table A.1 — Fundamental physical constants\n")
    L.append(_md_table(["Constant", "Symbol", "Value", "Unit"],
                       [(r["constant"], "`%s`" % r["symbol"], r["value"], r["unit"])
                        for r in built["A1"]]))

    L.append("\n\n## Table A.3 — Physical properties of the elements\n")
    L.append("%d elements (Z = 1–92). Full data in `A3_element_properties.csv`.\n"
             % len(built["A3"]))
    L.append(_md_table(["Z", "El", "Atomic weight", "Density (g/cm³)", "MP (°C)", "BP (°C)"],
                       [(r["Z"], r["symbol"], r["atomic_weight"], r["density_g_cm3"],
                         r["melting_C"], r["boiling_C"]) for r in built["A3"][:20]]))
    L.append("\n*(first 20 of %d rows)*\n" % len(built["A3"]))

    L.append("\n## Table A.4 — Isotopic abundances and decay data\n")
    stable = [r for r in built["A4"] if r["abundance_pct"]]
    L.append("%d nuclides, of which %d carry a natural abundance. "
             "Full data in `A4_isotopic_abundances.csv`.\n" % (len(built["A4"]), len(stable)))

    L.append("\n## Table B.1 — Atomic masses\n")
    L.append("%d nuclides, Z = 0–%d. Neutral-atom masses in u (Audi–Wapstra 1995); "
             "¹²C = 12 u exactly by definition. Full data in `B1_atomic_masses.csv`.\n"
             % (len(built["B1"]), max(int(r["Z"]) for r in built["B1"])))
    L.append(_md_table(["N", "Z", "A", "El", "Atomic mass (u)"],
                       [(r["N"], r["Z"], r["A"], r["symbol"], r["atomic_mass_u"])
                        for r in built["B1"][:12]]))
    L.append("\n*(first 12 of %d rows)*\n" % len(built["B1"]))

    L.append("\n## Table C.1 — Thermal-neutron cross sections (2200 m/s, 0.0253 eV)\n")
    by = {}
    for r in built["C1"]:
        by.setdefault(r["nuclide"], {})[r["reaction"]] = r["sigma_b"]
    L.append(_md_table(["Nuclide", "σ_γ (b)", "σ_s (b)", "σ_f (b)", "σ_α (b)", "σ_p (b)", "σ_t (b)"],
                       [(n, d.get("gamma", ""), d.get("s", ""), d.get("f", ""),
                         d.get("alpha", ""), d.get("p", ""), d.get("t", ""))
                        for n, d in by.items()]))

    L.append("\n\n## Table C.2 — Thermal-neutron activation products\n")
    L.append(_md_table(["Activated", "Half-life", "Parent", "Abundance (%)",
                        "Parent T½", "σ_activation (b)"],
                       [(r["activated_nuclide"], r["activated_half_life"],
                         r["parent_nuclide"], r["parent_abundance_pct"],
                         r["parent_half_life"], r["activation_sigma_b"])
                        for r in built["C2"]]))

    L.append("\n\n## Table C.3 — Photon mass coefficients (cm²/g)\n")
    for mat, desc, rho in C3_MATERIALS:
        rows = built["C3"][mat]
        L.append("\n**%s** (%s, ρ = %g g/cm³) — %d energies, "
                 "`C3_photon_coefficients_%s.csv`\n" % (mat, desc, rho, len(rows), mat))
    L.append("\nColumns: `mu_c` incoherent (Compton) with binding, `mu_ph` photoelectric,\n"
             "`mu_pp` pair production, `mu` = their sum, `mu_tr` energy transfer,\n"
             "`mu_en` energy absorption. Rows flagged in the `edge` column repeat an\n"
             "energy either side of an absorption edge.\n")
    L.append("\nSelected total mass attenuation coefficients μ/ρ (cm²/g):\n\n")
    energies = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    head = ["Material"] + ["%g MeV" % e for e in energies]
    rows = []
    for mat, _, _ in C3_MATERIALS:
        cells = [mat]
        for e in energies:
            hit = [r for r in built["C3"][mat]
                   if abs(float(r["E_MeV"]) - e) < 1e-9 and not r["edge"]]
            cells.append(hit[0]["mu_cm2_g"] if hit else "—")
        rows.append(cells)
    L.append(_md_table(head, rows))

    detail, totals = built["D"]
    L.append("\n\n## Appendix D — Decay characteristics of selected radionuclides\n")
    L.append("%d nuclides, %d individual radiations, %d per-group energy totals.\n"
             "`D1_decay_radiation.csv` (individual lines) and "
             "`D2_decay_group_totals.csv` (keV per decay by group).\n"
             % (len({t["nuclide"] for t in totals}), len(detail), len(totals)))
    L.append("\nA worked example — ⁶⁰Co:\n\n")
    L.append(_md_table(["Group", "Freq (%)", "E_av (keV)", "E_max (keV)", "E (keV)"],
                       [(d["group"], d["freq_pct"], d["E_avg_keV"], d["E_max_keV"], d["E_keV"])
                        for d in detail if d["nuclide"] == "60Co"]))

    L.append("\n\n## Validation summary\n")
    L.append("- Standard atomic weights rebuilt from Table A.4 abundances × Table B.1\n"
             "  masses and compared with Table A.3: **%d elements agree to better than\n"
             "  3×10⁻⁴** (worst %.1e, at Z=%s).\n"
             % (x["elements_reconstructed"], x["worst_rel"], x["worst_Z"]))
    L.append("- Every nuclide named in Table A.4 exists in the Table B.1 mass table.\n")
    L.append("- Every Table C.3 row satisfies μ = μ_c + μ_ph + μ_pp and μ_en ≤ μ_tr,\n"
             "  with μ_pp = 0 below the 1.022 MeV pair-production threshold.\n")
    L.append("- Every Appendix D beta group satisfies ⟨E⟩ ≤ E_max.\n")
    with open(os.path.join(HERE, "data_tables.md"), "w", encoding="utf-8") as fh:
        fh.write("".join(L) + "\n")


def main():
    global PDF
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    args = ap.parse_args()
    PDF = find_pdf()
    print("book:", PDF)

    built = {}
    built["A1"] = table_A1()
    print("  A.1 constants          %4d" % len(built["A1"]))
    built["A3"] = table_A3()
    print("  A.3 elements           %4d" % len(built["A3"]))
    built["A4"] = table_A4()
    print("  A.4 nuclides           %4d" % len(built["A4"]))
    built["B1"] = table_B1()
    print("  B.1 atomic masses      %4d" % len(built["B1"]))
    built["C1"] = table_C1()
    print("  C.1 cross sections     %4d" % len(built["C1"]))
    built["C2"] = table_C2()
    print("  C.2 activation         %4d" % len(built["C2"]))
    built["C3"] = table_C3()
    for mat, rows in built["C3"].items():
        print("  C.3 %-8s          %4d" % (mat, len(rows)))
    built["D"] = table_D()
    print("  D   radiations         %4d detail, %d totals" % (len(built["D"][0]), len(built["D"][1])))

    x = cross_checks(built)
    print("  cross-check: rebuilt %d standard atomic weights from A.4+B.1; "
          "worst deviation %.1e (Z=%s)" % (x["elements_reconstructed"], x["worst_rel"], x["worst_Z"]))

    if args.check:
        print("\nall validators passed (nothing written)")
        return

    write_csv("A1_physical_constants.csv", built["A1"], ["constant", "symbol", "value", "unit"])
    write_csv("A3_element_properties.csv", built["A3"],
              ["Z", "symbol", "atomic_weight", "density_g_cm3", "melting_C", "boiling_C",
               "solar_system_pct", "crustal_mg_per_kg", "ocean_mg_per_L", "note"])
    for r in built["A4"]:
        was_now = A4_ERRATA.get(r["nuclide"])
        r["note"] = ("printed %s; should be %s (see README errata)" % was_now) if was_now else ""
    write_csv("A4_isotopic_abundances.csv", built["A4"],
              ["nuclide", "Z", "A", "symbol", "metastable", "half_life",
               "abundance_pct", "decay_modes", "note"])
    write_csv("B1_atomic_masses.csv", built["B1"],
              ["N", "Z", "A", "symbol", "book_symbol", "atomic_mass_u"])
    write_csv("C1_thermal_neutron_cross_sections.csv", built["C1"],
              ["nuclide", "Z", "A", "symbol", "abundance_pct", "half_life", "reaction", "sigma_b"])
    write_csv("C2_activation_radionuclides.csv", built["C2"],
              ["activated_nuclide", "activated_half_life", "parent_nuclide",
               "parent_abundance_pct", "activation_sigma_b"])
    for mat, rows in built["C3"].items():
        write_csv("C3_photon_coefficients_%s.csv" % mat, rows,
                  ["E_MeV", "edge", "mu_c_cm2_g", "mu_ph_cm2_g", "mu_pp_cm2_g",
                   "mu_cm2_g", "mu_tr_cm2_g", "mu_en_cm2_g"])
    detail, totals = built["D"]
    write_csv("D1_decay_radiation.csv", detail,
              ["nuclide", "half_life", "group", "freq_pct", "E_avg_keV", "E_max_keV", "E_keV"])
    write_csv("D2_decay_group_totals.csv", totals,
              ["nuclide", "half_life", "group", "keV_per_decay", "incomplete"])
    write_markdown(built, x)
    print("\nwrote CSVs + data_tables.md to", HERE)


if __name__ == "__main__":
    try:
        main()
    except Problem as e:
        sys.exit("VALIDATION FAILED: %s" % e)
