# -*- coding: utf-8 -*-
# For some reason it's now UTF-8
# Skeleton code starting point for Yr 1 Theory Group Project

from visual import *
from random import *

#function to create planets with set mas and initial distance but random position and colour
def create_planet(initial_distance,m):
    angle = randrange(0, 6, 1) # random angle between 0 and 2pi with steps of pi/8
    planet_pos = initial_distance * vector(sin(angle),cos(angle),0) # initial position vector of Planet
    mag_v = (sqrt(G*M/initial_distance))#magnitude of velocity of planet
    print(m*mag_v**2/initial_distance, G*M*m/initial_distance**2)
    planet_v = mag_v * -vector(cos(angle), sin(angle), 0) # initial velocity of planet
    planet = sphere(pos=planet_pos,radius=0.05,color=color.blue, mass=m, velocity = planet_v)
    planets.append(planet)

# ########## Settings ####################
keplers_law = False
keplers_law_planet_index = 1 # Index of the planet to use in K2L calculations
keplers_law_period = 10
# ########## End settings ####################

# ########## Definitions ####################
step = 0 # Current step
dt = 0.001 # timestep
G = 1.0

# List of planets
planets = []

# Star
M = 1000# mass of star (G == 1)
Star = sphere(pos=vector(0,0,0),radius=0.1,color=color.yellow, velocity=vector(0,0,0), mass=M)
planets.append(Star)

# Planets
##create_planet(10,1)
##create_planet(20,1)
##create_planet(50,4)
##create_planet(80,6)
##create_planet(60,7)
##create_planet(30,3)
create_planet(3,1)

# Trace for Kepler's Second Law proof
kepler_trace = curve(color = color.blue)

# ########## End definitions ####################

# ########## Function definitions ####################

# Returns force on obj1 due to obj2
def calc_gravity(obj1, obj2):
    magnitude = (G*obj1.mass*obj2.mass)/(((obj2.pos-obj1.pos).mag)**2)
    direction = (obj2.pos - obj1.pos).norm()
    return magnitude*direction

# Returns the area a planet has swept out since the last measurement
# p is the planet, s is the star.
def kepler(p,s):
    return ((diff_angle((s.pos - p.pos),(s.pos - p.lastpos)))*mag(s.pos - p.lastpos)*mag(s.pos - p.pos)*(1./2))

# ########## End function definitions ###################

while True:

    rate(30)  # max fps

    for planet in planets:
        for otherplanet in planets:
            if planet != otherplanet:
                # Calculate the force
                F = calc_gravity(planet, otherplanet)
                # Update velocity
                planet.velocity = planet.velocity + F*dt/planet.mass
                #planet.velocity = F
                
        # Update position
        if planet!=Star:
            planet.pos = planet.pos+(dt*planet.velocity)

    if keplers_law == True:
        if step%keplers_law_period==0:
            kepler_trace.append(pos=planets[0].pos)
            kepler_trace.append(pos=planets[keplers_law_planet_index].pos)
            print(kepler(planets[keplers_law_planet_index], planets[0]))
            planets[keplers_law_planet_index].lastpos = vector(planets[keplers_law_planet_index].pos)

    step+=1
