# Layer 1：HookeJointGeom，只 import functional 并转发
"""
    joint.py 中禁止出现数学公式实现

    所有计算都调用 functional.py 的函数

    joint.py 允许做参数校验、默认值、文档字符串
"""


from typing import Sequence
import core

class HookeJointGeom:
    r: float
    h: float
    phis: Sequence[float]
    eps: float = 1e-12
    pole_theta_x: float = 0.0

    def __init__(self, r: float, h: float, phis: Sequence[float], eps: float = 1e-12, pole_theta_x: float = 0.0):
        self.r = r
        self.h = h
        self.phis = phis
        self.eps = eps
        self.pole_theta_x = pole_theta_x

    def direction_from_angles(tx, ty)

    def angles_from_direction(n)

    def rope_lengths_from_angles(tx, ty)

    def rope_lengths_from_direction(n)
