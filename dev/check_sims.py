#!/usr/bin/env python3
"""check_sims.py — an INDEPENDENT check of what sync_sims.py did (it shares no
code with it).  Run from anywhere:  python3 dev/check_sims.py

Asserts: the copied set equals the source set; every copy is byte-equal to
its source apart from exactly the two documented nav-href rewrites; no
un-rewritten ../website/ or ../modules/ href survives; every copy keeps its
../index.html and ../../modules/ nav targets; the cards on simulations.html
are a bijection onto the copies with no duplicates; the page is tag-balanced;
and the lede/meta count matches the number of cards.
"""
import io, os, re, sys
from html.parser import HTMLParser

here = os.path.dirname(os.path.abspath(__file__))
site = os.path.dirname(here)
src = os.path.join(os.path.dirname(site), 'simulations')
dst = os.path.join(site, 'simulations')
WORDS = {49: 'Forty-nine', 55: 'Fifty-five', 56: 'Fifty-six', 57: 'Fifty-seven',
         58: 'Fifty-eight', 59: 'Fifty-nine', 60: 'Sixty'}

sims = sorted(f for f in os.listdir(src) if f.endswith('.html'))
copies = sorted(f for f in os.listdir(dst) if f.endswith('.html'))
problems = []
if sims != copies:
    problems.append('copied set != source set: %s' % sorted(set(sims) ^ set(copies)))
for f in sorted(set(sims) & set(copies)):
    a = io.open(os.path.join(src, f), 'rb').read()
    b = io.open(os.path.join(dst, f), 'rb').read()
    exp = a.replace(b'href="../website/', b'href="../').replace(b'href="../modules/', b'href="../../modules/')
    if exp != b:
        problems.append('%s differs from source beyond the two rewrites' % f)
    if b'href="../website/' in b or b'href="../modules/' in b:
        problems.append('%s still carries an un-rewritten href' % f)
    if b'href="../index.html"' not in b or b'href="../../modules/teaching_modules.html"' not in b:
        problems.append('%s lost a nav target' % f)

page = io.open(os.path.join(site, 'simulations.html'), encoding='utf-8').read()
hrefs = re.findall(r'href="simulations/([^"]+\.html)"', page)
if len(hrefs) != len(set(hrefs)):
    problems.append('duplicate cards: %s' % sorted(h for h in set(hrefs) if hrefs.count(h) > 1))
if set(hrefs) != set(sims):
    problems.append('cards vs sims: %s' % sorted(set(hrefs) ^ set(sims)))

class Bal(HTMLParser):
    VOID = {'meta', 'link', 'br', 'img', 'hr', 'input'}
    def __init__(self):
        super().__init__(); self.stack = []; self.err = 0
    def handle_starttag(self, t, a):
        if t not in self.VOID: self.stack.append(t)
    def handle_endtag(self, t):
        if not self.stack or self.stack.pop() != t: self.err += 1
b = Bal(); b.feed(page)
if b.err or b.stack:
    problems.append('simulations.html tag balance: %d errors, open %s' % (b.err, b.stack))
n = len(set(hrefs))
word = WORDS.get(n)
if word is None or ('%s of them' % word) not in page or ('content="%d interactive' % n) not in page:
    problems.append('lede/meta count does not say %d (%s)' % (n, word))

print('%d sims, %d copies, %d cards' % (len(sims), len(copies), len(hrefs)))
for p in problems:
    print('PROBLEM:', p)
print('%d problems' % len(problems))
sys.exit(1 if problems else 0)
