from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import LoginForm, UserCreationForm
#import login functionality
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash


from app.models import User, db #connecting your MODELS Class, how to draw data from your SQL

auth = Blueprint('auth', __name__, template_folder='authtemplates')

@auth.route('/login', methods=["GET", "POST"])
def logMeIn():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == "POST": 
        if form.validate():
            username = form.username.data
            password = form.password.data
            #Query user based off of our username
            user = User.query.filter_by(username=username).first()
            if user:
                #compare passwords
                if check_password_hash(user.password, password):
                    flash('You have successfully logged in!', 'success')
                    login_user(user)
                    return redirect(url_for('shop.getAllProducts'))
                else:
                    flash('Incorrect username/password combination.', 'danger')
            else:
                flash('User with that username does not exist.', 'danger')

    return render_template('login.html', form = form)

@auth.route('/logout')
@login_required
def logMeOut():
    flash('Successfully logged out', 'success')
    logout_user()
    return redirect(url_for('auth.logMeIn'))


@auth.route('/signup', methods = ["GET", "POST"])
def signMeUp():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserCreationForm() #the form I want access for this page
    if request.method == "POST": 
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            #Add USER to Database
            user = User(username, email, password)

            #Add INSTANCE to Database
            db.session.add(user)
            db.session.commit()

            flash('Successfully registered a new user!', 'success')
            return redirect(url_for('auth.logMeIn'))
        else:
            flash('Invalid form. Please try again', 'danger')
    return render_template('signup.html', form = form)


# -----------------------------------REACT ROUTES ===================================#

@auth.route('/api/signup', methods=["POST"])
def apiSignMeUp():
    data = request.json
     
    username = data['username']
    email = data['email']
    password = data['password']

    # add user to database
    user = User(username, email, password)

    # add instance to our db
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'ok',
        'message': f"Successfully created user {username}"
    }


from app.apiauthhelper import basic_auth, token_auth

@auth.route('/token', methods=['POST'])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
                'status': 'ok',
                'message': "You have successfully logged in",
                'data':  user.to_dict()
            }
