"""Tests for ST-13 joint distributions of two random variables.

Run:  python3 test_joint_distributions.py     ->  "All N tests passed."
Asserts the headline identities: pmf/pdf normalization, marginals summing/
integrating to 1, the independence factorization f=f_X f_Y, continuous and
discrete LOTUS, linearity of expectation, and the cdf corner limits.
"""
import math

import numpy as np

from joint_distributions import (
    joint_pmf_is_valid, marginal_x, marginal_y, independent_rv_check,
    expectation_joint, joint_cdf, marginal_cdf_x,
    joint_pdf_is_valid, normalize_joint_pdf, marginal_pdf_x, marginal_pdf_y,
    independent_pdf_check, expectation_joint_continuous, joint_cdf_continuous,
    _integrate,
)

# canonical discrete example (STAT 414 L17):  f(x,y)=(x+y)/32, x in {1,2}, y in {1,2,3,4}
XV, YV = [1, 2], [1, 2, 3, 4]
P = np.array([[(x + y) for y in YV] for x in XV], dtype=float) / 32.0

# canonical continuous examples (STAT 414 L20) on the unit square
F_IND = lambda x, y: 4.0 * x * y     # independent: f_X=2x, f_Y=2y
F_DEP = lambda x, y: x + y           # dependent:   f_X=x+1/2, f_Y=y+1/2


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


# --- discrete (L17) ----------------------------------------------------------

def test_discrete_pmf_validity():
    assert joint_pmf_is_valid(P) is True
    # negative entry -> invalid
    bad = P.copy(); bad[0, 0] = -bad[0, 0]
    assert joint_pmf_is_valid(bad) is False
    # mass != 1 -> invalid
    assert joint_pmf_is_valid(0.9 * P) is False


def test_discrete_marginals_are_pmfs():
    fx, fy = marginal_x(P), marginal_y(P)
    # marginals sum to 1 and match the hand values 14/32, 18/32 and (3+2y)/32
    assert _approx(fx.sum(), 1.0) and _approx(fy.sum(), 1.0)
    assert _approx(fx[0], 14 / 32) and _approx(fx[1], 18 / 32)
    assert _approx(fy[0], 5 / 32) and _approx(fy[3], 11 / 32)


def test_discrete_independence():
    # (x+y)/32 does NOT factor:  f(1,1)=2/32 but f_X(1)f_Y(1)=(14/32)(5/32)
    assert independent_rv_check(P) is False
    fx, fy = marginal_x(P), marginal_y(P)
    assert not _approx(P[0, 0], fx[0] * fy[0])
    # an outer-product table IS independent and reproduces its own marginals
    Pi = np.outer([0.4, 0.6], [0.5, 0.5])
    assert independent_rv_check(Pi) is True
    assert _approx(marginal_x(Pi)[0], 0.4) and _approx(marginal_y(Pi)[0], 0.5)


def test_discrete_lotus_and_marginal_means_agree():
    EX = expectation_joint(lambda x, y: x, XV, YV, P)
    EY = expectation_joint(lambda x, y: y, XV, YV, P)
    EXY = expectation_joint(lambda x, y: x * y, XV, YV, P)
    assert _approx(EX, 50 / 32) and _approx(EY, 90 / 32) and _approx(EXY, 140 / 32)
    # joint LOTUS for a function of X alone must equal the 1-D marginal mean (~ST-05)
    fx = marginal_x(P)
    EX_marg = sum(x * fx[i] for i, x in enumerate(XV))
    assert _approx(EX, EX_marg)


def test_discrete_expectation_linearity():
    EX = expectation_joint(lambda x, y: x, XV, YV, P)
    EY = expectation_joint(lambda x, y: y, XV, YV, P)
    EXpY = expectation_joint(lambda x, y: x + y, XV, YV, P)
    assert _approx(EXpY, EX + EY)               # holds with or without independence


def test_discrete_cdf_limits_and_monotonicity():
    # corner = total mass = 1, and the marginal cdf is the joint cdf at y = max
    assert _approx(joint_cdf(P, XV, YV, 2, 4), 1.0)
    assert _approx(joint_cdf(P, XV, YV, 1, 2), 5 / 32)      # f(1,1)+f(1,2)
    assert _approx(joint_cdf(P, XV, YV, 1, 4), marginal_cdf_x(P, XV, 1))
    # nondecreasing in each argument
    assert joint_cdf(P, XV, YV, 2, 4) >= joint_cdf(P, XV, YV, 1, 4)
    assert joint_cdf(P, XV, YV, 2, 4) >= joint_cdf(P, XV, YV, 2, 2)


