#!/usr/bin/env python3
"""derive.py -- the Python twin of energy-forms-and-changes.html.

Re-derives the model independently of the JavaScript and prints reference
values (label, two or more spaces, value) to refvals.txt; gen_refs.py turns
that file into p7a_refs.js, which selfTest reads through R(label).  Read the
output IN FULL (Known-bad: a value that never appeared in output you read is
a guess wearing a citation).

  python3 derive.py > refvals.txt

Sources of the model: PhET's build 1.4.24 (docs/phets/energy-forms-and-changes_en.html),
read directly: EFACConstants, HeatTransferConstants, ThermalContactArea,
RectangularThermalMovableModelElement, Beaker, Block, Burner, Air,
EFACIntroModel.stepModel, and on the Systems screen Biker, FaucetAndWater,
SunEnergySource, TeaKettle, Generator, SolarPanel, BeakerHeater, LightBulb,
Fan, SystemsModel.  Every constant below carries the name PhET gives it.
"""
import math
import sys
from fractions import Fraction

import numpy as np
from scipy.linalg import expm

OUT = []


def P(label, value):
    """print one reference line; labels must be unique (gen_refs.py checks)"""
    if isinstance(value, bool):
        value = 1.0 if value else 0.0
    if isinstance(value, int):
        value = float(value)
    OUT.append('%-72s  %s' % (label, repr(float(value))))


def H(title):
    OUT.append('=== ' + title)


def roundsym(v):
    """dot's Utils.roundSymmetric: Math.round(|v|) carrying the sign"""
    a = math.floor(abs(v) + 0.5)
    return -a if v < 0 else a


def linear(a1, a2, b1, b2, a3):
    """dot's Utils.linear"""
    return (b2 - b1) / (a2 - a1) * (a3 - a1) + b1


# ===================================================================
#  PhET's constants
# ===================================================================
T_ROOM = 296.0                       # ROOM_TEMPERATURE
T_FREEZE = 273.15                    # WATER_FREEZING_POINT_TEMPERATURE
T_BOIL = {'water': 373.15, 'oil': 573.15}
T_BLOCK_MAX = 620.0                  # Block.getEnergyBeyondMaxTemperature
MAT = {'iron': (450.0, 7800.0), 'brick': (840.0, 3300.0),
       'water': (3000.0, 1000.0), 'oil': (1411.0, 916.0)}   # (c J/kg/K, rho kg/m^3)
BLOCK = 0.045                        # BLOCK_SURFACE_WIDTH
BEAKER_W = 0.085
BEAKER_H = 0.085 * 1.1
FLUID0 = 0.5                         # INITIAL_FLUID_PROPORTION
DISPLACE = 120.0                     # BeakerContainer.updateFluidDisplacement
K_BODY = 1000.0                      # HeatTransferConstants, any two of iron/brick/water/oil
K_AIR = 30.0                         # ... any of them with the air
MAXSTEP = 1.0 / 60                   # MAX_HEAT_EXCHANGE_TIME_STEP
DT = 1.0 / 60                        # SIM_TIME_PER_TICK_NORMAL
EQ_THRESH = 1e-6                     # TEMPERATURES_EQUAL_THRESHOLD
P_BURN = 5e3                         # Burner.addOrRemoveEnergyToFromObject
P_BURN_AIR = 1500.0                  # Burner.addOrRemoveEnergyToFromAir
BURNER_HALF = 0.0375
BURNER_TOP = 0.075
AIR_W, AIR_H = 0.7, 0.85
AIR_M = 10 * (AIR_W * AIR_H * 0.1)
AIR_E = 1012 * AIR_M * T_ROOM
T_AIR = AIR_E / (1012 * AIR_M)
AIR_AREA = (-AIR_W / 2, 0.0, AIR_W, AIR_H, True)   # PhET's Bounds2(-w/2, 0, w, h): maxX = 0.7, harmless
MAXP = 1e4                           # MAX_ENERGY_PRODUCTION_RATE

# the energy-chunk map: brick at 0 C is 1.25 chunks, at room temperature 2.4
QB = 3300 * math.pow(0.045, 3) * 840 * 273.15
ZB = 3300 * math.pow(0.045, 3) * 840 * 296


def gchunks(E):
    return linear(QB, ZB, 1.25, 2.4, E)


def fchunks(n):
    return linear(1.25, 2.4, QB, ZB, n)


EPC = fchunks(2) - fchunks(1)        # ENERGY_PER_CHUNK


def nchunks(E):
    return max(roundsym(gchunks(E)), 0)


SPACING = (0.568 - 0.085) / (6 - 1)
SPOTS = [roundsym(1e3 * (SPACING * r + (0.0425 - 0.284))) / 1e3 for r in range(6)]


# ===================================================================
#  the bench: bodies, contact, exchange, burners, air
# ===================================================================
class Body:
    def __init__(self, name, kind, mat, mats=None):
        self.name, self.kind, self.mat = name, kind, mat
        c, rho = (mats or MAT)[mat]
        if kind == 'block':
            self.w = BLOCK
            self.h = BLOCK
            self.m = math.pow(BLOCK, 3) * rho
            self.imm = False
        else:
            self.w = BEAKER_W
            self.h = BEAKER_H
            self.m = math.pi * math.pow(self.w / 2, 2) * self.h * FLUID0 * rho
            self.imm = True
        self.c = c
        self.E = self.m * self.c * T_ROOM
        self.f = FLUID0
        self.x = 0.0
        self.y = 0.0

    def temp(self):
        t = self.E / (self.m * self.c)
        if self.kind == 'beaker':
            t = min(t, T_BOIL[self.mat])
        return t

    def min_e(self):
        return T_FREEZE * self.m * self.c

    def beyond(self):
        cap = T_BLOCK_MAX if self.kind == 'block' else T_BOIL[self.mat]
        return max(self.E - cap * self.m * self.c, 0.0)

    def bounds(self):
        return (self.x - self.w / 2, self.y, self.x + self.w / 2, self.y + self.h)

    def area(self):
        if self.kind == 'block':
            b = self.bounds()
            return (b[0], b[1], b[2], b[3], False)
        return (self.x - self.w / 2, self.y, self.x + self.w / 2, self.y + self.h * self.f, True)


def contact_len(a, b):
    """ThermalContactArea.getThermalContactLength, a.getThermalContactLength(b)"""
    ox = max(min(a[2], b[2]) - max(a[0], b[0]), 0.0)
    oy = max(min(a[3], b[3]) - max(a[1], b[1]), 0.0)
    n = 0.0
    if ox > 0 and oy > 0:
        if a[4] or b[4]:
            rx0, rx1 = max(a[0], b[0]), min(a[2], b[2])
            ry0, ry1 = max(a[1], b[1]), min(a[3], b[3])
            rw, rh = rx1 - rx0, ry1 - ry0
            n = 2 * rw + 2 * rh
            if rw != (a[2] - a[0]) and rw != (b[2] - b[0]):
                n -= rh
            if rh != (a[3] - a[1]) and rh != (b[3] - b[1]):
                n -= rw
    elif ox > 0 or oy > 0:
        if ((ox > 0 and abs(a[3] - b[1]) < 0.001) or abs(a[1] - b[3]) < 0.001
                or (oy > 0 and abs(a[2] - b[0]) < 0.001) or abs(a[0] - b[2]) < 0.001):
            n = ox
    return n


def exchange(a, b, dt):
    """a.exchangeEnergyWith(b, dt): returns the energy that went from a to b"""
    tot = 0.0
    L = contact_len(a.area(), b.area())
    if L > 0:
        if abs(b.temp() - a.temp()) > EQ_THRESH:
            nsub = math.floor(dt / MAXSTEP)
            rem = dt - nsub * MAXSTEP
            for o in range(nsub + 1):
                h = MAXSTEP if o < nsub else rem
                q = (b.temp() - a.temp()) * L * K_BODY * h
                b.E -= q
                a.E += q
                tot += -q
    return tot


