import cv2
import numpy as np

from antnestcv.scene import Scene
from antnestcv.ant import Ant



background_img = np.zeros(shape = (800,800,3), dtype = np.uint8)


colony1 = []
color1 = {'b': 250, 'g':0, 'r':200}

colony2 = []
color2 = {'b': 250, 'g':200, 'r':50}


x0 = 0
y0 = 0

num_of_ants = 100

for _ in range(num_of_ants):
    colony1.append(Ant(spawn_position = (y0,x0), color = color1))

    x0 += 1
    y0 += 1

for _ in range(num_of_ants - 50):
    colony2.append(Ant(spawn_position = ((800 - y0),(800 - x0)), color = color2))

    x0 -=1
    
my_ants = colony1 + colony2

my_scene = Scene(background = background_img)
my_scene.display(ant_list = my_ants, wait_key = 50)

