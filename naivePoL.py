import numpy as np
import random
from matplotlib import pyplot as plt
import networkx as nx
#IMPORTANT: scipy must be at least version 1.8 otherwise it will throw an attribute error: 
# https://github.com/pyg-team/pytorch_geometric/issues/4378 

class Car():
    """class to create a car with a given position, range of sight and list of neighbors"""
    
    def __init__(self, position: list, velocity: list, range_of_sight: float, ID):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.position_history = []
        self.position_history.append(np.array(position))
        self.range_of_sight = range_of_sight

        self.neighbors = []
        self.ID = ID
        self.neighbor_validations = 0

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

    def add_neighbours(self, car):
        self.neighbors.append(car)
        return self.neighbors

    def is_car_a_neighbour(self, car):
        if car in self.neighbors:
            return True
        else:
            raise Exception("The car is not a neighbour!") 

    def claim_position(self):
            return self.ID, self.position

    def name_witness(self):
        #select two witnesses at random from list of neighbours
        if len(self.neighbors) > 1:
            self.witnesses = random.choices(self.neighbors, k = 2)
        else:
            raise Exception("The car does not have sufficient neighbours to witness its position!")
        return self.witnesses

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

#---------------------------- Calls -----------------------

Number_of_Cars= 500
cars = []

#initialising cars with a random position, velocity and range of sight
for car in range(Number_of_Cars):
    position = (np.random.rand(2)*2).tolist()
    velocity = ((np.random.rand(2)*2)-1).tolist()
    range_of_sight = round(random.uniform(0.1,0.2), 2)
    ID = str(car)
    cars.append(Car(position, velocity, range_of_sight, ID))

London = Environment([0,2], [0,2], 0.25)
#put all the cars into the Environment for the first time
for car in cars:
    London.assign(car)

#move each car, and put the car in its new corresponding cell in the environment
for car in cars:
    car.move(0.1, London.x_coordinates, London.y_coordinates)
    car.neighbors = []
    London.assign(car)
#print(London.grid)

#Once all cars have been moved: for every square in the grid, we go through each car
#That car must check all other cars in the square and if they are in range of sight
#add them to its list of neighbours
for square in London.grid:
    for set in square:
        for car_ in set:
            for nearby_car in set:
                if car_ != nearby_car: #make sure car does not add itself to the list of neighbours
                    car_.add_neighbours(nearby_car) #the size of neighbours is equal to the number of cars in that grid - 1


#-------------Aida Proof of Location Protocol-----------------
#A Car claims their position
#WARNING: CANNOT PICK 1ST CAR, that is in essence the genesis block so it will never have neighbours
DAG = nx.Graph()
threshold = 0.5
valid_nodes = []
for a_car in cars:

    test_car = a_car
    position_claim = test_car.claim_position()
    print('Car '+test_car.ID +' claims position:',position_claim)
    print('CAR range of sight is', test_car.range_of_sight)
    print('number of neighbours: ', len(test_car.neighbors))
    #Visualise(cars, London)  

    for neighbor in test_car.neighbors:
        #print('is the car a neighbour? ',neighbor.is_car_a_neighbour(test_car))
        #print('neighbor ID',neighbor.ID)
        #print('neighbour range of sight is', neighbor.range_of_sight)
        #print(neighbor.is_in_range_of_sight(test_car.position))

        if test_car.is_in_range_of_sight(neighbor.position):
            #print('test car validations', test_car.neighbor_validations)
            test_car.neighbor_validations += 1


    score = test_car.neighbor_validations/len(test_car.neighbors)
    print('score =', score)
    if score >= threshold:
        valid_nodes.append(test_car)

for any_Car in valid_nodes:
    for neighbour_of_CAR in any_Car.neighbors:
        if neighbour_of_CAR in valid_nodes:
            DAG.add_node(any_Car)
            DAG.add_node(neighbour_of_CAR)
            DAG.add_edge(any_Car, neighbour_of_CAR)

nx.draw(DAG)
plt.show()

print('no. of nodes: ',DAG.number_of_nodes())


