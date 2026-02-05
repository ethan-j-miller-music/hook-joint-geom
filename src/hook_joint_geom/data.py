# 参数绑定类
from dataclasses import dataclass
import numpy as np
from typing import Sequence

@dataclass(frozen=True)
class TendonParams:
    r: float
    h: float
    phis: np.ndarray

    def __post_init__(self):
        if self.r <= 0:
            raise ValueError("r must be positive")
        if self.h <= 0:
            raise ValueError("h must be positive")

        phis = np.asarray(self.phis, dtype=float)
        if phis.ndim != 1 or phis.size == 0:
            raise ValueError("phis must be a non-empty 1D array")

        # frozen=True 时，必须用 object.__setattr__
        object.__setattr__(self, "phis", phis)
