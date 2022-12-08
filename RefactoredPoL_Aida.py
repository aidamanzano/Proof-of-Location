import numpy as np
import random
from matplotlib import pyplot as plt
import networkx as nx
#IMPORTANT: scipy must be at least version 1.8 otherwise it will throw an attribute error: 
# https://github.com/pyg-team/pytorch_geometric/issues/4378 

class Car():
    """class to create a car with a given position, range of sight and list of neighbors. Car is assumed to be honest"""
    
    def __init__(self, position: list, velocity: list, range_of_sight: float, ID, honest: True):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.position_history = []
        self.position_history.append(np.array(position))
        self.range_of_sight = range_of_sight

        self.neighbors = []
        self.ID = ID
        self.honest = honest #is the car honest or a liar
        self.algorithm_honesty_output = None #does the algorithm dictate that this car is honest or a liar
        self.fake_position = None

    @property
    def range_of_sight(self):
        return(self._range_of_sight)

    #The range of sight must be greater than 0
    @range_of_sight.setter
    def range_of_sight(self, value):
        if value <= 0:
            return ValueError("Your car must be able to see something")
        self._range_of_sight = value
    
    #if the car is malicious, we assign it a fake position
    def assign_fake_position(self):
        if self.honest == False:
            self.fake_position = (np.random.rand(2)*2).tolist()
            return self.fake_position

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

    def add_neighbours(self, car):
        if self.is_in_range_of_sight(car.position):
            self.neighbors.append(car)
        return self.neighbors

    def is_car_a_neighbour(self, car):
        if car in self.neighbors:
            return True
        else:
            print("The car is not a neighbour!")
            return False

    def claim_position(self):
        if self.honest == False:
            print('this car is a lying car', ' its real position is: ', self.position, ' its fake position is: ', self.fake_position)
            return self.ID, self.fake_position
        else:
            return self.ID, self.position

    def name_witness(self):
        #select two witnesses at random from list of neighbours
        #TODO: if the car is lying, it must name neighbours from its fake position, not its real one!
        if len(self.neighbors) >= 2:
            self.witnesses = random.choices(self.neighbors, k = 2)
            return self.witnesses
        else:
            #self.witnesses = self.neighbors
            print("The car does not have sufficient neighbours to witness its position!")
            return None
        
    def move(self, dt, environment_Xcoordinates, environment_Ycoordinates):
        
        preliminary_position = self.position + (dt * self.velocity) 
        #if the agent is getting close to the grid boundaries, invert the velocity
        #I am assuming no car would voluntarily drive towards a wall

        if preliminary_position[0] <= environment_Xcoordinates[0] or preliminary_position[0] >= environment_Xcoordinates[1]:
            
            self.velocity[0] = -1 * self.velocity[0]
            preliminary_position = self.position + (dt * self.velocity)
            
        if preliminary_position[1] <= environment_Ycoordinates[0] or preliminary_position[1] >= environment_Ycoordinates[1]:
            self.velocity[1] = -1 * self.velocity[1]
            preliminary_position = self.position + (dt * self.velocity)
        
        self.position = preliminary_position
        self.position_history.append(self.position)
        

class Environment:
    #Pietro's environment definition funct.
    def __init__(self, x_coordinates:list, y_coordinates:list, grid_size):

        self.x_coordinates = x_coordinates
        self.y_coordinates = y_coordinates
        self.grid_size = grid_size

        self.width = int((self.x_coordinates[1]-self.x_coordinates[0])/self.grid_size)
        self.height = int((self.y_coordinates[1]-self.y_coordinates[0])/self.grid_size)
        self.grid = [[set() for i in range(self.width)] for j in range(self.height)]


    def assign(self, car):

        x_index = int(np.floor(car.position[0]/self.grid_size))
        y_index = int(np.floor(car.position[1]/self.grid_size))

        self.grid[x_index][y_index].add(car)
        #print('position', car.position, 'x index', x_index, 'y index', y_index)
        

def Visualise(cars, environment):
    for car in cars:
        x = car.position[0]
        y = car.position[1]

        plt.xlim(environment.x_coordinates[0], environment.x_coordinates[1])
        plt.ylim(environment.y_coordinates[0], environment.y_coordinates[1])
        
        plt.plot(x, y, marker="o", markersize=10, markerfacecolor="magenta")
        
    plt.grid()
    plt.show()
