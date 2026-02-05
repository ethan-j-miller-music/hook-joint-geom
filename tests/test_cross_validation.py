import numpy as np
import pytest

from hook_joint_geom import (
    angles_from_direction,
    create_joint,
    direction_from_angles,
    rope_lengths_from_angles,
    rope_lengths_from_direction,
)
from hook_joint_geom import core
from hook_joint_geom.data import TendonParams


@pytest.fixture
def tendon_params() -> TendonParams:
    return TendonParams(r=0.01, h=0.02, phis=np.deg2rad([0.0, 120.0, 240.0]))


def test_angle_direction_round_trip_random() -> None:
    rng = np.random.default_rng(7)
    theta_x = rng.uniform(-np.pi + 0.2, np.pi - 0.2, size=128)
    theta_y = rng.uniform(-np.pi / 2 + 0.2, np.pi / 2 - 0.2, size=128)

    for tx, ty in zip(theta_x, theta_y, strict=True):
        n = direction_from_angles(tx, ty)
        tx2, ty2 = angles_from_direction(n)
        n2 = direction_from_angles(tx2, ty2)
        assert np.isclose(np.linalg.norm(n), 1.0, atol=1e-12)
        assert np.linalg.norm(n - n2) <= 1e-12


def test_pole_branch_selection_is_direction_consistent() -> None:
    eps = 1e-12
    pole_theta_x = 0.9
    n_near_pole = np.array([1.0, 1e-15, -1e-15])

    tx, ty = angles_from_direction(n_near_pole, eps=eps, pole_theta_x=pole_theta_x)
    n2 = direction_from_angles(tx, ty)

    n_unit = n_near_pole / np.linalg.norm(n_near_pole)
    assert np.linalg.norm(n2 - n_unit) <= 1e-9


def test_rope_lengths_angles_vs_direction_cross_validation(
    tendon_params: TendonParams,
) -> None:
    rng = np.random.default_rng(11)
    theta_x = rng.uniform(-np.pi + 0.2, np.pi - 0.2, size=64)
    theta_y = rng.uniform(-np.pi / 2 + 0.2, np.pi / 2 - 0.2, size=64)

    for tx, ty in zip(theta_x, theta_y, strict=True):
        l1 = rope_lengths_from_angles(tx, ty, params=tendon_params)
        n = direction_from_angles(tx, ty)
        l2 = rope_lengths_from_direction(
            n,
            params=tendon_params,
            eps=1e-12,
            pole_theta_x=0.25,
        )
        assert np.allclose(l1, l2, atol=1e-12)


def test_hook_joint_wrapper_delegates_to_core(tendon_params: TendonParams) -> None:
    joint = create_joint(tendon_params, eps=1e-10, pole_theta_x=0.3)
    tx, ty = 0.4, -0.35
    n = np.array([0.2, -0.3, 0.7])

    assert np.allclose(
        joint.direction_from_angles(tx, ty), core.direction_from_angles(tx, ty), atol=0.0
    )
    assert np.allclose(
        joint.angles_from_direction(n),
        core.angles_from_direction(n, eps=joint.eps, pole_theta_x=joint.pole_theta_x),
        atol=0.0,
    )
    assert np.allclose(
        joint.rope_lengths_from_angles(tx, ty),
        core.rope_lengths_from_angles(tx, ty, params=tendon_params),
        atol=0.0,
    )
    assert np.allclose(
        joint.rope_lengths_from_direction(n),
        core.rope_lengths_from_direction(
            n,
            params=tendon_params,
            eps=joint.eps,
            pole_theta_x=joint.pole_theta_x,
        ),
        atol=0.0,
    )


def test_angles_from_direction_accepts_non_unit_vector() -> None:
    n = np.array([2.0, -3.0, 7.0])
    tx, ty = angles_from_direction(n)
    n2 = direction_from_angles(tx, ty)
    assert np.isclose(np.linalg.norm(n2), 1.0, atol=1e-12)


def test_angles_from_direction_rejects_invalid_shape() -> None:
    with pytest.raises(ValueError, match=r"shape \(3,\)"):
        angles_from_direction(np.array([1.0, 2.0]))


@pytest.mark.parametrize("bad", [np.zeros(3), np.array([1e-16, 0.0, 0.0])])
def test_angles_from_direction_rejects_zero_norm(bad: np.ndarray) -> None:
    with pytest.raises(ValueError, match="non-zero"):
        angles_from_direction(bad)
