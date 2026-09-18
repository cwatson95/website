#!/usr/bin/env python3
"""
Extract the SI steam tables (Tables A-2 ... A-6) from
  Moran, Shapiro, Boettner & Bailey -- Fundamentals of Engineering
  Thermodynamics, 8th ed.  (modules/Thermo/thermodynamics.pdf)

and emit:
  steam_tables/A2_sat_water_temperature.csv
  steam_tables/A3_sat_water_pressure.csv
  steam_tables/A4_superheated_water.csv
  steam_tables/A5_compressed_liquid_water.csv
  steam_tables/A6_sat_water_solid_vapor.csv
  steam_tables/steam_tables.md     (human-readable rendering)
  steam_tables/README.md           (documentation)

A-2..A-5 are parsed from the PDF text layer by word-coordinate row
clustering.  A-6 (printed rotated 90 deg, so its text layer is
transposed/scrambled) was read from a high-DPI render and is embedded
below; it is guarded by internal-consistency asserts (hig=hg-hi, etc.)
and a cross-check against A-2 at the triple point.

Every table is validated before any file is written: row counts,
monotonicity, known anchor values, and cross-table agreement between the
superheated/compressed saturation lines and the independent A-3 table.

Run from modules/Thermo/ :   python3 steam_tables/_extract.py
"""
import csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDF  = os.path.join(HERE, os.pardir, "thermodynamics.pdf")
OUT  = HERE

# ---------------------------------------------------------------- PDF helpers
def _load_doc():
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("PyMuPDF (fitz) required:  pip install pymupdf")
    return fitz.open(PDF)

NUM = re.compile(r'^-?\.?\d[\d.]*$')
isnum = lambda t: bool(NUM.match(t))

def rows_of(doc, page_idx, y_tol=2.5):
    """Cluster a page's words into visual rows (sorted top->bottom, left->right)."""
    words = [w for w in doc[page_idx].get_text("words") if w[4].strip()]
    words.sort(key=lambda w: (round(w[1], 1), w[0]))
    rows, cur, cy = [], [], None
    for w in words:
        y = (w[1] + w[3]) / 2
        if cy is None or abs(y - cy) <= y_tol:
            cur.append(w); cy = y if cy is None else cy * 0.7 + y * 0.3
        else:
            rows.append(cur); cur = [w]; cy = y
    if cur:
        rows.append(cur)
    rows.sort(key=lambda r: min(w[1] for w in r))
    return [[w[4] for w in r] for r in rows]

def payload(raw, n):
    """Recover an n-wide data row [temp, n-1 numbers] from a band that may carry
    stray watermark/conversion-note tokens ('H2O', '= 102 kPa', ...)."""
    t = list(raw)
    while t and not isnum(t[-1]) and t[-1] != 'Sat.':   # trim trailing junk
        t.pop()
    if 'Sat.' in t:                                      # anchor on the Sat. token
        t = t[t.index('Sat.'):]
    else:
        while t and not isnum(t[0]):                     # trim leading alpha junk
            t.pop(0)
        if len(t) > n:                                   # numeric junk glued in front
            t = t[-n:]
    if len(t) == n and (isnum(t[0]) or t[0] == 'Sat.') and all(isnum(x) for x in t[1:]):
        return t
    return None

# ------------------------------------------------------ A-2 / A-3 (clean rows)
def clean12(doc, pages):
    out = []
    for p in pages:
        for raw in rows_of(doc, p):
            t = payload(raw, 12)
            if t and t[0] == t[11]:        # first & last column repeat the index var
                out.append(t[:11])
    return out

# ----------------------------------------------- A-4 / A-5 (pressure-block rows)
PHDR = re.compile(r'\bp\s+5?\s*([\d.]+)\s+bar')   # '5' is the PDF font's '='
TSAT = re.compile(r'T\s+5?\s*([\d.]+)8C')         # '8C' is the PDF font's 'degC'

