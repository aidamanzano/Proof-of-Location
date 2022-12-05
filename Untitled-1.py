import PoL_Aida as p
import numpy as np 
Number_of_Cars= 5
grid_square = []

#initialising cars with a random position, velocity and range of sight
for car in range(Number_of_Cars):
    position = (np.random.rand(2)*2).tolist()
    velocity = ((np.random.rand(2)*2)-1).tolist()
    range_of_sight = 20
    ID = str(car)
    grid_square.append(p.Car(position, velocity, range_of_sight, ID))

print('cars in grid square',grid_square)

for car in grid_square:
    for nearby_car in grid_square:
        if car != nearby_car:
            car.add_neighbours(nearby_car)
    print('car neighbours', car.neighbors)

