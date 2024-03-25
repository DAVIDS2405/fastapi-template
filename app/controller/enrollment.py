from helper.validator import is_valid_uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from models.tables import Students as students, Subjects as subjects, Enrollments as enrollments


async def Get_All_Enrollments():
    enrollments_DB = []

    enrollments_db = Session.execute(select(enrollments, students.c.id.label("student"), students.c.name, students.c.last_name, students.c.identification, subjects.c.id.label("subject"), subjects.c.name.label("subject_name"), subjects.c.code.label("subject_code"), subjects.c.credits).select_from(students, enrollments, subjects).where(
        enrollments.c.student_id == students.c.id).where(enrollments.c.subject_id == subjects.c.id)).fetchall()

    if not enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay inscripciones registradas."
        )

    for enrollment in enrollments_db:
        enrollment = enrollments_db.asdict()
        enrollments_DB.append(enrollment)

    raise HTTPException(status_code=status.HTTP_200_OK, detail=enrollments_DB)


async def Get_Enrollment_id(id: str):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    enrollments_db = Session.execute(select(enrollments, students.c.id.label("student"), students.c.name, students.c.last_name, students.c.identification, subjects.c.id.label("subject"), subjects.c.name.label("subject_name"), subjects.c.code.label("subject_code"),
                                            subjects.c.credits).select_from(students, enrollments, subjects).where(enrollments.c.student_id == students.c.id).where(enrollments.c.subject_id == subjects.c.id).where(enrollments.c.id == id)).first()

    if not enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen esta inscripción."
        )

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=enrollments_db)


async def Create_Enrollments(data):

    students_db = Session.execute(students.select().where(
        students.c.id == data.student_id)).fetchall()

    subjects_db = Session.execute(subjects.select().where(
        subjects.c.id == data.subject_id)).fetchall()

    if not students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe este estudiante."
        )

    if not subjects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe esta materia."
        )

    enrollments_db = Session.execute(enrollments.select().where(
        enrollments.c.student_id == data.student_id, enrollments.c.subject_id == data.subject_id)).fetchone()

    if enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe esta inscripción."
        )
    data = data.dict()

    Session.execute(enrollments.insert().values(data))
    Session.commit()

    raise HTTPException(status_code=status.HTTP_201_CREATED,
                        detail="Inscripción creada con éxito.")


async def Update_Enrollment(id: str, data):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    students_db = Session.execute(students.select().where(
        students.c.id == data.student_id)).fetchall()

    subjects_db = Session.execute(subjects.select().where(
        subjects.c.id == data.subject_id)).fetchall()

    if not students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe este estudiante."
        )

    if not subjects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe esta materia."
        )

    enrollments_db = Session.execute(enrollments.select().where(
        enrollments.c.id == id)).first()

    if not enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe esta inscripción."
        )

    Session.execute(enrollments.update().values(data).where(
        enrollments.c.id == id))
    Session.commit()

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail="Inscripción actualizada con éxito.")


async def Delete_Enrollment(id: str):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    enrollments_db = Session.execute(enrollments.select().where(
        enrollments.c.id == id)).first()

    if not enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe esta inscripción."
        )

    Session.execute(enrollments.delete().where(enrollments.c.id == id))
    Session.commit()

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail="Inscripción eliminada con éxito.")
