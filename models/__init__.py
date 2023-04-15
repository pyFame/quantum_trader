from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from base_model import CommonModel
from conf.db import engine

Base = declarative_base(cls=CommonModel, bind=engine)  # bind is deprecated

_Session = sessionmaker(bind=engine)

session = _Session()

# session.add(User(username="XXXX", password="1yfeMlIWnr7xxiqUeXw5Qw"))
# session.add(.User(username="XXXX", password="1yfeMlIWnr7xxiqUeXw5Qw"))
# session.commit()
# session.close()
# session.query(models.User).all()
# ForeignKey("tablename.attribute"

# .filter(models.User.username == "XXXX")
