import numpy as np
import random
import networkx as nx
from matplotlib import pyplot as plt

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
        if self.is_in_range_of_sight(car.position):
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

    def move(self, dt, environment_Xcoordinate, environment_Ycoordinate):
        
        preliminary_position = self.position + (dt * self.velocity) 
        #if the agent is getting close to the grid boundaries, invert the velocity
        #I am assuming no car would voluntarily drive towards a wall

        if preliminary_position[0] <= environment_Xcoordinate[0] or preliminary_position[0] >= environment_Xcoordinate[1]:
            
            self.velocity[0] = -1 * self.velocity[0]
            preliminary_position = self.position + (dt * self.velocity)
            
        if preliminary_position[1] <= environment_Ycoordinate[0] or preliminary_position[1] >= environment_Ycoordinate[1]:
            self.velocity[1] = -1 * self.velocity[1]
            preliminary_position = self.position + (dt * self.velocity)
        
        self.position = preliminary_position
        self.position_history.append(self.position)
        
        #TODO: have to update the list of neighbours in the move function ever time the car moves to a new grid
        

class Environment:
    #Pietro's environment definition funct.
    def __init__(self, x_coordinates:list, y_coordinates:list, grid_size):

        self.x_coordinates = x_coordinates
        self.y_coordinates = y_coordinates
        self.grid_size = grid_size

        self.width = int((self.x_coordinates[1]-self.x_coordinates[0])/self.grid_size)
     
        self.height = int((self.y_coordinates[1]-self.y_coordinates[0])/self.grid_size)
        self.grid = [[set() for i in range(self.width)] for j in range(self.height)]


    def assign(self, car, dt):

        print(car)
        
        x_index = int(np.floor(car.position[0]/self.grid_size))
        y_index = int(np.floor(car.position[1]/self.grid_size))

        if self.grid[x_index][y_index] != True:
            self.grid[x_index][y_index].add(car)
        #print('position', car.position, 'x index', x_index, 'y index', y_index)

        if dt > 0:
            self.grid[x_index][y_index].remove(car)
            car.move(dt, self.x_coordinates, self.y_coordinates)
            car.neighbors = []
            for nearby_car in self.grid[x_index][y_index]: #neighbour here is a class instance of the car, so we can access its position in the is_neighbour function
                car.add_neighbours(nearby_car) #add_neighbours function calls is_in_range_of_sight function, and only appends if True
                #add neighbours after the moving.
        new_x = int(np.floor(car.position[0]/self.grid_size))
        new_y = int(np.floor(car.position[1]/self.grid_size))
        
        self.grid[new_x][new_y].add(car)
        

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
    range_of_sight = 20
    ID = str(car)
    cars.append(Car(position, velocity, range_of_sight, ID))

London = Environment([0,2], [0,2], 0.25)

for tester in cars:
    London.assign(tester, 0.1)
    #print(tester.ID, tester.neighbors)
    

#print('Grid', London.grid)

#-------------Aida Proof of Location Protocol-----------------
#A Car claims their position
#WARNING: CANNOT PICK 1ST CAR, that is in essence the genesis block so it will never have neighbours
Car_301 = cars[301]

position_claim = Car_301.claim_position()
print('Car '+Car_301.ID +' claims position:',position_claim)
Visualise(cars, London)

#Car 1 names two witnesses
named_witnesses = Car_301.name_witness()
print('Car'+Car_301.ID+'names witnesses:', named_witnesses)

# Two witnesses must attest to seeing Car 1: Car 1 must be a neighbour AND in range of sight
for witness in named_witnesses:
    #witness.is_car_a_neighbour(Car_301)
    print(witness.is_in_range_of_sight(Car_301.position))

# If previous is True: 

# Witness 1 must name their attestors and Witness 2 must name their attestors

# Attestors must be a neighbour AND be in range of sight of witness

#If all True: Car 1 can submit position.

#TODO make a graph for the positions that get approved. 
#G = nx.Graph()
#G.add_nodes_from(cars)
#G.add_nodes_from(cars)
#for node in G.nodes:
    #print('node position', node.position)
    #if node.is_in_range_of_sight( location)
#nx.draw(G)
#plt.show()  