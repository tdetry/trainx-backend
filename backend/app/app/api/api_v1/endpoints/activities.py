from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Activity])
def read_activities(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 20,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve activties for user.
    """
    activities = crud.activity.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )

    return activities  # current_user.activities also works - idk differences yet (probably skip and limit).
