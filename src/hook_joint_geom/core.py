"""Core closed-form mappings for the hook joint geometry."""

from __future__ import annotations

import numpy as np

from .data import TendonParams


def direction_from_angles(theta_x: float, theta_y: float) -> np.ndarray:
    """Map joint angles to the local direction vector.

    Args:
        theta_x: Rotation angle about local ``x`` axis in radians.
        theta_y: Rotation angle about local ``y`` axis in radians.

    Returns:
        A unit-length direction vector ``n`` with shape ``(3,)``.

    Notes:
        Uses the closed-form relation for
        ``R(theta_x, theta_y) = R_x(theta_x) @ R_y(theta_y)`` and then
        normalizes for numerical robustness.

    Raises:
        ValueError: If the computed direction norm is zero.
    """
    n = np.array(
        [
            np.sin(theta_y),
            -np.sin(theta_x) * np.cos(theta_y),
            np.cos(theta_x) * np.cos(theta_y),
        ],
        dtype=float,
    )
    norm = np.linalg.norm(n)
    if norm == 0.0:
        raise ValueError("direction vector has zero length")
    return n / norm


def angles_from_direction(
    n: np.ndarray, *, eps: float = 1e-12, pole_theta_x: float = 0.0
) -> tuple[float, float]:
    """Map a direction vector back to canonical joint angles.

    Args:
        n: Input direction vector-like object with 3 components.
        eps: Positive tolerance used for zero-norm and pole checks.
        pole_theta_x: Fallback ``theta_x`` branch value when direction is near
            the pole (``n`` aligned with ``+/-x``).

    Returns:
        Tuple ``(theta_x, theta_y)`` in radians.

    Notes:
        The input vector is normalized internally so non-unit vectors are
        accepted. Pole handling is branch-based; comparisons should be done on
        reconstructed direction vectors rather than raw angle equality.

    Raises:
        ValueError: If ``n`` is not a length-3 vector or has near-zero norm.
    """
    n = np.asarray(n, dtype=float)
    if n.shape != (3,):
        raise ValueError("direction vector must have shape (3,)")

    norm = np.linalg.norm(n)
    if norm <= eps:
        raise ValueError("direction vector must be non-zero")
    n = n / norm

    theta_y = float(np.arcsin(n[0]))
    theta_x = float(np.arctan2(-n[1], n[2]))

    # At poles, theta_x is geometrically unobservable, so enforce a branch.
    if abs(n[1]) <= eps and abs(n[2]) <= eps:
        theta_x = float(pole_theta_x)

    return theta_x, theta_y


def rope_lengths_from_angles(
    theta_x: float, theta_y: float, *, params: TendonParams
) -> np.ndarray:
    """Compute tendon lengths for a given pair of joint angles.

    Args:
        theta_x: Rotation angle about local ``x`` axis in radians.
        theta_y: Rotation angle about local ``y`` axis in radians.
        params: Tendon geometry parameters ``(r, h, phis)``.

    Returns:
        One-dimensional array of rope lengths, one per tendon in ``params``.

    Notes:
        Top anchors are rotated by ``R_x(theta_x) @ R_y(theta_y)`` while bottom
        anchors remain fixed in the same local frame.

    Raises:
        ValueError: If ``params.phis`` is not one-dimensional.
    """
    r = params.r
    h = params.h
    phis = np.asarray(params.phis, dtype=float)
    if phis.ndim != 1:
        raise ValueError("params.phis must be a 1D array")

    cos_phi = np.cos(phis)
    sin_phi = np.sin(phis)

    p_top = np.stack([r * cos_phi, r * sin_phi, np.full_like(phis, h)], axis=1)
    p_bot = np.stack([r * cos_phi, r * sin_phi, np.full_like(phis, -h)], axis=1)

    cx = np.cos(theta_x)
    sx = np.sin(theta_x)
    cy = np.cos(theta_y)
    sy = np.sin(theta_y)

    rx = np.array([[1.0, 0.0, 0.0], [0.0, cx, -sx], [0.0, sx, cx]], dtype=float)
    ry = np.array([[cy, 0.0, sy], [0.0, 1.0, 0.0], [-sy, 0.0, cy]], dtype=float)

    rot = rx @ ry
    q = (rot @ p_top.T).T
    d = q - p_bot
    return np.linalg.norm(d, axis=1)


def rope_lengths_from_direction(
    n: np.ndarray,
    *,
    params: TendonParams,
    eps: float = 1e-12,
    pole_theta_x: float = 0.0,
) -> np.ndarray:
    """Compute tendon lengths from direction by delegating through inverse map.

    Args:
        n: Input direction vector-like object with 3 components.
        params: Tendon geometry parameters ``(r, h, phis)``.
        eps: Tolerance forwarded to :func:`angles_from_direction`.
        pole_theta_x: Pole branch choice forwarded to
            :func:`angles_from_direction`.

    Returns:
        One-dimensional array of rope lengths.
    """
    theta_x, theta_y = angles_from_direction(n, eps=eps, pole_theta_x=pole_theta_x)
    return rope_lengths_from_angles(theta_x, theta_y, params=params)
