import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from exosphere.particles import ParticleSwarm
from exosphere.visualizer import ExosphereVisualizer


def main() -> None:
    n_particles: int = 1_000_00
    particles = ParticleSwarm(n_particles)
    #particles.update(80)

    visualizer = ExosphereVisualizer(particles)

    visualizer.add_earth()
    #visualizer.add_moon()
    #visualizer.add_sun_arrow()

    visualizer.show()


if __name__ == '__main__':
    main()