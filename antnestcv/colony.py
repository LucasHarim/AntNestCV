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

        self.name = name
        self.init_num_ants = init_num_ants
        self.spawn_position = spawn_position
        self.color = color

        self.ants_pos_y = self.spawn_position['y']*np.ones(shape = (self.init_num_ants), dtype= int)
        self.ants_pos_x = self.spawn_position['x']*np.ones(shape = (self.init_num_ants), dtype= int)
        self.positions = None
        self.ants_move_y = np.zeros(shape = (1, self.init_num_ants), dtype= int)
        self.ants_move_x = np.zeros(shape = (1, self.init_num_ants), dtype= int)
        
        self.food_array = np.zeros(shape = (1, self.init_num_ants), dtype= int)

        self.ive_food = np.zeros(shape = (1, self.init_num_ants), dtype = bool)
        
    def init_ants(self):
        ant_list = []
        
        for _ in range(self.init_num_ants):
            ant_list.append(Ant(spawn_position = self.spawn_position, color = self.color))
        
        self.colony_ants = np.array(ant_list)

    
    def update_ants_positions(self, ymax: int, xmax: int) -> None:
        

        '''
            ymax: img.shape[0] - 1
            xmax: img.shape[1] - 1

            https://numpy.org/doc/stable/reference/random/generated/numpy.random.randint.html            
            https://numpy.org/doc/stable/reference/generated/numpy.clip.html
        '''
        ymax -= 1
        xmax -= 1
        
        #RANDOM movements
        #Note: The 'high' param is exclusive
        self.ants_move_y = np.random.randint(low = -1, high = 2, size = self.init_num_ants, dtype = int)
        self.ants_move_x = np.random.randint(low = -1, high = 2, size = self.init_num_ants, dtype = int)
        
        #limit pos_y and pos_x values
        self.ants_pos_y = np.clip( self.ants_pos_y + self.ants_move_y, a_min = 0, a_max = ymax)
        self.ants_pos_x = np.clip( self.ants_pos_x + self.ants_move_x, a_min = 0, a_max = xmax)
        
        
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

