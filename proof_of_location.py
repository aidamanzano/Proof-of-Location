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
    
    #nx.draw(DAG, node_color=car_colors)
    #print(Accuracy)
    #print(True_Negative, True_Positive, False_Negative, False_Positive)
    #plt.show()
    return Accuracy, DAG