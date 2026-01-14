"""
Main script for ExoSpy satellite imaging simulation
"""

import matplotlib.pyplot as plt
from src.simulation.config import SatelliteConfig
from src.simulation.satellite import SatelliteImager
from src.simulation.visualization import SatelliteVisualizer


def main():
    """
    Main execution function
    """
    # ========== SATELLITE CONFIGURATION ==========
    print("Configuring satellite parameters...")
    config = SatelliteConfig()
    
    # Customize satellite parameters here
    config.position = {
        'x': 16.6 * 0.70710678,  # 6.6 * cos(45°)
        'y': 6.6 * 0.70710678,  # 6.6 * sin(45°)
        'z': 0.0
    }
    
    config.target = {
        'x': 0.0,
        'y': 6.6 * 0.70710678,  # 6.6 * sin(45°)
        'z': -0.15
    }
    
    # Imager specifications
    config.imager = {
        'fov': 18,           # Field of view in degrees
        'pixangres': 0.25    # Angular resolution (degrees between pixels)
    }
    
    # Solar irradiance
    config.solar = {
        'irradiance': 0.008519  # LISIRD COMPOSITE LY-ALPHA JAN 9, 2015
    }
    
    # Hydrogen model parameters
    config.model = {
        'type': 'Z15MAX',
        'dl': 0.05,       # Integration step size
        'maxRAD': 8,      # Maximum radius (RE)
        'minRAD': 3       # Minimum radius (RE)
    }
    
    # ========== RUN SIMULATION ==========
    print("Initializing satellite imager...")
    imager = SatelliteImager(config)
    
    print("Running simulation...")
    print(f"  - Satellite position: {config.position}")
    print(f"  - Target position: {config.target}")
    print(f"  - FOV: {config.imager['fov']}°")
    print(f"  - Pixel resolution: {config.imager['pixangres']}°")
    
    intensity = imager.run_simulation()
    
    print(f"✓ Simulation complete!")
    print(f"  - Image size: {imager.numpix} x {imager.numpix} pixels")
    print(f"  - Intensity range: {intensity.min():.2f} - {intensity.max():.2f} R") # type: ignore
    
    # ========== VISUALIZATION ==========
    print("\nGenerating visualizations...")
    visualizer = SatelliteVisualizer(imager)
    
    # Plot intensity map
    print("  - Creating intensity map...")
    visualizer.plot_intensity_map(
        title="Satellite Intensity Map",
        cmap='inferno'
    )
    
    # Plot 3D geometry
    print("  - Creating 3D geometry plot...")
    visualizer.plot_3d_geometry(
        orbit_radius=6.6,
        view_elev=60,
        view_azim=15
    )
    
    print("✓ Visualizations complete!")
    print("\nDisplaying plots...")
    plt.show()


if __name__ == "__main__":
    main()