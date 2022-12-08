import numpy as np
import random
from matplotlib import pyplot as plt
import networkx as nx
#IMPORTANT: scipy must be at least version 1.8 otherwise it will throw an attribute error: 
# https://github.com/pyg-team/pytorch_geometric/issues/4378 

class Car():
    """class to create a car with a given position, range of sight and list of neighbours. Car is assumed to be honest"""
    
    def __init__(self, position: list, velocity: list, range_of_sight: float, ID):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.position_history = []
        self.position_history.append(np.array(position))
        self.range_of_sight = range_of_sight

        self.neighbours = set()
        self.ID = ID
        self.honest = True #is the car honest or a liar
        self.algorithm_honesty_output = None #does the algorithm dictate that this car is honest or a liar

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
        x_index, y_index = self.get_position_indicies(city.grid_size)
        for car in city.grid[x_index][y_index]:
        #for an honest car we only add neighbours that are within the range of sight of its position
            if self.is_in_range_of_sight(car.position) and car.ID != self.ID:
                self.neighbours.add(car)
        return self.neighbours

    def is_car_a_neighbour(self, car):
        if car in self.neighbours:
            return True
        else:
            print("The car is not a neighbour!")
            return False

    def claim_position(self):
        return self.ID, self.position

    def name_witness(self):
        #select two witnesses at random from list of neighbours
        if len(self.neighbours) >= 2:
            self.witnesses = random.choices(self.neighbours, k = 2)
            return self.witnesses
        else:
            print("The car does not have sufficient neighbours to witness its position!")
            return None
            #Even if a car has exactly one neighbour, I will ignore because it is not enough to proceed in the protocol.
            #do bla bla bla if witnesses != None else pass
        
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

    def get_position_indicies(self, grid_size):
        x_index = int(np.floor(self.position[0]/grid_size))
        y_index = int(np.floor(self.position[1]/grid_size))
        return x_index, y_index

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

        x_index, y_index = car.get_position_indicies(self.grid_size)
        self.grid[x_index][y_index].add(car)

def Visualise(cars, environment):
    for car in cars:
        x = car.position[0]
        y = car.position[1]

        plt.xlim(environment.x_coordinates[0], environment.x_coordinates[1])
        plt.ylim(environment.y_coordinates[0], environment.y_coordinates[1])
        
        plt.plot(x, y, marker="o", markersize=10, markerfacecolor="magenta")
        
    plt.grid()
    plt.show()


class lying_car(Car):
    def __init__(self, position: list, velocity: list, range_of_sight: float, ID):
        super().__init__(position, velocity, range_of_sight, ID)
        self.fake_position = (np.random.rand(2)*2).tolist()
        self.honest = False

    def claim_position(self):
        print('this car is a lying car', ' its real position is: ', self.position, ' its fake position is: ', self.fake_position)
        return self.ID, self.fake_position

    def move_fake_position(self, dt, environment_Xcoordinates, environment_Ycoordinates):
        #When the lying car moves, it moves it's fake position, the real position may or may not have changed
        #TODO: is this bad?
        preliminary_position = self.fake_position + (dt * self.velocity) 

        if preliminary_position[0] <= environment_Xcoordinates[0] or preliminary_position[0] >= environment_Xcoordinates[1]:
            
            self.velocity[0] = -1 * self.velocity[0]
            preliminary_position = self.fake_position + (dt * self.velocity)
            
        if preliminary_position[1] <= environment_Ycoordinates[0] or preliminary_position[1] >= environment_Ycoordinates[1]:
            self.velocity[1] = -1 * self.velocity[1]
            preliminary_position = self.fake_position + (dt * self.velocity)
        
        self.fake_position = preliminary_position
        self.position_history.append(self.fake_position)

    def get_fake_position_indicies(self, grid_size):
        x_index = int(np.floor(self.fake_position[0]/grid_size))
        y_index = int(np.floor(self.fake_position[1]/grid_size))
        return x_index, y_index

    def add_neighbours(self, city):
        #get the indicies of the fake location
        x_index, y_index = self.get_fake_position_indicies(city.grid_size)
        for alleged_nearby_car in city.grid[x_index][y_index]:
        #for an lying car we add neighbours w.r.t the fake position, even if they are not in range of sight
            if alleged_nearby_car.ID != self.ID:
                self.neighbours.add(alleged_nearby_car)
        return self.neighbours


Number_of_honest_cars= 10
Number_of_lying_cars = 2
cars = []

#initialising honest cars with a random position, velocity and range of sight
for car in range(Number_of_honest_cars):
    position = (np.random.rand(2)*2).tolist()
    velocity = ((np.random.rand(2)*2)-1).tolist()
    range_of_sight = round(random.uniform(0.1,0.2), 2)
    ID = str(car)
    cars.append(Car(position, velocity, range_of_sight, ID))

#initialising lying cars with a random position, velocity and range of sight
for liar_car in range(Number_of_lying_cars):
    position = (np.random.rand(2)*2).tolist()
    velocity = ((np.random.rand(2)*2)-1).tolist()
    range_of_sight = round(random.uniform(0.1,0.2), 2)
    ID = str(liar_car)
    cars.append(lying_car(position, velocity, range_of_sight, ID))

#initialising the environment
London = Environment([0,2], [0,2], 0.25)

#put all the cars into the Environment for the first time
for car in cars:
    London.assign(car)

Visualise(cars, London)
#Move all the cars in the environment
for car in cars:
    if car.honest == True:
        car.move(0.1, London.x_coordinates, London.y_coordinates)
    else:
        car.move_fake_position(0.1, London.x_coordinates, London.y_coordinates)
    London.assign(car)

Visualise(cars, London)

for car in cars:
    car.add_neighbours(London)
    print(car.neighbours)

