from fastapi import APIRouter


router = APIRouter(tags=["Student"])


@router.get("/student")
async def get_students():
    return {"message": "Get Student"}


@router.get("/student/{id}")
async def get_student_id(id: int):
    return {"message": f"Get Student {id}"}


@router.post("/student")
async def create_students():
    return {"message": "Post Student"}


@router.put("/student")
async def update_student():
    return {"message": "Put Student"}


@router.delete("/student")
async def delete_student():
    return {"message": "Delete Student"}
