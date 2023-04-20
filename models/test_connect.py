import os.path

import pytest
import sqlalchemy
from sqlalchemy import text

from models.connect import create_engine


@pytest.mark.parametrize("engine", [
    create_engine()
])
def test_create_engine(engine):
    conn = engine.connect()
    query = ["1", "'Hiro'"]
    query_string = ",".join(query)
    res = conn.execute(text(f"SELECT {query_string}")).fetchall()

    print(res)

    record = res[0]
    one, hiro = record
    assert one == int(query[0])
    assert hiro == query[1].replace("'", "")


def test_create_sqlite():
    DATABASE_URL = "sqlite:///app.db"

    engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)

    test_create_engine(engine)

    assert os.path.exists("app.db") is True

    os.remove("app.db")


@pytest.fixture(scope='session', autouse=True)
def cleanup():
    db_file = "app.db"
    # Perform cleanup tasks before running tests
    yield
    # Perform cleanup tasks after running tests
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except Exception as e:
            print(e)
