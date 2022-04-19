import numpy as np
import cv2

class Food:
    def __init__(self, food_layer: np.array):
        
        self.food_layer = food_layer
        self.image_bw: np.array = cv2.cvtColor(self.food_layer, cv2.COLOR_BGR2GRAY)
        _ , self.thresh = cv2.threshold(self.image_bw, 0, 255, 0)
        
        self.area = len(np.nonzero(self.thresh)[0])
        
        self.food_pts_x, self.food_pts_y = self.food_pts(thresh = self.thresh)
        self.x_contours, self.y_contours = self.find_food_contours(thresh = self.thresh) 
        self.some_x_contours, self.some_y_contours = self.some_pts_in_contour(
            x_contour = self.x_contours,
            y_contour = self.y_contours,
            percent = 0.02)

        self.lift_food = np.zeros(shape = (1, self.area), dtype = bool)

        
    @staticmethod
    def find_food_contours(thresh) -> list:
        '''
            Find the edges of the food (target).
            Only contours with more than 50 points will be considered.

            -> _contours: list(np.array)
            -> self.food_contours: list(np.array), we can consider each array as 
            the contour of a food object.
            
            https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html             
        '''
        # _ , thresh = cv2.threshold(self.image_bw, 0, 255, 0)
        _contours, _ = cv2.findContours(
                        thresh,
                        cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_NONE)
        
        food_contours = []
        for contour in _contours:
            if len(contour) > 50:
                food_contours.append(contour)
        
        x_contours, y_contours = [], []
        for pt in food_contours[0].squeeze():
            x_contours.append(pt[0])
            y_contours.append(pt[1])
        
        return x_contours, y_contours
        
    @staticmethod
    def some_pts_in_contour(x_contour: list, y_contour: list, percent: float) -> list:
        
        assert len(x_contour) == len(y_contour)
        
        
        length = len(x_contour)
        n_pts = min(length, int(length * percent), 1) 

        '''
            length = n_pts * q + r
            q = length//n_pts
            r = length%n_pts        
        '''
        r = length%n_pts
        q = length//n_pts
        new_length = length - r

        x_of_interest = x_contour[:new_length:q]
        y_of_interest = y_contour[:new_length:q]
        return x_of_interest, y_of_interest
    
    @staticmethod
    def food_pts(thresh) -> list:
        '''
            #*Structured Arrays
            https://numpy.org/doc/stable/user/basics.rec.html
            food_pts: np.array([(y1, x1, (y2, x2), ...], dtype = [('y', np.uint8), ('x', np.uint8)])
        '''
        
        all_food_pts = np.nonzero(thresh)
        food_pts_y, food_pts_x = all_food_pts[0], all_food_pts[1]
                
        # food_pts = np.array([(food_y[i], food_x[i]) for i in range(n_pts)],
        #                     dtype = [('y', np.uint32), ('x', np.uint32)])
        return food_pts_x, food_pts_y

    def ant_detection(self, ants_pos_x: np.array, ants_pos_y: np.array) -> None:
        
        food_bool_x = np.in1d(ants_pos_x, self.food_pts_x)
        food_bool_y = np.in1d(ants_pos_y, self.food_pts_y)        
        
        self.lift_food = food_bool_x * food_bool_y        
        
        
    def update_food(self, ants_pos_x: np.array, ants_pos_y: np.array) -> None:
        '''
            #TODO:
            1. Try to remove a list of points instead of just removing one
                self.food_pts = self.food_pts[array([True, True, False, ..])]
            #!2. There's something wrong with self.lift_food. When num_ants = n,
                self.lift_food.shape is assuming even n^2: #* Solved
        '''

        self.ant_detection(ants_pos_x = ants_pos_x, ants_pos_y = ants_pos_y)
                
        remove_pts_x = ants_pos_x[self.lift_food]
        remove_pts_y = ants_pos_y[self.lift_food]
        
        
        self.food_layer[remove_pts_y, remove_pts_x] = [0, 0, 0]
        self.image_bw[remove_pts_y, remove_pts_x] = 0
        self.thresh[remove_pts_y, remove_pts_x] = 0
        self.area -= len(remove_pts_x)
        
        # self.x_contours.remove(remove_pt_x)
        # self.y_contours.remove(remove_pt_y)
        # self.some_x_contours, self.some_y_contours = self.some_pts_in_contour(
        #     x_contour = self.x_contours,
        #     y_contour = self.y_contours,
        #     percent = 0.02)