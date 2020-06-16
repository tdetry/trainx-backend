from typing import List
from .schemas import Athlete, Token, Activity
from .v3.client import Client


class AthleteClient():

    def __init__(self, access_token=None) -> None:
        self.client = Client(access_token=access_token)
        return

    def exchange_code_access_token(self, code) -> Token:
        response = self.client.exchange_code_access_token(code)
        token = Token(**response)
        self.client.access_token = token.access_token
        return token

    def refresh_access_token(self, access_token) -> Token:
        response = self.client.refresh_access_token(access_token)
        token = Token(**response)
        self.client.access_token = token.access_token
        return token

    def get_activity(self, activity_id) -> Activity:
        response = self.client.api(f'/activities/{activity_id}', 'GET')
        return Activity(**response)

    def get_activities(self) -> List[Activity]:
        params = {
            'scope': 'activity:read_permission',
            'per_page': 200
            }
        response = self.client.api('/athlete/activities', 'GET', params)
        return [Activity(**activity) for activity in response]

    def get_athlete(self) -> Athlete:
        response = self.client.api('/athlete')
        return Athlete(**response)
