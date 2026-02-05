"""Data structures for hook-joint geometric mappings."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TendonParams:
    """Immutable tendon geometry parameters for one joint module.

    Args:
        r: Radial distance from joint center to each tendon anchor in the
            local ``xy`` plane. Must be positive.
        h: Half spacing between top and bottom anchor planes along local
            ``z``. Must be positive.
        phis: One-dimensional array of tendon azimuth angles (radians) in the
            local ``xy`` plane.

    Raises:
        ValueError: If ``r`` or ``h`` is non-positive, or if ``phis`` is not a
            non-empty one-dimensional array.
    """

    r: float
    h: float
    phis: np.ndarray

    def __post_init__(self) -> None:
        """Validate scalar parameters and coerce ``phis`` to a float array."""
        if self.r <= 0:
            raise ValueError("r must be positive")
        if self.h <= 0:
            raise ValueError("h must be positive")

        phis = np.asarray(self.phis, dtype=float)
        if phis.ndim != 1 or phis.size == 0:
            raise ValueError("phis must be a non-empty 1D array")

        # dataclass is frozen, so field replacement must use object.__setattr__
        object.__setattr__(self, "phis", phis)