def air_exchange(b, dt):
    """Air.exchangeEnergyWith(b, dt): returns the energy that went from b to the room"""
    i = 0.0
    L = contact_len(AIR_AREA, b.area())
    if L > 0:
        nsub = math.floor(dt / MAXSTEP)
        rem = dt - nsub * MAXSTEP
        for o in range(nsub + 1):
            h = MAXSTEP if o < nsub else rem
            i += (b.temp() - T_AIR) * L * K_AIR * h
        if i >= 0:
            i = max(i, b.beyond())
        b.E -= i
    return i


def contains(outer, inner):
    return outer[0] <= inner[0] and outer[2] >= inner[2] and outer[1] <= inner[1] and outer[3] >= inner[3]


class Bench:
    """PhET's EFACIntroModel.stepModel at a fixed 1/60 s, with the remake's
    stacks (six spots, burners on spots 2 and 3) and its energy-chunk rule"""

    def __init__(self):
        self.bodies = [Body('iron', 'block', 'iron'), Body('brick', 'block', 'brick'),
                       Body('water', 'beaker', 'water'), Body('oil', 'beaker', 'oil')]
        self.level = [0.0, 0.0]
        self.chains = [[0], [1], [], [], [2], [3]]
        self.layout()
        self.room = 0.0
        self.work = 0.0
        self.t = 0.0
        self.steps = 0
        self.own = [nchunks(b.E) for b in self.bodies]
        self.own0 = list(self.own)
        self.E0 = [b.E for b in self.bodies]
        self.link = {}          # key -> [balance energy a->b, a, b]
        self.moved = {'pair': 0, 'burner': 0, 'air': 0}
        self.corr = {'excess': 0, 'deficit': 0}
        self.maxdev = 0.0

    def layout(self):
        for k in range(6):
            y = BURNER_TOP if k in (2, 3) else 0.0
            prev = None
            for i in self.chains[k]:
                b = self.bodies[i]
                b.x = SPOTS[k]
                if prev is None:
                    b.y = y
                elif prev.kind == 'beaker':
                    b.y = prev.y + 0.001
                else:
                    b.y = prev.y + prev.h
                prev = b

    def place(self, i, k):
        """drop body i (and everything above it) on spot k if the stack allows (PhET's rule)"""
        for ch in self.chains:
            if i in ch:
                j = ch.index(i)
                group = ch[j:]
                del ch[j:]
                break
        gbeaker = any(self.bodies[g].kind == 'beaker' for g in group)
        cbeaker = any(self.bodies[g].kind == 'beaker' for g in self.chains[k])
        assert not (gbeaker and cbeaker), 'a beaker cannot stack on a beaker'
        self.chains[k].extend(group)
        self.layout()

    def burner_contact(self, k, b):
        a = b.area()
        cx = (a[0] + a[2]) / 2
        bx = SPOTS[2 + k]
        return cx > bx - BURNER_HALF and cx < bx + BURNER_HALF and abs(a[1] - BURNER_TOP) < 0.001

    def flow(self, key, a, b, q):
        L = self.link.get(key)
        if L is None:
            L = self.link[key] = [0.0, a, b, False]
        L[0] += q
        L[3] = True

    def step(self):
        B = self.bodies
        dt = DT
        for L in self.link.values():
            L[3] = False
        # 1. fluid displacement, one update per step (PhET)
        for bk in B:
            if bk.kind != 'beaker':
                continue
            fx0 = bk.x - bk.w / 2
            fy0 = bk.y
            fx1 = fx0 + bk.w
            fy1 = fy0 + bk.h * bk.f
            area = 0.0
            for bl in B:
                if bl.kind != 'block':
                    continue
                b = bl.bounds()
                ix0, ix1 = max(b[0], fx0), min(b[2], fx1)
                iy0, iy1 = max(b[1], fy0), min(b[3], fy1)
                if ix1 - ix0 >= 0 and iy1 - iy0 >= 0:
                    area += (ix1 - ix0) * (iy1 - iy0)
            bk.f = min(FLUID0 + DISPLACE * area, 1.0)
        Esum0 = sum(b.E for b in B)
        work = 0.0
        room = 0.0
        # 2. every pair once, in PhET's order (blocks, then beakers)
        for i in range(4):
            for j in range(i + 1, 4):
                q = exchange(B[i], B[j], dt)
                if contact_len(B[i].area(), B[j].area()) > 0:
                    self.flow('p%d%d' % (i, j), i, j, q)
        # 3. burners: into whatever sits on them, else into the room
        for k in range(2):
            lev = self.level[k]
            if any(self.burner_contact(k, b) for b in B):
                for i, b in enumerate(B):
                    if self.burner_contact(k, b):
                        q = 0.0
                        if b.temp() > T_FREEZE:
                            q = P_BURN * lev * dt
                            if lev < 0 and abs(q) > b.E - b.min_e():
                                q = -(b.E - b.min_e())
                        b.E += q
                        work += q
                        self.flow('b%d%d' % (k, i), 'b%d' % k, i, q)
            else:
                q = P_BURN_AIR * lev * dt
                work += q
                room += q
                self.flow('b%dA' % k, 'b%d' % k, 'A', q)
        # 4. the room, for every body not immersed in a beaker
        for i, b in enumerate(B):
            imm = False
            if b.kind == 'block':
                for bk in B:
                    if bk is not b and bk.kind == 'beaker' and contains(bk.area(), b.bounds()):
                        imm = True
            if not imm:
                q = air_exchange(b, dt)
                room += q
                self.flow('a%d' % i, i, 'A', q)
        self.work += work
        self.room += room
        resid = sum(b.E for b in B) - Esum0 + room - work
        self.chunks()
        self.t += dt
        self.steps += 1
        return resid

    # ---- the chunk rule -------------------------------------------------
    def _give(self, src, dst):
        """move one chunk src -> dst (a body index, 'A' the room, 'bK' a burner)"""
        if isinstance(src, int):
            self.own[src] -= 1
        if isinstance(dst, int):
            self.own[dst] += 1

    def chunks(self):
        B = self.bodies
        # (a) PhET's threshold pass: a link carries a chunk when more than one
        #     chunk's worth has crossed it (never a body's last chunk)
        for key in sorted(self.link):
            L = self.link[key]
            if not L[3]:
                continue
            if L[0] > EPC:
                a, b = L[1], L[2]
                if not (isinstance(a, int) and self.own[a] <= 1):
                    self._give(a, b)
                    L[0] -= EPC
                    self.moved['pair' if isinstance(b, int) and isinstance(a, int) else ('air' if 'A' in (a, b) else 'burner')] += 1
            elif L[0] < -EPC:
                a, b = L[2], L[1]
                if not (isinstance(a, int) and self.own[a] <= 1):
                    self._give(a, b)
                    L[0] += EPC
                    self.moved['pair' if isinstance(b, int) and isinstance(a, int) else ('air' if 'A' in (a, b) else 'burner')] += 1
        # (b) the corrective pass: no body more than one chunk from its energy
        for _ in range(8):
            bad = False
            for i in range(4):
                g = gchunks(B[i].E)
                dev = self.own[i] - g
                if dev >= 1 or dev <= -1:
                    bad = True
                    self._correct(i, dev > 0)
            if not bad:
                break
        for i in range(4):
            self.maxdev = max(self.maxdev, abs(self.own[i] - gchunks(B[i].E)))

    def _links_of(self, i):
        out = []
        for key in sorted(self.link):
            L = self.link[key]
            if not L[3]:
                continue
            if L[1] == i:
                out.append((key, L, L[2], L[0]))       # outward balance = +B
            elif L[2] == i:
                out.append((key, L, L[1], -L[0]))      # outward balance = -B
        return out

    def _ok_partner(self, p, receiving):
        if p == 'A':
            return True
        if isinstance(p, str):                        # a burner: heating ones give, cooling ones take
            lev = self.level[int(p[1])]
            return lev < 0 if receiving else lev > 0
        dev = self.own[p] - gchunks(self.bodies[p].E)
        return dev < 0 if receiving else (dev > 0 and self.own[p] > 1)

    def _correct(self, i, excess):
        cands = self._links_of(i)
        best = None
        for key, L, p, outb in cands:
            score = outb if excess else -outb
            if self._ok_partner(p, excess) and (best is None or score > best[0]):
                best = (score, key, L, p)
        if best is None:
            for key, L, p, outb in cands:
                score = outb if excess else -outb
                if best is None or score > best[0]:
                    best = (score, key, L, p)
        _, key, L, p = best
        self.corr['excess' if excess else 'deficit'] += 1
        if excess:
            self._give(i, p)
            if L[1] == i:
                L[0] -= EPC
            else:
                L[0] += EPC
        else:
            self._give(p, i)
            if L[1] == i:
                L[0] += EPC
            else:
                L[0] -= EPC
        kind = 'pair' if isinstance(p, int) else ('air' if p == 'A' else 'burner')
        self.moved[kind] += 1

    def identity(self, i):
        """E_i + S_i - EPC*own_i, which the chunk rule keeps equal to its reset value"""
        S = 0.0
        for key, L in self.link.items():
            if L[1] == i:
                S += L[0]
            elif L[2] == i:
                S -= L[0]
        return self.bodies[i].E + S - EPC * self.own[i]


