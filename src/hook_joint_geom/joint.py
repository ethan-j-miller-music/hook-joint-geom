"""Object-oriented wrapper for the hook-joint geometric mappings."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import core
from .data import TendonParams


@dataclass(frozen=True, slots=True)
class HookJoint:
    """Thin wrapper that binds parameters and delegates all math to ``core``.

    Args:
        params: Tendon geometry bound to this instance.
        eps: Tolerance used in inverse mapping calls.
        pole_theta_x: Pole branch value for inverse mapping calls.

    Notes:
        This class intentionally contains no duplicated math to preserve
        ``core.py`` as the single source of truth.
    """

    params: TendonParams
    eps: float = 1e-12
    pole_theta_x: float = 0.0

    def direction_from_angles(self, theta_x: float, theta_y: float) -> np.ndarray:
        """Return direction vector for the provided angle pair."""
        return core.direction_from_angles(theta_x, theta_y)

    def angles_from_direction(self, n: np.ndarray) -> tuple[float, float]:
        """Return ``(theta_x, theta_y)`` for input direction vector ``n``."""
        return core.angles_from_direction(n, eps=self.eps, pole_theta_x=self.pole_theta_x)

    def rope_lengths_from_angles(self, theta_x: float, theta_y: float) -> np.ndarray:
        """Return tendon lengths from an angle pair using bound parameters."""
        return core.rope_lengths_from_angles(theta_x, theta_y, params=self.params)

    def rope_lengths_from_direction(self, n: np.ndarray) -> np.ndarray:
        """Return tendon lengths from direction vector ``n``."""
        return core.rope_lengths_from_direction(
            n, params=self.params, eps=self.eps, pole_theta_x=self.pole_theta_x
        )

    @property
    def tendon_count(self) -> int:
        """Number of tendons in the bound parameter set."""
        return int(self.params.phis.size)
