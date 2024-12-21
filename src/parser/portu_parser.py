# src/parser/degiro_parser.py
from .base_parser import BaseParser

import os
import pandas as pd

from src.transformer.dividends import add_eur_column

# Get the current working directory
current_directory = os.getcwd()


class PortuParser(BaseParser):
    def parse_dividends(self, file_path, year):
       
        pass
    
    def parse_transactions(self, file_path, year):
        
        pass