# --- continuous (L20) --------------------------------------------------------

def test_continuous_normalization():
    assert joint_pdf_is_valid(F_IND, 0, 1, 0, 1) is True
    assert joint_pdf_is_valid(F_DEP, 0, 1, 0, 1) is True
    # an unnormalized shape: normalize_joint_pdf recovers the constant 4 for xy
    c = normalize_joint_pdf(lambda x, y: x * y, 0, 1, 0, 1)
    assert _approx(c, 4.0, tol=1e-3)


def test_continuous_marginals_integrate_to_one_and_match_closed_form():
    # f=4xy:  f_X(x) = 2x ; integrates to 1
    assert _approx(marginal_pdf_x(F_IND, 0.5, 0, 1), 1.0, tol=1e-6)
    assert _approx(marginal_pdf_x(F_IND, 0.7, 0, 1), 1.4, tol=1e-6)
    tot = _integrate(lambda x: marginal_pdf_x(F_IND, x, 0, 1), 0, 1, n=200)
    assert _approx(tot, 1.0, tol=1e-3)
    # f=x+y:  f_X(x) = x + 1/2
    assert _approx(marginal_pdf_x(F_DEP, 0.3, 0, 1), 0.8, tol=1e-6)
    assert _approx(marginal_pdf_y(F_DEP, 0.9, 0, 1), 1.4, tol=1e-6)


def test_continuous_independence():
    assert independent_pdf_check(F_IND, 0, 1, 0, 1) is True    # 4xy = (2x)(2y)
    assert independent_pdf_check(F_DEP, 0, 1, 0, 1) is False   # x+y not separable


def test_continuous_lotus_and_independence_product():
    # f=x+y:  E[X]=7/12, E[XY]=1/3 by direct double integral
    eX = expectation_joint_continuous(lambda x, y: x, F_DEP, 0, 1, 0, 1)
    eXY = expectation_joint_continuous(lambda x, y: x * y, F_DEP, 0, 1, 0, 1)
    assert _approx(eX, 7 / 12, tol=1e-3) and _approx(eXY, 1 / 3, tol=1e-3)
    # f=4xy is independent  =>  E[XY] = E[X] E[Y] = (2/3)(2/3) = 4/9
    iX = expectation_joint_continuous(lambda x, y: x, F_IND, 0, 1, 0, 1)
    iY = expectation_joint_continuous(lambda x, y: y, F_IND, 0, 1, 0, 1)
    iXY = expectation_joint_continuous(lambda x, y: x * y, F_IND, 0, 1, 0, 1)
    assert _approx(iX, 2 / 3, tol=1e-3) and _approx(iY, 2 / 3, tol=1e-3)
    assert _approx(iXY, iX * iY, tol=1e-3)


def test_continuous_expectation_linearity():
    eX = expectation_joint_continuous(lambda x, y: x, F_DEP, 0, 1, 0, 1)
    eY = expectation_joint_continuous(lambda x, y: y, F_DEP, 0, 1, 0, 1)
    eXpY = expectation_joint_continuous(lambda x, y: x + y, F_DEP, 0, 1, 0, 1)
    assert _approx(eXpY, eX + eY, tol=1e-6)


def test_continuous_cdf_corner_and_value():
    # f=4xy has cdf F(x,y) = x^2 y^2
    assert _approx(joint_cdf_continuous(F_IND, 0, 0, 0.5, 0.5), 0.0625, tol=1e-3)
    assert _approx(joint_cdf_continuous(F_IND, 0, 0, 1.0, 1.0), 1.0, tol=1e-3)
    # f=x+y has F(0.5,0.5) = 1/8
    assert _approx(joint_cdf_continuous(F_DEP, 0, 0, 0.5, 0.5), 0.125, tol=1e-3)
    assert _approx(joint_cdf_continuous(F_DEP, 0, 0, 1.0, 1.0), 1.0, tol=1e-3)
    # below support -> 0, and nondecreasing
    assert joint_cdf_continuous(F_IND, 0, 0, 0.0, 0.5) == 0.0
    assert (joint_cdf_continuous(F_IND, 0, 0, 1, 1)
            >= joint_cdf_continuous(F_IND, 0, 0, 0.5, 1))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
