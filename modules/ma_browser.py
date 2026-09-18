#!/usr/bin/env python3
"""
MA Module Browser -- a desktop window to study the physics modules.

Pick a module on the left; on the right you get its scope, its key equations
(rendered as real math), and a worked example problem -- read straight from the
module's own README.md / notes.md / problems.md, so it always matches the files
in git. A button runs the module's demo so you can see the equations compute.

Design (matches schedule/calendar_app.py):
- Tkinter for the window (stdlib -- no install needed to browse).
- matplotlib's mathtext renders the $$...$$ equations to crisp images; anything
  mathtext can't do (matrices, multi-line) falls back to clean monospace text,
  so the GUI never breaks. If matplotlib is missing, every equation is text.
- Reads the live files under modules/<TRUNK>/<ID>_<slug>/ -- nothing is hardcoded.

Run it:   python3 modules/ma_browser.py
"""

import base64
import io
import os
import re
import subprocess
import sys

import tkinter as tk
from tkinter import ttk, font as tkfont

# matplotlib is optional: without it, equations show as their LaTeX source.
try:
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import mathtext
    from matplotlib.font_manager import FontProperties
    _MPL = True
except Exception:
    _MPL = False


# --------------------------------------------------------------------------
# Config & palette
# --------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))          # the modules/ folder
FONT_FAMILY = "DejaVu Sans"                                # full Unicode coverage
MONO_FAMILY = "DejaVu Sans Mono"

BG = "#f6f6fb"
PANEL = "#ffffff"
INK = "#1b1b2e"
ACCENT = "#3b3b6d"
MUTED = "#6b6b85"
CHECK_BG = "#eef3ff"
RULE = "#d9d9e6"
EQ_COLOR = "#16213e"
WRAP = 660                                                  # text wrap width (px)


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
    """Find every modules/<TRUNK>/<ID>_<slug>/ unit. Returns a list of dicts
    {id, trunk, num, slug, title, dir} sorted by trunk then number."""
    mods = []
    for trunk in sorted(os.listdir(root)):
        tdir = os.path.join(root, trunk)
        if not os.path.isdir(tdir) or not re.fullmatch(r"[A-Z]{2,3}x?|[A-Z]{2,8}_[A-Z]{2,8}", trunk):
            continue
        for name in os.listdir(tdir):
            mdir = os.path.join(tdir, name)
            m = re.fullmatch(r"([A-Z]{2,3}|[A-Z]{2,8}_[A-Z]{2,8})-(\d+)_(.+)", name)
            if not (os.path.isdir(mdir) and m):
                continue
            mid = f"{m.group(1)}-{m.group(2)}"
            title = _title_from_readme(os.path.join(mdir, "README.md")) or m.group(3).replace("_", " ").title()
            mods.append({"id": mid, "trunk": m.group(1), "num": int(m.group(2)),
                         "slug": m.group(3), "title": title, "dir": mdir})
    mods.sort(key=lambda d: (d["trunk"], d["num"]))
    return mods


def _title_from_readme(path):
    for line in _read(path).splitlines():
        if line.startswith("# "):
            head = line[2:].strip()
            for dash in ("—", " - ", " – "):       # em / hyphen / en dash
                if dash in head:
                    return head.split(dash, 1)[1].strip()
            return head
    return ""


