#!/usr/bin/env python3
"""derive.py -- the Python twin of quantum-measurement.html's engine.

Re-derives every closed form the sim uses and prints reference values (repr,
17 significant digits) for selfTest to assert.  Run it, redirect to
refvals.txt, and READ THE FILE IN FULL (never through head/tail).

    python3 derive.py > refvals.txt

Independent routes, so the pins are not a same-file self-consistency check:
  * the PRNG (mulberry32) is re-implemented with explicit 32-bit arithmetic;
    the JS must reproduce its draws bit for bit;
  * the binomial pmf is scipy.stats.binom, and the sim's Stirling lnFact is
    checked against math.lgamma;
  * Stern-Gerlach sequences are products of 2x2 complex projectors (numpy),
    not the (1 + r.n)/2 formula the sim uses;
  * Larmor precession is scipy.linalg.expm of the Hamiltonian acting on the
    ket, read back as a Bloch vector, not a rotation matrix;
  * chi-square quantiles are scipy.stats.chi2.ppf.
"""
import math, cmath
import numpy as np
from scipy import stats
from scipy.linalg import expm

M32 = 0xFFFFFFFF


def P(name, val):
    print('%s = %r' % (name, val))


# --------------------------------------------------------------------------
#  the PRNG: mulberry32, mirrored bit for bit from the JS
#    R.s=(R.s+0x6D2B79F5)|0; t=imul(s^(s>>>15),1|s); t=(t+imul(t^(t>>>7),61|t))^t;
#    return ((t^(t>>>14))>>>0)/4294967296
# --------------------------------------------------------------------------
def imul(a, b):
    return (a * b) & M32


class Rng:
    def __init__(self, seed):
        self.s = seed & M32

    def next(self):
        self.s = (self.s + 0x6D2B79F5) & M32
        a = self.s
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & M32) ^ t
        return ((t ^ (t >> 14)) & M32) / 4294967296.0


# --------------------------------------------------------------------------
#  lnFact exactly as the JS writes it (a 0..30 table of summed logs, Stirling
#  with four correction terms above), and the pmf built from it
# --------------------------------------------------------------------------
LNF = [0.0]
_s = 0.0
for _i in range(1, 31):
    _s += math.log(_i)
    LNF.append(_s)


def lnFact(n):
    if n <= 30:
        return LNF[n]
    x = float(n)
    return (x * math.log(x) - x + 0.5 * math.log(2 * math.pi * x)
            + 1 / (12 * x) - 1 / (360 * x ** 3) + 1 / (1260 * x ** 5) - 1 / (1680 * x ** 7))


def binomPmf(N, k, p):
    if k < 0 or k > N:
        return 0.0
    if p <= 0:
        return 1.0 if k == 0 else 0.0
    if p >= 1:
        return 1.0 if k == N else 0.0
    return math.exp(lnFact(N) - lnFact(k) - lnFact(N - k) + k * math.log(p) + (N - k) * math.log1p(-p))


def chi2Binned(obs, N, p, M):
    """merge k = 0..N left to right until the expected count reaches 5;
    a short tail joins the last bin.  Returns (chi2, dof, nbins)."""
    bins = []
    co, ce = 0.0, 0.0
    for k in range(N + 1):
        co += obs[k]
        ce += M * binomPmf(N, k, p)
        if ce >= 5:
            bins.append([co, ce])
            co, ce = 0.0, 0.0
    if (ce > 0 or co > 0) and bins:
        bins[-1][0] += co
        bins[-1][1] += ce
    chi = 0.0
    for o, e in bins:
        chi += (o - e) * (o - e) / e
    return chi, len(bins) - 1, len(bins)


def coinSet(R, N, p):
    k = 0
    for _ in range(N):
        if R.next() < p:
            k += 1
    return k


def repeats(seed, N, p, M):
    R = Rng(seed)
    ks = [coinSet(R, N, p) for _ in range(M)]
    obs = [0] * (N + 1)
    for k in ks:
        obs[k] += 1
    mean = sum(ks) / M
    var = sum((k - mean) ** 2 for k in ks) / (M - 1)
    chi, dof, nb = chi2Binned(obs, N, p, M)
    return ks, obs, mean, var, chi, dof