def blocks(doc, pages):
    bands = []
    for p in pages:
        bands += rows_of(doc, p)
    recs, cur = [], []
    for i, raw in enumerate(bands):
        ps = PHDR.findall(" ".join(raw))
        if ps:                                       # pressure-header band
            win = " ".join(bands[i] + (bands[i+1] if i+1 < len(bands) else [])
                                    + (bands[i+2] if i+2 < len(bands) else []))
            ts = TSAT.findall(win)
            cur = [(ps[k], (ts[k] if k < len(ts) else None)) for k in range(len(ps))]
            continue
        t = payload(raw, 9)
        if t and len(cur) == 2:                      # full row: both pressures present
            sat = (t[0] == 'Sat.')
            for s, (p_, ts_) in enumerate(cur):
                seg = t[1+4*s:5+4*s]
                T = ts_ if sat else t[0]
                recs.append(dict(p=p_, Tsat=ts_, T=T, sat=int(sat),
                                 v=seg[0], u=seg[1], h=seg[2], s=seg[3]))
            continue
        t = payload(raw, 5)
        if t and len(cur) == 2:                      # half row: one side supercritical
            sat = (t[0] == 'Sat.')
            side = 0 if cur[0][1] is not None else 1  # the subcritical side has a Tsat
            p_, ts_ = cur[side]
            T = ts_ if sat else t[0]
            recs.append(dict(p=p_, Tsat=ts_, T=T, sat=int(sat),
                             v=t[1], u=t[2], h=t[3], s=t[4]))
    return recs

# --------------------------------------------------- A-6 (rotated; read & verified)
# T_C, P_kPa, vi*1e3, vg, ui, uig, ug, hi, hig, hg, si, sig, sg
A6 = [
    [".01",  "0.6113", "1.0908", "206.1",  "-333.40", "2708.7", "2375.3", "-333.40", "2834.8", "2501.4", "-1.221", "10.378", "9.156"],
    ["0",    "0.6108", "1.0908", "206.3",  "-333.43", "2708.8", "2375.3", "-333.43", "2834.8", "2501.3", "-1.221", "10.378", "9.157"],
    ["-2",   "0.5176", "1.0904", "241.7",  "-337.62", "2710.2", "2372.6", "-337.62", "2835.3", "2497.7", "-1.237", "10.456", "9.219"],
    ["-4",   "0.4375", "1.0901", "283.8",  "-341.78", "2711.6", "2369.8", "-341.78", "2835.7", "2494.0", "-1.253", "10.536", "9.283"],
    ["-6",   "0.3689", "1.0898", "334.2",  "-345.91", "2712.9", "2367.0", "-345.91", "2836.2", "2490.3", "-1.268", "10.616", "9.348"],
    ["-8",   "0.3102", "1.0894", "394.4",  "-350.02", "2714.2", "2364.2", "-350.02", "2836.6", "2486.6", "-1.284", "10.698", "9.414"],
    ["-10",  "0.2602", "1.0891", "466.7",  "-354.09", "2715.5", "2361.4", "-354.09", "2837.0", "2482.9", "-1.299", "10.781", "9.481"],
    ["-12",  "0.2176", "1.0888", "553.7",  "-358.14", "2716.8", "2358.7", "-358.14", "2837.3", "2479.2", "-1.315", "10.865", "9.550"],
    ["-14",  "0.1815", "1.0884", "658.8",  "-362.15", "2718.0", "2355.9", "-362.15", "2837.6", "2475.5", "-1.331", "10.950", "9.619"],
    ["-16",  "0.1510", "1.0881", "786.0",  "-366.14", "2719.2", "2353.1", "-366.14", "2837.9", "2471.8", "-1.346", "11.036", "9.690"],
    ["-18",  "0.1252", "1.0878", "940.5",  "-370.10", "2720.4", "2350.3", "-370.10", "2838.2", "2468.1", "-1.362", "11.123", "9.762"],
    ["-20",  "0.1035", "1.0874", "1128.6", "-374.03", "2721.6", "2347.5", "-374.03", "2838.4", "2464.3", "-1.377", "11.212", "9.835"],
    ["-22",  "0.0853", "1.0871", "1358.4", "-377.93", "2722.7", "2344.7", "-377.93", "2838.6", "2460.6", "-1.393", "11.302", "9.909"],
    ["-24",  "0.0701", "1.0868", "1640.1", "-381.80", "2723.7", "2342.0", "-381.80", "2838.7", "2456.9", "-1.408", "11.394", "9.985"],
    ["-26",  "0.0574", "1.0864", "1986.4", "-385.64", "2724.8", "2339.2", "-385.64", "2838.9", "2453.2", "-1.424", "11.486", "10.062"],
    ["-28",  "0.0469", "1.0861", "2413.7", "-389.45", "2725.8", "2336.4", "-389.45", "2839.0", "2449.5", "-1.439", "11.580", "10.141"],
    ["-30",  "0.0381", "1.0858", "2943",   "-393.23", "2726.8", "2333.6", "-393.23", "2839.0", "2445.8", "-1.455", "11.676", "10.221"],
    ["-32",  "0.0309", "1.0854", "3600",   "-396.98", "2727.8", "2330.8", "-396.98", "2839.1", "2442.1", "-1.471", "11.773", "10.303"],
    ["-34",  "0.0250", "1.0851", "4419",   "-400.71", "2728.7", "2328.0", "-400.71", "2839.1", "2438.4", "-1.486", "11.872", "10.386"],
    ["-36",  "0.0201", "1.0848", "5444",   "-404.40", "2729.6", "2325.2", "-404.40", "2839.1", "2434.7", "-1.501", "11.972", "10.470"],
    ["-38",  "0.0161", "1.0844", "6731",   "-408.06", "2730.5", "2322.4", "-408.06", "2839.0", "2430.9", "-1.517", "12.073", "10.556"],
    ["-40",  "0.0129", "1.0841", "8354",   "-411.70", "2731.3", "2319.6", "-411.70", "2838.9", "2427.2", "-1.532", "12.176", "10.644"],
]

