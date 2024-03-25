from fastapi import APIRouter, Depends
from requests import Session
from database.database_neon import get_db
from schemas.student import StudentCreate, StudentUpdate
from controller.student import Get_All_Students, Get_Student_id, Create_Students, Update_Student, Delete_Student

router = APIRouter(tags=["Student"])


@router.get("/student")
async def get_students(session: Session = Depends(get_db)):
    response = await Get_All_Students(session)
    return response


@router.get("/student/{id}")
async def get_student_id(id: str, session: Session = Depends(get_db)):
    response = await Get_Student_id(id, session)
    return response


@router.post("/student")
async def create_students(data: StudentCreate, session: Session = Depends(get_db)):
    response = await Create_Students(data, session)
    return response


@router.put("/student/{id}")
async def update_student(id: str, data: StudentUpdate, session: Session = Depends(get_db)):
    response = await Update_Student(id, data, session)
    return response


@router.delete("/student/{id}")
async def delete_student(id: str, session: Session = Depends(get_db)):
    response = await Delete_Student(id, session)
    return response
