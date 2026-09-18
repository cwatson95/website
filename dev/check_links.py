#!/usr/bin/env python3
"""check_links.py — audit the Teaching ↔ Modules round trip.

teaching.html (the network) offers "open module" on every orb whose module
page exists, pointing at ../modules/teaching_modules.html#<id>; every module
that is a node of the network links back to ../website/teaching.html#<id>.
This checks the two generated artefacts against each other and against the
module folders, with no browser:

  1. the DATA baked into teaching_network.js carries the has-page field, and
     it agrees with the folders projects/modules/<TRUNK>/<ID>_*/;
  2. every flagged node's href lands on a <section id="m-<id>"> of
     teaching_modules.html (a hub: on some m-<trunk>-nn), unflagged ones on
     none;
  3. exactly the module sections that are nodes carry one netlink, each
     inside its own section, and every netlink's node is flagged;
  4. teaching.html holds the #net-module anchor, keeps its Modules tab and is
     tag-balanced; style.css styles the anchor;
  5. if deno is installed, render_check/links_harness.js drives both pages'
     scripts headlessly (hash -> orb, hash -> module, panel link, URL sync).

Usage: python3 dev/check_links.py          (from projects/website/)
Exit status 1 on any failure. Rerun after build_network.py or
generate_webpage.py.
"""
import json
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'source', 'track', 'wbr'}


class Balance(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f'unexpected </{tag}> (open: {self.stack[-3:]})')


