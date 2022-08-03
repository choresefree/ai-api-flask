from app.create_app import app
from app.views.account import bp as account_bp
from app.views.image import bp as image_bp
from app.views.speech import bp as speech_bp

app.register_blueprint(account_bp)
app.register_blueprint(image_bp)
app.register_blueprint(speech_bp)
app.run()