# --------------------------------------------------------------------------
#  qubit algebra (independent: numpy complex matrices)
# --------------------------------------------------------------------------
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def ket(th, ph):
    return np.array([math.cos(th / 2), cmath.exp(1j * ph) * math.sin(th / 2)], dtype=complex)


def bloch(k):
    k = k / np.linalg.norm(k)
    return np.array([np.real(np.conj(k) @ S @ k) for S in (SX, SY, SZ)])


def proj(n, sign):
    """projector onto the +-n eigenstate of n.sigma"""
    return 0.5 * (I2 + sign * (n[0] * SX + n[1] * SY + n[2] * SZ))


def seqProbs(psi, axes):
    """joint probabilities of a two-stage SG run: first magnet axes[0]; its UP
    beam enters axes[1], its DOWN beam enters axes[2].  Returns
    [P(up,up), P(up,down), P(down,up), P(down,down)] from projectors."""
    out = []
    for s1 in (+1, -1):
        a1 = proj(axes[0], s1) @ psi
        second = axes[1] if s1 > 0 else axes[2]
        for s2 in (+1, -1):
            a2 = proj(second, s2) @ a1
            out.append(float(np.real(np.vdot(a2, a2))))
    return out


AX = {'z': np.array([0.0, 0.0, 1.0]), 'x': np.array([1.0, 0.0, 0.0])}


