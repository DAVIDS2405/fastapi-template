
import uuid


def is_valid_uuid(id: str) -> bool:
    try:
        uuid.UUID(id)
        return True
    except ValueError:
        return False
