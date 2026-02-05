# api.py
from __future__ import annotations

import numpy as np

from .data import TendonParams
from .joint import HookJoint as _HookJoint  # OOP 入口（类型与命名即承诺）
from . import core as _core  # 内部实现源，不建议外部直接依赖


# -------------------------
# Procedural API (stable)
# -------------------------

def direction_from_angles(theta_x: float, theta_y: float) -> np.ndarray:
    """Stable procedural API. See README 'Minimal API Design'."""
    return _core.direction_from_angles(theta_x, theta_y)

def angles_from_direction(
    n: np.ndarray, *, eps: float = 1e-12, pole_theta_x: float = 0.0
) -> tuple[float, float]:
    """Stable procedural API. See README 'Minimal API Design'."""
    return _core.angles_from_direction(n, eps=eps, pole_theta_x=pole_theta_x)

def rope_lengths_from_angles(
    theta_x: float, theta_y: float, *, params: TendonParams
) -> np.ndarray:
    """Stable procedural API. See README 'Minimal API Design'."""
    return _core.rope_lengths_from_angles(theta_x, theta_y, params=params)

def rope_lengths_from_direction(
    n: np.ndarray, *, params: TendonParams, eps: float = 1e-12, pole_theta_x: float = 0.0
) -> np.ndarray:
    """Stable procedural API. See README 'Minimal API Design'."""
    return _core.rope_lengths_from_direction(
        n, params=params, eps=eps, pole_theta_x=pole_theta_x
    )


def create_joint(
    params: TendonParams,
    *,
    eps: float = 1e-12,
    pole_theta_x: float = 0.0,
) -> _HookJoint:
    """Factory for the OOP API.

    This is the recommended stable construction entry for a Hooke joint object.
    Keeping construction behind this function makes future compatibility easier
    (e.g., swapping implementations, adding configuration, deprecations).
    """
    return _HookJoint(params=params, eps=eps, pole_theta_x=pole_theta_x)


__all__ = [
    # OOP
    "create_joint",
    # procedural (the 4 functions)
    "direction_from_angles",
    "angles_from_direction",
    "rope_lengths_from_angles",
    "rope_lengths_from_direction",
]
