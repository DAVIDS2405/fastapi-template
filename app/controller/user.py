from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates

from database.database_neon import conn
from models.tables import users
from helper.jwt import create_token
from bcrypt import checkpw, hashpw, gensalt
from config.smtp import send_email, send_email_reset_password
from datetime import datetime
import secrets
import string

templates = Jinja2Templates(directory="app/templates/")


async def Register_User(data):
    users_db = conn.execute(users.select().where(
        users.c.email == data.email)).first()

    if users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este correo ya está registrado."
        )

    encode_password = data.password.get_secret_value().encode('utf-8')

    salt = gensalt(10)

    password = hashpw(encode_password, salt)

    token = string.ascii_letters + string.digits

    token = ''.join(secrets.choice(token) for i in range(36))

    data = data.dict()

    data.update({"password": password.decode('utf-8')})
    data.update({"token": token})
    data.update({"email_verified": False})
    data.update({"age": int(data["age"])})

    year = datetime.now().year
    email = send_email(data["name"], year, data["token"])

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Algo fallo intenta de nuevo"
        )

    conn.execute(users.insert().values(data))

    conn.commit()

    raise HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="Usuario registrado correctamente."
    )


async def Check_Mail(token: str, request):
    users_db = conn.execute(users.select().where(
        users.c.token == token)).first()

    if not users_db:
        return templates.TemplateResponse(
            "400.html", {"request": request, "success": False}, status_code=status.HTTP_400_BAD_REQUEST)

    conn.execute(users.update().where(users.c.token == token).values(
        {"token": None, "email_verified": True}))

    conn.commit()

    return templates.TemplateResponse(
        "email-verified.html", {"request": request, "success": True})


async def Recover_Password(data):
    users_db = conn.execute(users.select().where(
        users.c.email == data.email)).first()

    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este correo registrado."
        )

    if not users_db.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya solicitaste un cambio de contraseña."
        )

    conn.execute(users.update().where(users.c.email ==
                 data.email).values({"email_verified": False}))
    conn.commit()

    year = datetime.now().year
    email = send_email_reset_password(users_db.name, year, str(users_db.id))

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Algo fallo intenta de nuevo"
        )

    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="Revisa tu correo electrónico."
    )


async def Update_Password(data):
    users_db = conn.execute(users.select().where(
        users.c.id == data.id)).first()

    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe este usuario."
        )

    if users_db.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya cambiaste has cambiado tu contraseña no lo puedes hacer de nuevo"
        )

    password = data.password.get_secret_value().encode('utf-8')
    confirm_password = data.confirm_password.get_secret_value().encode('utf-8')

    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden."
        )

    salt = gensalt(10)

    password = hashpw(password, salt)

    conn.execute(users.update().where(users.c.id == data.id).values(
        {"password": password.decode('utf-8'), "email_verified": True}))

    conn.commit()

    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="Contraseña actualizada correctamente."
    )


async def Login(data):
    users_db = conn.execute(users.select().where(
        users.c.email == data.email)).first()

    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este correo registrado."
        )
    if not users_db.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo no verificado."
        )

    if not checkpw(data.password.get_secret_value().encode(), users_db.password.encode()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta."
        )

    user_db_data = users_db._asdict()

    user_db_data.update({"token": str(create_token(users_db.id))})

    user_db_data.update({"id": str(users_db.id)})

    user_db_data.pop("password")

    user_db_data.pop("email_verified")

    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail=user_db_data
    )


async def Get_User_id(id: str):
    users_db = conn.execute(users.select().where(
        users.c.id == id)).first()

    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este usuario."
        )

    user_db_data = users_db._asdict()

    user_db_data.update({"id": str(users_db.id)})

    user_db_data.pop("password")

    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail=user_db_data
    )


async def Get_Account_Whit_Id(id: str):
    users_db = conn.execute(users.select().where(
        users.c.id == id)).first()

    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este usuario."
        )

    user_db_data = users_db._asdict()

    user_db_data.update({"id": str(users_db.id)})

    user_db_data.pop("password")

    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail=user_db_data
    )


async def Delete_Account_Whit_Id(id: str):
    users_db = conn.execute(users.select().where(
        users.c.id == id)).first()

    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este usuario."
        )

    conn.execute(users.delete().where(users.c.id == id))

    conn.commit()

    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="Usuario eliminado correctamente.")


async def Update_Account_Whit_Id(id: str, data):

    users_db = conn.execute(users.select().where(
        users.c.id == id)).first()

    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este usuario."
        )
    data = data.dict()

    conn.execute(users.update().where(users.c.id == id).values(data))

    conn.commit()

    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="Usuario actualizado correctamente.")
