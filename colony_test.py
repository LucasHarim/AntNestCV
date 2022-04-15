import cv2
import numpy as np
from antnestcv.colony import Colony


spartans = Colony(   name='Spartans',
                        init_num_ants = 10000,
                        spawn_position = {'x': 250, 'y': 300},
                        color = {'b': 250, 'g':0, 'r':200})

persas = Colony(   name='Persas',
                        init_num_ants = 50000,
                        spawn_position = {'x': 250, 'y': 400},
                        color = {'b': 0, 'g':200, 'r':250})

gregos = Colony(   name='Gregos',
                        init_num_ants = 20000,
                        spawn_position = {'x': 350, 'y': 450},
                        color = {'b': 250, 'g': 200, 'r':100})


# background_img[spartans.ants_pos_y, ants_pos_x, 0] = spartans.color['b']
# background_img[spartans.ants_pos_y, ants_pos_x, 1] = spartans.color['g']
# background_img[spartans.ants_pos_y, ants_pos_x, 2] = spartans.color['r']

background_img = np.zeros(shape = (500, 800, 3), dtype = np.uint8)

while True:

    #update background
    background_img = np.zeros(shape = (500, 800, 3), dtype = np.uint8)

    height = background_img.shape[0]
    width = background_img.shape[1]
    spartans.update_ants_positions(ymax = height, xmax = width)


    background_img[spartans.ants_pos_y, spartans.ants_pos_x, 0] = spartans.color['b']
    background_img[spartans.ants_pos_y, spartans.ants_pos_x, 1] = spartans.color['g']
    background_img[spartans.ants_pos_y, spartans.ants_pos_x, 2] = spartans.color['r']
    
    persas.update_ants_positions(ymax = height, xmax = width)
    background_img[persas.ants_pos_y, persas.ants_pos_x, 0] = persas.color['b']
    background_img[persas.ants_pos_y, persas.ants_pos_x, 1] = persas.color['g']
    background_img[persas.ants_pos_y, persas.ants_pos_x, 2] = persas.color['r']

    gregos.update_ants_positions(ymax = height, xmax = width)
    background_img[gregos.ants_pos_y, gregos.ants_pos_x, 0] = gregos.color['b']
    background_img[gregos.ants_pos_y, gregos.ants_pos_x, 1] = gregos.color['g']
    background_img[gregos.ants_pos_y, gregos.ants_pos_x, 2] = gregos.color['r']


    cv2.namedWindow('Colony', cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow('Colony', background_img)

    k = cv2.waitKey(75) & 0xff
    
    if k == 27:
        break