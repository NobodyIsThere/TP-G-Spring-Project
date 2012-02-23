#Skeleton code starting point for Yr 1 Theory Group Project

from visual import *

dt = 0.0001 # timestep # the time step can be decreased to decrease the approximation
step = 1 # loop counter

#  Define the star, planets and constants
M = 1000 # mass of star (G == 1)
m1 = 1 # mass of planet 1
initpos1 = vector(0,1,0) # initial position vector of Planet1
Planet1 = sphere(pos=initpos1,radius=0.05*m1,color=color.blue, lastpos = (0,1,0))

Star = sphere(pos=vector(0,0,0),radius=0.1,color=color.yellow)
vel1 = -vector(25, 0, 0) # initial velocity of planet 1
trajectory=curve(color=color.white)
kepler=curve(color=color.blue)
def calc_area(p,s):
    return ((diff_angle((s.pos - p.pos),(s.pos - p.lastpos)))*mag(s.pos - p.lastpos)*mag(s.pos - p.pos)*(1/2)) #calculates the area between each step of the planet
    
while step <= 12000:

    rate(10000)
    denom1M = mag(Planet1.pos) ** 3 
    dv1M = dt * Planet1.pos * M / denom1M
    vel1 = vel1 - dv1M
    Planet1.pos = Planet1.pos + vel1 * dt
    trajectory.append (Planet1.pos)
    step = step + 1
    if step%150 == 0:   #by changing this value, the angle swept out between each measurement can be decreased, this also decreases error
        kepler.append (pos=(Star.pos))
        kepler.append (pos=(Planet1.pos))
        print (calc_area(Planet1,Star))
        Planet1.lastpos = copy(Planet1.pos)

#the area will vary due to the planet slowly falling towards the sun, this can be considered for
        
        
        
        
        
