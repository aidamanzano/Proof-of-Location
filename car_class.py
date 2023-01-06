import random
import numpy as np

class Car():
    """class to create a car with a given position, range of sight and list of neighbours. Car is assumed to be honest"""
    def __init__(self, position: list, velocity: list, range_of_sight: float, ID, coerced):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.position_history = []
        self.position_history.append(np.array(position))
        self.range_of_sight = range_of_sight

        self.neighbours = set()
        self.ID = ID
        self.honest = True #is the car honest or a liar
        self.algorithm_honesty_output = None #does the algorithm dictate that this car is honest or a liar
        self.coerced = coerced

    @property
    def range_of_sight(self):
        return(self._range_of_sight)

    #The range of sight must be greater than 0
    @range_of_sight.setter
    def range_of_sight(self, value):
        if value <= 0:
            return ValueError("Your car must be able to see something")
        self._range_of_sight = value

    def is_in_range_of_sight(self, location):
        """This is a check to see if the position of a car that is being 'viewed' is within the range of sight of the viewing car.
        I assume the range of sight is a radius, and calculate if the position of the viewed car falls within the circle 
        of range of sight"""
        x = location[0]
        y = location[1]
        if (x - self.position[0])**2 + (y - self.position[1])**2 <= self.range_of_sight**2:
            return True
        else:
            return False

    def add_neighbours(self, city):
        """Find the grid quadrant of the car. Then, for every other neighbouring car in that quadrant, if it is in the range of sight 
        and not the car itself, add it to the set of neighbours"""
        x_index, y_index = self.get_position_indicies(city.grid_size)
        #coerced will chose to add a lying car it does NOT see in the fake position grid
        if self.coerced is True:
            for car in city.grid[x_index][y_index]:
                if car.honest is False and self.ID != car.ID:
                    self.neighbours.add(car)

        for car in city.grid[x_index][y_index]:
            #if neighbouring car is a lying car, the honest car would not see it, because it is in a fake position

            #for an honest car we only add neighbours that are within the range of sight of its position
            if self.is_in_range_of_sight(car.position) and car.ID != self.ID:
                self.neighbours.add(car)

        return self.neighbours

    def is_car_a_neighbour(self, car):
        if car in self.neighbours:
            return True
        else:
            #print("The car is not a neighbour!")
            return False

    def claim_position(self):
        return self.ID, self.position

    def name_witness(self):
        """Function to return two witnesses (or attestors), provided the car has sufficient neighbours"""
        if len(self.neighbours) >= 2:
            #select two witnesses at random from list of neighbours
            self.witnesses = random.sample(self.neighbours, 2)
            return self.witnesses
        else:
            #print("The car does not have sufficient neighbours to witness its position!")
            return None
            #Even if a car has exactly one neighbour, I will ignore because it is not enough to proceed in the protocol.
        
    def move(self, dt, environment):
        """First removes the car from its current grid position, then checks that the next position is within bounds of the environment
        and then updates position if so. Finally, adds the car into the new position grid"""
        
        #Find the indicies of the car position
        x_index, y_index = self.get_position_indicies(environment.grid_size)
        #REMOVE the car from previous position
        environment.grid[x_index][y_index].remove(self) #TODO: check self
        
        preliminary_position = self.position + (dt * self.velocity) 
        #if the agent is getting close to the grid boundaries, invert the velocity
        #I am assuming no car would voluntarily drive towards a wall

        if preliminary_position[0] <= environment.x_coordinates[0] or preliminary_position[0] >= environment.x_coordinates[1]:
            
            self.velocity[0] = -1 * self.velocity[0]
            preliminary_position = self.position + (dt * self.velocity)
            
        if preliminary_position[1] <= environment.y_coordinates[0] or preliminary_position[1] >= environment.y_coordinates[1]:
            self.velocity[1] = -1 * self.velocity[1]
            preliminary_position = self.position + (dt * self.velocity)
        
        self.position = preliminary_position
        self.position_history.append(self.position)

        #Assign the car in its new position
        environment.assign(self) #TODO: check self

    def get_position_indicies(self, grid_size):
        """Calculating the grid indicies given a position"""
        x_index = int(np.floor(self.position[0]/grid_size))
        y_index = int(np.floor(self.position[1]/grid_size))
        return x_index, y_index

class lying_car(Car):
    """Class for dishonest cars. Position claim, move function, position indicies and neighbour adding functions are added to 
    consider the fake position."""

    def __init__(self, position: list, velocity: list, range_of_sight: float, ID, coerced):
        super().__init__(position, velocity, range_of_sight, ID, coerced)
        self.fake_position = (np.random.rand(2)*2).tolist()
        self.honest = False

    def claim_position(self):
        #print('this car is a lying car', ' its real position is: ', self.position, ' its fake position is: ', self.fake_position)
        return self.ID, self.fake_position

    def move_fake_position(self, dt, environment):
        """When the lying car moves, it moves it's fake position, the real position may or may not have changed"""

        #Find the indicies of the car's fake position
        x_index, y_index = self.get_fake_position_indicies(environment.grid_size)
        #REMOVE the car from previous position
        environment.grid[x_index][y_index].remove(self) #TODO: check self

        preliminary_position = self.fake_position + (dt * self.velocity) 

        if preliminary_position[0] <= environment.x_coordinates[0] or preliminary_position[0] >= environment.x_coordinates[1]:
            
            self.velocity[0] = -1 * self.velocity[0]
            preliminary_position = self.fake_position + (dt * self.velocity)
            
        if preliminary_position[1] <= environment.y_coordinates[0] or preliminary_position[1] >= environment.y_coordinates[1]:
            self.velocity[1] = -1 * self.velocity[1]
            preliminary_position = self.fake_position + (dt * self.velocity)
        
        self.fake_position = preliminary_position
        self.position_history.append(self.fake_position)

        #add car to its new fake position in the grid
        environment.assign(self) #TODO: check self

    def get_fake_position_indicies(self, grid_size):
        x_index = int(np.floor(self.fake_position[0]/grid_size))
        y_index = int(np.floor(self.fake_position[1]/grid_size))
        return x_index, y_index

    def add_neighbours(self, city):
        #get the indicies of the fake location
        x_index, y_index = self.get_fake_position_indicies(city.grid_size)

        for alleged_nearby_car in city.grid[x_index][y_index]:
            #for an lying car we add neighbours w.r.t the fake position, provided they are in range of sight
            if self.is_in_range_of_sight(alleged_nearby_car.position) and alleged_nearby_car.ID != self.ID:
                self.neighbours.add(alleged_nearby_car)
        return self.neighbours

