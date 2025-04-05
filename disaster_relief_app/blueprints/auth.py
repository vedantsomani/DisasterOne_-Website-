from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import db, User
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import random

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if user.mfa_enabled:
                mfa_code = str(random.randint(100000, 999999))
                session['mfa_code'] = mfa_code
                session['pending_user_id'] = user.id
                flash(f"Your MFA code is: {mfa_code}", "info")  # In production, send via SMS/email
                return redirect(url_for('auth.mfa'))
            else:
                login_user(user)
                flash("Logged in successfully", "success")
                return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@auth_bp.route('/mfa', methods=['GET', 'POST'])
def mfa():
    if request.method == 'POST':
        code = request.form.get('code')
        if code == session.get('mfa_code'):
            user_id = session.get('pending_user_id')
            from flask_login import login_user
            user = User.query.get(user_id)
            login_user(user)
            session.pop('mfa_code', None)
            session.pop('pending_user_id', None)
            flash("MFA verified, logged in!", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Incorrect MFA code", "danger")
    return render_template('mfa.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        mfa_enabled = request.form.get('mfa_enabled') == 'on'
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw, mfa_enabled=mfa_enabled)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful, please login", "success")
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    from flask_login import logout_user
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for('auth.login'))
