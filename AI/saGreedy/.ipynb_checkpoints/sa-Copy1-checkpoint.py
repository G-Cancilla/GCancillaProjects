#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import numpy as np
import random
import sys
import SumofGaussians as SG
import math

def printWithDimensions(dimensions, currentX, current_Gx):
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
    if len(sys.argv) != 4:
        print("Usage: sa.py <seed (s)> <dimensions (d)> <centers (n)>")
        return 1
    randomSeed = int(sys.argv[1]) # random seed
    dimensions = int(sys.argv[2])  #number of dimensions in the Gaussian Function
    centers = int(sys.argv[3]) # number of Gaussians (basically this is just the number of curves that are put together)

    rng = np.random.default_rng(randomSeed)
    sog = SG.SumofGaussians(dimensions, centers, rng)
    random.seed(randomSeed)
    max_iterations = 100000

    currentX = rng.uniform(size=(dimensions))*10.0 

    temperature = 1.0
    cooling_rate = .9992
    iterations = 0
    testValidityOfMove = 0
    while iterations != max_iterations:
        randomChangeVector = np.random.uniform(-0.05,0.05) # add this to x => recalculate Y => Test Reject or Take
        testValidityOfMove = currentX + randomChangeVector
        current_Gx = sog.Evaluate(currentX)
        
        if sog.Evaluate(testValidityOfMove) > sog.Evaluate(currentX):
            currentX = testValidityOfMove
            current_Gx = sog.Evaluate(testValidityOfMove)
        else:
            function_exponent = (sog.Evaluate(testValidityOfMove)-(sog.Evaluate(currentX)))/temperature
            probability = math.exp(function_exponent)
            randomDecisionNumber = random.random()
            
            if randomDecisionNumber < probability:
                currentX = testValidityOfMove
                current_Gx = sog.Evaluate(testValidityOfMove)
        
        
        printWithDimensions(dimensions, currentX, current_Gx)
        
        temperature *= cooling_rate
        if temperature < 0.01:
            break
        
        
        
        
        iterations +=1
    printWithDimensions(dimensions,currentX, current_Gx)
    # The program should create an annealing schedule for the termperature (-0.05 to 0.05 ), and slowly lowering over time.

    # on each iteration the program should generate a new location y = x + epsilon
    # epsilon is a d-dimnesional vector of random, uniform values in the range [-0.05,0.05] and choose to accept it or reject it based on the metropolis criterion
    
    # metropolis criterion
        # G(y) > G(x) then accept the move to y
        # else accept the move to y with probabibility e^(G(y)-G(x)/t)

    #Max 100k iterations
    # print x and G(x) at each step


main()



#NOTES
## Assume we dont have access to the Gradient for SA and instead we are going to generate small random moves 
## If we take a Y then you replace x with Y on the next iteration
## For probabiblity if it below your threshold take the move, if it is above it then dont take it.