#!/usr/bin/env python3
"""
Teaching-modules webpage generator -- view the physics modules with *real* math.

Generates a self-contained page, modules/teaching_modules.html, with a sidebar of
every module; pick one to see its scope, ALL its equations rendered by KaTeX
exactly as written in notes.md (matrices, \\boxed, \\mathbf, multi-line --
everything), and the worked example problems. Then opens it in your browser.
(Formerly ma_browser_web.py writing ma_browser.html; renamed 2026-08-12.)

Why a web page rather than the Tkinter app (ma_browser.py): KaTeX is a real TeX
renderer, so every equation renders (the Tkinter version uses matplotlib mathtext,
which can't do matrices / multi-line and leaves some LaTeX as raw text), and the
browser's fonts render every Unicode symbol (no missing-glyph boxes for em-dashes
etc.). This mirrors the KaTeX setup already used in
Kinetic_Modeling/KrF_and_LoKI/docs/about/index.html.

Deep links, both ways with the personal site's Teaching Network
(../website/teaching.html): teaching_modules.html#MA-02 (or #m-MA-02) opens that
module and #MA the trunk's first module, picking a module keeps the URL in step,
and every module that is a node of topic_network.txt carries "open in the
Teaching Network" (teaching.html#<id>) under its title. The network side is
baked by website/dev/build_network.py; website/dev/check_links.py audits both.

Run:  python3 modules/generate_webpage.py
      python3 modules/generate_webpage.py --no-open      # just (re)generate the HTML
      python3 modules/generate_webpage.py --serve [PORT] # serve on localhost & keep
                                                         # running (best on WSL: no
                                                         # explorer.exe / xdg-open needed)
"""

import html
import json
import os
import re
import subprocess
import sys
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))      # the modules/ folder
OUT = os.path.join(HERE, "teaching_modules.html")
KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"
NETWORK_TXT = os.path.join(HERE, "topic_network.txt")   # the Teaching Network's source
TEACHING_PAGE = "../website/teaching.html"              # the network page on the site

TRUNK_NAMES = {
    "MA": "Mathematics", "CM": "Classical Mechanics", "EM": "Electricity & Magnetism",
    "QM": "Quantum Mechanics", "RE": "Relativity", "SM": "Statistical Mechanics",
    "QO": "Quantum Optics", "PK": "Plasma & Kinetics", "QF": "Quantum Field Theory",
    "ST": "Probability Theory", "TD": "Thermodynamics",
    "MACRO_EM": "Macroscopic Electrodynamics",
}

# Trunk dirs are 2-3 uppercase letters (optional trailing x), or an underscored
# uppercase name like MACRO_EM (the Wilcox problems trunk).
TRUNK_DIR_RE = r"[A-Z]{2,3}x?|[A-Z]{2,8}_[A-Z]{2,8}"
MODULE_DIR_RE = r"([A-Z]{2,3}|[A-Z]{2,8}_[A-Z]{2,8})-(\d+)_(.+)"

# Thermodynamics lives under Thermo/Topic_<n>/ with a different layout than the
# XX-NN_ trunks: concept subtopics (NN.M_name) are full modules (README/notes/
# problems, rendered like any other), while the per-topic EQ/EP/HP folders are
# single markdown docs (equation tables, worked examples) rendered via md_doc.
THERMO_TRUNK = "TD"
AUX_FILES = {"EQ": "equations.md", "EP": "examples.md", "HP": "problems.md"}
AUX_LABEL = {"EQ": "List of equations", "EP": "Worked examples", "HP": "Homework problems"}
AUX_ORDER = {"EQ": 0.90, "EP": 0.91, "HP": 0.92}   # sort after a topic's numeric subtopics


# --------------------------------------------------------------------------
# Reading the module files
# --------------------------------------------------------------------------

def _read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def discover_modules(root=HERE):
    mods = []
    for trunk in sorted(os.listdir(root)):
        tdir = os.path.join(root, trunk)
        if not os.path.isdir(tdir) or not re.fullmatch(TRUNK_DIR_RE, trunk):
            continue
        for name in sorted(os.listdir(tdir)):
            mdir = os.path.join(tdir, name)
            m = re.fullmatch(MODULE_DIR_RE, name)
            if os.path.isdir(mdir) and m:
                title = _title_from_readme(os.path.join(mdir, "README.md")) or \
                    m.group(3).replace("_", " ").title()
                mods.append({"id": f"{m.group(1)}-{m.group(2)}", "trunk": m.group(1),
                             "num": int(m.group(2)), "title": title, "dir": mdir})
    mods.sort(key=lambda d: (d["trunk"], d["num"]))
    return mods


def _title_from_readme(path):
    for line in _read(path).splitlines():
        if line.startswith("# "):
            head = line[2:].strip()
            for dash in ("—", " - ", "–"):
                if dash in head:
                    return head.split(dash, 1)[1].strip()
            return head
    return ""


