from typing import cast
import numpy as np
import math

class Sphere:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def ray_intersect(self, orig, dir, t0):
        L = np.subtract(self.center, orig)
        tca = np.dot(L, dir)
        d2 = np.dot(L,L) - tca*tca
        if d2 > self.radius * self.radius:
            return False
        thc = math.sqrt(self.radius*self.radius - d2)
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return False
        return True

def cast_ray(orig, dir, sphere):
    sphere_dist = 9999.999999
    if sphere.ray_intersect(orig, dir, sphere_dist) is False:
        return np.array([128, 152, 242])
    return np.array([101, 91, 85])

def render(sphere):
    WIDTH = 1024
    HEIGHT = 768
    framebuffer = np.zeros((WIDTH*HEIGHT, 3), dtype=np.ubyte)

    for j in range(HEIGHT):
        for i in range(WIDTH):
            #framebuffer[i+j*WIDTH][0] = (255 * i) / WIDTH 
            #framebuffer[i+j*WIDTH][1] = (255 * j) /HEIGHT
            #framebuffer[i+j*WIDTH][2] = 0
            x = (2*(i + 0.5)/WIDTH - 1)*math.tan(40/2.)*WIDTH/HEIGHT
            y = -(2*(j + 0.5)/HEIGHT - 1)*math.tan(40/2.)
            dir = np.array([x,y,-1])
            dirNorm = np.linalg.norm(dir)
            res = cast_ray(np.zeros(3), dir/dirNorm, sphere)
            framebuffer[i+j*WIDTH][0] = res[0]
            framebuffer[i+j*WIDTH][1] = res[1]
            framebuffer[i+j*WIDTH][2] = res[2]
    
    f = open("out.ppm", "wb")
    f.write(("P6\n" + str(WIDTH) + " " + str(HEIGHT) + "\n255\n").encode(encoding='UTF-8'))
    for i in range(HEIGHT*WIDTH):
        for j in range(3):
            #f.write(bytes(255 * max(0, min(1, framebuffer[i][j]))))
            f.write(framebuffer[i][j])
    f.close()

if __name__ == "__main__":
    sphere =  Sphere(np.array([-3, 0, -3]), 2)
    render(sphere)
