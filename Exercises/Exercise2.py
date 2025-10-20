'''
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


GET /api/people/1/

{
    "name": "Luke Skywalker", 
    "height": "172", 
    "mass": "77", 
    "hair_color": "blond", 
    "skin_color": "fair", 
    "eye_color": "blue", 
    "birth_year": "19BBY", 
    "gender": "male", 
    "homeworld": "https://swapi.dev/api/planets/1/", 
    "films": [
        "https://swapi.dev/api/films/1/", 
        "https://swapi.dev/api/films/2/", 
        "https://swapi.dev/api/films/3/", 
        "https://swapi.dev/api/films/6/"
    ], 
    "species": [], 
    "vehicles": [
        "https://swapi.dev/api/vehicles/14/", 
        "https://swapi.dev/api/vehicles/30/"
    ], 
    "starships": [
        "https://swapi.dev/api/starships/12/", 
        "https://swapi.dev/api/starships/22/"
    ], 
    "created": "2014-12-09T13:50:51.644000Z", 
    "edited": "2014-12-20T21:17:56.891000Z", 
    "url": "https://swapi.dev/api/people/1/"
}

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
''' 

import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import asyncio
import aiohttp
import uvicorn

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('solution_errors.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StarWarsAPIError(Exception):
    """Custom exception for Star Wars API related errors"""
    pass

class Person(BaseModel):
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    homeworld: str
    films: List[str]
    species: List[str]
    vehicles: List[str]
    starships: List[str]
    created: str
    edited: str
    url: str

class PersonResponse(BaseModel):
    name: str
    height: str
    mass: str
    hair_color: str

app = FastAPI(title="Star Wars Characters API", version="1.0.0")

URLS = (
    "https://swapi.dev/api/people/1",
    "https://swapi.dev/api/people/2", 
    "https://swapi.dev/api/people/3",
)

async def fetch_character_data(url: str, session: aiohttp.ClientSession) -> Optional[Person]:
    """
    Fetch character data from a single URL with error handling
    
    Parameters:
    - url: str - The URL to fetch data from
    - session: aiohttp.ClientSession - The aiohttp session to use for the request
    Returns:
    - Person object if successful, None otherwise
    """
    try:
        async with session.get(url) as response:
            if response.status != 200:
                logger.error(f"HTTP {response.status} for URL: {url}")
                raise StarWarsAPIError(f"HTTP {response.status} error for {url}")
            
            data = await response.json()
            
            if not data:
                logger.error(f"Empty response data from URL: {url}")
                raise StarWarsAPIError(f"Empty response from {url}")
            
            return Person(**data)
            
    except aiohttp.ClientError as e:
        logger.error(f"Network error fetching {url}: {str(e)}")
        raise StarWarsAPIError(f"Network error: {str(e)}")
    except ValidationError as e:
        logger.error(f"Data validation error for {url}: {str(e)}")
        raise StarWarsAPIError(f"Invalid data format: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {str(e)}")
        raise StarWarsAPIError(f"Unexpected error: {str(e)}")

async def solution() -> List[Person]:
    """
    Main solution function that aggregates responses from URLs and returns data sorted by height in descending order
    
    returns:
    - List of Person objects sorted by height descending
    """
    characters = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_character_data(url, session) for url in URLS]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                continue
            if result:
                characters.append(result)
    
    characters.sort(key=lambda x: int(x.height) if x.height.isdigit() else 0, reverse=True)
    
    return characters

def write_results_to_file(characters: List[Person], filename: str = "result.json"):
    """
    Write the results to a JSON file
    """
    try:
        character_dicts = [char.model_dump() for char in characters]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(character_dicts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Successfully wrote {len(characters)} characters to {filename}")
        
    except Exception as e:
        logger.error(f"Error writing to file {filename}: {str(e)}")
        raise

@app.get("/")
async def root():
    return {"message": "Star Wars Characters API", "version": "1.0.0"}

@app.get("/characters/", response_model=List[PersonResponse])
async def get_characters_sorted():
    """
    Get Star Wars characters sorted by height in descending order
    """
    try:
        characters = await solution()
        return [PersonResponse.model_validate(char.model_dump()) for char in characters]
    except Exception as e:
        logger.error(f"Error in get_characters_sorted: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/characters/full", response_model=List[Person])
async def get_characters_full():
    """
    Get full Star Wars characters data sorted by height in descending order
    """
    try:
        return await solution()
    except Exception as e:
        logger.error(f"Error in get_characters_full: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/characters/write-file")
async def write_characters_to_file():
    """
    Execute solution and write results to file
    """
    try:
        characters = await solution()
        write_results_to_file(characters)
        return {
            "message": f"Successfully processed {len(characters)} characters",
            "file": "result.json",
            "characters_count": len(characters)
        }
    except Exception as e:
        logger.error(f"Error in write_characters_to_file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def main():
        try:
            characters = await solution()
            write_results_to_file(characters)
            print(f"Successfully processed {len(characters)} characters")
            print("Results written to result.json")
            print("Errors logged to solution_errors.log")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    
    uvicorn.run(app, host="0.0.0.0", port=8000)