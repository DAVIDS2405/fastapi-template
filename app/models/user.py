from sqlalchemy import Table, Column, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from database.database_neon import meta, engine
import uuid


users = Table(
    "users",
    meta,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", Text),
    Column("email", Text),
    Column("password", Text),
    Column("age", Integer),
)

meta.create_all(engine)
