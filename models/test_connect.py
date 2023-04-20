import logging

from sqlalchemy import create_engine, text

# DATABASE_URL = "sqlite:///app.db"

SQL_USER = "api"
SQL_PASS = "7RWprblOldzfhu9lIlegrA"
DB_NAME = "defaultdb"
DB_PORT = 26257
SQL_HOST = "quantum-trader-3674.g8z.cockroachlabs.cloud"

DATABASE_URL = f"cockroachdb://{SQL_USER}:{SQL_PASS}@{SQL_HOST}:{DB_PORT}/{DB_NAME}?sslmode=verify-full"

try:
    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20,
                           echo=True)
except Exception as e:
    logging.critical("Failed to connect to database.")
    logging.critical(f"{e}")

conn = engine.connect()

query = ["1", "'Hiro'"]
query_string = ",".join(query)

res = conn.execute(text(f"SELECT {query_string}")).fetchall()
print(res)

record = res[0]
one, hiro = record
assert one == int(query[0])
assert hiro == query[1].replace("'", "")
