from flask import Flask, request
from flask_mail import Mail, Message
from flask_cors import CORS
from models.users import db, bcrypt
from flask_migrate import Migrate
import os
from flask import jsonify, make_response
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager, get_jwt_identity
from models.users import User

jwt = JWTManager()
csrf = CSRFProtect()

# Flask app instance
app = Flask(__name__)


# Load configuration
from config import Config, TestConfig

# Load Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development').lower()
TESTING = os.getenv('TESTING', 'False').lower() == 'true'

if TESTING:
    app.config.from_object(TestConfig)
elif FLASK_ENV == 'production':
    app.config.from_object(Config)
else:
    app.config.from_object(Config)

# App initializations
cors = CORS(app, supports_credentials=True ,resources={r"/*": {"origins": "/*"}})
jwt.init_app(app)
bcrypt.init_app(app)
csrf.init_app(app)
mail = Mail(app)
mail.init_app(app)
migrate = Migrate(app, db)
db.init_app(app)
 
# Import blueprints
from routes.business import business_bp as business_bp
from routes.auth import auth_bp as auth_bp
from routes.reviews import review_bp as review_bp
from routes.products import products_bp as products_bp
from routes.generate_csrf import gen_csrf_bp as gen_csrf_bp
from routes.services import services_bp as services_bp
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
        # csrf_token = generate_csrf()
        response = make_response()
        response.set_cookie(
            'csrf_token',
            # csrf_token,
            httponly=False,
            samesite='Lax',  # Use 'Strict' if you want stricter handling
            secure=False  # Set to True in production with HTTPS
        )
        return response

# Landing page
@app.route('/')
def landing_page():
    """ This is the landing page for each first
    or registered users.(Current_user)
    """
    current_user = get_jwt_identity()
    if current_user:
        # Show personalized content for logged-in users
        return jsonify({
            "message": f"Welcome back, {current_user['username']}! You are now logged in."
        })
    else:
        # Show general content for unauthenticated users
        return jsonify({
            "message": "Welcome to our app! Please log in or sign up to get started."
        })

# Home page.
@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home():
    """ Handles the homepage of the app"""
    current_user = get_jwt_identity()
    if current_user:
        response = {
            "message": f"Welcome back, {current_user['username']}!",
            "authenticated": True
        }
    else:
        response = {
            "message": "Welcome, please log in to access more features.",
            "authenticated": False
        }
    return jsonify(response)

# Page not found error
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page not found"}), 404


# User lookup loader
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """Load user from JWT data."""
    user_id = jwt_data["sub"]  # `sub` contains the user ID in the JWT payload
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=False)