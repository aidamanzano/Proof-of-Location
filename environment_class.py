class Environment:
    
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