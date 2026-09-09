import numpy as np

from gravity_assist.models import CelestialBody, OrbitalState
from gravity_assist.integrators import rk4_step
from gravity_assist.simulation import (
    pack_system_state,
    restricted_three_body_derivative,
)

epoch = "2000-01-01 12:00:00 TDB"


sun_body = CelestialBody(
    name="Sun",
    mass_kg=1.989e30,
    radius_km=695_700.0,
)

sun_state = OrbitalState(
    position_km=[0.0, 0.0, 0.0],
    velocity_km_s=[0.0, 0.0, 0.0],
)


jupiter_body = CelestialBody(
    name="Jupiter",
    mass_kg=1.8986e27,
    radius_km=69_911.0,
)

jupiter_state = OrbitalState(
    position_km=[
        5.985676246570644e8,
        4.396046799481729e8,
        -1.522686167298746e7,
    ],
    velocity_km_s=[
        -7.909860292172008,
        11.15621752636729,
        0.1308656815823666,
    ],
)


spacecraft_position_relative_to_jupiter_km = np.array([
    -10_000_000.0,
    1_500_000.0,
    300_000.0,
])

spacecraft_velocity_relative_to_jupiter_km_s = np.array([
    5.0,
    0.0,
    0.0,
])

spacecraft_state = OrbitalState(
    position_km=(
        jupiter_state.position_km
        + spacecraft_position_relative_to_jupiter_km
    ),
    velocity_km_s=(
        jupiter_state.velocity_km_s
        + spacecraft_velocity_relative_to_jupiter_km_s
    ),
)


system_state = pack_system_state(
    jupiter_state,
    spacecraft_state
)

def derivative_for_this_flyby(time_s, state):
    return restricted_three_body_derivative(
        time_s,
        state,
        sun_body,
        sun_state,
        jupiter_body,
    )

original_state = system_state.copy()

next_system_state = rk4_step(
    state=system_state,
    time_s=0.0,
    dt_s=60.0,
    derivative_function=derivative_for_this_flyby,
)

print("Original shape:", system_state.shape)
print("Next shape:", next_system_state.shape)
print("Original unchanged:", np.array_equal(system_state, original_state))
print("State changed:", not np.array_equal(next_system_state, system_state))
