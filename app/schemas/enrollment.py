from pydantic import BaseModel, Field


class EnrollmentCreate(BaseModel):
    student_id: str = Field(examples=['47740c3f-7cb5-48c3-912e-9ad4a24bac9d'])
    subject_id: str = Field(examples=['def2c2d9-8284-4e9d-a69e-de1cd2733b34'])
    code: int = Field(examples=[1234])
    description: str = Field(examples=['Mathematics Inscription'])


class EnrollmentUpdate(BaseModel):
    student_id: str = Field(examples=['47740c3f-7cb5-48c3-912e-9ad4a24bac9d'])
    subject_id: str = Field(examples=['def2c2d9-8284-4e9d-a69e-de1cd2733b34'])
    code: int = Field(examples=[1234])
    description: str = Field(examples=['Social Inscription'])
