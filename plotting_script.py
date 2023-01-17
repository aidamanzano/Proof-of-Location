import visualisation_functions as v
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns

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
            #print('HERE! ',simulation_path)
            data = pd.read_csv(simulation_path)
            df = df.append(data)

    print(df)
    df.to_csv(directory_path_string+'full_data.csv')


""" #------------------------------------------------

directory_pathfile = '/Users/amm3117/Desktop/Proof-of-Location/Proof-of-Location/Percent of honest cars/'
full_csv(directory_pathfile)

v.simulation_box_plots('Collaborative ', 100, directory_pathfile+'full_data.csv', 'Percent of honest cars', 'Accuracy')
v.subplots('Collaborative ', directory_pathfile, 100, 'Percent of honest cars')
#v.simulation_violin_plots('Collaborative ', 100, directory_pathfile+'full_data.csv', 'Percent of honest cars', 'Accuracy')

#--------------------------------------
directory_pathfile = '/Users/amm3117/Desktop/Proof-of-Location/Proof-of-Location/Percent of coerced cars/'
full_csv(directory_pathfile)


v.simulation_box_plots('Collaborative ', 100, directory_pathfile+'full_data.csv', 'Percent of coerced cars', 'Accuracy')
v.subplots('Collaborative ', directory_pathfile, 100, 'Percent of coerced cars')
#v.simulation_violin_plots('Collaborative ', 100, directory_pathfile+'full_data.csv', 'Percent of coerced cars', 'Accuracy')

#--------------------------------------

directory_pathfile = '/Users/amm3117/Desktop/Proof-of-Location/Proof-of-Location/Percent of lying cars/'
full_csv(directory_pathfile)


v.simulation_box_plots('Collaborative ', 100, directory_pathfile+'full_data.csv', 'Percent of lying cars', 'Accuracy')
v.subplots('Collaborative ', directory_pathfile, 100, 'Percent of lying cars')
#v.simulation_violin_plots('Collaborative ', 100, directory_pathfile+'full_data.csv', 'Percent of lying cars', 'Accuracy') 

 """
#--------------------------------------

directory_pathfile = '/Users/amm3117/Desktop/Proof-of-Location/Proof-of-Location/naivePoL/Percent of honest cars/'
full_csv(directory_pathfile)


v.simulation_box_plots('Naive ', 100, directory_pathfile+'full_data.csv', 'Percent of honest cars', 'Accuracy')
v.subplots('Naive ', directory_pathfile, 100, 'Percent of honest cars')

#---------------------------

directory_pathfile = '/Users/amm3117/Desktop/Proof-of-Location/Proof-of-Location/naivePoL/Percent of lying cars/'
full_csv(directory_pathfile)

v.simulation_box_plots('Naive ', 100, directory_pathfile+'full_data.csv', 'Percent of lying cars', 'Accuracy')
v.subplots('Naive ', directory_pathfile, 100, 'Percent of lying cars')

#TODO: check regret values? plot confusion matrix