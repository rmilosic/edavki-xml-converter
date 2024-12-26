import os
import pandas as pd


# Get the current working directory
current_directory = os.getcwd()

def parse_historical_currency_data(file_path):
    
    # transform columns
    df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"),
                     parse_dates=[0])
    
    df.sort_values(inplace=True, by="Date")
       
    # Return the DataFrame or relevant data based on your requirements
    return df