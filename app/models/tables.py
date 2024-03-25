from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, Text, Boolean
from database.database_neon import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, nullable=False)
    name = Column(Text)
    email = Column(Text, unique=True)
    password = Column(Text)
    token = Column(Text)
    email_verified = Column(Boolean, default=False)
    age = Column(Integer)


class Students(Base):
    __tablename__ = "students"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text)
    last_name = Column(Text)
    email = Column(Text, unique=True)
    age = Column(Integer)
    city = Column(Text)
    address = Column(Text)
    phone = Column(Text)
    identification = Column(Text)
    birthday = Column(Date)


class Subjects(Base):
    __tablename__ = "subjects"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text)
    code = Column(Text)
    description = Column(Text)
    credits = Column(Integer)


class Enrollments(Base):
    __tablename__ = "enrollments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"))
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"))
    description = Column(Text)
    subject = relationship("Subjects")
    student = relationship("Students")
    code = Column(Integer)


Base.metadata.create_all(bind=engine)
