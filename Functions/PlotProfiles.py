#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:48:52 2018

@author: joeschulze
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_profiles(Planet):
    
    figure = plt.figure(figsize = (12,10))
    # figure.suptitle('Your planet is %.3f Earth Masses with Average Density of %.1f kg/m$^3$' %((Plan.mass/5.97e24), \
    #                (Plan.mass/(4./3.*np.pi*Plan.radial_slices[-1]*Plan.radial_slices[-1]*Plan.radial_slices[-1]))),\
    #                 fontsize=20)

    ax1 = plt.subplot2grid((6, 3), (0, 0), colspan=3, rowspan=3)
    ax2 = plt.subplot2grid((6, 3), (3, 0), colspan=3, rowspan=1)
    ax3 = plt.subplot2grid((6, 3), (4, 0), colspan=3, rowspan=1)
    ax4 = plt.subplot2grid((6, 3), (5, 0), colspan=3, rowspan=1)

    ax1.plot(Planet['radius'] / 1.e3, Planet['density'] / 1.e3, 'k', linewidth=2.)
    ax1.set_ylim(0., (max(Planet['density']) / 1.e3) + 1.)
    ax1.set_xlim(0., max(Planet['radius']) / 1.e3)
    ax1.set_ylabel("Density ( $\cdot 10^3$ kg/m$^3$)")
    ax1.tick_params(axis = 'x', which = 'both', bottom = False, labelbottom=False)

    # Make a subplot showing the calculated pressure profile
    ax2.plot(Planet['radius'] / 1.e3, Planet['pressure'] / 1.e4, 'b', linewidth=2.)
    ax2.set_ylim(0., (max(Planet['pressure']) / 1e4) + 10.)
    ax2.set_xlim(0., max(Planet['radius']) / 1.e3)
    ax2.set_ylabel("Pressure (GPa)")
    ax2.tick_params(axis = 'x', which = 'both', bottom = False, labelbottom=False)

    # Make a subplot showing the calculated gravity profile
    ax3.plot(Planet['radius'] / 1.e3, Planet['gravity'], 'r', linewidth=2.)
    ax3.set_ylabel("Gravity (m/s$^2)$")
    ax3.set_xlim(0., max(Planet['radius']) / 1.e3)
    ax3.set_ylim(0., max(Planet['gravity']) + 0.5)
    ax3.tick_params(axis = 'x', which = 'both', bottom = False, labelbottom=False)

    # Make a subplot showing the calculated temperature profile
    ax4.plot(Planet['radius'] / 1.e3, Planet['temperature'], 'g', linewidth=2.)
    ax4.set_ylabel("Temperature ($K$)")
    ax4.set_xlabel("Radius (km)")
    ax4.set_xlim(0., max(Planet['radius']) / 1.e3)
    ax4.set_ylim(0., max(Planet['temperature']) + 100)

    plt.show()
    
    return figure





