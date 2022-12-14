import random
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
#IMPORTANT: scipy must be at least version 1.8 otherwise it will throw an attribute error: 
# https://github.com/pyg-team/pytorch_geometric/issues/4378 

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
            print("The car is not a neighbour!")
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
            print("The car does not have sufficient neighbours to witness its position!")
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
    """Visualising cars in the environment, if they are honest they are shown in green, otherwise shown in red"""
    for car in cars:
        x = car.position[0]
        y = car.position[1]

        plt.xlim(environment.x_coordinates[0], environment.x_coordinates[1])
        plt.ylim(environment.y_coordinates[0], environment.y_coordinates[1])
        #TODO: trying to show coerced cars in another colour as well
        plt.scatter(x, y, marker="o", c = ['r' if car.honest is False else 'g'])     
    plt.grid()
    plt.show()

class lying_car(Car):
    """Class for dishonest cars. Position claim, move function, position indicies and neighbour adding functions are added to 
    consider the fake position."""

    def __init__(self, position: list, velocity: list, range_of_sight: float, ID, coerced):
        super().__init__(position, velocity, range_of_sight, ID, coerced)
        self.fake_position = (np.random.rand(2)*2).tolist()
        self.honest = False

    def claim_position(self):
        print('this car is a lying car', ' its real position is: ', self.position, ' its fake position is: ', self.fake_position)
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

#---------------------START OF AIDA POL protocol----------------------:
def PoL(cars):
    DAG = nx.Graph()

    True_Positive = 0
    True_Negative = 0
    False_Positive = 0
    False_Negative = 0


    for car in cars:
    #A Car claims their position
        position_claim = car.claim_position()
        print('Car '+ car.ID +' claims position:', position_claim)
        

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

            #TODO: add the red car to the graph only if the witnesses tests pass
            DAG.add_node(car, color = 'red')

            # Two witnesses must attest to seeing Car 1: Car 1 must be a neighbour AND in range of sight
            for witness in named_witnesses:
                
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

                    #check that neither of the attestors named is the car AND
                    #check that witness doesn't select same attestor twice AND
                    #check attestor 1 is not already a witness AND
                    #check attestor 2 is not already a witness
                    tries = 5
                    for trial in range(tries):
                        witness_attestors = witness.name_witness()
                        if (witness_attestors[0] != car and witness_attestors[1] != car) and (witness_attestors[0] != witness_attestors[1]) and (witness_attestors[0] != named_witnesses[0] and witness_attestors[0] != named_witnesses[1]) and (witness_attestors[1] != named_witnesses[0] and witness_attestors[1] != named_witnesses[1]):
                            break                

                    # Attestors must be a neighbour AND be in range of sight of witness
                    for attestor in witness_attestors:
                        #TODO: check car is in range of sight of attestor

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
            
        car_colors = [color_map.get(node) for node in DAG.nodes()]
    nx.draw(DAG, node_color=car_colors)
    #print(Accuracy)
    #print(True_Negative, True_Positive, False_Negative, False_Positive)
    plt.show()
    return Accuracy, DAG

#TODO: plots of accuracy vs percentage of lying cars and coerced cars
#over varying N of total cars and car density per network.

def honest_cars_init(N_honest_cars:int, car_list:list):
#initialising honest cars with a random position, velocity and range of sight
    for car in range(N_honest_cars):
        position = (np.random.rand(2)*2).tolist()
        velocity = ((np.random.rand(2)*2)-1).tolist()
        range_of_sight = 1000
        ID = str(car)
        coerced = False
        car_list.append(Car(position, velocity, range_of_sight, ID, coerced))
    return car_list

def coerced_cars_init(N_coerced_cars:int, car_list:list):
#initialising coerced cars with a random position, velocity and range of sight
    for car in range(N_coerced_cars):
        position = (np.random.rand(2)*2).tolist()
        velocity = ((np.random.rand(2)*2)-1).tolist()
        range_of_sight = 1000
        ID = str(car)
        coerced = True
        car_list.append(Car(position, velocity, range_of_sight, ID, coerced))
    return car_list

def lying_cars_init(N_lying_cars:int, car_list:list):
#initialising lying cars with a random position, velocity and range of sight
    for liar_car in range(N_lying_cars):
        position = (np.random.rand(2)*2).tolist()
        velocity = ((np.random.rand(2)*2)-1).tolist()
        #range_of_sight = round(random.uniform(0.1,0.2), 100)
        range_of_sight = 1000
        ID = str(liar_car)
        coerced = False
        car_list.append(lying_car(position, velocity, range_of_sight, ID, coerced))
    return car_list

#--------------------------------
Number_of_honest_cars= 700
Number_of_lying_cars = 100
Number_of_coerced_cars = 200
cars = []

cars = honest_cars_init(Number_of_honest_cars, cars)
cars = coerced_cars_init(Number_of_coerced_cars, cars)
cars = lying_cars_init(Number_of_lying_cars, cars)

#initialising the environment
London = Environment([0,2], [0,2], 0.25)

#Visualise(cars, London)
def environment_update(car_list, dt, environment):
    for car in car_list:
        #put all the cars into the Environment for the first time
        environment.assign(car)
        
    for car in car_list:
        if car.honest is True:
            car.move(dt, environment)
        else:
            car.move_fake_position
        car.neighbours = set()
        
    for car in car_list:
        car.add_neighbours(environment) 

#environment_update(cars, 0.1, London)
#Accuracy, DAG = PoL(cars)
#Visualise(cars, London)

number_of_simulations = 10
fig = plt.figure()
plt.title('Monte Carlo Simulations of Proof of Location Protocol, Number of Simulations = ' + str(number_of_simulations))
plt.xlabel('simulation number')
plt.ylabel('Accuracy')
plt.xlim([0, number_of_simulations])

simulation_no = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Accuracies = []
for simulation in range(number_of_simulations):
    
    percent_of_coerced_cars = []
    environment_update(cars, 0.1, London)
    simulation_Accuracy, DAG = PoL(cars)
    x = ((Number_of_coerced_cars) / (Number_of_honest_cars + Number_of_coerced_cars + Number_of_lying_cars)) * 100
    percent_of_coerced_cars.append(x)
    Accuracies.append(simulation_Accuracy)
plt.bar(simulation_no, Accuracies)
plt.show()




#TODO: cluster of lying cars can attack the system
#TODO: time varying component: showing how the graph varies over time

#TODO: add entropy measure to the proof of position ??