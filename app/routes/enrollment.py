from fastapi import APIRouter


router = APIRouter(tags=["Enrollment"])


@router.get("/enrollment")
async def get_enrollments():
    return {"message": "Get Enrollment"}


@router.get("/enrollment/{id}")
async def get_enrollment_id(id: int):
    return {"message": f"Get Enrollment {id}"}


@router.post("/enrollment")
async def create_enrollments():
    return {"message": "Post Enrollment"}


@router.put("/enrollment")
async def update_enrollment():
    return {"message": "Put Enrollment"}


@router.delete("/enrollment")
async def delete_enrollment():
    return {"message": "Delete Enrollment"}
