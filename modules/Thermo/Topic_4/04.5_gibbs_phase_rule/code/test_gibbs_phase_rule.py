"""test_gibbs_phase_rule.py — checks for Module 4.5.  Run: python3 test_gibbs_phase_rule.py"""
from gibbs_phase_rule import gibbs_phase_rule, single_component_dof, max_phases

_n = 0
def chk(name, got, want):
    global _n
    assert got == want, f"{name}: {got!r} != {want!r}"
    _n += 1

# core rule
chk("water vapor (1,1)", gibbs_phase_rule(1, 1), 2)
chk("vapor+ice (1,2)", gibbs_phase_rule(1, 2), 1)      # why quality is needed
chk("triple point (1,3)", gibbs_phase_rule(1, 3), 0)
chk("water+ammonia (2,1)", gibbs_phase_rule(2, 1), 3)
chk("ammonia-water liq+vap (2,2)", gibbs_phase_rule(2, 2), 2)
# single-component shortcut == general rule with N=1
chk("single P=1", single_component_dof(1), 2)
chk("single P=2", single_component_dof(2), 1)
chk("single P=3", single_component_dof(3), 0)
chk("single==general", single_component_dof(2), gibbs_phase_rule(1, 2))
# max coexisting phases
chk("max phases pure", max_phases(1), 3)
chk("max phases binary", max_phases(2), 4)
# Moran review questions 19-24 (N, P) -> F
chk("Q19 water vapor", gibbs_phase_rule(1, 1), 2)
chk("Q20 water+ammonia liq", gibbs_phase_rule(2, 1), 3)
chk("Q21 vapor+ice", gibbs_phase_rule(1, 2), 1)
chk("Q22 liquid water", gibbs_phase_rule(1, 1), 2)
chk("Q23 NH3-water liq+vap", gibbs_phase_rule(2, 2), 2)
chk("Q24 water+LiBr liq", gibbs_phase_rule(2, 1), 3)

print(f"All {_n} tests passed.")
