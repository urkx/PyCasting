from typing import cast
import numpy as np
import math

class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

class Material:
    def __init__(self, color):
        self.color = color

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def ray_intersect(self, orig, dir, t0_):
        res = [False, 0]
        t0 = t0_
        L = np.subtract(self.center, orig)
        tca = np.dot(L, dir)
        d2 = np.dot(L,L) - tca*tca
        if d2 > self.radius * self.radius:
            res[0] = False
            res[1] = t0
            return res
        thc = math.sqrt(self.radius*self.radius - d2)
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            res[0] = False
            res[1] = t0
            return res
        res[0] = True
        res[1] = t0
        return res

def scene_intersect(orig, dir, spheres, hit, N, material):
    sphere_dist = 9999.999999
    res = [False, np.zeros(3), np.zeros(3), np.zeros(3)]
    dist_i = 0
    for sphere in spheres:
        res2 = sphere.ray_intersect(orig, dir, dist_i)
        if res2[0] and res2[1] < sphere_dist:
            sphere_dist = res2[1]
            hit = orig + dir * res2[1]
            N_aux = np.subtract(hit, sphere.center)
            res[1] = N_aux / np.linalg.norm(N_aux)
            res[2] = sphere.material.color
            res[3] = hit
        dist_i = res2[1]
    res[0] = sphere_dist < 1000 
    return res

def cast_ray(orig, dir, spheres, lights):
    point = np.zeros(3)
    N = np.zeros(3)
    material = Material(np.zeros(3))

    res = scene_intersect(orig, dir, spheres, point, N, material)

    if res[0] is False:
        return np.array([128, 152, 242])
    
    light_intensity = 0
    for light in lights:
        light_dir = np.subtract(light.position, res[3])
        light_dir_aux = np.linalg.norm(light_dir)
        light_dir = light_dir/light_dir_aux
        light_intensity += light.intensity * max(0, np.dot(light_dir, res[1]))

    return res[2] * light_intensity
    

def render(spheres, lights):
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
            res = cast_ray(np.zeros(3), dir/dirNorm, spheres, lights)
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
    material_rojo = Material(np.array([95, 11, 43]))
    material_marron = Material(np.array([101, 91, 85]))
    light1 = Light(np.array([-20, 20, 20]), 1.5)
    light2 = Light(np.array([10, 10, 10]), 0.9)
    sphere1 =  Sphere(np.array([-6, 0, -10]), 2, material_marron)
    sphere2 = Sphere(np.array([-4, 0, -12]), 3, material_rojo)
    spheres = [sphere1, sphere2]
    lights = [light1, light2]
    render(spheres, lights)
