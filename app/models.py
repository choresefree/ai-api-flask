from app.create_app import db
from sqlalchemy import Column, String
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    uid = Column(String(20), primary_key=True)
    pwd = Column(String(20), nullable=False, unique=True)
    email = Column(String(25), nullable=False)
    phone = Column(String(11), nullable=False)

    def get_id(self):
        try:
            return str(self.uid)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None
