import psycopg2
import pandas as pd

def fetch_data_from_db(query, host="localhost", database="tellcom", user="postgres", password="ofge"):
    """
    Connects to the PostgreSQL database and fetches data based on the provided query.

    Parameters:
    - query: SQL query to execute.
    - host: Database host (default is localhost).
    - database: Name of the database to connect to (default is tellcom).
    - user: Database user (default is postgres).
    - password: Password for the user (default is ofge).

    Returns:
    - Pandas DataFrame containing the result of the query.
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        
        # Query data and load into a DataFrame
        df = pd.read_sql(query, conn)
        
        # Close the connection
        conn.close()
        
        return df

    except psycopg2.DatabaseError as error:
        print(f"Error: {error}")
        return None

# # Example usage of the function
# query = "SELECT * FROM xdr_data;"  # Replace with your table name
# data = fetch_data_from_db(query)

# # Display the first few rows of the data
# if data is not None:
#     print(data.head())
