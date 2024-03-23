from helper.validator import is_valid_uuid
from database.database_neon import conn
from sqlalchemy import select, join
from fastapi import status, HTTPException
from models.tables import students, subjects, enrollments


async def Get_All_Enrollments():
    enrollments_DB = []

    enrollments_db = conn.execute(select(enrollments, students.c.id.label("student"), students.c.name, students.c.last_name, students.c.identification, subjects.c.id.label("subject"), subjects.c.name.label("subject_name"), subjects.c.code.label("subject_code"), subjects.c.credits).select_from(students, enrollments, subjects).where(
        enrollments.c.student_id == students.c.id).where(enrollments.c.subject_id == subjects.c.id)).fetchall()

    if not enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay inscripciones registradas."
        )

    for enrollment in enrollments_db:
        enrollment_dict = {
            "enrollment_id": str(enrollment.id),
            "student": {
                "id": str(enrollment.student),
                "name": enrollment.name,
                "last_name": enrollment.last_name,
                "identification": enrollment.identification,
            },
            "subject": {
                "id": str(enrollments_db.subject),
                "name": enrollments_db.subject_name,
                "code": enrollments_db.subject_code,
                "credits": enrollment.credits
            },
            "enrollment_description": enrollment.description,
            "enrollment_code": enrollment.code,
        }
        enrollments_DB.append(enrollment_dict)

    raise HTTPException(status_code=status.HTTP_200_OK, detail=enrollments_DB)


async def Get_Enrollment_id(id: str):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    enrollments_db = conn.execute(select(enrollments, students.c.id.label("student"), students.c.name, students.c.last_name, students.c.identification, subjects.c.id.label("subject"), subjects.c.name, subjects.c.code,
                                  subjects.c.credits).select_from(students, enrollments, subjects).where(enrollments.c.student_id == students.c.id).where(enrollments.c.subject_id == subjects.c.id).where(enrollments.c.id == id)).first()

    if not enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen esta inscripción."
        )

    enrollment_dict = {
        "enrollment_id": str(enrollments_db.id),
        "student": {
            "id": str(enrollments_db.student),
            "name": enrollments_db.name,
            "last_name": enrollments_db.last_name,
            "identification": enrollments_db.identification,
        },
        "subject": {
            "id": str(enrollments_db.subject),
            "name": enrollments_db.subject_name,
            "code": enrollments_db.subject_code,
            "credits": enrollments_db.credits
        },
        "enrollment_description": enrollments_db.description,
        "enrollment_code": enrollments_db.code,
    }

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=enrollment_dict)


async def Create_Enrollments(data):

    students_db = conn.execute(students.select().where(
        students.c.id == data.student_id)).fetchall()

    subjects_db = conn.execute(subjects.select().where(
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

    enrollments_db = conn.execute(enrollments.select().where(
        enrollments.c.student_id == data.student_id, enrollments.c.subject_id == data.subject_id)).fetchone()

    if enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe esta inscripción."
        )
    data = data.dict()

    conn.execute(enrollments.insert().values(data))
    conn.commit()

    raise HTTPException(status_code=status.HTTP_201_CREATED,
                        detail="Inscripción creada con éxito.")


async def Update_Enrollment(id: str, data):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    students_db = conn.execute(students.select().where(
        students.c.id == data.student_id)).fetchall()

    subjects_db = conn.execute(subjects.select().where(
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

    enrollments_db = conn.execute(enrollments.select().where(
        enrollments.c.id == id)).first()

    if not enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe esta inscripción."
        )

    conn.execute(enrollments.update().values(data).where(
        enrollments.c.id == id))
    conn.commit()

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail="Inscripción actualizada con éxito.")


async def Delete_Enrollment(id: str):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    enrollments_db = conn.execute(enrollments.select().where(
        enrollments.c.id == id)).first()

    if not enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe esta inscripción."
        )

    conn.execute(enrollments.delete().where(enrollments.c.id == id))
    conn.commit()

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail="Inscripción eliminada con éxito.")
