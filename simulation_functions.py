import os
import car_class as c
import environment_class as e
import proof_of_location as p
import refactoredNaivePoL as npol
import pandas as pd
import initialiser_functions as i
import numpy as np

def parser(simulation_number, coerced_cars, lying_cars, honest_cars, density, accuracy, True_Positive, True_Negative, False_Positive, False_Negative):
    #return list: ['Simulation number', 'Percent of coerced cars', 'Percent of lying cars', 'Percent of honest cars', 'Accuracy']
    total_cars = coerced_cars + lying_cars + honest_cars
    percent_coerced_cars = np.round(((coerced_cars / total_cars) * 100), 2)
    percent_lying_cars = np.round(((lying_cars / total_cars) * 100), 2)
    percent_honest_cars = np.round(((honest_cars / total_cars) * 100), 2)
    
    percent_true_positives = np.round(((True_Positive / total_cars) * 100), 2)
    percent_true_negatives = np.round(((True_Negative / total_cars ) * 100), 2)
    percent_false_positives = np.round(((False_Positive / total_cars) * 100), 2)
    percent_false_negatives = np.round(((False_Negative / total_cars) * 100), 2)

    row_list = [simulation_number, percent_coerced_cars, percent_lying_cars, percent_honest_cars, density, accuracy, 
    True_Positive, True_Negative, False_Positive, False_Negative, percent_true_positives, percent_true_negatives, 
    percent_false_positives, percent_false_negatives]

    return row_list

def check_interest_variable(var, list):
    '''Given an index for the variable of interest, it finds the absolute value for the variable of interest
    and returns a string, to use it as the filename of the simulation'''
    for index in range(len(list)):
        
        if var == index:
            return str(list[index])



def aPoL_simulation_generator(number_of_simulations:int, Number_of_coerced_cars:int, Number_of_lying_cars:int, Number_of_honest_cars:int, interest_variable:int, variable_list:list):
    """Simulation generator for aPoL that takes number of simulations to perform, the three relevant variables. 
    interest_variable the index corresponding to the variable you want to pick from the variable_list"""

    data = []
    
    for simulation in range(number_of_simulations):
        cars = []
        cars = i.car_list_generator(Number_of_honest_cars, Number_of_lying_cars, Number_of_coerced_cars)
        
        total_cars = len(cars)
        

        London = e.Environment([0,2], [0,2], 0.25)
        e.environment_update(cars, 0.1, London)
        
        density = (London.width * London.height) / total_cars

        #Load the PoL algoritm and feed it the initialised objects
        Accuracy, DAG, True_Positive, True_Negative, False_Positive, False_Negative = p.PoL(cars)

        row = parser(simulation, Number_of_coerced_cars, Number_of_lying_cars, Number_of_honest_cars, density, Accuracy, True_Positive, True_Negative, False_Positive, False_Negative)
        
        data.append(row)
        
    df = pd.DataFrame(data, columns=['Simulation number', 'Percent of coerced cars', 'Percent of lying cars', 'Percent of honest cars', 'Density', 'Accuracy', 
    'True Positives', 'True Negatives', 'False Positives', 'False Negatives', 
    'Percent True Positives', 'Percent True Negatives', 'Percent False Positives','Percent False Negatives'])
    
    #filename will be the absolute number of cars of the variable of interest
    filename = check_interest_variable(interest_variable, variable_list)
    
    headers = df.columns.tolist()
    cwd = os.getcwd()
    
    #interest_variable is an index, and to match it to the correct header title we add one, since the headers list starts
    #with 'Simulation number' as its first element
    path = cwd + '/' +  headers[interest_variable+1] + '/'
    os.makedirs(path, exist_ok =True)

    #create a csv file in the path that is the current working directory + a new folder called the same as the interest variable +
    # + the absolute number of cars of the variable of interest.txt
    df.to_csv(path + filename + '.txt')
    
    return path + filename + '.txt', total_cars

