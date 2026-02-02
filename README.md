# hook-joint-geom

Minimal geometric mappings for a 2-DOF Hooke (universal) joint

> This package provides a minimal, local, and geometry-complete mapping between joint angles ($\theta_x$, $\theta_y$) and a direction vector $\mathbf n \in S^2$ for a single universal (Hooke) joint module in a snake-arm robot.

The design strictly follows the **minimum & local coordinate system principle**:

- The package is responsible for exactly one joint
- The local coordinate frame is fixed and immutable
- All mappings are closed-form
- No numerical solvers, iterations, or tolerances

---

# 1. Local Joint Coordinate Convention (Fixed 90° Angle)

All definitions are based on a **local joint frame $\{x, y, z\}$**, which must not be redefined elsewhere.

The two rotational axes are fixed and orthogonal.

### Axes definition

- **x-axis**
  First rotational axis
- **y-axis**
  Second rotational axis, always perpendicular to the x-axis
- **z-axis**
  Defined by the right-hand rule: $x \rightarrow y$

---

## 2. Pose Definition

The joint pose is parameterized by two angles.

$$
R(\theta_x, \theta_y) = R_x(\theta_x)\, R_y(\theta_y)
$$

where:

- $R_x(\theta_x)$: rotation about local x-axis
- $R_y(\theta_y)$: rotation about local y-axis

The angle between the two axes is fixed at $90^\circ$.

---

## 3. Direction Vector Definition

The pose is represented by a direction vector defined as the rotated local $+z$ axis.

$$
\mathbf n = R(\theta_x, \theta_y)\, \mathbf e_z,
\qquad
\mathbf e_z =
\begin{bmatrix}
0 \\ 0 \\ 1
\end{bmatrix}
$$

Properties:

- $\mathbf n \in S^2$
- Exactly 2 DOF
- Invertible back to joint angles

---

## 4. Forward Mapping

### Angles → Direction Vector

$$
\mathbf n =
\begin{bmatrix}
\sin \theta_y \\
-\sin \theta_x \cos \theta_y \\
\cos \theta_x \cos \theta_y
\end{bmatrix}
$$

This mapping is smooth and globally defined.

---

## 5. Inverse Mapping

### Direction Vector → Angles

Given a non-zero direction vector $\mathbf n$, it is first normalized.

$$
\mathbf n \leftarrow \frac{\mathbf n}{\lVert \mathbf n \rVert}
$$

The inverse mapping is:

$$
\theta_y = \arcsin(n_x)
$$

$$
\theta_x = \operatorname{atan2}(-n_y,\; n_z)
$$

The mapping depends only on direction, not magnitude.

---

## 6. Rope Length Mapping

### 6.1 Local frame and angle conventions

- Local frame: $\{x, y, z\}$
- Rotation model:

$$
R(\theta_x, \theta_y) = R_x(\theta_x)\, R_y(\theta_y)
$$

- Azimuth angle $\phi$ is measured in the $xy$-plane
  $\phi = 0$ aligned with $+x$, positive direction by right-hand rule about $+z$

---

### 6.2 Tendon anchor points

For tendon $i$ with azimuth $\phi_i$:

- $r$: radial distance in $xy$-plane
- $h$: vertical offset along $z$

Top and bottom anchor points:

$$
\mathbf p_i^{\text{top}} =
\begin{bmatrix}
r \cos \phi_i \\
r \sin \phi_i \\
h
\end{bmatrix},
\qquad
\mathbf p_i^{\text{bot}} =
\begin{bmatrix}
r \cos \phi_i \\
r \sin \phi_i \\
- h
\end{bmatrix}
$$

---

### 6.3 Rope length formula

The rope connects the rotated top point to the fixed bottom point.

$$
\ell_i(\theta_x, \theta_y)
=
\left\|
R(\theta_x, \theta_y)\, \mathbf p_i^{\text{top}}
-
\mathbf p_i^{\text{bot}}
\right\|
$$

Computational steps:

1. $R = R_x(\theta_x)\, R_y(\theta_y)$
2. $\mathbf q_i = R\, \mathbf p_i^{\text{top}}$
3. $\mathbf d_i = \mathbf q_i - \mathbf p_i^{\text{bot}}$
4. $\ell_i = \sqrt{\mathbf d_i^\top \mathbf d_i}$

---

## 7. Canonical Angle Ranges

To ensure uniqueness:

$$
\theta_y \in \left[-\frac{\pi}{2},\; \frac{\pi}{2}\right]
$$

$$
\theta_x \in (-\pi,\; \pi]
$$

Within these ranges, the mapping is unique almost everywhere.

---

## 8. Pole Degeneracy

At:

$$
\cos \theta_y = 0
\quad \Longleftrightarrow \quad
\theta_y = \pm \frac{\pi}{2}
$$

the direction vector becomes:

$$
\mathbf n =
\begin{bmatrix}
\pm 1 \\ 0 \\ 0
\end{bmatrix}
$$

At the pole:

- $n_y = 0$
- $n_z = 0$
- $\theta_x$ is unobservable

This is an intrinsic geometric degeneracy.

### Convention at the pole

$$
\theta_x := 0
$$

---

## 9. Scope of This Package

### Included

- Closed-form mappings
- Deterministic inverse with pole handling
- Floating-point tolerant normalization

### Explicitly excluded

- Numerical solvers
- Iterative optimization
- Residual minimization

---

## 10. Minimal API Design

- `direction_from_angles(theta_x, theta_y)`
- `angles_from_direction(n)`
- `rope_lengths_from_angles(theta_x, theta_y)`
- `rope_lengths_from_direction(n)`

Higher-level logic is pure composition.

---

## 11. Design Philosophy

> This package behaves like a caliper.

- Precisely aligned
- Locally defined
- Unaware of global structure

Global coordination and optimization belong to outer layers.

This package targets **small-angle tendon-driven universal joints**.
Pole configurations are physically unreachable due to tension and force-closure constraints.

Mathematical singularities exist but do not appear in the operating regime.
