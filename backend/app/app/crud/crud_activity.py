from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):
    def create_all(
        self, db: Session, *, objs_in: List[ActivityCreate]
    ) -> List[Activity]:
        objs_in_data = [jsonable_encoder(obj_in) for obj_in in objs_in]
        db_objs = [
            self.model(**obj_in_data) for obj_in_data in objs_in_data
        ]
        db.add_all(db_objs)
        db.commit()

        return db_objs

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Activity]:
        return (
            db.query(self.model)
            .filter(Activity.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


activity = CRUDActivity(Activity)
