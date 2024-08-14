#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Giuliano Cancilla
#Description: Takes two command line arguments, testing data and validation data. ./split.bash is used to create the data at a split
# Usage: cat iris-data.txt | ./split.bash {x} python3 id3.py
# Where x is the amount of validation examples you would like.


import sys
import numpy as np
import math
import pandas as pd
class Node:
    def __init__(self,attribute = None, split_value = None, label = None, left = None, right = None):
        self.attribute = attribute
        self.split_value = split_value
        self.label = label
        self.left = left
        self.right = right

#This reads in a file from the main functions and formats the data by loading it into a numpy array and splicing it into features and labels.
def convertData(filename):
    data = np.loadtxt(filename)
    ## this is just so when the data is read with the minimum or maximum amount of validation data examples
    if len(data.shape) < 2:
        data = np.array([data])

    ## split the features by all of the rows and columns except the last
    features = data[:,:-1]
    
    ## the labels in turn are the last column
    labels = data[:,-1].astype(int)
    
    return features,labels

#This calculates the entropy of a set of data.
def Entropy(labels):
    unique_labels,counts = np.unique(labels,return_counts=True) #Store the unique labels, and how many times they occur
    probabilities = counts/len(labels) # The probability is the count of unique labels divided by the length of how many labels there are.
    entropy = -np.sum(probabilities* np.log2(probabilities)) # formula for entropy = -Sum(probability * log (base 2) of probability)
    return entropy

#This function calculates the information gain
def InformationGain(features,labels,split_value,attribute):
        starting_entropy = Entropy(labels) # find the starting entropy by calculating the entropy of the entire set before any split
        
        left = features[:,attribute] < split_value #set up a boolean mask, basically it just tells me which values are less than the split_value
        
        right = ~left     #this is the remaining values after determining if they are lower than the split.

        #Then, based off of the split we want to calculate the weighted average of the entropies in the two divided subsets.
        ending_entropy = (np.sum(left)/len(labels))*Entropy(labels[left]) + (np.sum(right) / len(labels)) * Entropy(labels[right])
        informationGain = starting_entropy - ending_entropy
        return informationGain

#This function sorts the data while maintaining the class labels.
#It sorts it from lowest to highest in column order
#Then it also maintains that same sort with the class labels, so nothing gets misplaced.
def sortAlongAxis(features,labels,attribute):
    
    indices = np.argsort(features[:,attribute])
    sorted_features = features[indices]
    sorted_labels = labels[indices]
    return sorted_features, sorted_labels

def findSplit(features,labels):
    num_attributes = features.shape[1] # finding the number of attributes using shape method, good for re-useability.
    bestIG = 0
    bestAttr = None #initiliaze best attribute to None because if we do any number it will be out of range or a number we dont want if we dont find one
    bestSplit = None # same here
    
    for attribute in range(num_attributes):
        sorted_attributes,sorted_labels = sortAlongAxis(features,labels,attribute)
        attribute_values = sorted_attributes[:,attribute]
        previous = attribute_values[0]
        for value in attribute_values:
            if previous is None: #only executing if the attribute values are unique values and some change has been made
                continue
            else:
                split_value = (previous + value)/2 # averaging the split values only if they are unique values
                temp_information_gain = InformationGain(sorted_attributes,sorted_labels,split_value,attribute)
                #Here we are searching for the best information gain so we can determine what is the best attribute to split on.
                if temp_information_gain > bestIG:
                    bestIG = temp_information_gain
                    bestAttr = attribute
                    bestSplit = split_value
                previous = value
    return bestAttr, bestSplit #this is going to return the bestattribute to follow down and the best split.

def BuildTree(features,labels):
    #are all current class labels in a subset the same?
    #The probability is 1 so we add a terminal node.
    if len(np.unique(labels)) == 1:
        leafNode = Node(label = labels[0])
        return leafNode
      
    #find best attributes and split for current subset.
    bestAttr, bestSplit = findSplit(features,labels)
    
    #if no splits, then there is no information gain and so we make a terminal node.
    if bestAttr == None:
        majority = np.argmax(np.bincount(labels)) ## find the most frequent element in the labels
        leafNode = Node(label = majority)
        return leafNode
    #again we make a boolean mask to tell us which numbers are below the split and which ones are above the split
    left_indices = features[:, bestAttr] < bestSplit
    right_indices = ~left_indices

    #Recursively call BuildTree on the left and the right subsets.
    left_leaf = BuildTree(features[left_indices], labels[left_indices])
    right_leaf = BuildTree(features[right_indices], labels[right_indices])


    #EDITORS NOTE: (Relating to the next line of code) Recursion is really good in tree structures. It took me a bit to figure this out but using recursion
    #   in a tree structure is probably one of the easiest ways to do it.

    
    #This is why the recursive call works.
    #This actually sets up a node with all of the information we have gathered so far.
    #This propogates down until a base case is met and then is re-propogated up.
    #If we think of the deepest recursive level this program will reach, this will be the node that contains the information for last node in the structure
    #Alternatively, on the most shallow end of the recursive call we will see the root node.
    retNode = Node(attribute = bestAttr, split_value = bestSplit, left = left_leaf, right = right_leaf)

    return retNode
#Iterating through the tree recursively until a label is found
def classify(tree, data):
    #if current node = terminal node, return the label (Base Case)
    if tree.label is not None:
        return tree.label
    
    #recursive cases

    #if the current attribute value is less than the current split_value, then follow the left node.
    if data[tree.attribute] < tree.split_value:
        return classify(tree.left,data)
    #if the current attribute value is greater than, just follow the right node.
    else:
        return classify(tree.right,data)

#using our classification function to classify the validation data by looping through the rows in the validation data and classifying it based off of the tree.
def classifyAll(tree,data):
    return np.array([classify(tree, example) for example in data])

def main():
    #import the name of the files we need to process
    #pre-partitioned using ./split.bash
    trainingFile = sys.argv[1]
    validationFile = sys.argv[2]

    #convert both of the data
    training_features,training_labels = convertData(trainingFile)
    validation_features,validation_labels = convertData(validationFile)

    #build decision tree
    decision_tree = BuildTree(training_features, training_labels)

    #get the predictions
    predictions = classifyAll(decision_tree, validation_features)

    #basically this just says that you take the sum of what the boolean (predictions == validation_labels)
    correct = np.sum(predictions == validation_labels)

    #print result
    print(correct)
    

main()