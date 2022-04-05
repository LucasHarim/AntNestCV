import numpy as np
import cv2
from antnestcv.ant import Ant

class Scene:
    def __init__(self, background: np.array, sugar_img: np.array):
        
        '''
            self.backgroud: 3 channel image
            self.sugar_img: 3 channel image 
            self.sugar_bw: 1 channel image
            self.sugar_contours: list[np.array([y,x]), np.array([y,x]), ..]

        '''

        self.background = background
        self.ants_mask = np.zeros_like(background)
        self.trails = np.zeros_like(background)
        self.sugar_img = sugar_img
        self.sugar_contours: list = []

        if self.sugar_img is not None:
            self.sugar_bw = cv2.cvtColor(self.sugar_img, cv2.COLOR_BGR2GRAY)
            self.sugar_contours = self.find_sugar_contours()
            
            assert self.background.shape == self.sugar_img.shape
            
            #scene: background + sugar
            self.scene = cv2.addWeighted(
                src1 = self.background, alpha = 1,
                src2 = self.sugar_img, beta = 1,
                gamma = 1)
            
            #*uncomment to draw the contours
            cv2.drawContours(
                image = self.scene,
                contours = self.sugar_contours,
                contourIdx = -1,
                color = (255,0,0),
                thickness = 2)
                        

        else:
            self.sugar_img = np.zeros_like(self.background)
            #scene: background + sugar
            self.scene = cv2.addWeighted(
                src1 = self.background, alpha = 1,
                src2 = self.sugar_img, beta = 1,
                gamma = 1)


    def find_sugar_contours(self) -> list:
        '''
            Find the edges of the sugar (target).
            Only contours with more than 50 points will be considered.

            -> _contours: list(np.array)
            -> self.sugar_contours: list(np.array), we can consider each array as 
            the contour of a sugar object.
                        
        '''
        _ , thresh = cv2.threshold(self.sugar_bw, 0, 255, 0)
        _contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        
        for contour in _contours:
            if len(contour) > 50:
                self.sugar_contours.append(contour)
        
        return self.sugar_contours
    



    def ant_update_positions(self, ant_list: list):
        
        '''
                blue ant: channel 0
                green ant: channel 1
                red ant: channel 2    

                ant's size: 1 pixel

                ant's position (y,x) is limited to background shape
            '''
        #*maintain (or clean) the mask:
        self.ants_mask = np.zeros_like(self.background)
        
        background_height = self.background.shape[0]
        background_width = self.background.shape[1]
        for ant in ant_list:
           
            self.ants_mask[ant.pos_y, ant.pos_x, 0] = ant.color['b']
            self.ants_mask[ant.pos_y, ant.pos_x, 1] = ant.color['g']
            self.ants_mask[ant.pos_y, ant.pos_x, 2] = ant.color['r']

            ant.ant_move(ymax = background_height, xmax = background_width, pixel_step = 1)

    def display(self, ant_list: list, wait_key: int = 1):

        while True:
            
            self.ant_update_positions(ant_list = ant_list)

            #scene: background + ants + sugar
            scene = cv2.addWeighted(    src1 = self.scene, alpha = 1,
                                        src2 = self.ants_mask, beta = 1,
                                        gamma = 1)
            
           
            cv2.namedWindow('scene',cv2.WINDOW_GUI_EXPANDED)
            cv2.imshow('scene', scene)
            
            
            k = cv2.waitKey(wait_key) & 0xff
            if k == 27:
                break

            