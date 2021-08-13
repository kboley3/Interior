#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:12:34 2018

@author: joeschulze
"""

import numpy as np
import sys
sys.path.append('../Functions')
from find_nearest import find_nearest 


def calc_adiabatic_atm(Planet):
    
    
    
        bar2pa =  100000;
        #atmosphere parameters
        #mean molecular weight kg/mol
        G = 6.67408e-11  #gravitational constant
        Rgas = 8.31    #J/mol/K
        gamma = 7.0/5.0 #diatomic gas
        
        
        
        
        #Use ExoPlex
        
        mu = 0.029
        #parameters given from ExoPlex
        radius_rock = Planet['radius'][-1]   
        temp = Planet['temperature'][-1]
        mass_rock = Planet['mass'][-1]
        pressure = Planet['pressure'][-1]*bar2pa          #ExoPlex gives Pressure in Bar
        pressure0 = Planet['pressure'][-1]*bar2pa #to calc scale height
        
        
        '''
        #Neptune params
        mu = 0.0027
        radius_rock = 2.716*6.371e6
        #radius_rock = 3.88*6.371e6
        temp = 67.07
        pressure = 1.0e08
        mass_rock = 15.2*5.972e24 
        #mass_rock = 17.14*5.972e24 
        density = pressure*mu/(Rgas*temp)
        pressure0 = pressure
        '''
        
        
        #Earth's atmosphere.   
        '''
        mu = 0.029
        radius_rock = 6.371e6
        temp = 288.0
        pressure = 0.101325*1e6 
        mass_rock = 5.972e24 
        density = pressure*mu/(Rgas*temp)
        pressure0 = pressure
        '''
        
        #Venus's atmosphere.
        '''
        mu = 0.044     
        radius_rock = 6.0e6
        temp = 735
        pressure = 90*0.101325*1e6 
        mass_rock = 0.815*5.972e24 
        density = pressure*mu/(Rgas*temp)
        pressure0 = pressure
        '''

        #SH_P = pressure/np.exp(1);
        
        #initialize Parameters to hold values
        radius = radius_rock
        height = 0.

        #set some initial params
        m_atm = 0. 
        m_shell = 0.
        grav = G*mass_rock/(radius_rock**2) #gravity at the surface   
        dh = 10.    #set size in meters
        scale_H=0.0
        density = pressure*mu/(Rgas*temp)
            
        while pressure>=0.0:
            
            #calc mass of atm shell at current height 
            m_shell = 4*np.pi*(radius**2)*density*dh
            m_atm = m_atm+m_shell

            

            #step up in height
            height = height+dh
            radius = height+radius_rock
            
            
            #calc gravity at current height
            grav = G*(mass_rock+m_atm)/(radius**2)
            
            #calc temp at this height
            temp = temp-((gamma-1)/gamma)*(mu*grav/Rgas)*dh
            
            
            #calc pressure at this height
            pressure = pressure - density*grav*dh


            #calc density for shell at current height
            density = pressure*mu/(Rgas*temp)
            
            #provided the pressure is not negative append values to their
            #respective arrays
            if pressure>=0:
                Planet['mass'] = np.append(Planet['mass'], m_atm)    
                Planet['radius'] = np.append(Planet['radius'], radius)
                Planet['temperature'] = np.append(Planet['temperature'],temp)
                Planet['pressure'] = np.append(Planet['pressure'], pressure/bar2pa)
                Planet['density'] = np.append(Planet['density'], density)
                Planet['gravity'] = np.append(Planet['gravity'], grav)
                
        scale_H_index = find_nearest(Planet['pressure'], pressure0/bar2pa/np.exp(1))
        scale_H = Planet['radius'][scale_H_index] - radius_rock
        
        print ('Mass of Atm: ', m_atm)
        
        return Planet, scale_H