def main():
    print('# derive.py -- quantum-measurement reference values (read in full)')
    print('# ---------------------------------------------------------------- PRNG')
    for seed in (1, 42, 20260918, 2 ** 31 + 5):
        R = Rng(seed)
        P('rng_first5[%d]' % seed, [R.next() for _ in range(5)])
    R = Rng(7)
    v = None
    for i in range(1000):
        v = R.next()
    P('rng_seed7_1000th', v)
    R = Rng(3)
    xs = [R.next() for _ in range(100000)]
    P('rng_seed3_mean100k', sum(xs) / len(xs))
    P('rng_seed3_min', min(xs))
    P('rng_seed3_max', max(xs))
    # a uniform on [0,1): mean 1/2, sd of the mean sqrt(1/12/n)
    P('rng_mean_sd_100k', math.sqrt(1 / 12 / 100000))

    print('# ---------------------------------------------------------------- lnFact and the pmf')
    for n in (5, 20, 30, 31, 100, 1000, 10000):
        P('lnFact[%d]' % n, lnFact(n))
        P('lgamma[%d]' % n, math.lgamma(n + 1))
    for (N, k, p) in ((10, 3, 0.3), (100, 50, 0.5), (10000, 5000, 0.5), (10000, 3500, 0.35),
                      (100, 0, 0.05), (100, 100, 0.95), (10, 10, 0.5), (1000, 312, 0.3)):
        P('pmf_scipy[%d,%d,%g]' % (N, k, p), float(stats.binom.pmf(k, N, p)))
        P('pmf_twin[%d,%d,%g]' % (N, k, p), binomPmf(N, k, p))
    # the pmf sums to one (twin), N = 10000, p = 0.35
    P('pmf_sum_10000_035', math.fsum(binomPmf(10000, k, 0.35) for k in range(10001)))

    print('# ---------------------------------------------------------------- coins')
    # one coin flipped 10000 times, p = 0.3, seed 20260918: u < p is heads
    R = Rng(20260918)
    seq = [1 if R.next() < 0.3 else 0 for _ in range(10000)]
    P('coin_single_first20', ''.join(str(s) for s in seq[:20]))
    P('coin_single_heads10000', sum(seq))
    P('coin_single_sigma', math.sqrt(10000 * 0.3 * 0.7))
    # a set of 10000 identical coins at p = 0.35, seed 11
    P('coin_set10000_k', coinSet(Rng(11), 10000, 0.35))
    P('coin_set10000_sigma', math.sqrt(10000 * 0.35 * 0.65))
    # a set of 10 at p = 0.5, seed 3: the individual faces
    R = Rng(3)
    P('coin_set10_faces', ''.join('1' if R.next() < 0.5 else '0' for _ in range(10)))
    # 2000 sets of 100 at p = 0.5, seed 5: the binomial
    ks, obs, mean, var, chi, dof = repeats(5, 100, 0.5, 2000)
    P('rep_100_05_mean', mean)
    P('rep_100_05_var', var)
    P('rep_100_05_chi2', chi)
    P('rep_100_05_dof', dof)
    P('rep_100_05_chi2_q999', float(stats.chi2.ppf(0.999, dof)))
    P('rep_100_05_chi2_pvalue', float(stats.chi2.sf(chi, dof)))
    P('rep_100_05_first10', ks[:10])
    P('rep_100_05_obs50', obs[50])
    # the variance of the sample variance (4th central moment), for the tolerance
    Npq = 100 * 0.25
    mu4 = Npq * (1 + 3 * (100 - 2) * 0.25)
    P('rep_100_05_sd_of_var', math.sqrt((mu4 - Npq ** 2) / 2000))
    P('rep_100_05_sd_of_mean', math.sqrt(Npq / 2000))

    print('# ---------------------------------------------------------------- the binomial view')
    ks, obs, mean, var, chi, dof = repeats(71, 100, 0.3, 1000)
    P('binv_100_03_1000_mean', mean)
    P('binv_100_03_1000_var', var)
    P('binv_100_03_1000_chi2', chi)
    P('binv_100_03_1000_dof', dof)
    P('binv_100_03_1000_q999', float(stats.chi2.ppf(0.999, dof)))
    ks, obs, mean, var, chi, dof = repeats(72, 10000, 0.5, 200)
    P('binv_10000_05_200_mean', mean)
    P('binv_10000_05_200_var', var)
    P('binv_10000_05_200_chi2', chi)
    P('binv_10000_05_200_dof', dof)
    P('binv_10000_05_200_q999', float(stats.chi2.ppf(0.999, dof)))
    ks, obs, mean, var, chi, dof = repeats(73, 10, 0.65, 3000)
    P('binv_10_065_3000_mean', mean)
    P('binv_10_065_3000_var', var)
    P('binv_10_065_3000_chi2', chi)
    P('binv_10_065_3000_dof', dof)
    P('binv_10_065_3000_q999', float(stats.chi2.ppf(0.999, dof)))
    # the spread law: sd(k/N) = sqrt(p(1-p)/N) at p = 0.3
    for N in (10, 100, 1000, 10000):
        P('sdfrac_03[%d]' % N, math.sqrt(0.3 * 0.7 / N))

    print('# ---------------------------------------------------------------- photons')
    # PhET's geometry (model units): laser x -0.15, PBS at 0 with a diagonal
    # surface y = x, V detector line y = 0.2 above it, mirror on x + y = 0.11,
    # H detector line y = -0.09, photon speed 0.3 per second
    v = 0.3
    xs0 = -0.15
    for y0 in (-0.02, -0.013, 0.0, 0.007, 0.02):
        to_split = (y0 - xs0)
        armV = 0.2 - y0
        armH = (0.11 - y0 - y0) + (y0 + 0.09)
        P('photon_arms[%g]' % y0, [to_split, armV, armH, (to_split + armV) / v])
    P('photon_arrival', (0.2 - xs0) / v)
    for th in (0.0, 30.0, 45.0, 60.0, 90.0, 17.5, 72.5):
        r = math.radians(th)
        P('pV[%g]' % th, math.sin(r) ** 2)
        P('expect[%g]' % th, math.sin(r) ** 2 - math.cos(r) ** 2)
    # batches: one draw per photon, u < sin^2(theta) goes to V
    R = Rng(99)
    pv = math.sin(math.radians(30)) ** 2
    P('photon_batch_30_99_V', sum(1 for _ in range(5000) if R.next() < pv))
    R = Rng(17)
    nv = 0
    for _ in range(5000):
        ang = 360 * R.next()
        if R.next() < math.sin(math.radians(ang)) ** 2:
            nv += 1
    P('photon_unpol_17_V', nv)
    P('photon_unpol_sigma', math.sqrt(5000 * 0.25))
    R = Rng(62)
    pv = math.sin(math.radians(60)) ** 2
    nV = sum(1 for _ in range(2000) if R.next() < pv)
    P('born_photon_60_62_H', 2000 - nV)
    # the averaging counter: counts arriving in a fixed pattern of frames
    #   (1 s window, 0.5 s sample), 1/60-s frames, one count every third frame
    val, hist, cur, tsl = 0.0, [], 0, 0.0
    for f in range(1, 301):
        if f % 3 == 0:
            cur += 1
        tsl += 1 / 60
        if tsl >= 0.5:
            hist.append((tsl, cur))
            e, t, i = 0.0, 0, 0
            for n in range(len(hist) - 1, -1, -1):
                e += hist[n][0]
                t += hist[n][1]
                i += 1
                if e >= 1:
                    break
            val = round(t / e, 12) if e > 0 else 0
            del hist[:len(hist) - i]
            cur, tsl = 0, 0.0
    P('avgcounter_20per_s', val)

    print('# ---------------------------------------------------------------- Stern-Gerlach')
    src = {'+Z': ket(0, 0), '+X': ket(math.pi / 2, 0), '-Z': ket(math.pi, 0)}
    a2 = 0.3
    thc = 2 * math.acos(math.sqrt(a2))
    src['custom0.3'] = np.array([math.sqrt(a2), math.sqrt(1 - a2)], dtype=complex)
    P('custom_theta_03', thc)
    P('custom_bloch_03', list(bloch(src['custom0.3'])))
    P('custom_Pz_03', abs(src['custom0.3'][0]) ** 2)
    # PhET's own custom state: theta = pi (1 - a^2), so P(z up) = (1 + cos theta)/2
    P('phet_custom_Pz_075', (1 + math.cos(math.pi * (1 - 0.75))) / 2)
    P('phet_custom_Pz_03', (1 + math.cos(math.pi * (1 - 0.3))) / 2)
    exps = {'1': ['z'], '2': ['x'], '3': ['z', 'x', 'x'], '4': ['z', 'z', 'z'],
            '5': ['x', 'z', 'z'], '6': ['x', 'x', 'x'], 'custom': ['x', 'z', 'z']}
    for e, axes in exps.items():
        for sname, psi in src.items():
            if len(axes) == 1:
                pu = float(np.real(np.vdot(proj(AX[axes[0]], 1) @ psi, proj(AX[axes[0]], 1) @ psi)))
                P('sg[%s,%s]' % (e, sname), [pu, 1 - pu])
            else:
                P('sg[%s,%s]' % (e, sname), seqProbs(psi, [AX[a] for a in axes]))

    def sgBatch(seed, r0, axes, n):
        R = Rng(seed)
        cnt = [0, 0, 0, 0]
        for _ in range(n):
            r = np.array(r0, dtype=float)
            n1 = AX[axes[0]]
            up1 = R.next() < 0.5 * (1 + r @ n1)
            r = n1 if up1 else -n1
            if len(axes) == 1:
                cnt[0 if up1 else 1] += 1
                continue
            n2 = AX[axes[1]] if up1 else AX[axes[2]]
            up2 = R.next() < 0.5 * (1 + r @ n2)
            cnt[(0 if up1 else 2) + (0 if up2 else 1)] += 1
        return cnt
    P('sg_batch_exp3_+X_31', sgBatch(31, [1, 0, 0], ['z', 'x', 'x'], 10000))
    P('sg_batch_exp5_+Z_32', sgBatch(32, [0, 0, 1], ['x', 'z', 'z'], 10000))
    P('sg_batch_exp1_c03_33', sgBatch(33, list(bloch(src['custom0.3'])), ['z'], 10000))
    P('sg_batch_exp4_-Z_34', sgBatch(34, [0, 0, -1], ['z', 'z', 'z'], 4000))
    # beyond PhET: DIFFERENT second-stage magnets (PhET links them), so that the
    # routing of the up and down beams is pinned by something
    P('sg_mixed_zxz_+X', seqProbs(src['+X'], [AX['z'], AX['x'], AX['z']]))
    P('sg_mixed_zxz_c03', seqProbs(src['custom0.3'], [AX['z'], AX['x'], AX['z']]))
    P('sg_batch_zxz_+X_35', sgBatch(35, [1, 0, 0], ['z', 'x', 'z'], 10000))

    print('# ---------------------------------------------------------------- the Bloch sphere')
    # electron: gamma/2pi = |g_e| (mu_B/h); CODATA 2022 as stored in bloch_sphere.html
    g_e = -2.00231930436092
    muB_Hz = 13996244917.1           # Hz/T
    gam_e_MHz = 28024.9513861        # MHz/T
    P('gamma_e_from_g_muB_MHzT', abs(g_e) * muB_Hz / 1e6)
    P('gamma_e_rel_diff', abs(g_e) * muB_Hz / 1e6 / gam_e_MHz - 1)
    P('B0_mT', 1e3 / gam_e_MHz * 1e3)       # the field that turns an electron once per ns
    # precession: H = (hbar w / 2) sigma_z, w = 2 pi s per ns; U = expm(-i w t sigma_z/2)
    for (th, ph, s, tau) in ((math.pi / 2, 0.0, 1.0, 0.75), (1.1, 0.4, 0.6, 0.4), (2.3, 5.1, -0.35, 0.9)):
        w = 2 * math.pi * s
        U = expm(-1j * w * tau * SZ / 2)
        k1 = U @ ket(th, ph)
        P('prec_bloch[%g,%g,%g,%g]' % (th, ph, s, tau), list(bloch(k1)))
        P('prec_U[%g,%g,%g,%g]' % (th, ph, s, tau), [U[0, 0].real, U[0, 0].imag, U[1, 1].real, U[1, 1].imag])
        for axn, n in (('X', [1, 0, 0]), ('Y', [0, 1, 0]), ('Z', [0, 0, 1])):
            b = bloch(k1)
            P('prec_Pup[%g,%g,%g,%g,%s]' % (th, ph, s, tau, axn), 0.5 * (1 + float(np.dot(b, n))))
    # the equation in each basis: |psi> = a|up_n> + b e^{i chi}|down_n>
    kets = {'Z': (np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)),
            'X': (np.array([1, 1], dtype=complex) / math.sqrt(2), np.array([1, -1], dtype=complex) / math.sqrt(2)),
            'Y': (np.array([1, 1j], dtype=complex) / math.sqrt(2), np.array([1, -1j], dtype=complex) / math.sqrt(2))}
    for (th, ph) in ((1.1, 2.3), (math.pi / 2, 0.0), (0.4, 4.0)):
        psi = ket(th, ph)
        for bn, (u, d) in kets.items():
            au = np.vdot(u, psi)
            ad = np.vdot(d, psi)
            chi = (cmath.phase(ad) - cmath.phase(au)) % (2 * math.pi)
            P('basis[%g,%g,%s]' % (th, ph, bn), [abs(au), abs(ad), chi / math.pi, cmath.phase(au) / math.pi])
    # PhET's displayed Y-basis relative phase for +X, reconstructed in the standard kets
    o, a = math.cos(math.pi / 4), math.sin(math.pi / 4)
    ph = 0.0
    d = math.atan2(a * math.cos(ph), o + a * math.sin(ph)) / math.pi
    u = math.atan2(-a * math.cos(ph), o - a * math.sin(ph)) / math.pi
    c = (u - d) % 2
    recon = (kets['Y'][0] + cmath.exp(1j * math.pi * c) * kets['Y'][1]) / math.sqrt(2)
    P('phet_Ybasis_chi_plusX', c)
    P('phet_Ybasis_recon_bloch', list(bloch(recon)))
    # measuring 10 atoms, seeded: 1000 rounds along Y after the default precession
    R = Rng(41)
    b = bloch(expm(-1j * 2 * math.pi * 1.0 * 0.75 * SZ / 2) @ ket(math.pi / 2, 0))
    pY = 0.5 * (1 + b[1])
    P('bloch10_pY_default', pY)
    R = Rng(42)
    b2 = bloch(expm(-1j * 2 * math.pi * 0.6 * 0.4 * SZ / 2) @ ket(1.1, 0.4))
    pX = 0.5 * (1 + b2[0])
    P('bloch10_pX_06_04', pX)
    P('bloch10_upX_06_04_seed42', sum(1 for _ in range(10000) if R.next() < pX))

    print('# ---------------------------------------------------------------- the Born rule view')
    for N in (1, 2, 3, 4, 8, 10, 30, 100, 1000):
        T = math.cos(math.pi / (2 * N)) ** (2 * N)
        P('chainT[%d]' % N, T)
    P('chain_ratio_100_1000', (1 - math.cos(math.pi / 200) ** 200) / (1 - math.cos(math.pi / 2000) ** 2000))
    P('chain_asym_1000', (1 - math.cos(math.pi / 2000) ** 2000) * 4 * 1000 / math.pi ** 2)
    for al in (30.0, 45.0, 60.0, 90.0, 120.0):
        r = math.radians(al)
        P('middle_spin[%g]' % al, math.sin(r) ** 2 / 4)
        P('middle_photon[%g]' % al, math.sin(2 * r) ** 2 / 4)

    def chainMC(seed, N, n):
        R = Rng(seed)
        ok = 0
        for _ in range(n):
            r = np.array([0.0, 0.0, 1.0])
            alive = True
            for k in range(1, N + 1):
                a = math.pi * k / N
                nn = np.array([math.sin(a), 0.0, math.cos(a)])
                if R.next() < 0.5 * (1 + r @ nn):
                    r = nn
                else:
                    alive = False
                    break
            if alive:
                ok += 1
        return ok
    P('chainMC_8_51', chainMC(51, 8, 5000))
    P('chainMC_1_55', chainMC(55, 1, 3000))

    def middleSpinMC(seed, al, n):
        R = Rng(seed)
        ok = 0
        a = math.radians(al)
        nn = np.array([math.sin(a), 0.0, math.cos(a)])
        for _ in range(n):
            r = np.array([0.0, 0.0, 1.0])
            if R.next() < 0.5 * (1 + r @ nn):
                r = nn
                # the engine measures along +z and counts NOT-up: u >= (1 + r.z)/2
                if not (R.next() < 0.5 * (1 + r[2])):
                    ok += 1
        return ok

    def middlePhotonMC(seed, al, n):
        # the JS passes the first polariser as photonDecide(R, 90 - alpha):
        # pV(90 - alpha) = sin^2(90 - alpha) = cos^2(alpha), written the same way
        R = Rng(seed)
        ok = 0
        pv = lambda t: math.sin(math.radians(t)) ** 2
        for _ in range(n):
            if R.next() < pv(90 - al):
                if R.next() < pv(al):
                    ok += 1
        return ok
    P('middle_spin_MC_60_52', middleSpinMC(52, 60, 5000))
    P('middle_photon_MC_60_53', middlePhotonMC(53, 60, 5000))
    R = Rng(61)
    th = math.radians(60)
    P('born_spin_60_61_up', sum(1 for _ in range(2000) if R.next() < 0.5 * (1 + math.cos(th))))
    P('cos2half_60', math.cos(math.radians(30)) ** 2)
    P('cos2_60', math.cos(math.radians(60)) ** 2)
    # the Born view's default points: 2000 shots, seed 61; the spin at angle a
    # uses seed 61 + i, the photon (a <= 90) seed 161 + i; counts and chi^2
    angs = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]
    spin_up, ph_H, chi, dof = [], [], 0.0, 0
    for i, a in enumerate(angs):
        R = Rng(61 + i)
        t = math.radians(a)
        pu = 0.5 * (1 + math.cos(t))            # the engine: r = (sin t, 0, cos t), n = z
        u = sum(1 for _ in range(2000) if R.next() < pu)
        spin_up.append(u)
        law = math.cos(math.radians(a) / 2) ** 2
        sd = math.sqrt(law * (1 - law) / 2000)
        if sd > 1e-12:
            chi += ((u / 2000 - law) / sd) ** 2
            dof += 1
        if a <= 90:
            R = Rng(161 + i)
            pv = math.sin(math.radians(a)) ** 2
            h = 2000 - sum(1 for _ in range(2000) if R.next() < pv)
            ph_H.append(h)
            lawp = math.cos(math.radians(a)) ** 2
            sdp = math.sqrt(lawp * (1 - lawp) / 2000)
            if sdp > 1e-12:
                chi += ((h / 2000 - lawp) / sdp) ** 2
                dof += 1
    P('bornview_spin_up', spin_up)
    P('bornview_photon_H', ph_H)
    P('bornview_chi2', chi)
    P('bornview_dof', dof)
    P('bornview_chi2_q999', float(stats.chi2.ppf(0.999, dof)))
    # the chain view's points: min(shots, 4000) = 2000 per N, seed 61 + 500 + i
    CH = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
    P('chainview_T', [chainMC(561 + i, N, 2000) / 2000 for i, N in enumerate(CH)])
    P('norm_ppf_0999', float(stats.norm.ppf(0.999)))
    for nu in (8, 23, 28, 34):
        P('chi2_ppf_0999[%d]' % nu, float(stats.chi2.ppf(0.999, nu)))


if __name__ == '__main__':
    main()
