import numpy as np
import cv2
from antnestcv.ant import Ant

class Scene:
    def __init__(self, background: np.array):
        
        self.background = background
        self.ants_mask = np.zeros_like(background)

    def ant_update_positions(self, ant_list: list):
        
        '''
                blue ant: channel 0
                green ant: channel 1
                red ant: channel 2    

                ant's size: 1 pixel

                ant's position (y,x) is limited to background shape
            '''
        #maintain (or clean) the mask:
        # self.ants_mask = np.zeros_like(self.background)
        
        for ant in ant_list:
            
            y = min(abs(ant.pos_y), self.background.shape[0] - 1)
            x = min(abs(ant.pos_x), self.background.shape[1] - 1)
                        
            
            self.ants_mask[y, x, 0] = ant.color['b']
            self.ants_mask[y, x, 1] = ant.color['g']
            self.ants_mask[y, x, 2] = ant.color['r']
            

            ant.ant_move(pixel_step = 1)

    def display(self, ant_list: list, wait_key: int = 1):

        while True:
            self.ant_update_positions(ant_list = ant_list)
            
            cv2.namedWindow('scene',cv2.WINDOW_GUI_EXPANDED)
            cv2.imshow('scene', self.ants_mask)
            
            
            k = cv2.waitKey(wait_key) & 0xff
            if k == 27:
                break

            