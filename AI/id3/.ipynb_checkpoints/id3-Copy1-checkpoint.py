#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import numpy as np

class Node:
    def __init__(self,data,target):
        self.data = data
        self.target = target
        self.children = {}
        self.attribute = None


# this will sort and print to console we need to change the implementation to just return the sorted data based off of the length of the attributes which should be easy.
def sortAlongAxis(fileName):
    # args

    data = np.loadtxt(fileName)
    # Special case of just one data sample will fail
    # without this check!
    if len(data.shape) < 2:
        data = np.array([data])

    # Sort all columns - just retain sorted indices
    # NOT the sorted data to prevent need to resort
    # later on...
    indices = np.argsort(data,axis=0)
    
    # Proceed for each column
    for x in range(data.shape[1]):
        print("Sorting along column number:",x)
        # Go through all data in sorted order
        for y in indices[:,x]:
            # Get one training example in sorted order
            print(data[y,:])
# Sdef Entropy():
    
def main():
    #import the name of the files we need to process
    #Remember we partition the data outside of the code in here.
    testFile = sys.argv[1]
    valFile = sys.argv[2]

    
    
    #Each line will contain the real-valued features for several attributes and a single integer class label at the end
    print(testFile)
    print(valFile)
    testData = np.loadtxt(testFile)
    valData = np.loadtxt(valFile)

    informationGain = 0
    entropy = 0
    sortAlongAxis(testFile)
    """
    The program should build an ID3 decision tree by:        
Sorting the training data along each attribute,        
Determining all potential binary split points based on attribute value changes (averag            e
the two values to make the split: those examples less than the split value or those exampl            es
greater than or equal to the split valu
    e),
Calculating the associated information gain for all of the potential split poi
    nts,
Choose to make a split node for the potential split with the maximum information     
    gain,
Ties (in maximum information gain) should be broken by attribute order (left to righ        t) and
then attribute value (smallest to largest) as found in the inpu
    t file,
Terminal nodes are created instead of split nod        es when:
the probability of one of the class labels is 1 (all others         zero) or
there are no more potential split points found among the attributes (in this c        ase, use a
majority class label vote, with ties in favor of the smaller integer label).
    """






main()