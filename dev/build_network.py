#!/usr/bin/env python3
"""build_network.py — bake projects/modules/topic_network.txt into the
AUTO-GENERATED DATA block of teaching_network.js.

The page must work over file:// (no fetch), so the network is embedded:
nodes get positions from a seeded force layout here, at build time.
Rerun this after editing topic_network.txt -- and after a module lands: each
node also carries a has-module-page flag (field 8), set for a module node when
projects/modules/<TRUNK>/<ID>_<slug>/ exists and for a trunk hub when its
folder holds any module. The Teaching page offers its "open module" link
(../modules/teaching_modules.html#<id>) only on flagged nodes; the modules
page links back with teaching.html#<id>. dev/check_links.py audits both ways.

Usage:
  python3 build_network.py [--source PATH] [--target PATH] [--modules DIR] [--preview PNG]

Edges extracted:
  chain   consecutive modules within a trunk ("rough prerequisite order")
  hub     trunk hub -> its first module
  cross   the "~XX-nn" tags (deduplicated symmetric pairs)
  bridge  consecutive ids inside each KEY BRIDGES entry (B1..B11);
          an existing chain/cross edge is upgraded to bridge
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np

TRUNKS = ['MA', 'CM', 'EM', 'QM', 'RE', 'SM', 'QO', 'PK', 'QF', 'ST', 'CMx', 'QC']
ID_RE = r'CMx|QC|[A-Z]{2}-\d{2}'
EK = {'chain': 0, 'hub': 1, 'cross': 2, 'bridge': 3}
SEED = 20260812
MOD_DIR_RE = re.compile(r'^([A-Z]{2,3}-\d{2})_')   # modules/<TRUNK>/<ID>_<slug>/


def module_pages(nodes, modules_dir):
    """Which nodes have a page in the modules browser (teaching_modules.html):
    a module node when modules/<TRUNK>/<ID>_<slug>/ exists, a trunk hub when
    its folder holds at least one such module. Returns {id: bool}."""
    root = Path(modules_dir)
    built = set()
    for t in {nd['trunk'] for nd in nodes}:
        tdir = root / t
        if not tdir.is_dir():
            continue
        for p in tdir.iterdir():
            m = MOD_DIR_RE.match(p.name)
            if m and p.is_dir():
                built.add(m.group(1))
    return {nd['id']: (any(b.startswith(nd['trunk'] + '-') for b in built)
                       if nd['kind'] == 'trunk' else nd['id'] in built)
            for nd in nodes}


def parse(text):
    lines = text.split('\n')

    trunk_names = {}
    for ln in lines:
        m = re.match(r'^\s{4}(MA|CM|EM|QM|RE|SM|QO|PK|QF|ST|CMx|QC)\s+(.+)$', ln)
        if m and m.group(1) not in trunk_names:
            name = re.split(r'\s{2,}|\s+\(', m.group(2))[0].strip()
            if name:
                trunk_names[m.group(1)] = name

    header_re = re.compile(r'^\s*\[(MA|CM|EM|QM|RE|SM|QO|PK|QF|ST|CMx|QC)\]\s+[A-Z]')
    mod_re = re.compile(r'^\s{2}([A-Z]{2}-\d{2})\s+(.+)$')

    nodes, node_ix = [], {}
    pending_cross = []           # (from_id, to_id)
    edges = {}                   # normalized (a,b) -> kind name

    def add_node(nid, label, trunk, kind, adv=False, stub=False):
        node_ix[nid] = len(nodes)
        nodes.append({'id': nid, 'label': label, 'trunk': trunk,
                      'kind': kind, 'adv': adv, 'stub': stub})

    def add_edge(a, b, kind):
        if a == b:
            return
        key = (min(a, b), max(a, b))
        if kind == 'bridge':
            edges[key] = 'bridge'
        else:
            edges.setdefault(key, kind)

    cur_trunk, prev_mod = None, None
    in_bridges, passed_close = False, False
    bridge_entries = []

    for ln in lines:
        if not in_bridges and ln.strip().startswith('KEY BRIDGES'):
            in_bridges, passed_close = True, False
            cur_trunk, prev_mod = None, None
            continue
        if in_bridges:
            if re.match(r'^\s*=+\s*$', ln):
                if not passed_close:
                    passed_close = True
                    continue
                in_bridges = False
                continue
            if not passed_close:
                continue
            m = re.match(r'^\s{2}(B\d+)\s+(.+)$', ln)
            if m:
                bridge_entries.append(m.group(2))
            elif bridge_entries and ln.strip():
                bridge_entries[-1] += ' ' + ln.strip()
            continue

        m = header_re.match(ln)
        if m:
            cur_trunk, prev_mod = m.group(1), None
            if cur_trunk not in node_ix:
                add_node(cur_trunk, trunk_names.get(cur_trunk, cur_trunk),
                         cur_trunk, 'trunk', stub='[stub]' in ln)
            continue

        m = mod_re.match(ln)
        if m and cur_trunk and m.group(1).startswith(cur_trunk):
            nid, rest = m.group(1), m.group(2)
            for tgt in re.findall(r'~(' + ID_RE + r')', rest):
                pending_cross.append((nid, tgt))
            title = re.split(r'\s{2,}~', rest)[0]
            title = re.sub(r'\s*\(->.*?\)', '', title)
            adv = '[adv]' in title
            title = title.replace('[adv]', '').strip()
            add_node(nid, title, cur_trunk, 'module', adv=adv)
            if prev_mod:
                add_edge(prev_mod, nid, 'chain')
            else:
                add_edge(cur_trunk, nid, 'hub')
            prev_mod = nid

    missing = []
    for a, b in pending_cross:
        if a in node_ix and b in node_ix:
            add_edge(a, b, 'cross')
        else:
            missing.append((a, b))

    for entry in bridge_entries:
        ids = [i for i in re.findall(ID_RE, entry) if i in node_ix]
        for a, b in zip(ids, ids[1:]):
            add_edge(a, b, 'bridge')

    edge_list = [(node_ix[a], node_ix[b], EK[k]) for (a, b), k in sorted(edges.items())]
    return nodes, edge_list, trunk_names, missing


# Hub ring order: heavily-linked trunks adjacent (each neighbor pair shares
# cross-links) AND big clusters interleaved with small ones so no arc crowds.
RING = ['MA', 'ST', 'SM', 'PK', 'QO', 'QF', 'QM', 'QC', 'CMx', 'EM', 'RE', 'CM']
RING_R = 1200


def layout(nodes, edge_list):
    """Constellation layout: hubs pinned on a ring; each trunk's chain wound
    as an arc-length spiral around its hub; relaxation only *within* trunks
    (plus short-range separation), so cross-links/bridges stay long faint
    threads between clusters instead of dragging them into a hairball."""
    n = len(nodes)
    rng = np.random.default_rng(SEED)
    pos = np.zeros((n, 2))

    hub_xy = {}
    for i, nd in enumerate(nodes):
        if nd['kind'] == 'trunk':
            th = 2 * np.pi * RING.index(nd['trunk']) / len(RING) - np.pi / 2
            pos[i] = [RING_R * np.cos(th), RING_R * np.sin(th)]
            hub_xy[nd['trunk']] = pos[i].copy()

    counters = {}
    for i, nd in enumerate(nodes):
        if nd['kind'] != 'module':
            continue
        j = counters.setdefault(nd['trunk'], 0)
        counters[nd['trunk']] = j + 1
        if j == 0:
            # spiral cursor per trunk: radius, angle (start facing outward)
            hx, hy = hub_xy[nd['trunk']]
            counters[nd['trunk'] + '_r'] = 58.0
            counters[nd['trunk'] + '_a'] = np.arctan2(hy, hx) + rng.uniform(-0.8, 0.8)
        r = counters[nd['trunk'] + '_r']
        a = counters[nd['trunk'] + '_a']
        pos[i] = hub_xy[nd['trunk']] + [r * np.cos(a), r * np.sin(a)]
        pos[i] += rng.normal(0, 6, 2)
        counters[nd['trunk'] + '_a'] = a + 60.0 / r        # ~constant arc step
        counters[nd['trunk'] + '_r'] = r + 5.2

    anchor = pos.copy()
    trunk_ix = {t: k for k, t in enumerate(TRUNKS)}
    tof = np.array([trunk_ix[nd['trunk']] for nd in nodes])
    same = tof[:, None] == tof[None, :]

    ea = np.array([e[0] for e in edge_list])
    eb = np.array([e[1] for e in edge_list])
    ek = np.array([e[2] for e in edge_list])
    chain = (ek == 0) | (ek == 1)          # chain + hub spokes shape clusters
    ca, cb = ea[chain], eb[chain]

    is_hub = np.array([nd['kind'] == 'trunk' for nd in nodes])

    for it in range(300):
        diff = pos[:, None, :] - pos[None, :, :]
        d2 = (diff ** 2).sum(-1) + 1e-3
        np.fill_diagonal(d2, np.inf)
        rep = np.where(same, 9000.0, 0.0)            # cluster-internal spacing
        rep = rep + np.where(d2 < 140 ** 2, 5000.0, 0.0)  # border separation
        force = (diff * (rep / d2 ** 1.5)[..., None]).sum(axis=1)

        delta = pos[ca] - pos[cb]
        dist = np.linalg.norm(delta, axis=1) + 1e-6
        f = (0.25 * (dist - 62.0) / dist)[:, None] * delta
        np.subtract.at(force, ca, f)
        np.add.at(force, cb, f)

        force += (anchor - pos) * 0.03               # remember the spiral
        force[is_hub] = 0.0                          # hubs are pinned

        cool = 1 - 0.8 * it / 300
        pos += np.clip(force, -8, 8) * cool

    pos -= pos.mean(axis=0)
    pos *= 1150 / np.abs(pos).max()
    return np.round(pos, 1)


def emit(nodes, edge_list, trunk_names, pos, target, has_page):
    data = {
        'nodes': [[nd['id'], nd['label'], nd['trunk'],
                   1 if nd['kind'] == 'trunk' else 0,
                   1 if nd['adv'] else 0, float(pos[i][0]), float(pos[i][1]),
                   1 if has_page.get(nd['id']) else 0]
                  for i, nd in enumerate(nodes)],
        'edges': [list(e) for e in edge_list],
        'trunks': {t: trunk_names.get(t, t) for t in TRUNKS},
    }
    js = json.dumps(data, separators=(',', ':'))
    src = target.read_text()
    start = src.index('/* === AUTO-GENERATED NETWORK DATA')
    start = src.index('*/', start) + 2
    end = src.index('/* === END AUTO-GENERATED === */')
    target.write_text(src[:start] + '\n  var DATA = ' + js + ';\n  ' + src[end:])


def preview(nodes, edge_list, pos, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='black')
    ax.set_facecolor('black')
    for a, b, k in edge_list:
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]],
                color='white', alpha=(0.28 if k == 3 else 0.10), lw=0.6)
    for i, nd in enumerate(nodes):
        big = nd['kind'] == 'trunk'
        ax.scatter([pos[i][0]], [pos[i][1]], s=(90 if big else 14),
                   facecolors='black', edgecolors='white',
                   linewidths=(1.2 if big else 0.6), zorder=3)
        if big:
            ax.annotate(nd['id'], pos[i], color='white', fontsize=9,
                        ha='center', va='center', xytext=(0, 14),
                        textcoords='offset points')
    ax.set_aspect('equal')
    ax.axis('off')
    fig.savefig(path, dpi=100, facecolor='black', bbox_inches='tight')
    print(f'preview -> {path}')


def main():
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', default=str(here.parent.parent / 'modules' / 'topic_network.txt'))
    ap.add_argument('--target', default=str(here.parent / 'teaching_network.js'))
    ap.add_argument('--modules', default=str(here.parent.parent / 'modules'))
    ap.add_argument('--preview', default=None)
    args = ap.parse_args()

    nodes, edge_list, trunk_names, missing = parse(Path(args.source).read_text())
    pos = layout(nodes, edge_list)

    kinds = {v: k for k, v in EK.items()}
    from collections import Counter
    cnt = Counter(kinds[e[2]] for e in edge_list)
    n_mod = sum(1 for nd in nodes if nd['kind'] == 'module')
    n_hub = len(nodes) - n_mod
    print(f'nodes: {len(nodes)} ({n_mod} modules + {n_hub} trunk hubs)')
    print(f"edges: {len(edge_list)} ({', '.join(f'{k} {v}' for k, v in sorted(cnt.items()))})")
    if missing:
        print(f'WARNING unresolved cross-links: {missing}')

    has_page = module_pages(nodes, args.modules)
    n_pm = sum(1 for nd in nodes if nd['kind'] == 'module' and has_page[nd['id']])
    n_ph = sum(1 for nd in nodes if nd['kind'] == 'trunk' and has_page[nd['id']])
    print(f'module pages: {n_pm} of {n_mod} modules, {n_ph} of {n_hub} hubs '
          f'(from {args.modules})')
    unbuilt = [nd['id'] for nd in nodes if nd['kind'] == 'module' and not has_page[nd['id']]]
    if unbuilt:
        print(f'WARNING modules listed in the network with no folder yet '
              f'(no "open module" link): {unbuilt}')

    if args.preview:
        preview(nodes, edge_list, pos, args.preview)
    emit(nodes, edge_list, trunk_names, pos, Path(args.target), has_page)
    print(f'baked into {args.target}')


if __name__ == '__main__':
    main()
