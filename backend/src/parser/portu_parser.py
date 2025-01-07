# src/parser/degiro_parser.py
from .base_parser import BaseParser

import os
import pandas as pd

from src.handlers.dividends import add_eur_column

# Get the current working directory
current_directory = os.getcwd()


class PortuParser(BaseParser):
    def parse_dividends(self, file_path, year):
       
        pass
    
    def parse_transactions(self, file_path, year):
        df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"),
                         decimal=",", sep=";")
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
            "Kusy / Pozice": "Count",
            "Symbol": "isin"
        }, inplace=True)

        return df
