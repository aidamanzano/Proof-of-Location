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

#---------------------------- Calls -----------------------

Number_of_Cars= 500
cars = []

#initialising cars with a random position, velocity and range of sight
for car in range(Number_of_Cars):
    position = (np.random.rand(2)*2).tolist()
    velocity = ((np.random.rand(2)*2)-1).tolist()
    range_of_sight = round(random.uniform(0.1,0.2), 2)
    ID = str(car)
    honest = random.choice([True, False])
    cars.append(Car(position, velocity, range_of_sight, ID, honest))

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
            if car_.honest == False:
                car_.assign_fake_position()
                x_index = int(np.floor(car_.fake_position[0]/London.grid_size))
                y_index = int(np.floor(car_.fake_position[1]/London.grid_size))
                for alleged_nearby_car in London.grid[x_index][y_index]:
                    if car_ != alleged_nearby_car:
                        car_.add_neighbours(alleged_nearby_car)
                #go to fake position square
                #for nearby_car in fake position
                #add the neighbours
            for nearby_car in set:
                if car_ != nearby_car: #make sure car does not add itself to the list of neighbours
                    car_.add_neighbours(nearby_car) 

#TODO: if the car is lying, it must add neighbours from its fake position, not its real one!

#Visualise(cars, London)

#-----------------------------Aida Proof of Location Protocol---------------------------

DAG = nx.Graph()

True_Positive = 0
True_Negative = 0
False_Positive = 0
False_Negative = 0

for car in cars:
    test_car = car

    test_car.algorithm_honesty_output = True
    
    #A Car claims their position
    position_claim = test_car.claim_position()
    print('Car '+test_car.ID +' claims position:', position_claim)
    DAG.add_node(test_car, color = 'red')

    #Car 1 names two witnesses
    named_witnesses = test_car.name_witness()
    if named_witnesses == None:
        #test_car.algorithm_honesty_output = False
        pass

    else:
        print('Car'+test_car.ID+'names witnesses:', named_witnesses)

        #check that the witness named is not the car itself
        if named_witnesses[0] == test_car or named_witnesses[1] == test_car:
            print('car named itself as a witness')
            named_witnesses = test_car.name_witness()
            print('Car'+test_car.ID+'names new witnesses:', named_witnesses)

        #check that car doesn't select same witness twice
        if named_witnesses[0] == named_witnesses[1]:
            print('car is sharing witnesses')
            named_witnesses = test_car.name_witness()
            print('Car'+test_car.ID+'names new witnesses:', named_witnesses)

        # Two witnesses must attest to seeing Car 1: Car 1 must be a neighbour AND in range of sight
        for witness in named_witnesses:
            print('is witness a neighbour? ', witness.is_car_a_neighbour(test_car))
            print('witness ID',witness.ID)
            print(witness.is_in_range_of_sight(test_car.position))

            if witness.is_car_a_neighbour(test_car) == False or witness.is_in_range_of_sight(test_car.position) == False:
                test_car.algorithm_honesty_output = False
                print('witness is not neighbour of car OR witness is not in range of sight of car')
                
            else:
                DAG.add_node(witness, color = 'blue')

            DAG.add_edge(test_car, witness)

            # Witness 1 must name their attestors and Witness 2 must name their attestors
            witness_attestors = witness.name_witness()
            if witness_attestors == None:
                pass
            else:
                print('witness '+ str(witness.ID) + ' names attestors: ', witness_attestors[0].ID, witness_attestors[1].ID)

                #check that the witness named is not the car
                if witness_attestors[0] == test_car or witness_attestors[1] == test_car:
                    print('witness named car as an attestor')
                    witness_attestors = witness.name_witness()
                    print('witness '+ str(witness.ID) + ' names new attestors: ', witness_attestors[0].ID, witness_attestors[1].ID)

                #check that witness doesn't select same attestor twice
                if witness_attestors[0] == witness_attestors[1]:
                    print('witness is sharing attestors')
                    witness_attestors = witness.name_witness()
                    print('witness '+ str(witness.ID) + ' names new attestors: ', witness_attestors[0].ID, witness_attestors[1].ID)

                #check attestor 1 is not already a witness
                if witness_attestors[0] == named_witnesses[0] or witness_attestors[0] == named_witnesses[1]:
                    print('attestor 1 is the same as a witness')
                    witness_attestors = witness.name_witness()
                    print('witness '+ str(witness.ID) + ' names new attestors: ', witness_attestors[0].ID, witness_attestors[1].ID)

                #check attestor 2 is not already a witness
                if witness_attestors[1] == named_witnesses[0] or witness_attestors[1] == named_witnesses[1]:
                    print('attestor 2 is the same as witness')
                    witness_attestors = witness.name_witness()
                    print('witness '+ str(witness.ID) + ' names new attestors: ', witness_attestors[0].ID, witness_attestors[1].ID)

                # Attestors must be a neighbour AND be in range of sight of witness
                for attestor in witness_attestors:
                    print('is attestor a neighbour of the witness? ',attestor.is_car_a_neighbour(witness))
                    print('attestor ID',attestor.ID)
                    print(attestor.is_in_range_of_sight(witness.position))

                    if attestor.is_car_a_neighbour(witness) == False or attestor.is_in_range_of_sight(witness.position) == False:
                        test_car.algorithm_honesty_output = False
                        print('attestor is not a neighbour, OR attestor is not in range of sight of witness')

                    else:
                        DAG.add_node(attestor, color = 'green')
                        #test_car.algorithm_honesty_output = True

                    DAG.add_edge(witness, attestor)
        print('Is this car actually honest?: ' + str(test_car.honest) + ' Does the algorithm think this car is honest?: ' + str(test_car.algorithm_honesty_output))
        #If all True: attestors' positions get verified

    if test_car.honest and test_car.algorithm_honesty_output == True:
        True_Positive += 1
    if test_car.honest == True and test_car.algorithm_honesty_output == False:
        False_Negative += 1
    if test_car.honest == False and test_car.algorithm_honesty_output == True:
        False_Positive += 1
    if test_car.honest == False and test_car.algorithm_honesty_output == False:
        True_Negative += 1
    
    Accuracy = ((True_Positive + True_Negative) / (True_Positive + True_Negative + False_Positive + False_Negative)) * 100

    color_map = nx.get_node_attributes(DAG, 'color')

    #some code i copied from stack overflow to change the color of each node, 
    # probably will do this better later
    for key in color_map:
        if color_map[key] == 'green':
            color_map[key] = 'green'
        if color_map[key] == 'blue':
            color_map[key] = 'blue'
        if color_map[key] == 'red':
            color_map[key] = 'red'
        if color_map[key] == 'magenta':
            color_map[key] = 'magenta'
    car_colors = [color_map.get(node) for node in DAG.nodes()]

print('total accuracy = ' + str(Accuracy) + '%')
nx.draw(DAG, node_color=car_colors)
#print('no. of nodes: ',DAG.number_of_nodes())
#plt.show()  



