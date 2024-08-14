import sys
import numpy as np
from sklearn import metrics

def dist(data, centroids):
    print(data.shape)
    print(centroids.shape)
    distances = np.sqrt(((data[:, np.newaxis] - centroids)**2).sum(axis=2))
    return distances

def build_k_means(data, num_clusters):
    centroids = data[np.random.choice(data.shape[0], num_clusters, replace=False), :]
    print(centroids)
    old_centroids = np.zeros(centroids.shape)

    while not np.array_equal(centroids, old_centroids):
        old_centroids = centroids.copy()
        distances = dist(data, centroids)
        labels = np.argmin(distances, axis=1)
        centroids = np.array([data[labels == k, :].mean(axis=0) for k in range(num_clusters)])

    return centroids, labels

def predict(centroids, validation_data):
    print("Validation Data Shape:", validation_data.shape)
    print("Centroids Shape:", centroids.shape)

    distances = np.sqrt(((validation_data[:, np.newaxis, :] - centroids)**2).sum(axis=2))

    print("Distances Shape:", distances.shape)

    predicted_labels = np.argmin(distances, axis=1)
    return predicted_labels

def accuracy(predictions, validation_data_labels, num_clusters):
    cluster_to_class = {}
    
    validation_data_labels = validation_data_labels.astype(int)

    for cluster in range(num_clusters):
        cluster_points = validation_data_labels[predictions == cluster]

        if len(cluster_points) > 0:
            majority_class = np.argmax(np.bincount(cluster_points))
        else:
            majority_class = np.argmax(np.bincount(validation_data_labels))

        cluster_to_class[cluster] = majority_class
    mapped_predictions = np.array([cluster_to_class[cluster] for cluster in predictions])

    correct = sum(mapped_predictions == validation_data_labels)
    return correct

def main():
    numClusters = int(sys.argv[1])
    train_file = sys.argv[2]
    val_file = sys.argv[3]
    
    train_data = np.loadtxt(train_file) # Load only the feature vectors
    train_data = train_data[:,:-1]
    validation_data = np.loadtxt(val_file)
    validation_data_labels = np.loadtxt(val_file, usecols=(-1,))  # Load the class labels
    validation_data = validation_data[:,:-1]
    #print(train_data)
    #print(validation_data)
    #print(validation_data_labels)
    centroids, _ = build_k_means(train_data, numClusters)
    predictions = predict(centroids, validation_data)
    #print(predictions)
    correct_classifications = accuracy(predictions, validation_data_labels, numClusters)
    print(correct_classifications)


    
if __name__ == "__main__":
    main()