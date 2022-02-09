from dataclasses import dataclass
import requests

@dataclass
class Activity:
    Name: str
    Distance: float
    MovingTime: int
    ElapsedTime: int
    AverageHeartrate: float
    MaxHeartrate: float
    def __str__(self):
        return f'{self.Name} {self.Distance} {self.MovingTime} {self.ElapsedTime} {self.AverageHeartrate} {self.MaxHeartrate}'

@dataclass
class Auth:
    ExpiresAt: int
    RefreshToken: str
    AccessToken: str
    def __str__(self):
        return f'{self.ExpiresAt} {self.RefreshToken} {self.AccessToken}'


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
                res_json['access_token'])
    return str(res_json['athlete']['id']), auth


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
