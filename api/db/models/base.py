import uuid
from sqlalchemy.orm import DeclarativeBase 
from sqlalchemy.inspection import inspect


class DictSerializerMixin:
    def asdict(self) -> dict:
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }


class Base(DeclarativeBase, DictSerializerMixin):
    pass
