# src/parser/degiro_parser.py
from .base_parser import BaseParser

import os
import pandas as pd

from src.handlers import add_eur_column

# Get the current working directory
current_directory = os.getcwd()


class PortuParser(BaseParser):
    def parse_dividends(self, file_path, year):
       
        pass
    
    def parse_transactions(self, file_path, year):
        
        # if not portfolio:
        #     raise ValueError("Portfolio name is required for Portu data source")
        
        df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"),
                         decimal=",", sep=";", encoding="utf-8")
        df["Datum"] = pd.to_datetime(df["Datum"], dayfirst=True)
        # set dtypes for columns (Hodnota: float, Kusy / Pozice: float  )
        df["Hodnota"] = df["Hodnota"].str.replace(" ", "").str.replace(".", "").str.replace(",",".")
        df["Hodnota"] = df["Hodnota"].str.encode('ascii', 'ignore').str.decode('ascii').astype(float)
        # df["Kusy / Pozice"] = df["Kusy / Pozice"].str.replace(",", ".").str.replace(".", "").astype(float)
        # Convert columns at location 0 and 1 to datetime
        df.sort_values(by="Datum", inplace=True)
        
         # Filter by year
        if year:
            df = df[df.iloc[:,0].dt.year <= year]

        # concat columns nazev and popis with hyphen
        df["isin"] = df["Název"] + " - " + df["Symbol"]
        
        df.rename(columns={
            "Název": "Portfolio",
            "Datum": "Date",
            "Měna": "Currency",
            "Cena": "Amount",
            "Kusy / Pozice": "Count"
            # "Symbol": "isin"
        }, inplace=True)


        # df = df[df["Portfolio"] == portfolio]
        df = add_eur_column(df)
        
        return df
