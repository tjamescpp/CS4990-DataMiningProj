from clustering import dbscan
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

cancer_data = pd.read_csv('cancer_pca_data.csv')

# Run algorithm on first 400 rows
cancer_data = cancer_data.iloc[:400, :]

columns = cancer_data.columns.tolist()

clusters = dbscan(cancer_data, columns, .5, 4)

score = silhouette_score(cancer_data, clusters)

print("Silhouette Score:", score)

cancer_data['Cluster'] = clusters

plt.figure(figsize=(10, 7))
sns.scatterplot(x=cancer_data.iloc[:, 0], y=cancer_data.iloc[:, 1], hue='Cluster', palette='viridis', data=cancer_data, legend='full')
plt.title("DBSCAN Cluster Visualization")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend(title="Cluster", loc="upper right")
plt.show()