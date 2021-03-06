import sys
import os
import numpy as np
Earth_radius = 6.371e6
Earth_mass = 5.97e24
if not os.path.exists('ExoPlex') and os.path.exists('../ExoPlex'):
    sys.path.insert(1, os.path.abspath('..'))
    
import minphys

def initialize_by_radius(*args):
    radius_planet = args[0]
    structural_params = args[1]
    compositional_params = args[2]
    num_mantle_layers, num_core_layers, number_h2o_layers = args[3]

    wt_frac_water, FeMg, SiMg, CaMg, AlMg, mol_frac_Fe_mantle, wt_frac_Si_core, \
    wt_frac_O_core, wt_frac_S_core, cmf_que = compositional_params

    core_rad_frac = structural_params[6]
    Mantle_potential_temp = structural_params[7]
    water_rad_frac = structural_params[8]
    water_potential_temp = structural_params[9]

    #def Setup(Mp, masMan, masCor, masH2O, nr, tCrstMan, dtManCor):
    # global Th,Tss
    #    global rad, rho, rho0, vol, dmass, mass, delta,\
    #        T, nic, noc, grav, P, rhon, alpha, cp,phase

    # use inputs to find actual mass of mantle and core

    # if there is a water layer, the imput temperature is lowered because that temperature is for the crustal layer
    # also 50 shells are used for the water layer hence the nh20 vaiable

    if wt_frac_water == 0. and number_h2o_layers > 0:
       print ("You have layers of water but no water!")
       number_h2o_layers = 0

    num_layers = num_core_layers+num_mantle_layers + number_h2o_layers # add 50 shells if there is an h2O layer
    # arrays to be used

    # these grids are initialized in this function and are then a passed around through the other routines and edited each iteration
    radius_layers = np.zeros(num_layers)
    density_layers = np.zeros(num_layers)
    volume_layers = np.zeros(num_layers)
    mass_layers = np.zeros(num_layers)
    cumulative_mass = np.zeros(num_layers)
    Temperature_layers = np.zeros(num_layers)
    # used for compressiofh2on funciton
    gravity_layers = np.zeros(num_layers)
    Pressure_layers = np.zeros(num_layers)
    alpha = np.zeros(num_layers)
    cp = np.zeros(num_layers)
    Vphi = np.zeros(num_layers )

    Vs = np.zeros(num_layers )
    Vp = np.zeros(num_layers)
    K =  np.zeros(num_layers)

    # 15 mineral phases + 2ice + liquid water #phasechange
    planet_radius_guess = radius_planet*Earth_radius
    water_thickness_guess = water_rad_frac*planet_radius_guess
    core_thickness_guess = core_rad_frac * (planet_radius_guess-water_thickness_guess)
    mantle_thickness_guess = planet_radius_guess - water_thickness_guess - core_thickness_guess



    for i in range(num_layers):
        if i <num_core_layers:
            radius_layers[i]=((float(i)/num_core_layers)*core_thickness_guess)
            #density_layers[i]= 8280.0
            #Temperature_layers[i] = 4500.+ (float((3000.-4500.))/float(num_core_layers))\
                                                            #*float((i))
            Temperature_layers[i] = 4500.+ (float((3000.-4500.))/float(num_core_layers))\
                                                            *float((i))

        elif i < (num_core_layers+num_mantle_layers):
            radius_layers[i]=(core_thickness_guess+((float(i-num_core_layers)/num_mantle_layers)*mantle_thickness_guess))
            #density_layers[i]=3100.
            Temperature_layers[i] = 2700.

        else:
            radius_layers[i]=core_thickness_guess+mantle_thickness_guess+\
                             ((float(i-num_core_layers-num_mantle_layers)/number_h2o_layers)*water_thickness_guess)
            #density_layers[i]=1100.
            Temperature_layers[i] = 300.

    for i in range(num_layers):
        if i > num_core_layers+num_mantle_layers:
            Pressure_layers[i] = 1.
        else:
            Pressure_layers[i] = (float((5000.-(300.*10000))/float(num_core_layers+num_mantle_layers))*float(i)
                                  + 300.*10000)

    print (Pressure_layers)
    #initial temperature guess of 0.5 K per km
    keys = ['radius','density','temperature','gravity','pressure',\
            'alpha','cp','Vphi''Vp','Vs','K']


    return dict(zip(keys,[radius_layers, density_layers,Temperature_layers,gravity_layers, Pressure_layers,
                          alpha, cp,Vphi,Vp,Vs,K]))

