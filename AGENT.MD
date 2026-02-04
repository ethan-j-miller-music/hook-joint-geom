# AGENT.MD — hook-joint-geom

## Objective

Complete the implementation of the **four core procedural functions** in `core.py`.These four functions are the **only implementation source** for the package’s math, as stated in `core.py` and `README.md`:

- `direction_from_angles(theta_x, theta_y) -> n (3,)`
- `angles_from_direction(n, *, eps=1e-12, pole_theta_x=0.0) -> (theta_x, theta_y)`
- `rope_lengths_from_angles(theta_x, theta_y, *, params: TendonParams) -> L (N,)`
- `rope_lengths_from_direction(n, *, params: TendonParams, eps=1e-12, pole_theta_x=0.0) -> L (N,)`

The math and conventions are defined in `README.md` sections:

- **## 4. Forward Mapping**
- **## 5. Inverse Mapping**
- **## 6. Rope Length Mapping**
- and composition for direction → rope length.

## Scope & Non-Goals

### Must do

- Implement the above four functions in **closed form**.
- Follow the fixed local frame and rotation convention:
  - `R(theta_x, theta_y) = Rx(theta_x) * Ry(theta_y)`
  - `n = R * e_z`
- Use floating-point tolerant normalization and pole handling per README.
- Replace structural parameters `r, h, phis` with `data.py::TendonParams`:
  - `params.r`, `params.h`, `params.phis`
- Return numpy arrays with correct shapes:
  - `n` is shape `(3,)`
  - `L` is shape `(N,)`, where `N = len(params.phis)`

### Must NOT do

- No numerical solvers, no iterations, no tolerances beyond `eps` for pole detection.
- No API redesign beyond the minimal signature change to use `TendonParams`.
- Do not add new public API beyond what `__init__.py` exports (if present).

## Detailed Requirements

### 1) `direction_from_angles(theta_x, theta_y)`

Implement exactly the forward mapping:

n = [
sin(theta_y),
-sin(theta_x) * cos(theta_y),
cos(theta_x) * cos(theta_y)
]

- Return `np.ndarray` of dtype float, shape `(3,)`.
- Normalize the resulting direction vector to unit length before returning.

### 2) `angles_from_direction(n, *, eps=1e-12, pole_theta_x=0.0)`

Implement inverse mapping, per README:

- First normalize input direction:

  - If `||n|| <= eps`, raise `ValueError` (invalid direction).
  - Else `n = n / ||n||`.
- Compute:

  - `theta_y = arcsin(n_x)`
  - `theta_x = atan2(-n_y, n_z)`
- Pole degeneracy handling:

  - Pole condition corresponds to `cos(theta_y) ≈ 0`, equivalently `|n_y| <= eps` and `|n_z| <= eps` (since at pole n = [±1, 0, 0]).
  - If pole detected, set `theta_x = pole_theta_x` (default 0.0) deterministically.
  - `theta_y` should still be computed consistently (it will be ±pi/2 from arcsin).
- Output ranges should match canonical conventions:

  - `theta_y ∈ [-pi/2, pi/2]` naturally from `arcsin`
  - `theta_x ∈ (-pi, pi]` naturally from `atan2` (and pole assignment should respect that).

### 3) `rope_lengths_from_angles(theta_x, theta_y, *, params: TendonParams)`

Use the rope length formula from README:

For each tendon i with azimuth `phi_i`:

- Top anchor point:
  p_top = [ r cos(phi_i), r sin(phi_i),  h ]
- Bottom anchor point (fixed):
  p_bot = [ r cos(phi_i), r sin(phi_i), -h ]

Rope connects rotated top point to fixed bottom:
l_i = || R(theta_x, theta_y) * p_top - p_bot ||

Implementation notes:

- Use numpy vectorization over `phis` (preferred) but clarity is more important than micro-optimizations.
- Construct Rx and Ry consistent with right-hand rule:
  - Rx rotates around x-axis
  - Ry rotates around y-axis
  - Ensure order: Rx(theta_x) @ Ry(theta_y)
- Return `L` as `np.ndarray` shape `(N,)`.

### 4) `rope_lengths_from_direction(n, *, params: TendonParams, eps=1e-12, pole_theta_x=0.0)`

This function is pure composition:

- (theta_x, theta_y) = angles_from_direction(n, eps=eps, pole_theta_x=pole_theta_x)
- L = rope_lengths_from_angles(theta_x, theta_y, params=params)
- Return L.

## Code Quality Expectations

- Add concise docstrings matching README terminology.
- Add type hints (at least for inputs/outputs).
- Validate shapes where helpful (e.g., ensure `phis` is 1D via TendonParams, but still be defensive if needed).
- Keep dependencies minimal: numpy only.
- Prefer deterministic behavior over “best effort”.

## Acceptance Checklist

- All four functions exist in `core.py` and run without stubs.
- Signatures use `TendonParams` for structural parameters.
- Numerical behavior:
  - `angles_from_direction` handles non-unit vectors by normalization.
  - Pole condition sets `theta_x = pole_theta_x` deterministically.
  - Invalid zero vector input raises `ValueError`.
- Matches README formulas and conventions exactly.
- Output shapes correct and stable.

## Files

- `core.py`: implement the four functions (the only implementation source).
- `README.md`: authoritative math definitions and conventions.
- `data.py`: contains `TendonParams` dataclass; use it in `core.py`.
