from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    student_id: str
    subject_id: str
    code: int
    description: str


class EnrollmentUpdate(BaseModel):
    student_id: str
    subject_id: str
    code: int
    description: str
