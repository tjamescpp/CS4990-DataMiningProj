import pandas as pd

# Load the dataset
data = pd.read_csv('cancer_data.csv')

# This set of code help identify which demographic groups are most affected by a certain cancer
# Group by race, sex, and primary diagnosis then count occurrences
frequent_pairs_1 = data.groupby(['race', 'sex', 'primary_diagnosis']).size().reset_index(name='count')
# Sort by count to see the most frequent combinations
frequent_pairs_sorted_1 = frequent_pairs_1.sort_values(by='count', ascending=False).head(10)

# This set of code help identify which primary diagnosis conditions are most common for a certain cancer
# Group by primary diagnosis, primary diagnosis condition, and primary diagnosis site then count occurrences
frequent_pairs_2 = data.groupby(['primary_diagnosis', 'primary_diagnosis_condition', 'primary_diagnosis_site']).size().reset_index(name='count')
# Sort by count to see the most frequent combinations
frequent_pairs_sorted_2 = frequent_pairs_2.sort_values(by='count', ascending=False).head(10)

# This set of code help identify which treatment types are most common for a certain cancer
# Group by primary diagnosis, primary diagnosis site, and treatment type then count occurrences
frequent_pairs_3 = data.groupby(['primary_diagnosis', 'primary_diagnosis_site', 'treatment_type']).size().reset_index(name='count')
# Sort by count to see the most frequent combinations
frequent_pairs_sorted_3 = frequent_pairs_3.sort_values(by='count', ascending=False).head(10)

# Print the most frequent pairs
print(frequent_pairs_sorted_1)
print("-" * 70)
print(frequent_pairs_sorted_2)
print("-" * 70)
print(frequent_pairs_sorted_3)


