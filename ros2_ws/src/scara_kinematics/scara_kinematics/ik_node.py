import math

def fk(q1: float, q2: float, l1: float, l2: float) -> tuple[float, float]:
    """Углы суставов (рад) -> положение конца (x, y) в метрах."""
    x = l1 * math.cos(q1) + l2 * math.cos(q1 + q2)
    y = l1 * math.sin(q1) + l2 * math.sin(q1 + q2)
    return x, y

def ik(x: float, y: float, L1: float, L2:float, elbow: int = 1):
    c2 = (x ** 2 + y ** 2 - L1 ** 2 - L2 ** 2) / (2*L1*L2)
    if abs(c2) > 1.0 + 1e-9:
        return None

    c2 = max(-1.0, min(1.0, c2))
    q2 = elbow * math.acos(c2)
    q1 = math.atan2(y, x) - math.atan2(L2 * math.sin(q2), L1 + L2 * math.cos(q2))

    return q1, q2

def main() -> None:
    print('Hi from scara_kinematics.')


if __name__ == '__main__':
    main()