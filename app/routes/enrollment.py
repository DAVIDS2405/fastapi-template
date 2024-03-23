from fastapi import APIRouter
from schemas.enrollment import EnrollmentCreate, EnrollmentUpdate
from controller.enrollment import Get_All_Enrollments, Get_Enrollment_id, Create_Enrollments, Update_Enrollment, Delete_Enrollment

router = APIRouter(tags=["Enrollment"])


@router.get("/enrollment")
async def get_enrollments():
    response = await Get_All_Enrollments()
    return response


@router.get("/enrollment/{id}")
async def get_enrollment_id(id: str):
    response = await Get_Enrollment_id(id)
    return response


@router.post("/enrollment")
async def create_enrollments(data: EnrollmentCreate):
    response = await Create_Enrollments(data)
    return response


@router.put("/enrollment/{id}")
async def update_enrollment(id: str, data: EnrollmentUpdate):
    response = await Update_Enrollment(id, data)
    return response


@router.delete("/enrollment/{id}")
async def delete_enrollment(id: str):
    response = await Delete_Enrollment(id)
    return response
