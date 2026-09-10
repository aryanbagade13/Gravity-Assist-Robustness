import numpy as np
from .models import CelestialBody, OrbitalState

def position_intersects_body(
    target_position_km: np.ndarray,
    body: CelestialBody,
    body_state: OrbitalState,
) -> bool:
    target_to_body_distance_km = np.linalg.norm(target_position_km - body_state.position_km)
    if target_to_body_distance_km <= body.radius_km:
        return True
    return False
