# Mapping Theory Overview

## Angle to direction mapping

For one joint module:

$$
R(\theta_x, \theta_y) = R_x(\theta_x)R_y(\theta_y)
$$



The direction state uses the rotated `+z` axis:

$$
n = R(\theta_x, \theta_y)e_z
$$


which expands to:

$$
n_x = \sin\theta_y,\quad
n_y = -\sin\theta_x\cos\theta_y,\quad
n_z = \cos\theta_x\cos\theta_y
$$

## Direction to angle inverse

Given non-zero `n`, **the input vector is not required to be unit-length**.
The implementation will internally normalize `n` before applying:

$$
\theta_y = \arcsin(n_x),\quad
\theta_x = \operatorname{atan2}(-n_y, n_z)
$$

This recovers a canonical pair except at poles.

## Singularities and poles

Pole condition occurs when `cos(theta_y)=0`, equivalent to `n = [±1, 0, 0]`.
At poles:

- `theta_x` does not affect `n`
- inverse is underdetermined in `theta_x`

The implementation resolves this with a branch parameter `pole_theta_x`.

## Rope length map

For each tendon azimuth `phi_i` with radius `r` and half-height `h`:

$$
p_i^{top}=[r\cos\phi_i, r\sin\phi_i, h]^T,
\quad
p_i^{bot}=[r\cos\phi_i, r\sin\phi_i, -h]^T
$$

Length is:

$$
\ell_i = \left\|R(\theta_x,\theta_y)p_i^{top} - p_i^{bot}\right\|_2
$$

The direction-based rope function composes inverse mapping with this formula.

