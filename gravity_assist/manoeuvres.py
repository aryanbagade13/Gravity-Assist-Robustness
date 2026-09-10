import numpy as np
from dataclasses import dataclass

@dataclass
class ImpulsiveManoeuvre:
    time_s: float
    delta_velocity_km_s: np.ndarray

    def __post_init__(self):
        self.delta_velocity_km_s = np.asarray(
            self.delta_velocity_km_s,
            dtype=float,
        ).copy()

        if self.delta_velocity_km_s.shape != (3,):
            raise ValueError(
                "delta_velocity_km_s must have shape (3,)"
            )

        if self.time_s < 0:
            raise ValueError("Impulsive manoeuvre time must be non-negative")

        if not np.isfinite(self.time_s):
            raise ValueError("time_s must be finite")

        if not np.isfinite(self.delta_velocity_km_s).all():
            raise ValueError(
                "delta_velocity_km_s must contain only finite values"
            )
    @property
    def magnitude_km_s(self) -> float:
        return float(
            np.linalg.norm(self.delta_velocity_km_s)
        )


from .models import OrbitalState

def apply_impulsive_manoeuvre(
        state: OrbitalState,
        delta_velocity_km_s: np.ndarray,
) -> OrbitalState:
    delta_velocity_km_s = np.asarray(
        delta_velocity_km_s,
        dtype=np.float64,
    )

    if delta_velocity_km_s.shape != (3, ):
        raise ValueError("delta_velocity_km_s must have shape (3,)")

    if not np.isfinite(delta_velocity_km_s).all():
        raise ValueError(
            "delta_velocity_km_s must contain only finite values"
        )

    return OrbitalState(
        position_km=state.position_km.copy(),
        velocity_km_s=(
                state.velocity_km_s + delta_velocity_km_s
        ),
    )
