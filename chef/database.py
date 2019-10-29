import os

from mongoengine import *

# Model/Schema definitions

class User(Document):
    email = StringField(required=True)
    username = StringField(required=True, max_length=24)
    password = StringField(required=True)
    user_type = StringField()
    user_id = StringField()
    auth_token = StringField()

# Management
def start():
    try:
        MONGO_URL = os.environ['MONGO_URL']
        MONGO_PORT = os.environ['MONGO_PORT']
    except:
        print('\nMongoDB Config not set\n')
        raise

    connect('chef-db', alias='default', host=MONGO_URL, port=int(MONGO_PORT))

if __name__ == "__main__":
    start()    
