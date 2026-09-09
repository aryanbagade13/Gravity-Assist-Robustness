import numpy as np
from .models import OrbitalState, CelestialBody

def total_gravitational_acceleration(
        target_position_km: np.ndarray,
        bodies: list[CelestialBody],
        body_states: list[OrbitalState],
) -> np.ndarray:

    total_acceleration = np.zeros(3)

    if len(bodies) != len(body_states):
        raise ValueError("bodies and body_states must have equal lengths")

    for body, body_state in zip(bodies, body_states):

        displacement = target_position_km - body_state.position_km
        distance = np.linalg.norm(displacement)

        if distance == 0:
            raise ValueError("target position cannot equal a body's position")

        acceleration_from_body = -body.mu/distance**3 * displacement
        total_acceleration += acceleration_from_body

    return total_acceleration