from helper.validator import is_valid_uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import status
from models.tables import Subjects as subjects, Enrollments as enrollments


async def Get_All_Subjects():

    subjects_DB = []

    subjects_db = Session.execute(subjects.select()).fetchall()

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

    subjects_db = Session.execute(subjects.select().where(
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

    subjects_db = Session.execute(subjects.select().where(
        subjects.c.name == data.name)).fetchall()

    if subjects_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe esta materia."
        )
    data = data.dict()

    Session.execute(subjects.insert().values(data))

    Session.commit()

    raise HTTPException(status_code=status.HTTP_201_CREATED,
                        detail="Materia creada correctamente.")


async def Update_Subject(id: str, data):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    subjects_db = Session.execute(subjects.select().where(
        subjects.c.id == id)).first()

    name_subject = Session.execute(subjects.select().where(
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

    Session.execute(subjects.update().where(
        subjects.c.id == id).values(data))

    Session.commit()

    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                        detail="Materia actualizada correctamente.")


async def Delete_Subject(id: str):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    subjects_db = Session.execute(subjects.select().where(
        subjects.c.id == id)).first()

    enrollments_db = Session.execute(enrollments.select().where(
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

    Session.execute(subjects.delete().where(subjects.c.id == id))

    Session.commit()

    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                        detail="Materia eliminada correctamente.")
