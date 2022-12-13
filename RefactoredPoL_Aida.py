import random
import numpy as np
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
        x_index, y_index = self.get_position_indicies(city.grid_size) #TODO: check if the indicies are correct: they are correct
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
            self.witnesses = random.sample(self.neighbours, 2)
            return self.witnesses
        else:
            print("The car does not have sufficient neighbours to witness its position!")
            return None
            #Even if a car has exactly one neighbour, I will ignore because it is not enough to proceed in the protocol.
            #do bla bla bla if witnesses != None else pass
        
    def move(self, dt, environment):
        x_index, y_index = self.get_position_indicies(environment.grid_size)
        #TODO: REMOVE the car from previous position
        environment.grid[x_index][y_index].remove(car)
        
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

        #TODO: Assign the car in its new position
        environment.assign(car)

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
        
        plt.scatter(x, y, marker="o", c = ['r' if car.honest is False else 'g'])     
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


Number_of_honest_cars= 300
Number_of_lying_cars = 100
cars = []

#initialising honest cars with a random position, velocity and range of sight
for car in range(Number_of_honest_cars):
    position = (np.random.rand(2)*2).tolist()
    velocity = ((np.random.rand(2)*2)-1).tolist()
    range_of_sight = 1000
    ID = str(car)
    cars.append(Car(position, velocity, range_of_sight, ID))

#initialising lying cars with a random position, velocity and range of sight
for liar_car in range(Number_of_lying_cars):
    position = (np.random.rand(2)*2).tolist()
    velocity = ((np.random.rand(2)*2)-1).tolist()
    #range_of_sight = round(random.uniform(0.1,0.2), 100)
    range_of_sight = 1000
    ID = str(liar_car)
    cars.append(lying_car(position, velocity, range_of_sight, ID))

#initialising the environment
London = Environment([0,2], [0,2], 0.25)

#put all the cars into the Environment for the first time


#Visualise(cars, London)

for car in cars:
    #put all the cars into the Environment for the first time
    London.assign(car)
    print(car.get_position_indicies(London.grid_size), car.position)


""" for car in cars:
    #Move all the honest cars' position in the environment
    if car.honest is True:
        car.move(0.1, London.x_coordinates, London.y_coordinates)

    else:
        #if the car is lying, we move its fake position
        car.move_fake_position(0.1, London.x_coordinates, London.y_coordinates)
        #car.move(0.1, London.x_coordinates, London.y_coordinates)
        # we also want to move its real position """
for car in cars:
    car.move(0.1, London)
    car.neighbours = set()
    print(car.get_position_indicies(London.grid_size), car.position)



for car in cars:
    car.add_neighbours(London)

        


#Visualise(cars, London)


#START OF AIDA POL protocol:
DAG = nx.Graph()

True_Positive = 0
True_Negative = 0
False_Positive = 0
False_Negative = 0

for car in cars:
#A Car claims their position
    position_claim = car.claim_position()
    print('Car '+ car.ID +' claims position:', position_claim)
    #DAG.add_node(car, color = 'red')

    #Car 1 names two witnesses
    named_witnesses = car.name_witness()

    if named_witnesses is None:
        car.algorithm_honesty_output = False
        pass
        

    else:
        print('Car'+ car.ID +'names witnesses:', named_witnesses[0].ID, named_witnesses[1].ID)
        
        #check that the witness named is not the car itself (superfluous anyway) # AND check that car doesn't select same witness twice
        tries = 5
        for trial in range(tries):
            named_witnesses = car.name_witness()    
            if (named_witnesses[0] != car and named_witnesses[1] != car) and (named_witnesses[0] != named_witnesses[1]):
                break

        # Two witnesses must attest to seeing Car 1: Car 1 must be a neighbour AND in range of sight
        for witness in named_witnesses:
            #print('is witness a neighbour? ', witness.is_car_a_neighbour(car))
            #print('witness ID',witness.ID)
            #print(witness.is_in_range_of_sight(car.position))

            if witness.is_car_a_neighbour(car) is False:
                car.algorithm_honesty_output = False
                print('car is not a neighbour of the witness')
                break
            elif witness.is_in_range_of_sight(car.position) is False:
                car.algorithm_honesty_output = False
                print('car is not in range of sight of witness')
                break
            else:
                DAG.add_node(witness, color = 'blue')
                car.algorithm_honesty_output = True

            DAG.add_edge(car, witness)
            

            # Witness 1 must name their attestors and Witness 2 must name their attestors
            witness_attestors = witness.name_witness()
            if witness_attestors is None:
                car.algorithm_honesty_output = False
                print('witness is not in range of sight of car')
                break
            else:
                print('witness '+ str(witness.ID) + ' names attestors: ', witness_attestors[0].ID, witness_attestors[1].ID)

                #check that the attestor named is not the car
                tries = 5
                for trial in range(tries):
                    witness_attestors = witness.name_witness()
                    if (witness_attestors[0] != car and witness_attestors[1] != car) and (witness_attestors[0] != witness_attestors[1]) and (witness_attestors[0] != named_witnesses[0] and witness_attestors[0] != named_witnesses[1]) and (witness_attestors[1] != named_witnesses[0] and witness_attestors[1] != named_witnesses[1]):
                        break


                #check that witness doesn't select same attestor twice
                

                #check attestor 1 is not already a witness
                

                #check attestor 2 is not already a witness
                

                # Attestors must be a neighbour AND be in range of sight of witness
                for attestor in witness_attestors:
                    #print('is attestor a neighbour of the witness? ',attestor.is_car_a_neighbour(witness))
                    #print('attestor ID',attestor.ID)
                    #print(attestor.is_in_range_of_sight(witness.position))

                    if attestor.is_car_a_neighbour(witness) is False:
                        car.algorithm_honesty_output = False
                        print('witness is not a neighbour of the attestor')
                        break
                    elif attestor.is_in_range_of_sight(witness.position) is False:
                        car.algorithm_honesty_output = False
                        print('witness position is not in range of sight of attestor')
                        break

                    else:
                        car.algorithm_honesty_output = True
                        DAG.add_node(attestor, color = 'green')
                        DAG.add_edge(witness, attestor)

    print('Is this car actually honest?: ' + str(car.honest) + ' Does the algorithm think this car is honest?: ' + str(car.algorithm_honesty_output))
    if car.honest is True and car.algorithm_honesty_output is True:
        True_Positive += 1
    if car.honest is True and car.algorithm_honesty_output is False:
        False_Negative += 1
    if car.honest is False and car.algorithm_honesty_output is True:
        False_Positive += 1
    if car.honest is False and car.algorithm_honesty_output is False:
        True_Negative += 1
    
    Accuracy = ((True_Positive + True_Negative) / (True_Positive + True_Negative + False_Positive + False_Negative)) * 100
print(Accuracy)