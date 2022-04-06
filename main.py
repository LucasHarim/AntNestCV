import cv2
import numpy as np

from antnestcv.scene import Scene
from antnestcv.ant import Ant


food_img = cv2.imread('antnestcv/img_src/food/food.png')
background_img = np.zeros_like(food_img)

# background_img = cv2.imread('antnestcv/img_src/backgrounds/sand.jpg')

colony1 = []
color1 = {'b': 250, 'g':0, 'r':200}

colony2 = []
color2 = {'b': 250, 'g':200, 'r':50}

colony3 = []
color3 = {'b': 0, 'g':200, 'r':250}

one_ant = [Ant(spawn_position = (0,0))]

x0 = 10
y0 = 10

num_of_ants = 1000

for _ in range(num_of_ants):
    colony1.append(Ant(spawn_position = (10,10), color = color1))

    

for _ in range(num_of_ants):
    colony2.append(Ant(spawn_position = (200,200), color = color2))

for _ in range(num_of_ants):
    colony2.append(Ant(spawn_position = (background_img.shape[0] - 20,background_img.shape[1] - 20), color = color3))
    
    
my_ants = colony1 + colony2 + colony3

my_scene = Scene(background = background_img, food_img = food_img)
my_scene.display(ant_list = my_ants, wait_key = 1)

