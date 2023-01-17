import random
import numpy as np
import car_class as c
import environment_class as e
import networkx as nx
from matplotlib import pyplot as plt
import initialiser_functions as i

def NaivePoL(cars, threshold):
    DAG = nx.Graph()

    True_Positive = 0
    True_Negative = 0
    False_Positive = 0
    False_Negative = 0

    valid_nodes = []
    for car in cars:

        
        position_claim = car.claim_position()
        if len(car.neighbours) == 0:
            car.algorithm_honesty_output = False
            pass
        else:
        #print('Car '+car.ID +' claims position:',position_claim)
        #print('CAR range of sight is', car.range_of_sight)
        #print('number of neighbours: ', len(car.neighbours))


            for neighbor in car.neighbours:
                
                if car.is_in_range_of_sight(neighbor.position):
                    car.neighbour_validations += 1


            score = car.neighbour_validations/len(car.neighbours)
            #print('score =', score)
            if score >= threshold:
                car.algorithm_honesty_output = True
                valid_nodes.append(car)
            else:
                car.algorithm_honesty_output = False

        if car.honest is True and car.algorithm_honesty_output is True:
            True_Positive += 1
        if car.honest is True and car.algorithm_honesty_output is False:
            False_Negative += 1
        if car.honest is False and car.algorithm_honesty_output is True:
            False_Positive += 1
        if car.honest is False and car.algorithm_honesty_output is False:
            True_Negative += 1
    

    for any_Car in valid_nodes:
        for neighbour_of_CAR in any_Car.neighbours:
            if neighbour_of_CAR in valid_nodes:
                DAG.add_node(any_Car)
                DAG.add_node(neighbour_of_CAR)
                DAG.add_edge(any_Car, neighbour_of_CAR)


    Accuracy = ((True_Positive + True_Negative) / (True_Positive + True_Negative + False_Positive + False_Negative)) * 100
    #TODO: check that only cars that have a sufficiently high threshold are used to validate
    #nx.draw(DAG)
    #plt.show()

    #print('no. of nodes: ',DAG.number_of_nodes())

    return Accuracy, DAG, True_Positive, True_Negative, False_Positive, False_Negative
    #https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.connected_components.html



