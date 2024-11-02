import pandas as pd
import numpy as np
import random
import math

# Set DEBUG to True to print debug information
DEBUG = False

# # Uncomment the following lines for custom test cases
# # For custom test cases, the provided test cases use a different function for distance calculation
# def euclidean_distance(a, b):
#     return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def manhattan_distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

# DO NOT CHANGE THE FOLLOWING LINE


def kmeans(data, k, columns, centers=None, n=None, eps=None):
    # Convert the data to a numpy array using specified columns
    if isinstance(data, pd.DataFrame):
        data_points = data[columns].values
    else:
        data_points = np.array(data)

    # Initialize cluster centers
    if centers is None:
        random_indices = random.sample(range(len(data_points)), k)
        centers = data_points[random_indices]
    else:
        centers = np.array(centers)

    iteration = 0  # Initialize iteration count

    while True:
        # Assign each point to the nearest cluster center
        labels = []
        for point in data_points:
            # Use Euclidean distance
            distances = [np.sqrt(np.sum((point - center) ** 2))
                         for center in centers]
            labels.append(np.argmin(distances))
        labels = np.array(labels)

        # Update cluster centers
        new_centers = np.copy(centers)  # Copy current centers to update

        for j in range(k):
            # Check if any points were assigned to cluster j
            if np.any(labels == j):
                new_centers[j] = data_points[labels == j].mean(axis=0)
            else:
                # Optionally, reinitialize the center randomly if it's empty
                new_centers[j] = data_points[random.sample(
                    range(len(data_points)), 1)].flatten()

        # Check for convergence
        center_shifts = np.sqrt(np.sum((new_centers - centers) ** 2, axis=1))

        # Stop if eps is provided and center shifts are less than eps
        if eps is not None and np.all(center_shifts < eps):
            break

        # If n is provided, stop after n iterations
        if n is not None:
            iteration += 1
            if iteration >= n:
                break

        centers = new_centers

    # Format and round cluster centers before returning
    centers = [list(map(lambda x: round(x, 2), center)) for center in centers]
    return centers


# DO NOT CHANGE THE FOLLOWING LINE
def dbscan(data, columns, eps, min_samples):
    # DO NOT CHANGE THE PRECEDING LINE
    # This function has to return a list of cluster centers (lists of floats of the same length as columns)
    # This function has to return a list of cluster centers (lists of floats of the same length as columns)

    # Finds all points which are neighbors of a datapoint P
    def epsilon_neighbors(data, columns, eps, p):
        print("Finding direct epsilon neighbors for point: ", p)
        # All neighbors of a point p
        p_neighbors = []

        # Data for point p
        data_p = data.loc[p, columns]

        # For each datapoint in data:
        for i in range(0, len(data)):
            data_point = data.loc[i, columns]

            # Calculate the euclidean distance between point p and point i
            distance = np.sqrt(np.sum((data_p - data_point) ** 2))

            # If the distance is within epsilon, it is a neighbor of our point
            if distance <= eps:
                p_neighbors.append(i)

        p_neighbors.remove(p)
        return p_neighbors

    # Finds all points which are epsilon reachable from point i (core point)
    def all_epsilon_reachable(data, columns, eps, min_samples, cluster, clustered_points, i, i_neighbors):
        print("Finding all epsilon reachable points from core point: ", i)
        # Add the core point to the cluster
        clustered_points[i] = cluster

        # For each point which is epsilon reachable from the core point (i)
        for p in i_neighbors:
            # If the point was marked as noisy, add it to the cluster
            if clustered_points[p] == -1:
                clustered_points[p] = cluster

            # If the point already belongs to a cluster, continue to the next point
            if clustered_points[p] >= 1:
                continue
            # If the point was unvisited, add it to the cluster and check if it is a core point
            else:
                clustered_points[p] = cluster
                p_neighbors = epsilon_neighbors(data, columns, eps, p)
                if len(p_neighbors) >= min_samples:
                    i_neighbors.extend(p_neighbors)
    """
    Use a list to output clusters, where indices are the data point and the values are labels:
    -1: noisy point
    0: a point which has been unvisited
    """
    clustered_points = [0]*len(data)

    # Counter to create unique cluster IDs
    cluster = 1

    # traverse through each data point in our data
    for i in range(len(data)):
        print("Point: ", i)

        # if the point has already been visited, continue to the next iteration
        if clustered_points[i] != 0:
            continue

        # Find the neighbors of point i
        i_neighbors = epsilon_neighbors(data, columns, eps, i)

        # if the number of neighbors of our point is greater than min_samples, it is a core point
        print(f"Number of neighbors for point {i}: {len(i_neighbors)}")
        if len(i_neighbors) >= min_samples:
            all_epsilon_reachable(
                data, columns, eps, min_samples, cluster, clustered_points, i, i_neighbors)
            print(f"Cluster {cluster} completed\n")
            cluster += 1

        # Otherwise it is a noisy point
        else:
            clustered_points[i] = -1

    return clustered_points