# ----------------------------------------------------------------- validation
def validate(A2, A3, A4, A5):
    fv = float
    assert len(A2) == 70, len(A2)
    assert len(A3) == 50, len(A3)
    # monotonic index columns
    t2 = [fv(r[0]) for r in A2]
    assert all(t2[i] < t2[i+1] for i in range(len(t2)-1)), "A-2 T not increasing"
    p3 = [fv(r[0]) for r in A3]
    assert all(p3[i] < p3[i+1] for i in range(len(p3)-1)), "A-3 P not increasing"
    # endpoints: triple point & critical point
    assert A2[0][0] == ".01" and A2[0][8] == "2501.4"      # hg at triple point
    assert A2[-1][0] == "374.14" and A2[-1][1] == "220.9"  # critical T, P
    assert abs(fv(A2[-1][2]) - fv(A2[-1][3])*1e3) < 1e-6   # vf*1e3 == vg*1e3 at critical
    # A-2 anchor at 100 C
    r100 = next(r for r in A2 if r[0] == "100")
    assert r100[1] == "1.014" and r100[7] == "2257.0" and r100[8] == "2676.1" and r100[10] == "7.3549"
    # A-4 / A-5 structure
    pc = 220.9
    subcrit_nosat = sorted({fv(r['p']) for r in A4 if r['sat']} ^
                           {fv(r['p']) for r in A4 if fv(r['p']) < pc})
    assert not subcrit_nosat, f"A-4 subcritical pressures missing Sat row: {subcrit_nosat}"
    assert not any(r['sat'] for r in A4 if fv(r['p']) > pc), "A-4 supercritical row marked Sat"
    assert len({fv(r['p']) for r in A4}) == 24, "A-4 should have 24 pressures"
    assert len({fv(r['p']) for r in A5}) == 8,  "A-5 should have 8 pressures"
    # A-4 anchors (independent of the cross-check below)
    r = next(r for r in A4 if r['p']=="100" and r['T']=="400" and not r['sat'])
    assert (r['v'],r['u'],r['h'],r['s']) == ("0.02641","2832.4","3096.5","6.2120"), r
    r = next(r for r in A4 if r['p']=="10.0" and r['T']=="200" and not r['sat'])
    assert (r['v'],r['u'],r['h'],r['s']) == ("0.2060","2621.9","2827.9","6.6940"), r
    # cross-table: A-4 Sat(vapor) and A-5 Sat(liquid) must match A-3 at equal P
    a3 = {round(fv(r[0]),4): r for r in A3}   # P,T,vf3,vg,uf,ug,hf,hfg,hg,sf,sg
    for r in A4:
        if r['sat'] and round(fv(r['p']),4) in a3:
            a = a3[round(fv(r['p']),4)]
            d = (abs(fv(r['v'])-fv(a[3])) + abs(fv(r['u'])-fv(a[5])) +
                 abs(fv(r['h'])-fv(a[8])) + abs(fv(r['s'])-fv(a[10])))
            assert d < 0.06, f"A-4 Sat vs A-3 mismatch at {r['p']} bar (d={d})"
    for r in A5:
        if r['sat'] and round(fv(r['p']),4) in a3:
            a = a3[round(fv(r['p']),4)]
            d = (abs(fv(r['v'])-fv(a[2])) + abs(fv(r['u'])-fv(a[4])) +
                 abs(fv(r['h'])-fv(a[6])) + abs(fv(r['s'])-fv(a[9])))
            assert d < 0.06, f"A-5 Sat vs A-3 mismatch at {r['p']} bar (d={d})"
    # A-6 internal consistency: uig=ug-ui, hig=hg-hi, sig=sg-si ; and vs A-2 triple point
    assert len(A6) == 22
    for row in A6:
        T,P,vi,vg,ui,uig,ug,hi,hig,hg,si,sig,sg = map(fv, row)
        assert abs(uig-(ug-ui)) < 0.15, f"A-6 uig!=ug-ui at T={row[0]}"
        assert abs(hig-(hg-hi)) < 0.15, f"A-6 hig!=hg-hi at T={row[0]}"
        assert abs(sig-(sg-si)) < 0.02, f"A-6 sig!=sg-si at T={row[0]}"
        assert abs(hi-ui) < 0.05,       f"A-6 hi!=ui at T={row[0]}"      # P*vi negligible
    assert A6[0][6] == "2375.3" and A6[0][9] == "2501.4"  # ug,hg @ .01C == A-2 triple point
    return True

