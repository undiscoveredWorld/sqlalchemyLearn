from typing import Type

from sqlalchemy.orm import Session
from src.common.db.db import Base


def clear_table(model: Type[Base], session: Session):
    session.query(model).delete()
    session.commit()
