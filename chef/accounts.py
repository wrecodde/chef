import json, string, random
import uuid

from . import util

from chef import database as db
db.start()


def get_account(auth_token):
    # function is responsible for splitting auth_token
    # into authorization (authr) and authentication (auhtn) components
    # fetch user data using authr and confirm validity using authn

    # can we assume that possession of some auth_token is as good as security goes?
    try:
        account = db.Users.objects.get(auth_token=auth_token)
        return account
    except db.DoesNotExist as err:
        # logging: use 'err'
        # invalid credentials were provided
        return None

def create_account(username, email, password, user_type='user'):
    # functionality as well as validity is being worked on
    check = util.validate_new_account(email, username, password)
    
    try:
        if check['valid']:
            user = db.Users(
                email=email,
                username=username,
                password=util.encrypt_password(password),
                user_type=user_type,
                user_id=str(uuid.uuid4()),
                auth_token=util.generate_auth_token(user_type, username)
            )
            user.save()
            op_status = {'status': 'success', 'message': 'Account created successfully'}
        else:
            op_status = {'status': 'error', 'message': check['error_msg']}
    except:
        raise
        op_status = {'status': 'error', 'message': 'Some error occured'}
    
    return op_status

def confirm_account(username, password):
    # functionality as well as validity is being worked on
    user = util.get_user_account(username)

    try:
        if user['exists']:
            authd = util.verify_password(user['password'], password)
            if authd:
                op_status = {'status': 'success', 'message': 'User authenticated', 'auth_token': user['auth_token']}
            else:
                op_status = {'status': 'error', 'message': 'Incorrect user credentials'}
        else:
            op_status = {'status': 'error', 'message': 'Incorrect user credentials'}
    except:
        raise
        op_status = {'status': 'error', 'message': 'Incorrect user credentials'}

    return op_status
