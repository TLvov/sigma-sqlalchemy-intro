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


def insert_lecturer(engine: Engine, name: str):
    """Easy insert with no SQL code necessary"""
    with Session(engine) as session:
        lecturer = Lecturer(lecturer_name=name)
        session.add(lecturer)
        session.commit()
    return lecturer


def insert_lecturers(engine: Engine, names: list[str]):
    """Just pass a list of names and this will insert a new lecturer for each one!"""
    with Session(engine) as session:
        lecturers = [Lecturer(lecturer_name=name)
                     for name in names]
        session.add_all(lecturers)
        session.commit()

    return lecturers


def get_by_key(engine: Engine, table: type, key: int):
    with Session(engine) as session:
        row = session.get(table, key)
    return row


def select_lecturer_by_name(engine: Engine, name: str):
    with Session(engine) as session:
        # Build an SQL statement out of python code
        stmt = select(Lecturer).where(Lecturer.lecturer_name == "SigmaBot")

        # We can use .scalar to run our statement
        by_name = session.scalar(stmt)

    return by_name


if __name__ == "__main__":
    # For now we will use our old method to clear the db
    reset_database(engine)

    # Insert into table
    insert_lecturer(engine, "SigmaBot")

    # Select from table (by id)
    lecturer = get_by_key(engine, Lecturer, 1)

    print(lecturer.lecturer_name)

    # Select from lecturer table (by name)
    by_name = select_lecturer_by_name(engine, "SigmaBot")

    print(by_name.lecturer_name)

    # Beautiful OOP code instead of multiline SQL strings everywhere!
