from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

file_photos = app.config['UPLOAD_FOLDER']
if os.path.exists(file_photos) == False:
    os.makedirs(file_photos)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)


from app import routes, models