def run(bench, n):
    worst = 0.0
    tot = 0.0
    for _ in range(n):
        r = bench.step()
        scale = sum(abs(b.E) for b in bench.bodies) + abs(bench.room) + abs(bench.work)
        worst = max(worst, abs(r) / scale)
        tot += r
    return worst, tot


# ===================================================================
#  output
# ===================================================================
H('PhET constants and the chunk map')
P('EPC (J) = Fb(2) - Fb(1)', EPC)
P('EPC direct = (ZB - QB)/1.15', (ZB - QB) / 1.15)
P('QB brick energy at 273.15 K (J)', QB)
P('ZB brick energy at 296 K (J)', ZB)
P('T_AIR (K)', T_AIR)
P('T_AIR - 296', T_AIR - 296)
for k, s in enumerate(SPOTS):
    P('spot %d x (m)' % k, s)
bodies = Bench().bodies
for b in bodies:
    P('mass %s (kg)' % b.name, b.m)
    P('C %s (J/K)' % b.name, b.m * b.c)
    P('E %s at 296 K (J)' % b.name, b.E)
    P('g chunks %s at 296 K' % b.name, gchunks(b.E))
    P('n chunks %s at 296 K' % b.name, nchunks(b.E))
    P('n chunks %s at 273.15 K' % b.name, nchunks(b.min_e()))
    cap = T_BLOCK_MAX if b.kind == 'block' else T_BOIL[b.mat]
    P('n chunks %s at cap %g K' % (b.name, cap), nchunks(cap * b.m * b.c))
# PhET's predistributed configurations carry 6 (iron), 2 (brick), 34 (water),
# 8 (oil) and 20 (the Systems heater's beaker) chunks: an independent check
hb_m = math.pi * math.pow(0.075 / 2, 2) * 0.0825 * FLUID0 * 1000.0
P('heater beaker mass (kg)', hb_m)
P('heater beaker C (J/K)', hb_m * 3000.0)
P('n chunks heater beaker at 296 K', nchunks(hb_m * 3000.0 * T_ROOM))
P('water slices total area (m^2)', sum((1 - (2 * ((i + 1) / 7) - 1) ** 2) * BEAKER_W for i in range(6)) * BEAKER_H * FLUID0)
P('heater slices total area (m^2)', sum((1 - (2 * ((i + 1) / 7) - 1) ** 2) * 0.075 for i in range(6)) * 0.0825 * FLUID0)

H('contact lengths')
iron, brick, water, oil = bodies
bl = lambda x, y: (x - 0.0225, y, x + 0.0225, y + 0.045, False)
bk = lambda x, y, f: (x - 0.0425, y, x + 0.0425, y + BEAKER_H * f, True)
P('L stacked aligned', contact_len(bl(0, 0), bl(0, 0.045)))
P('L stacked offset 0.01', contact_len(bl(0, 0), bl(0.01, 0.045)))
P('L stacked reversed', contact_len(bl(0, 0.045), bl(0, 0)))
P('L side by side', contact_len(bl(0, 0), bl(0.045, 0)))
P('L immersed (block in beaker f=0.743)', contact_len(bl(0.145, 0.001), bk(0.145, 0, 0.743)))
P('L half immersed (block top above fluid f=0.3)', contact_len(bl(0.145, 0.001), bk(0.145, 0, 0.3)))
P('L beaker on block', contact_len(bl(0, 0), bk(0, 0.045, 0.5)))
P('L air around block', contact_len(AIR_AREA, bl(0, 0)))
P('L air around water f=0.5', contact_len(AIR_AREA, bk(0.145, 0, 0.5)))
P('L beaker to beaker side by side', contact_len(bk(0, 0, 0.5), bk(0.085, 0, 0.5)))

H('scenario A: iron on the left burner at full heat, 30 s')
A = Bench()
A.place(0, 2)
A.level = [1.0, 0.0]
wA, tA = run(A, 1800)
for i, b in enumerate(A.bodies):
    P('A E %s (J)' % b.name, b.E)
    P('A T %s (K)' % b.name, b.temp())
    P('A own %s' % b.name, A.own[i])
P('A room (J)', A.room)
P('A work (J)', A.work)
P('A worst step residual / scale', wA)
P('A summed residual (J)', tA)
P('A max |own - g|', A.maxdev)
for i in range(4):
    P('A identity drift %d (J)' % i, A.identity(i) - (A.E0[i] - EPC * A.own0[i]))

H('scenario B: then into the water, burner off, 10 s')
A.level = [0.0, 0.0]
A.place(0, 4)
P('B iron y (m)', A.bodies[0].y)
r1 = A.step()
P('B water fluid proportion after one step', A.bodies[2].f)
wB, tB = run(A, 599)
for i, b in enumerate(A.bodies):
    P('B E %s (J)' % b.name, b.E)
    P('B T %s (K)' % b.name, b.temp())
    P('B own %s' % b.name, A.own[i])
P('B room (J)', A.room)
P('B work (J)', A.work)
P('B water fluid proportion', A.bodies[2].f)
P('B worst step residual / scale', wB)
P('B max |own - g|', A.maxdev)
P('B chunks moved pair', A.moved['pair'])
P('B chunks moved burner', A.moved['burner'])
P('B chunks moved air', A.moved['air'])
for i in range(4):
    P('B identity drift %d (J)' % i, A.identity(i) - (A.E0[i] - EPC * A.own0[i]))

H('scenario C: brick on iron on the right burner, cooling at full, 20 s')
C = Bench()
C.place(0, 3)
C.place(1, 3)
P('C brick y (m)', C.bodies[1].y)
C.level = [0.0, -1.0]
wC, tC = run(C, 1200)
for i, b in enumerate(C.bodies):
    P('C E %s (J)' % b.name, b.E)
    P('C T %s (K)' % b.name, b.temp())
    P('C own %s' % b.name, C.own[i])
P('C room (J)', C.room)
P('C work (J)', C.work)
P('C worst step residual / scale', wC)
P('C max |own - g|', C.maxdev)