def extract_section(md, header):
    """Return the body of a '## <header>' section (up to the next '## ')."""
    m = re.search(r"^##\s+" + re.escape(header) + r"\s*\n(.*?)(?=^##\s|\Z)",
                  md, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else ""


def extract_equations(notes_md, limit=12):
    """Pull the $$...$$ display equations from notes.md, in order."""
    eqs = [e.strip() for e in re.findall(r"\$\$(.+?)\$\$", notes_md, re.DOTALL)]
    eqs = [re.sub(r"\s+", " ", e) for e in eqs if e.strip()]
    return eqs[:limit]


def extract_first_problem(problems_md):
    """Return (title, citation, body) for the first '### P1.' problem."""
    blocks = re.split(r"^### ", problems_md, flags=re.MULTILINE)
    for blk in blocks[1:]:
        head, _, rest = blk.partition("\n")
        m = re.match(r"P\d+\.\s+(.*?)\s*(?:\*\((.*?)\)\*)?\s*$", head)
        if not m:
            continue
        title = m.group(1).strip()
        citation = (m.group(2) or "").strip()
        body = _clean_prose(rest.strip())
        return title, citation, body
    return "", "", ""


def _clean_prose(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)                  # drop bold markers
    s = re.sub(r"\*(.+?)\*", r"\1", s)                       # drop italics markers
    return s.strip()


# --------------------------------------------------------------------------
# Equation rendering (mathtext -> PNG -> Tk image), with a text fallback
# --------------------------------------------------------------------------

_BAD = (r"\begin", r"\\", r"\xrightarrow", r"\xleftarrow", "&",
        r"\underbrace", r"\overbrace", r"\substack")


def _clean_latex(s):
    s = re.sub(r"\\boxed\{(.*)\}", r"\1", s)                 # render boxed content
    s = re.sub(r"\\textbf\{(.*?)\}", r"\\mathbf{\1}", s)     # \textbf -> \mathbf (mathtext)
    s = re.sub(r"\\text\{(.*?)\}", r"\\mathrm{\1}", s)       # \text  -> \mathrm
    s = s.replace(r"\operatorname", r"\mathrm")
    s = s.replace(r"\tfrac", r"\frac").replace(r"\dfrac", r"\frac")
    s = s.replace(r"\lvert", "|").replace(r"\rvert", "|").replace(r"\lVert", r"\|").replace(r"\rVert", r"\|")
    s = s.replace(r"\!", "")                                 # negative space mathtext lacks
    tok = r"(\\[A-Za-z]+|[A-Za-z0-9])"
    s = re.sub(r"\\frac([A-Za-z0-9])\{", r"\\frac{\1}{", s)              # \frac1{..} -> \frac{1}{..}
    s = re.sub(r"\\frac\s*" + tok + r"\s*" + tok, r"\\frac{\1}{\2}", s)   # \frac1n -> \frac{1}{n}
    s = re.sub(r"\\sqrt\s+(\\?[A-Za-z0-9])", r"\\sqrt{\1}", s)            # \sqrt z -> \sqrt{z}
    # mathtext needs braces: "\mathbf a" -> "\mathbf{a}" (and \hat/\vec/\mathsf/...)
    s = re.sub(r"\\(mathbf|mathsf|mathrm|mathcal|mathbb|mathit|hat|vec|bar|tilde|dot|ddot)\s+(\\?[A-Za-z0-9])",
               r"\\\1{\2}", s)
    for big in (r"\Bigg", r"\bigg", r"\Big", r"\big"):       # sizing macros mathtext lacks
        s = s.replace(big, "")
    return s.strip()


def render_equation_png(latex, dpi=132, size=17):
    """Render a LaTeX display equation to PNG bytes via mathtext, or None if
    matplotlib is absent or the expression is outside mathtext's subset."""
    if not _MPL or any(tok in latex for tok in _BAD):
        return None
    try:
        buf = io.BytesIO()
        mathtext.math_to_image("$" + _clean_latex(latex) + "$", buf,
                               prop=FontProperties(size=size), dpi=dpi,
                               format="png", color=EQ_COLOR)
        return buf.getvalue()
    except Exception:
        return None


# --------------------------------------------------------------------------
# The application window
# --------------------------------------------------------------------------

class ModuleBrowser(tk.Tk):
    def __init__(self, modules):
        super().__init__()
        self.modules = modules
        self.title("MA Module Browser — equations & examples")
        self.geometry("1040x720")
        self.minsize(820, 560)
        self.configure(bg=BG)
        self._imgs = []                                     # keep PhotoImage refs alive

        self.h1 = tkfont.Font(family=FONT_FAMILY, size=17, weight="bold")
        self.h2 = tkfont.Font(family=FONT_FAMILY, size=12, weight="bold")
        self.body = tkfont.Font(family=FONT_FAMILY, size=11)
        self.small = tkfont.Font(family=FONT_FAMILY, size=10)
        self.mono = tkfont.Font(family=MONO_FAMILY, size=11)

        self._build_layout()
        if self._shown:
            start = next((i for i, m in enumerate(self._shown) if m["trunk"] == "MA"), 0)
            self.listbox.selection_set(start)
            self.listbox.see(start)
            self._show(self._shown[start])

    # ---- layout -------------------------------------------------------
    def _build_layout(self):
        header = tk.Frame(self, bg=ACCENT, height=46)
        header.pack(side="top", fill="x")
        tk.Label(header, text="  Physics Modules", bg=ACCENT, fg="white",
                 font=self.h1).pack(side="left", pady=8)
        tk.Label(header, text=f"{len(self.modules)} modules   ", bg=ACCENT,
                 fg="#c9c9ee", font=self.small).pack(side="right", pady=8)

        left = tk.Frame(self, bg=BG, width=250)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        self.filter_var = tk.StringVar()
        fe = tk.Entry(left, textvariable=self.filter_var, font=self.body,
                      relief="flat", bg=PANEL, fg=INK)
        fe.pack(fill="x", padx=8, pady=(8, 2), ipady=4)
        fe.insert(0, "")
        self.filter_var.trace_add("write", lambda *_: self._refresh_list())
        tk.Label(left, text="type to filter", bg=BG, fg=MUTED,
                 font=self.small).pack(anchor="w", padx=10)

        lb_wrap = tk.Frame(left, bg=BG)
        lb_wrap.pack(fill="both", expand=True, padx=8, pady=6)
        self.listbox = tk.Listbox(lb_wrap, font=self.body, activestyle="none",
                                  bg=PANEL, fg=INK, selectbackground=ACCENT,
                                  selectforeground="white", relief="flat",
                                  highlightthickness=0)
        sb = ttk.Scrollbar(lb_wrap, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)
        self._refresh_list()

        # right: scrollable content area
        right = tk.Frame(self, bg=PANEL)
        right.pack(side="right", fill="both", expand=True)
        self.canvas = tk.Canvas(right, bg=PANEL, highlightthickness=0)
        rsb = ttk.Scrollbar(right, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=rsb.set)
        rsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.content = tk.Frame(self.canvas, bg=PANEL)
        self._win = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.content.bind("<Configure>",
                          lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self._win, width=e.width))
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.canvas.bind_all(seq, self._on_wheel)

    def _on_wheel(self, e):
        delta = 1 if getattr(e, "num", None) == 5 else -1 if getattr(e, "num", None) == 4 else int(-e.delta / 120)
        self.canvas.yview_scroll(delta, "units")

    # ---- list ---------------------------------------------------------
    def _refresh_list(self):
        flt = self.filter_var.get().lower().strip()
        self.listbox.delete(0, "end")
        self._shown = []
        for mod in self.modules:
            label = f"{mod['id']} — {mod['title']}"
            if flt in label.lower():
                self.listbox.insert("end", label)
                self._shown.append(mod)

    def _on_select(self, _evt):
        sel = self.listbox.curselection()
        if sel:
            self._show(self._shown[sel[0]])

    # ---- content ------------------------------------------------------
    def _add_rule(self):
        tk.Frame(self.content, bg=RULE, height=1).pack(fill="x", padx=24, pady=(14, 10))

    def _heading(self, text):
        tk.Label(self.content, text=text, bg=PANEL, fg=ACCENT, font=self.h2,
                 anchor="w").pack(fill="x", padx=24, pady=(2, 6))

    def _para(self, text, font=None, fg=INK, pad=24):
        tk.Label(self.content, text=text, bg=PANEL, fg=fg, font=font or self.body,
                 wraplength=WRAP, justify="left", anchor="w").pack(fill="x", padx=pad, pady=2)

    def _show(self, mod):
        for w in self.content.winfo_children():
            w.destroy()
        self._imgs.clear()
        self.current = mod

        readme = _read(os.path.join(mod["dir"], "README.md"))
        notes = _read(os.path.join(mod["dir"], "notes.md"))
        problems = _read(os.path.join(mod["dir"], "problems", "problems.md"))

        tk.Label(self.content, text=f"{mod['id']}  —  {mod['title']}", bg=PANEL,
                 fg=INK, font=self.h1, wraplength=WRAP, justify="left",
                 anchor="w").pack(fill="x", padx=24, pady=(16, 2))

        scope = extract_section(readme, "Scope")
        if scope:
            self._para(_clean_prose(scope), fg=MUTED)

        # equations
        self._add_rule()
        self._heading("Key equations")
        eqs = extract_equations(notes)
        if not eqs:
            self._para("(no display equations in notes.md)", fg=MUTED)
        for eq in eqs:
            png = render_equation_png(eq)
            if png:
                img = tk.PhotoImage(data=base64.b64encode(png).decode("ascii"))
                if img.width() > WRAP + 40:                 # shrink very wide equations
                    img = img.subsample(-(-img.width() // (WRAP + 40)))
                self._imgs.append(img)
                tk.Label(self.content, image=img, bg=PANEL, anchor="w").pack(fill="x", padx=30, pady=7)
            else:
                tk.Label(self.content, text=eq, bg=PANEL, fg=EQ_COLOR, font=self.mono,
                         wraplength=WRAP, justify="left", anchor="w").pack(fill="x", padx=30, pady=5)

        # example problem
        self._add_rule()
        self._heading("Example problem")
        title, citation, pbody = extract_first_problem(problems)
        if title:
            self._para(title, font=self.h2, fg=INK)
            if citation:
                self._para(citation, font=self.small, fg=MUTED)
            for line in pbody.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if line.startswith("Check:"):
                    tk.Label(self.content, text=line, bg=CHECK_BG, fg=ACCENT, font=self.mono,
                             wraplength=WRAP, justify="left", anchor="w").pack(fill="x", padx=30, pady=(8, 2))
                else:
                    self._para(line, pad=30)
        else:
            self._para("(no problems.md found)", fg=MUTED)

        # run-demo button
        self._add_rule()
        demo = self._demo_path(mod)
        btn = tk.Button(self.content, text="▶  Run module demo", font=self.body,
                        bg=ACCENT, fg="white", relief="flat", activebackground="#2c2c55",
                        activeforeground="white", padx=14, pady=6,
                        command=lambda: self._run_demo(mod),
                        state=("normal" if demo else "disabled"))
        btn.pack(anchor="w", padx=30, pady=(2, 26))

        self.canvas.yview_moveto(0.0)

    # ---- demo runner --------------------------------------------------
    def _demo_path(self, mod):
        code = os.path.join(mod["dir"], "code")
        if not os.path.isdir(code):
            return None
        for f in sorted(os.listdir(code)):
            if f.endswith(".py") and not f.startswith("test_"):
                return os.path.join(code, f)
        return None

    def _run_demo(self, mod):
        demo = self._demo_path(mod)
        win = tk.Toplevel(self)
        win.title(f"{mod['id']} demo — {os.path.basename(demo)}")
        win.geometry("760x520")
        win.configure(bg=PANEL)
        txt = tk.Text(win, font=self.mono, bg="#0f1020", fg="#e6e6f0", wrap="none",
                      relief="flat", padx=10, pady=8)
        txt.pack(fill="both", expand=True)
        txt.insert("end", f"$ python3 {os.path.basename(demo)}\n\n")
        win.update()
        try:
            out = subprocess.run([sys.executable, os.path.basename(demo)],
                                 cwd=os.path.dirname(demo), capture_output=True,
                                 text=True, timeout=60)
            txt.insert("end", out.stdout or "")
            if out.stderr:
                txt.insert("end", "\n[stderr]\n" + out.stderr)
        except subprocess.TimeoutExpired:
            txt.insert("end", "\n[timed out after 60 s]")
        except Exception as exc:                            # pragma: no cover
            txt.insert("end", f"\n[error: {exc}]")
        txt.configure(state="disabled")


def main():
    mods = discover_modules()
    if not mods:
        print("No modules found under", HERE)
        return
    try:
        app = ModuleBrowser(mods)
    except tk.TclError as exc:
        print("Could not open a window (no display?):", exc)
        print("Found modules:", ", ".join(m["id"] for m in mods))
        return
    app.mainloop()


if __name__ == "__main__":
    main()
