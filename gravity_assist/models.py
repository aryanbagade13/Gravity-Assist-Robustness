from dataclasses import dataclass
import numpy as np
from .constants import G

@dataclass(frozen=True)
class CelestialBody:
    name: str
    mass_kg: float
    radius_km: float

    @property
    def mu(self):
        return G * self.mass_kg

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        if self.mass_kg <= 0:
            raise ValueError("mass_kg <= 0")
        if self.radius_km <= 0:
            raise ValueError("radius_km <= 0")

@dataclass
class OrbitalState:
    position_km: np.ndarray
    velocity_km_s: np.ndarray

    def __post_init__(self):
        self.position_km = np.asarray(self.position_km, dtype=float)
        self.velocity_km_s = np.asarray(self.velocity_km_s, dtype=float)
        if self.position_km.shape != (3, ):
            raise ValueError("position_km has wrong shape")
        if self.velocity_km_s.shape != (3, ):
            raise ValueError("velocity_km has wrong shape")
        if not np.isfinite(self.position_km).all():
            raise ValueError("position_km must contain only finite values")
        if not np.isfinite(self.velocity_km_s).all():
            raise ValueError("velocity_km_s must contain only finite values")