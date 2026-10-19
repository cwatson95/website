#!/usr/bin/env python3
"""Inventory the PhET HTML5 builds in docs/phets/.

For every <stem>_en.html: title, version, the screens, and the sim's own English
strings (keys under its repo prefix), read from the embedded
`phet.chipper.strings = {"en": {...}}` table. Nothing is executed.

Writes inventory.json (full string maps, one entry per sim) and prints a
compact table.  Run from anywhere:  python3 survey.py
"""
import io
import json
import os
import re
import subprocess
import tempfile

JSC = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"
HERE = os.path.dirname(os.path.abspath(__file__))
PHETS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "phets"))
BIDI = dict.fromkeys(map(ord, "‪‫‬‎‏"), None)
# PhET framework repos: generic chrome (menus, keyboard help, sound, games),
# not the sim's own content
FRAMEWORK = {"JOIST", "SCENERY_PHET", "SUN", "TAMBO", "VEGAS", "SCENERY", "PHETCOMMON",
             "AXON", "DOT", "KITE", "TWIXT", "UTTERANCE_QUEUE", "BRAND", "CHIPPER",
             "SHERPA", "PHET_IO", "TANDEM", "QUERY_STRING_MACHINE", "GRIDDLE", "BAMBOO",
             "PHET_CORE", "INTERACTION_DIALOG", "PERENNIAL", "SIMULA_RASA"}
NOT_UI = re.compile(r"(a11y|[dD]escription|[hH]elp|pdom|PDOM|[vV]oicing|[kK]eyboard)")


def clean(v):
    return v.translate(BIDI) if isinstance(v, str) else v


def strings_table(src):
    """The first `phet.chipper.strings = {...}` whose right-hand side is JSON
    with an "en" table (earlier assignments can be code, e.g. `|| {}`)."""
    for m in re.finditer(r"phet\.chipper\.strings\s*=\s*", src):
        if src[m.end():m.end() + 1] != "{":
            continue
        try:
            obj, _ = json.JSONDecoder().raw_decode(src, m.end())
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("en"), dict):
            return obj["en"]
    # newer builds: `phet.chipper.strings = (y=>{...decoder...})('...');` on one
    # line. Evaluate just that statement in JavaScriptCore and read the result.
    m = re.search(r"phet\.chipper\.strings\s*=\s*\(", src)
    if not m:
        return {}
    stmt = src[m.start():src.index("\n", m.start())]
    js = ("var phet={chipper:{}};\n" + stmt +
          "\nprint(JSON.stringify(phet.chipper.strings));\n")
    fd, tmp = tempfile.mkstemp(suffix=".js")
    os.close(fd)
    with io.open(tmp, "w", encoding="utf-8") as f:
        f.write(js)
    try:
        r = subprocess.run([JSC, tmp], capture_output=True, text=True, timeout=60)
    finally:
        os.remove(tmp)
    if r.returncode != 0:
        raise RuntimeError("jsc failed: " + r.stderr[:300])
    obj = json.loads(r.stdout)
    return obj.get("en", {})


def main():
    out = {}
    for fn in sorted(os.listdir(PHETS)):
        if not fn.endswith(".html"):
            continue
        stem = fn[:-len("_en.html")] if fn.endswith("_en.html") else fn[:-5]
        src = io.open(os.path.join(PHETS, fn), encoding="utf-8", errors="replace").read()
        title = re.search(r"<title>(.*?)</title>", src, flags=re.S)
        title = clean(re.sub(r"&#\d+;", "", title.group(1))).strip() if title else stem
        ver = re.search(r"phet\.chipper\.version\s*=\s*['\"]([^'\"]+)['\"]", src)
        table = strings_table(src)
        own_repo = stem.upper().replace("-", "_")
        # every non-framework repo's UI strings, grouped by repo; a11y /
        # description / help text is voluminous and not UI labels
        ui = {}
        for k, v in table.items():
            repo, _, key = k.partition("/")
            if repo in FRAMEWORK or NOT_UI.search(key):
                continue
            ui.setdefault(repo, {})[key] = clean(v)
        screens = {repo: [v for k, v in d.items() if re.fullmatch(r"screen\.[A-Za-z0-9]+", k)]
                   for repo, d in ui.items()}
        screens = {r: s for r, s in screens.items() if s}
        out[stem] = {"file": fn, "title": title, "version": ver.group(1) if ver else "?",
                     "bytes": len(src.encode("utf-8", "replace")), "own_repo": own_repo,
                     "screens_by_repo": screens,
                     "n_ui": sum(len(d) for d in ui.values()), "ui_by_repo": ui}
    with io.open(os.path.join(HERE, "inventory.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    for stem, d in out.items():
        own = d["screens_by_repo"].get(d["own_repo"])
        scr = ", ".join(own) if own else "; ".join(
            f"{r}: {', '.join(s)}" for r, s in d["screens_by_repo"].items()) or "(single)"
        repos = ",".join(sorted(d["ui_by_repo"]))
        print(f"{stem:40s} ui={d['n_ui']:4d} [{repos}]  screens: {scr}")
    print(len(out), "sims")


if __name__ == "__main__":
    main()
