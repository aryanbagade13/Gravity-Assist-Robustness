import matplotlib.pyplot as plt
import numpy as np

from gravity_assist.integrators import propagate_fixed_step
from gravity_assist.models import CelestialBody, OrbitalState
from gravity_assist.simulation import (
    pack_system_state,
    restricted_three_body_derivative,
)

EPOCH = "2000-01-01 12:00:00 TDB"
SECONDS_PER_DAY = 24 * 60 * 60


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
    spacecraft_state,
)


def derivative_for_this_flyby(time_s, state):
    return restricted_three_body_derivative(
        time_s,
        state,
        sun_body,
        sun_state,
        jupiter_body,
    )


start_time_s = 0.0
end_time_s = 50 * SECONDS_PER_DAY
dt_s = 60.0

times, states = propagate_fixed_step(
    initial_state=system_state,
    start_time_s=start_time_s,
    end_time_s=end_time_s,
    dt_s=dt_s,
    derivative_function=derivative_for_this_flyby,
)

jupiter_positions_km = states[:, 0:3]
spacecraft_positions_km = states[:, 6:9]

spacecraft_positions_relative_to_jupiter_km = (
    spacecraft_positions_km - jupiter_positions_km
)
spacecraft_distances_from_jupiter_km = np.linalg.norm(
    spacecraft_positions_relative_to_jupiter_km,
    axis=1,
)

closest_approach_index = np.argmin(
    spacecraft_distances_from_jupiter_km
)

closest_approach_distance_km = (
    spacecraft_distances_from_jupiter_km[closest_approach_index]
)

closest_approach_altitude_km = (
    closest_approach_distance_km - jupiter_body.radius_km
)

closest_approach_time_days = (
    times[closest_approach_index] / SECONDS_PER_DAY
)

# Construct a correctly scaled spherical surface for Jupiter.
longitude = np.linspace(0, 2 * np.pi, 80)
latitude = np.linspace(0, np.pi, 40)

#using spherical co-ordinates
jupiter_surface_x_km = (
    jupiter_body.radius_km
    * np.outer(np.cos(longitude), np.sin(latitude))
)

jupiter_surface_y_km = (
    jupiter_body.radius_km
    * np.outer(np.sin(longitude), np.sin(latitude))
)

jupiter_surface_z_km = (
    jupiter_body.radius_km
    * np.outer(np.ones_like(longitude), np.cos(latitude))
)

# Select only the nearby section of the trajectory for the close-up.
close_up_limit_km = 500_000.0
close_up_mask = (
    spacecraft_distances_from_jupiter_km <= close_up_limit_km
)
close_up_positions_km = (
    spacecraft_positions_relative_to_jupiter_km[close_up_mask]
)

closest_position_relative_to_jupiter_km = (
    spacecraft_positions_relative_to_jupiter_km[
        closest_approach_index
    ]
)

figure = plt.figure(figsize=(9, 8))
axes = figure.add_subplot(projection="3d")

axes.plot_surface(
    jupiter_surface_x_km,
    jupiter_surface_y_km,
    jupiter_surface_z_km,
    color="orange",
    alpha=0.8,
    linewidth=0,
)

axes.plot(
    close_up_positions_km[:, 0],
    close_up_positions_km[:, 1],
    close_up_positions_km[:, 2],
    color="blue",
    label="Spacecraft trajectory",
)

axes.scatter(
    closest_position_relative_to_jupiter_km[0],
    closest_position_relative_to_jupiter_km[1],
    closest_position_relative_to_jupiter_km[2],
    color="red",
    s=50,
    label="Closest approach",
)

axes.set_xlim(-close_up_limit_km, close_up_limit_km)
axes.set_ylim(-close_up_limit_km, close_up_limit_km)
axes.set_zlim(-close_up_limit_km, close_up_limit_km)
axes.set_box_aspect((1, 1, 1))
axes.set_xlabel("x relative to Jupiter (km)")
axes.set_ylabel("y relative to Jupiter (km)")
axes.set_zlabel("z relative to Jupiter (km)")
axes.set_title("Close-up of Jupiter gravity-assist trajectory")
axes.legend()
figure.tight_layout()
plt.show()

print(f"Epoch: {EPOCH}")
print(f"Closest-approach time: {closest_approach_time_days:.3f} days")
print(f"Distance from Jupiter's centre: {closest_approach_distance_km:,.1f} km")
print(f"Altitude above Jupiter's surface: {closest_approach_altitude_km:,.1f} km")
print(f"Stored times shape: {times.shape}")
print(f"Stored states shape: {states.shape}")
