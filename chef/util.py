import os, json, secrets

import jwt

from hashlib import blake2b
from hmac import compare_digest

try:
    from . import database as db
except:
    import database as db

try:
    SECRET_KEY = bytes(os.environ['SECRET_KEY'], 'utf-8')
    AUTH_SIZE = int(os.environ['AUTH_SIZE'])
except:
    print('\nSecurity hash config not set\n')
    raise


def encrypt_password(password):
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(bytes(password, 'utf-8'))
    return h.hexdigest().encode('utf-8')

def verify_password(known_key, password):
    return compare_digest(bytes(known_key, 'utf-8'), encrypt_password(password))

def generate_auth_token(user_type, username):
    # generate_auth_token can be called as needed for scenarios such as
    # new accounts, password change, new token on request...

    payload = {
        'user_type': user_type,
        'username': username,
        'salt': secrets.token_hex(8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def get_user_account(username):
    try:
        user = db.Users.objects.get(username=username)
        return {
            'exists': True,
            'password': user.password,
            'auth_token': user.auth_token
        }
    except:
        return {'exists':False}

def validate_email(email):
    # MongoEngine (at least as far as I know now) does not provide
    # a method to check the existence of a Document and responds
    # with errors if it does not exist
    try:
        db.Users.objects.get(email=email)
        email_check = {'status':False, 'msg':'Email address is in use'}
    except db.DoesNotExist:
        email_check = {'status':True, 'msg':'Email address is not in use'}
    except:
        email_check = {'status':False, 'msg':'Email address is in use'}
    finally:
        return email_check

def validate_username(username):
    # MongoEngine (at least as far as I know now) does not provide
    # a method to check the existence of a Document and responds
    # with errors if it does not exist
    try:
        db.Users.objects.get(username=username)
        username_check = {'status':False, 'msg':'Username is in use'}
    except db.DoesNotExist:
        username_check = {'status':True, 'msg':'Username is not in use'}
    except:
        username_check = {'status':False, 'msg':'Username is in use'}
    finally:
        return username_check

def validate_new_account(email, username, password):
    # ideally, run validation through a couple of db specific checks
    # check username
    username_check = validate_username(username)
    if not username_check['status']:
        return {'valid':False, 'error_msg':username_check['msg']}
    
    # validate email
    email_check = validate_email(email)
    if not email_check['status']:
        return {'valid':False, 'error_msg':email_check['msg']}
    
    return {'valid':True, 'msg':'Account is good to go'}
