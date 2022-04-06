import numpy as np
import cv2
from antnestcv.ant import Ant

'''
    #TODO
    1. Implementar 'grab food'
        1.1 Compute the centers of each food's contour
        1.2 
    2. Implementar as trails: (pixel food_img) passa para (pixel trails)    
'''
class Scene:
    def __init__(self, background: np.array, food_img: np.array):
        
        '''
            self.backgroud: 3 channel image
            self.food_img: 3 channel image 
            self.food_bw: 1 channel image
            self.food_contours: list[np.array([y,x]), np.array([y,x]), ..]

        '''

        self.background = background
        self.ants_mask = np.zeros_like(background)
        self.trails = np.zeros_like(background)
        self.food_img = food_img
        self.food_contours: list = []

        if self.food_img is not None:
            self.food_bw = cv2.cvtColor(self.food_img, cv2.COLOR_BGR2GRAY)
            self.food_contours = self.find_food_contours()
                        
            assert self.background.shape == self.food_img.shape
            
                        
            
            ##*uncomment to draw the contours:
            # cv2.drawContours(
            #     image = self.scene,
            #     contours = self.food_contours,
            #     contourIdx = -1,
            #     color = (255,0,0),
            #     thickness = 2)

            ##*Considering just one piece of food (len(self.food_contours = 1)):
            self.food_contours = self.food_contours[0].squeeze()
                        
            #Compute the center of a piece of food:
            self.food_center_position = {
                'x':  int(np.mean(self.food_contours[:,0])),
                'y': int(np.mean(self.food_contours[:,1]))}
            
            self.food_mean_radius = self.compute_mean_radius(
                food_contour_x_pts = self.food_contours[:,0],
                food_contour_y_pts = self.food_contours[:,1],
                food_center = self.food_center_position)

            self.background[self.food_center_position['y'], self.food_center_position['x']] = [255, 255, 255]
            
            ##*Uncomment to draw circle
            cv2.circle(
                self.background,
                (self.food_center_position['x'],
                self.food_center_position['y']), 
                self.food_mean_radius,
                (50,50,50), 1)



            #scene: background + food  
            self.scene = cv2.addWeighted(
                src1 = self.background, alpha = 1,
                src2 = self.food_img, beta = 1,
                gamma = 1)

        else:
            self.food_img = np.zeros_like(self.background)
            #scene: background + food
            self.scene = cv2.addWeighted(
                src1 = self.background, alpha = 1,
                src2 = self.food_img, beta = 1,
                gamma = 1)

    @staticmethod
    def compute_mean_radius(    food_contour_x_pts: np.array,
                                food_contour_y_pts: np.array,
                                food_center: dict) -> int:
        
        dy = food_contour_y_pts - food_center['y']
        dx = food_contour_x_pts - food_center['x']
        distances = np.sqrt(dx**2 + dy**2)
        
        mean_radius = int(np.mean(distances))

        return mean_radius




    def find_food_contours(self) -> list:
        '''
            Find the edges of the food (target).
            Only contours with more than 50 points will be considered.

            -> _contours: list(np.array)
            -> self.food_contours: list(np.array), we can consider each array as 
            the contour of a food object.
           
           https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html             
        '''
        _ , thresh = cv2.threshold(self.food_bw, 0, 255, 0)
        _contours, _ = cv2.findContours(
                        thresh,
                        cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_NONE)
        
        
        for contour in _contours:
            if len(contour) > 50:
                self.food_contours.append(contour)
        
        return self.food_contours
   
  

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

            ant.ant_move(
                ymax = background_height,
                xmax = background_width,
                pixel_step = 1)
                
            dy = ant.pos_y - self.food_center_position['y']
            dx = ant.pos_x - self.food_center_position['x']
            
            ant.lift_food(
                food_center_pos = self.food_center_position,
                tolerance = 1)

    def display(self, ant_list: list, wait_key: int = 1):

        while True:
            
            self.ant_update_positions(ant_list = ant_list)

            #scene: background + ants + food
            scene = cv2.addWeighted(    src1 = self.scene, alpha = 1,
                                        src2 = self.ants_mask, beta = 1,
                                        gamma = 1)
            
            cv2.namedWindow('scene',cv2.WINDOW_GUI_EXPANDED)
            cv2.imshow('scene', scene)
            
            
            k = cv2.waitKey(wait_key) & 0xff
            if k == 27:
                break

            