# DO NOT CHANGE THE FOLLOWING LINE
def kmedoids(data, k, distance, centers=None, n=None, eps=None):
    # DO NOT CHANGE THE PRECEDING LINE
    # This function has to return a list of k cluster centroids (data instances!)

    # Step 1: Set initial medoids as specified by the user or choose randomly
    if centers is None:
        centers = random.sample(data, k)
    curr_medoids = centers

    if DEBUG:
        print("Initial medoids:", curr_medoids)

    # Helper function to assign clusters as a dictionary (map)
    def assign_clusters(medoids):
        # Use medoids as dictionary keys
        clusters = {tuple(medoid): [] for medoid in medoids}
        for instance in data:
            # Find the nearest medoid for each instance
            min_dist = float('inf')
            closest_medoid = None
            for medoid in medoids:
                dist = distance(instance, medoid)
                if dist < min_dist:
                    min_dist = dist
                    # Store medoid as tuple for dictionary key compatibility
                    closest_medoid = tuple(medoid)
            clusters[closest_medoid].append(instance)
        return clusters

    # Helper function to calculate total clustering cost
    def calculate_total_cost(medoids, clusters):
        cost = 0
        for medoid in medoids:
            # Use tuple(medoid) as dictionary key
            for instance in clusters[tuple(medoid)]:
                cost += distance(instance, medoid)
        return cost

    # Step 2: Initial assignment based on provided centers
    clusters = assign_clusters(curr_medoids)
    cost = calculate_total_cost(curr_medoids, clusters)

    if DEBUG:
        print("Initial cost:", cost)
        print("Initial clusters:", clusters)

    # Step 3: While the cost of the clusters (or error E) is decreasing, do
    iteration = 0
    while iteration < (n or float('inf')):
        improved = False
        best_cost_reduction = 0
        best_medoid_idx = None
        best_candidate = None

        # Step 4: For each medoid m and each non-medoid data point p
        for i, medoid in enumerate(curr_medoids):
            for candidate in data:
                if tuple(candidate) == tuple(medoid):
                    continue

                # Swap medoid with candidate and compute new cost
                new_medoids = curr_medoids[:]
                new_medoids[i] = candidate
                new_clusters = assign_clusters(new_medoids)
                new_cost = calculate_total_cost(new_medoids, new_clusters)

                # Calculate the cost reduction
                cost_reduction = cost - new_cost

                # Track the best swap
                if cost_reduction > best_cost_reduction:
                    best_cost_reduction = cost_reduction
                    best_medoid_idx = i
                    best_candidate = candidate

        # Perform the best swap if it improves the cost
        if best_cost_reduction > (eps or 0):
            curr_medoids[best_medoid_idx] = best_candidate
            clusters = assign_clusters(curr_medoids)
            cost = calculate_total_cost(curr_medoids, clusters)
            improved = True

        iteration += 1

        # Terminate if no significant improvement was made
        if not improved:
            break

    if DEBUG:
        print("Final medoids:", curr_medoids)
        print("Final cost:", cost)
        print("Final clusters:", clusters)

    return curr_medoids

# Uncomment the following line for custom test cases
# TEST CASES


def main():
    # Test case 1
    data1 = [[1, 2], [2, 1], [4, 4], [5, 5]]

    # Test case 2
    data2 = [
        [2, 6],  # X1
        [3, 4],  # X2
        [3, 8],  # X3
        [4, 7],  # X4
        [6, 2],  # X5
        [6, 4],  # X6
        [7, 3],  # X7
        [7, 4],  # X8
        [8, 5],  # X9
        [7, 6]   # X10
    ]

    # Test case 3
    data3 = [
        [1, 2],  [2, 1],  [1, 1],   # Cluster 1
        [5, 5],  [6, 5],  [5, 6],   # Cluster 2
        [9, 8],  [8, 9],  [9, 9]    # Cluster 3
    ]

    # Test case 1 with fixed initial medoids
    k = 2
    kmedoids(data1, k, manhattan_distance, centers=[[1, 2], [4, 4]], n=1)
    print("Expected final medoids: [[1, 2], [4, 4]]")
    print('-' * 50)

    kmedoids(data1, k, manhattan_distance, centers=[[1, 2], [4, 4]])
    print("Expected final medoids: [[1, 2], [4, 4]]")
    print('-' * 50)

    # Test case 2 with fixed initial medoids
    k = 2
    kmedoids(data2, k, manhattan_distance, centers=[[3, 4], [6, 4]], n=1)
    print("Expected final medoids: [[3, 8], [6, 4]]")
    print('-' * 50)

    kmedoids(data2, k, manhattan_distance, centers=[[3, 4], [6, 4]])
    print("Expected final medoids: [[3, 8], [7, 4]]")
    print('-' * 50)

    # Test case 3 with random initial medoids
    k = 3
    kmedoids(data3, k, manhattan_distance,
             centers=[[1, 2], [5, 5], [9, 8]], n=1)
    print("Expected final medoids: [[1, 1], [5, 5], [9, 8]]")
    print('-' * 50)

    kmedoids(data3, k, manhattan_distance, centers=[[1, 2], [5, 5], [9, 8]])
    print("Expected final medoids: [[1, 1], [5, 5], [9, 9]]")
    print('-' * 50)


if __name__ == "__main__":
    main()
