from flask import Flask, request
from flask_mail import Mail
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from models.users import login_manager, db, bcrypt
from flask_migrate import Migrate
import os
from flask import jsonify, make_response
from flask_wtf.csrf import CSRFProtect, generate_csrf
csrf = CSRFProtect()
from datetime import timedelta

csrf = CSRFProtect()
mail = Mail()

# Flask app instance
app = Flask(__name__)

# # Import Configurations
# from config import Config, TestConfig

# # Check if testing
# if os.getenv('FLASK_ENV') == 'testing' or os.getenv('TESTING') == 'True':
#     app.config.from_object(TestConfig)
# else:
#     app.config.from_object(Config)

# Load configuration
from config import Config, TestConfig

# # if os.getenv('FLASK_ENV') == 'testing' or os.getenv('TESTING') == 'True':
# #     app.config.from_object(TestConfig)
# # else:
# app.config.from_object(Config)

# Load Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development').lower()
TESTING = os.getenv('TESTING', 'False').lower() == 'true'

if TESTING:
    app.config.from_object(TestConfig)  # Use test configuration
    print("🚨 Using Test Configuration")
elif FLASK_ENV == 'production':
    app.config.from_object(Config)  # Production Config
    print("✅ Using Production Configuration")
else:
    app.config.from_object(Config)  # Default to development
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies', 'query_string']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    print("⚙️ Using Development Configuration")


cors = CORS(app, supports_credentials=True ,resources={r"/*": {"origins": "/*"}})

bcrypt.init_app(app)
csrf.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Import blueprints
from routes.business import business_bp as business_bp
from routes.auth import auth_bp as auth_bp
from services.reviews import review_bp as review_bp
from services.products import products_bp as products_bp
from routes.generate_csrf import gen_csrf_bp as gen_csrf_bp
from services.services import services_bp as services_bp
from routes.user_dashboard import user_dashboard_bp as user_dashboard_bp
from routes.admin_dashboard import admin_dashboard_bp as admin_dashboard_bp
from routes.wishlist import wishlist_bp as wishlist_bp
from routes.category import category_bp as category_bp
from routes.payments import payment_bp as payment_bp
from routes.inventory import inventory_bp as inventory_bp


# Register blueprints
app.register_blueprint(business_bp, url_prefix='/business')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(gen_csrf_bp, url_prefix='/gen_csrf')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(services_bp, url_prefix='/services')
app.register_blueprint(user_dashboard_bp, url_prefix='/user')
app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')
app.register_blueprint(review_bp, url_prefix='/review')
app.register_blueprint(wishlist_bp, url_prefix='/wishlist')
app.register_blueprint(category_bp, url_prefix='/categories')
app.register_blueprint(payment_bp, url_prefix='/payments')
app.register_blueprint(inventory_bp, url_prefix='/inventory')

# @app.before_request
# def set_csrf_cookie():
#     csrf_token = generate_csrf()
#     response = make_response(jsonify({'message': 'CSRF token set'}))
#     response.set_cookie('csrf_token', csrf_token, httponly=False)
#     response.set_cookie('csrf_token', csrf_token)

# @app.before_request
# def set_csrf_cookie():
#     if not request.cookies.get('csrf_token'):
#         csrf_token = generate_csrf()
#         response = make_response()
#         response.set_cookie(
#             'csrf_token',
#             csrf_token,
#             httponly=False,
#             samesite='Lax',
#             secure=False  # Change to True if using HTTPS
#         )
#         return response

@app.before_request
def csrf_protect():
    """
    CSRF Protection: Verify CSRF token from cookies and headers.
    """
    csrf_token_cookie = request.cookies.get('csrf_token')
    csrf_token_header = request.headers.get('X-CSRFToken')

    if request.method in ['POST', 'PUT', 'DELETE']:
        if not csrf_token_cookie or not csrf_token_header:
            return jsonify({"error": "CSRF token missing"}), 400

        if csrf_token_cookie != csrf_token_header:
            return jsonify({"error": "CSRF token mismatch"}), 400
        
    # Set CSRF token if it's missing in the cookie
    if not csrf_token_cookie:
        csrf_token = generate_csrf()
        response = make_response()
        response.set_cookie(
            'csrf_token',
            csrf_token,
            httponly=False,
            samesite='Lax',  # Use 'Strict' if you want stricter handling
            secure=False  # Set to True in production with HTTPS
        )
        return response


@app.route('/')
def landing_page():
    return "I am landing soon"

@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """ Handles the homepage of the app"""
    return "This is the home page"


if __name__ == "__main__":
    app.run(debug=True)