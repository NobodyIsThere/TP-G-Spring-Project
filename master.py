# -*- coding: utf-8 -*-
# For some reason it's now UTF-8
# Skeleton code starting point for Yr 1 Theory Group Project

from visual import *
from visual.controls import *
from random import *

# ########## Classes ####################

class Planet:
    pos = vector(0,0,0)
    velocity = vector(0,0,0)
    mass = 0
    lastpos = vector(0,0,0)
    avatar1 = None
    avatar2 = None

    def __init__(self, pos, velocity, mass, lastpos):
        self.pos = pos
        self.velocity = velocity
        self.mass = mass
        self.lastpos = lastpos

# ########## Classes ####################

# ########## Function definitions ####################

#function to create planets with set mass and initial distance but random position and colour
def create_planet(initial_distance,m):
    angle = randrange(0, 6, 1) # random angle between 0 and 2pi with steps of pi/8
    planet_pos = initial_distance * vector(sin(angle),cos(angle),0) # initial position vector of Planet
    mag_v = (sqrt(G*M/initial_distance))#magnitude of velocity of planet
    print(m*mag_v**2/initial_distance, G*M*m/initial_distance**2)
    planet_v = mag_v * -vector(-cos(angle), sin(angle), 0) # initial velocity of planet
    planet = Planet(pos=planet_pos, velocity=planet_v, mass=m, lastpos=vector(0,0,0))
    planets.append(planet)

# Returns force on obj1 due to obj2
def calc_gravity(obj1, obj2):
    magnitude = (G*obj1.mass*obj2.mass)/(((obj2.pos-obj1.pos).mag)**2)
    direction = (obj2.pos - obj1.pos).norm()
    return magnitude*direction

def calc_relative_pos(obj, refobj):
    return obj.pos - refobj.pos

def changeframe():
    global following
    if(following == len(planets) - 1):
        following = 0
    else:
        following += 1

    for planet in planets:
        planet.avatar2.trail_object.pos = []

# Returns the area a planet has swept out since the last measurement
# p is the planet, s is the star.
def kepler(p,s):
    return ((diff_angle((s.pos - p.pos),(s.pos - p.lastpos)))*mag(s.pos - p.lastpos)*mag(s.pos - p.pos)*(1./2))

# ########## End function definitions ###################

# ########## Settings ####################
keplers_law = True
keplers_law_planet_index = 1 # Index of the planet to use in K2L calculations
keplers_law_period = 10
# ########## End settings ####################

# ########## Definitions ####################

# Multiple reference frames:
# A new window is created with the system as seen from the perspective of a planet
# The windows
scene1 = display(title='Main scene', visible=True)
scene2 = display(title='Other frame', x=500, visible=True)
scene1.select()

step = 0 # Current step
dt = 0.001 # timestep
G = 1.0

# List of planets
planets = []

# Star
M = 1000# mass of star (G == 1)
Star = Planet(pos=vector(0,0,0), velocity=vector(0,0,0), mass=M, lastpos=vector(0,0,0))
Star.avatar1 = sphere(pos=vector(0,0,0),radius=0.1,color=color.yellow)
planets.append(Star)

# The index of the planet we're following
following = 0

# Planets
create_planet(3,1)
create_planet(4,1)
create_planet(5,1)

# Trace for Kepler's Second Law proof
kepler_trace = curve(color = color.blue)

# The control window and controls
cwindow = controls()
bChangeFrame = button(pos=(0,0), width=40, height=30, text="Change", action=changeframe)

# ########## End definitions ####################

while True:

    rate(30)  # max fps
    scene1.select()

    cwindow.interact()

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

    # Now draw the planets
    for planet in planets:
        scene1.select()
        if(planet.avatar1==None):
            planet.avatar1 = sphere(pos=planet.pos,radius=0.05,color=color.blue, make_trail=True)
        planet.avatar1.pos = planet.pos

        scene2.select()
        if(planet.avatar2==None):
            planet.avatar2 = sphere(pos=calc_relative_pos(planet, planets[following]),radius=0.05,color=color.blue, make_trail=True)
        planet.avatar2.pos = calc_relative_pos(planet, planets[following])

        planet.avatar1.color = color.blue
        planet.avatar2.color = color.blue

    planets[following].avatar1.color = color.red
    planets[following].avatar2.color = color.red
    Star.avatar1.color = color.yellow
    Star.avatar2.color = color.yellow
    step+=1