def initialize_by_mass(*args):
    mass_planet = args[0]
    structural_params = args[1]
    compositional_params = args[2]
    num_mantle_layers, num_core_layers, number_h2o_layers = args[3]
    core_mass_frac = args[4]
    #pWATM = args[6]
    

    wt_frac_water, FeMg, SiMg, CaMg, AlMg, mol_frac_Fe_mantle, wt_frac_Si_core, \
     wt_frac_O_core, wt_frac_S_core, cmf_que = compositional_params

    core_rad_frac = structural_params[6]
    Mantle_potential_temp = structural_params[7]
    water_rad_frac = structural_params[8]
    water_potential_temp = structural_params[9]

    CMF = args[-1]
    print('CORE MASS FRAC: ' + str(CMF))
    print('ARGS[-1]: ' + str(args[-1]))
    #def Setup(Mp, masMan, masCor, masH2O, nr, tCrstMan, dtManCor):
    # global Th,Tss
    #    global rad, rho, rho0, vol, dmass, mass, delta,\
    #        T, nic, noc, grav, P, rhon, alpha, cp,phase

    # use inputs to find actual mass of mantle and core

    # if there is a water layer, the imput temperature is lowered because that temperature is for the crustal layer
    # also 50 shells are used for the water layer hence the nh20 vaiable

    if wt_frac_water == 0. and number_h2o_layers > 0:
       print ("You have layers of water but no water!")
       number_h2o_layers = 0

    num_layers = num_core_layers+num_mantle_layers + number_h2o_layers # add 50 shells if there is an h2O layer
    # arrays to be used

    # these grids are initialized in this function and are then a passed around through the other routines and edited each iteration
    radius_layers = np.zeros(num_layers)
    density_layers = np.zeros(num_layers)
    volume_layers = np.zeros(num_layers)
    mass_layers = np.zeros(num_layers)
    cumulative_mass = np.zeros(num_layers)
    Temperature_layers = np.zeros(num_layers)
    radius_layers = np.zeros(num_layers)
    # used for compressiofh2on funciton
    gravity_layers = np.zeros(num_layers)
    Pressure_layers = np.zeros(num_layers)
    alpha = np.zeros(num_layers)
    cp = np.zeros(num_layers)
    Vphi = np.zeros(num_layers )

    Vs = np.zeros(num_layers )
    Vp = np.zeros(num_layers)
    K =  np.zeros(num_layers)


    # 15 mineral phases + 2ice + liquid water #phasechange
    water_mass = (wt_frac_water*mass_planet)*Earth_mass
    
    #if else statement added by js for spallation calculations
    '''
    if CMF>=0.0:
        core_mass = (core_mass_frac * (mass_planet*Earth_mass))
    else:
        core_mass = (core_mass_frac * (mass_planet*Earth_mass-water_mass))
    ''' 
    '''    
    #Hack added by JS for spallation -- comment out when done
    spallation = 0.0;
    if spallation == 1.0 and CMF>=0.0:
        core_mass = core_mass_frac*mass_planet*Earth_mass
        print str(mass_planet)
        print(str(Earth_mass))
        print "COREMASS " + str(core_mass)
        core_mass_frac = core_mass/(mass_planet*Earth_mass) 
    else:
        core_mass = (core_mass_frac * (mass_planet*Earth_mass-water_mass))
        print("COREMASS 2: " + str(core_mass))
    '''
    print('CORE MASS IN PLANET: ' + str(core_mass_frac))
    water_mass = (wt_frac_water*mass_planet)*Earth_mass 
    core_mass = (core_mass_frac * (mass_planet*Earth_mass-water_mass))
    mantle_mass = (mass_planet*Earth_mass)-water_mass-core_mass
    Radius_planet_guess = 1.3

    mass_layers[0] = 0

    for i in range(num_layers):

        if i <num_core_layers:

            radius_layers[i] = (float(i)/float(num_layers))*(Radius_planet_guess*Earth_radius)
            mass_layers[i]  = core_mass/num_core_layers
            

            Temperature_layers[i] = 4500.+ (float((3000.-4500.))/float(num_core_layers))\
                                                            *float((i))

        elif i < (num_core_layers+num_mantle_layers):

            radius_layers[i] = (float(i)/float(num_layers))*(Radius_planet_guess*Earth_radius)
            mass_layers[i] = (mantle_mass/num_mantle_layers)

            Temperature_layers[i] = 2700.

        else:
            radius_layers[i] = (float(i)/float(num_layers))*(Radius_planet_guess*Earth_radius)
            mass_layers[i] = (water_mass/number_h2o_layers)


            Temperature_layers[i] = 300.

    for i in range(num_layers):
        if i > num_core_layers+num_mantle_layers:
            Pressure_layers[i] = 1
        else:
            Pressure_layers[i] = (float((5000.-(300.*10000))/float(num_core_layers+num_mantle_layers))*float(i)
                                  + 300.*10000)
            
    mass_update = np.zeros(num_layers)

    for i in range(len(mass_layers)):
        mass_update[i]=(sum(mass_layers[:i+1]))

    mass_layers= mass_update
    print("CORE MASS: " + str(mass_layers[num_core_layers]))
    print('CORE MASS IN INITIALIZE BEING PASSED: '+str(core_mass))

    #initial temperature guess of 0.5 K per km
    keys = ['mass','density','temperature','gravity','pressure',\
            'alpha','cp','Vphi''Vp','Vs','K']


    return dict(zip(keys,[mass_layers, density_layers,Temperature_layers,gravity_layers, Pressure_layers,
                          alpha, cp,Vphi,Vp,Vs,K]))



