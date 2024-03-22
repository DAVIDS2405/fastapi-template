from fastapi import APIRouter
from controller.subject import Get_All_Subjects, Get_Subject_id, Create_Subjects, Update_Subject, Delete_Subject
from schemas.subject import SubjectCreate, SubjectUpdate
router = APIRouter(tags=["Subject"])


@router.get("/subject")
async def get_subjects():
    response = await Get_All_Subjects()
    return response


@router.get("/subject/{id}")
async def get_subject_id(id: str):
    response = await Get_Subject_id(id)
    return response


@router.post("/subject")
async def create_subjects(data: SubjectCreate):
    response = await Create_Subjects(data)
    return response


@router.put("/subject/{id}")
async def update_subject(id: str, data: SubjectUpdate):
    response = await Update_Subject(id, data)
    return response


@router.delete("/subject/{id}")
async def delete_subject(id: str):
    response = await Delete_Subject(id)
    return response
