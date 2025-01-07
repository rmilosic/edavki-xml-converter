import argparse
import os
import yaml

# from src.parser.dividends import parse_degiro_account_data
# from src.parser.stocks import parse_degiro_transactions_data, get_sold_products, get_historical_ticker_transactions
# from src.parser.exchange_rate import parse_historical_currency_data
# from src.transformer.dividends import add_eur_column
# from src.transformer.stocks import add_fifo_data
from src.handlers import get_parser
from src.handlers.stocks import process_fifo
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


        

if __name__ == "__main__":
    main()