def network_ids(path=NETWORK_TXT):
    """Module ids that are nodes of the Teaching Network: the 'XX-nn  title'
    lines of topic_network.txt (the same lines website/dev/build_network.py
    bakes). Modules outside it (NE, MACRO_EM, Thermo today) get no back-link."""
    return set(re.findall(r"^\s{2}([A-Z]{2}-\d{2})\s", _read(path), re.MULTILINE))


NET_IDS = network_ids()


def thermo_topic_names(root=HERE):
    """Map topic number -> human group name, parsed from Thermo/list.txt
    (lines like '1. FOUNDATIONS & SYSTEM CONCEPTS')."""
    txt = _read(os.path.join(root, "Thermo", "list.txt"))
    names = {}
    for m in re.finditer(r"^(\d+)\.\s+([A-Z][^\n]+?)\s*$", txt, re.MULTILINE):
        names[int(m.group(1))] = m.group(2).strip().title()
    return names


def discover_thermo(root=HERE):
    """Discover Thermodynamics modules under Thermo/Topic_<n>/.

    Two kinds, both grouped under the synthetic 'TD' trunk:
      * concept subtopics  NN.M_name      -> full modules (built like any other)
      * the EQ/EP/HP folders N.XX_name    -> single markdown docs (kind = EQ/EP/HP)
    """
    troot = os.path.join(root, "Thermo")
    if not os.path.isdir(troot):
        return []
    topic_names = thermo_topic_names(root)
    mods = []
    for tname in sorted(os.listdir(troot)):
        tm = re.fullmatch(r"Topic_(\d+)", tname)
        tdir = os.path.join(troot, tname)
        if not (tm and os.path.isdir(tdir)):
            continue
        tnum = int(tm.group(1))
        for name in sorted(os.listdir(tdir)):
            mdir = os.path.join(tdir, name)
            if not os.path.isdir(mdir):
                continue
            sub = re.fullmatch(r"(\d+)\.(\d+)_(.+)", name)
            aux = re.fullmatch(r"(\d+)\.(EQ|EP|HP)_(.+)", name)
            if sub:
                snum = int(sub.group(2))
                title = _title_from_readme(os.path.join(mdir, "README.md")) or \
                    sub.group(3).replace("_", " ").title()
                mods.append({"id": f"TD-{tnum}.{snum}", "trunk": THERMO_TRUNK,
                             "num": tnum + snum / 100.0, "title": title, "dir": mdir,
                             "kind": "module", "topic": tnum,
                             "topic_name": topic_names.get(tnum, "")})
            elif aux:
                kind = aux.group(2)
                mods.append({"id": f"TD-{tnum}.{kind}", "trunk": THERMO_TRUNK,
                             "num": tnum + AUX_ORDER[kind], "title": AUX_LABEL[kind],
                             "dir": mdir, "kind": kind, "topic": tnum,
                             "topic_name": topic_names.get(tnum, "")})
    return mods


