#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Giuliano Cancilla
#OLA 2 Greedy Search Algorithm
#Intro To Artificial Intelligience
#
import numpy as np
import random
import sys
import SumofGaussians as SG

#Custom print function to print values based off of dimension
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
    #grab terminal arguments
    if len(sys.argv) != 4:
        print("Usage: greedy.py <seed> <dimensions> <centers>")
        return 1
    
    randomSeed = int(sys.argv[1]) # random seed
    dimensions = int(sys.argv[2])  #number of dimensions in the Gaussian Function
    centers = int(sys.argv[3]) # number of Gaussians (basically this is just the number of curves that are put together)

    #Set up Random Number Generator

    rng = np.random.default_rng(randomSeed)
    sog = SG.SumofGaussians(dimensions, centers, rng) #this gives u a function
    
    currentX = rng.uniform(size=(dimensions))*10.0 #initialize a random point along the function as a start value
    
    
    

    stepSize = 0.01 #step size => steps in each direction which we will take = StepSize*Gradient
    max_iterations = 100000
    tolerance = 1e-8 #setup tolerance
    iterations = 0 #init counter variable to know if iterations hits 100k
    new_Gx = None #initialize new_Gx to None for initialization purposes
    
    #main while loop <START GREEDY ALGORITHM>
    while iterations < max_iterations:
        gradient = sog.Gradient(currentX) # get the gradient for the current point     X 1
        current_Gx = sog.Evaluate(currentX) #get the Gx of current X value             G(X) 1
        
        
        
        step = stepSize * gradient #Find the step-size of the point
        
        newX = currentX + step                 # Changing our current X
        
        new_Gx = sog.Evaluate(newX) # Y value of our changed X
        
        #check to see if a move is accepted or not
        if new_Gx is not None and abs(current_Gx - new_Gx) < tolerance: #boolean : if absolute_value of (current G(x) - Stepsize Changed G(x))
            if current_Gx < new_Gx: 
                printWithDimensions(dimensions, currentX, current_Gx)
            else:
                printWithDimensions(dimensions, currentX, current_Gx)
            break
        
        printWithDimensions(dimensions, currentX, current_Gx)
        
        #update the currentX if the Y value is lower than that of the step-changed value (The greedy part)
        
        currentX = newX
        iterations += 1 #add an iteration
    
    
    

main()

