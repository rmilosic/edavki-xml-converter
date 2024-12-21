# src/parser/degiro_parser.py
from .base_parser import BaseParser

import os
import pandas as pd

from src.transformer.dividends import add_eur_column

# Get the current working directory
current_directory = os.getcwd()


class DegiroParser(BaseParser):
    def parse_dividends(self, file_path, year):
       # transform columns
        df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"),
                        parse_dates=[0,2], date_format="%d-%m-%Y")
        # Convert columns at location 0 and 1 to datetime
        df = df[df.iloc[:,5] == "Dividenda"]
        
        
        df.sort_values(by="Datum", inplace=True)
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
        # labels mapping
        # Datum -> Date
        
        
        return df
    
    
    def parse_transactions(self, file_path, year):
        # transform columns
        df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"))
        df["Datum"] = pd.to_datetime(df["Datum"], dayfirst=True)
        
        # Convert columns at location 0 and 1 to datetime
        df.sort_values(by="Datum", inplace=True)
        
        df = add_eur_column(df)
        
        # labels mapping
        # Datum -> Date
        
        # Filter by year
        if year:
            df = df[df.iloc[:,0].dt.year <= year]

        
        return df
