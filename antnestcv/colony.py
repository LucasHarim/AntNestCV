import numpy as np
from antnestcv.ant import Ant

class Colony:
    def __init__(   self,
                    name: str,
                    init_num_ants: int,
                    spawn_position: dict,                    
                    color: dict):

        '''
            name: Name of colony
            init_num_ants: Initial number of ants 
            spawn_position: {'x': int, 'y': int}
            color: {'r': int, 'g': int, 'b': int}
        '''

        self.name: str = name
        self.init_num_ants: int = init_num_ants
        self.spawn_position: dict = spawn_position
        self.color: dict = color
        
        self.ants_pos_y = self.spawn_position['y']*np.ones(shape = (self.init_num_ants), dtype= int)
        self.ants_pos_x = self.spawn_position['x']*np.ones(shape = (self.init_num_ants), dtype= int)
        self.positions = None
        self.ants_move_y = np.zeros(shape = (1, self.init_num_ants), dtype= int)
        self.ants_move_x = np.zeros(shape = (1, self.init_num_ants), dtype= int)
        
        self.food_array = np.zeros(shape = (1, self.init_num_ants), dtype= int)

        self.ive_food = np.zeros(shape = (1, self.init_num_ants), dtype = bool)
        
    def init_ants(self):
        ant_list = []
        
        #TODO: replace 'for loop'. Use 'while loop' in place
        
        for _ in range(self.init_num_ants):
            ant_list.append(Ant(spawn_position = self.spawn_position, color = self.color))
        
        self.colony_ants = np.array(ant_list)

    
    def update_ants_positions(self, ymax: int, xmax: int, food_thresh: np.array = None) -> None:
        
        '''
            ymax: img.shape[0] - 1
            xmax: img.shape[1] - 1

            https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html            
            https://numpy.org/doc/stable/reference/generated/numpy.clip.html
        '''
        
        ymax -= 1
        xmax -= 1
        
        #RANDOM movements [-1, 0, 1]
        #Note: The 'high' param is exclusive
        random_x = np.random.randint(low = -1, high = 2, size = self.init_num_ants, dtype = int)
        random_y = np.random.randint(low = -1, high = 2, size = self.init_num_ants, dtype = int)
        
        planned_x = None
        planned_y = None
        
        self.ants_move_y = np.random.randint(low = -1, high = 2, size = self.init_num_ants, dtype = int)
        self.ants_move_x = np.random.randint(low = -1, high = 2, size = self.init_num_ants, dtype = int)
        
        #limit pos_y and pos_x values
        #boundary_thickness is important due to obstacle/food detection
        #We are considering that each ant can detect obstacles from 2 pixels alway
        boundary_thickness = 2
        
        self.ants_pos_y = np.clip( self.ants_pos_y + self.ants_move_y,
                                    a_min = boundary_thickness,
                                    a_max = ymax)
        
        self.ants_pos_x = np.clip( self.ants_pos_x + self.ants_move_x,
                                    a_min = boundary_thickness,
                                    a_max = xmax)
        
    #Alterar esse nome 
    def path_planner(self, food_thresh_img: np.ndarray):
        
        '''
                Each ant can detect 2 pixels in every direction. 
            We will construct matrices (5x5) like:
                                                    | 1 1 0 0 0 |
                                                    | 1 1 0 0 0 |
                                                Ft= | 0 0 x 0 0 |
                                                    | 0 0 0 0 0 |
                                                    | 0 0 0 1 1 |
            Where ones are food pixels, and 0 are empty pixels. 
            x is the ant position.

                The ant motion is based on food density in each direction.
                We will compute the (x_cg, y_cg) in each F matrix, i. e., 
                the center of mass position of food detected.  
        '''
        
        # We assume the initial CG as the center of the matrix
        food_xcg = 0
        food_ycg = 0
        
        #count the number of food pieces in each matrix F
        num_food_pixels = np.zeros(self.init_num_ants)

        for i in range(-2, 3):
            for j in range(-2, 3):
                
                #food_around_us example: [1 1 0 ... 0 0]
                food_around_us = food_thresh_img[self.ants_pos_y - j, self.ants_pos_x - i]/255
                num_food_pixels += food_around_us

                #Weighted arithmetic sum, where the weights are i and j
                food_xcg += i*food_around_us
                food_ycg += j*food_around_us        
        '''
            Compute x and y components of the vectors (ant -> food_cg) 
            to go from (2,2).
            (nao vale mais a afirmacao anterior)
            #*We have -15 <= food_ycg_max, food_xcg_max <= +15, as we can verify:

                                                    | 0 0 0 0 0 |
                                                    | 0 0 0 0 0 |
                                                Ft= | 0 0 x 0 0 | (ycg_max)
                                                    | 1 1 1 1 1 |
                                                    | 1 1 1 1 1 |

                                                    | 0 0 0 1 1 |
                                                    | 0 0 0 1 1 |
                                                Ft= | 0 0 x 1 1 | (xcg_max)
                                                    | 0 0 0 1 1 |
                                                    | 0 0 0 1 1 |
        '''

        #We sum 0.001 to denominator to avoid division by zero
        distances_x = food_xcg/(num_food_pixels + 0.001)
        distances_y = food_ycg/(num_food_pixels + 0.001)

        move_x = np.sign(distances_x)
        move_y = np.sign(distances_y)
        
        

    def i_have_food(self, do_you_have_food: np.array(bool)) -> None:
        
        '''
            #*Structured Arrays
            https://numpy.org/doc/stable/user/basics.rec.html
            food_pts: np.array([(y1, x1, (y2, x2), ...], dtype = [('y', np.uint8), ('x', np.uint8)])
            example: self.food_bool([True, True, False, ..]) means that ants 
            with indexes 0 and 1 have food, whereas ant 2 have not.
        
            Implement a method to verify if an ant is over the food or not
            https://numpy.org/doc/stable/reference/generated/numpy.in1d.html
        
        '''
        self.ive_food = do_you_have_food
        ...

    