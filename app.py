import os
from datetime import datetime, timezone
from html_sanitizer import Sanitizer
from flask import Flask, request, render_template, session, redirect
from flask_mail import Mail, Message
from lib.database_connection import get_flask_database_connection
from lib.user_repository import *
from lib.user import *
from lib.post_repository import *
from lib.post import *

mail = Mail()
# Create a new Flask app
app = Flask(__name__)

sanitizer = Sanitizer()
app.secret_key = os.environ.get('SECRET_KEY') or 'you-cannot-guess'
# flask mail
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail.init_app(app)

# return the landing page with login form and signin page link
@app.route('/', methods=['GET', 'POST'])
def landingpage():
    if request.method == 'GET':
        if not session.get("user_id"):
            return render_template('landingpage.html')
        return redirect('/feed')
    else:
        connection = get_flask_database_connection(app)
        repository = UserRepository(connection)

        email = request.form['email']
        password = request.form['password']
        if repository.check_password(email, password):
            user = repository.find_by_email(email)
            # Set the user ID in session
            session['user_id'] = user.id
            return redirect('/feed')
        else:
            # return the same page with errors populated
            error = 'Password or email incorrect.'
            return render_template('landingpage.html', error=error)

# feed page shows posts, new post form, and logout button
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if request.method == 'GET':
        if 'user_id' not in session:
        # No user id in the session so the user is not logged in.
            return redirect('/')
        else:
            connection = get_flask_database_connection(app)
            repository = PostRepository(connection)
            posts = repository.all()
            return render_template('feed.html', posts=posts)
    else:
        connection = get_flask_database_connection(app)
        repository = PostRepository(connection)
        # sanitize user input
        message = sanitizer.sanitize(request.form.get('message'))
        tag = sanitizer.sanitize(request.form.get('tag'))
        email = repository.find_email_by_username(tag)
        # create a post object
        t = datetime.now(timezone.utc)
        time = t.isoformat()
        user_id = session['user_id']
        username = repository.find_username_with_userid(user_id)
        post = Post(None, message, time, user_id, username)
        # if another user is tagged in their post notify them with an email
        if email is not None:
            msg = Message(subject='You were tagged in a post on Chitter', body=f'{username} tagged you in their post. Here is what they wrote:\n\n{message}', sender = 'hello@chitter.com', recipients = [f'{email}'])
            mail.send(msg)  
        repository.create(post)
        return redirect('/feed')

@app.route('/logout')
def logout():
    session.clear()
    # when logged out return to landing page
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', error=None)
    else:
        connection = get_flask_database_connection(app)
        repository = UserRepository(connection)

        email = request.form['email']
        password = sanitizer.sanitize(request.form.get('password'))
        username = sanitizer.sanitize(request.form.get('username'))

        # You already have an account!
        if repository.find_by_email(email) is not None:
            error = 'You already have an account with this email.'
            return render_template('signup.html', error=error)
        
        # Check email and password are valid
        if not repository.validity_checker(email, password):
            error = 'Invalid email or password.'
            return render_template('signup.html', error=error)
        
        # Check username is unique
        if not repository.check_username_unique(username):
            error = 'Username is already taken.'
            return render_template('signup.html', error=error)
        
        # Create account
        user = User(None, email, password, username)
        repository.create(user)
        session['user_id'] = user.id
        return render_template('signup_success.html')

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