def compress_radius(*args):
    Planet = args[0]
    grids = args[1]
    Core_wt_per = args[2]
    structural_params= args[3]
    layers= args[4]
    n_iterations = 1
    max_iterations = 100


    old_rho = [10  for i in range(len(Planet['density']))]
    converge = False
    print
    while n_iterations <= max_iterations and converge == False:
        #print ("iteration #",n_iterations)


        for i in range(len(Planet['density'])):
            if np.isnan(Planet['density'][i]) == True:
                print ("Density has a nan")
                print (i, Planet['pressure'][i],Planet['temperature'][i])
                print
                #print "pressure range mantle",structural_params[0]
                #print "temperature range mantle",structural_params[1]
                sys.exit()

        Planet['density'] = minphys.get_rho(Planet,grids,Core_wt_per,layers)

        Planet['gravity'] = minphys.get_gravity(Planet,layers)

        Planet['pressure'] = minphys.get_pressure(Planet,layers)

        if n_iterations >2:
            Planet['temperature'] = minphys.get_temperature(Planet, grids, structural_params, layers)
            converge, old_rho = minphys.check_convergence(Planet['density'], old_rho)

        n_iterations+=1

    return Planet

def compress_mass(*args):
    Planet = args[0]
    grids = args[1]
    Core_wt_per = args[2]
    structural_params= args[3]
    layers= args[4]
    n_iterations = 1
    max_iterations = 100


    old_r = [10  for i in range(len(Planet['mass']))]
    converge = False
    print
    while n_iterations <= max_iterations and converge == False:
        #print ("iteration #",n_iterations)
        if n_iterations>1:
            converge,old_r = minphys.check_convergence(Planet['density'],old_r)




        for i in range(len(Planet['density'])):
            if np.isnan(Planet['density'][i]) == True:
                print ("Density has a nan")
                print (i, Planet['pressure'][i],Planet['temperature'][i])
                print
                #print "pressure range mantle",structural_params[0]
                #print "temperature range mantle",structural_params[1]
                sys.exit()


        Planet['density'] = minphys.get_rho(Planet,grids,Core_wt_per,layers)
        #print (Planet['density'][-1])

        Planet['radius'] = minphys.get_radius(Planet, layers)
        Planet['gravity'] = minphys.get_gravity(Planet,layers)
        Planet['temperature'] = minphys.get_temperature(Planet, grids, structural_params, layers)

        Planet['pressure'] = minphys.get_pressure(Planet,layers)

        
        
        n_iterations+=1

    return Planet
