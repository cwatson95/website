#!/usr/bin/env python3
"""derive.py -- the Python twin of quantum-coin-toss.html's own view (the
hidden difference).  The engine it shares with quantum-measurement.html is
twinned in ../quantum-measurement/derive.py, whose PRNG this file imports;
the coin and binomial pins this sim's selfTest shares are that file's output
(../quantum-measurement/refvals.txt).

    python3 derive.py > refvals.txt      # read the output IN FULL

Independent routes: the density matrices and P(+x) are numpy 2x2 algebra
(projector traces), not the (1 + r.n)/2 the sim uses; the seeded runs mirror
the engine's draw order bit for bit.
"""
import math, os, sys
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, '..', 'quantum-measurement'))
from derive import Rng, SX, SY, SZ, I2, proj   # noqa: E402  (the shared, bit-exact twin)


def P(name, val):
    print('%s = %r' % (name, val))


def main():
    print('# derive.py -- quantum-coin-toss: the hidden difference (read in full)')
    X = np.array([1.0, 0.0, 0.0])
    Z = np.array([0.0, 0.0, 1.0])
    for p in (0.0, 0.05, 0.3, 0.5, 0.7, 0.85, 1.0):
        rho_mix = np.array([[p, 0], [0, 1 - p]], dtype=complex)            # a hidden classical face
        psi = np.array([math.sqrt(p), math.sqrt(1 - p)], dtype=complex)
        rho_pure = np.outer(psi, psi.conj())                                # the quantum coin
        Pz_mix = float(np.real(np.trace(rho_mix @ proj(Z, 1))))
        Pz_pure = float(np.real(np.trace(rho_pure @ proj(Z, 1))))
        Px_mix = float(np.real(np.trace(rho_mix @ proj(X, 1))))
        Px_pure = float(np.real(np.trace(rho_pure @ proj(X, 1))))
        pur_mix = float(np.real(np.trace(rho_mix @ rho_mix)))
        pur_pure = float(np.real(np.trace(rho_pure @ rho_pure)))
        P('mix[%g]' % p, [Pz_mix, Pz_pure, Px_mix, Px_pure, pur_mix, pur_pure, float(np.real(rho_pure[0, 1]))])
        rx = [float(np.real(np.trace(r @ S))) for r in (rho_mix,) for S in (SX, SY, SZ)]
        rq = [float(np.real(np.trace(rho_pure @ S))) for S in (SX, SY, SZ)]
        P('bloch_mix[%g]' % p, rx)
        P('bloch_pure[%g]' % p, rq)

    def mixRun(seed, p, n):
        """the engine's order: n classical faces (u < p), n classical faces then
        a sideways measurement (u < 1/2 is +x), n quantum face-on (u < (1 + rz)/2),
        n quantum sideways (u < (1 + rx)/2)"""
        R = Rng(seed)
        rq = [2 * math.sqrt(p * (1 - p)), 0.0, 2 * p - 1]
        cz = sum(1 for _ in range(n) if R.next() < p)
        cx = 0
        for _ in range(n):
            face = R.next() < p
            rz = 1.0 if face else -1.0
            if R.next() < 0.5 * (1 + (rz * 0.0)):        # (+-z).x = 0: exactly 1/2
                cx += 1
        qz = sum(1 for _ in range(n) if R.next() < 0.5 * (1 + rq[2]))
        qx = sum(1 for _ in range(n) if R.next() < 0.5 * (1 + rq[0]))
        return [cz, cx, qz, qx]
    for (seed, p, n) in ((7, 0.7, 1000), (21, 0.5, 2000), (3, 0.15, 1500), (9, 1.0, 500)):
        P('mixRun[%d,%g,%d]' % (seed, p, n), mixRun(seed, p, n))
    # the law against p, for the view's curve (and its maximum at p = 1/2)
    for p in (0.1, 0.25, 0.5, 0.75, 0.9):
        P('Px_pure_law[%g]' % p, (1 + 2 * math.sqrt(p * (1 - p))) / 2)


if __name__ == '__main__':
    main()
