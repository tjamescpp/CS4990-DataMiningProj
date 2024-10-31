import random
import math

# Set DEBUG to True to print debug information
DEBUG = False

# # Uncomment the following lines for custom test cases
# # For custom test cases, the provided test cases use a different function for distance calculation
# def euclidean_distance(a, b):
#     return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

# def manhattan_distance(a, b):
#     return sum(abs(x - y) for x, y in zip(a, b))

# DO NOT CHANGE THE FOLLOWING LINE
def kmeans(data, k, columns, centers=None, n=None, eps=None):
# DO NOT CHANGE THE PRECEDING LINE
    # This function has to return a list of k cluster centers (lists of floats of the same length as columns)
    pass

# DO NOT CHANGE THE FOLLOWING LINE
def dbscan(data, columns, eps, min_samples):
# DO NOT CHANGE THE PRECEDING LINE
    # This function has to return a list of cluster centers (lists of floats of the same length as columns)
    pass
    
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

    # Because we will repeat the process until convergence, we need to define some helper functions
    # Helper function to assign clusters as a dictionary (map)
    def assign_clusters(medoids):
        clusters = {tuple(medoid): [] for medoid in medoids}  # Use medoids as dictionary keys
        for instance in data:
            # Find the nearest medoid for each instance
            min_dist = float('inf')
            closest_medoid = None
            for medoid in medoids:
                dist = distance(instance, medoid)
                if dist < min_dist:
                    min_dist = dist
                    closest_medoid = tuple(medoid)  # Store medoid as tuple for dictionary key compatibility
            clusters[closest_medoid].append(instance)
        return clusters
    
    # Helper function to calculate total clustering cost
    def calculate_total_cost(medoids, clusters):
        cost = 0
        for medoid in medoids:
            for instance in clusters[tuple(medoid)]:  # Use tuple(medoid) as dictionary key
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
            if DEBUG:
                print(f"Swapping medoid {curr_medoids[best_medoid_idx]} with candidate {best_candidate} improves cost from {cost} by {best_cost_reduction}")
            
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
        print("Iterations:", iteration)

    return curr_medoids

# # Uncomment the following line for custom test cases
# # TEST CASES
# def main():
#     # Test case 1
#     data1 = [[1, 2], [2, 1], [4, 4], [5, 5]]

#     # Test case 2
#     data2 = [
#         [2, 6],  # X1
#         [3, 4],  # X2
#         [3, 8],  # X3
#         [4, 7],  # X4
#         [6, 2],  # X5
#         [6, 4],  # X6
#         [7, 3],  # X7
#         [7, 4],  # X8
#         [8, 5],  # X9
#         [7, 6]   # X10
#     ]

#     # Test case 3
#     data3 = [
#     [1, 2],  [2, 1],  [1, 1],   # Cluster 1
#     [5, 5],  [6, 5],  [5, 6],   # Cluster 2
#     [9, 8],  [8, 9],  [9, 9]    # Cluster 3
#     ]

#     # Test case 1 with fixed initial medoids
#     k = 2
#     kmedoids(data1, k, manhattan_distance, centers=[[1, 2], [4, 4]], n=1)
#     print("Expected final medoids: [[1, 2], [4, 4]]")
#     print('-' * 50)

#     kmedoids(data1, k, manhattan_distance, centers=[[1, 2], [4, 4]])
#     print("Expected final medoids: [[1, 2], [4, 4]]")
#     print('-' * 50)

#     # Test case 2 with fixed initial medoids
#     k = 2
#     kmedoids(data2, k, manhattan_distance, centers=[[3, 4], [6, 4]], n=1)
#     print("Expected final medoids: [[3, 8], [6, 4]]")
#     print('-' * 50)

#     kmedoids(data2, k, manhattan_distance, centers=[[3, 4], [6, 4]])
#     print("Expected final medoids: [[3, 8], [7, 4]]")
#     print('-' * 50)

#     # Test case 3 with random initial medoids
#     k = 3
#     kmedoids(data3, k, manhattan_distance, centers=[[1, 2], [5, 5], [9, 8]], n=1)
#     print("Expected final medoids: [[1, 1], [5, 5], [9, 8]]")
#     print('-' * 50)

#     kmedoids(data3, k, manhattan_distance, centers=[[1, 2], [5, 5], [9, 8]])
#     print("Expected final medoids: [[1, 1], [5, 5], [9, 9]]")
#     print('-' * 50)

# if __name__ == "__main__":
#     main()







    







    



