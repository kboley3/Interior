#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 19:10:22 2019

@author: joeschulze
"""

import os
import sys
# hack to allow scripts to be placed in subdirectories next to burnman:
if not os.path.exists('ExoPlex') and os.path.exists('../ExoPlex'):
    sys.path.insert(1, os.path.abspath('..'))
    
import numpy as np


import ExoPlex as exo



def compCMF(water, Si, Fe, mass, radius0, CMF_var, cmf_flag = 1.0):
        '''
        mass = mass of the planet in Earth masses
        radius0 = radius of the planet in Earth radii.
               I call this radius0 b/c my code is fitting to it. The mass on the 
               other hand is fixed the entire time. The code basically varies CMF
               until the radius calculated via ExoPlex is within 1e-04 Earth Radii
        CMF_var is just an initial guess for the FRACTIONAL (not %) CMF of the planet. 
               Obviously, The closer your initial guess is to the true value the more
               quickly this code will converge. However, even if you are wildly off
               it still doesn't take all that long.
               
        Code overview: The code runs ExoPlex and calculates the radius for two CMF values (CMF and CMF + a very small number).
                       It then calculates the difference between the two radii to get dCMF/dR.
                       It uses the derivative to calculate the new guess for CMF using CMF_next = CMF_current + CMF_current*(current_radius - radius0).
                       It does this until current_radius - radius0 is less than 1e-04 Earth Radii or you consistenly get a CMF value of <0 (LDSPs).
        '''
        
        
        
        '''
        -----------------------------------------------------------------------
        Exoplex parameters.
        -----------------------------------------------------------------------
        '''
            
        #compositional parameters
        wt_frac_Si_core = 0.; mol_frac_Fe_mantle = 0.0; 
        wt_frac_O_core = 0.; wt_frac_S_core = 0.0; 


        Pressure_range_mantle_UM = '10000 1400000'
        Temperature_range_mantle_UM = '1400 3500'
        resolution_UM = '80 140' #22500

        Pressure_range_mantle_LM = '1250000 900000'
        Temperature_range_mantle_LM = '2200 5000'

        resolution_LM = '40 40' #6400


        #specify mantle and core layers
        num_mantle_layers = 2000; num_core_layers = 1000; number_h2o_layers = 0;

        Core_rad_frac_guess = 0.015;  Water_rad_frac_guess = 0.; 
        Mantle_potential_temp = 1600.;  Water_potential_temp = 300.;

        #0.324
    
        #mantle grid
        #Star = 'CMB_P20000GPa_T20000K_FeMg_1p0_SiMg_1p0'
        #Star = 'CMB_640GPa_7000K_SiMg_1p0_FeMg_1p0'
        #Star='Wasp47_CMB_50000GPa_30000K_SiMg_1p0_FeMg_1p0'
        Star='CMB_P19000GPa_T20000K_FeMg_1p0_SiMg_1p0_v2'
        filename = Star
        #abundance ratios
        CaMg = 0.0; SiMg = Si; AlMg = 0.0; FeMg = Fe;
        
        #define radius tolerance
        radius_tolerance = 1.0e-04;

        layers = [num_mantle_layers, num_core_layers, number_h2o_layers]

        #cmf_que = 0.0 #This tells ExoPlex that the second compositional param is a CMF and not Fe/Mg
                      #A value of 0 means the second param is an Fe/Mg. Anything else indicates a CMF value.
                      #I have modified ExoPlex to calculate Fe/Mg from the CMF value if cmf_que !=0 (see functions file)
 
        
        #vary CMF by a very small number (0.000001)
        if cmf_flag !=0:
            #work in terms of fractional CMF
            compositional_params1 = [0,CMF_var,SiMg,CaMg,AlMg,mol_frac_Fe_mantle,wt_frac_Si_core, \
                                wt_frac_O_core,wt_frac_S_core, cmf_flag]
        
            compositional_params2 = [0,CMF_var+0.000001,SiMg,CaMg,AlMg,mol_frac_Fe_mantle,wt_frac_Si_core, \
                                wt_frac_O_core,wt_frac_S_core, cmf_flag]
                
        else:
            #work in terms of FeMg
            FeMg = CMF_var
            compositional_params1 = [0,FeMg,SiMg,CaMg,AlMg,mol_frac_Fe_mantle,wt_frac_Si_core, \
                                wt_frac_O_core,wt_frac_S_core, cmf_flag]
        
            compositional_params2 = [0,FeMg+0.000001,SiMg,CaMg,AlMg,mol_frac_Fe_mantle,wt_frac_Si_core, \
                                wt_frac_O_core,wt_frac_S_core, cmf_flag]
                    
        structure_params = [Pressure_range_mantle_UM, Temperature_range_mantle_UM, resolution_UM,
                            Pressure_range_mantle_LM, Temperature_range_mantle_LM, resolution_LM,
                            Core_rad_frac_guess, Mantle_potential_temp,Water_rad_frac_guess,Water_potential_temp]

        #build the planet
        
        
        '''
        -----------------------------------------------------------------------
        End Exoplex parameters.
        -----------------------------------------------------------------------
        '''
        
        
        #Planet1 = exo.run_planet_mass(mass, compositional_params, structure_params, layers, filename, CMF = CMF_var)
        #Planet2 = exo.run_planet_mass(mass, compositional_params, structure_params, layers, filename, CMF = CMF_var+0.000001)
        
        
        # calculate radius for both CMF and CMF + 0.000001
        Planet1 = exo.run_planet_mass(mass, compositional_params1, structure_params, layers, filename)
        Planet2 = exo.run_planet_mass(mass, compositional_params2, structure_params, layers, filename)
        
        curr_radius1 = Planet1['radius'][-1]/6371000.0
        curr_radius2 = Planet2['radius'][-1]/6371000.0
        
        #calculate dCMF/dR
        dCMFdr = abs(0.000001/(curr_radius1-curr_radius2))
        
        n=0.0
        
        #if radius_tolerance criteria not met use dCMF/dR to make a new CMF guess and run again
        if abs(curr_radius1-radius0)>radius_tolerance:
            if curr_radius1>radius0:
                CMF_var = CMF_var + dCMFdr*abs(curr_radius1-radius0)
            if curr_radius1<radius0:
                CMF_var = CMF_var - dCMFdr*abs(curr_radius1-radius0)  
              
            if CMF_var >0.0:
                return compCMF(water, Si, Fe,mass, radius0, CMF_var, cmf_flag)
            
            
            #This is here to avoid negative CMF values which will break ExoPlex. If the code guessed a negative value
            #then this artificially sets it back to 0.001. Then the code will run again and hopefully guess a non-negative value.
            if CMF_var < 0.0 or np.isnan(CMF_var) == True:
                CMF_var = 0.001
                n = n+1.0
            
            #if you guess a negative value more than 11 times then you are probably dealing with an LDSP that requires an envelope or water layer.
            #In other words, this planet is less dense than a pure MgSiO3 sphere, in which case the approximation of a solid Fe core and Fe-free silicate
            #mantle is not valid. The code quits when this happens.
            if n >=10:
                CMF_var = 0.0
                return(CMF_var, Planet1, num_core_layers, num_mantle_layers, number_h2o_layers)
                
            print('RADIUS DIF: ', curr_radius1-radius0)
                
        
        #return current parameters when radius crit is met.
        if abs(curr_radius1-radius0)<radius_tolerance:
            
            CMF_out = Planet1['mass'][num_core_layers]/Planet1['mass'][-1]
            
        print ("Mass = ", '%.3f'%(Planet1['mass'][-1]/5.97e24), "Earth masses")
        print ("Radius = ", '%.3f'%(Planet1['radius'][-1]/6371e3), "Earth radii")
        print ("Core Mass Fraction = ", '%.4f'%(Planet1['mass'][num_core_layers]/Planet1['mass'][-1]))
        print ("Core Radius Fraction = ", '%.4f'%(Planet1['radius'][num_core_layers]/Planet1['radius'][-1]))
        print ("Core Radius Fraction Variance = ", '%.4f'%(CMF_var))
        print ("CMB Pressure = " ,'%.2f' % (Planet1['pressure'][num_core_layers]/10000), "GPa")
        print ("number of oceans:",'%.2f' % (water*Planet1['mass'][-1]/1.4e21))
            
        return (CMF_out, Planet1, num_core_layers, num_mantle_layers, number_h2o_layers)
        
                
        
            
        
        
        

            
            
        
        
        
        
        
        