def extract_section(md, header):
    m = re.search(r"^##\s+" + re.escape(header) + r"\s*\n(.*?)(?=^##\s|\Z)",
                  md, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else ""


def extract_equations(notes_md):
    """Raw $$...$$ display blocks, exactly as written (KaTeX renders them)."""
    eqs = re.findall(r"\$\$(.+?)\$\$", notes_md, re.DOTALL)
    return [e.strip() for e in eqs if e.strip()]


def extract_problems(problems_md):
    out = []
    for blk in re.split(r"^### ", problems_md, flags=re.MULTILINE)[1:]:
        head, _, rest = blk.partition("\n")
        m = re.match(r"(P\d+)\.\s+(.*?)\s*(?:\*\((.*?)\)\*)?\s*$", head)
        if m:
            stmt, _sep, soln = rest.partition("**Solution.**")
            out.append({"tag": m.group(1), "title": m.group(2).strip(),
                        "cite": (m.group(3) or "").strip(),
                        "body": stmt.strip(), "solution": soln.strip()})
    return out


# --------------------------------------------------------------------------
# Markdown-ish -> HTML (inline code, keep paragraphs; math left for KaTeX)
# --------------------------------------------------------------------------

def md_inline(text):
    s = html.escape(text)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def md_block(text):
    """Paragraphs separated by blank lines; single newlines become spaces."""
    paras = re.split(r"\n\s*\n", text.strip())
    return "\n".join(f"<p>{md_inline(' '.join(p.split()))}</p>" for p in paras if p.strip())


def md_mixed(text):
    """Like md_block but each $$...$$ display block becomes its own centered
    equation (a proper KaTeX display), with prose between them as paragraphs."""
    out, idx = [], 0
    for m in re.finditer(r"\$\$(.+?)\$\$", text, re.DOTALL):
        pre = text[idx:m.start()].strip()
        if pre:
            out.append(md_block(pre))
        out.append(f'<div class="eq">\\[{html.escape(m.group(1).strip())}\\]</div>')
        idx = m.end()
    tail = text[idx:].strip()
    if tail:
        out.append(md_block(tail))
    return "\n".join(out)


# --------------------------------------------------------------------------
# Full markdown -> HTML (for the Thermo EQ/EP/HP docs: headings, pipe tables,
# lists, blockquotes, fenced code, paragraphs). Math ($, $$) is left untouched
# so KaTeX auto-render handles it; html.escape round-trips through the DOM text
# node back to the literal the renderer reads.
# --------------------------------------------------------------------------

def _md_cells(row):
    r = row.strip()
    if r.startswith("|"):
        r = r[1:]
    if r.endswith("|"):
        r = r[:-1]
    return [c.strip() for c in r.split("|")]


def _md_table(lines, i):
    head = _md_cells(lines[i])
    i += 2                                          # skip header + separator row
    body = []
    while i < len(lines) and "|" in lines[i] and lines[i].strip():
        body.append(_md_cells(lines[i]))
        i += 1
    th = "".join(f"<th>{md_inline(c)}</th>" for c in head)
    rows = "".join("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>"
                   for r in body)
    return f"<table class='md'><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>", i


def _md_list(lines, i):
    ordered = bool(re.match(r"\d+[.)]\s+", lines[i].strip()))
    items = []
    while i < len(lines):
        raw, s = lines[i], lines[i].strip()
        if not s:
            break
        m = re.match(r"(?:[-*+]|\d+[.)])\s+(.*)", s)
        if m:
            items.append(m.group(1))
        elif raw[:1].isspace() and items:
            items[-1] += " " + s                    # indented wrapped continuation
        else:
            break
        i += 1
    tag = "ol" if ordered else "ul"
    return f"<{tag}>" + "".join(f"<li>{md_inline(it)}</li>" for it in items) + f"</{tag}>", i


def _md_blocks(text):
    lines = text.split("\n")
    out, para, i = [], [], 0

    def flush():
        if para:
            joined = " ".join(" ".join(para).split())
            if joined:
                out.append(f"<p>{md_inline(joined)}</p>")
            para.clear()

    while i < len(lines):
        line, s = lines[i], lines[i].strip()
        if not s:
            flush(); i += 1; continue
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            flush(); out.append("<hr>"); i += 1; continue
        hm = re.match(r"(#{1,6})\s+(.*)", s)
        if hm:
            flush()
            lvl = len(hm.group(1))
            tag = {1: "h3", 2: "h3", 3: "h4", 4: "h5", 5: "h6", 6: "h6"}[lvl]
            cls = ' class="sec"' if lvl <= 2 else ""
            out.append(f"<{tag}{cls}>{md_inline(hm.group(2).strip())}</{tag}>")
            i += 1; continue
        # pipe table: a header row followed by a |---|---| separator
        if "|" in line and i + 1 < len(lines) and "-" in lines[i + 1] \
                and re.fullmatch(r"\s*\|?[\s:|-]+\|?\s*", lines[i + 1]):
            flush()
            tbl, i = _md_table(lines, i)
            out.append(tbl); continue
        if s.startswith(">"):
            flush()
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip()[1:].strip()); i += 1
            out.append(f"<blockquote>{md_inline(' '.join(q))}</blockquote>"); continue
        if re.match(r"[-*+]\s+", s) or re.match(r"\d+[.)]\s+", s):
            flush()
            lst, i = _md_list(lines, i)
            out.append(lst); continue
        para.append(s); i += 1
    flush()
    return "\n".join(out)


def md_doc(text):
    """Render a whole markdown document, protecting fenced code blocks."""
    out = []
    for j, seg in enumerate(re.split(r"(```.*?```)", text, flags=re.DOTALL)):
        if j % 2 == 1:                              # fenced code block
            code = seg[3:-3]
            if "\n" in code:
                code = re.sub(r"\A[^\n]*\n", "", code)   # drop the ```lang line
            out.append(f"<pre class='codeblk'><code>{html.escape(code.rstrip())}</code></pre>")
        elif seg.strip():
            out.append(_md_blocks(seg))
    return "\n".join(p for p in out if p)


# --------------------------------------------------------------------------
# HTML generation
# --------------------------------------------------------------------------

