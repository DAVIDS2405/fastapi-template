from helper.validator import is_valid_uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from models.tables import Students as students, Enrollments as enrollments


async def Get_All_Students(session: Session):
    students_DB = []

    students_db = session.query(students).all()

    if not students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay estudiantes registrados."
        )

    for student in students_db:

        student_dict = student.__dict__

        student_dict.update({"id": str(student_dict.get(
            "id")), "birthday": str(student_dict.get("birthday")), })
        student_dict.pop("_sa_instance_state")

        students_DB.append(student_dict)

    raise HTTPException(status_code=status.HTTP_200_OK, detail=students_DB)


async def Get_Student_id(id: str, session: Session):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )

    students_db = session.query(students).where(students.id == id).first()

    if not students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este estudiante."
        )

    students_db = students_db.__dict__

    students_db.update({"id": str(students_db.get("id")), "birthday": str(
        students_db.get("birthday"))})
    students_db.pop("_sa_instance_state")

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=students_db)


async def Create_Students(data, session: Session):

    students_db = session.query(students).where(
        students.identification == data.identification).first()

    students_email_db = session.query(students).where(
        students.email == data.email).first()

    if students_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe este estudiante."
        )

    if students_email_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un estudiante con este correo."
        )

    data = data.dict()
    new_student = students(**data)
    session.add(new_student)
    session.commit()

    raise HTTPException(status_code=status.HTTP_201_CREATED,
                        detail="Estudiante registrado con éxito.")


async def Update_Student(id: str, data, session: Session):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )
    students_db = session.query(students).where(students.id == id).first()

    students_email_db = session.query(students).where(
        students.email == data.email).first()

    if not students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen este estudiante."
        )

    if students_email_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un estudiante con este correo."
        )

    data = data.dict()

    session.query(students).where(students.id == id).update(data)
    session.commit()

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail="Estudiante actualizado con éxito.")


async def Delete_Student(id: str, session: Session):

    if not is_valid_uuid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id inválido."
        )
    students_db = session.query(students).where(students.id == id).first()

    enrollments_db = session.query(enrollments).where(
        enrollments.student_id == id).first()

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

    session.query(students).where(students.id == id).delete()
    session.commit()

    raise HTTPException(status_code=status.HTTP_200_OK,
                        detail="Estudiante eliminado con éxito.")
