import cv2
import numpy as np

from antnestcv.scene import Scene
from antnestcv.ant import Ant
from antnestcv.colony import Colony

# food_img = cv2.imread('antnestcv/img_src/food/food.png')
# background_img = np.zeros_like(food_img)

background_img = np.zeros(shape = (500, 800, 3), dtype = np.uint8)

# background_img = cv2.imread('antnestcv/img_src/backgrounds/sand.jpg')

colony1 = []
color1 = {'b': 250, 'g':0, 'r':200}

colony2 = []
color2 = {'b': 250, 'g':200, 'r':50}

colony3 = []
color3 = {'b': 0, 'g':200, 'r':250}

one_ant = [Ant(spawn_position = {'x': 0,'y': 0})]

x0 = 10
y0 = 10

num_of_ants = 1000

for _ in range(100000):
    colony1.append(Ant(spawn_position = {'x': 100, 'y': 100}, color = color1))

    

# for _ in range(num_of_ants):
#     colony2.append(Ant(spawn_position = {'x': 200, 'y': 200}, color = color2))

for _ in range(50000):
    colony3.append(Ant(spawn_position = {'y': 400, 'x': 250}, color = color3))
    
    
my_ants = colony1 + colony3

my_scene = Scene(background = background_img, food_layer = None)
my_scene.display(ant_list = my_ants, wait_key = 1)

