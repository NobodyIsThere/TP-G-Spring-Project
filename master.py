# Skeleton code starting point for Yr 1 Theory Group Project

from __future__ import print_function, division
from visual import *
from random import *

#function to create planets with set mas and initial distance but random position and colour
def create_planet(initial_distance,m):
    angle = randrange(0, 6, 1) # random angle between 0 and 2pi with steps of pi/8
    
    planet_pos = initial_distance * vector(sin(angle),cos(angle),0) # initial position vector of Planet
    mag_v = (sqrt(G*M/initial_distance))#magnitude of velocity of planet
    #print(m*mag_v**2/initial_distance, G*M*m/initial_distance**2)
    planet_v = mag_v * -vector(-cos(angle), sin(angle), 0) # initial velocity of planet
    planet = sphere(pos=planet_pos,radius=0.05,color=color.blue, mass=m, velocity = planet_v)
    planets.append(planet)

def change_v(angle):
    return
    

# Definitions
dt = 0.001 # timestep
G = 1.0#0.0001

# List of planets
planets = []

# Star
M = (1000)# mass of star (G == 1)
Star = sphere(pos=vector(0,0,0),radius=0.1,color=color.yellow, velocity=vector(0,0,0), mass=M)
planets.append(Star)

# Planets
create_planet(1,1)
create_planet(4,0.5)
#create_planet(6,2)
create_planet(0.5,0.2)
create_planet(1.5,0.8)
create_planet(2.5,1.5)

# Function definitions

# Returns force on obj1 due to obj2
def calc_gravity(obj1, obj2):
    magnitude = (G*obj1.mass*obj2.mass)/(((obj2.pos-obj1.pos).mag)**2)
    ##magnitude = 0
    direction = (obj2.pos - obj1.pos).norm()
    return magnitude*direction

while True:

    rate(10)  # max fps

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
