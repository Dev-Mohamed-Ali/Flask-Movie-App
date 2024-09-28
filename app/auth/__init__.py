from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db

bp = Blueprint('auth', __name__)

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
        username = request.form.get('username')
        password = request.form.get('password')

        # Input validation
        if not username or not password:
            flash('Both username and password are required.')
            return render_template('auth/login.html')

        # Check if user exists
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful.')
            next_page = request.args.get('next')  # Redirect to the page the user was trying to access before login
            return redirect(next_page or url_for('routes.index'))
        else:
            flash('Invalid username or password.')

    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
