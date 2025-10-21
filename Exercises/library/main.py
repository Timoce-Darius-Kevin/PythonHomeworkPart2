'''
Exercise 3

Review the FastAPI tutorial (https://fastapi.tiangolo.com/tutorial/) carefully and use it to build a simple REST API for managing a collection of books in a library.

Endpoints requirements.
- Create a book
    Endpoint: POST /books/
    Request body:
    {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "year": 1999,
        "isbn": "978-0201616224"
    }
    Response: Return the created book with a unique ID.
- Read all books
    Endpoint: GET /books/
    Response: List all stored books.
- Read a single book by ID
    Endpoint: GET /books/{book_id}
    Response: Return the book with that ID or an error if not found.
- Update a book
    Endpoint: PUT /books/{book_id}
    Request body: Same as creation.
    Response: Return the updated book.
- Delete a book
    Endpoint: DELETE /books/{book_id}
    Response: Confirm deletion.

Moreover, find a way to integrate the requests and pandas libraries into your solution. Use your creativity.
'''
from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, status
from pydantic import AfterValidator
from .Model.book import Book
from .Repository.csv_repository import CSV_Repository
app = FastAPI()

book_repository = CSV_Repository()

def check_valid_isbn(isbn: str):
    if not isbn.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return isbn

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/books", response_model=list[Book])
async def get_all_books() -> list[Book]:
    '''
        ### Retrieves all books from the csv.
    '''
    return book_repository.get_all()


@app.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: Annotated[int, Path(title="id of the needed book", gt=0)]) -> Book:
    '''
        ### Get one book by it's ID
        
        *params*:
            - book_id: an integer representing a unique instance of a book
        
        *returns*:
            - book: the book according to it's unique id
            - HTTPException: if no book has been found
    '''
    
    book = book_repository.get(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
            )
    return book

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: Annotated[Book, AfterValidator(check_valid_isbn)]) -> Book:
    '''
        ### Create a new instance of type Book and add it to the CSV repository
        
        *params*: 
        - book: an object of type Book
        *returns*:
        - book the created object
    '''
    try:
        created_book = book_repository.add(book)
        return created_book
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating book: {str(e)}"
        )

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: Annotated[int, Path(title="id of the needed book", gt=0)], book: Annotated[Book, AfterValidator(check_valid_isbn)]) -> Book:
    """
    ### Updates a book found by it's book_id
    
    *params*:
    - book_id: the id of the book which needs to be updated
    - book: the new details of the book
    
    *returns*:
    - updated_book: the book with the same id but changed details
    """
    updated_book = book_repository.update(book_id, book)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} was not found when trying to update it"
        )
    return updated_book

@app.delete("/book/{book_id}")
async def delete_book(book_id: int):
    """
    ### deletes a book form csv
    
    *params*:
    - book_id: the id of the book that needs to be deleted
    """
    
    success = book_repository.remove(book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} was not found when trying to update it"
        )
    return {"message": f"book with ID {book_id} deleted succesfully"}
    