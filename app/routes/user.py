from fastapi import APIRouter, Body, Depends, Request
from controller.user import Login, Register_User, Get_User_id
from schemas.user import UserLogin, UserRegister
from middleware.bearer import verify_token
from helper.jwt import verify_rol
router = APIRouter(tags=["user"])


@router.post("/login")
async def login(data: UserLogin = Body()):
    response = await Login(data)
    return response


@router.post("/register")
async def register(data: UserRegister):
    response = await Register_User(data)
    return response


@router.get("/user/{id}", dependencies=[Depends(verify_token)])
async def get_user_ud(id: str):
    response = await Get_User_id(id)
    return response


@router.get("/account", dependencies=[Depends(verify_token)])
async def get_account(request: Request):
    token = request.headers.get("authorization").split()[1]
    await verify_rol(token)
    response = {"message": "Tienes permisos para acceder a este recurso."}
    return response
