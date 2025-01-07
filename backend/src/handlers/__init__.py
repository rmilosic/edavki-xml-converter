import pandas as pd

from src.parser.exchange_rate import parse_historical_currency_data

def add_eur_column(degiro_data):
    # Assuming 'Amount' is the column in DeGiro data that needs to be recalculated
    # Assuming 'ExchangeRate' is the column in historical currency data

    currency_data = parse_historical_currency_data("eurofxref-hist.csv")
    currency_data["Date"] = pd.to_datetime(currency_data["Date"])
    
    # Merge DeGiro data with currency data based on a common column (e.g., 'Date')
    merged_data = pd.merge_asof(degiro_data, currency_data, left_on='Date', right_on="Date")

    # Recalculate the 'Amount' column using the 'ExchangeRate'
    # merged_data['transaction_eur'] = merged_data['Unnamed: 8'] / merged_data['USD']
    merged_data['transaction_eur'] = merged_data.apply(recalculate_to_eur, axis=1)
    return merged_data

def recalculate_to_eur(row):
    if row["Currency"] == 'EUR':
        return row["Amount"]
    else:
        # dynamically divide the transaction/dividend amount by exchange rate for currency based on the currency of the transaction/dividend
        return row["Amount"]/row[row["Currency"]]
    

def get_parser(source):
    if source == 'degiro':
        from src.parser.degiro_parser import DegiroParser
        return DegiroParser()
    elif source == 'portu':
        from src.parser.portu_parser import PortuParser
        return PortuParser()
    else:
        raise ValueError("Unsupported source.")