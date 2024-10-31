from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.decomposition import PCA
import clustering 
import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('cancer_data.csv')

# Take the first 400 rows for simplicity
df = df.head(400)

# Separate columns for encoding and normalization
numerical_cols = df.select_dtypes(include=[np.number]).columns
categorical_cols = ['race', 'sex', 'primary_diagnosis', 'primary_diagnosis_site', 'vital_status', 'treatment_type']

# Normalize numerical columns
scaler = MinMaxScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# One-hot encode the categorical columns
encoder = OneHotEncoder(sparse_output=False)
encoded_data = encoder.fit_transform(df[categorical_cols])
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out())

# Dimensionality Reduction with PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(encoded_data)
pca_result_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])

# Choose data for clustering
# Uncomment one of the following options based on your choice:
# data_for_clustering = encoded_df.values.tolist()  # Full one-hot encoded data
data_for_clustering = pca_result_df.values.tolist()  # Reduced PCA data

# Define Manhattan distance for clustering
def manhattan_distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

# Run kmedoids clustering
k = 3  # Number of clusters
medoids = clustering.kmedoids(data_for_clustering, k, distance=manhattan_distance, n=100, eps=1e-3)

# Print the medoids from PCA-reduced data
print("Cluster Medoids (using PCA-reduced data):")
for i, medoid in enumerate(medoids, 1):
    print(f"Medoid {i}: PC1={medoid[0]}, PC2={medoid[1]}")

# Function to find the closest row in the original dataset to each medoid
def find_closest_row(medoid, pca_result, original_df):
    min_dist = float('inf')
    closest_row = None
    for i, row in enumerate(pca_result):
        dist = manhattan_distance(medoid, row)
        if dist < min_dist:
            min_dist = dist
            closest_row = original_df.iloc[i]
    return closest_row

# Decode each medoid by finding the closest matching row in the original data
print("\nDecoded Medoids (closest original rows):")
for i, medoid in enumerate(medoids, 1):
    closest_row = find_closest_row(medoid, pca_result, df)
    print(f"Medoid {i}:")
    print(closest_row)
    print()
