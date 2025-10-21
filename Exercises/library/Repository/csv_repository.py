import pandas as pd
from pathlib import Path
from typing import List, Optional
from ..Model.book import Book

class CSV_Repository:
    
    books_dataframe: pd.DataFrame
    
    def __init__(self, csv_file: str = "books.csv"):
        self.csv_file = Path(csv_file)
        self.initialize()
    
    def initialize(self):
        """Initialize the CSV file with headers if it doesn't exist"""
        if not self.csv_file.exists():
            self.books_dataframe = pd.DataFrame(columns=['id', 'title', 'author', 'year', 'isbn'])
            self.save_to_csv()
        else:
            self.load_from_csv()
    
    def load_from_csv(self):
        """Load books from CSV file"""
        try:
            self.books_dataframe = pd.read_csv(self.csv_file)
            if not self.books_dataframe.empty and 'id' in self.books_dataframe.columns:
                self.books_dataframe['id'] = self.books_dataframe['id'].astype(int)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            self.books_dataframe = pd.DataFrame(columns=['id', 'title', 'author', 'year', 'isbn'])
    
    def save_to_csv(self):
        """Save books to CSV file"""
        if self.books_dataframe is not None:
            self.books_dataframe.to_csv(self.csv_file, index=False)
    
    def _get_next_id(self) -> int:
        """Get the next available ID"""
        if self.books_dataframe.empty or 'id' not in self.books_dataframe.columns:
            return 1
        return self.books_dataframe['id'].max() + 1 if not self.books_dataframe.empty else 1
    
    def get_all(self) -> List[Book]:
        """Get all books"""
        self.load_from_csv()
        if self.books_dataframe.empty:
            return []
        
        books = []
        for _, row in self.books_dataframe.iterrows():
            book_data = row.to_dict()
            books.append(Book(**book_data))
        return books
    
    def get(self, book_id: int) -> Optional[Book]:
        """Get a book by ID"""
        self.load_from_csv()
        if self.books_dataframe.empty:
            return None
        
        book_data = self.books_dataframe[self.books_dataframe['id'] == book_id]
        if book_data.empty:
            return None
        
        return Book(**book_data.iloc[0].to_dict())
    
    def add(self, book: Book) -> Book:
        """Add a new book"""
        self.load_from_csv()
        
        # Create new book with ID
        new_book = book.model_copy()
        new_book.id = self._get_next_id()
        
        # Convert to DataFrame and append
        new_book_df = pd.DataFrame([new_book.model_dump()])
        self.books_dataframe = pd.concat([self.books_dataframe, new_book_df], ignore_index=True)
        self.save_to_csv()
        
        return new_book
    
    def update(self, book_id: int, book: Book) -> Optional[Book]:
        """Update a book"""
        self.load_from_csv()
        
        if self.books_dataframe.empty or book_id not in self.books_dataframe['id'].values:
            return None
        
        # Update the book
        updated_book = book.model_copy()
        updated_book.id = book_id
        
        # Update in DataFrame
        mask = self.books_dataframe['id'] == book_id
        for column in ['title', 'author', 'year', 'isbn']:
            self.books_dataframe.loc[mask, column] = getattr(updated_book, column)
        
        self.save_to_csv()
        return updated_book
    
    def remove(self, book_id: int) -> bool:
        """Remove a book by ID"""
        self.load_from_csv()
        
        if self.books_dataframe.empty or book_id not in self.books_dataframe['id'].values:
            return False
        
        # Remove the book
        self.books_dataframe = self.books_dataframe[self.books_dataframe['id'] != book_id]
        self.save_to_csv()
        return True
    
    def get_books_statistics(self) -> dict:
        """Get statistics about the books collection using pandas"""
        self.load_from_csv()
        
        if self.books_dataframe.empty:
            return {"total_books": 0, "message": "No books in collection"}
        
        stats = {
            "total_books": len(self.books_dataframe),
            "authors_count": self.books_dataframe['author'].nunique(),
            "publication_years": {
                "oldest": int(self.books_dataframe['year'].min()),
                "newest": int(self.books_dataframe['year'].max()),
                "average": float(round(self.books_dataframe['year'].mean(), 1))
            },
            "books_per_author": self.books_dataframe['author'].value_counts().to_dict()
        }
        
        return stats