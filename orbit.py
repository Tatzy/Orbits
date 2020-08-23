from math import sqrt, acos, atan2, sin, cos
from time import sleep
from random import randint, uniform
import pickle

G = 6.67428e-11

# Assumed scale: 100 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 250 / AU

class Point():
    def __init__(self,px,py,pz,vx,vy,vz,m):
        self.px = px
        self.py = py
        self.pz = pz
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = m

    def attraction(self, other):
        if self == other: pass
        else:
            dx = (self.px - other.px)
            dy = (self.py - other.py)
            dz = (self.pz - other.pz)
            d = sqrt(dx**2 + dy**2 + dz**2)

            if d == 0:
                return 0,0,0
            else:
                theta = atan2(dy,dx)
                phi = acos(dz/d)

                F = G * self.mass * other.mass / d**2

                fx = sin(phi)*cos(theta)*F
                fy = sin(phi)*sin(theta)*F
                fz = cos(phi)*F

                return -fx,-fy,-fz

def update(bodies):
    time = 24*3600
    for body in bodies:
        total_fx = total_fy = total_fz = 0
        for other in bodies:
            if body != other:
                fx, fy, fz = body.attraction(other)
                total_fx += fx
                total_fy += fy
                total_fz += fz
        body.vx += total_fx / body.mass * time
        body.vy += total_fy / body.mass * time
        body.vz += total_fz / body.mass * time

        body.px += body.vx * time
        body.py += body.vy * time
        body.pz += body.vz * time


sun = Point(0,0,0,0,0,0,1.98892 * 10**30)
earth = Point(-1*AU, 0,0, 0, 29.783 * 1000,0,5.9742 * 10**24)

bodies = []
history = []

for i in range(0,20):
        position = randint(-10,10)
        velocity = randint(5000,200000)
        mass = randint(10**10, 10**20)
        theta = uniform(0, 6.28)
        phi = uniform(0, 6.28)
        
        bodies.append(Point(position*sin(phi)*cos(theta)*AU,position*sin(phi)*sin(theta)*AU,position*cos(phi),velocity*sin(phi)*cos(theta),velocity*sin(phi)*sin(theta),velocity*cos(phi),mass))

bodies.append(sun)

for t in range(0,10000):
    print("Working on step: {}.".format(t))
    update(bodies)
    frame = []
    for body in bodies:
        frame.append([body.px, body.py, body.pz])
    history.append(frame)

with open('trajectories.data', 'wb') as f:
    pickle.dump(history,f, protocol=2)
    f.close()
        