H('scenario D: water beaker on the left burner at full heat, 60 s (it boils)')
D = Bench()
D.place(2, 2)
D.level = [1.0, 0.0]
wD, tD = run(D, 3600)
P('D E water (J)', D.bodies[2].E)
P('D T water (K)', D.bodies[2].temp())
P('D E water cap (J)', T_BOIL['water'] * D.bodies[2].m * D.bodies[2].c)
P('D room (J)', D.room)
P('D work (J)', D.work)
P('D own water', D.own[2])
P('D worst step residual / scale', wD)
t_boil = None
D2 = Bench()
D2.place(2, 2)
D2.level = [1.0, 0.0]
for s in range(3600):
    D2.step()
    if t_boil is None and D2.bodies[2].E >= T_BOIL['water'] * D2.bodies[2].m * D2.bodies[2].c:
        t_boil = D2.t
P('D time to reach boiling (s)', t_boil)

H('scenario E: oil beaker on the right burner at full heat, 90 s')
Eb = Bench()
Eb.place(3, 3)
Eb.level = [0.0, 1.0]
wE, _ = run(Eb, 5400)
P('E E oil (J)', Eb.bodies[3].E)
P('E T oil (K)', Eb.bodies[3].temp())
P('E room (J)', Eb.room)
P('E worst step residual / scale', wE)

H('scenario F: iron alone on the left burner at full heat, 120 s (the 620 K cap)')
F = Bench()
F.place(0, 2)
F.level = [1.0, 0.0]
wF, _ = run(F, 7200)
P('F E iron (J)', F.bodies[0].E)
P('F T iron (K)', F.bodies[0].temp())
P('F room (J)', F.room)
P('F own iron', F.own[0])
P('F worst step residual / scale', wF)

H('scenario G: cooling the water on the left burner, 40 s (the 273.15 K clamp)')
G = Bench()
G.place(2, 2)
G.level = [-1.0, 0.0]
wG, _ = run(G, 2400)
P('G E water (J)', G.bodies[2].E)
P('G T water (K)', G.bodies[2].temp())
P('G room (J)', G.room)
P('G work (J)', G.work)
P('G worst step residual / scale', wG)

H('scenario H: an empty burner heats the room; the other cools it')
Hh = Bench()
Hh.level = [0.7, -0.4]
wH, _ = run(Hh, 600)
P('H room (J)', Hh.room)
P('H work (J)', Hh.work)
P('H E iron (J)', Hh.bodies[0].E)

H('scenario I: two blocks in the water beaker (displacement)')
I = Bench()
I.place(0, 4)
I.place(1, 4)
P('I iron y (m)', I.bodies[0].y)
P('I brick y (m)', I.bodies[1].y)
fs = []
for s in range(8):
    I.step()
    fs.append(I.bodies[2].f)
for s, f in enumerate(fs):
    P('I water f after step %d' % (s + 1), f)
run(I, 592)
P('I E iron (J)', I.bodies[0].E)
P('I E brick (J)', I.bodies[1].E)
P('I E water (J)', I.bodies[2].E)

H('scenario J: a hot iron into the water, no burner, stepped against the exact 2x2 solution')


def pair_run(T1, T2, n, air=True, mats=None):
    """iron (hot) immersed in water: the bench's own step, air on or off"""
    J = Bench()
    J.place(0, 4)
    iron_, water_ = J.bodies[0], J.bodies[2]
    iron_.E = iron_.m * iron_.c * T1
    water_.E = water_.m * water_.c * T2
    J.own = [nchunks(b.E) for b in J.bodies]
    J.own0 = list(J.own)
    J.E0 = [b.E for b in J.bodies]
    out = []
    for s in range(n):
        if air:
            J.step()
        else:
            # the same step without stage 4 (an insulated pair)
            for bk2 in J.bodies:
                pass
            B = J.bodies
            fx0 = B[2].x - B[2].w / 2
            area = 0.0
            b = B[0].bounds()
            ix0, ix1 = max(b[0], fx0), min(b[2], fx0 + B[2].w)
            iy0, iy1 = max(b[1], B[2].y), min(b[3], B[2].y + B[2].h * B[2].f)
            if ix1 - ix0 >= 0 and iy1 - iy0 >= 0:
                area += (ix1 - ix0) * (iy1 - iy0)
            B[2].f = min(FLUID0 + DISPLACE * area, 1.0)
            exchange(B[0], B[2], DT)
        out.append((iron_.temp(), water_.temp()))
    return J, out


Cw = water.m * water.c
Ci = iron.m * iron.c
G_imm = K_BODY * contact_len(bl(0.145, 0.001), bk(0.145, 0, 0.743))
P('J G immersed (W/K)', G_imm)
Teq = (Ci * 400.0 + Cw * 296.0) / (Ci + Cw)
tau = 1.0 / (G_imm * (1 / Ci + 1 / Cw))
P('J T_eq iron 400 K in water 296 K (K)', Teq)
P('J tau (s)', tau)
Jn, outn = pair_run(400.0, 296.0, 600, air=False)
P('J stepped no air T iron at 1 s', outn[59][0])
P('J stepped no air T water at 1 s', outn[59][1])
P('J stepped no air T iron at 10 s', outn[599][0])
P('J stepped no air T water at 10 s', outn[599][1])
P('J stepped no air C-weighted mean at 10 s (K)', (Ci * outn[599][0] + Cw * outn[599][1]) / (Ci + Cw))
# the exact solution, insulated
for tt in (1.0, 2.0, 10.0):
    d = (400.0 - 296.0) * math.exp(-tt / tau)
    P('J exact no air T iron at %g s' % tt, Teq + Cw / (Ci + Cw) * d)
    P('J exact no air T water at %g s' % tt, Teq - Ci / (Ci + Cw) * d)
# the discrete map of one exchange step: the difference decays by (1 - G(1/Ci+1/Cw) dt) per step
lam_d = 1 - G_imm * (1 / Ci + 1 / Cw) * DT
P('J discrete factor per step', lam_d)
P('J exact factor per step', math.exp(-DT / tau))
P('J stepped difference at 1 s (K) closed form', (400.0 - 296.0) * lam_d ** 60)
# with the air: the 2x2 linear system (iron immersed: no air of its own)
f_w = 0.743 if False else FLUID0 + DISPLACE * (0.045 * 0.045)
L_wair = contact_len(AIR_AREA, bk(0.145, 0, f_w))
P('J water fluid f with one block', f_w)
P('J L water-air (m)', L_wair)
a2 = K_AIR * L_wair
M = np.array([[-G_imm / Ci, G_imm / Ci], [G_imm / Cw, -(G_imm + a2) / Cw]])
bvec = np.array([0.0, a2 * T_AIR / Cw])
Tss = -np.linalg.solve(M, bvec)
P('J with air steady T iron', Tss[0])
u0 = np.array([400.0, 296.0]) - Tss
for tt in (1.0, 5.0, 30.0, 120.0):
    u = expm(M * tt) @ u0 + Tss
    P('J exact air T iron at %g s' % tt, u[0])
    P('J exact air T water at %g s' % tt, u[1])
Ja, outa = pair_run(400.0, 296.0, 7200, air=True)
for tt in (1.0, 5.0, 30.0, 120.0):
    k = int(round(tt * 60)) - 1
    P('J stepped air T iron at %g s' % tt, outa[k][0])
    P('J stepped air T water at %g s' % tt, outa[k][1])
ev = np.linalg.eigvals(M)
P('J eigenvalue slow (1/s)', max(ev.real))
P('J eigenvalue fast (1/s)', min(ev.real))
# the 2x2 closed form the JS uses: exp(Mt) = e^{st}[cosh(qt) I + sinh(qt)/q (M - sI)]
s_ = (M[0, 0] + M[1, 1]) / 2
det = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
q_ = math.sqrt(s_ * s_ - det)
tt = 5.0
E2 = math.exp(s_ * tt) * (math.cosh(q_ * tt) * np.eye(2) + math.sinh(q_ * tt) / q_ * (M - s_ * np.eye(2)))
P('J closed-form expm vs scipy max abs diff', float(np.max(np.abs(E2 - expm(M * tt)))))

