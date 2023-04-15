from sqlalchemy import Column, DateTime, func, Integer
from sqlalchemy.ext.declarative import declared_attr


class CommonModel:
    """
    Common model for all models
    """

    @declared_attr
    def id(self):
        return Column(
            "id",
            Integer,
            primary_key=True,
            nullable=False,
            autoincrement=True,
        )

    @declared_attr
    def created_at(self):
        return Column(DateTime(), default=func.now())

    @declared_attr
    def updated_at(self):
        return Column(DateTime(), default=func.now(), onupdate=func.now())
