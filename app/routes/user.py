from fastapi import APIRouter, Body, Depends, Request
from controller.user import Check_Mail, Login, Recover_Password, Register_User, Get_User_id, Get_Account_Whit_Id, Delete_Account_Whit_Id, Update_Account_Whit_Id, Update_Password
from schemas.user import RecoverPass, RecoverPassEmail, UserLogin, UserRegister, UserUpdate
from middleware.bearer import verify_token
from helper.jwt import verify_rol
router = APIRouter(tags=["User"])


@router.post("/login")
async def login(data: UserLogin = Body()):
    response = await Login(data)
    return response


@router.post("/register")
async def register(data: UserRegister):
    response = await Register_User(data)
    return response


@router.get("/check-mail/{token}")
async def check_mail(token: str, request: Request):
    response = await Check_Mail(token, request)
    return response


@router.post("/recover-password")
async def recover_pass(data: RecoverPassEmail):
    response = await Recover_Password(data)
    return response


@router.post("/update-password")
async def update_password(data: RecoverPass):
    response = await Update_Password(data)
    return response


@router.get("/user/{id}", dependencies=[Depends(verify_token)])
async def get_user_ud(id: str, request: Request):
    token = request.headers.get("authorization").split()[1]
    await verify_rol(token)
    response = await Get_User_id(id)
    return response


@router.get("/account", dependencies=[Depends(verify_token)])
async def get_account(request: Request):
    token = request.headers.get("authorization").split()[1]
    token_validate = await verify_rol(token)
    response = await Get_Account_Whit_Id(token_validate)
    return response


@router.put("/user", dependencies=[Depends(verify_token)])
async def update_user(data: UserUpdate, request: Request):
    token = request.headers.get("authorization").split()[1]
    token_validate = await verify_rol(token)
    response = await Update_Account_Whit_Id(token_validate, data)
    return response


@router.delete("/user", dependencies=[Depends(verify_token)])
async def delete_user(request: Request):
    token = request.headers.get("authorization").split()[1]
    token_validate = await verify_rol(token)
    response = await Delete_Account_Whit_Id(token_validate)
    return response
