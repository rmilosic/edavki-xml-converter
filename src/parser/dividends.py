import os
import pandas as pd

# Get the current working directory
current_directory = os.getcwd()


# Create the absolute path

def parse_degiro_account_data(file_path, year):

    # transform columns
    df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"),
                     parse_dates=[0,2])
    # Convert columns at location 0 and 1 to datetime
    date_columns = [0, 2]
    
    # df[["Unnamed: 8", "Unnamed: 10"]] = df[["Unnamed: 8", "Unnamed: 10"]].astype("float")

    # Convert specified columns to datetime with the specified format
    for col_loc in date_columns:
        df.iloc[:, col_loc] = pd.to_datetime(df.iloc[:, col_loc], format='%d-%m-%Y', dayfirst=True)  

    # Filter by year
    if year:
        df = df[df.iloc[:,2].dt.year == year]

    # Filter by event
    
    df = df[df["Popis"] == "Dividenda"]
    # Return the DataFrame or relevant data based on your requirements
    return df


def parse_historical_currency_data(file_path):
    
    # transform columns
    df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"),
                     parse_dates=[0])
       
    # Return the DataFrame or relevant data based on your requirements
    return df