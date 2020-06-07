from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

import requests

router = APIRouter()


@router.get("/token/{user_id}/")
def token_exchange(
    code: str,
    user_id: int,
) -> Any:
    """
    Token exchange with Strava
    """
    # TODO: better: module strava ? with token refresh (see front fb token manager)
    # TODO: better: check scope received
    # TODO: security: check id and secret
    # TODO: security: in configuration
    url_token = f'https://www.strava.com/oauth/token?client_id=49328&client_secret=b20d6d5ee200036f6ca331d3bd12cd2a9d31fb6b&code={code}&grant_type=authorization_code'
    r = requests.post(url_token)

    r = r.json()
    access_token = r['access_token']
    athlete = r['athlete']
    print(athlete)

    headers = {'Authorization': f'Bearer {access_token}'}
    url_activity = 'https://www.strava.com/api/v3/athlete/activities?scope=activity:read_permission&per_page=200'
    r = requests.get(url_activity, headers=headers)
    print(r.status_code)
    r = r.json()
    print(len(r))
    print(r[1])

    activities = [schemas.ActivityCreate(
        **activity, owner_id=user_id) for activity in r]

    print(activities)
    print(activities[1])

    # TODO: save db + history route

    # TODO: better: in configuration
    return RedirectResponse(url='trainx://trainx.com')
