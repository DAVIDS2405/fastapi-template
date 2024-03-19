from database.database_neon import conn
from fastapi import HTTPException
from fastapi import status
from models.user import users
from passlib.context import CryptContext
from helper.jwt import create_token


crypt = CryptContext(schemes=["bcrypt"])


async def Register_User(data):
    users_db = conn.execute(users.select().where(
        users.c.email == data.email)).first()

    if users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este correo ya está registrado."
        )

    password = crypt.hash(data.password.get_secret_value())
    data = data.dict()
    data.update({"password": password})
    data.update({"age": int(data["age"])})

    conn.execute(users.insert().values(data))
    conn.commit()

    raise HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="Usuario registrado correctamente."
    )


async def Login(data):
    users_db = conn.execute(users.select().where(
        users.c.email == data.email)).first()
    if not users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No existen este correo registrado.")

    if not crypt.verify(data.password.get_secret_value(), users_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta.")

    user_db_data = users_db._asdict()
    user_db_data.update({"token": str(create_token(users_db.id))})
    user_db_data.update({"id": str(users_db.id)})

    raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED, detail=user_db_data)
