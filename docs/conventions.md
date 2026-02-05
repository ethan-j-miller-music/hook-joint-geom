# Coordinate and API Conventions

## Local frame

- Frame is right-handed: `(x, y, z)`.
- Joint orientation uses ordered rotations:
  - first about `x` by `theta_x`
  - then about `y` by `theta_y`
- Effective rotation matrix is `R(theta_x, theta_y) = R_x(theta_x) @ R_y(theta_y)`.

## Direction vector

- Direction vector is rotated local `+z` axis.
- Forward map:

\[
n =
\begin{bmatrix}
\sin\theta_y \\
-\sin\theta_x\cos\theta_y \\
\cos\theta_x\cos\theta_y
\end{bmatrix}
\]

- `n` is treated as a direction only (magnitude ignored in inverse map).

## Angle ranges and branch convention

- Canonical inverse ranges:
  - `theta_y in [-pi/2, pi/2]`
  - `theta_x in (-pi, pi]` from `atan2`.
- At poles (`|n_y|` and `|n_z|` near zero), `theta_x` is unobservable and set to `pole_theta_x`.

## Normalization and tolerances

- `angles_from_direction` normalizes non-zero input vectors.
- `eps` controls:
  - minimum norm accepted for `n`
  - pole detection tolerance for branch assignment.
