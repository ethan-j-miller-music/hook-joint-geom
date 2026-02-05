"""Core closed-form mappings for the hook joint geometry."""

from __future__ import annotations

import numpy as np

from .data import TendonParams


# Layer 0：四个函数实现（唯一实现源）

def direction_from_angles(theta_x: float, theta_y: float) -> np.ndarray:
    """Compute the direction vector from joint angles.

    Uses the closed-form mapping defined in the README and normalizes the
    resulting vector to unit length.
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
    """Compute joint angles from a direction vector.

    Normalizes the input direction, then uses the analytic inverse mapping.
    Handles pole degeneracy by assigning theta_x to ``pole_theta_x`` when the
    direction aligns with ±x.
    """
    n = np.asarray(n, dtype=float)
    norm = np.linalg.norm(n)
    if norm <= eps:
        raise ValueError("direction vector must be non-zero")
    n = n / norm

    theta_y = float(np.arcsin(n[0]))
    theta_x = float(np.arctan2(-n[1], n[2]))

    if abs(n[1]) <= eps and abs(n[2]) <= eps:
        theta_x = float(pole_theta_x)

    return theta_x, theta_y


def rope_lengths_from_angles(
    theta_x: float, theta_y: float, *, params: TendonParams
) -> np.ndarray:
    """Compute tendon rope lengths from joint angles.

    Each tendon length is the distance between a rotated top anchor point and
    a fixed bottom anchor point.
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
    """Compute tendon rope lengths directly from a direction vector."""
    theta_x, theta_y = angles_from_direction(
        n, eps=eps, pole_theta_x=pole_theta_x
    )
    return rope_lengths_from_angles(theta_x, theta_y, params=params)
