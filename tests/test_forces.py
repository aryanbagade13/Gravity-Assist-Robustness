import numpy as np
import pytest

from gravity_assist.constants import G
from gravity_assist.forces import total_gravitational_acceleration
from gravity_assist.models import CelestialBody, OrbitalState

def test_single_body_gravitational_acceleration():
    mass_kg = 1.0/G
    test_celestial_body = CelestialBody(
        name = "test_celestial_body",
        mass_kg = mass_kg,
        radius_km = 1,
        )

    test_orbital_state = OrbitalState(
        position_km= np.array([0, 0, 0]),
        velocity_km_s= np.array([0, 0, 0])
    )

    target_position_km = np.array([2, 0, 0])
    expected_acceleration = np.array([-0.25, 0.0, 0.0])

    actual_acceleration = total_gravitational_acceleration(
        target_position_km,
        [test_celestial_body],
        [test_orbital_state],
    )

    np.testing.assert_allclose(
        actual_acceleration,
        expected_acceleration,
    )
