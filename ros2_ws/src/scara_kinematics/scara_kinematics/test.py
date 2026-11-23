import math

import random

from ik_node import ik, fk

L1, L2 = 0.175, 0.175

def test_roundtrip():
    random.seed(0)
    for _ in range(200):
        q1 = random.uniform(-math.pi, math.pi)
        q2 = random.uniform(-3.0, 3.0)
        x, y = fk(q1, q2, L1, L2)
        for elbow in (-1,1):
            sol = ik(x, y, L1, L2, elbow)
            assert sol is not None
            x2, y2 = fk(*sol, L1, L2)
            assert math.isclose(x, x2, abs_tol=1e-9)
            assert math.isclose(y, y2, abs_tol=1e-9)


def test_unreachable():
    assert ik(1.0, 0.0, L1, L2) is None            
    assert ik(0.0, 0.0, L1, 0.05) is None          


def test_full_reach():
    sol = ik(L1 + L2, 0.0, L1, L2)                 
    assert sol is not None
    assert math.isclose(sol[1], 0.0, abs_tol=1e-6)