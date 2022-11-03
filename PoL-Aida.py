import numpy as np
class Car:
    """class to create a car with a given position, range of sight and list of neighbors"""

    def __init__(self, position: list, velocity: list, range_of_sight: float):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.range_of_sight = range_of_sight

        self.x = position[0]
        self.y = position[1]

        self.vx = velocity[0]
        self.vy = velocity[1]

        self.neighbors = []

    @property
    def position(self):
        return(self._position)

    #Making sure the coordinates given are not less than [0, 0]
    @position.setter
    def position(self, value):
        if value[0] < 0 or value[1] < 0:
            raise ValueError('Position must be a positive coordinate')
        self._position = value

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

    def move(self, dt):
        #self.x += dt* self.vx
        #self.y += dt * self.vy
        self.position += dt * self.velocity

Honda = Car([5, 3], [-5,8], 10.0)
print('position before moving', Honda.position)
Zoe = Car([1,3], [7,-2], 2)
print(Honda.is_newCar_in_range_of_sight(Zoe.position))
Honda.move(1)
print('position after moving', Honda.position)

