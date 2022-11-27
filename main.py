import cv2
import numpy as np
from antnestcv.animation import Animation
from antnestcv.ant import Ant
from antnestcv.colony import Colony

food_img = cv2.imread('antnestcv/img_src/food/food.png')

background_img = np.zeros_like(food_img)

# background_img = np.zeros(shape = (500, 800, 3), dtype = np.uint8)

# background_img = cv2.imread('antnestcv/img_src/backgrounds/sand.jpg')

spartans = Colony(   name='Spartans',
                        init_num_ants = 500,
                        spawn_position = {'x': 50, 'y': 50},
                        color = {'b': 250, 'g':0, 'r':200})

persas = Colony(   name='Persas',
                        init_num_ants = 500,
                        spawn_position = {'x': 150, 'y': 450},
                        color = {'b': 0, 'g':200, 'r':250})

gregos = Colony(   name='Gregos',
                        init_num_ants = 200,
                        spawn_position = {'x': 450, 'y': 450},
                        color = {'b': 250, 'g': 200, 'r':100})

    
my_ants = [spartans, persas, gregos]

my_scene = Animation(background = background_img, food_layer = food_img)
frame = my_scene.display(colony_list = my_ants, wait_key = 1)

