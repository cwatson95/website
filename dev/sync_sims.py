#!/usr/bin/env python3
"""sync_sims.py — copy every simulation from projects/simulations/ into
projects/website/simulations/.

The site is a self-contained folder (file:// now, static hosting later), so
the sims it links are copies, not ../ references. projects/simulations/ stays
the source of truth — rerun this after a sim changes there or a new one
lands. There is no hand-kept list: every top-level *.html in the source
directory is a finished sim (house rule), so discovery IS the catalog.

Every sim carries the injected site header whose tabs point at
../website/*.html and ../modules/teaching_modules.html (right for
projects/simulations/, one level beside both). Inside the site the sims live
in website/simulations/, so the copy step rewrites
href="../website/ -> href="../ and href="../modules/ -> href="../../modules/
— the copies are otherwise byte-identical to the source.

After copying, stale copies whose source is gone are deleted, and the cards
in simulations.html are audited against the copied set: a card linking a sim
that does not exist is an ERROR (dead link on the site); a copied sim with
no card is a WARNING (nothing links it — add a card).

Usage: python3 dev/sync_sims.py [--source DIR]
"""
import argparse
import hashlib
import re
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent          # .../website/dev
    site = here.parent
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default=str(site.parent / 'simulations'))
    args = ap.parse_args()
    src = Path(args.source)
    dst = site / 'simulations'
    dst.mkdir(exist_ok=True)

    sims = sorted(p.name for p in src.glob('*.html'))
    if not sims:
        raise SystemExit(f'no *.html found in {src}')

    for s in sims:
        shutil.copy2(src / s, dst / s)
        b = dst / s
        data = (b.read_bytes()
                .replace(b'href="../website/', b'href="../')
                .replace(b'href="../modules/', b'href="../../modules/'))
        b.write_bytes(data)
        h = hashlib.sha256(data).hexdigest()[:12]
        print(f'{s:32s} {len(data):8d} B  sha256:{h}')

    for p in sorted(dst.glob('*.html')):
        if p.name not in sims:
            p.unlink()
            print(f'removed stale copy: {p.name}')

    page = (site / 'simulations.html').read_text()
    carded = set(re.findall(r'href="simulations/([^"]+\.html)"', page))
    for s in sorted(set(sims) - carded):
        print(f'WARNING: {s} copied but has no card in simulations.html')
    print(f'{len(sims)} sims -> {dst} (site-nav hrefs rewritten for in-site paths)')
    dead = sorted(carded - set(sims))
    if dead:
        raise SystemExit(f'ERROR: cards link missing sims: {dead}')


if __name__ == '__main__':
    main()
