"""
This file demonstrates use of SQLAlchemy in a very
similar way to use of psycopg2, it's a versatile tool!
"""

from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine, text, Row, Engine

SQL_DIALECT = "postgresql"  # We're used to postgresql, but we can use any.
DIALECT_LIBRARY = "psycopg2"  # How our dialect interacts with python.

# You will need to provide your PSQL username and password,
# mine are hidden away in a .env file.
# You can reset your password in postgres with:
# `ALTER USER {username} WITH PASSWORD '{password}';`
load_dotenv()
USER = getenv("USER")  # PSQL username.
PASSWORD = getenv("PASSWORD")  # PSQL user password.

DATABASE = "test_sqlalchemy"  # Name of PSQL database.


def get_engine():
    # Engines manage connections to the database
    return create_engine(
        f"{SQL_DIALECT}+{DIALECT_LIBRARY}://{USER}:{PASSWORD}@localhost/{DATABASE}")


def reset_database(engine: Engine):
    """Runs the schema.sql file to reset the database"""
    with engine.connect() as conn:
        with open("schema.sql", "r", encoding="UTF-8") as schema:
            conn.execute(
                text(schema.read()))
        conn.commit()


def select_hello_word(engine: Engine):
    """The simplest SQL query, returns 'hello world!'."""

    query = "SELECT 'hello world!';"

    with engine.connect() as conn:
        result = conn.execute(
            text(query))

        row = result.fetchone()

    return row[0]


def insert_lecturer(engine: Engine, lecturer_name: str) -> Row:
    """
    A query that inserts a lecturer into lecturer table given a name.
    Returns inserted row.
    """

    # Note slightly different syntax for parameterization
    # Parameters are preceded by colons
    query = """
            INSERT INTO lecturer (lecturer_name)
            VALUES (:lecturer_name)
            RETURNING *;
            """

    with engine.connect() as conn:
        # Similar to psycopg2 we pass parameters with execution
        result = conn.execute(
            text(query),
            {"lecturer_name": lecturer_name})

        row = result.fetchone()
        conn.commit()

    return row


def select_lecturers(engine: Engine) -> list[Row]:
    """Simple query to output all lecturers"""

    query = "SELECT * FROM lecturer;"

    with engine.connect() as conn:
        result = conn.execute(
            text(query))

        rows = result.fetchall()

    return rows


def main():
    engine = get_engine()

    reset_database(engine)

    print(select_hello_word(engine))

    sigma_bot = insert_lecturer(engine, "SigmaBot")

    # Each row is similar to a namedtuple,
    # we can access their attributes directly
    print(f"\nYou've just inserted {sigma_bot.lecturer_name}!")

    insert_lecturer(engine, "Siggy")
    insert_lecturer(engine, "Ciggy??")

    lecturers = select_lecturers(engine)

    # We can print each row
    print("\nHere are all the lecturers!")
    for lecturer in lecturers:
        print(lecturer)

    # Or print just the attributes we want
    print("\nHere are the names of all lecturers:")
    for lecturer in lecturers:
        print(lecturer.lecturer_name)


if __name__ == "__main__":
    main()
