from sqlalchemy import create_engine, text

# os.environ['DATABASE_URL']

DATABASE_URL = "cockroachdb://hiro:1yfeMlIWnr7xxiqUeXw5Qw@quantum-trader-3674.g8z.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=coachroach.crt"
engine = create_engine(DATABASE_URL)
engine.connect()

with engine.connect() as conn:
    version = conn.execute('SELECT version()').fetchone()
    print(f'CockroachDB version: {version[0]}')

res = conn.execute(text("SELECT now()")).fetchall()
print(res)
