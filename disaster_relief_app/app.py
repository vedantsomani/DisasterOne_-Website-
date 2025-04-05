from flask import Flask
from config import Config
from models import db
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

# Import Blueprints
from blueprints.auth import auth_bp
from blueprints.main import main_bp
from blueprints.admin import admin_bp
from blueprints.volunteer import volunteer_bp
from blueprints.resources import resources_bp
from blueprints.notifications import notifications_bp
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
csrf = CSRFProtect(app)
talisman = Talisman(app)
socketio = SocketIO(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
app.register_blueprint(resources_bp)
app.register_blueprint(notifications_bp, url_prefix='/notifications')

# Create tables if they do not exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True)
