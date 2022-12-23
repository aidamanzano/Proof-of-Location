import matplotlib as plt

def Visualise(cars, environment):
    """Visualising cars in the environment, if they are honest they are shown in green, otherwise shown in red"""
    for car in cars:
        x = car.position[0]
        y = car.position[1]

        plt.xlim(environment.x_coordinates[0], environment.x_coordinates[1])
        plt.ylim(environment.y_coordinates[0], environment.y_coordinates[1])
        #TODO: trying to show coerced cars in another colour as well
        plt.scatter(x, y, marker="o", c = ['r' if car.honest is False else 'g'])     
    plt.grid()
    plt.show()

def simulation_plots(number_of_simulations, csv):
    
    fig = plt.figure()
    plt.title('Monte Carlo Simulations of Proof of Location Protocol, Number of Simulations = ' + str(number_of_simulations))
    plt.xlabel('Simulation number')
    plt.ylabel('Accuracy in percentage')
    plt.xlim([0, number_of_simulations])

    #TODO: this is NOT finished/correct at all, need to write this properly

    #Load csv file from path

    #should I make this boxplot or violin?
    plt.bar(simulation_no, Accuracies)
    plt.show()

    #generate plots for each simulation and save them into folder

#call this function for each set of variable simulations
