import numpy as np
from .models import OrbitalState, CelestialBody
from .forces import total_gravitational_acceleration

def pack_system_state(
    planet_state: OrbitalState,
    spacecraft_state: OrbitalState,
) -> np.ndarray:
    return np.concatenate((
        planet_state.position_km,
        planet_state.velocity_km_s,
        spacecraft_state.position_km,
        spacecraft_state.velocity_km_s,
    ))


def restricted_three_body_derivative(time, system_state, sun_body, sun_state, planet_body):
    if system_state.shape != (12,):
        raise ValueError("system_state must have shape (12,)")

    planet_state = OrbitalState(
        position_km=system_state[0:3],
        velocity_km_s=system_state[3:6],
    )

    spacecraft_state = OrbitalState(
        position_km=system_state[6:9],
        velocity_km_s=system_state[9:12],
    )

    planet_acceleration = total_gravitational_acceleration(
        target_position_km=planet_state.position_km,
        bodies=[sun_body],
        body_states=[sun_state],
    )

    spacecraft_acceleration = total_gravitational_acceleration(
        target_position_km=spacecraft_state.position_km,
        bodies=[sun_body, planet_body],
        body_states=[sun_state, planet_state],
    )

    return np.concatenate((
        planet_state.velocity_km_s,
        planet_acceleration,
        spacecraft_state.velocity_km_s,
        spacecraft_acceleration,
    ))
