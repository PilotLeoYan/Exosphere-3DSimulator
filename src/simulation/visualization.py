"""
Visualization module for satellite imaging results
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class SatelliteVisualizer:
    """Class to handle visualization of satellite data"""
    
    def __init__(self, satellite_imager):
        """
        Initialize visualizer
        
        Parameters:
        -----------
        satellite_imager : SatelliteImager
            Satellite imager object with computed intensity
        """
        self.imager = satellite_imager
        
    def plot_intensity_map(self, title="Intensity Map", cmap='inferno', 
                          vmin=None, vmax=None, figsize=(7, 7)):
        """
        Plot 2D intensity map
        
        Parameters:
        -----------
        title : str
            Plot title
        cmap : str
            Colormap name
        vmin, vmax : float
            Min and max values for colorbar (in kR)
        figsize : tuple
            Figure size
        """
        if self.imager.intensity is None:
            raise ValueError("No intensity data to plot")
        
        numpix = self.imager.numpix
        intensity_kR = np.fliplr(self.imager.intensity) / 1000  # Convert to kR
        
        # Auto-calculate vmin/vmax if not provided
        if vmin is None:
            vmin = np.amin(intensity_kR)
        if vmax is None:
            vmax = np.amax(intensity_kR)
        
        extent = (1, numpix, numpix, 1)
        
        fig, ax = plt.subplots(figsize=figsize)
        im = ax.imshow(intensity_kR, extent=extent, cmap=cmap, 
                      origin='lower', vmin=vmin, vmax=vmax)
        
        cb = fig.colorbar(im, fraction=0.046, pad=0.04)
        cb.set_label('Intensity [kR]', fontsize=15)
        cb.ax.tick_params(labelsize=15)
        
        ax.set_xlabel('Pixel H', fontsize=15)
        ax.set_ylabel('Pixel V', fontsize=15)
        ax.set_title(title, fontsize=15)
        
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.tight_layout()
        
        return fig, ax
    
    def plot_3d_geometry(self, orbit_radius=6.6, figsize=(10, 10), 
                        view_elev=60, view_azim=15):
        """
        Plot 3D visualization of satellite geometry
        
        Parameters:
        -----------
        orbit_radius : float
            Orbital radius in Earth Radii
        figsize : tuple
            Figure size
        view_elev : float
            Elevation viewing angle
        view_azim : float
            Azimuth viewing angle
        """
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot Earth
        self._plot_earth(ax)
        
        # Plot orbit
        self._plot_orbit(ax, orbit_radius)
        
        # Plot satellite position
        sat_pos = self.imager.sat_pos
        ax.scatter3D(sat_pos[0], sat_pos[1], sat_pos[2], 
                    s=100, c='r', zorder=20, label='Satellite')
        
        # Plot Field of View
        self._plot_fov(ax, sat_pos, self.imager.r_los, self.imager.numpix)
        
        # Plot model boundaries
        self._plot_model_boundaries(ax, self.imager.config.model['minRAD'],
                                   self.imager.config.model['maxRAD'])
        
        # Set labels and limits
        ax.set_xlabel('X [RE]', fontsize=12)
        ax.set_ylabel('Y [RE]', fontsize=12)
        ax.set_zlabel('Z [RE]', fontsize=12)
        ax.set_xlim3d(-10, 10)
        ax.set_ylim3d(-10, 10)
        ax.set_zlim3d(-10, 10)
        
        # Set view angle
        ax.view_init(view_elev, view_azim)
        ax.legend()
        
        plt.tight_layout()
        
        return fig, ax
    
    def _plot_earth(self, ax):
        """Plot Earth as a sphere"""
        u = np.linspace(0, 2*np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x, y, z, rstride=4, cstride=4, 
                       color='b', zorder=-1, alpha=0.6)
    
    def _plot_orbit(self, ax, radius):
        """Plot orbital path"""
        theta = np.linspace(0, 2*np.pi, 100)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        z = np.zeros(len(x))
        
        ax.plot3D(x, y, z, 'k', linewidth=2, zorder=-1, label='Orbit')
    
    def _plot_fov(self, ax, sat_pos, r_los, numpix):
        """Plot Field of View lines"""
        fov_indices = [0, numpix-1, numpix*numpix-1, numpix*(numpix-1)]
        
        for idx in fov_indices:
            new_point = sat_pos + 15 * r_los[idx, :]
            ax.plot3D([sat_pos[0], new_point[0]], 
                     [sat_pos[1], new_point[1]], 
                     [sat_pos[2], new_point[2]], 
                     color='g', zorder=-1, alpha=0.5)
    
    def _plot_model_boundaries(self, ax, min_rad, max_rad):
        """Plot hydrogen model boundaries"""
        theta = np.linspace(0, 2*np.pi, 100)
        
        for radius in [min_rad, max_rad]:
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            z = np.zeros(len(x))
            ax.plot3D(x, y, z, 'gray', linewidth=1.5, 
                     zorder=-1, alpha=0.7)