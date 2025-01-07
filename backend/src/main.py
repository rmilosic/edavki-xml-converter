import argparse
import os
import yaml

# from src.parser.dividends import parse_degiro_account_data
# from src.parser.stocks import parse_degiro_transactions_data, get_sold_products, get_historical_ticker_transactions
# from src.parser.exchange_rate import parse_historical_currency_data
# from src.transformer.dividends import add_eur_column
# from src.transformer.stocks import add_fifo_data
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
    parser.add_argument(
        '--source', '-s',
        choices=['degiro', 'portu'],
        help='Specify the data source')
    parser.add_argument("--year", "-y", type=int, help="Year for which the report is")
    parser.add_argument("--config", "-c", type=str, default="config.yaml", help="Path to the configuration file")
    parser.add_argument("--fifo_date", "-d", type=str, default="config.yaml", required=False, help="Path to the configuration file")
    args = parser.parse_args()
    
    # Use the selected mode
    
    config = load_config(args.config)
    if args.mode == 'dividend':
        process_dividends(args, config)
    # elif args.mode == 'stock':
    #     process_stocks(args, config)
    elif args.mode == "fifo":
        process_fifo(args, config)
    else:
        print(f"Invalid mode: {args.mode}")

def get_parser(source):
    if source == 'degiro':
        from src.parser.degiro_parser import DegiroParser
        return DegiroParser()
    elif source == 'portu':
        from src.parser.portu_parser import PortuParser
        return PortuParser()
    else:
        raise ValueError("Unsupported source.")
    
def process_dividends(args, config):
    
    parser = get_parser(args.source)
    
    degiro_data = parser.parse_dividends(args.file_path, args.year)
    # xml_data = build_dividend_xml(degiro_data, args.year, config)
    
    # Parse Excel
    # degiro_data = parse_degiro_account_data(args.file_path, args.year)

    # Recalculate a column in DeGiro account data using currency data

    # Build XML
    xml_data = build_dividend_xml(degiro_data, args.year, config)

    # file directory
    dirpath = os.path.join(os.getcwd(), "output", str(args.source), "dividends", str(args.year))
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    with open(os.path.join(dirpath, f"degiro_dividends_doh_div_v3_{args.year}.xml"), "w", encoding="utf-8") as file:
        file.write(xml_data)

# def process_stocks(args, config):
    
#     degiro_data = parse_degiro_transactions_data(args.file_path, args.year)

#     # get all sold tickrs within tax year
#     sold_products = get_sold_products(degiro_data, args.year
#                                       )
#     # Build XML
#     xml_data = build_stock_xml(degiro_data, sold_products, args.year, config)

#     with open(f"degiro_stocks_doh_kdvp_v9_{args.year}.xml", "w", encoding="utf-8") as file:
#         file.write(xml_data)
#     # for each sold tickr, build a popisni list
#     # get all buys ands sells for tax year and before
    
   
    
#     return degiro_data


        

