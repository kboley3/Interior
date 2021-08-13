#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 09:31:58 2018

@author: joeschulze
"""

''' This function calculates the scale height, opaque atmospheric thickness, and 
the mass given the atmospheric temp, acceleration due to gravity at the bottom
of the atmosphere (or the surface of the planet), the radius at the bottom of the
atmosphere, and the pressure at the bottom of the atmosphere.

An isothermal atmosphere is assumed. This approximation is only valid for an
atmospheric mass fraction (m_env/M_planet) of ~<0.0001 (per Dorn et al. 2017).'''




import math
import numpy as np


def isotherm_atm(T_atm, g_batm, P_batm, r_batm):
    
    '''Usage: H, d_atm, m_atm = isothem_atm(T_atm, g_batm, P_batm, r_batm)
       
        T_atm -- temp assumed for isothermal atmosphere in K
        g_batm -- surface gravity  in m/s^2
        P_batm -- surface pressure in bars
        r_batm -- surface radius in m
    
    returns
    
        H -- scale height
        d_atm -- opaque atmospheric thickness or height
        m_atm -- mass of atmosphere in kg
    
    '''
    
    #Define Constant Parameters, and conversion factors
    P_out = 0.02                     #20 mbar per Dorn et al. 2017 -- See how valid this is...
    bar2pa = 100000                 #conversion from bars to pascals, in case the input pressure
                                    #is in bars.
    mu = 0.0288                     #rough estimate of mean molecular weight in kg/mol
    R = 8.3144598                   #universal gas constant in J/mol*K
                      
    
    #calculate the scale height:
    H = T_atm*R/(g_batm*mu)
    
    #calc the opaque thickness (assuming a pressure at the top of the atm)
    d_atm = H*np.log(P_batm/P_out)
    
    m_atm = 4*math.pi*P_batm*bar2pa*(np.power(r_batm,2))/g_batm;
    
    return H, d_atm, m_atm
    
    