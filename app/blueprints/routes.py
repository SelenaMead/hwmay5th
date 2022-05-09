from flask import render_template, current_app as app, request, redirect, url_for, flash
from datetime import datetime as dt
from app.blueprints.models import  User
from app import db
from flask_login import current_user, login_required, login_user, logout_user

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = request.form
        user = User.query.filter_by(email=form_data.get('email')).first()
        
        if user is None or not user.check_password(form_data.get('password')):
            return redirect(url_for('login'))
        
        login_user(user)
        
        return redirect(url_for('profile'))
    return render_template('main/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form
        
        email = User.query.filter_by(email=form_data.get('email')).first()
        if email is not None:
            flash('That email address is already in use. Please try another one.', 'warning')
            return(redirect(url_for('register')))
        if form_data.get('password') == form_data.get('confirm_password'):
            user = User(
                first_name=form_data.get('first_name'),
                last_name=form_data.get('last_name'),
                email=form_data.get('email')
            )
            user.generate_password(form_data.get('password'))
            db.session.add(user)
            db.session.commit()


            
            flash('You have registered successfully', 'success')
            return redirect(url_for('login'))
        else:
            flash("Your passwords don't match. Please try again.", 'warning')
            return redirect(url_for('register'))
    
    
    return render_template('main/register.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        form_data = request.form

        user = User.query.get(current_user.get_id())
        user.first_name = form_data.get('first_name')
        user.last_name = form_data.get('last_name')
        user.email = form_data.get('email')

        if len(form_data.get('password')) == 0:
            pass
        elif form_data.get('password') == form_data.get('confirm_password'):
            user.generate_password(form_data.get('password'))
        else:
            flash('There was an error updating your password', 'danger')
            return redirect(url_for('profile'))

        db.session.commit()
    
        flash('You have updated your information', 'primary')
        return redirect(url_for('profile'))

    if request.method == 'DELETE':
        print('hello')
        button_data= request.form
        user = User.query.filter_by(current_user.get_id())
        if user.first_name == button_data.get('first_name'):
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('register'))

    return render_template('main/profile.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
