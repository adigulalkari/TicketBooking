from .database import db

class Show_Venue(db.Model):
    __tablename__= 'venue_for_show'
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.venue_id"), primary_key=True, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"), primary_key=True, nullable=False)

class Venue(db.Model):
    __tablename__= 'venue'
    venue_id = db.Column(db.Integer, autoincrement =True, primary_key=True)
    venue_name = db.Column(db.String, unique=True)
    venue_place = db.Column(db.String, unique=False)
    venue_capacity = db.Column(db.Integer, unique=False)

class Show(db.Model):
    __tablename__= 'show'
    show_id=db.Column(db.Integer, autoincrement =True, primary_key=True)
    show_name = db.Column(db.String, unique=True)
    show_rating = db.Column(db.Integer)
    show_tags = db.Column(db.String)
    show_price = db.Column(db.Integer)
    venues_for_show= db.relationship("Venue", secondary="venue_for_show")

class Admin(db.Model):
    __tablename__= 'admin'
    admin_username = db.Column(db.String, unique=True, primary_key=True)
    admin_password = db.Column(db.String)

class User(db.Model):
    __tablename__= 'user'
    user_username = db.Column(db.String, unique=True, primary_key=True)
    user_password = db.Column(db.String)