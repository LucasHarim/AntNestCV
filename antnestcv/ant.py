import numpy as np
import cv2
from random import sample

class Ant:

    
    def __init__(self, spawn_position: tuple, color: dict = {'b':0, 'g':0, 'r':255}):
        
        '''
            spawn_position: (y0, x0)
            color: {'b' ,'g', 'r'} ( b,g,r E [0,255])

        '''

        self.spawn_position = spawn_position
        self.pos_y = spawn_position[0]
        self.pos_x = spawn_position[1]
        self.color = color
        
        
    def ant_move(self, ymax: int, xmax: int,pixel_step: int) -> None:
        
        ymax -= 1
        xmax -= 1

        '''
            ymax: background height
            xmax: background width
            pixel_step: pixel deslocado por loop

        '''
        
        self.y_possible_movements = [0, max(1 - self.pos_y, 1), min(ymax - self.pos_y, -1)]
        self.x_possible_movements = [0, max(1 - self.pos_x, 1), min(xmax - self.pos_x, -1)]
        
        # self.y_possible_movements = [0, min(self.pos_y -1, 1), min(self.pos_y%ymax, -1)]
        # self.x_possible_movements = [0, max(1 - self.pos_x, 1)]

        # print(self.pos_y, self.pos_x)
        # print(self.y_possible_movements, self.x_possible_movements)
        # print('\n')

        move_y = sample(self.y_possible_movements , 1).pop()
        move_x = sample(self.x_possible_movements, 1).pop()

        self.pos_y += move_y
        self.pos_x += move_x

        self.pos_y = min(ymax, abs(self.pos_y))
        self.pos_x = min(xmax, abs(self.pos_x))

        '''
            #TODO: 
            Ajeitar o movimento aleatório para nao permitir 
            sair de 0 -> ymax, xmax
        '''