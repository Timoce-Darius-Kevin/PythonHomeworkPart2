"""
Exercise 1

Using pandas, determine the following for the sales.csv data:
The total revenue for each product (quantity  x price_per_unit).
The total cost for each product (quantity  x cost_per_unit).
The profit for each product (total revenue - total cost).
Finally, find the most profitable product overall.

------------------------------------------------------------------------

Exercise 2

Create a function solution() that aggregates the responses from the following URLs within a list.
Your function should return the data, sorted by height, in descending order.
(ATTENTION: height is of type str). Make sure you have some minimal sanity checks (e.g. status_code, empty data).

You only need to fetch the data from the first 3 URLs. That is:

URLS = (
    "https://swapi.dev/api/people/1",
    "https://swapi.dev/api/people/2",
    "https://swapi.dev/api/people/3",
)
NOTE:

URLS_TEMPLATE = "https://swapi.dev/api/people/{}"
Create a custom exception class. Handle an exception (at your choice) that the requests module
might raise in the function you have just created. Raise the newly created exception.

Write the final result to a result.json file and log the exceptions in solution_errors.log.

Pay attention to:
Naming conventions (or really, any PEP8 conventions, in general);
Scalability of your code (what if we want to extend the functionality by getting the data from
all the available URLs / or create unit tests etc);
Runtime complexity.
Resources
requests | already installed
Exceptions
JSON

------------------------------------------------------------------------

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
"""
