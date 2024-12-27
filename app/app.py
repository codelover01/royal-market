from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from .models.users import login_manager, db, bcrypt
from flask_migrate import Migrate

csrf = CSRFProtect()
mail = Mail()

# Flask app instance
app = Flask(__name__)

# Import Configurations
from .config import Config
app.config.from_object(Config)

if app.config['TESTING']:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
cors = CORS(app, supports_credentials=True ,resources={r"/*": {"origins": "/*"}})

bcrypt.init_app(app)
csrf.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Import blueprints
from .routes.auth import auth_bp as auth_bp
from .services.products import products_bp as products_bp
from .routes.generate_csrf import gen_csrf_bp as gen_csrf_bp
from .services.services import services_bp as services_bp
from .routes.user_dashboard import user_dashboard_bp as user_dashboard_bp
from .routes.admin_dashboard import admin_dashboard_bp as admin_dashboard_bp


# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(gen_csrf_bp, url_prefix='/gen_csrf')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(services_bp, url_prefix='/services')
app.register_blueprint(user_dashboard_bp, url_prefix='/user')
app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')


@app.route('/')
def landing_page():
    return "I am landing soon"

@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """ Handles the homepage of the app"""
    return "This is the home page"


if __name__ == "__main__":
    app.run(debug=True)