# --------------------------------------------------------------- CSV emitters
def w_csv(name, header, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(rows)
    return path, len(rows)

def emit_csvs(A2, A3, A4, A5):
    written = []
    hdr_sat = ["{0}", "{1}", "vf_x1e3_m3kg", "vg_m3kg",
               "uf_kJkg", "ug_kJkg", "hf_kJkg", "hfg_kJkg", "hg_kJkg",
               "sf_kJkgK", "sg_kJkgK"]
    h2 = ["T_C","P_bar"] + hdr_sat[2:]
    written.append(w_csv("A2_sat_water_temperature.csv", h2,
                         sorted(A2, key=lambda r: float(r[0]))))
    h3 = ["P_bar","T_C"] + hdr_sat[2:]
    written.append(w_csv("A3_sat_water_pressure.csv", h3,
                         sorted(A3, key=lambda r: float(r[0]))))
    h4 = ["P_bar","Tsat_C","T_C","v_m3kg","u_kJkg","h_kJkg","s_kJkgK","sat"]
    a4 = sorted(A4, key=lambda r: (float(r['p']), float(r['T'])))
    written.append(w_csv("A4_superheated_water.csv", h4,
        [[r['p'], r['Tsat'] or "", r['T'], r['v'], r['u'], r['h'], r['s'], r['sat']] for r in a4]))
    h5 = ["P_bar","Tsat_C","T_C","v_x1e3_m3kg","u_kJkg","h_kJkg","s_kJkgK","sat"]
    a5 = sorted(A5, key=lambda r: (float(r['p']), float(r['T'])))
    written.append(w_csv("A5_compressed_liquid_water.csv", h5,
        [[r['p'], r['Tsat'] or "", r['T'], r['v'], r['u'], r['h'], r['s'], r['sat']] for r in a5]))
    h6 = ["T_C","P_kPa","vi_x1e3_m3kg","vg_m3kg","ui_kJkg","uig_kJkg","ug_kJkg",
          "hi_kJkg","hig_kJkg","hg_kJkg","si_kJkgK","sig_kJkgK","sg_kJkgK"]
    written.append(w_csv("A6_sat_water_solid_vapor.csv", h6, A6))
    return written, a4, a5

# --------------------------------------------------------------- markdown render
def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)

