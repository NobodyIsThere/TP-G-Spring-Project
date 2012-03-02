# -*- coding: utf-8 -*-
# (When I edit it on the Mac, it becomes UTF-8.)
# TP-G Year 1 Theory Project
#
# Creates a system of planets orbiting a star. The system, as
# far as possible, obeys Newton's Laws of Motion.
# In the first window, titled "Main Scene", the view is locked
# onto the star. In the second window, titled "Other Frame",
# the view follows a body decided by the user. Clicking the
# "Change" button cycles through the various objects.
# The other buttons in the control window add extra planets
# (with distance and mass set by the sliders to the right) and
# enable/disable the routines for verifying Kepler's Second
# Law.
#
# -- Adding extra planets --
# Click the "+1 Planet" button to add a planet to the system.
# The upper slider sets the mass, and the lower slider sets
# the radius of the orbit.
#
# -- Kepler's Second Law --
# Any of the planets in the system can be used for the purpose
# of verifying Kepler's Second Law. The planet used is the one
# with array index (within the list "planets") equal to the
# value of keplers_law_planet_index (under "Settings" below).
# The area of each segment is calculated and printed to the
# console.
#
# -- Audio --
# The angular velocity of the followed planet (multiplied by a
# constant) is used as a sound frequency and played out of the
# computer's speakers. The "Toggle sound" button turns the
# sound output on and off.

from visual import *
from visual.controls import *
from random import *
import audiere 

# ########## Classes ####################

# Planet class. This is the template for a planet.
# The class contains variables for position, mass, velocity
# and the last position of the planet.
# The two "avatars" will be sphere objects (from VPython)
# which are what the user sees.
# avatar1 is the sphere drawn in the star's reference frame.
# avatar2 is the sphere drawn in the other frame.
class Planet:
    pos = vector(0,0,0)
    velocity = vector(0,0,0)
    mass = 0
    lastpos = vector(0,0,0)
    avatar1 = None
    avatar2 = None

    # Constructor. Accepts values for initial position,
    # velocity, mass and last position.
    def __init__(self, pos, velocity, mass, lastpos):
        self.pos = pos
        self.velocity = velocity
        self.mass = mass
        self.lastpos = lastpos

# ########## End Classes ####################

# ########## Function definitions ####################

# Creates planets with set mass and initial distance but random angular position.
# The function can create objects which orbit any other object, using the third
# parameter.
# E.g. to create a planet, use create_planet(distance, mass, Star)
# For a moon, use create_planet(distance from planet, mass, planet to orbit)
def create_planet(initial_distance, m, obj_to_orbit):
    angle = randrange(0, 6, 1) # random angle between 0 and 2pi with steps of pi/8
    planet_pos = obj_to_orbit.pos + initial_distance * vector(sin(angle),cos(angle),0) # initial position vector of planet
    mag_v = (sqrt(G*obj_to_orbit.mass/initial_distance))# magnitude of velocity of planet
    planet_v = obj_to_orbit.velocity + mag_v * -vector(-cos(angle), sin(angle), 0) # initial velocity of planet

    # Create the planet
    planet = Planet(pos=planet_pos, velocity=planet_v, mass=m, lastpos=vector(0,0,0))
    # Add the planet to the global planet list
    planets.append(planet)

# Retrieves the slider values and creates a planet with those values
def addplanet():
    Mass = float(((M_Slider.value)*(9.5/100))+0.5)
    Distance = float(((D_Slider.value)*(9.5/100))+0.5)
    create_planet(Distance, Mass, Star)

# Returns force on obj1 due to obj2
def calc_gravity(obj1, obj2):
    magnitude = (G*obj1.mass*obj2.mass)/(((obj2.pos-obj1.pos).mag)**2)
    direction = (obj2.pos - obj1.pos).norm()
    return magnitude*direction

# Calculates the position of obj in refobj's frame
def calc_relative_pos(obj, refobj):
    return obj.pos - refobj.pos

# Cycles through the various planets
def changeframe():
    global following

    # If we're following the planet at the end of the list,
    # follow the first one again. Otherwise, follow the next
    # planet.
    if(following == len(planets) - 1):
        following = 0
    else:
        following += 1

    # Remove all trails
    for planet in planets:
        planet.avatar2.trail_object.pos = []

# Returns the area a planet has swept out since the last measurement
# p is the planet, s is the star.
def kepler(p,s):
    return ((diff_angle((s.pos - p.pos),(s.pos - p.lastpos)))*mag(s.pos - p.lastpos)*mag(s.pos - p.pos)*(1./2))

# Turns K2L proof on or off.
def toggle_kepler():
    global keplers_law # Use global variable keplers_law

    # Toggle the value of keplers_law
    keplers_law = keplers_law == False

    # Update button label
    if keplers_law:
        bToggleKepler.text = 'Kepler off'
    else:
        # Remove trace
        kepler_trace.pos = []
        bToggleKepler.text = 'Kepler on'

def toggle_sound():
    global play_sound
    
    play_sound = play_sound==False
    
# ########## End function definitions ###################

# ########## Audio ################

# Open default audio device, with label "d"
d = audiere.open_device()
tone = d.create_tone(1000)
 
