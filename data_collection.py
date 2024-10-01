# Project: CS4990 Data Mining Group-Assignment 1
# Authors: Tommy James, C.Fortino Flores, Iker Goni, Khoi Tran

"""
Working with cancer data

The cdapython library is a Python client for the Cancer Data Aggregator (CDA) API. 
It provides a simple interface to query the CDA API using Python.

documentation: https://cda.readthedocs.io/en/latest/documentation/cdapython/man_pages/

install cdapython library: pip install git+https://github.com/CancerDataAggregator/cdapython.git
python3
"""

import pandas as pd
import numpy as np
from cdapython import tables, columns, column_values, fetch_rows, summary_counts


def get_dataset(filename, rows=None):

    # join two tables: 'subject' and 'diagnosis'
    subject_diagnosis = fetch_rows(table='subject', link_to_table='diagnosis')

    # join tabels 'subject' and 'researchsubject'
    subject_researchsubject = fetch_rows(
        table='subject', link_to_table='researchsubject')

    # merge the previous two tables to get tables 'subject', 'diagnosis', and 'researchsubject'
    # Inner Join on 'patient_id'
    inner_join = pd.merge(
        subject_diagnosis, subject_researchsubject, on='subject_id', how='inner')

    # join tables 'subject' and 'treatment'
    subject_treatment = fetch_rows(table='subject', link_to_table='treatment')

    # final table with all tables joined
    final_join = pd.merge(inner_join, subject_treatment,
                          on='subject_id', how='inner')

    # filter dataframe from primary condition sites: 'Breast', 'Ovary', 'Brain', 'Kidney'
    values_to_filter = ['Breast', 'Ovary', 'Brain', 'Kidney']

    # filter 'primary_diagnosis_site' based on filter values
    df_filtered = final_join[final_join['primary_diagnosis_site'].isin(
        values_to_filter)]

    # drop columns with a lot of null values
    df_filtered = df_filtered.drop(columns=['days_to_death_x', 'days_to_death_y', 'days_to_death',
                                   'days_to_treatment_end', 'days_to_treatment_start', 'number_of_cycles'])

    # List of columns to keep
    columns_to_keep = ['subject_id', 'race_x', 'sex_x', 'age_at_diagnosis', 'morphology', 'primary_diagnosis',
                       'primary_diagnosis_condition', 'primary_diagnosis_site', 'vital_status', 'treatment_type']

    # Drop all columns except the ones in columns_to_keep
    df_filtered2 = df_filtered.drop(
        columns=df_filtered.columns.difference(columns_to_keep))

    # drop all rows that have at least 1 null value
    df_cleaned = df_filtered2.dropna()

    # drop rows containing at least one '<NA>'
    value_to_drop = '<NA>'
    df_cleaned2 = df_cleaned[~df_cleaned.isin([value_to_drop]).any(axis=1)]
    df_cleaned2.drop_duplicates(inplace=True)

    # rename columns
    df_cleaned2.rename(
        columns={'race_x': 'race', 'sex_x': 'sex'}, inplace=True)
    print(df_cleaned2.info())

    # print unique values from each column
    for column in df_cleaned2.columns:
        unique_values = df_cleaned2[column].unique()
        print(f"Unique values for column '{column}': {unique_values}")

    # write to csv file
    if rows == None:
        df_cleaned2.to_csv(f'{filename}.csv', index=False)
    else:
        df_cleaned2[:rows].to_csv(f'{filename}.csv', index=False)

    return


def main():
    filename = input("Enter filename: ")
    rows = int(input('Enter number of rows (Press 0 for all): '))

    if rows != 0:
        get_dataset(filename, rows)
    else:
        get_dataset(filename)

    cancer_data = pd.read_csv(f'{filename}.csv')
    print(f'\nHead of Dataset: {cancer_data.head()}')


main()
