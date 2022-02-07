from dataclasses import dataclass
import requests


@dataclass
class Basic_Athlete:
    ID: int
    FirstName: str
    LastName: str
    def __str__(self):
        return f'{self.ID} {self.FirstName} {self.LastName}'


@dataclass
class Auth:
    ExpiresAt: int
    RefreshToken: str
    AccessToken: str
    Athlete: Basic_Athlete
    def __str__(self):
        return f'{self.ExpiresAt} {self.RefreshToken} {self.AccessToken}\n{self.Athlete}'


def token_exchange(client_id, client_secret, code):
    auth_url = "https://www.strava.com/api/v3/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': "authorization_code",
    }
    res = requests.post(auth_url, data=payload, verify=False)
    res_json = res.json()
    auth = Auth(res_json['expires_at'],
                res_json['refresh_token'],
                res_json['access_token'],
                Basic_Athlete(res_json['athlete']['id'],
                              res_json['athlete']['firstname'], 
                              res_json['athlete']['lastname'])
                )
    return auth

# Currently unused
#==============================================================================
def refresh_token(client_id, client_secret, auth):
    auth_url = "https://www.strava.com/api/v3/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': auth.RefreshToken,
        'grant_type': "refresh_token",
    }
    res = requests.post(auth_url, data=payload, verify=False)
    res_json = res.json()
    auth['expires_at'] = res_json['expires_at']
    auth['refresh_token'] = res_json['refresh_token']
    auth['access_token'] = res_json['access_token']
    return auth
