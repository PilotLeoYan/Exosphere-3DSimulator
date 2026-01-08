import numpy as np
from dataclasses import dataclass
from . import constants as C


@dataclass
class ExosphereState:
    positions: np.ndarray
    velocities: np.ndarray


class ParticleSwarm:
    def __init__(self, n_particles: int) -> None:
        self.n_particles = n_particles
        self.state: ExosphereState = self._init_particles(self.n_particles)

    def _init_particles(self, n_particles: int) -> ExosphereState:
        r_max_scale: float = 10
        kappa: float = 2.0

        r_grid = np.linspace(1.0, r_max_scale, 10000) * C.R_EARTH
        
        r_normalized = r_grid / C.R_EARTH

        term_inner = 10**4 * np.exp(-r_normalized / 1.02)  
        term_outer = 70 * np.exp(-r_normalized / 8.2)
        density_profile = kappa * (term_inner + term_outer)

        prob_density = density_profile * (r_grid ** 2)

        # CDF (Cumulative Distribution Function)
        cdf = np.cumsum(prob_density)
        cdf = cdf / cdf[-1]

        random_uniform = np.random.random(n_particles)
        r_particles = np.interp(random_uniform, cdf, r_grid)

        phi = np.random.uniform(0, 2 * np.pi, n_particles)
        costheta = np.random.uniform(-1, 1, n_particles)
        theta = np.arccos(costheta)
        
        x = r_particles * np.sin(theta) * np.cos(phi)
        y = r_particles * np.sin(theta) * np.sin(phi)
        z = r_particles * np.cos(theta)
        
        positions = np.vstack((x, y, z)).T

        return ExosphereState(positions=positions, velocities=np.zeros_like(positions))
    
    def update(self, dt: float = 1.0) -> None:
        pos = self.state.positions
        vel = self.state.velocities

        solar_wind_force = np.array([500.0, 0, 0])

        vel += solar_wind_force * dt

        pos += vel * dt

        self.state.positions = pos
        self.state.velocities = vel