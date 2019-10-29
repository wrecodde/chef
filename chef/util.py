try:
    from . import database as db
except:
    import database as db

def encrypt_password(password):
    return password

def compare_password(password, check):
    return password == check

def get_user_account(username):
    try:
        user = db.User.objects.get(username=username)
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
        db.User.objects.get(email=email)
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
        db.User.objects.get(username=username)
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
