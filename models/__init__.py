from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from models.base_model import CommonModel
from .connect import create_engine

# Base.metadata.create_all(engine)

engine = create_engine(echo=True)

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
