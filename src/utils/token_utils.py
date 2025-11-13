import os
import jwt
import datetime

ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', 'cambiame_access_secret')
REFRESH_TOKEN_SECRET = os.environ.get('REFRESH_TOKEN_SECRET', 'cambiame_refresh_secret')

def create_access_token(payload, minutes=15):
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    data = payload.copy()
    data.update({"exp": exp})
    token = jwt.encode(data, ACCESS_TOKEN_SECRET, algorithm='HS256')
    return token

def create_refresh_token(payload, days=1):
    exp = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    data = payload.copy()
    data.update({"exp": exp})
    token = jwt.encode(data, REFRESH_TOKEN_SECRET, algorithm='HS256')
    return token

def verify_access_token(token):
    try:
        data = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=['HS256'])
        return True, data
    except Exception as e:
        return False, str(e)

def verify_refresh_token(token):
    try:
        data = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=['HS256'])
        return True, data
    except Exception as e:
        return False, str(e)
