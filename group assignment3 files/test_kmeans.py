from analysis import test_kmeans
import pandas as pd


def main():
    # Use 400 rows of data for testing
    data = pd.read_csv('cancer_pca_data.csv')
    test_data = data.iloc[:400]

    # Specifying the columns to use for clustering
    columns = ['PC1', 'PC2']
    k = 4
    test_kmeans(test_data, columns, k)


main()
