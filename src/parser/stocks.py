import os
import pandas as pd
from src.transformer.stocks import add_eur_column

# Get the current working directory
current_directory = os.getcwd()

def calculate_value(row):
    if row.iloc[8] == 'EUR':
        return row.iloc[7]
    else:
        # Recalculate using another column and Column7
        return row['AnotherColumn'] * row['Column7']
    

def parse_degiro_transactions_data(file_path, year):

    # transform columns
    df = pd.read_csv(os.path.join(current_directory, f"data/{file_path}"),
                     parse_dates=[0])
    # Convert columns at location 0 and 1 to datetime
    df.sort_values(by="Datum", inplace=True)
    
    df = add_eur_column(df)
    # TODO: recalculate Price "Cena" based on currency
    # df[["Unnamed: 8", "Unnamed: 10"]] = df[["Unnamed: 8", "Unnamed: 10"]].astype("float")

    # Convert specified columns to datetime with the specified format
    # for col_loc in date_columns:
    #     df.iloc[:, col_loc] = pd.to_datetime(df.iloc[:, col_loc], format='%d-%m-%Y', dayfirst=True)  

    # Filter by year
    if year:
        df = df[df.iloc[:,0].dt.year <= year]

    
    # Return the DataFrame or relevant data based on your requirements
    return df

def get_sold_products(df, year):
    
    # Date is within tax year and "Počet" (number) is negative, indicating a sell
    df_new = df[(df.iloc[:, 0].dt.year == year) & (df.iloc[:,6] < 0) ]
    
    sold_products = df_new[["Produkt", "ISIN", "Reference"]].drop_duplicates()
    return sold_products


def get_historical_ticker_transactions(df, isin, tax_year):
    
    df_new = df[(df.iloc[:,0].dt.year <= tax_year) & (df.iloc[:,3] == isin)]
    return df_new
    
