# hook-joint-geom

`hook-joint-geom` provides closed-form geometric mappings for one 2-DOF Hooke (universal) joint module. It maps between joint angles `(theta_x, theta_y)`, a local direction vector `n in S^2`, and tendon rope lengths for fixed tendon anchor geometry.

The package is intentionally minimal: `core.py` holds the procedural truth, and `HookJoint` is a thin wrapper that binds parameters and delegates to the same equations.

## Installation

### Development install

```bash
pip install -e .
```

### Install from GitHub tag

```bash
pip install "git+https://github.com/<org>/<repo>.git@<tag>"
```

## Quickstart

```python
import numpy as np
from hook_joint_geom import create_joint, TendonParams

params = TendonParams(
    r=0.01,
    h=0.02,
    phis=np.deg2rad([0.0, 120.0, 240.0]),
)
joint = create_joint(params)

n = joint.direction_from_angles(theta_x=0.2, theta_y=-0.1)
theta_x, theta_y = joint.angles_from_direction(n)
lengths = joint.rope_lengths_from_angles(theta_x, theta_y)
```

## API overview

- `direction_from_angles(theta_x, theta_y)`
- `angles_from_direction(n, eps=..., pole_theta_x=...)`
- `rope_lengths_from_angles(theta_x, theta_y, params=...)`
- `rope_lengths_from_direction(n, params=..., eps=..., pole_theta_x=...)`
- `create_joint(params, eps=..., pole_theta_x=...)`

## Conventions (must know)

- Local rotation order is `R_x(theta_x) @ R_y(theta_y)`.
- Direction vectors are normalized internally for inverse mapping.
- Near poles (`n ~= [+/-1, 0, 0]`), `theta_x` is branch-selected via `pole_theta_x`.

## Detailed docs

- [Coordinate conventions](docs/conventions.md)
- [Mapping theory and singularities](docs/mapping-theory.md)
- [Design notes](docs/design-notes.md)
- [Validation scope](docs/validation.md)

