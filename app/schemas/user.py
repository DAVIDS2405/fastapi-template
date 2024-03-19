from pydantic import BaseModel, SecretStr, Field


class UserLogin(BaseModel):
    email: str = Field(examples=["test@gmail.com"])
    password: SecretStr = Field(examples=["password"])


class UserRegister(BaseModel):
    name: str = Field(
        min_length=5,
        max_length=30,
        examples=["testuser"]
    )
    email: str = Field(
        examples=["test@gmail.com"]
    )
    password: SecretStr = Field(
        min_length=8,
        max_length=16,
        examples=["password"]
    )
    age: str = Field(
        min_length=1,
        max_length=2,
        examples=["18"]
    )
