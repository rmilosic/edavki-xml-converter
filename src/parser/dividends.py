import os
import pandas as pd

from src.transformer.dividends import add_eur_column

# Get the current working directory
current_directory = os.getcwd()


# Create the absolute path

def parse_degiro_account_data(file_path, year):

    # transform columns
    df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"),
                     parse_dates=[0,2])
    # Convert columns at location 0 and 1 to datetime
    df = df[df.iloc[:,5] == "Dividenda"]
    
    
    df.sort_values(by="Datum.1", inplace=True)
    df = add_eur_column(df)
    
    
    # df[["Unnamed: 8", "Unnamed: 10"]] = df[["Unnamed: 8", "Unnamed: 10"]].astype("float")

    # # Convert specified columns to datetime with the specified format
    # for col_loc in date_columns:
    #     df.iloc[:, col_loc] = pd.to_datetime(df.iloc[:, col_loc], format='%d-%m-%Y', dayfirst=True)  

    # Filter by year
    if year:
        df = df[df.iloc[:,2].dt.year == year]

    # Filter by event
    
    
    # Return the DataFrame or relevant data based on your requirements
    return df