import random

class SuperMarket:
    
    def __init__(self, name, transition_matrix, map, sections):
        self.name = name
        self.map = map
        
        assert name != None, 'The name should have a value'
        assert transition_matrix is not None, 'There should be a transition_matrix on construction'
        assert sections != None, 'There should be a section on construction'
        
        self.customers = []
        self.total_visits = 0
        
        self.transition_matrix = transition_matrix
        self.sections = sections
        
        self.probs_dict = transition_matrix.to_dict(orient='index')
        self.probs_arr = {}
        
        for key in self.probs_dict.keys():
            self.probs_arr[key] = list(self.probs_dict[key].values())
            
    
    def __repr__(self):
        return f'<SuperMarket {self.name}>'
    
    
    def add_customers(self, new_customers: list):
        self.total_visits += 1
        self.customers = [*self.customers, *new_customers]
        
        
    def remove_customers(self, customer_arr):
        for customer in customer_arr:
            self.customers.remove(customer)
    
    def get_customer_count(self):
        return len(self.customers)
    
    def get_total_customer_count(self):
        return self.total_visits
        
    def tick_minute(self):
        current_status = [ ]
        
        for customer in self.customers:
            
            new_customer_state = customer.next_state(self.probs_dict)
            
            new_customer_location = customer.move(self.sections.get_location_from_state(new_customer_state))
            
            if new_customer_state == 'exit':
                # print('Removing customer with state', new_customer_state)
                self.remove_customers([customer])
                
            current_status = [*current_status, { 'id': customer.name, 'state': new_customer_state, 'location': new_customer_location }]
                
        return current_status
    
    
    def draw(self, frame):
        frame = self.map.draw(frame)

        frame = self.draw_customers(frame)
        
        return frame
    
    
    def draw_customers(self, frame):
        """Draws customers onto the frame and returns a new frame"""
        
        for customer in self.customers:
            
            frame = customer.draw(frame)
                
        return frame
   
    
class Sections(dict):
    
    def __init__(self, dairy, drinks, spices, fruit, checkout, exit, entrance):
        super(Sections, self).__init__(dairy=dairy, drinks=drinks,spices=spices, fruit=fruit, checkout=checkout, exit=exit, entrance=entrance)
        
        assert type(dairy) is list
        assert type(checkout) is list
        assert type(drinks) is list
        assert type(spices) is list
        assert type(fruit) is list
        assert type(exit) is list
        
        self.dairy = dairy
        self.drinks = drinks
        self.spices = spices
        self.fruit = fruit
        self.checkout = checkout
        self.exit = exit
        self.entrance = entrance
        
    def get_location_from_state(self, state):
        """Returns the x,y coordinates of the current state from the list of locations associated with a state"""
        choices = self.__dict__[state]
        return random.choice(choices)