from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required

from app import db
from app.auth import bp
from app.models import User


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Input validation
        if not username or not email or not password:
            flash('All fields are required.')
            return render_template('auth/register.html')

        # Check if the user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose a different one.')
            return render_template('auth/register.html')

        try:
            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)

            # Add user to database
            db.session.add(user)
            db.session.commit()

            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))

        except Exception as e:
            # Handle any errors during database operations
            db.session.rollback()
            flash(f'An error occurred during registration: {str(e)}')
            return render_template('auth/register.html')

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the JSON data from the request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Check if user exists
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            # Get the 'next' argument or redirect to the default page after login
            next_page = request.args.get('next') or url_for('main.index')

            return jsonify({"status": "success", "next_page": next_page}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
