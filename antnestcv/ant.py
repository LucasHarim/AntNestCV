import numpy as np
import cv2
from random import sample

class Ant:

    
    def __init__(self, spawn_position: tuple, color: dict):
        
        '''
            spawn_position: (y0, x0)
            color: {'b' ,'g', 'r'} ( b,g,r E [0,255])

        '''

        self.spawn_position = spawn_position
        self.pos_y = spawn_position[0]
        self.pos_x = spawn_position[1]
        self.color = color
        
        
    def ant_move(self, pixel_step: int) -> None:
        move_y = sample([-1,0,1], 1).pop()
        move_x = sample([-1,0,1], 1).pop()

        self.pos_y += move_y
        self.pos_x += move_x
    