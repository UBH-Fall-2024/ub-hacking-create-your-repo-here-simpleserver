from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note



auth = Blueprint('auth', __name__)



@auth.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = request.form.get("message")
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if len(message) > 0:
            if user:
                flash("Valid email!", category='success')
                new_note = Note(data=message + "  -From: " + current_user.email, user_id=user.id)
                db.session.add(new_note)
                db.session.commit()
            else:
                flash("Invalid email. Not found in system.", category='error')
        else:
            flash("Invalid message. Maybe try typing something?", category='error')


    return render_template("contact.html", user = current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category = 'error')
        else:
            flash('Email does not exist.', category='error')


    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category ='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category ='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category ='error')
        elif len(password1) < 7:
            flash('Pasword must be at least 7 characters.', category ='error')
        else:
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
            print(hashed_password)
            db.create_all()
            new_user = User(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category ='success')
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user = current_user)