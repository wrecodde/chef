import database as db

db.start()

print(dir(db.User.objects.get('username', 'dejijoseph')))
