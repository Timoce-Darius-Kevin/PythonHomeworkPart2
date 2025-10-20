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
from fastapi import FastAPI, Path
from pydantic import AfterValidator
from .Model.book import Book
app = FastAPI()

def check_valid_isbn(isbn: str):
    if not isbn.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return isbn

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/books")
async def get_all_books():
    return {"books": "This will get all the books"}


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: Annotated[int, Path(title="id of the needed book", gt=0)]):
    return {"book": "This will return book with id: {book_id}"}

@app.post("/books")
async def create_book(
    book: Annotated[Book, AfterValidator(check_valid_isbn)]):
    return book

@app.put("/books/{book_id}")
async def update_book(book_id: Annotated[int, Path(title="id of the needed book", gt=0)], book: Annotated[Book, AfterValidator(check_valid_isbn)]):
    return {"book_id": book_id, **book.model_dump()}

@app.delete("/book/{book_id}")
async def delete_book(book_id: int):
    return {"book_id": book_id}
    