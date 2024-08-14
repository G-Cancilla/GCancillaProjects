import sys
import numpy as np
import seaborn as sns
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def main():
    K = int(sys.argv[1])
    train_file = sys.argv[2]
    val_file = sys.argv[3]
    
    train_data = np.loadtxt(train_file)
    validation_data = np.loadtxt(val_file)
    validation_data_labels = np.loadtxt(val_file, usecols=(4,))  # Load the class labels
    samplePoints = train_data.shape[0]

    x_train, labels = make_blobs(n_samples = samplePoints, centers = K, random_state = 30) # using make_blobs from sklearn library
    x_train = StandardScaler().fit_transform(x_train)

    sns.scatterplot(x = [X[0] for X in x_train], y = [X[1] for X in x_train], hue = labels, pallette = "deep", legend = None)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


    

    print(samplePoints)
    print(train_data)
    print(validation_data)
    print(validation_data_labels)
    #centroids, _ = build_k_means(train_data, numClusters)
    #predictions = predict(centroids, validation_data)
    #print(predictions)
    #correct_classifications = accuracy(predictions, validation_data_labels)
    
    #print(correct_classifications)

if __name__ == "__main__":
    main()