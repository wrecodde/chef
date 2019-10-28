import string, random

def get_account(auth_token):
    # function is responsible for splitting auth_token
    # into authorization (authr) and authentication (auhtn) components
    # fetch user data using authr and confirm validity using authn
    return {'username': 'bobthebuilder', 'password': 'greatestbuilderever'}

def create_account(username, email, password):
    # some functionality is to be added here
    success = {
        'status': 'success',
        'message': 'Account created successfully',
        'auth_token': ''.join(random.choices(string.ascii_lowercase, k=16),)
    }

    error = {
        'status': 'error',
        'message': 'Some error occured',
    }

    return random.choice([success, error])

def confirm_account(username, password):
    # functionality to be added
    success = {
        'status': 'success',
        'message': 'User authenticated',
        'auth_token': ''.join(random.choices(string.ascii_lowercase, k=16),)
    }

    error = {
        'status': 'error',
        'message': 'Incorrect user credentials'
    }

    return random.choice([success, error])
