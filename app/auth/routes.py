from flask import redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required

from app import db
from app.auth import bp
from app.models import User


@bp.route('/register', methods=['POST'])
def register():
    # Check if the request is a POST
    if request.method == 'POST':
        # Get data from the request
        username = request.form.get('name')  # Changed 'username' to 'name' to match AJAX data
        email = request.form.get('email')
        password = request.form.get('password')

        # Input validation
        if not username or not email or not password:
            return jsonify({"status": "error", "message": "All fields are required."}), 400  # Return error with 400 status

        # Check if the user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({"status": "error", "message": "Username or email already exists. Please choose a different one."}), 400  # Return error with 400 status

        try:
            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)

            # Add user to database
            db.session.add(user)
            db.session.commit()

            return jsonify({"status": "success", "message": "Registration successful. Please log in."}), 201  # Successful registration

        except Exception as e:
            # Handle any errors during database operations
            db.session.rollback()
            return jsonify({"status": "error", "message": f"An error occurred during registration: {str(e)}"}), 500  # Return error with 500 status



@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            # Get the 'next' argument or redirect to the default page after login
            next_page = request.args.get('next') or url_for('main.index')

            return jsonify({"status": "success", "next_page": next_page}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
