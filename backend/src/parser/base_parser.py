# src/parser/base_parser.py
from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def parse_dividends(self, file_path, year):
        pass
    
    @abstractmethod
    def parse_transactions(self, file_path, year):
        pass
