from flask import Flask
from application import config
from flask_restful import Api
from application.config import LocalDevConfig
from application.database import db


app=None
api=None

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = 'my_secret_key'
    app.config.from_object(LocalDevConfig)
    db.init_app(app)
    api=Api(app)
    app.app_context().push()
    return app,api

app,api = create_app()
# Importing all the routes
from application.controllers import *


# Importing all routes from API
from application.api import VenueAPI, ShowAPI
api.add_resource(VenueAPI,"/venue")
api.add_resource(ShowAPI, "/show", "/show/<int:show_id>/delete","/show/<int:show_id>/update")


if __name__ == "__main__":
    app.run(debug =False, host='0.0.0.0', port=8080)
