"""
Configuration file for ExoSpy satellite imaging simulation
"""

class SatelliteConfig:
    """Configuration for satellite parameters"""
    def __init__(self):
        # Satellite Position (in Earth Radii)
        self.position = {
            'x': 6.6,  # RE
            'y': 6.6,  # RE  
            'z': 0.0   # RE
        }
        
        # Target Position (in Earth Radii)
        self.target = {
            'x': 0.0,   # RE
            'y': 6.6,   # RE
            'z': -0.15  # RE
        }
        
        # Imager Specifications
        self.imager = {
            'fov': 18,           # Field of view in degrees
            'pixangres': 0.25    # Angular resolution (degrees between pixels)
        }
        
        # Solar Conditions
        self.solar = {
            'irradiance': 0.008519  # FROM LISIRD COMPOSITE LY-ALPHA JAN 9, 2015
        }
        
        # Model Parameters
        self.model = {
            'type': 'Z15MAX',
            'dl': 0.05,       # Integration step
            'maxRAD': 8,      # Maximum radius (RE)
            'minRAD': 3       # Minimum radius (RE)
        }
        
    def get_sat_position_array(self):
        """Returns satellite position as numpy array"""
        import numpy as np
        
        return np.array(
            [self.position['x'], 
             self.position['y'], 
             self.position['z']]
        )
    
    def get_target_position_array(self):
        """Returns target position as numpy array"""
        import numpy as np

        return np.array(
            [self.target['x'], 
             self.target['y'], 
             self.target['z']]
        )