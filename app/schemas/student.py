from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class StudentCreate(BaseModel):
    name: str = Field(..., examples=["John"])
    last_name: str = Field(..., examples=["Doe"])
    age: int = Field(..., examples=[20], ge=16, le=60)
    email: EmailStr = Field(..., examples=["studen@gmail.com"])
    city: str = Field(..., examples=["New York"])
    address: str = Field(..., examples=["Street 123"])
    phone: str = Field(..., examples=["1234567892"],
                       max_length=10, min_length=10)
    identification: str = Field(..., examples=[
                                "1234567891"], max_length=10, min_length=10)
    birthday: datetime = Field(..., examples=["1990-01-01"])


class StudentUpdate(BaseModel):
    name: str = Field(..., examples=["John"])
    last_name: str = Field(..., examples=["Doe"])
    email: EmailStr = Field(..., examples=["studen2@gmail.com"])
    city: str = Field(..., examples=["New York"])
    address: str = Field(..., examples=["Street 124"])
    phone: str = Field(..., examples=["123456789"],
                       max_length=10, min_length=10)