def aPoL_simulation(number_of_simulations:int, Number_of_coerced_cars:int, Number_of_lying_cars:int, Number_of_honest_cars:int, interest_variable:int, variable_list:list):
    """Simulation generator for aPoL that takes number of simulations to perform, the three relevant variables. 
    interest_variable the index corresponding to the variable you want to pick from the variable_list"""

    data = []
    
    for simulation in range(number_of_simulations):
        cars = []
        cars = i.car_list_generator(Number_of_honest_cars, Number_of_lying_cars, Number_of_coerced_cars)
        
        total_cars = len(cars)
        

        London = e.Environment([0,2], [0,2], 0.25)
        e.environment_update(cars, 0.1, London)
        
        density = (London.width * London.height) / total_cars

        #Load the PoL algoritm and feed it the initialised objects
        Accuracy, DAG, True_Positive, True_Negative, False_Positive, False_Negative = p.PoL(cars)

        row = parser(simulation, Number_of_coerced_cars, Number_of_lying_cars, Number_of_honest_cars, density, Accuracy, True_Positive, True_Negative, False_Positive, False_Negative)
        
        data.append(row)
        
    simulation_df = pd.DataFrame(data, columns=['Simulation number', 'Percent of coerced cars', 'Percent of lying cars', 'Percent of honest cars', 'Density', 'Accuracy', 
    'True Positives', 'True Negatives', 'False Positives', 'False Negatives', 
    'Percent True Positives', 'Percent True Negatives', 'Percent False Positives','Percent False Negatives'])

    return simulation_df

def make_directory(target_path):
    cwd = os.getcwd()
    path = cwd + target_path
    os.makedirs(path, exist_ok =True)
    return path

def save_simulation(simulation_df, path, simulation_id):
    simulation_path = path + str(simulation_id) + '.txt'
    simulation_df.to_csv(simulation_path)

    return simulation_path


def npol_simulation_generator(number_of_simulations:int, Number_of_coerced_cars:int, Number_of_lying_cars:int, Number_of_honest_cars:int, interest_variable:int, variable_list:list, threshold):
    """Simulation generator for naive PoL algorithm that takes number of simulations to perform, the three relevant variables. 
    interest_variable the index corresponding to the variable you want to pick from the variable_list"""

    data = []
    
    for simulation in range(number_of_simulations):
        cars = []
        cars = i.car_list_generator(Number_of_honest_cars, Number_of_lying_cars, Number_of_coerced_cars)
        
        total_cars = len(cars)
        

        London = e.Environment([0,2], [0,2], 0.25)
        e.environment_update(cars, 0.1, London)
        
        density = (London.width * London.height) / total_cars

        #Load the PoL algoritm and feed it the initialised objects
        Accuracy, DAG, True_Positive, True_Negative, False_Positive, False_Negative = npol.NaivePoL(cars, threshold)

        row = parser(simulation, Number_of_coerced_cars, Number_of_lying_cars, Number_of_honest_cars, density, Accuracy, True_Positive, True_Negative, False_Positive, False_Negative)
        
        data.append(row)
        
    df = pd.DataFrame(data, columns=['Simulation number', 'Percent of coerced cars', 'Percent of lying cars', 'Percent of honest cars', 'Density', 'Accuracy', 
    'True Positives', 'True Negatives', 'False Positives', 'False Negatives', 
    'Percent True Positives', 'Percent True Negatives', 'Percent False Positives','Percent False Negatives'])
    
    #filename will be the absolute number of cars of the variable of interest
    filename = check_interest_variable(interest_variable, variable_list)
    
    headers = df.columns.tolist()
    cwd = os.getcwd()
    
    #interest_variable is an index, and to match it to the correct header title we add one, since the headers list starts
    #with 'Simulation number' as its first element
    path = cwd + '/' + 'naivePoL/' + headers[interest_variable+1] + '/'
    os.makedirs(path, exist_ok =True)

    #create a csv file in the path that is the current working directory + a new folder called the same as the interest variable +
    # + the absolute number of cars of the variable of interest.txt
    df.to_csv(path + filename + '.txt')
    
    return path + filename + '.txt', total_cars


def full_csv(directory_path_string):
    """Given a directory pathfile with .txt files of simulation data, 
    loops through each one, reads them and creates one .csv file with 
    all the simulation data"""
    
    directory = os.fsencode(directory_path_string)
    df = pd.DataFrame()

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        if filename.endswith('.txt'):
            simulation_path = directory_path_string + filename
            data = pd.read_csv(simulation_path)
            df = df.append(data)

    print(df)
    df.to_csv(directory_path_string+'full_data.csv')