def plot_atm_profiles(Planet, num_atm_layers, scale_H):
    
   
    
    figure = plt.figure(figsize = (12,20))
    # figure.suptitle('Your planet is %.3f Earth Masses with Average Density of %.1f kg/m$^3$' %((Plan.mass/5.97e24), \
    #                (Plan.mass/(4./3.*np.pi*Plan.radial_slices[-1]*Plan.radial_slices[-1]*Plan.radial_slices[-1]))),\
    #                 fontsize=20)

    ax1 = plt.subplot2grid((7, 3), (0, 0), colspan=3, rowspan=3)
    ax2 = plt.subplot2grid((7, 3), (3, 0), colspan=3, rowspan=1)
    ax3 = plt.subplot2grid((7, 3), (4, 0), colspan=3, rowspan=1)
    ax4 = plt.subplot2grid((7, 3), (5, 0), colspan=3, rowspan=1)
    ax5 = plt.subplot2grid((7, 3), (6, 0), colspan=3, rowspan=1)
    
    
    atm = num_atm_layers    #keep the code cleaner
    
    fsize = 20

    ax1.tick_params(labelsize = 14)
    ax1.plot(Planet['radius'][-atm:]/1.e3, Planet['density'][-atm:], 'k', linewidth=2.)

    ax1.set_ylim(min(Planet['density'][-atm:]), (max(Planet['density'][-atm:])))
    ax1.set_xlim(min(Planet['radius'][-atm:])/ 1.e3, max(Planet['radius'][-atm:]) / 1.e3)
    ax1.set_ylabel("Density (kg/m$^3$)", FontSize = fsize)
    ax1.tick_params(axis = 'x', which = 'both', bottom = False, labelbottom=False)
    ax1.axvline(x=(scale_H+Planet['radius'][-atm])/1.e3, linewidth = 2.,color = 'k', linestyle = '--')
    ax1.text((scale_H+Planet['radius'][-atm])/1.e3 +1,max(Planet['density'][-atm:])*0.9, 'Scale Height = ' + str(scale_H/1.e3)+  ' km', fontsize = 16)

    # Make a subplot showing the calculated pressure profile
    ax2.tick_params(labelsize = 14)
    ax2.plot(Planet['radius'][-atm:] / 1.e3, Planet['pressure'][-atm:], 'b', linewidth=2.)
    ax2.set_ylim(min(Planet['pressure'][-atm:]), (max(Planet['pressure'][-atm:])))
    ax2.set_xlim(min(Planet['radius'][-atm:])/ 1.e3, max(Planet['radius'][-atm:]) / 1.e3)
    ax2.set_ylabel("Pressure (Bar)", fontsize = fsize)
    ax2.tick_params(axis = 'x', which = 'both', bottom = False, labelbottom=False)
    ax2.axvline(x=(scale_H+Planet['radius'][-atm])/1.e3, linewidth = 2.,color = 'k', linestyle = '--')

    # Make a subplot showing the calculated gravity profile
    
    ax3.tick_params(labelsize = 14)
    ax3.plot(Planet['radius'][-atm:] / 1.e3, Planet['gravity'][-atm:], 'r', linewidth=2.)
    ax3.set_ylabel("Gravity (m/s$^2)$", fontsize = fsize)
    ax3.set_xlim(min(Planet['radius'][-atm:])/ 1.e3, max(Planet['radius'][-atm:]) / 1.e3)
    ax3.set_ylim(min(Planet['gravity'][-atm:]), max(Planet['gravity'][-atm:]))
    ax3.tick_params(axis = 'x', which = 'both', bottom = False, labelbottom=False)
    ax3.axvline(x=(scale_H+Planet['radius'][-atm])/1.e3, linewidth = 2.,color = 'k', linestyle = '--')
    
    
    # Make a subplot showing the calculated temperature profile
    ax4.tick_params(labelsize = 14)
    #ax4.set_xlabel("Radius (km)", fontsize = fsize)
    ax4.plot(Planet['radius'][-atm:] / 1.e3, Planet['temperature'][-atm:], 'g', linewidth=2.)
    ax4.set_ylabel("Temperature ($K$)", fontsize = fsize)
    ax4.set_xlim(min(Planet['radius'][-atm:])/ 1.e3, max(Planet['radius'][-atm:]) / 1.e3)
    ax4.set_ylim(min(Planet['temperature'][-atm:]), max(Planet['temperature'][-atm:]))
    ax4.tick_params(axis = 'x', which = 'both', bottom = False, labelbottom=False)
    ax4.axvline(x=(scale_H+Planet['radius'][-atm])/1.e3, linewidth = 2.,color = 'k', linestyle = '--')

    
    
    
    ax5.tick_params(labelsize = 14)
    ax5.plot(Planet['radius'][-atm:] / 1.e3, Planet['mass'][-atm:], 'm', linewidth=2.)
    ax5.set_ylabel("Mass (kg)", fontsize = fsize)
    ax5.set_xlabel("Radius (km)", fontsize = fsize)
    ax5.set_xlim(min(Planet['radius'][-atm:])/ 1.e3, max(Planet['radius'][-atm:]) / 1.e3)
    ax5.set_ylim(min(Planet['mass'][-atm:]), max(Planet['mass'][-atm:])+max(Planet['mass'][-atm:])/10)
    ax5.axvline(x=(scale_H+Planet['radius'][-atm])/1.e3, linewidth = 2.,color = 'k', linestyle = '--')
    

    '''
    #Earth stoof
    earth_atm = pd.read_csv('../Scripts/siLong.csv')
    ax1.plot(earth_atm['height'] + Planet['radius'][-atm]/1.e3, earth_atm['density'], 'k--', linewidth = 2.) 
    ax2.plot(earth_atm['height'] + Planet['radius'][-atm]/1.e3, earth_atm['pressure']/101325., 'b--', linewidth = 2. )
    ax4.plot(earth_atm['height'] + Planet['radius'][-atm]/1.e3, earth_atm['temp'], 'g--', linewidth = 2.)
    '''
    
    
    #Venus stoof
    venus_atm = pd.read_csv('../Scripts/venus_atm.csv')
    ax1.plot(venus_atm['height'] + Planet['radius'][-atm]/1.e3, venus_atm['density'], 'k--', linewidth = 2.) 
    ax2.plot(venus_atm['height'] + Planet['radius'][-atm]/1.e3, venus_atm['pressure']/101325., 'b--', linewidth = 2. )
    ax4.plot(venus_atm['height'] + Planet['radius'][-atm]/1.e3, venus_atm['temp'], 'g--', linewidth = 2.)
    
    
    '''
    #Neptune stoof
    neptune_atm = pd.read_csv('../Scripts/neptune_atm.csv')
    ax1.plot(neptune_atm['height'] + Planet['radius'][-atm]/1.e3, neptune_atm['density'], 'k--', linewidth = 2.) 
    ax2.plot(neptune_atm['height'] + Planet['radius'][-atm]/1.e3, neptune_atm['pressure']/101325., 'b--', linewidth = 2. )
    ax4.plot(neptune_atm['height'] + Planet['radius'][-atm]/1.e3, neptune_atm['temp'], 'g--', linewidth = 2.)
    '''
    
    fig_fname = './../Plots/Venus.png'             
    
    plt.savefig(fig_fname, transparent = True)
    plt.show()
    
    return figure
    