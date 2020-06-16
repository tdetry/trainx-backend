from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.external_user import ExternalUser
from app.schemas.external_user import ExternalUserCreate, ExternalUserUpdate


class CRUDExternalUser(CRUDBase[ExternalUser, ExternalUserCreate, ExternalUserUpdate]):
    def create(self, db: Session, *, obj_in: ExternalUserCreate) -> ExternalUser:
        db_obj = ExternalUser(
            external_user_id=obj_in.external_user_id,
            external_source=obj_in.external_source,
            full_name=obj_in.full_name,
            owner_id=obj_in.owner_id,
            external_user_access_token=obj_in.external_user_access_token,
            external_user_refresh_token=obj_in.external_user_refresh_token,
            external_user_access_token_expires_at=obj_in.external_user_access_token_expires_at
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_external_id_and_external_source(
        self, db: Session, *, external_user_id: str, external_source: str,
    ) -> Optional[ExternalUser]:
        return (
            db.query(ExternalUser)
            .filter(ExternalUser.external_user_id == external_user_id,
                    ExternalUser.external_source == external_source)
            .first()
        )


external_user = CRUDExternalUser(ExternalUser)
