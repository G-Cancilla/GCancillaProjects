#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Giuliano Cancilla
#OLA 2 Simulated Annealing
#Intro To Artificial Intelligience
#Description: This program performs Simulated Annealing (hill climbing) search to find local Maxima in a Sum of Gaussian function.
#  X and G(x) are printed to the console for each iteration.

import numpy as np
import random
import sys
import SumofGaussians as SG
import math

#Custom print function depending on the type of dimensions passed from console
def printWithDimensions(dimensions, currentX, current_Gx):
    # since currentX is a numpy array if we have different dimensions we need to account for that
    # Doing it this way made the most sense to me, but I think there is probably a simpler solution
    if dimensions == 1:
        print(f'{currentX[0]:.8f} {current_Gx:.8f}')
    if dimensions == 2:
        print(f'{currentX[0]:.8f} {currentX[1]:.8f} {current_Gx:.8f}')
    if dimensions == 3:
        print(f'{currentX[0]:.8f} {currentX[1]:.8f} {currentX[2]:.8f} {current_Gx:.8f}')
    if dimensions == 4:
        print(f'{currentX[0]:.8f} {currentX[1]:.8f} {currentX[2]:.8f} {currentX[3]:.8f} {current_Gx:.8f}')
    if dimensions == 5:
        print(f'{currentX[0]:.8f} {currentX[1]:.8f} {currentX[2]:.8f} {currentX[3]:.8f} {currentX[4]:.8f} {current_Gx:.8f}')

def main():
    # I wanted to add this because it allowed me to have a way to easily remember the order of things being passed in
    if len(sys.argv) != 4:
        print("Usage: sa.py <seed (s)> <dimensions (d)> <centers (n)>")
        return 1
    
    # init our variables from STDIN
    randomSeed = int(sys.argv[1]) # random seed
    dimensions = int(sys.argv[2])  #number of dimensions in the Gaussian Function
    centers = int(sys.argv[3]) # number of Gaussians (basically this is just the number of curves that are put together)

    #init random number generator
    rng = np.random.default_rng(randomSeed)
    #initialize the SOG function
    sog = SG.SumofGaussians(dimensions, centers, rng)
    #set the seed
    random.seed(randomSeed)
    
    #Program should not go over 100k iterations
    max_iterations = 100000

    #set currentX to a random starting point between 0 and 10
    currentX = rng.uniform(size=(dimensions))*10.0 

    #I chose to do a linear annealing schedule by setting temp to 1.0 and then slowly decrementing it over time
    temperature = 1.0
    cooling_rate = .9995 #Annealing schedule variable to decrement the temperature after each iteration
    #iteration count and another variable so we can keep track of a second point along the SOG
    iterations = 0
    testValidityOfMove = 0

    #main loop <START SIMULATED ANNEALING>
    while iterations != max_iterations:
        #init a random vector between -0.05 and 0.05, also takes into account the dimensions because it could be a multidimensional SOG
        randomChangeVector = np.random.uniform(-0.05,0.05,dimensions) # add this to x => recalculate Y => Test Reject or Take
        # add currentX with the randomChangeVector and store that in testValidityOfMove
        testValidityOfMove = currentX + randomChangeVector
        
        #find the Y of currentX so we can test the difference between testValidityOfMove 
        current_Gx = sog.Evaluate(currentX)

        #<CHECK TO SEE IF WE TAKE OR REJECT MOVE>
        #If the G(x) value of the translated point is greater than the current G(x) then we accept the move and update G(x) for current_Gx
        if sog.Evaluate(testValidityOfMove) > current_Gx:
            currentX = testValidityOfMove
            current_Gx = sog.Evaluate(testValidityOfMove)
        #Metropolis Criterion
        else:
            #set the probabibility e^(( G(x)1 - G(x)2)/Temperature) => probability
            #this is essentially calculating a probability that the move we make is a good move
            function_exponent = (sog.Evaluate(testValidityOfMove)-(sog.Evaluate(currentX)))/temperature
            probability = math.exp(function_exponent)
            
            #random roll of the dice to see if we fall within the probability or not
            randomDecisionNumber = random.random()

    
            if randomDecisionNumber < probability: # if the dice roll is less than the probability then we take the move else we continue
                currentX = testValidityOfMove
                current_Gx = sog.Evaluate(testValidityOfMove)
        
        #print CurrentX vals and the Current G(x)
        printWithDimensions(dimensions, currentX, current_Gx)

        #apply the linear change in the temperature
        temperature *= cooling_rate

        #As temperature gets really really low, the probability that we are going to make a move goes down. This stipulation here says that if the temperature is getting close to 0 we are settling around a point.
        #This speeds up the code because if we are approaching 0 for temperature then we can quit.
        if temperature < 0.001: #he key factor in the SA algorithm is the temperature parameter. As the temperature decreases, the probability of accepting a new value decreases. 
            break
        
        
        
        #increment iterations
        iterations +=1
    #print the last value
    printWithDimensions(dimensions,currentX, current_Gx)
main()

