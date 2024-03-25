from fastapi import APIRouter, Body, Depends, Request
from controller.user import Check_Mail, Login, Recover_Password, Register_User, Get_User_id, Get_Account_Whit_Id, Delete_Account_Whit_Id, Update_Account_Whit_Id, Update_Password
from schemas.user import RecoverPass, RecoverPassEmail, UserLogin, UserRegister, UserUpdate
from sqlalchemy.orm import Session
from database.database_neon import get_db
from middleware.bearer import verify_token
from helper.jwt import verify_rol
router = APIRouter(tags=["User"])


@router.post("/login")
async def login(data: UserLogin = Body(), session: Session = Depends(get_db)):
    response = await Login(data, session)
    return response


@router.post("/register")
async def register(data: UserRegister, session: Session = Depends(get_db)):
    response = await Register_User(data, session)
    return response


@router.get("/check-mail/{token}")
async def check_mail(token: str, request: Request, session: Session = Depends(get_db)):
    response = await Check_Mail(token, request, session)
    return response


@router.post("/recover-password")
async def recover_pass(data: RecoverPassEmail, session: Session = Depends(get_db)):
    response = await Recover_Password(data, session)
    return response


@router.post("/update-password")
async def update_password(data: RecoverPass, session: Session = Depends(get_db)):
    response = await Update_Password(data, session)
    return response


@router.get("/user/{id}", dependencies=[Depends(verify_token)])
async def get_user_ud(id: str, request: Request, session: Session = Depends(get_db)):
    token = request.headers.get("authorization").split()[1]
    await verify_rol(token)
    response = await Get_User_id(id, session)
    return response


@router.get("/account", dependencies=[Depends(verify_token)])
async def get_account(request: Request, session: Session = Depends(get_db)):
    token = request.headers.get("authorization").split()[1]
    token_validate = await verify_rol(token)
    response = await Get_Account_Whit_Id(token_validate, session)
    return response


@router.put("/user", dependencies=[Depends(verify_token)])
async def update_user(data: UserUpdate, request: Request, session: Session = Depends(get_db)):
    token = request.headers.get("authorization").split()[1]
    token_validate = await verify_rol(token)
    response = await Update_Account_Whit_Id(token_validate, data, session)
    return response


@router.delete("/user", dependencies=[Depends(verify_token)])
async def delete_user(request: Request, session: Session = Depends(get_db)):
    token = request.headers.get("authorization").split()[1]
    token_validate = await verify_rol(token)
    response = await Delete_Account_Whit_Id(token_validate, session)
    return response
