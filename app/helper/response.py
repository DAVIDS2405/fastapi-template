def create_enrollment_dict(enrollment) -> dict:
    enrollment_dict = {
        "enrollment_id": str(enrollment.id),
        "student": {
            "id": str(enrollment.student),
            "name": enrollment.name,
            "last_name": enrollment.last_name,
            "identification": enrollment.identification,
        },
        "subject": {
            "id": str(enrollment.subject),
            "name": enrollment.subject_name,
            "code": enrollment.subject_code,
            "credits": enrollment.credits
        },
        "enrollment_description": enrollment.description,
        "enrollment_code": enrollment.code,
    }

    return enrollment_dict
