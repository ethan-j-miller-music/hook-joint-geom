"""Stable public API that re-exports core mappings and wrapper construction."""

from __future__ import annotations

import numpy as np

from . import core as _core
from .data import TendonParams
from .joint import HookJoint as _HookJoint


def direction_from_angles(theta_x: float, theta_y: float) -> np.ndarray:
    """Public procedural mapping from angles to direction vector."""
    return _core.direction_from_angles(theta_x, theta_y)


def angles_from_direction(
    n: np.ndarray, *, eps: float = 1e-12, pole_theta_x: float = 0.0
) -> tuple[float, float]:
    """Public procedural mapping from direction vector to joint angles."""
    return _core.angles_from_direction(n, eps=eps, pole_theta_x=pole_theta_x)


def rope_lengths_from_angles(
    theta_x: float, theta_y: float, *, params: TendonParams
) -> np.ndarray:
    """Public procedural mapping from angles to tendon lengths."""
    return _core.rope_lengths_from_angles(theta_x, theta_y, params=params)


def rope_lengths_from_direction(
    n: np.ndarray,
    *,
    params: TendonParams,
    eps: float = 1e-12,
    pole_theta_x: float = 0.0,
) -> np.ndarray:
    """Public procedural mapping from direction vector to tendon lengths."""
    return _core.rope_lengths_from_direction(
        n, params=params, eps=eps, pole_theta_x=pole_theta_x
    )


def create_joint(
    params: TendonParams,
    *,
    eps: float = 1e-12,
    pole_theta_x: float = 0.0,
) -> _HookJoint:
    """Construct a :class:`HookJoint` instance using stable factory semantics.

    Args:
        params: Joint tendon geometry.
        eps: Tolerance used in inverse mapping methods.
        pole_theta_x: Branch value used for pole inverse solutions.

    Returns:
        Configured :class:`HookJoint` instance.
    """
    return _HookJoint(params=params, eps=eps, pole_theta_x=pole_theta_x)


__all__ = [
    "create_joint",
    "direction_from_angles",
    "angles_from_direction",
    "rope_lengths_from_angles",
    "rope_lengths_from_direction",
]
