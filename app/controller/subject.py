from helper.validator import is_valid_uuid
from database.database_neon import conn
from fastapi import HTTPException
from fastapi import status
from models.tables import subjects, enrollments


async def Get_All_Subjects():

    subjects_DB = []

    subjects_db = conn.execute(subjects.select()).fetchall()

    if not subjects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay materias registradas."
        )

    for subject in subjects_db:

        subject_dict = subject._asdict()

        subject_dict.update({"id": str(subject_dict.get("id"))})

        subjects_DB.append(subject_dict)

    raise HTTPException(status_code=status.HTTP_200_OK, detail=subjects_DB)


async def Get_Subject_id(id: str):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    subjects_db = conn.execute(subjects.select().where(
        subjects.c.id == id)).first()

    if not subjects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen esta materia."
        )

    subjects_db = subjects_db._asdict()

    subjects_db.update({"id": str(subjects_db.get("id"))})

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=subjects_db)


async def Create_Subjects(data):

    subjects_db = conn.execute(subjects.select().where(
        subjects.c.name == data.name)).fetchall()

    if subjects_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe esta materia."
        )
    data = data.dict()

    conn.execute(subjects.insert().values(data))

    conn.commit()

    raise HTTPException(status_code=status.HTTP_201_CREATED,
                        detail="Materia creada correctamente.")


async def Update_Subject(id: str, data):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    subjects_db = conn.execute(subjects.select().where(
        subjects.c.id == id)).first()

    name_subject = conn.execute(subjects.select().where(
        subjects.c.name == data.name)).first()

    if not subjects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen esta materia."
        )

    if name_subject:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe esta materia."
        )
    data = data.dict()

    conn.execute(subjects.update().where(
        subjects.c.id == id).values(data))

    conn.commit()

    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                        detail="Materia actualizada correctamente.")


async def Delete_Subject(id: str):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    subjects_db = conn.execute(subjects.select().where(
        subjects.c.id == id)).first()

    enrollments_db = conn.execute(enrollments.select().where(
        enrollments.c.subject_id == id)).fetchone()

    if not subjects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen esta materia."
        )

    if enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar la materia, ya que hay estudiantes inscritos."
        )

    conn.execute(subjects.delete().where(subjects.c.id == id))

    conn.commit()

    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                        detail="Materia eliminada correctamente.")
