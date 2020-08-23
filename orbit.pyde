import pickle
AU = (149.6e6 * 1000) 
SCALE = 250 / AU
with open('trajectories.data', 'rb') as f:
    history = pickle.load(f)

def setup():
    size(1920,1080,P3D)
    background(0)
    stroke(255)
    strokeWeight(2)


timestep = 0
rot = 0
def draw(): 
    clear()
    global timestep, history, rot
    pushMatrix()
    
    translate(800,500)
    rotateZ(rot)
    rotateX(rot)
    i = 100 
    for frame in history[timestep:timestep+100]:
        stroke(230, 3*i%200, 100)
        i+=1
        for body in frame:
            point(SCALE*body[0], SCALE*body[1], SCALE*body[2])
    popMatrix()
    timestep += 1
    
    rot+=PI/1000
    filename = '{:>10}'.format(str(timestep))
    saveFrame("frames/" + filename +".tif")
