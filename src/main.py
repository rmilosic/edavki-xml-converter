import argparse
import os
import yaml

from src.parser import parse_degiro_account_data, parse_historical_currency_data
from src.transformer import recalculate_column_using_currency_data
from src.xml_builder import build_xml


def load_config(filename):    
    
    # Load configuration from YAML file
    with open(os.path.join(os.getcwd(), "config", filename), "r") as config_file:
        config = yaml.safe_load(config_file)
        return config


def main():
    
    parser = argparse.ArgumentParser(description="Parse Excel and build XML.")
    parser.add_argument("file_path", help="Path to the Degiro Account Statement file")
    parser.add_argument("--year", "-y", type=int, help="Year for which the report is")
    parser.add_argument("--config", "-c", type=str, default="config.yaml", help="Path to the configuration file")

    args = parser.parse_args()
    
    config = load_config(args.config)

    # Parse Excel
    degiro_data = parse_degiro_account_data(args.file_path, args.year)

    # Parse historical currency data
    currency_data = parse_historical_currency_data("eurofxref-hist.csv")

    # Recalculate a column in DeGiro account data using currency data
    recalculated_data = recalculate_column_using_currency_data(degiro_data, currency_data)

    # Build XML
    xml_data = build_xml(recalculated_data, args.year, config)

    with open(f"degiro_dividends_doh_div_v3_{args.year}.xml", "w", encoding="utf-8") as file:
        file.write(xml_data)
        
if __name__ == "__main__":
    main()