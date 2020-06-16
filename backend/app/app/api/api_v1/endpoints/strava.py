from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from fastapi.responses import PlainTextResponse
from datetime import datetime


from app import crud, schemas
from app.api import deps
from app.core.config import settings
from app.strava import AthleteClient
from app.strava.schemas import WebhookEvent

router = APIRouter()


def register_and_download_activity_history(db: Session, user: schemas.User, code: str):
    print('START REGISTRATION BACKGROUND TASK STRAVA')

    client = AthleteClient()
    token = client.exchange_code_access_token(code)

    external_user_in = schemas.ExternalUserCreate(
        external_user_id=token.athlete.id,
        external_source='strava',
        full_name=token.athlete.username,
        owner_id=user.id,
        external_user_access_token=token.access_token,
        external_user_access_token_expires_at=datetime.utcfromtimestamp(token.expires_at),  # TODO: check timestamp
        external_user_refresh_token=token.refresh_token,
    )

    crud.external_user.create(db, obj_in=external_user_in)

    activies_strava = client.get_activities()

    activities = [
        schemas.ActivityCreate(
            **dict(activity), owner_id=user.id, activity_type=activity.type, external_id=activity.id
        )
        for activity in activies_strava
    ]

    crud.activity.create_all(db=db, objs_in=activities)

    print('END BACKGROUND TASK STRAVA')


def query_and_add_activity_db(db: Session, owner_id: int, activity_id: int):
    external_user = crud.external_user.get_by_external_id_and_external_source(db, external_user_id=str(owner_id), external_source='strava')
    client = AthleteClient(access_token=external_user.external_user_access_token)

    # refresh token
    if datetime.now() >= external_user.external_user_access_token_expires_at:
        token = client.refresh_access_token(external_user.external_user_refresh_token)
        external_user_to_update = {
            'external_user_access_token': token.access_token,
            'external_user_refresh_token': token.refresh_token,
            'external_user_access_token_expires_at': datetime.utcfromtimestamp(token.expires_at)
        }
        crud.external_user.update(db, db_obj=external_user, obj_in=external_user_to_update)

    # get activity
    activity = client.get_activity(activity_id)

    # store activity
    activity_in = schemas.ActivityCreate(**dict(activity), activity_type=activity.type, external_id=activity.id, owner_id=external_user.owner_id)

    return crud.activity.create(db, obj_in=activity_in)


def process_webhook(db: Session, event: WebhookEvent):
    # TODO: handle all cases

    if event.aspect_type == "create" and event.object_type == "activity":
        query_and_add_activity_db(db, event.owner_id, event.object_id)

    return


@router.get("/token/{user_id}/")
def token_exchange(code: str, scope: str, user_id: int, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)) -> Any:
    """
    Token exchange with Strava, this register a new strava external user + get activities
    """

    if 'activity:read_all' not in scope:
        raise HTTPException(status_code=404, detail="Missing permissions")

    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    background_tasks.add_task(register_and_download_activity_history, db, user, code)

    return RedirectResponse(url="trainx://trainx.com")


@router.post('/webhook/', response_class=PlainTextResponse)
def webhook(event_in: WebhookEvent, background_tasks: BackgroundTasks, db: Session = Depends(deps.get_db)):
    """
    Receive updates from Strava
    https://developers.strava.com/docs/webhooks/ 
    """

    # TODO: security?
    background_tasks.add_task(process_webhook, db, event_in)
    return "OK"


@router.get('/webhook/')
def webhook_subscription(r: Request):
    """
    Validate webhook subscription
    """
    hub_mode = r.query_params.get('hub.mode')
    hub_challenge = r.query_params.get('hub.challenge')
    hub_verify_token = r.query_params.get('hub.verify_token')

    if hub_verify_token != settings.STRAVA_WEBHOOK_VERIFY_TOKEN or hub_mode != "subscribe":
        raise HTTPException(status_code=404, detail="Verify token do not match")

    return {'hub.challenge': hub_challenge}
