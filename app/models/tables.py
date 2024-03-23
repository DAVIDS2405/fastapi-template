from sqlalchemy import Table, Column, Integer, Text, Date, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from database.database_neon import meta, engine
import uuid


users = Table(
    "users",
    meta,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", Text),
    Column("email", Text, unique=True),
    Column("password", Text),
    Column("token", Text),
    Column("email_verified", Boolean, default=False),
    Column("age", Integer),
)

students = Table(
    "students",
    meta,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", Text),
    Column("last_name", Text),
    Column("email", Text, unique=True),
    Column("age", Integer),
    Column("city", Text),
    Column("address", Text),
    Column("phone", Text),
    Column("identification", Text),
    Column("birthday", Date),

)

subjects = Table(
    "subjects",
    meta,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", Text),
    Column("code", Text),
    Column("description", Text),
    Column("credits", Integer),
)

enrollments = Table(
    "enrollments",
    meta,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("student_id", UUID(as_uuid=True), ForeignKey("students.id")),
    Column("subject_id", UUID(as_uuid=True), ForeignKey("subjects.id")),
    Column("description", Text),
    Column("code", Integer),

)

meta.create_all(engine)
