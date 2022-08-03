from app.create_app import db
import models


db.drop_all()
db.create_all()
print("Finish tables creating")