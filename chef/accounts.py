import string, random
import uuid

from . import util

from chef import database as db
db.start()


def get_account(auth_token):
    # function is responsible for splitting auth_token
    # into authorization (authr) and authentication (auhtn) components
    # fetch user data using authr and confirm validity using authn
    return {'username': 'bobthebuilder', 'password': 'greatestbuilderever'}

def create_account(username, email, password, user_type='user'):
    # functionality being added
    # validity is up next
    check = util.validate_new_account(email, username, password)
    
    try:
        if check['valid']:
            user = db.User(
                email=email,
                username=username,
                password=password,
                user_type=user_type,
                user_id=str(uuid.uuid4())
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
    # functionality to be added
    try:
        op_status = {
            'status': 'success',
            'message': 'User authenticated',
            'auth_token': ''.join(random.choices(string.ascii_lowercase, k=16),)
        }
    except:
        op_status = {
            'status': 'error',
            'message': 'Incorrect user credentials'
        }

    return random.choice([success, error])
