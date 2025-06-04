import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler

from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
import numpy as np


def list_missing_values(df):
    """
    Finds missing values and returns a summary.

    Args:
        df: The DataFrame to check for missing values.

    Returns:
        A summary of missing values, including the number of missing values per column.
    """

    null_counts = df.isnull().sum()
    missing_value = null_counts
    percent_of_missing_value = 100 * null_counts / len(df)
    data_type=df.dtypes

    missing_data_summary = pd.concat([missing_value, percent_of_missing_value,data_type], axis=1)
    missing_data_summary_table = missing_data_summary.rename(columns={0:"Missing values", 1:"Percent of Total Values",2:"DataType" })
    missing_data_summary_table = missing_data_summary_table[missing_data_summary_table.iloc[:, 1] != 0].sort_values('Percent of Total Values', ascending=False).round(1)

    print(f"From {df.shape[1]} columns selected, there are {missing_data_summary_table.shape[0]} columns with missing values.")

    return missing_data_summary_table


def replace_missing_values(data):
    """
    Replaces missing values in a DataFrame with the mean for numeric columns and the mode for categorical columns.

    Args:
        data: The input DataFrame.

    Returns:
        The DataFrame with missing values replaced.
    """

    # Identify numeric and categorical columns
    numeric_columns = data.select_dtypes(include='number').columns
    categorical_columns = data.select_dtypes(include='object').columns

    # Replace missing values in numeric columns with the mean
    for column in numeric_columns:
        column_mean = data[column].mean()
        data[column] = data[column].fillna(column_mean)

    # Replace missing values in categorical columns with the mode
    for column in categorical_columns:
        column_mode = data[column].mode().iloc[0]
        data[column] = data[column].fillna(column_mode)

    return data


def convertByteIntoMegaByte(data):
    # We Have to convert some the data into MB or TB or GB
    megabyte=1*10e+5
    data['Bearer Id']=data['Bearer Id']/megabyte
    data['IMSI']=data['IMSI']/megabyte
    data['MSISDN/Number']=data['MSISDN/Number']/megabyte
    data['IMEI']=data['IMEI']/megabyte
    for column in data.columns:
        if 'Bytes' in column:
            data[column]=data[column]/megabyte
    return data


# Define a function to identify outliers using the IQR method
def get_outlier_summary(data):
    """
    Calculates outlier summary statistics for a DataFrame.

    Args:
        data : Input DataFrame.

    Returns:
        Outlier summary DataFrame.
    """

    outlier_summary = pd.DataFrame(columns=['Variable', 'Number of Outliers'])
    data = data.select_dtypes(include='number')

    for column_name in data.columns:
        q1 = data[column_name].quantile(0.25)
        q3 = data[column_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data[column_name] < lower_bound) | (data[column_name] > upper_bound)]

        outlier_summary = pd.concat(
            [outlier_summary, pd.DataFrame({'Variable': [column_name], 'Number of Outliers': [outliers.shape[0]]})],
            ignore_index=True
        )
    non_zero_count = (outlier_summary['Number of Outliers'] > 0).sum()
    print(f"From {data.shape[1]} selected numerical columns, there are {non_zero_count} columns with outlier values.")

    return outlier_summary

def remove_outliers(xdr_data):
    """
    Removes outliers from specified columns of a DataFrame using winsorization.

    Args:
        data: The input DataFrame.
        column_names (list): A list of column names to process.

    Returns:
        The DataFrame with outliers removed.
    """
    # data = xdr_data.select_dtypes(include='number')
    for column_name in xdr_data.select_dtypes(include='number').columns:
        q1 = xdr_data[column_name].quantile(0.25)
        q3 = xdr_data[column_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        xdr_data[column_name] = xdr_data[column_name].clip(lower_bound, upper_bound)

    return xdr_data


def visualize_outlies(df):
    # Select only the numerical columns
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns

    # Calculate the number of rows and columns for the subplot grid
    num_cols = 3  # Number of columns for subplots
    num_rows = (len(numerical_cols) + num_cols - 1) // num_cols  # Calculate number of rows needed

    plt.figure(figsize=(15, 5 * num_rows))  # Adjusting the figure size

    for i, col in enumerate(numerical_cols):
        plt.subplot(num_rows, num_cols, i + 1)  # Creating subplots
        sns.boxplot(x=df[col])  # Boxplot for each numerical column
        plt.title(f'Box plot for {col}')  # Title for each subplot

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()  # Display the plots
    
    

def user_aggregation(df_cleaned):
    user_aggregation = df_cleaned.groupby(['IMSI', 'MSISDN/Number']).agg(
        number_of_sessions=('Bearer Id', 'count'),
        total_session_duration=('Dur. (ms)', 'sum'),
        total_DL_data=('Total DL (Bytes)', 'sum'),
        total_UL_data=('Total UL (Bytes)', 'sum'),
        total_HTTP_DL_data=('HTTP DL (Bytes)', 'sum'),
        total_HTTP_UL_data=('HTTP UL (Bytes)', 'sum'),
        total_Social_Media_DL_data=('Social Media DL (Bytes)', 'sum'),
        total_Social_Media_UL_data=('Social Media UL (Bytes)', 'sum')
    ).reset_index()
    print(user_aggregation)
    
    
def seg_user_into_deciles(df_cleaned):
    # Create a new column for total data (DL + UL)
    df_cleaned['Total Data (Bytes)'] = df_cleaned['Total DL (Bytes)'] + df_cleaned['Total UL (Bytes)']

    # Calculate the decile classes based on the total session duration
    df_cleaned['Decile Class'] = pd.qcut(df_cleaned['Dur. (ms)'], 10, labels=False)  # 0-9 labels

    # Group by Decile Class to compute total data
    decile_summary = df_cleaned.groupby('Decile Class')['Total Data (Bytes)'].sum().reset_index()

    print("Total Data per Decile Class:")
    print(decile_summary)