CSS = """
:root{--bg:#070b18;--panel:#fff;--ink:#1b1b2e;--accent:#3b3b6d;--muted:#6b6b85;
      --rule:#e3e3ee;--chip:#eef1fb;--check:#eef3ff;}
*{box-sizing:border-box}
body{margin:0;font:15px/1.6 -apple-system,Segoe UI,Roboto,"DejaVu Sans",sans-serif;
     color:var(--ink);background:var(--bg);display:flex;height:100vh;overflow:hidden}
#side{width:290px;flex:0 0 290px;background:var(--panel);border-right:1px solid var(--rule);
      display:flex;flex-direction:column;height:100%}
#side h1{font-size:16px;margin:0;padding:16px 18px;background:var(--accent);color:#fff}
#side h1 small{display:block;font-weight:400;color:#c9c9ee;font-size:12px;margin-top:2px}
#filter{margin:10px;padding:8px 10px;border:1px solid var(--rule);border-radius:8px;font:inherit}
#list{overflow:auto;padding:0 8px 16px;flex:1}
.trunk{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);
       margin:14px 10px 4px;font-weight:700}
.subtrunk{font-size:10.5px;letter-spacing:.03em;color:var(--muted);margin:8px 10px 2px 14px;
       font-weight:600;opacity:.85}
.item{display:block;width:100%;text-align:left;border:0;background:none;font:inherit;color:var(--ink);
      padding:7px 10px;border-radius:8px;cursor:pointer}
.item:hover{background:var(--chip)}
.item.active{background:var(--accent);color:#fff}
#main{flex:1;overflow:auto;padding:34px 46px 80px}
#main h2{font-size:24px;margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 18px;font-size:13px}
.sub .netlink{color:var(--accent);text-decoration:none;border-bottom:1px solid #c5c5de}
.sub .netlink:hover{color:var(--ink);border-bottom-color:var(--accent)}
.scope{color:#33334d;background:var(--panel);border:1px solid var(--rule);border-radius:10px;
       padding:14px 18px;margin:0 0 24px}
h3.sec{color:var(--accent);font-size:14px;letter-spacing:.04em;text-transform:uppercase;
       border-bottom:1px solid var(--rule);padding-bottom:6px;margin:30px 0 14px}
.eq{margin:12px 0;overflow-x:auto;overflow-y:hidden}
.prob{background:var(--panel);border:1px solid var(--rule);border-left:4px solid var(--accent);
      border-radius:8px;padding:12px 16px;margin:12px 0}
.prob .ptag{font-weight:700;color:var(--accent)}
.prob .cite{color:var(--muted);font-size:12.5px;margin-left:6px}
.prob p{margin:6px 0}
.soln{margin:10px 0 2px;padding:10px 14px;background:#f3f8f3;border:1px solid #d6e6d6;
      border-left:4px solid #4a8a52;border-radius:8px}
.soln .slabel{display:inline-block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;
      font-weight:700;color:#3a7a42;margin-bottom:4px}
.soln .eq{margin:8px 0}
.soln p{margin:5px 0}
code{background:#eef0f6;border-radius:5px;padding:1px 5px;font:13px/1.5 "DejaVu Sans Mono",monospace}
.module{display:none;background:var(--panel);border:1px solid var(--rule);
        border-radius:12px;padding:26px 30px 34px}
.module.on{display:block}
.foot{color:var(--muted);font-size:12.5px;margin-top:28px;border-top:1px solid var(--rule);padding-top:10px}
.katex{font-size:1.05em}
.katex-display{margin:.5em 0;text-align:left}
.fig{margin:16px 0;padding:12px 12px 6px;background:#fcfcff;border:1px solid var(--rule);border-radius:10px}
.fig svg{max-width:100%;height:auto;display:block;margin:0 auto}
.fig figcaption{color:var(--muted);font-size:13px;line-height:1.5;margin:8px 6px 4px;text-align:center}
.doc h4{color:var(--accent);font-size:15px;margin:22px 0 8px}
.doc h5,.doc h6{color:#33334d;font-size:13.5px;margin:16px 0 6px}
.doc p{margin:10px 0}
.doc ul,.doc ol{margin:10px 0;padding-left:22px}
.doc li{margin:3px 0}
.doc hr{border:0;border-top:1px solid var(--rule);margin:22px 0}
.doc blockquote{margin:12px 0;padding:8px 14px;background:var(--check);border-left:4px solid var(--accent);
       border-radius:6px;color:#33334d}
table.md{border-collapse:collapse;margin:14px 0;font-size:13.5px;display:block;overflow-x:auto;max-width:100%}
table.md th,table.md td{border:1px solid var(--rule);padding:5px 9px;text-align:left;vertical-align:top}
table.md th{background:var(--chip);font-weight:700;white-space:nowrap}
table.md tr:nth-child(even) td{background:#fafaff}
pre.codeblk{background:#f4f4fb;border:1px solid var(--rule);border-radius:8px;padding:10px 12px;
       overflow-x:auto;font:12.5px/1.5 "DejaVu Sans Mono",monospace}
pre.codeblk code{background:none;padding:0}
"""

