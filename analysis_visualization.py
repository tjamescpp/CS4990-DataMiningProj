# -*- coding: utf-8 -*-
"""
Author: Tommy James

Description: CS4490 Data Mining - Group Assignment #2

 4. Attribute Analysis and Visualization

Your data set should contain a number of different attributes. Pick the most relevant
ones (at least 3, with at least one numerical and one categorical; do not use IDs), and
for each of them:

- Describe the range of valid values (in the sample, and - if appropriate - in the population), and their distribution (summary statistics) in an appropriate form
- Visualize the attribute values in an appropriate form
- Note anything interesting, unusual and/or unexpected that you notice about the data

Where appropriate, you can visualize multiple attributes in a single graph. You can also
provide the summary statistics in a table, if that makes it more readable.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('cancer_data.csv')
print(df.head())

print(df.info())

# Age

"""
note: age_at_diagnosis is the age in days of the individual at the time of diagnosis, 
so we have to divide by 365 to get an estimate of the age in years
"""

# convert the entire column of 'age_at_diagnosis' from days to years
df2 = pd.DataFrame
df2 = df2.copy(df)
df2['age_at_diagnosis'] = df2['age_at_diagnosis'] / 365
df2['age_at_diagnosis'] = df2['age_at_diagnosis'].astype(int)
df2.head()

# summary statistics
print(df2['age_at_diagnosis'].describe())

sns.catplot(data=df2, x='age_at_diagnosis', kind='box', height=6, aspect=1.5)
plt.title('Distribution of Age at Diagnosis')

"""
# Note: there are outliers at younger ages below 
# approxiamtely 18 years old
"""

sns.catplot(data=df2, x='sex', y='age_at_diagnosis', kind='bar',
            hue='primary_diagnosis_site', height=6, aspect=1.5)
plt.title('Average Age per Sex\n(for each Diagnosis Site)')

"""
Notes:
- Males and Females with Brain cancer are diagnosed at a younger 
age on average compared to others
- Average age for most diagnosis are in the 50s
"""

# Primary Diagnosis Site

print(df2['primary_diagnosis_site'].value_counts())

sns.displot(data=df2, x='primary_diagnosis_site',
            height=6, aspect=1.5, shrink=0.8)
plt.title('Primary Diagnosis Site')

# visualize the distribution of primary diagnosis site for each sex
sns.displot(data=df2, x='primary_diagnosis_site', hue='sex',
            multiple='dodge', height=6, aspect=1.5, shrink=0.8)
plt.title('Primary Diagnosis Site per Sex')

"""
Note: More males have Brain or Kidney cancer. 
Of course, only females have Ovary cancer, but some males 
also have Breast cancer.
"""

male_breast_cancer = df2.loc[(
    df2['primary_diagnosis_site'] == 'Breast') & (df['sex'] == 'male')]
print(f'Number of males with breast cancer: {len(male_breast_cancer)}')
# There are 48 males with Breast cancer

# visualize the distribution of primary diagnosis site for each vital status
sns.displot(data=df2, x='primary_diagnosis_site', hue='vital_status',
            multiple='dodge', height=6, aspect=1.5, shrink=0.8)
plt.title('Primary Diagnosis Site per Vital Status')

"""
Note: 
- More patients died from Brain and Ovary cancer than survived. 
- More patients survived from Kidney and Breast cancer than died.
"""

# Vital Status

sns.displot(data=df2, x='vital_status', height=6, aspect=1.5, shrink=0.8)

"""
Note: there are more survivors than non-surviviors
"""

sns.displot(data=df2, x='vital_status', hue='primary_diagnosis_site',
            multiple='dodge', height=6, aspect=1.5, shrink=0.8)
plt.title('Vital Status per Primary Condition Site')

"""
Note:
- The primary diagnosis site with the most deaths is Brain
- The primary diagnosis site with the most survivors is Breast
"""

sns.catplot(data=df2, x='vital_status', y='age_at_diagnosis',
            hue='primary_diagnosis_site', kind='bar', height=6, aspect=1.5)
plt.title('Average Age per Vital Status\n(for each Primary Diagnosis Site)')

plt.show()
