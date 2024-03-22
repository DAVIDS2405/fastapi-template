from pydantic import BaseModel, Field


class SubjectCreate(BaseModel):
    name: str = Field(examples=["Matemáticas"])
    code: str = Field(examples=["MAT-101"])
    description: str = Field(examples=["Matemáticas básicas"])
    credits: int = Field(examples=[4])


class SubjectUpdate(BaseModel):
    name: str = Field(examples=["Matemáticas"])
    code: str = Field(examples=["MAT-101"])
    description: str = Field(examples=["Matemáticas básicas"])
    credits: int = Field(examples=[4])