def process_fifo(args, config):
    
    fifo_queue = deque()
    fifo = 0
    
    
    source = args.source
    year = args.year
    
    # Function to handle buying stocks
    def buy(quantity, price, date):
        nonlocal fifo
        fifo = fifo + quantity
        fifo_queue.append((quantity, price, date, fifo))
        print("fifo", fifo)

    # Function to handle selling stocks and calculate profit/loss
    def sell(quantity, sale_price, sell_date):
        nonlocal fifo
        #TODO: upgrade to track which buy orders (price, quantity, ID were used for a sale)
        total_cost = 0
        total_proceeds = quantity * sale_price
        
        # sell table
        sell_table = pd.DataFrame(columns=["date", "date_sold", "sold_qty", "sold_price", "date_bought", "bought_qty", "bought_price", "fifo", "fifo_sold"])
        while quantity > 0:
            oldest_stock = fifo_queue.popleft()
            available_qty, buy_price, buy_date, fifo_at_buy = oldest_stock
            
            # add buy record
            sell_table.loc[len(sell_table)] = {
                "date": buy_date,
                "date_sold": pd.NA,
                "sold_qty": pd.NA,
                "sold_price": pd.NA,
                "date_bought": buy_date,
                "bought_qty": available_qty,
                "bought_price": buy_price,
                "fifo": fifo_at_buy,
                "fifo_sold": pd.NA
            }
            
            
            # add sell record
            
            
            # store pairing
            # date, sold stock, price, quantity
            # matched stocks date, stock, price, matched quantity 
            # sell_table.loc[len(sell_table)] = {
            #     "date": sell_date,
            #     "date_sold": sell_date,
            #     "sold_qty": quantity,
            #     "sold_price": sale_price,
            #     "date_bought": pd.NA,
            #     "bought_qty": pd.NA,
            #     "bought_price": pd.NA,
            #     "fifo": fifo
            # }
            
            

            if quantity >= available_qty:
                total_cost += available_qty * buy_price
                quantity -= available_qty
               
                fifo = fifo - available_qty
               
                sell_table.loc[len(sell_table)] = {
                "date": sell_date,
                "date_sold": sell_date,
                "sold_qty": available_qty,
                "sold_price": sale_price,
                "date_bought": pd.NA,
                "bought_qty": pd.NA,
                "bought_price": pd.NA,
                "fifo": fifo,
                "fifo_sold": fifo
            }
            else:
                total_cost += quantity * buy_price
                fifo_queue.appendleft((available_qty - quantity, buy_price, buy_date, fifo_at_buy))
                
                fifo = fifo - quantity
                
                sell_table.loc[len(sell_table)] = {
                "date": sell_date,
                "date_sold": sell_date,
                "sold_qty": quantity,
                "sold_price": sale_price,
                "date_bought": pd.NA,
                "bought_qty": pd.NA,
                "bought_price": pd.NA,
                "fifo": fifo,
                "fifo_sold": fifo
            }
                quantity = 0
                
        # Calculate profit/loss
        profit_or_loss = total_proceeds - total_cost
        return total_cost, total_proceeds, profit_or_loss, sell_table
    
    # FIFO queue to hold purchased stocks
    parser = get_parser(args.source)
    
    degiro_data = parser.parse_transactions(args.file_path, args.year)
    
    overall_sales_data = pd.DataFrame(columns=["isin", "date_sold", "sold_qty", "sold_price", "date_bought", "bought_qty", "bought_price", "fifo", "fifo_sold"])
    # TODO: proces each product separately 
    for isin in degiro_data["isin"].drop_duplicates():
        
        # datum, Product, isin, Count, price, fifo cost, proceeds, profit/loss
        # sales_records = []
        product_data = degiro_data[degiro_data["isin"] == isin]
        product_data.sort_values("Date", ascending=True, axis=0, inplace=True)
        
        sale_master_table = pd.DataFrame(columns=["date", "isin", "date_sold", "sold_qty", "sold_price", "date_bought", "bought_qty", "bought_price", "fifo", "fifo_sold"])
        
        
        fifo = 0
        for index, row in product_data.iterrows():
            
            
            
            count = row["Count"]
            price = row["Amount"]
            date = row["Date"]
            
            try:
                product = row["Product"]
            except KeyError:
                product = row["isin"]
            
            if source == 'degiro':
                action = "buy" if count > 0 else "sell"
            elif source == 'portu':
                action = "buy" if row["Hodnota"] < 0 else "sell"
            else:
                raise NotImplementedError
            
            if action == 'buy':
                buy(count, price, date)
            elif action == 'sell':
                
                    
                total_cost, total_proceeds, profit_or_loss, sell_table = sell(abs(count), price, date)
                
                sell_table["isin"] = row["isin"]
                
                if date.year == year:
                    sale_master_table = pd.concat([sale_master_table, sell_table], axis=0, ignore_index=True)
                    
                    
                    # sales_records.append((row["Date"], product, row["isin"], row["Count"], row["Amount"], total_cost, total_proceeds, profit_or_loss))
                    print(f"Sold {count} shares:")
                    print(f"  FIFO Cost: €{total_cost}")
                    print(f"  Proceeds: €{total_proceeds}")
                    print(f"  Profit/Loss: €{profit_or_loss}")
            
           
        sale_master_table.sort_values(["date", "fifo_sold"], axis=0, ascending=[True, False], inplace=True)
        sale_master_table.drop_duplicates(inplace=True, subset=["date_bought", "bought_price", "fifo"])
        overall_sales_data = pd.concat([overall_sales_data, sale_master_table], axis=0, ignore_index=True)
            
            
            
        # fifo_sales = pd.DataFrame(columns=["Datum", "Product", "isin", "Count", "Amount", "fifo cost", "proceeds", "profit/loss"], data=sales_records)
        # fifo_sales.to_csv(f"{source}_fifo_{product}.csv", encoding='utf-8')
        
        # file directory
        dirpath = os.path.join(os.getcwd(), "output", str(source), "stocks", str(year))
        
        if len(sale_master_table) > 0:
            
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            sale_master_table.to_csv(os.path.join(dirpath, f"{source}_fifo_detail_{product}.csv"), encoding='utf-8')
        
        if len(overall_sales_data) > 0:
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            overall_sales_data.to_csv(os.path.join(dirpath, f"{source}_overall.csv"), encoding='utf-8')
            
            # Build XML
            xml_data = build_stock_xml(overall_sales_data, args.year, config)

            with open(os.path.join(dirpath, f"degiro_stocks_doh_kdvp_v9_{args.year}.xml"), "w", encoding="utf-8") as file:
                file.write(xml_data)
                
    return degiro_data


if __name__ == "__main__":
    main()