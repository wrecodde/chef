import string, random


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