H('equilibrium pairs (the view): conductances and T_eq, PhET and real materials')
# real values, each from its source:
#   water: NIST Chemistry WebBook (IAPWS-95), 22.85 C (296 K), 0.101325 MPa:
#          rho 997.577 kg/m^3, cp 4.18232 J/(g K)
#   iron:  NIST-JANAF Fe(cr) Cp(298.15 K) = 25.094 J/(mol K); M(Fe) = 55.845 g/mol (IUPAC);
#          rho 7.874 g/cm^3 at 20 C (Arblaster 2018, via Wikipedia's infobox)
#   brick: c 0.840 J/(g K) (Wikipedia building-materials table); Engineering ToolBox gives 0.9
#          for common brick; rho 1.4-2.4 g/cm^3 (ToolBox), 1.9 taken as the middle
#   olive oil: c 1.97 kJ/(kg K) (Engineering ToolBox, liquids); sg 0.911 at 20 C (USDA
#          grading manual, via Wikipedia)
REAL = {'iron': (25.094 / 55.845 * 1000.0, 7874.0), 'brick': (840.0, 1900.0),
        'water': (4182.32, 997.577), 'oil': (1970.0, 911.0)}
P('real c iron (J/kg/K) from JANAF', REAL['iron'][0])


def cap_of(mat, kind, real):
    c, rho = (REAL if real else MAT)[mat]
    if kind == 'block':
        m = math.pow(BLOCK, 3) * rho
    else:
        m = math.pi * math.pow(BEAKER_W / 2, 2) * BEAKER_H * FLUID0 * rho
    return m, m * c


# body 1 is always the block that starts hot (the JS pairs' convention)
PAIRS = {'iron-water': ('iron', 'block', 'water', 'beaker', 0.18),
         'brick-water': ('brick', 'block', 'water', 'beaker', 0.18),
         'iron-oil': ('iron', 'block', 'oil', 'beaker', 0.18),
         'brick-iron': ('iron', 'block', 'brick', 'block', 0.045),
         'water-iron': ('iron', 'block', 'water', 'beaker', 0.045)}
for name, (m1, k1, m2, k2, L) in PAIRS.items():
    for real in (False, True):
        tag = 'real' if real else 'PhET'
        _, C1 = cap_of(m1, k1, real)
        _, C2 = cap_of(m2, k2, real)
        G = K_BODY * L
        P('eq %s %s C1 (J/K)' % (name, tag), C1)
        P('eq %s %s C2 (J/K)' % (name, tag), C2)
        P('eq %s %s T_eq from 380 K and 296 K' % (name, tag), (C1 * 380.0 + C2 * 296.0) / (C1 + C2))
        P('eq %s %s tau (s)' % (name, tag), 1.0 / (G * (1 / C1 + 1 / C2)))

# ===================================================================
#  the Systems screen
# ===================================================================
H('Systems: PhET constants and what PhET itself does not close')
OMEGA_MAX = 3 * math.pi
CRANK_ACC = math.pi / 2
FOOD0 = 21 * EPC
BIKE_LOAD = MAXP
BIKE_FREE = MAXP / 5
BIKE_MECH = 5.0 / 6.0
FALL_STEPS = 24                     # FaucetAndWater: 400 ms delay, at 60 steps/s
TAU_K = 10.0                        # TeaKettle: energyProductionRate decays 0.1 per second
STEAM = 0.8                         # TeaKettle: 80 % of the heat chunks become steam
KETTLE_CUT = 30.0
GEN_R = 0.039
TAU_W = 5.0 / 3.0                   # Generator: dw/dt = (r - 3w)/5
ETA_W = (GEN_R * 0.5 * (1 / 60) / 3) * MAXP / (math.pi / 2)
ETA_PANEL = 0.68
HEAT_MAXP = 5e3                     # BeakerHeater: 5000 W x heat proportion into the water
HEAT_RAMP = 0.5
HB_W, HB_H = 0.075, 0.0825
HB_M = math.pi * math.pow(HB_W / 2, 2) * HB_H * FLUID0 * 1000.0
HB_C = HB_M * 3000.0
HB_L = 2 * HB_W + 2 * HB_H * FLUID0
LIGHT = {'incandescent': 0.65, 'fluorescent': 0.8}
FAN_W = 0.0051
FAN_MIN = 4.0
FAN_ACC = 4 * math.pi
P('ETA_W generator on water or steam (PhET at 60 fps)', ETA_W)
P('ETA_W closed form 13/(6 pi)', 13 / (6 * math.pi))


def phet_gen_out_over_in(Pin, fps):
    """PhET's Generator on water or steam, settled: w = min(0.039 x 0.5 x (P dt)/3, pi/2),
    output 10 kW x w/(pi/2); the Systems screen steps once per frame, dt = 1/fps"""
    w = min(GEN_R * 0.5 * (Pin / fps) / 3, math.pi / 2)
    return MAXP * w / (math.pi / 2) / Pin


P('PhET generator out/in at 60 fps, 5 kW', phet_gen_out_over_in(5e3, 60))
P('PhET generator out/in at 30 fps, 5 kW', phet_gen_out_over_in(5e3, 30))
P('PhET generator out/in at 30 fps, 10 kW (at its speed limit)', phet_gen_out_over_in(1e4, 30))
P('PhET teapot steady steam / burner power below the cap', 2000 / 0.1 / MAXP)
P('PhET teapot heat that reaches the 10 kW cap', MAXP * 0.1 / 2000)
P('food store (J) = 21 EPC', FOOD0)
P('biker at full crank, chemical power with a load (W)', BIKE_LOAD)
P('biker time to empty at full crank from rest (s) approx', 21 * EPC / BIKE_LOAD + OMEGA_MAX / CRANK_ACC / 2)
P('heater beaker L to air (m)', HB_L)
P('heater beaker loss at 373.15 K (W)', (373.15 - T_ROOM) * K_AIR * HB_L)


def phet_fan_fraction(Pin, nsteps=200000):
    """PhET's Fan: an arriving electrical chunk goes to the air (mechanical)
    while internalTemperature < 38 (it then rises 1.5), else it radiates as
    heat and the temperature resets to 22; the temperature falls 0.5/s to 22"""
    T = 22.0
    acc = 0.0
    th = 0
    tot = 0
    for s in range(nsteps):
        acc += Pin * DT
        if acc >= EPC:
            acc -= EPC
            tot += 1
            if T < 38:
                T += 1.5
            else:
                th += 1
                T = 22.0
        T = max(T - 0.5 * DT, 22.0)
    return th / tot, tot


for Pin in (1e4, 5e3, 2e3, 1e3):
    fr, tot = phet_fan_fraction(Pin)
    P('PhET fan thermal chunk fraction at %g W' % Pin, fr)
FAN_HEAT = 1.0 / 14.0
P('FAN_HEAT used (1/14)', FAN_HEAT)


def sun_frac(c):
    i = 1 - c
    return 0.0 if i == 0 else 0.1 + 0.9 * i


for c in (0.0, 0.25, 0.5, 0.99, 1.0):
    P('sun fraction through clouds %g' % c, sun_frac(c))

CHANNELS = ['b.chem', 'b.mech', 'b.heat', 'f.water', 's.light', 's.refl', 't.flame', 't.loss', 't.steam',
            'g.elec', 'g.heat', 'p.elec', 'p.heat', 'h.coil', 'h.loss', 'h.water', 'l.light', 'l.heat',
            'n.wind', 'n.heat', 'x.miss']