# Create tones on audio device "d" with frequency freq

# ########## Settings ####################
keplers_law = False
keplers_law_planet_index = 1 # Index of the planet to use in K2L calculations
keplers_law_period = 10
play_sound = True
# ########## End settings ####################

# ########## Definitions ####################

# Multiple reference frames:
# A new window is created with the system as seen from the perspective of a planet
scene1 = display(title='Main scene', visible=True)
scene2 = display(title='Other frame', x=500, visible=True)
scene1.select()

step = 0 # Current step
dt = 0.001 # timestep

# Universal gravitational constant
G = 1.0

# This is the global list of simulated bodies. The star and
# its planets are all instances of the Planet class defined
# above, and are contained in this list.
planets = []

# Star
M = 1000 # Stellar mass
# Star is an instance of Planet
Star = Planet(pos=vector(0,0,0), velocity=vector(0,0,0), mass=M, lastpos=vector(0,0,0))
# Set its avatar to a yellow sphere
Star.avatar1 = sphere(pos=vector(0,0,0),radius=0.1,color=color.yellow)
# Not calling the create_planet function, so add to list manually.
planets.append(Star)

# The index of the planet we're following.
# 0 is the star, since it's defined first.
following = 0

# Planets
create_planet(3,1,Star)
create_planet(4,1,Star)

# Trace for Kepler's Second Law proof
kepler_trace = curve(color = color.blue)

# The control window and controls
cwindow = controls()
bChangeFrame = button(pos=(-50,8), width=40, height=30, text="Change", action=changeframe)
bSpawnPlannet = button(pos=(-65,-25), width=70, height=30, text="+1 Planet", action=addplanet)
bToggleKepler = button(pos=(-65,40), width=70, height=30, text="Kepler on", action=toggle_kepler)
bToggleSound = button(pos=(-65,-55), width=85, height=30, text="Toggle sound", action=toggle_sound)
# Sliders to control variables mass and initial distance
M_Slider = slider( pos=(-10,-20), width=7, length=70, axis=(1,0,0)) # Mass slider
M_Slider.value = 50

D_Slider = slider( pos=(-10,-30), width=7, length=70, axis=(1,0,0))# Radius slider
D_Slider.value = 50

# ########## End definitions ####################

while True:

    rate(30)  # max fps

    # Play a tone dependent on the angular velocity of the
    # planet we're following, unless we're following the star.
    
    if (planets[following]!=Star) and play_sound:
        freq = planets[following].velocity.mag*500/mag(planets[following].pos - planets[0].pos)
        tone = d.create_tone(freq)
        tone.pan = 0
        tone.volume = 1
        tone.play()
        tone.pitchshift = 1
    else:
        tone.stop()

    # Draw to the first window.
    scene1.select()

    # Not necessary for newer versions or VPython; might as
    # well include it though.
    cwindow.interact()

    # Loop through each planet and perform simulation
    for planet in planets:
        for otherplanet in planets:
            # Don't include gravity with self
            if planet != otherplanet:
                # Calculate the force
                F = calc_gravity(planet, otherplanet)
                # Update velocity
                planet.velocity = planet.velocity + F*dt/planet.mass
                
        # Update position, unless it was the star.
        if planet!=Star:
            planet.pos = planet.pos+(dt*planet.velocity)

        # Remove planet from view if it leaves solar system
        if abs(planet.pos)> 20:
            # Get rid of the trails
            planet.avatar1.trail_object.pos = []
            planet.avatar2.trail_object.pos = []
            # Remove planet
            planet.visible = False
            planets.remove(planet)
            del planet
            
    # Kepler's Second Law simulation
    if keplers_law == True:
        # Take readings when step is divisible by our period
        # variable keplers_law_period
        if step%keplers_law_period==0:
            # Draw a line between the planet and the star
            kepler_trace.append(pos=planets[0].pos)
            kepler_trace.append(pos=planets[keplers_law_planet_index].pos)
            # Print the area
            print(kepler(planets[keplers_law_planet_index], planets[0]))
            # Update the last position, to calculate the next area
            planets[keplers_law_planet_index].lastpos = vector(planets[keplers_law_planet_index].pos)

    if bToggleKepler.text == 'Kepler on':  
            kepler_trace.pos = []

    # Now draw the planets
    for planet in planets:
        # Draw to the first window
        scene1.select()
        if(planet.avatar1==None):
            planet.avatar1 = sphere(pos=planet.pos,radius=0.05,color=color.blue, make_trail=True)
        planet.avatar1.pos = planet.pos

        # Draw to the second window
        scene2.select()
        if(planet.avatar2==None):
            planet.avatar2 = sphere(pos=calc_relative_pos(planet, planets[following]),radius=0.05,color=color.blue, make_trail=True)
        planet.avatar2.pos = calc_relative_pos(planet, planets[following])

        # Set all objects to blue
        planet.avatar1.color = color.blue
        planet.avatar2.color = color.blue
           
    # Colour the planet we're following in red
    planets[following].avatar1.color = color.red
    planets[following].avatar2.color = color.red
    # Colour the star yellow
    Star.avatar1.color = color.yellow
    Star.avatar2.color = color.yellow

    # Increase the step (K2L)
    step+=1
