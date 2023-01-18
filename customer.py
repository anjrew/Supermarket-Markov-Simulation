import random

import numpy as np
from tiles_skeleton import TILE_SIZE


class Customer:
    """
    a single customer that moves through the supermarket
    in a MCMC simulation
    """
    def __init__(
            self, 
            name, 
            supermarket, 
            avatar_id, 
            row=0, 
            col=0, 
            initial_state='entrance', 
            avatar_colors = [[222,173, 173],[222,173,219], [194,173,222], [235, 231, 124], [246, 207,116], [246, 164, 116], [246, 129, 116]]
        ):
        """
        supermarket: A SuperMarketMap object
        avatar : a numpy array containing a 32x32 tile image
        row: the starting row
        col: the starting column
        """
    
        self.name = name
        self.state = initial_state
        
        ## Properties for animation
        self.supermarket = supermarket
        self.avatar = supermarket.get_tile(avatar_id) 
        self.avatar = self.__get_customer_color_avatar(self.avatar)
        self.row = row
        self.col = col

    
    def __repr__(self):
        return f'<Customer {self.name} in {self.state} {id(self)}>'


    def next_state(self, probs_dict):
        '''
        Propagates the customer to the next state.
        Returns nothing.
        '''
        
        probs_arr = {}
        
        for key in probs_dict.keys():
            probs_arr[key] = list(probs_dict[key].values())
           
        next_location_choices = list(probs_dict[self.state].keys())
                
        probability_weights = probs_arr[self.state]
                
        self.state = random.choices(next_location_choices, weights=probability_weights)[0]
        return self.state
    
      
    def draw(self, frame):

        y = self.row * TILE_SIZE
        x = self.col * TILE_SIZE

        one = y + self.avatar.shape[0]  # type: ignore
        two = x + self.avatar.shape[1]  # type: ignore

        frame[y:one, x:two] = self.avatar

        return frame
    
    
    def move(self, location):
        assert(type(location) is tuple)
        new_row = location[0]
        new_col = location[1]

        # if self.supermarket.contents[new_row][new_col] == '.':
        self.col = new_col
        self.row = new_row
        
        
    def __get_customer_color_avatar(self, avatar):
        color = np.random.choice(range(256), size=3)
        BLACK_FACIAL_FEATURES_TO_KEEP = [0,0,0]
        avatar = self.__replace_element(avatar, BLACK_FACIAL_FEATURES_TO_KEEP , color)
        return avatar
    
    
    def __replace_element(self, arr, keep_vector, replacer_vector):
        
        keep_vector = np.array(keep_vector)
        
        replacer_vector = np.array(replacer_vector)
        
        assert type(arr) is np.ndarray, "arr must be a np.array"
        
        for el in arr:
            
            if type(el) is np.ndarray and type(el[0]) is not np.uint8:
                                 
                el = self.__replace_element(el, keep_vector, replacer_vector)
                
            elif type(el) is np.ndarray and type(el[0]) is np.uint8:
                
                if (el != keep_vector).all():
                    
                    for i, _ in enumerate(el):
                        el[i] = replacer_vector[i]
                else:
                    el = el
            else:
                raise Exception('An element was found that was not a list or int')
        
        return arr