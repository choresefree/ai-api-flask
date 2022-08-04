from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import DevConfig
from app.deep_learning.speech_rec import SpeechRec
from app.deep_learning.image_rec import CharacterRec

character_recognizer = CharacterRec()
speech_recognier = SpeechRec()

static_conf = {
    'template_folder': 'templates',
    'static_folder': 'templates/static',
}
app = Flask(__name__, **static_conf)

app.config.from_object(DevConfig)
db = SQLAlchemy(app)

''' login_manager'''
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)