class Systems:
    """the remake's ledger model of the Systems screen at a fixed 1/60 s"""

    def __init__(self, src, conv, user):
        self.src, self.conv, self.user = src, conv, user
        self.omega = 0.0
        self.target = 0.0
        self.food = FOOD0
        self.flow_ = 0.0
        self.clouds = 0.0
        self.heat = 0.0
        self.fall = [0.0] * FALL_STEPS
        self.kettle = 0.0
        self.wheel = 0.0
        self.hp = 0.0
        self.water = HB_C * T_ROOM
        self.water0 = self.water
        self.fan = 0.0
        self.acc = {c: 0.0 for c in CHANNELS}
        self.count = {c: 0 for c in CHANNELS}
        self.chsum = {c: 0.0 for c in CHANNELS}
        self.inp = {'fed': 0.0, 'main': 0.0, 'sun': 0.0, 'gas': 0.0}
        self.sink = {'light': 0.0, 'wind': 0.0, 'room': 0.0, 'reflected': 0.0, 'escaped': 0.0}
        self.worst = 0.0
        self.t = 0.0
        self.stores0 = self.stores()

    def stores(self):
        return self.food + sum(self.fall) + self.kettle + self.wheel + (self.water - self.water0)

    def ch(self, c, E):
        self.chsum[c] += E
        self.acc[c] += E
        while self.acc[c] >= EPC:
            self.acc[c] -= EPC
            self.count[c] += 1

    def check(self, *terms):
        """in - out - loss - dstore = 0 for one element"""
        s = 0.0
        sc = 0.0
        for t in terms:
            s += t
            sc += abs(t)
        if sc > 0:
            self.worst = max(self.worst, abs(s) / sc)

    def step(self):
        dt = DT
        form = None
        Eout = 0.0
        # ---------------- the source
        if self.src == 'biker':
            tgt = self.target if self.food > 0 else 0.0
            d = tgt - self.omega
            if d != 0:
                r = CRANK_ACC * dt
                self.omega = min(self.omega + r, self.target) if d > 0 else max(self.omega - r, 0.0)
            load = self.conv == 'generator'
            pchem = (BIKE_LOAD if load else BIKE_FREE) * self.omega / OMEGA_MAX
            Ec = min(pchem * dt, self.food)
            self.food -= Ec
            Em = BIKE_MECH * Ec if load else 0.0
            Eh = Ec - Em
            self.sink['room'] += Eh
            self.check(Ec, -Em, -Eh)
            self.ch('b.chem', Ec)
            self.ch('b.mech', Em)
            self.ch('b.heat', Eh)
            form, Eout = 'mechanical', Em
        elif self.src == 'faucet':
            Ein = MAXP * self.flow_ * dt
            self.inp['main'] += Ein
            self.fall.append(Ein)
            Eout = self.fall.pop(0)
            self.check(Ein, -Eout, -(Ein - Eout))    # the falling water is the store
            self.ch('f.water', Ein)
            form = 'mechanical'
        elif self.src == 'sun':
            Ein = MAXP * dt
            Et = MAXP * sun_frac(self.clouds) * dt
            Er = Ein - Et
            self.inp['sun'] += Ein
            self.sink['reflected'] += Er
            self.check(Ein, -Et, -Er)
            self.ch('s.light', Et)
            self.ch('s.refl', Er)
            form, Eout = 'light', Et
        else:
            Ein = MAXP * self.heat * dt
            self.inp['gas'] += Ein
            Ek = STEAM * Ein
            El = Ein - Ek
            self.kettle += Ek
            Es = self.kettle * dt / TAU_K
            if self.heat == 0 and Es / dt < KETTLE_CUT:
                El += self.kettle
                self.kettle = 0.0
                Es = 0.0
            else:
                self.kettle -= Es
            self.sink['room'] += El
            self.ch('t.flame', Ein)
            self.ch('t.loss', El)
            self.ch('t.steam', Es)
            form, Eout = 'mechanical', Es
        # ---------------- the converter
        Ee = 0.0
        if self.conv == 'generator' and form == 'mechanical':
            if self.src == 'biker':
                Ee = Eout
                self.check(Eout, -Ee)
            else:
                self.wheel += Eout
                Er = self.wheel * dt / TAU_W
                self.wheel -= Er
                Ee = ETA_W * Er
                Eh = Er - Ee
                self.sink['room'] += Eh
                self.ch('g.heat', Eh)
            self.ch('g.elec', Ee)
        elif self.conv == 'panel' and form == 'light':
            Ee = ETA_PANEL * Eout
            Eh = Eout - Ee
            self.sink['room'] += Eh
            self.check(Eout, -Ee, -Eh)
            self.ch('p.elec', Ee)
            self.ch('p.heat', Eh)
        else:
            self.sink['escaped'] += Eout
            self.ch('x.miss', Eout)
        # ---------------- the user
        if self.user == 'heater':
            r = (Ee / dt) / MAXP
            self.hp = min(r, self.hp + HEAT_RAMP * dt)
            Ew = HEAT_MAXP * self.hp * dt
            El = Ee - Ew
            self.water += Ew
            T = min(self.water / HB_C, 373.15)
            s = T - T_ROOM
            Ea = 0.0
            if abs(s) > EQ_THRESH:
                Ea = s * K_AIR * HB_L * dt
                self.water -= Ea
            Eb = max(self.water - 373.15 * HB_C, 0.0)
            self.water -= Eb
            self.sink['room'] += El + Ea + Eb
            self.ch('h.coil', Ew)
            self.ch('h.loss', El)
            self.ch('h.water', Ea + Eb)
        elif self.user in LIGHT:
            El = LIGHT[self.user] * Ee
            Eh = Ee - El
            self.sink['light'] += El
            self.sink['room'] += Eh
            self.ch('l.light', El)
            self.ch('l.heat', Eh)
        else:
            Eh = FAN_HEAT * Ee
            Ew = Ee - Eh
            self.sink['wind'] += Ew
            self.sink['room'] += Eh
            self.ch('n.wind', Ew)
            self.ch('n.heat', Eh)
            tgt = FAN_W * Ee / dt
            tgt = 0.0 if tgt < FAN_MIN else tgt
            d = tgt - self.fan
            if d != 0:
                self.fan = min(self.fan + FAN_ACC * dt, tgt) if d > 0 else max(self.fan - FAN_ACC * dt, 0.0)
        self.t += dt

    def closure(self):
        return sum(self.inp.values()) - sum(self.sink.values()) - (self.stores() - self.stores0)

    def balance(self):
        IN = self.inp['main'] + self.inp['sun'] + self.inp['gas'] + self.chsum['b.chem']
        OUT = self.sink['light'] + self.sink['wind']
        LOST = self.sink['room'] + self.sink['reflected'] + self.sink['escaped']
        STORED = sum(self.fall) + self.kettle + self.wheel + (self.water - self.water0)
        return IN, OUT, LOST, STORED


def sys_run(src, conv, user, n, **ctl):
    S = Systems(src, conv, user)
    S.target = ctl.get('target', 0.0)
    S.flow_ = ctl.get('flow', 0.0)
    S.clouds = ctl.get('clouds', 0.0)
    S.heat = ctl.get('heat', 0.0)
    worst = 0.0
    for _ in range(n):
        S.step()
        scale = sum(S.inp.values()) + abs(S.stores0)
        worst = max(worst, abs(S.closure()) / scale)
    return S, worst


def sys_print(tag, S, worst):
    P('%s time (s)' % tag, S.t)
    for k in ('fed', 'main', 'sun', 'gas'):
        if S.inp[k]:
            P('%s input %s (J)' % (tag, k), S.inp[k])
    for k, v in S.sink.items():
        P('%s sink %s (J)' % (tag, k), v)
    P('%s store food (J)' % tag, S.food)
    P('%s store fall (J)' % tag, sum(S.fall))
    P('%s store kettle (J)' % tag, S.kettle)
    P('%s store wheel (J)' % tag, S.wheel)
    P('%s store water above start (J)' % tag, S.water - S.water0)
    P('%s water T (K)' % tag, min(S.water / HB_C, 373.15))
    P('%s worst closure / input' % tag, worst)
    IN, OUT, LOST, STORED = S.balance()
    P('%s balance IN (J)' % tag, IN)
    P('%s balance OUT (J)' % tag, OUT)
    P('%s balance LOST (J)' % tag, LOST)
    P('%s balance STORED (J)' % tag, STORED)
    P('%s balance residual (J)' % tag, IN - OUT - LOST - STORED)
    P('%s food chunks shown' % tag, math.ceil(S.food / EPC - 1e-9))
    P('%s worst element residual' % tag, S.worst)
    for c in CHANNELS:
        if S.chsum[c]:
            P('%s channel %s sum (J)' % (tag, c), S.chsum[c])
            P('%s channel %s chunks' % (tag, c), S.count[c])


