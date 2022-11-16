import numpy as np

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
        #self.position = max(self.position  + (dt * self.velocity), 0)
        self.position = self.position + (dt * self.velocity)
        print('first position update',self.position)
        self.position_history.append(self.position)

        #if the agent is getting close to the grid boundaries, invert the velocity
        #I am assuming no car would voluntarily drive towards a wall
        if self.position[0] - self.range_of_sight <= environment_Xcoordinate[0] or self.position[0] + self.range_of_sight >= environment_Xcoordinate[1]: #pass the x and y coordinate of the environment
            self.vx = -1 * self.vx 
            self.position[0] = self.position[0] + (dt * self.vx)
            print('X position update', self.position)
        
        if self.position[1] - self.range_of_sight <= environment_Ycoordinate[0] or self.position[1] + self.range_of_sight >= environment_Ycoordinate[1]:
            self.vy = -1 * self.vy
            print(self.position[1], self.vy)
            self.position[1] = self.position[1] + (dt * self.vy)
            print('Y position update', self.position)
        
        #TODO
        #also need to account for cars not colliding against each other

#Pietro's environment code
class Environment:
    def __init__(self, x_coordinates:list, y_coordinates:list, grid_size):

        self.x_coordinates = x_coordinates
        self.y_coordinates = y_coordinates
        self.grid_size = grid_size

        self.width = int(self.x_coordinates[1]-self.x_coordinates[0]/self.grid_size)       
        self.height = int(self.y_coordinates[1]-self.y_coordinates[0]/self.grid_size)
        self.grid = [[set() for i in range(self.width)] for j in range(self.height)]
        
        #TODO assign agents to a cell
        #if car is in position, put the car ID in the cell set of that position.
        #every time there is a car move, check the positions of each

    def assign(self, car, dt):

        self.grid[car.x][car.y].add(car.ID)
        if dt > 1:
        
            previous_x = car.position[0]
            previous_y = car.position[1]
            
            self.grid[previous_x][previous_y].remove(car.ID)
            
            car.move(dt, self.x_coordinates, self.y_coordinates)
            
        new_x = car.position[0]
        new_y = car.position[1]
        self.grid[new_x][new_y].add(car.ID)
        print('new grid', self.grid)



London = Environment([0,5], [0,6], 1)
print(London.grid)

Honda = Car([5,3], [-5,8], 10.0, 'Aida ID')
print('position before moving', Honda.position)
#Zoe = Car([1,3], [7,-2], 2)
#print(Zoe.position_history)
#print(Honda.is_newCar_in_range_of_sight(Zoe.position))

London.assign(Honda, 5)


#Honda.move(5, London)
#print('position after moving', Honda.position)
#print(Honda.position_history)




