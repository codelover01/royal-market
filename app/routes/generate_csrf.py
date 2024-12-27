from flask import Blueprint, jsonify, request, make_response
from flask_wtf.csrf import CSRFProtect, generate_csrf
csrf = CSRFProtect()

gen_csrf_bp = Blueprint('gen_csrf', __name__, url_prefix='/gen_csrf')


@gen_csrf_bp.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    """
    Generate CSRF token and set it in a secure cookie with SameSite attribute.
    """
    csrf_token = generate_csrf() # Generate CSRF token
    response = make_response(jsonify({'message': 'CSRF token set'}))
    response.set_cookie(
        'csrf_token', csrf_token, max_age=None , samesite=None, secure=True, httponly=True  # Secure=True for HTTPS
    )
    return response


@gen_csrf_bp.before_request
def csrf_protect():
    """
    CSRF Protection: Verify CSRF token both from cookies and headers (Double Submit Cookie pattern).
    """
    if request.method in ['POST', 'PUT', 'DELETE']:
        csrf_token_cookie = request.cookies.get('csrf_token')
        csrf_token_header = request.headers.get('X-CSRFToken')

        if not csrf_token_cookie or not csrf_token_header:
            return jsonify({"error": "CSRF token missing"}), 400
        if csrf_token_cookie != csrf_token_header:
            return jsonify({"error": "CSRF token mismatch"}), 400


@gen_csrf_bp.after_request
def apply_csp(response):
    """
    Apply a strong Content Security Policy (CSP) to block external scripts and mitigate XSS attacks.
    """
    response.headers["Content-Security-Policy"] = (
        "script-src 'self' 'strict-dynamic'; object-src 'none';"
    )
    return response