# The personal site's header bar — same injected block every sim in
# projects/simulations/ carries (see simulations CHANGELOG 2026-08-12 (d));
# palette matches projects/website/style.css. Modules is marked current:
# this page IS the Modules tab (self-link; the rest point at ../website/).
SITE_NAV_CSS = """
/* injected site header — palette & tabs match ../website/style.css */
body{padding-top:36px;}
html{scroll-padding-top:36px;}   /* any scroll-to-target lands below the fixed bar */
header.site-nav{position:fixed; top:0; left:0; right:0; height:36px; z-index:400;
  display:flex; justify-content:center; align-items:center; padding:0 1rem;
  background:#070b18; border:0;}
.site-nav nav{margin:0; display:flex; flex-wrap:wrap; justify-content:center;
  gap:0 1.5rem; letter-spacing:.16em; text-transform:uppercase; font-size:.78rem;
  font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;}
.site-nav a{color:#8fb8d4; text-decoration:none; padding:.2rem .1rem;
  border-bottom:1px solid transparent; transition:color 120ms ease, border-color 120ms ease;}
.site-nav a:hover{color:#7deeff;}
.site-nav a[aria-current="page"]{color:#1bbeeb; border-bottom-color:#1bbeeb;}
"""

SITE_NAV_HTML = """<header class="site-nav">
  <nav aria-label="Site">
    <a href="../website/index.html">Home</a>
    <a href="../website/about.html">About</a>
    <a href="../website/teaching.html">Teaching</a>
    <a href="teaching_modules.html" aria-current="page">Modules</a>
    <a href="../website/simulations.html">Simulations</a>
    <a href="../website/research.html">Research</a>
    <a href="../website/cv.html">CV</a>
  </nav>
</header>"""

JS = """
const items=[...document.querySelectorAll('.item')];
const KOPTS={delimiters:[
  {left:'$$',right:'$$',display:true},{left:'\\\\[',right:'\\\\]',display:true},
  {left:'$',right:'$',display:false},{left:'\\\\(',right:'\\\\)',display:false}],
  throwOnError:false,errorColor:'#c0392b'};
// Lazy KaTeX: render a module's math the first time it is shown, then cache.
function renderModule(m){
  if(!m||m.dataset.rendered||!window.renderMathInElement)return;
  renderMathInElement(m,KOPTS);m.dataset.rendered='1';
}
function show(id,fromHash){
  document.querySelectorAll('.module').forEach(m=>m.classList.toggle('on',m.id===id));
  items.forEach(b=>b.classList.toggle('active',b.dataset.t===id));
  renderModule(document.getElementById(id));
  document.getElementById('main').scrollTop=0;
  revealItem(items.find(b=>b.dataset.t===id),fromHash);
  if(!fromHash)setHash(id.replace(/^m-/,''));
}
items.forEach(b=>b.onclick=()=>show(b.dataset.t));
// Scroll the sidebar list itself, never scrollIntoView: that also scrolls every
// ancestor, and any nudge of the page under the fixed site header clips the
// top of both columns. Arriving by deep link, start the trunk (or Thermo
// topic) from its heading when the item fits below it, else put the item a
// third of the way down; on a click, only nudge an item that is out of view.
function revealItem(it,fromHash){
  const list=document.getElementById('list');
  if(!it||!list)return;
  const lr=list.getBoundingClientRect(),ir=it.getBoundingClientRect();
  const top=ir.top-lr.top+list.scrollTop,h=ir.height,view=list.clientHeight;
  if(!fromHash){
    if(top<list.scrollTop)list.scrollTop=Math.max(0,top-8);
    else if(top+h>list.scrollTop+view)list.scrollTop=top+h-view+8;
    return;
  }
  let hd=it.previousElementSibling;
  while(hd&&!hd.classList.contains('trunk')&&!hd.classList.contains('subtrunk'))hd=hd.previousElementSibling;
  const htop=hd?hd.getBoundingClientRect().top-lr.top+list.scrollTop:top;
  list.scrollTop=(top+h-htop<=view-8)?Math.max(0,htop-6):Math.max(0,top-view/3);
}
// The reading column and the page start at the top on arrival: nothing here
// scrolls them, and a browser's own fragment handling must not either.
function pinTop(){
  const m=document.getElementById('main');if(m)m.scrollTop=0;
  if(document.documentElement)document.documentElement.scrollTop=0;
  if(document.body)document.body.scrollTop=0;
  if(typeof window.scrollTo==='function')window.scrollTo(0,0);
}
// Deep links, both ways with the Teaching Network (../website/teaching.html):
// #MA-02 (or #m-MA-02) opens that module and #MA the trunk's first module, so
// the network's "open module" links land on the right page; picking a module
// here keeps the URL in step (replaceState: Back still leaves the page), and
// each module's subtitle links to its orb, teaching.html#<id>.
function moduleFromHash(){
  let h=location.hash.replace(/^#/,'');
  try{h=decodeURIComponent(h);}catch(e){}
  h=h.trim();
  if(!/^m-/.test(h))h='m-'+h;
  if(!/^m-[A-Z][A-Za-z_]*(-[\\w.]+)?$/.test(h))return null;
  const el=document.getElementById(h);
  if(el&&el.classList.contains('module'))return h;
  const first=document.querySelector('.module[id^="'+h+'-"]');
  return first?first.id:null;
}
function setHash(bare){
  const want='#'+encodeURIComponent(bare);
  if(location.hash===want)return;
  try{history.replaceState(null,'',want);}catch(e){}
}
function routeHash(){
  const id=moduleFromHash();
  if(!id)return false;
  const f=document.getElementById('filter');
  if(f&&f.value){f.value='';f.dispatchEvent(new Event('input'));}   // the item must be visible
  show(id,true);pinTop();return true;
}
window.addEventListener('hashchange',routeHash);
document.getElementById('filter').addEventListener('input',e=>{
  const q=e.target.value.toLowerCase();
  items.forEach(b=>b.style.display=b.textContent.toLowerCase().includes(q)?'block':'none');
  // hide a topic (sub)header when nothing under it (up to the next header) is visible
  document.querySelectorAll('.subtrunk').forEach(h=>{
    let n=h.nextElementSibling,any=false;
    while(n&&!n.classList.contains('trunk')&&!n.classList.contains('subtrunk')){
      if(n.classList.contains('item')&&n.style.display!=='none')any=true;n=n.nextElementSibling;}
    h.style.display=any?'block':'none';
  });
  // hide a trunk header when its whole group (items + any topic headers) is empty
  document.querySelectorAll('.trunk').forEach(h=>{
    let n=h.nextElementSibling,any=false;
    while(n&&!n.classList.contains('trunk')){
      if(n.classList.contains('item')&&n.style.display!=='none')any=true;n=n.nextElementSibling;}
    h.style.display=any?'block':'none';
  });
});
// Only the initially-open module renders at load; the rest render on first view.
function render(){
  const routed=routeHash();
  renderModule(document.querySelector('.module.on'));
  if(routed){                                  // and again after the browser's own load-time scrolling
    if(typeof window.requestAnimationFrame==='function')window.requestAnimationFrame(pinTop);
    window.addEventListener('load',pinTop,{once:true});
  }
}
window.addEventListener('DOMContentLoaded',render);
"""


