# Layer 1：HookeJoint
# joint.py
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .data import TendonParams
from . import core  # 只做委托，不复制实现

@dataclass(frozen=True, slots=True)
class HookJoint:
    """OOP wrapper for one Hooke joint module (one instance = one joint).

    This class binds structural parameters (r, h, phis) and delegates all math
    to core.py procedural functions (single source of truth).
    """
    params: TendonParams
    eps: float = 1e-12
    pole_theta_x: float = 0.0

    # --- Angle <-> direction ---

    def direction_from_angles(self, theta_x: float, theta_y: float) -> np.ndarray:
        return core.direction_from_angles(theta_x, theta_y)

    def angles_from_direction(self, n: np.ndarray) -> tuple[float, float]:
        return core.angles_from_direction(n, eps=self.eps, pole_theta_x=self.pole_theta_x)

    # --- Rope lengths ---

    def rope_lengths_from_angles(self, theta_x: float, theta_y: float) -> np.ndarray:
        return core.rope_lengths_from_angles(theta_x, theta_y, params=self.params)

    def rope_lengths_from_direction(self, n: np.ndarray) -> np.ndarray:
        return core.rope_lengths_from_direction(
            n, params=self.params, eps=self.eps, pole_theta_x=self.pole_theta_x
        )

    # 可选：一些语义小糖（不会引入新实现）
    @property
    def tendon_count(self) -> int:
        return int(self.params.phis.size)