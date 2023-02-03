import random
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
#IMPORTANT: scipy must be at least version 1.8 otherwise it will throw an attribute error: 
# https://github.com/pyg-team/pytorch_geometric/issues/4378 

#---------------------START OF AIDA POL protocol----------------------:
def PoL(cars):
    DAG = nx.Graph()

    True_Positive = 0
    True_Negative = 0
    False_Positive = 0
    False_Negative = 0


    for car in cars:

        #A Car claims their position, starting the protocol round
        position_claim = car.claim_position()

        #Car 1 names two witnesses
        named_witnesses = car.name_witness()
        named_cars = set()
        named_cars.add(car.ID)


        if named_witnesses is None:
            car.algorithm_honesty_output = False
            

        elif len(named_witnesses) < 2 or (len(named_witnesses) != len(set(named_witnesses))):
            car.algorithm_honesty_output = False
            
            
        else:
            #print('Car'+ car.ID +'names witnesses:', named_witnesses[0].ID, named_witnesses[1].ID)
            
            #check that the witness named is not the car itself (superfluous anyway) # AND check that car doesn't select same witness twice
            #tries = 5
            #for trial in range(tries):
                #named_witnesses = car.name_witness()   
                #if (named_witnesses[0].ID != car and named_witnesses[1].ID != car) and (named_witnesses[0].ID != named_witnesses[1].ID) and len(named_witnesses) >= 2:
                    #break
                #else:
                    #car.algorithm_honesty_output = False
                    #break
                
            #if named_witnesses[0].ID == car.ID or named_witnesses[1].ID == car.ID or named_witnesses[0].ID == named_witnesses[1].ID  or len(named_witnesses) < 2:
                #car.algorithm_honesty_output = False
                #continue

            #if (named_witnesses[0] == car or named_witnesses[1] == car) or (named_witnesses[0] == named_witnesses[1]) or len(named_witnesses) < 2:
                #car.algorithm_honesty_output = False
                #continue

            #TODO: add the red car to the graph only if the witnesses tests pass
            DAG.add_node(car, color = 'red')

            # Two witnesses must attest to seeing Car 1: Car 1 must be a neighbour AND in range of sight
            for witness in named_witnesses:

                if witness.ID in named_cars:
                    car.algorithm_honesty_output = False
                    
                elif witness.is_car_a_neighbour(car) is False:
                    car.algorithm_honesty_output = False
                    
                elif witness.is_in_range_of_sight(car.position) is False:
                    car.algorithm_honesty_output = False
                    

                else:
                    car.algorithm_honesty_output = True

                    named_cars.add(witness.ID)

                    DAG.add_node(witness, color = 'blue')
                    DAG.add_edge(car, witness)
                

                # Witness 1 must name their attestors and Witness 2 must name their attestors
                witness_attestors = witness.name_witness()

                if witness_attestors is None:
                    car.algorithm_honesty_output = False
                    

                #if len(witness_attestors) < 2 or (witness_attestors[0] == witness_attestors[1]):
                elif len(witness_attestors) < 2 or (len(witness_attestors) != len(set(witness_attestors))):
                    car.algorithm_honesty_output = False
                    #print('witness ihas no')
                    

                else:

                    #check that neither of the attestors named is the car AND
                    #check that witness doesn't select same attestor twice AND
                    #check attestor 1 is not already a witness AND
                    #check attestor 2 is not already a witness
                    #tries = 5
                    #for trial in range(tries):
                        #witness_attestors = witness.name_witness()
                        #if witness_attestors[0].ID not in named_cars and witness_attestors[1] not in named_cars and len(witness_attestors) >= 2:
                            #break
                        #else:
                            #car.algorithm_honesty_output = False
                        #if (witness_attestors[0] != car and witness_attestors[1] != car) and (witness_attestors[0] != witness_attestors[1]) and (witness_attestors[0] != named_witnesses[0] and witness_attestors[0] != named_witnesses[1]) and (witness_attestors[1] != named_witnesses[0] and witness_attestors[1] != named_witnesses[1]):
                            #break
                    
                    #if (witness_attestors[0] == car or witness_attestors[1] == car) or (witness_attestors[0] == witness_attestors[1]) or (witness_attestors[0] == named_witnesses[0] or witness_attestors[0] == named_witnesses[1]) or (witness_attestors[1] == named_witnesses[0] or witness_attestors[1] == named_witnesses[1]):
                        #car.algorithm_honesty_output = False
                        #continue


                    # Attestors must be a neighbour AND be in range of sight of witness
                    for attestor in witness_attestors:
                        #TODO: check car is in range of sight of attestor


                        if attestor.is_car_a_neighbour(witness) is False:
                            car.algorithm_honesty_output = False
                            

                        elif attestor.is_in_range_of_sight(witness.position) is False:
                            car.algorithm_honesty_output = False                            

                        else:
                            car.algorithm_honesty_output = True
                            DAG.add_node(attestor, color = 'green')
                            DAG.add_edge(witness, attestor)

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
    plt.show()
    return Accuracy, DAG, True_Positive, True_Negative, False_Positive, False_Negative

import environment_class as e
import initialiser_functions as i

number_of_cars = 1000

for percent in range(0, 110, 10):
    
    coerced_cars = int((percent/100) * number_of_cars)
    remanining_cars = number_of_cars - coerced_cars
    lying_cars = int(remanining_cars/2)
    honest_cars = int(remanining_cars/2)



    print('lying cars: ', lying_cars, 'coerced cars: ', coerced_cars, 'honest cars: ', honest_cars)
    cars = []
    cars = i.car_list_generator(honest_cars, lying_cars, coerced_cars)

    total_cars = len(cars)


    London = e.Environment([0,2], [0,2], 0.25)
    e.environment_update(cars, 0.1, London)

    density = (London.width * London.height) / total_cars

    #Load the PoL algoritm and feed it the initialised objects
    Accuracy, DAG, True_Positive, True_Negative, False_Positive, False_Negative = PoL(cars)
    print('Accuracy',Accuracy, 'Tp: ',((True_Positive/total_cars)*100), True_Positive, 'TN: ',((True_Negative/total_cars)*100), True_Negative, 'FP: ',((False_Positive/total_cars)*100), False_Positive, 'FN: ',((False_Negative/total_cars)*100), False_Negative)

""" lying_cars = 900
remanining_cars = number_of_cars - lying_cars
honest_cars = int(remanining_cars/2)
coerced_cars = int(remanining_cars/2) """