def build_html(mods):
    # sidebar grouped by trunk (Thermo additionally sub-grouped by topic)
    side, body = [], []
    last_trunk = last_topic = None
    for m in mods:
        if m["trunk"] != last_trunk:
            tn = TRUNK_NAMES.get(m["trunk"], m["trunk"])
            side.append(f'<div class="trunk">{m["trunk"]} &middot; {html.escape(tn)}</div>')
            last_trunk, last_topic = m["trunk"], None
        if m.get("topic") is not None and m.get("topic") != last_topic:
            tlab = f'Topic {m["topic"]}'
            if m.get("topic_name"):
                tlab += f' &middot; {html.escape(m["topic_name"])}'
            side.append(f'<div class="subtrunk">{tlab}</div>')
            last_topic = m["topic"]
        mid = "m-" + m["id"]
        side.append(f'<button class="item" data-t="{mid}">{m["id"]} &mdash; {html.escape(m["title"])}</button>')
        body.append(build_module(m, mid))
    first = "m-" + next((m["id"] for m in mods if m["trunk"] == "MA"), mods[0]["id"])
    body_html = "\n".join(body).replace(f'id="{first}" class="module"',
                                        f'id="{first}" class="module on"', 1)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Physics Module Browser</title>
<link rel="stylesheet" href="{KATEX}/katex.min.css" crossorigin="anonymous">
<style>{CSS}</style>
<style id="site-nav-css">{SITE_NAV_CSS}</style></head><body>
{SITE_NAV_HTML}
<nav id="side">
  <h1>Physics Modules<small>{len(mods)} modules &middot; KaTeX</small></h1>
  <input id="filter" placeholder="filter (e.g. MA-1, tensor)" autocomplete="off">
  <div id="list">{''.join(side)}</div>
