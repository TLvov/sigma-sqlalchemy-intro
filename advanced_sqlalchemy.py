"""
This file shows the real power of SQLAlchemy.
Object Oriented Programming!
"""

from typing import Any
from sqlalchemy import ForeignKey, String, Engine, create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column

from basic_sqlalchemy import reset_database, SQL_DIALECT, DIALECT_LIBRARY, USER, PASSWORD, DATABASE

# Manages connections to the database
engine = create_engine(
    f"{SQL_DIALECT}+{DIALECT_LIBRARY}://{USER}:{PASSWORD}@localhost/{DATABASE}")


# We need to use inheritance to define a Base class for our tables,
# for now it doesn't need to do anything
class Base(DeclarativeBase):
    pass


# Now we define each table as a class, inheriting from the Base class we defined.
class Lecturer(Base):
    # Define the table
    __tablename__ = "lecturer"

    # Define the columns
    lecturer_id: Mapped[int] = mapped_column(primary_key=True)
    lecturer_name: Mapped[str] = mapped_column(String(30))


class Course(Base):
    __tablename__ = "course"

    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str] = mapped_column(String(30))


class Student(Base):
    __tablename__ = "student"

    student_id: Mapped[int] = mapped_column(primary_key=True)
    student_name: Mapped[str] = mapped_column(String(30))


class StudentCourse(Base):
    __tablename__ = "student_course"

    student_course_id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.course_id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("student.student_id"))


if __name__ == "__main__":
    # For now we will use our old method to clear the db
    reset_database(engine)

    # Insert into database
    with Session(engine) as session:
        sigma_bot = Lecturer(
            lecturer_name="SigmaBot"
        )
        session.add(sigma_bot)
        session.commit()

    # Select from database
    with Session(engine) as session:
        # We can easily refer to any entity by primary key
        by_id = session.get(Lecturer, 1)

    print(by_id.lecturer_name)

    with Session(engine) as session:
        by_name = session.scalar(
            select(Lecturer).where(Lecturer.lecturer_name == "SigmaBot"))
    print(by_name.lecturer_name)

    # Beautiful OOP code instead of multiline SQL strings everywhere!
