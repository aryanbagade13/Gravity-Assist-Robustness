import numpy as np

from gravity_assist.manoeuvres import apply_impulsive_manoeuvre
from gravity_assist.models import OrbitalState


def test_impulsive_manoeuvre_changes_only_velocity():
    state = OrbitalState(
        position_km=np.array([1.0, 2.0, 3.0]),
        velocity_km_s=np.array([4.0, 5.0, 6.0]),
    )
    delta_velocity_km_s = np.array([0.1, -0.2, 0.3])

    manoeuvred_state = apply_impulsive_manoeuvre(
        state,
        delta_velocity_km_s,
    )

    np.testing.assert_allclose(
        manoeuvred_state.position_km,
        [1.0, 2.0, 3.0],
    )
    np.testing.assert_allclose(
        manoeuvred_state.velocity_km_s,
        [4.1, 4.8, 6.3],
    )
    np.testing.assert_allclose(
        state.position_km,
        [1.0, 2.0, 3.0],
    )
    np.testing.assert_allclose(
        state.velocity_km_s,
        [4.0, 5.0, 6.0],
    )
