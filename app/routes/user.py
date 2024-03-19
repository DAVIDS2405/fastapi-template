from fastapi import APIRouter, Body, Depends
from controller.user import Login, Register_User
from schemas.user import UserLogin, UserRegister
from middleware.bearer import verify_token

router = APIRouter(tags=["user"])


@router.post("/login")
async def login(data: UserLogin = Body()):
    response = await Login(data)
    return response


@router.post("/user")
async def register(data: UserRegister):
    response = await Register_User(data)
    return response


@router.get("/user/{id}", dependencies=[Depends(verify_token)])
async def get_user_ud(id: str):
    return {"id": id}
