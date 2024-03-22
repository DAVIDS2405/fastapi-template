from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    last_name: str
    age: int
    email: str
    city: EmailStr
    address: str
    phone: str
    Identification: str
    birthday: str


class StudentUpdate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    city: str
    address: str
    phone: str
