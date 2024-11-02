from clustering import kmeans, dbscan, kmedoids, manhattan_distance
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def describe_clusters(df, labels):
    # Create a dictionary to hold the results
    cluster_frequent_attributes = {}

    # Convert labels to a pandas Series to use it for indexing
    labels_series = pd.Series(labels)

    # Loop through each unique cluster
    for cluster in labels_series.unique():
        # Filter dataframe to include only rows in the current cluster
        cluster_df = df[labels_series == cluster]

        # Store the most frequent values for each attribute in the cluster
        cluster_frequent_attributes[cluster] = {}
        for column in df.columns:
            # Use Counter to find the most common value in each column
            most_common_value = Counter(cluster_df[column]).most_common(1)[0][0]
            cluster_frequent_attributes[cluster][column] = most_common_value

        # Print the results for the current cluster
        print(f"Cluster {cluster}:")
        for attribute, value in cluster_frequent_attributes[cluster].items():
            print(f"  Most frequent {attribute}: {value}")


if __name__ == "__main__":
    # ---------------------DBSCAN---------------------
    # Load the data
    data = pd.read_csv('cancer_data.csv')
    cancer_data = pd.read_csv('cancer_pca_data.csv')

    # Run algorithm on first 400 rows
    data = data.iloc[:400, :]
    cancer_data = cancer_data.iloc[:400, :]

    columns = cancer_data.columns.tolist()

    clusters = dbscan(cancer_data, columns, .5, 4)

    score = silhouette_score(cancer_data, clusters)

    print("Silhouette Score:", score)

    cancer_data['Cluster'] = clusters
    data['Cluster'] = clusters

    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=cancer_data.iloc[:, 0], y=cancer_data.iloc[:, 1],
                    hue='Cluster', palette='viridis', data=cancer_data, legend='full')
    plt.title("DBSCAN Cluster Visualization")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend(title="Cluster", loc="upper right")
    plt.show()

    describe_clusters(data, clusters)

    # ---------------------Kmedoid---------------------
    # Prepare data for kmedoids clustering
    column = cancer_data[['PC1', 'PC2']].values.tolist()

    # Define range of k values to test
    k_values = range(2, 7)  # We will test k values from 2 to 7
    silhouette_scores = []

    # Test each k value and calculate silhouette score
    for k in k_values:
        medoids = kmedoids(
            column, k, distance=manhattan_distance, n=100, eps=1e-3)
        clusters_kmedoids = [
            min(range(k), key=lambda idx: manhattan_distance(
                point, medoids[idx]))
            for point in column
        ]
        score = silhouette_score(
            cancer_data[['PC1', 'PC2']], clusters_kmedoids)
        silhouette_scores.append(score)

    # Plot silhouette scores for each k
    plt.figure(figsize=(8, 5))
    plt.plot(k_values, silhouette_scores, marker='o', linestyle='-')
    plt.title("Silhouette Analysis for Optimal k in K-Medoids")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Silhouette Score")
    plt.show()

    # Select the optimal k with the highest silhouette score
    optimal_k = k_values[silhouette_scores.index(max(silhouette_scores))]
    print("Optimal number of clusters (k) based on silhouette analysis:", optimal_k)

    # Run kmedoids with optimal k
    medoids = kmedoids(column, optimal_k,
                       distance=manhattan_distance, n=100, eps=1e-3)
    # Assign clusters based on kmedoids medoids
    clusters_kmedoids = [
        min(range(optimal_k), key=lambda idx: manhattan_distance(
            point, medoids[idx]))
        for point in column
    ]

    # Calculate silhouette score for final clustering
    final_score_kmedoids = silhouette_score(
        cancer_data[['PC1', 'PC2']], clusters_kmedoids)
    print("Final K-Medoids Silhouette Score with optimal k:", final_score_kmedoids)

    # Visualize final kmedoids clusters
    cancer_data['Cluster_KMedoids'] = clusters_kmedoids
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x='PC1', y='PC2', hue='Cluster_KMedoids',
                    palette='viridis', data=cancer_data, legend='full')
    plt.title("K-Medoids Cluster Visualization with Optimal k")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend(title="Cluster", loc="upper right")
    plt.show()

# -------------- KMeans ------------------


def test_kmeans(test_data, columns, k):
    centers = kmeans(test_data, k, columns, eps=0.001)

    print("Final Cluster Centers:", centers)

    def assign_labels(data, centers, columns):
        labels = []
        # Make sure to only use the selected columns for distance calculation
        selected_data = data[columns].to_numpy()

        for point in selected_data:
            # Calculate Euclidean distance to each cluster center
            distances = [np.sqrt(np.sum((point - np.array(center)) ** 2))
                         for center in centers]
            # Assign the data point to the nearest center
            labels.append(np.argmin(distances))
        return np.array(labels)

    # Get cluster labels based on the nearest center
    labels = assign_labels(test_data, centers, columns)

    # Calculate the silhouette score using the data and labels
    score = silhouette_score(test_data, labels)
    print("Silhouette Score:", score)

    # Plot the clusters
    plt.figure(figsize=(8, 6))
    for cluster in range(k):
        # Filter points belonging to the current cluster
        cluster_points = test_data[columns][labels == cluster]
        plt.scatter(cluster_points[columns[0]],
                    cluster_points[columns[1]], label=f'Cluster {cluster + 1}')

    # Plot cluster centers
    centers = np.array(centers)
    plt.scatter(centers[:, 0], centers[:, 1], c='red',
                marker='X', s=200, label='Centers')

    # Customize plot
    plt.xlabel(columns[0])
    plt.ylabel(columns[1])
    plt.legend()
    plt.title('KMeans Clustering')
    plt.show()
