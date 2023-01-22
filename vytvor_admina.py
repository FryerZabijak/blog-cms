from app import db, User

adminUser = User(id=1,login="Pepa",password="heslo",admin=1)
db.session.add(adminUser)
db.session.commit()