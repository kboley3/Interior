
# This file is part of ExoPlex - a self consistent planet builder
# Copyright (C) 2017 - by the ExoPlex team, released under the GNU
# GPL v2 or later.

import os
import sys
# hack to allow scripts to be placed in subdirectories next to burnman:
if not os.path.exists('ExoPlex') and os.path.exists('../ExoPlex'):
    sys.path.insert(1, os.path.abspath('..'))
import matplotlib.pyplot as plt

import time
start_time = time.time()



              
import mass_rad_comp_CMF_func_v4 as CMF

#This script basically just calls the CMF calculator and then does the standard exoplex plotting
#mass_rad_comp_CMF_func_v4 takes three inputs -- mass, radius, and an initial guess for CMF
#Exolens isn't exact but it is close and will give you a reasonable guess for CMF

water=0.001
FeMg=0.74
SiMg=0.89



cmf_rho, Planet, num_core_layers, num_mantle_layers, num_h2o_layers = CMF.compCMF(water, SiMg, FeMg,7.74, 1.89, 0.9, cmf_flag = 1.0)


figure = plt.figure(figsize = (12,10))

ax1 = plt.subplot2grid((6, 3), (0, 0), colspan=3, rowspan=3)
ax2 = plt.subplot2grid((6, 3), (3, 0), colspan=3, rowspan=1)
ax3 = plt.subplot2grid((6, 3), (4, 0), colspan=3, rowspan=1)
ax4 = plt.subplot2grid((6, 3), (5, 0), colspan=3, rowspan=1)

#Density profile
ax1.plot(Planet['radius'] / 1.e3, Planet['density'] / 1.e3, 'k', linewidth=2.)
ax1.set_ylim(0., (max(Planet['density']) / 1.e3) + 1.)
ax1.set_xlim(0., max(Planet['radius']) / 1.e3)
ax1.set_ylabel("Density ( $\cdot 10^3$ kg/m$^3$)")

# Make a subplot showing the calculated pressure profile
ax2.plot(Planet['radius'] / 1.e3, Planet['pressure'] / 1.e4, 'b', linewidth=2.)
ax2.set_ylim(0., (max(Planet['pressure']) / 1e4) + 10.)
ax2.set_xlim(0., max(Planet['radius']) / 1.e3)
ax2.set_ylabel("Pressure (GPa)")
ax2.axvline(Planet['radius'][num_core_layers]/1.e3, color = 'k', linestyle = '--')
ax2.text(Planet['radius'][num_core_layers]/1.e3 + 50, 0.75*max(Planet['pressure']/1.e4), 'CMB P: ' + str(round(Planet['pressure'][num_core_layers]/1.e4,2)) + ' GPa')
ax2.text(Planet['radius'][0]/1.e3 + 50, 0.75*max(Planet['pressure']/1.e4), 'Core P: ' + str(round(Planet['pressure'][0]/1.e4,2)) + ' GPa')



# Make a subplot showing the calculated gravity profile
ax3.plot(Planet['radius'] / 1.e3, Planet['gravity'], 'r', linewidth=2.)
ax3.set_ylabel("Gravity (m/s$^2)$")
ax3.set_xlim(0., max(Planet['radius']) / 1.e3)
ax3.set_ylim(0., max(Planet['gravity']) + 0.5)

# Make a subplot showing the calculated temperature profile
ax4.plot(Planet['radius'] / 1.e3, Planet['temperature'], 'g', linewidth=2.)
ax4.set_ylabel("Temperature ($K$)")
ax4.set_xlabel("Radius (km)")
ax4.set_xlim(0., max(Planet['radius']) / 1.e3)
ax4.set_ylim(0., max(Planet['temperature']) + 100)
ax4.axvline(Planet['radius'][num_core_layers]/1.e3, color = 'k', linestyle = '--')
ax4.text(Planet['radius'][num_core_layers]/1.e3 + 50, 0.75*max(Planet['temperature']), 'CMB T: ' + str(round(Planet['temperature'][num_core_layers],2)) + ' K')
ax4.text(Planet['radius'][0]/1.e3 + 50, 0.75*max(Planet['temperature']), 'Core T: ' + str(round(Planet['temperature'][0],2)) + ' K')

print (Planet['mass'][-1]/5.972e24)

plt.show()

print("--- %s seconds ---" % (time.time() - start_time))