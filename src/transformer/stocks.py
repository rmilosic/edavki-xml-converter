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
    
    degiro_data = degiro_data.sort_values(by=['ISIN', 'Datum'])
    
    # reinitialize left quantity with initial
    degiro_data["left"] = degiro_data["Počet"]
    
    degiro_data["left_on"] = date
    
    # todo, for each position calculate left of order on given date
    # get sell row indexes, rows
    # for each sell, filter all previous buys where left >0
    # 
    # Iterate through each unique stock
    for stock in degiro_data['ISIN'].unique():
        stock_df = degiro_data[degiro_data['ISIN'] == stock].copy()


        # Calculate FIFO for each stock
        for sell_index, sell_row in stock_df.iterrows():
            # IF SELL
            if sell_row['left'] < 0:
                # quantity does not update
                # cumulative_cost = 0

                # Deduct remaining quantity from corresponding buy transactions
                for buy_index, buy_row in stock_df.iterrows():
                    # if sell greater than buy 
                    if abs(sell_row['left']) > buy_row['left']:
                        # anull buy, deduct buy from sell, go to next buy
                        stock_df.at[sell_index, "left"] = sell_row['left'] + buy_row['left'] 
                        stock_df.at[buy_index, "left"] = 0
                        continue
                   
                   
                    # if sell = buy
                    if sell_row['left'] == buy_row['left']:
                        # anull buy, deduct buy from sell, go to next sell
                        stock_df.at[sell_index, "left"] = 0
                        stock_df.at[buy_index, "left"] = 0
                        continue
                    
                    # if sell smaller than buy
                    if abs(sell_row['left']) < buy_row['left']:
                        # deduct sell from buy, anull sell, go to next sell
                        stock_df.at[buy_index, "left"] = buy_row['left'] + sell_row['left']
                        stock_df.at[sell_index, "left"] = 0
                        continue
                    
                
    return degiro_data

def recalculate_to_eur(row):
    if row.iloc[8] == 'EUR':
        return row.iloc[7]
    else:
        # divide by currency 
        return row.iloc[7]/row[row.iloc[8]]