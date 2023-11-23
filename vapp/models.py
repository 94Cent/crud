from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):  
    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_fullname = db.Column(db.String(100),nullable=False)
    user_email = db.Column(db.String(120)) 
    user_pwd=db.Column(db.String(120),nullable=True)
    user_pix=db.Column(db.String(120),nullable=True) 
    user_datereg=db.Column(db.DateTime(), default=datetime.utcnow)#default 
    
class Post(db.Model):
   # __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    post_title = db.Column(db.String(255), nullable=False)
    post_content = db.Column(db.Text(), nullable=False)
    post_author = db.Column(db.String(255), nullable=True)
    post_cat_id = db.Column(db.Integer(),db.ForeignKey("category.cat_id"))
    post_created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    post_updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow) 

    #set relationship
    #overlaps="catdeets,myposts"
    catdeets=db.relationship('Category',backref="myposts") 
    #userdeets= db.relationship('Category',backref="userposts") 

class Contact(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    name= db.Column(db.String(255), nullable=False)
    email =db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    message= db.Column(db.Text(), nullable=False)
    datesent = db.Column(db.DateTime(), default=datetime.utcnow) 

class Category(db.Model):
    cat_id= db.Column(db.Integer(), primary_key=True,autoincrement=True)
    cat_name = db.Column(db.String(255), nullable=False)

class Newsletter(db.Model):
    id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    email= db.Column(db.String(255), nullable=False)

class Lga(db.Model):
    lga_id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_id=db.Column(db.Integer(),db.ForeignKey("state.state_id"))
    lga_name=db.Column(db.String(255), nullable=False)
#set relationship
statedeets= db.relationship('State',backref="all_lgas") 

class State(db.Model):
    state_id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_name=db.Column(db.String(255), nullable=False)