H('S1: faucet full, generator, beaker heater, 30 s')
S, w = sys_run('faucet', 'generator', 'heater', 1800, flow=1.0)
sys_print('S1', S, w)
P('S1 heater proportion', S.hp)
H('S2: sun half clouds, solar panel, incandescent bulb, 10 s')
S, w = sys_run('sun', 'panel', 'incandescent', 600, clouds=0.5)
sys_print('S2', S, w)
H('S3: teapot full heat, generator, fan, 40 s')
S, w = sys_run('teapot', 'generator', 'fan', 2400, heat=1.0)
sys_print('S3', S, w)
P('S3 fan omega (rad/s)', S.fan)
H('S4: biker full crank, generator, fluorescent bulb, 20 s')
S, w = sys_run('biker', 'generator', 'fluorescent', 1200, target=OMEGA_MAX)
sys_print('S4', S, w)
P('S4 crank omega (rad/s)', S.omega)
H('S5: biker full crank, solar panel (no load), incandescent bulb, 10 s')
S, w = sys_run('biker', 'panel', 'incandescent', 600, target=OMEGA_MAX)
sys_print('S5', S, w)
H('S6: sun on the generator (not captured), fan, 5 s')
S, w = sys_run('sun', 'generator', 'fan', 300, clouds=0.0)
sys_print('S6', S, w)
H('S7: biker until the food runs out (60 s at full crank, generator, heater)')
S, w = sys_run('biker', 'generator', 'heater', 3600, target=OMEGA_MAX)
sys_print('S7', S, w)
P('S7 crank omega (rad/s)', S.omega)
t_empty = None
S2 = Systems('biker', 'generator', 'heater')
S2.target = OMEGA_MAX
for s in range(3600):
    S2.step()
    if t_empty is None and S2.food <= 0:
        t_empty = S2.t
P('S7 time the food runs out (s)', t_empty)
H('S8: teapot at 0.3 heat, 60 s, generator, incandescent')
S, w = sys_run('teapot', 'generator', 'incandescent', 3600, heat=0.3)
sys_print('S8', S, w)
P('S8 steam power now (W)', S.kettle / TAU_K)
P('S8 steam power steady (W) 0.8 x 3000', STEAM * 3000.0)
H('S9: faucet on for 10 s, then off for 10 s (the wheel and the falling water empty)')
S = Systems('faucet', 'generator', 'fan')
S.flow_ = 1.0
for s in range(600):
    S.step()
P('S9 wheel store at 10 s (J)', S.wheel)
P('S9 fall store at 10 s (J)', sum(S.fall))
S.flow_ = 0.0
for s in range(600):
    S.step()
P('S9 wheel store at 20 s (J)', S.wheel)
P('S9 fall store at 20 s (J)', sum(S.fall))
P('S9 closure at 20 s (J)', S.closure())
P('S9 wind (J)', S.sink['wind'])
P('S9 room (J)', S.sink['room'])
P('S9 wheel steady store at full flow (J) = P tau', MAXP * TAU_W)


# ===================================================================
#  the equilibrium view's own run (the twin of eqRun: two bodies at spot 4)
# ===================================================================
H('equilibrium view: eqRun twin')
EQP = {'iron-water': (0, 2, 'in'), 'brick-water': (1, 2, 'in'), 'iron-oil': (0, 3, 'in'),
       'brick-iron': (0, 1, 'on'), 'water-iron': (0, 2, 'under')}
DEFS = [('iron', 'block', 'iron'), ('brick', 'block', 'brick'), ('water', 'beaker', 'water'), ('oil', 'beaker', 'oil')]


def eq_bodies(pair, T1, T2, mats):
    b1, b2, how = EQP[pair]
    M = REAL if mats == 'real' else MAT
    a = Body(*DEFS[b1], mats=M)
    b = Body(*DEFS[b2], mats=M)
    a.x = SPOTS[4]
    b.x = SPOTS[4]
    if how == 'in':
        b.y = 0.0
        a.y = 0.001
    else:
        a.y = 0.0
        b.y = BLOCK
    a.E = a.m * a.c * T1
    b.E = b.m * b.c * T2
    return a, b


def eq_imm(x, other):
    return x.kind == 'block' and other.kind == 'beaker' and contains(other.area(), x.bounds())


def eq_step(a, b, air):
    if b.kind == 'beaker':
        fx0 = b.x - b.w / 2
        fx1 = fx0 + b.w
        fy0 = b.y
        fy1 = fy0 + b.h * b.f
        bb = a.bounds()
        ix0, ix1 = max(bb[0], fx0), min(bb[2], fx1)
        iy0, iy1 = max(bb[1], fy0), min(bb[3], fy1)
        area = (ix1 - ix0) * (iy1 - iy0) if (ix1 - ix0 >= 0 and iy1 - iy0 >= 0) else 0.0
        b.f = min(FLUID0 + DISPLACE * area, 1.0)
    exchange(a, b, DT)
    room = 0.0
    if air:
        if not eq_imm(a, b):
            room += air_exchange(a, DT)
        if not eq_imm(b, a):
            room += air_exchange(b, DT)
    return room


def eq_linear(pair, T1, T2, mats, air):
    a, b = eq_bodies(pair, T1, T2, mats)
    if b.kind == 'beaker' and EQP[pair][2] == 'in':
        b.f = min(FLUID0 + DISPLACE * BLOCK * BLOCK, 1.0)
    G = K_BODY * contact_len(a.area(), b.area())
    imm = eq_imm(a, b)
    a1 = K_AIR * contact_len(AIR_AREA, a.area()) if (air and not imm) else 0.0
    a2 = K_AIR * contact_len(AIR_AREA, b.area()) if air else 0.0
    C1, C2 = a.m * a.c, b.m * b.c
    Mm = np.array([[-(G + a1) / C1, G / C1], [G / C2, -(G + a2) / C2]])
    Teq = (C1 * T1 + C2 * T2) / (C1 + C2)
    Tss = np.array([T_AIR, T_AIR]) if (a1 + a2) > 0 else np.array([Teq, Teq])
    return dict(G=G, a1=a1, a2=a2, C1=C1, C2=C2, M=Mm, Teq=Teq, Tss=Tss, tau=1 / (G * (1 / C1 + 1 / C2)),
                cap1=(T_BLOCK_MAX if a.kind == 'block' else T_BOIL[a.mat]),
                cap2=(T_BLOCK_MAX if b.kind == 'block' else T_BOIL[b.mat]))


def eq_window(L):
    ev = np.linalg.eigvals(L['M']).real
    fast = -1 / min(ev)
    return min(max(8 * fast, 4.0), 60.0)


def eq_run(pair, T1, T2, mats, air):
    L = eq_linear(pair, T1, T2, mats, air)
    win = eq_window(L)
    n = max(2, int(math.floor(win / DT + 0.5)))
    a, b = eq_bodies(pair, T1, T2, mats)
    u0 = np.array([T1, T2]) - L['Tss']
    tcap = None
    room = 0.0
    E0 = a.E + b.E
    dmax = 0.0
    last = None
    for k in range(1, n + 1):
        room += eq_step(a, b, air)
        x = expm(L['M'] * (k * DT)) @ u0 + L['Tss']
        if tcap is None and (a.E / (a.m * a.c) >= L['cap1'] - 1e-9 or b.E / (b.m * b.c) >= L['cap2'] - 1e-9
                             or a.beyond() > 0 or b.beyond() > 0):
            tcap = k * DT
        if tcap is None:
            dmax = max(dmax, abs(a.temp() - x[0]), abs(b.temp() - x[1]))
        last = (a.temp(), b.temp(), x[0], x[1])
    return dict(L=L, win=win, n=n, tcap=tcap, dmax=dmax, resid=a.E + b.E - E0 + room, room=room, last=last)


