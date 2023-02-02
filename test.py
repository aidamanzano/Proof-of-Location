import numpy as np
number_of_cars = 1000

for percent in range(0, 110, 10):
    
    lying_cars = percent/100 * number_of_cars
    print('lying cars: ',lying_cars, 'percentage', percent/100)
    honest_and_coerced = np.round((1 - (percent/100)), 2) * number_of_cars
    print('honest and coerced: ',honest_and_coerced, 'percentage', np.round((1 - (percent/100)), 2))

    for value in range(0, int(honest_and_coerced) + 10, 10):

        honest_cars = honest_and_coerced - value
        print('honest cars: ',honest_cars)

        coerced_cars = value
        print('coerced cars: ',coerced_cars)