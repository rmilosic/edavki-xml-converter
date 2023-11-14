import pandas as pd

def recalculate_column_using_currency_data(degiro_data, currency_data):
    # Assuming 'Amount' is the column in DeGiro data that needs to be recalculated
    # Assuming 'ExchangeRate' is the column in historical currency data

    # Merge DeGiro data with currency data based on a common column (e.g., 'Date')
    merged_data = pd.merge(degiro_data, currency_data[["Date", "USD"]], left_on='Datum.1', right_on="Date", how='left')

    # Recalculate the 'Amount' column using the 'ExchangeRate'
    merged_data['transaction_eur'] = merged_data['Unnamed: 8'] / merged_data['USD']

    return merged_data