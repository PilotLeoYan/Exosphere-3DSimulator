import pyvista as pv
from . import constants as C
from .particles import ParticleSwarm


class ExosphereVisualizer:
    def __init__(self, particles: ParticleSwarm) -> None:
        self.particles = particles

        self.plotter = pv.Plotter(window_size=[1600, 900])
        self.plotter.set_background('black') # type: ignore

        self.add_exosphere()

    def add_earth(self) -> None:
        earth = pv.Sphere(
            radius=C.R_EARTH,
            theta_resolution=100,
            phi_resolution=100,
            center=(0, 0, 0)
        )

        self.plotter.add_mesh(earth, color='blue')

    def add_moon(self) -> None:
        moon = pv.Sphere(
            radius=C.R_MOON,
            center=(C.D_MOON, 0, 0)
        )

        self.plotter.add_mesh(moon, color='white')

    def add_sun_arrow(self) -> None:
        arrow = pv.Arrow(
            start=(-C.R_EARTH * 10, 0, 0),
            direction=(2, 0, 0),
            scale=C.R_EARTH
        )

        self.plotter.add_mesh(arrow, color='yellow')

    def add_exosphere(self) -> None:
        cloud = pv.PolyData(self.particles.state.positions)

        self.plotter.add_mesh(
            cloud,
            color='#88ccee',
            point_size=2.0,
            opacity=0.5,
            render_points_as_spheres=True,
        )

    def show(self) -> None:
        self.plotter.show()