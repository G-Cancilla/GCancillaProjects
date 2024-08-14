#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
from sklearn import metrics

#Calculate the distances between the data points and the centroids using Euclidean Distance
def dist(data, centroids):
    distances = np.sqrt(((data[:, np.newaxis] - centroids)**2).sum(axis=2))
    return distances

#Main function to build the K Means Cluster model
def build_k_means(data, num_clusters):
    #initialize the centroids in random points using random.choice
    centroids = data[np.random.choice(data.shape[0], num_clusters, replace=False), :]
    #Temporary variable to hold the old centroids.
    #This just initializes the structure with zeros in the form of centroids.shape
    old_centroids = np.zeros(centroids.shape)

    #This while loop will stop executing when the centroids no longer move.
    while not np.array_equal(centroids, old_centroids):
        #update old_centroids
        old_centroids = centroids.copy()
        #calculate distances
        distances = dist(data, centroids)
        #assign the labels to data points based off of the closest centroid
        labels = np.argmin(distances, axis=1)
        
        new_centroids = []
        for k in range(num_clusters):
            cluster_points = data[labels == k, :]
            if len(cluster_points) > 0:
                centroid = cluster_points.mean(axis = 0)
                new_centroids.append(centroid)
            else:
                # If the cluster is empty, keep the centroid unchanged
                new_centroids.append(centroids[k])

        centroids = np.array(new_centroids)
    #return the centroids and the labels
    return centroids, labels

def predict(centroids, validation_data):
    #Find the distances between validation points and the centroids
    distances = np.sqrt(((validation_data[:, np.newaxis, :] - centroids)**2).sum(axis=2))
    #the predicted labels are then assigned by finding the lowest distance between each centroid and each validation data point.
    predicted_labels = np.argmin(distances, axis=1)
    #return labels for printing
    return predicted_labels



def accuracy(predictions, validation_data_labels, num_clusters):
    cluster_to_class = {}
    
    # Convert validation data labels to integers
    validation_data_labels = validation_data_labels.astype(int)
    

    # Map each cluster to the majority class in that cluster
    for cluster in range(num_clusters):
        cluster_points = validation_data_labels[predictions == cluster]
        if len(cluster_points) > 0:
            majority_class = np.argmax(np.bincount(cluster_points))
        else:
            majority_class = np.argmax(np.bincount(validation_data_labels))

        cluster_to_class[cluster] = majority_class

    # Map predicted labels to majority class labels
    mapped_predictions = np.array([cluster_to_class[cluster] for cluster in predictions])

    # Calculate the number of correct classifications
    correct = sum(mapped_predictions == validation_data_labels)
    return correct


def main():
    numClusters = int(sys.argv[1]) #load the amount of clusters we want
    train_file = sys.argv[2] #load the training data into a string
    val_file = sys.argv[3] #load the validation data into a string
     
    train_data = np.loadtxt(train_file) #load the file into a NumPy array
    train_data = train_data[:,:-1] # cut the last row off considering we wont need it and to make sure that it is truly unsupervised
    
    validation_data = np.loadtxt(val_file) # load the validation file into a NumPy array
    validation_data_labels = np.loadtxt(val_file, usecols=(-1,)) # Cut the last column off and store it in the validation labels.
    validation_data = validation_data[:,:-1] #Store the columns of the array in validation_data when for sending it to the prediction function
    
    
    centroids, temp = build_k_means(train_data, numClusters)
    predictions = predict(centroids, validation_data)
    correct_classifications = accuracy(predictions, validation_data_labels, numClusters)
    print(correct_classifications)

    
if __name__ == "__main__":
    main()