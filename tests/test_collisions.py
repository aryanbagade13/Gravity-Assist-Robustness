import numpy as np

from gravity_assist.collisions import position_intersects_body
from gravity_assist.models import CelestialBody, OrbitalState


def test_position_inside_body_counts_as_collision():
    body = CelestialBody(
        name="Test body",
        mass_kg=1.0,
        radius_km=10.0,
    )

    body_state = OrbitalState(
        position_km=np.array([100.0, 0.0, 0.0]),
        velocity_km_s=np.array([0.0, 0.0, 0.0]),
    )

    target_position_km = np.array([105.0, 0.0, 0.0])

    assert position_intersects_body(
        target_position_km,
        body,
        body_state,
    )

def test_position_outside_body_is_not_collision():
    body = CelestialBody(
        name="Test body",
        mass_kg=1.0,
        radius_km=10.0,
    )

    body_state = OrbitalState(
        position_km=np.array([100.0, 0.0, 0.0]),
        velocity_km_s=np.array([0.0, 0.0, 0.0]),
    )

    target_position_km = np.array([111.0, 0.0, 0.0])

    assert not position_intersects_body(
        target_position_km,
        body,
        body_state,
    )