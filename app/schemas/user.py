from pydantic import BaseModel, SecretStr, Field, EmailStr


class UserLogin(BaseModel):
    email: str = Field(examples=["test@gmail.com"])
    password: SecretStr = Field(examples=["password"])


class UserRegister(BaseModel):
    name: str = Field(
        min_length=5,
        max_length=30,
        examples=["testuser"]
    )
    email: EmailStr = Field(
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


class UserUpdate(BaseModel):
    name: str = Field(
        min_length=5,
        max_length=30,
        examples=["testuser"]
    )

    email: EmailStr = Field(
        examples=["testupdate@gmail.com"]
    )


class RecoverPassEmail(BaseModel):
    email: EmailStr = Field(
        examples=["test@gmail.com"])


class RecoverPass(BaseModel):
    id: str = Field(
        examples=["681146a3-98ba-4685-882e-0ea3600592cd"])
    password: SecretStr = Field(examples=["password1"])
    confirm_password: SecretStr = Field(examples=["password1"])
