from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///app.db"

engine = create_engine(DATABASE_URL, echo=True)
engine.connect()

# Base.metadata.create_all(engine)

# DATABASE_URL = "cockroachdb://hiro:1yfeMlIWnr7xxiqUeXw5Qw@quantum-trader-3674.g8z.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=coachroach.crt"
# with engine.connect() as conn:
#     version = conn.execute('SELECT version()').fetchone()
#     print(f'CockroachDB version: {version[0]}')
#
# res = conn.execute(text("SELECT now()")).fetchall()
# print(res)

# os.environ['DATABASE_URL']

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from models.base_model import CommonModel

Base = declarative_base(cls=CommonModel, bind=engine)  # bind is deprecated

_Session = sessionmaker(bind=engine)

session = _Session()

from models.indicator import *
from models.symbol import *
from models.binance import *
from models.futures import *

# session.add(User(username="XXXX", password="1yfeMlIWnr7xxiqUeXw5Qw"))
# session.add(.User(username="XXXX", password="1yfeMlIWnr7xxiqUeXw5Qw"))
# session.commit()
# session.close()
# session.query(models.User).all()
# ForeignKey("tablename.attribute"

# .filter(models.User.username == "XXXX")