def emit_markdown(A2, A3, a4, a5):
    L = []
    L.append("# SI Steam Tables (rendered)\n")
    L.append("Water (H₂O) property tables A-2 … A-6 from Moran *et al.*, "
             "*Fundamentals of Engineering Thermodynamics*, 8th ed. "
             "Canonical data live in the sibling `.csv` files; see `README.md` for units, "
             "column legends, and provenance.\n")
    L.append("> `vf`, `vi` columns are ×10³ (i.e. tabulated value /1000 = m³/kg). "
             "`hfg`/`uig`/etc. are evaporation/sublimation differences.\n")

    L.append("\n## Table A-2 — Saturated water, temperature index\n")
    L.append(md_table(["T °C","P bar","vf×10³","vg","uf","ug","hf","hfg","hg","sf","sg"],
                      sorted(A2, key=lambda r: float(r[0]))))
    L.append("\n## Table A-3 — Saturated water, pressure index\n")
    L.append(md_table(["P bar","T °C","vf×10³","vg","uf","ug","hf","hfg","hg","sf","sg"],
                      sorted(A3, key=lambda r: float(r[0]))))

    def by_pressure(recs, vlabel):
        out = []
        from itertools import groupby
        for p, grp in groupby(recs, key=lambda r: r['p']):
            grp = list(grp)
            ts = next((g['Tsat'] for g in grp if g['Tsat']), None)
            head = f"\n### p = {p} bar" + (f"  (Tsat = {ts} °C)" if ts else "  (supercritical)")
            out.append(head)
            rows = [["Sat." if g['sat'] else g['T'], g['v'], g['u'], g['h'], g['s']] for g in grp]
            out.append(md_table(["T °C", vlabel, "u kJ/kg", "h kJ/kg", "s kJ/kg·K"], rows))
        return "\n".join(out)

    L.append("\n## Table A-4 — Superheated water vapor\n")
    L.append(by_pressure(a4, "v m³/kg"))
    L.append("\n## Table A-5 — Compressed (subcooled) liquid water\n")
    L.append(by_pressure(a5, "v×10³ m³/kg"))

    L.append("\n## Table A-6 — Saturated water (solid–vapor), temperature index\n")
    L.append("Sublimation region. `i` = saturated solid (ice), `ig` = sublimation, "
             "`g` = saturated vapor. Internal energy / enthalpy / entropy of ice are negative "
             "(reference: saturated liquid at the triple point).\n")
    L.append(md_table(["T °C","P kPa","vi×10³","vg","ui","uig","ug",
                       "hi","hig","hg","si","sig","sg"], A6))
    path = os.path.join(OUT, "steam_tables.md")
    open(path, "w").write("\n".join(L) + "\n")
    return path

# ------------------------------------------------------------------------- main
def main():
    doc = _load_doc()
    A2 = clean12(doc, [944, 945])
    A3 = clean12(doc, [946, 947])
    A4 = blocks(doc, [948, 949, 950, 951])
    A5 = blocks(doc, [952])
    validate(A2, A3, A4, A5)
    written, a4, a5 = emit_csvs(A2, A3, A4, A5)
    mdpath = emit_markdown(A2, A3, a4, a5)
    print("VALIDATION PASSED")
    for path, n in written:
        print(f"  wrote {os.path.basename(path):40s} {n:4d} rows")
    print(f"  wrote {os.path.basename(mdpath)}")

if __name__ == "__main__":
    main()
