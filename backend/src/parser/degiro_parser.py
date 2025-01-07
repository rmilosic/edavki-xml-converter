# src/parser/degiro_parser.py
from .base_parser import BaseParser

import os
import pandas as pd

from src.handlers import add_eur_column

# Get the current working directory
current_directory = os.getcwd()


class DegiroParser(BaseParser):
    def parse_dividends(self, file_path, year):
        # transform columns
        # Convert columns at location 0 and 1 to datetime
        df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"),
                        parse_dates=[0,2], date_format="%d-%m-%Y")
        
        # filter for Dividenda 
        df = df[df.iloc[:,5] == "Dividenda"]
        
        
        df.sort_values(by="Datum", inplace=True)
        
        # Filter by year
        if year:
            df = df[df.iloc[:,2].dt.year == year]

        # change column names
        # labels mapping
        # Datum -> Date
        # Change amount column title
        # Change currency column title
        
        df.rename(columns={
            "Datum": "Date",
            "Pohyb": "Currency",
            "Unnamed: 8": "Amount"
            }, inplace=True)

        df = add_eur_column(df)
               
        return df
    
    
    def parse_transactions(self, file_path, year):
        # transform columns
        df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"))
        df["Datum"] = pd.to_datetime(df["Datum"], dayfirst=True)
        
        # Convert columns at location 0 and 1 to datetime
        df.sort_values(by="Datum", inplace=True)
        
        
        
        # Filter by year
        if year:
            df = df[df.iloc[:,0].dt.year <= year]
            
        df.rename(columns={
            "Datum": "Date",
            "Unnamed: 8": "Currency",
            "Cena": "Amount",
            "Počet": "Count",
            "Produkt": "Product",
            "ISIN": "isin"
            }, inplace=True)

        df = add_eur_column(df)
        
        # labels mapping
        # Datum -> Date
        
        
        # Datum -> Date
        # Change amount column title
        # Change currency column title
        
        
        return df
