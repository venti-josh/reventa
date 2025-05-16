from typing import Any

from sqlalchemy.orm.decl_api import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    id: Any

    # Generate __tablename__ automatically

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return cls.__name__.lower()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"