for pair in EQP:
    for mats in ('phet', 'real'):
        R = eq_run(pair, 380.0, 296.0, mats, True)
        tag = 'eqrun %s %s air' % (pair, mats)
        P(tag + ' window (s)', R['win'])
        P(tag + ' steps', R['n'])
        P(tag + ' G (W/K)', R['L']['G'])
        P(tag + ' a1 (W/K)', R['L']['a1'])
        P(tag + ' a2 (W/K)', R['L']['a2'])
        P(tag + ' T1 stepped end', R['last'][0])
        P(tag + ' T2 stepped end', R['last'][1])
        P(tag + ' T1 exact end', R['last'][2])
        P(tag + ' T2 exact end', R['last'][3])
        P(tag + ' max gap (K)', R['dmax'])
        P(tag + ' capped', 0.0 if R['tcap'] is None else 1.0)
R = eq_run('iron-water', 380.0, 296.0, 'phet', False)
P('eqrun iron-water phet insulated T1 stepped end', R['last'][0])
P('eqrun iron-water phet insulated T2 stepped end', R['last'][1])
P('eqrun iron-water phet insulated T1 exact end', R['last'][2])
P('eqrun iron-water phet insulated max gap (K)', R['dmax'])
P('eqrun iron-water phet insulated resid (J)', R['resid'])
worst_gap = 0.0
for pair in EQP:
    for mats in ('phet', 'real'):
        for air in (True, False):
            R = eq_run(pair, 620.0, 273.15, mats, air)
            worst_gap = max(worst_gap, R['dmax'])
P('eqrun worst gap over every pair at 620 K / 273.15 K (K)', worst_gap)
R = eq_run('iron-water', 620.0, 273.15, 'phet', True)
P('eqrun iron-water phet 620 into 273.15 capped', 0.0 if R['tcap'] is None else 1.0)
R = eq_run('iron-water', 620.0, 296.0, 'phet', True)
P('eqrun iron-water phet 620 into 296 cap time (s)', R['tcap'] if R['tcap'] is not None else -1.0)
P('eqrun iron-water phet 620 into 296 max gap before the cap (K)', R['dmax'])

H('claims the prose makes, measured')
A2 = Bench()
A2.place(0, 2)
A2.level = [1.0, 0.0]
t300 = None
while A2.t < 40:
    A2.step()
    if t300 is None and A2.bodies[0].temp() >= 573.15:
        t300 = A2.t
P('the iron on a full burner passes 300 C at (s)', t300)
Hp = Bench()
Hp.place(0, 4)
Hp.bodies[0].E = Hp.bodies[0].m * Hp.bodies[0].c * 500.0
Hp.own = [nchunks(b.E) for b in Hp.bodies]
Hp.own0 = list(Hp.own)
Hp.E0 = [b.E for b in Hp.bodies]
for k in range(180):
    Hp.step()
P('hot preset T iron at 3 s', Hp.bodies[0].temp())
P('hot preset T water at 3 s', Hp.bodies[2].temp())
for k in range(3420):
    Hp.step()
P('hot preset T iron at 60 s', Hp.bodies[0].temp())
P('hot preset T water at 60 s', Hp.bodies[2].temp())
P('hot preset own iron at 60 s', Hp.own[0])
P('hot preset own water at 60 s', Hp.own[2])
P('hot preset max |own - g|', Hp.maxdev)
P('real water C / PhET water C', REAL['water'][0] * REAL['water'][1] / (MAT['water'][0] * MAT['water'][1]))
P('real brick mass / PhET brick mass', REAL['brick'][1] / MAT['brick'][1])


H('paths the scenarios never reach, pinned directly')
# PhET's substeps: one exchange over 3/60 s is three 1/60-s steps, temperatures updated between
a = Body('iron', 'block', 'iron')
b = Body('water', 'beaker', 'water')
a.x = SPOTS[4]
b.x = SPOTS[4]
a.y = 0.001
b.f = FLUID0 + DISPLACE * BLOCK * BLOCK
a.E = a.m * a.c * 450.0
q = exchange(a, b, 3.0 / 60)
P('substep exchange 3/60 s: E iron (J)', a.E)
P('substep exchange 3/60 s: E water (J)', b.E)
P('substep exchange 3/60 s: energy iron -> water (J)', q)
a2 = Body('iron', 'block', 'iron')
b2 = Body('water', 'beaker', 'water')
a2.x = SPOTS[4]
b2.x = SPOTS[4]
a2.y = 0.001
b2.f = b.f
a2.E = a2.m * a2.c * 450.0
q2 = exchange(a2, b2, 0.05 / 1.0)
P('substep exchange 0.05 s: E iron (J)', a2.E)
# a block straddling a beaker wall (half in the liquid)
P('L straddling the wall', contact_len((0.145 - 0.0425 - 0.0225, 0.001, 0.145 - 0.0425 + 0.0225, 0.046, False),
                                       (0.145 - 0.0425, 0.0, 0.145 + 0.0425, BEAKER_H * 0.743, True)))
# the teapot switched off: the steam dies away, then PhET's 30-W cut empties the kettle
S = Systems('teapot', 'generator', 'fan')
S.heat = 1.0
for k in range(1200):
    S.step()
P('S10 kettle store when the burner goes off (J)', S.kettle)
S.heat = 0.0
tcut = None
for k in range(4800):
    S.step()
    if tcut is None and S.kettle == 0.0:
        tcut = S.t
P('S10 time the 30-W cut empties the kettle (s)', tcut)
P('S10 room at 100 s (J)', S.sink['room'])
P('S10 wind at 100 s (J)', S.sink['wind'])
# the fan's spin-up, mid-ramp: the faucet on a generator and fan, at 2 s
S = Systems('faucet', 'generator', 'fan')
S.flow_ = 1.0
for k in range(120):
    S.step()
P('S9 fan omega at 2 s (rad/s)', S.fan)
# the equal-temperature threshold: 30 s of an insulated iron in water stops the
# exchange once the two are within 1e-6 K
R30 = None
a, b = eq_bodies('iron-water', 380.0, 296.0, 'phet')
for k in range(1800):
    eq_step(a, b, False)
P('insulated 30 s: T iron - T water (K)', a.temp() - b.temp())


H('the corrective pass, both ways: a hot iron under the brick, in the open')
K = Bench()
K.place(1, 0)
K.bodies[0].E = K.bodies[0].m * K.bodies[0].c * 500.0
K.own = [nchunks(b.E) for b in K.bodies]
K.own0 = list(K.own)
K.E0 = [b.E for b in K.bodies]
wK, _ = run(K, 3600)
for i, b in enumerate(K.bodies):
    P('K E %s (J)' % b.name, b.E)
    P('K own %s' % b.name, K.own[i])
P('K corrections excess', K.corr['excess'])
P('K corrections deficit', K.corr['deficit'])
P('K max |own - g|', K.maxdev)
P('K room (J)', K.room)

H('the heater ramp binds when it is switched into a running chain')
S = Systems('faucet', 'generator', 'incandescent')
S.flow_ = 1.0
for k in range(600):
    S.step()
S.user = 'heater'
for k in range(30):
    S.step()
P('S11 heater proportion 0.5 s after the swap', S.hp)
P('S11 water above start 0.5 s after the swap (J)', S.water - S.water0)

sys.stdout.write('\n'.join(OUT) + '\n')
