import numpy as np
import cv2
from antnestcv.ant import Ant
from antnestcv.colony import Colony
from antnestcv.food import Food

'''
    #TODO
    1. Implementar 'grab food'
        1.1 Compute the centers of each food's contour
        1.2 
    2. Implementar as trails: (pixel food_layer) passa para (pixel trails)    
'''
class Animation:
    def __init__(self, background: np.array, food_layer: np.array):
        
        '''
            self.backgroud: 3 channel image
            self.food_layer: 3 channel image 
            self.food_bw: 1 channel image
            self.food_contours: list[np.array([y,x]), np.array([y,x]), ..]

        '''

        self.background = background
        self.ants_layer = np.zeros_like(background)
        self.trails = np.zeros_like(background)
        self.food = Food(food_layer = food_layer) #TODO: self.food added. I need
        # to update this code
          

    def update_state(self, colony_list: list):
        
        '''
                blue ant: channel 0
                green ant: channel 1
                red ant: channel 2    

                ant's size: 1 pixel

                ant's position (y,x) is limited to background shape
            '''
        #*maintain (or clean) the layer:
        self.ants_layer = np.zeros_like(self.background)
        
        background_height = self.background.shape[0]
        background_width = self.background.shape[1]

        for colony in colony_list:
            
            #* Update Ant's positions:
            colony.update_ants_positions(ymax = background_height, xmax = background_width)
            self.ants_layer[colony.ants_pos_y, colony.ants_pos_x, 0] = colony.color['b']
            self.ants_layer[colony.ants_pos_y, colony.ants_pos_x, 1] = colony.color['g']
            self.ants_layer[colony.ants_pos_y, colony.ants_pos_x, 2] = colony.color['r']

            #*Update food:
            self.food.update_food(ants_pos_x = colony.ants_pos_x, ants_pos_y = colony.ants_pos_y)

    def display(self, colony_list: list, wait_key: int = 1):

        while True:
            
            self.update_state(colony_list = colony_list)
            
            #scene: background + food  
            self.scene = cv2.addWeighted(
                src1 = self.background, alpha = 1,
                src2 = self.food.food_layer, beta = 1,
                gamma = 1)
            
            #scene: background + ants + food
            scene = cv2.addWeighted(    src1 = self.scene, alpha = 1,
                                        src2 = self.ants_layer, beta = 1,
                                        gamma = 1)
            
            cv2.namedWindow('scene',cv2.WINDOW_GUI_EXPANDED)
            cv2.imshow('scene', scene)
            
            
            k = cv2.waitKey(wait_key) & 0xff
            if k == 27:
                break

            