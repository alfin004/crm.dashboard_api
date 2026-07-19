from typing import Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T]):
        self.model = model

    def create(
        self,
        db: Session,
        obj: T
    ) -> T:
        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    def get_by_id(
        self,
        db: Session,
        id: UUID
    ) -> T | None:

        return (
            db.query(self.model)
            .filter(
                self.model.id == id,
                self.model.is_deleted == False
            )
            .first()
        )

    def get_all(
        self,
        db: Session,
        limit: int = 10,
        offset: int = 0,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ):

        query = db.query(self.model).filter(
            self.model.is_deleted == False
        )

        sort_column = getattr(
            self.model,
            sort_by,
            self.model.created_at
        )

        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        total = query.count()

        data = (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "items": data,
            "total": total
        }

    def update(
        self,
        db: Session,
        db_obj: T,
        update_data: dict
    ) -> T:

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    def delete(
        self,
        db: Session,
        db_obj: T
    ):

        db_obj.is_deleted = True

        db.commit()