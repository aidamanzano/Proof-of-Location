import random
import numpy as np
from car_class import Car, lying_car

def honest_cars_init(N_honest_cars:int, car_list:list):
#initialising honest cars with a random position, velocity and range of sight
    for car in range(N_honest_cars):
        position = (np.random.rand(2)*2).tolist()
        velocity = ((np.random.rand(2)*2)-1).tolist()
        range_of_sight = 0.1 #np.random.uniform(0, 0.25, size=(1)).astype(int)
        ID = str(car)
        coerced = False
        car_list.append(Car(position, velocity, range_of_sight, ID, coerced))
    return car_list

def coerced_cars_init(N_coerced_cars:int, car_list:list, position=(np.random.rand(2)*2).tolist()):
#initialising coerced cars with a random position, velocity and range of sight
    for car in range(N_coerced_cars):
        position = position
        velocity = ((np.random.rand(2)*2)-1).tolist()
        range_of_sight = 0.1 #np.random.uniform(0, 0.25, size=(1)).astype(int)
        ID = str(car)
        coerced = True
        car_list.append(Car(position, velocity, range_of_sight, ID, coerced))
    return car_list

def lying_cars_init(N_lying_cars:int, car_list:list, fake_position=(np.random.rand(2)*2).tolist()):
#initialising lying cars with a random position, velocity and range of sight
    for liar_car in range(N_lying_cars):
        position = (np.random.rand(2)*2).tolist()
        velocity = ((np.random.rand(2)*2)-1).tolist()
        range_of_sight = 0.1 #round(random.uniform(0.1,0.2), 100)
        #range_of_sight = np.random.uniform(0, 0.25, size=(1)).astype(float)
        ID = str(liar_car)
        coerced = False
        fake_position = fake_position #(np.random.rand(2)*2).tolist()  #position = np.random.uniform(0, 0.25, size=(2)).tolist()
        car_list.append(lying_car(position, velocity, range_of_sight, ID, coerced, fake_position))
    return car_list


def car_list_generator(Number_of_honest_cars, Number_of_lying_cars, Number_of_coerced_cars):
    cars = []
    cars = honest_cars_init(Number_of_honest_cars, cars)
    cars = coerced_cars_init(Number_of_coerced_cars, cars)
    cars = lying_cars_init(Number_of_lying_cars, cars)
    return cars
