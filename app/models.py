import unicodedata
from . import db


class UserProperty(db.Model):
    __tablename__ = 'UserProperty'
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(50), nullable=False)
    num_bedrooms = db.Column(db.Integer, nullable=False)
    num_bathrooms = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(15,2), nullable=False)
    type_ = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    upload = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.Date, nullable=False)

    def __init__(self, id, title, description, num_bedrooms, num_bathrooms, price, type_, location, upload, date_created):
        self.id = id
        self.title = title 
        self.description = description 
        self.num_bedrooms = num_bedrooms
        self.num_bathrooms = num_bathrooms 
        self.price = price 
        self.type_ = type_ 
        self.location = location 
        self.upload = upload 
        self.date_created = date_created 

    def is_authenticated(self):
        return True

    def is_active(self):
        return True 

    def is_anonymous(self):
        return False 

    def get_id(self):
        try:
            return unicodedata(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.title) 