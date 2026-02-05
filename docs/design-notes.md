# Design Notes

## Minimum & local coordinate system principle

This package deliberately models only one Hooke joint module in a fixed local frame. It does not include multi-joint composition, optimization loops, or controller-side abstractions.

## Layering and ownership

- `core.py`
  - single source of truth for all geometric equations
  - procedural functions for forward/inverse mappings and rope lengths
- `joint.py`
  - `HookJoint` wrapper
  - binds `TendonParams`, `eps`, and `pole_theta_x`
  - delegates to `core.py` only
- `api.py`
  - stable user-facing imports and construction helper (`create_joint`)

This separation minimizes drift between procedural and object-oriented entry points.

## Data model choices

- `TendonParams` is a frozen dataclass:
  - immutable parameter container after validation
  - safer sharing across callers
- `phis` coerced to a NumPy 1D float array in `__post_init__` for predictable downstream behavior.

## Import policy

Relative imports are used inside the package to keep module boundaries explicit and avoid path coupling.