</nav>
<main id="main">{body_html}</main>
<script defer src="{KATEX}/katex.min.js" crossorigin="anonymous"></script>
<script defer src="{KATEX}/contrib/auto-render.min.js" crossorigin="anonymous"></script>
<script defer>{JS}</script>
</body></html>"""


def _namespace_svg(svg, prefix):
    """Prefix every id and #ref in one inlined SVG so many figures coexist in one
    HTML document without id collisions (matplotlib reuses glyph/clip ids)."""
    ids = sorted(set(re.findall(r'id="([^"]+)"', svg)), key=len, reverse=True)
    for i in ids:
        svg = svg.replace(f'id="{i}"', f'id="{prefix}{i}"')
        svg = svg.replace(f'#{i}"', f'#{prefix}{i}"')
        svg = svg.replace(f'url(#{i})', f'url(#{prefix}{i})')
    return svg


def discover_figures(m):
    """Inlined SVGs + captions for <dir>/figures/*.svg (captions.json optional)."""
    fdir = os.path.join(m["dir"], "figures")
    if not os.path.isdir(fdir):
        return []
    caps = {}
    if os.path.isfile(os.path.join(fdir, "captions.json")):
        try:
            caps = json.loads(_read(os.path.join(fdir, "captions.json")))
        except Exception:
            caps = {}
    out = []
    for idx, fn in enumerate(sorted(f for f in os.listdir(fdir) if f.endswith(".svg"))):
        raw = _read(os.path.join(fdir, fn))
        k = raw.find("<svg")
        if k < 0:
            continue
        svg = re.sub(r"<metadata>.*?</metadata>", "", raw[k:], flags=re.DOTALL)
        svg = _namespace_svg(svg, f"{m['id'].replace('-', '')}_{idx}_")
        out.append({"svg": svg, "cap": caps.get(fn, "")})
    return out


def _sub_line(m):
    """The little grey subtitle under a module's H2 (trunk + path; Thermo adds
    its topic group)."""
    trunk = TRUNK_NAMES.get(m["trunk"], m["trunk"])
    rel = html.escape(os.path.relpath(m["dir"], HERE))
    if m.get("topic") is not None:
        tn = f': {html.escape(m["topic_name"])}' if m.get("topic_name") else ""
        return f'{trunk} &middot; Topic {m["topic"]}{tn} &middot; <code>{rel}</code>' + _net_link(m)
    return f'{trunk} trunk &middot; <code>{rel}</code>' + _net_link(m)


def _net_link(m):
    """Subtitle tail: the module's orb in the Teaching Network, for modules that
    are nodes of topic_network.txt (NE, MACRO_EM and Thermo have none yet)."""
    if m["id"] not in NET_IDS:
        return ""
    return (f' &middot; <a class="netlink" href="{TEACHING_PAGE}#{m["id"]}"'
            f' title="travel to {m["id"]} in the Teaching Network">'
            f'open in the Teaching Network</a>')


def build_thermo_aux(m, mid):
    """Render a Thermo EQ/EP/HP folder: one markdown doc (equation tables, worked
    examples, homework) rendered in full, plus a run-the-code footer."""
    md = _read(os.path.join(m["dir"], AUX_FILES[m["kind"]]))
    md = re.sub(r"\A#\s+[^\n]*\n", "", md)          # drop the leading title (shown as H2)
    parts = [f'<section id="{mid}" class="module">',
             f'<h2>{m["id"]} &mdash; {html.escape(m["title"])}</h2>',
             f'<p class="sub">{_sub_line(m)}</p>',
             f'<div class="doc">{md_doc(md)}</div>']
    demo = _demo_rel(m)
    if demo:
        parts.append(f'<p class="foot">Run / verify the code: '
                     f'<code>cd {html.escape(os.path.dirname(demo))} &amp;&amp; '
                     f'python3 {html.escape(os.path.basename(demo))}</code></p>')
    parts.append("</section>")
    return "\n".join(parts)


def build_module(m, mid):
    if m.get("kind") in AUX_FILES:
        return build_thermo_aux(m, mid)
    readme = _read(os.path.join(m["dir"], "README.md"))
    notes = _read(os.path.join(m["dir"], "notes.md"))
    problems = _read(os.path.join(m["dir"], "problems", "problems.md"))

    parts = [f'<section id="{mid}" class="module">',
             f'<h2>{m["id"]} &mdash; {html.escape(m["title"])}</h2>',
             f'<p class="sub">{_sub_line(m)}</p>']

    scope = extract_section(readme, "Scope")
    if scope:
        parts.append(f'<div class="scope">{md_block(scope)}</div>')

    eqs = extract_equations(notes)
    if eqs:
        parts.append('<h3 class="sec">Key equations</h3>')
        for e in eqs:
            parts.append(f'<div class="eq">\\[{html.escape(e)}\\]</div>')

    figs = discover_figures(m)
    if figs:
        parts.append('<h3 class="sec">Figures</h3>')
        for fig in figs:
            cap = f'<figcaption>{md_inline(fig["cap"])}</figcaption>' if fig["cap"] else ""
            parts.append(f'<figure class="fig">{fig["svg"]}{cap}</figure>')

    probs = extract_problems(problems)
    if probs:
        parts.append('<h3 class="sec">Example problems</h3>')
        for p in probs:
            cite = f'<span class="cite">{md_inline(p["cite"])}</span>' if p["cite"] else ""
            soln = (f'<div class="soln"><span class="slabel">Solution</span>'
                    f'{md_mixed(p["solution"])}</div>') if p.get("solution") else ""
            parts.append(f'<div class="prob"><span class="ptag">{p["tag"]}. '
                         f'{md_inline(p["title"])}</span>{cite}{md_block(p["body"])}{soln}</div>')

    demo = _demo_rel(m)
    if demo:
        parts.append(f'<p class="foot">Run the worked code: '
                     f'<code>cd {html.escape(os.path.dirname(demo))} &amp;&amp; '
                     f'python3 {html.escape(os.path.basename(demo))}</code></p>')
    parts.append("</section>")
    return "\n".join(parts)


def _demo_rel(m):
    code = os.path.join(m["dir"], "code")
    if os.path.isdir(code):
        for f in sorted(os.listdir(code)):
            if f.endswith(".py") and not f.startswith("test_"):
                return os.path.relpath(os.path.join(code, f), HERE)
    return None


def _is_wsl():
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        with open("/proc/version") as fh:
            return "microsoft" in fh.read().lower()
    except OSError:
        return False


def _win_path(path):
    """WSL path -> Windows path (for explorer/cmd/powershell); identity on failure."""
    try:
        return subprocess.check_output(["wslpath", "-w", path], text=True).strip()
    except Exception:
        return path


def open_detached(target, is_url=False):
    """Open `target` (a file path, or a URL when is_url=True) in the browser WITHOUT
    tying it to this terminal: the child is put in its own session and its
    stdout/stderr are discarded, so the prompt returns immediately and browser
    start-up chatter never reaches the terminal. Returns True if a launcher started.

    On WSL we try wslview (wslu) and the Windows-interop launchers before xdg-open,
    since a bare xdg-open usually has no GUI to talk to."""
    url = target if is_url else "file://" + target
    quiet = dict(stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    launchers = []
    if sys.platform == "darwin":
        launchers.append(["open", url])
    elif os.name == "nt":
        try:
            os.startfile(target)                                # noqa: F821  (Windows only)
            return True
        except Exception:
            pass
    else:
        if _is_wsl():
            launchers.append(["wslview", url])
            winarg = url if is_url else _win_path(target)
            launchers.append(["cmd.exe", "/c", "start", "", winarg])
            launchers.append(["powershell.exe", "-NoProfile", "-Command", "Start-Process", winarg])
            if not is_url:
                launchers.append(["explorer.exe", winarg])
        launchers.append(["xdg-open", url])
    for cmd in launchers:
        try:
            subprocess.Popen(cmd, start_new_session=True, **quiet)
            return True
        except Exception:
            continue
    try:
        webbrowser.open(url)                                    # best-effort fallback
        return True
    except Exception:
        return False


def serve(port=8000, do_open=True):
    """Serve the modules folder over http://localhost and keep running. This is the
    reliable path on WSL/headless boxes where no file:// launcher works: open the
    printed localhost URL once in your browser and just refresh after regenerating."""
    import http.server
    import socketserver
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir(HERE)                                              # SimpleHTTPRequestHandler serves cwd
    httpd = None
    for p in range(port, port + 25):
        try:
            httpd = socketserver.ThreadingTCPServer(("127.0.0.1", p), handler)
            port = p
            break
        except OSError:
            continue
    if httpd is None:
        print(f"  could not bind a port in {port}..{port + 24}; open file://{OUT} manually")
        return
    url = f"http://localhost:{port}/{os.path.basename(OUT)}"
    print(f"\n  Serving at:  {url}")
    print( "  Open that in your browser (Ctrl+click in most terminals); Ctrl-C to stop.\n")
    if do_open:
        open_detached(url, is_url=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped.")
    finally:
        httpd.server_close()


def main():
    args = sys.argv[1:]
    mods = discover_modules() + discover_thermo()
    mods.sort(key=lambda d: (d["trunk"], d["num"]))
    if not mods:
        print("No modules found under", HERE)
        return
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(build_html(mods))
    neq = sum(len(extract_equations(_read(os.path.join(m["dir"], "notes.md")))) for m in mods)
    nfig = sum(len(discover_figures(m)) for m in mods)
    ntd = sum(1 for m in mods if m["trunk"] == THERMO_TRUNK)
    print(f"Wrote {OUT}")
    print(f"  {len(mods)} modules ({ntd} Thermo), {neq} equations (rendered by KaTeX), {nfig} figures")
    nlink = sum(1 for m in mods if m["id"] in NET_IDS)
    print(f"  {nlink} modules link to their orb in the Teaching Network "
          f"({len(mods) - nlink} are not in topic_network.txt)")
    if "--serve" in args:
        port = 8000
        i = args.index("--serve")
        if i + 1 < len(args) and args[i + 1].isdigit():
            port = int(args[i + 1])
        serve(port=port, do_open="--no-open" not in args)
    elif "--no-open" in args:
        print(f"  open it with:  xdg-open {OUT}   (or: python3 {os.path.basename(__file__)} --serve)")
    elif open_detached(OUT):
        print("  opened in your browser (KaTeX loads from a CDN — needs network)")
        print(f"  if nothing opened, run:  python3 {os.path.basename(__file__)} --serve")
    else:
        print(f"  open it manually:  file://{OUT}")
        print(f"  or serve it:  python3 {os.path.basename(__file__)} --serve")


if __name__ == "__main__":
    main()
