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


class SubjectResponse(BaseModel):
    id: str = Field(examples=["def2c2d9-8284-4e9d-a69e-de1cd2733b34"])
    name: str = Field(examples=["Matemáticas"])
    code: str = Field(examples=["MAT-101"])
    description: str = Field(examples=["Matemáticas básicas"])
    credits: int = Field(examples=[4])

    class Config:
        from_attributes = True
