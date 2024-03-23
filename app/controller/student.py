from helper.validator import is_valid_uuid
from database.database_neon import conn
from fastapi import HTTPException
from fastapi import status
from models.tables import students, enrollments


async def Get_All_Students():
    students_DB = []

    students_db = conn.execute(students.select()).fetchall()

    if not students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay estudiantes registrados."
        )

    for student in students_db:

        student_dict = student._asdict()

        student_dict.update({"id": str(student_dict.get(
            "id")), "birthday": str(student_dict.get("birthday")), })

        students_DB.append(student_dict)

    raise HTTPException(status_code=status.HTTP_200_OK, detail=students_DB)


async def Get_Student_id(id: str):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    students_db = conn.execute(students.select().where(
        students.c.id == id)).first()

    if not students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este estudiante."
        )

    students_db = students_db._asdict()

    students_db.update({"id": str(students_db.get("id")), "birthday": str(
        students_db.get("birthday"))})

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=students_db)


async def Create_Students(data):

    students_db = conn.execute(students.select().where(
        students.c.identification == data.identification)).fetchall()

    if students_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe este estudiante."
        )
    data = data.dict()

    conn.execute(students.insert().values(data))
    conn.commit()

    raise HTTPException(status_code=status.HTTP_201_CREATED,
                        detail="Estudiante registrado con éxito.")


async def Update_Student(id: str, data):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )
    students_db = conn.execute(students.select().where(
        students.c.id == id)).first()

    if not students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este estudiante."
        )

    data = data.dict()

    conn.execute(students.update().values(data).where(students.c.id == id))
    conn.commit()

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail="Estudiante actualizado con éxito.")


async def Delete_Student(id: str):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )
    students_db = conn.execute(students.select().where(
        students.c.id == id)).first()

    enrollments_db = conn.execute(enrollments.select().where(
        enrollments.c.student_id == id)).fetchall()

    if enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar este estudiante porque tiene matrículas asociadas."
        )

    if not students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este estudiante."
        )

    conn.execute(students.delete().where(students.c.id == id))
    conn.commit()

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail="Estudiante eliminado con éxito.")
