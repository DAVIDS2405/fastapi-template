from fastapi import APIRouter
from schemas.student import StudentCreate, StudentUpdate
from controller.student import Get_All_Students, Get_Student_id, Create_Students, Update_Student, Delete_Student

router = APIRouter(tags=["Student"])


@router.get("/student")
async def get_students():
    response = await Get_All_Students()
    return response


@router.get("/student/{id}")
async def get_student_id(id: str):
    response = await Get_Student_id(id)
    return response


@router.post("/student")
async def create_students(data: StudentCreate):
    response = await Create_Students(data)
    return response


@router.put("/student/{id}")
async def update_student(id: str, data: StudentUpdate):
    response = await Update_Student(id, data)
    return response


@router.delete("/student/{id}")
async def delete_student(id: str):
    response = await Delete_Student(id)
    return response
