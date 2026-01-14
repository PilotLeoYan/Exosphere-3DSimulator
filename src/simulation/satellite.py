"""
Satellite imaging simulation module
"""

import numpy as np
import numpy.matlib
import exospy.exospy as ep


class SatelliteImager:
    """Class to handle satellite imaging operations"""
    
    def __init__(self, config):
        """
        Initialize satellite imager with configuration
        
        Parameters:
        -----------
        config : SatelliteConfig
            Configuration object with satellite parameters
        """
        self.config = config
        self.sat_pos = config.get_sat_position_array()
        self.target_pos = config.get_target_position_array()
        self.target_los = self.target_pos - self.sat_pos
        
        # LOS and POS arrays
        self.r_los = None
        self.r_pos = None
        self.numpix = None
        self.intensity = None
        
    def generate_los(self):
        """Generate Line of Sight vectors from imager"""
        fov = self.config.imager['fov']
        pixangres = self.config.imager['pixangres']
        
        self.r_los, self.numpix = ep.generateLOSfromImager(
            fov, pixangres, self.target_los
        )
        
        return self.r_los, self.numpix
    
    def generate_pos(self):
        """Generate Position vectors for imager"""
        if self.numpix is None:
            raise ValueError("Must generate LOS before POS")
            
        self.r_pos = np.matlib.repmat(
            self.sat_pos, 
            self.numpix * self.numpix, 
            1
        )
        
        return self.r_pos
    
    def calculate_intensity(self):
        """
        Calculate intensity using optically thin approximation
        
        Returns:
        --------
        intensity : numpy.ndarray
            2D array of intensity values reshaped to (numpix, numpix)
        """
        if self.r_los is None or self.r_pos is None:
            raise ValueError("Must generate LOS and POS before calculating intensity")
        
        irradiance = self.config.solar['irradiance']
        model_type = self.config.model['type']
        dl = self.config.model['dl']
        maxRAD = self.config.model['maxRAD']
        minRAD = self.config.model['minRAD']
        
        intensity_flat = ep.generateIntensityOpticallyThin(
            irradiance, 
            self.r_los, 
            self.r_pos, 
            model_type,
            dl=dl,
            maxRAD=maxRAD, 
            minRAD=minRAD
        )
        
        self.intensity = np.reshape(intensity_flat, (self.numpix, self.numpix)) # type: ignore
        
        return self.intensity
    
    def run_simulation(self):
        """
        Run complete simulation pipeline
        
        Returns:
        --------
        intensity : numpy.ndarray
            2D intensity map
        """
        self.generate_los()
        self.generate_pos()
        self.calculate_intensity()
        
        return self.intensity