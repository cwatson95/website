#!/usr/bin/env python3
"""Build em_prelim_problems.pdf from em_prelim_problems.md (tectonic + XeLaTeX).

The markdown is the browser-format transcription of em_prelim_notes.pdf
(### P<n>. Title *(pp. N-M)* headings, **Solution.** blocks, $$ display math).
This converts it to a LaTeX article (DejaVu fonts for the Unicode prose, TOC of
all problems, one problem per page) and compiles it. Display equations measure
themselves and shrink to the line width only when a single-line equation is too
wide; $$ blocks containing \\tag are wrapped in equation* so the tag renders.

Run:  python3 modules/em_prelim_pdf.py         # writes modules/em_prelim_problems.pdf
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "em_prelim_problems.md")
OUT = os.path.join(HERE, "em_prelim_problems.pdf")

CHARMAP = {
    "①": r"\textcircled{\scriptsize 1}", "②": r"\textcircled{\scriptsize 2}",
    "−": "-", "₀": r"\textsubscript{0}", "→": r"$\to$", "δ": r"$\delta$",
}

PREAMBLE = r"""\documentclass[11pt,letterpaper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{cancel}
\usepackage{parskip}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{fontspec}
\setmainfont{DejaVu Serif}
\setmonofont{DejaVu Sans Mono}
\usepackage[colorlinks=true,linkcolor=blue!50!black,pdftitle={EM Prelim Notes — Transcribed Problems}]{hyperref}
\setcounter{tocdepth}{1}
\setlength{\emergencystretch}{2em}
% display math that measures itself and shrinks to \linewidth only when needed
\newsavebox{\eqsavebox}
\newenvironment{fiteq}
  {\begin{lrbox}{\eqsavebox}$\displaystyle}
  {$\end{lrbox}\begin{displaymath}
   \ifdim\wd\eqsavebox>\linewidth
     \resizebox{\linewidth}{!}{\usebox{\eqsavebox}}%
   \else\usebox{\eqsavebox}\fi
   \end{displaymath}}
\begin{document}
\begin{center}
{\LARGE\bfseries EM Prelim Notes --- Transcribed Problems}\\[6pt]
{\large transcribed from \texttt{em\_prelim\_notes.pdf} \textperiodcentered{} July 2, 2026}
\end{center}
\bigskip
"""


def prose_tex(s):
    s = re.sub(r"([&%#_])", r"\\\1", s)
    for k, v in CHARMAP.items():
        s = s.replace(k, v)
    s = re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + m.group(1) + "}", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    # emphasis may span lines (it can contain math) but never a blank line
    s = re.sub(r"(?<!\*)\*(?!\*)((?:(?!\n[ \t]*\n).)+?)(?<!\*)\*(?!\*)",
               r"\\emph{\1}", s, flags=re.DOTALL)
    return s


def body_tex(text):
    """Prose + $/$$ math -> LaTeX. Math is stashed behind placeholders so the
    prose regexes (escaping, bold, italics) never touch it or pair asterisks
    across math spans."""
    stash = []

    def keep(m):
        s = m.group(0)
        if s.startswith("$$"):
            inner = s[2:-2].strip()
            s = ("\\begin{equation*}\n" + inner + "\n\\end{equation*}"
                 if "\\tag" in inner else
                 "\\begin{fiteq}\n" + inner + "\n\\end{fiteq}")
        stash.append(s)
        return f"\x00{len(stash) - 1}\x00"

    t = re.sub(r"\$\$.*?\$\$|\$[^$\n]+\$", keep, text, flags=re.DOTALL)
    t = prose_tex(t)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], t)


def build_tex(src):
    first = src.index("### P")
    header, body = src[:first], src[first:]
    header = re.sub(r"\A#\s+[^\n]*\n", "", header).strip()

    parts = []
    for e in re.split(r"^(?=### P\d+\.)", body, flags=re.MULTILINE):
        if not e.startswith("### P"):
            continue
        head, _, rest = e.partition("\n")
        m = re.match(r"### (P\d+)\.\s+(.*?)\s*(?:\*\((.*?)\)\*)?\s*$", head)
        tag, title, cite = m.group(1), m.group(2), (m.group(3) or "")
        t = prose_tex(title)
        parts.append(
            f"\\clearpage\n\\section*{{{tag}. {t}}}\n"
            f"\\addcontentsline{{toc}}{{section}}{{{tag}. {t}}}\n"
            + (f"\\noindent{{\\color{{gray}}\\small ({prose_tex(cite)})}}\\par\\medskip\n"
               if cite else "")
            + body_tex(rest.strip()) + "\n")

    doc = (PREAMBLE + body_tex(header)
           + "\n\\clearpage\n\\tableofcontents\n"
           + "\n".join(parts) + "\n\\end{document}\n")
    # let the long filename break after the underscore on the title page
    return doc.replace(r"\texttt{em\_prelim\_notes.pdf}",
                       r"\texttt{em\_prelim\_\allowbreak notes.pdf}")


def main():
    src = open(SRC, encoding="utf-8").read()
    with tempfile.TemporaryDirectory() as tmp:
        tex = os.path.join(tmp, "em_prelim_problems.tex")
        open(tex, "w", encoding="utf-8").write(build_tex(src))
        r = subprocess.run(["tectonic", tex], cwd=tmp)
        if r.returncode:
            sys.exit("tectonic failed")
        shutil.copy(os.path.join(tmp, "em_prelim_problems.pdf"), OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
