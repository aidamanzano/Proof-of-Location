import numpy as np
import random

class Car():
    """class to create a car with a given position, range of sight and list of neighbors"""
    
    def __init__(self, position: list, velocity: list, range_of_sight: float, ID):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.position_history = []
        self.position_history.append(np.array(position))
        self.range_of_sight = range_of_sight

        self.x = position[0]
        self.y = position[1]

        self.vx = velocity[0]
        self.vy = velocity[1]

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
    

    def is_newCar_in_range_of_sight(self, location):
        """This is a check to see if the position of a car that is being 'viewed' is within the range of sight of the viewing car.
        I assume the range of sight is a radius, and calculate if the position of the viewed car falls within the circle 
        of range of sight"""
        x = location[0]
        y = location[1]
        if (x - self.position[0])**2 + (y - self.position[1])**2 <= self.range_of_sight**2:
            return True
        else:
            return False

    #TODO: have to update the list of neighbours in the move function ever time the car moves to a new grid
    def add_neighbour(self, car):
        if self.is_newCar_in_range_of_sight(car.position):
            self.neighbors.append(car)
        else:
            raise Exception("The car is not in range of sight, therefore it cannot be a neighbour")

    def is_car_a_neighbour(self, car):
        if car in self.neighbors:
            return True
        else:
            raise Exception("The car is not in the set!") 

    def move(self, dt, environment_Xcoordinate, environment_Ycoordinate):
        
        preliminary_position = self.position + (dt * self.velocity) 
        print('prelim',preliminary_position, environment_Xcoordinate[0], environment_Xcoordinate[1])
        #if the agent is getting close to the grid boundaries, invert the velocity
        #I am assuming no car would voluntarily drive towards a wall

        while preliminary_position[0] <= environment_Xcoordinate[0] or preliminary_position[0] >= environment_Xcoordinate[1]:
            self.velocity[0] = -1 * self.velocity[0]
            preliminary_position = self.position + (dt * self.velocity)
            
        while preliminary_position[1] <= environment_Ycoordinate[0] or preliminary_position[1] >= environment_Ycoordinate[1]:
            self.velocity[1] = -1 * self.velocity[1]
            preliminary_position = self.position + (dt * self.velocity)
        
        self.position = preliminary_position
        print('final position',self.position)
        self.position_history.append(self.position)
        

class Environment:
    #Pietro's environment definition funct.
    def __init__(self, x_coordinates:list, y_coordinates:list, grid_size):

        self.x_coordinates = x_coordinates
        self.y_coordinates = y_coordinates
        self.grid_size = grid_size

        self.width = int(self.x_coordinates[1]-self.x_coordinates[0]/self.grid_size)       
        self.height = int(self.y_coordinates[1]-self.y_coordinates[0]/self.grid_size)
        self.grid = [[set() for i in range(self.width)] for j in range(self.height)]
        
        #TODO 
        #every time there is a car move, check the positions of each

    def assign(self, car, dt):
        
        x_index = int(np.floor(car.position[0]))
        y_index = int(np.floor(car.position[1]))
        self.grid[x_index][y_index].add(car.ID)
        #print('old grid', self.grid)
        if dt > 0:
            
            self.grid[x_index][y_index].remove(car.ID)
            car.move(dt, self.x_coordinates, self.y_coordinates)

        new_x = int(np.floor(car.position[0]))
        new_y = int(np.floor(car.position[1]))
        
        self.grid[new_x][new_y].add(car.ID)
        #print('new grid', self.grid)

class Protocol(Car):
    def __init__(self, position: list, velocity: list, range_of_sight: float, ID):
        super().__init__(position, velocity, range_of_sight, ID)

    def claim_position(self):
        return self.ID, self.position

    def name_witness(self):
        #select two witnesses at random from list of neighbours
        self.witnesses = random.choices(self.neighbors, k = 2)
        return self.witnesses

Number_of_Cars= 5
cars = []
for car in range(Number_of_Cars):
    position = random.sample(range(0, 6), 2)
    velocity = random.sample(range(-1, 1), 2)
    range_of_sight = random.randint(1, 2)
    ID = str(car)
    cars.append(Car(position, velocity, range_of_sight, ID))

London = Environment([0,6], [0,6], 1)
print(London.grid)

for car in cars:
    London.assign(car, 0.1)

print('initialised grid', London.grid)




