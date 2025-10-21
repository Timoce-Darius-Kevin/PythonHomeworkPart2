from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1000, le=2024)
    isbn: str = Field(..., min_length=10, max_length=20)
    id: Optional[int] = None

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, field):
        if not any(prefix in field.lower() for prefix in ['isbn', '978', '979']):
            raise ValueError('ISBN should contain "isbn", "978", or "979"')
        return field