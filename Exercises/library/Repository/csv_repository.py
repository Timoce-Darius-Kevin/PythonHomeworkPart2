import pandas
from ..Model.book import Book

class CSV_Repository:
    
    Books: list[Book]
    def __init__(self) -> None:
        pass
    
    def initialize(self):
        pass
    
    def get(self, book_id: int):
        pass
    
    def add(self, book: Book):
        pass
    
    def remove(self, book_id: int):
        pass
    
    def update(self, book_id: int, book: Book):
        pass
    
    def save_to_csv(self):
        pass
    
    def load_from_csv(self):
        pass