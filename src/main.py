import argparse
import os
import yaml

from src.parser.dividends import parse_degiro_account_data
from src.parser.stocks import parse_degiro_transactions_data, get_sold_products, get_historical_ticker_transactions
from src.parser.exchange_rate import parse_historical_currency_data
from src.transformer.dividends import add_eur_column
from src.transformer.stocks import add_fifo_data
from src.xml_builder.dividends import build_dividend_xml
from src.xml_builder.stocks import build_stock_xml

from collections import deque
import pandas as pd

def load_config(filename):    
    
    # Load configuration from YAML file
    with open(os.path.join(os.getcwd(), "config", filename), "r") as config_file:
        config = yaml.safe_load(config_file)
        return config


def main():
    
    parser = argparse.ArgumentParser(description="Parse Excel and build XML.")
    parser.add_argument('mode', choices=['dividend', 'stock', 'fifo'],
                        help='Specify the processing mode (dividend or stock).')
    parser.add_argument("file_path", help="Path to the Degiro Account Statement file")
    parser.add_argument("--year", "-y", type=int, help="Year for which the report is")
    parser.add_argument("--config", "-c", type=str, default="config.yaml", help="Path to the configuration file")
    parser.add_argument("--fifo_date", "-d", type=str, default="config.yaml", help="Path to the configuration file")
    args = parser.parse_args()
    
    # Use the selected mode
    
    config = load_config(args.config)
    if args.mode == 'dividend':
        process_dividends(args, config)
    elif args.mode == 'stock':
        process_stocks(args, config)
    elif args.mode == "fifo":
        process_fifo(args, config)
    else:
        print(f"Invalid mode: {args.mode}")
        
    
def process_dividends(args, config):
    
    # Parse Excel
    degiro_data = parse_degiro_account_data(args.file_path, args.year)

    # Recalculate a column in DeGiro account data using currency data

    # Build XML
    xml_data = build_dividend_xml(degiro_data, args.year, config)

    with open(f"degiro_dividends_doh_div_v3_{args.year}.xml", "w", encoding="utf-8") as file:
        file.write(xml_data)

def process_stocks(args, config):
    
    degiro_data = parse_degiro_transactions_data(args.file_path, args.year)

    # get all sold tickrs within tax year
    sold_products = get_sold_products(degiro_data, args.year
                                      )
    # Build XML
    xml_data = build_stock_xml(degiro_data, sold_products, args.year, config)

    with open(f"degiro_stocks_doh_kdvp_v9_{args.year}.xml", "w", encoding="utf-8") as file:
        file.write(xml_data)
    # for each sold tickr, build a popisni list
    # get all buys ands sells for tax year and before
    
   
    
    return degiro_data


def process_fifo(args, config):
    
    fifo_queue = deque()
    
    
    # Function to handle buying stocks
    def buy(quantity, price):
        fifo_queue.append((quantity, price))

    # Function to handle selling stocks and calculate profit/loss
    def sell(quantity, sale_price):
        total_cost = 0
        sold_quantity = quantity
        total_proceeds = quantity * sale_price
        while quantity > 0:
            oldest_stock = fifo_queue.popleft()
            available_qty, price = oldest_stock
            if quantity >= available_qty:
                total_cost += available_qty * price
                quantity -= available_qty
            else:
                total_cost += quantity * price
                fifo_queue.appendleft((available_qty - quantity, price))
                quantity = 0
                
        # Calculate profit/loss
        profit_or_loss = total_proceeds - total_cost
        return total_cost, total_proceeds, profit_or_loss
    # FIFO queue to hold purchased stocks
    
    degiro_data = parse_degiro_transactions_data(args.file_path, args.year)
    
    # TODO: proces each product separately 
    for product in degiro_data["Produkt"].drop_duplicates():
        
        # datum, produkt, isin, počet, price, fifo cost, proceeds, profit/loss
        sales_records = []
        product_data = degiro_data[degiro_data["Produkt"] == product]
        for index, row in product_data.iterrows():
            
            count = row["Počet"]
            price = row["Cena"]
            action = "buy" if count > 0 else "sell"
            if action == 'buy':
                buy(count, price)
            elif action == 'sell':
                total_cost, total_proceeds, profit_or_loss = sell(abs(count), price)
                sales_records.append((row["Datum"], row["Produkt"], row["ISIN"], row["Počet"], row["Cena"], total_cost, total_proceeds, profit_or_loss))
                print(f"Sold {count} shares:")
                print(f"  FIFO Cost: €{total_cost}")
                print(f"  Proceeds: €{total_proceeds}")
                print(f"  Profit/Loss: €{profit_or_loss}")

        
        fifo_sales = pd.DataFrame(columns=["Datum", "Produkt", "ISIN", "Počet", "Cena", "fifo cost", "proceeds", "profit/loss"], data=sales_records)
        fifo_sales.to_csv(f"degiro_fifo_{product}.csv", encoding='utf-8')
    
    
    
    return degiro_data
if __name__ == "__main__":
    main()