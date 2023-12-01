import pandas as pd

from src.parser.exchange_rate import parse_historical_currency_data

def add_eur_column(degiro_data):
    # Assuming 'Amount' is the column in DeGiro data that needs to be recalculated
    # Assuming 'ExchangeRate' is the column in historical currency data

    currency_data = parse_historical_currency_data("eurofxref-hist.csv")
    
    # Merge DeGiro data with currency data based on a common column (e.g., 'Date')
    merged_data = pd.merge_asof(degiro_data, currency_data, left_on='Datum', right_on="Date")

    # Recalculate the 'Amount' column using the 'ExchangeRate'
    # merged_data['transaction_eur'] = merged_data['Unnamed: 8'] / merged_data['USD']
    merged_data['transaction_eur'] = merged_data.apply(recalculate_to_eur, axis=1)


    return merged_data


def add_fifo_data(degiro_data, date):
    
    
    # reinitialize left quantity with initial
    degiro_data["left"] = degiro_data["Počet"]
    
    degiro_data["left_on"] = date
    
    # todo, for each position calculate left of order on given date
    # get sell row indexes, rows
    # for each sell, filter all previous buys where left >0
    # 
    
    return degiro_data

def recalculate_to_eur(row):
    if row.iloc[8] == 'EUR':
        return row.iloc[7]
    else:
        # divide by currency 
        return row.iloc[7]/row[row.iloc[8]]