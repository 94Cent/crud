#order of importation
#python #third party packages , local imports

from flask import Flask
from flask_migrate import Migrate  #new addition in init
from flask_wtf.csrf import CSRFProtect
csrf=CSRFProtect() #means that csrf protection is automatically availale on all our routes created on app. routes as long as it is a post request

def createapp():
    """keep all imports that may cause conflict within ths function so that anytime we write "from fapp.... import.... none of thes import statement will be executed"""
    app=Flask(__name__)
    from vapp import config
    app.config.from_pyfile("config.py",silent=True)
    from vapp.models import db
    db.init_app(app)
    csrf.init_app(app)
    migrate=Migrate(app,db) #new addition
    return app
app=createapp()

#load the routes
from vapp import routes, models,forms

