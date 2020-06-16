from app.core.config import settings
import requests


class Client():

    server = 'https://www.strava.com'
    api_base = '/api/v3'
    client_id = settings.STRAVA_CLIENT_ID
    client_secret = settings.STRAVA_CLIENT_SECRET

    def __init__(self, access_token=None, request_session=None):
        self.access_token = access_token
        if request_session is None:
            self.rsession = requests.Session()
        else:
            self.rsession = request_session
        return

    def exchange_code_access_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        print('params', params)

        return self.api('/oauth/token', method='POST', params=params, authorise_header=False)

    def refresh_access_token(self, refresh_access_token):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_access_token,
            'grant_type': 'refresh_token'
        }
        print('params', params)

        return self.api('/oauth/token', method='POST', params=params, authorise_header=False)

    def api(self, path, method='GET', params={}, authorise_header=True):

        methods = {
            'GET': self.rsession.get,
            'POST': self.rsession.post,
        }

        headers = {}

        if authorise_header:
            headers['Authorization'] = f'Bearer {self.access_token}'

        response = methods[method](f'{self.server}{self.api_base}{path}', headers=headers, params=params)
    
        if response.status_code != 200:
            print('BUG STRAVA')
            print(response.content)
            return {}

        return response.json()