def main():
    here = Path(__file__).resolve().parent
    site = here.parent
    modules = site.parent / 'modules'
    if not (modules / 'teaching_modules.html').exists():
        # deployed layout: modules/ is a child of the site root, not a sibling
        modules = site / 'modules'
    fails = []

    def ok(cond, msg):
        print(('  ok    ' if cond else '  FAIL  ') + msg)
        if not cond:
            fails.append(msg)

    # 1. the baked network
    js = (site / 'teaching_network.js').read_text()
    data = json.loads(re.search(r'var DATA = (\{.*?\});\n', js).group(1))
    nodes = data['nodes']
    ok(all(len(n) == 8 for n in nodes), f'{len(nodes)} nodes carry the has-page field')
    hubs = {n[0] for n in nodes if n[3] == 1}
    mods = {n[0] for n in nodes if n[3] == 0}
    flagged = {n[0] for n in nodes if len(n) > 7 and n[7] == 1}
    built = set()
    for h in hubs:
        d = modules / h
        if d.is_dir():
            for p in d.iterdir():
                m = re.match(r'^([A-Z]{2,3}-\d{2})_', p.name)
                if m and p.is_dir():
                    built.add(m.group(1))
    bad = sorted(i for i in mods if (i in flagged) != (i in built))
    ok(not bad, f'module-node flags agree with the folders '
                f'({len(mods & flagged)} of {len(mods)} flagged): {bad[:8]}')
    bad = sorted(h for h in hubs
                 if (h in flagged) != any(b.startswith(h + '-') for b in built))
    ok(not bad, f'hub flags agree with the folders (hubs with pages: '
                f'{sorted(hubs & flagged)}): {bad}')

    # 2. the modules page(s): sections
    # The browser is one page per trunk (modules_<TRUNK>.html) with
    # teaching_modules.html as the index and deep-link forwarder; --single puts
    # everything back on that one page. Audit whichever shape is on disk.
    trunk_pages = sorted(modules.glob('modules_*.html'))
    idx_html = (modules / 'teaching_modules.html').read_text()
    html = '\n'.join(p.read_text() for p in trunk_pages) if trunk_pages else idx_html
    secs = re.findall(r'<section id="m-([^"]+)" class="module', html)
    sec_set = set(secs)
    ok(len(secs) == len(sec_set), f'{len(secs)} module sections, ids unique')
    bad = sorted(i for i in mods if (i in flagged) != (i in sec_set))
    ok(not bad, f'module-node flags agree with the sections: {bad[:8]}')
    bad = sorted(h for h in hubs
                 if (h in flagged) != any(s.startswith(h + '-') for s in sec_set))
    ok(not bad, f'hub flags agree with the sections: {bad}')
    ok(all((any(s.startswith(f + '-') for s in sec_set) if f in hubs else f in sec_set)
           for f in flagged),
       'every "open module" href lands on a section of the modules page')

    # 2b. the index must be able to forward every deep link to the right page
    if trunk_pages:
        ok(len(trunk_pages) > 1, f'{len(trunk_pages)} trunk pages')
        mo = re.search(r'window\.ALLMODS=(\[.*?\]);window\.PAGE_TRUNK', idx_html, re.S)
        ok(mo is not None, 'the index carries the catalogue (ALLMODS)')
        cat = json.loads(mo.group(1)) if mo else []
        ids = {r[0] for r in cat}
        ok(sec_set <= ids, f'every section is listed in the index: '
                           f'{sorted(sec_set - ids)[:8]}')
        pages = {p.name for p in trunk_pages}
        want = {f'modules_{r[2]}.html' for r in cat}
        ok(want <= pages, f'every trunk in the index has a page: {sorted(want - pages)}')
        gone = sorted(i for i in (mods & flagged) if i not in ids)
        ok(not gone, f'every flagged network module is forwardable: {gone[:8]}')

    # 3. the back-links
    # the modules page is generated for either layout: the sibling checkout
    # (../website/) or GitHub Pages, where modules/ is a child of the site
    # root (../).  Detect which, then hold every back-link to that same prefix.
    mp = re.search(r'href="((?:\.\./)+(?:website/)?)teaching\.html">Teaching</a>', html)
    ok(mp is not None, 'modules page nav still points at teaching.html')
    PREF = mp.group(1) if mp else '../website/'
    NETLINK = r'class="netlink" href="%steaching\.html#([^"]+)"' % re.escape(PREF)
    links = re.findall('<a ' + NETLINK, html)
    link_set = set(links)
    ok(len(links) == len(link_set), f'{len(links)} netlinks, ids unique')
    ok(link_set <= (hubs | mods),
       f'every netlink targets a node of the network: {sorted(link_set - hubs - mods)[:8]}')
    want = sec_set & mods
    ok(link_set == want,
       f'exactly the module sections that are nodes link back ({len(want)}): '
       f'missing {sorted(want - link_set)[:8]}, extra {sorted(link_set - want)[:8]}')
    ok(link_set <= flagged, 'every module that links back is offered as "open module"')
    wrong = []
    for m in re.finditer(r'<section id="m-([^"]+)" class="module[^>]*>(.*?)'
                         r'(?=<section id="m-|</main>)', html, re.S):
        inside = re.findall(NETLINK, m.group(2))
        if inside and inside != [m.group(1)]:
            wrong.append((m.group(1), inside))
    ok(not wrong, f'each netlink sits in its own module section: {wrong[:5]}')

    # 4. the network page
    th = (site / 'teaching.html').read_text()
    ok('id="net-module"' in th, 'teaching.html has the #net-module anchor')
    ok('href="../modules/teaching_modules.html"' in th,
       'teaching.html nav still points at the modules page')
    b = Balance()
    b.feed(th)
    ok(not b.errors and not b.stack, f'teaching.html tag-balanced: {b.errors[:3]} {b.stack[:3]}')
    ok('.net-module' in (site / 'style.css').read_text(), 'style.css styles .net-module')

    # 5. the scripts, driven headlessly
    deno = shutil.which('deno')
    # the harness evals a page's inline script: give it one that has modules
    mod_page = trunk_pages[0] if trunk_pages else modules / 'teaching_modules.html'
    harness = here / 'render_check' / 'links_harness.js'
    if deno:
        for mode in ('network', 'modules'):
            print(f'-- links_harness.js {mode}')
            r = subprocess.run([deno, 'run', '--allow-read', str(harness), mode,
                                str(site), str(mod_page)],
                               capture_output=True, text=True)
            sys.stdout.write(r.stdout)
            if r.returncode:
                sys.stdout.write(r.stderr)
            ok(r.returncode == 0, f'links_harness.js {mode}: exit {r.returncode}')
    else:
        print('  skip  deno not found: links_harness.js not run')

    print(f'{len(fails)} failure(s)' if fails else 'all checks passed')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
