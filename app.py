import os
from datetime import datetime
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


@app.route('/')
def get_posts():
    connection = get_flask_database_connection(app)
    repository = PostRepository(connection)
    posts = repository.all()
    return render_template('posts/index.html', posts=posts)

# This route simply returns the login page
@app.route('/login')
def login():
    if not session.get("user_id"):
        return render_template('users/login.html')
    return redirect('/account_page')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('users/logout.html')

# This route receives login information (email and password) as POST parameters,
# checks whether the credentials are valid, and if so finds the user in the database
# using the email. If all goes well, it stores the user's ID in the session
# and shows a success page.
@app.route('/login', methods=['POST'])
def login_post():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    email = request.form['email']
    password = request.form['password']
    if repository.check_password(email, password):
        user = repository.find_by_email(email)
        # Set the user ID in session
        session['user_id'] = user.id
        return redirect('/account_page')
    else:
        return render_template('users/login_error.html')

@app.route('/signup')
def signup():
    return render_template('users/signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    email = request.form['email']
    password = sanitizer.sanitize(request.form.get('password'))
    username = sanitizer.sanitize(request.form.get('username'))
    # You already have an account!
    if repository.find_by_email(email) is not None:
        return render_template('users/account_exists.html')
    # check email and password are valid
    if repository.validity_checker(email, password) == False:
        return render_template('users/signup_error.html')
    # check username is unique
    if repository.check_username_unique(username) == False:
        return render_template('users/username_not_unique.html')

    # Create account
    else:
        user = User(None, email, password, username)
        repository.create(user)
        session['user_id'] = user.id
        return render_template('users/signup_success.html')

# This route is an example of a "authenticated-only" route. It can be accessed 
# only if a user is signed-in (if we have user information in session).
@app.route('/account_page')
def account_page():
    connection = get_flask_database_connection(app)
    repository = PostRepository(connection)
    if 'user_id' not in session:
        # No user id in the session so the user is not logged in.
        return redirect('/login')
    else:
        # The user is logged in, display their account page.
        user_id = session['user_id']
        posts = repository.find_by_user(user_id)
        return render_template('users/account.html', posts=posts)

@app.route('/account_post', methods=['POST'])
def account_post():
    connection = get_flask_database_connection(app)
    repository = PostRepository(connection)
    # sanitize user input
    message = sanitizer.sanitize(request.form.get('message'))
    tag = sanitizer.sanitize(request.form.get('tag'))
    email = repository.find_email_by_username(tag)
    # create a post object
    t = datetime.now()
    time = t.strftime("%H:%M:%S")
    user_id = session['user_id']
    username = repository.find_username_with_userid(user_id)
    post = Post(None, message, time, user_id, username)
    # if another user is tagged in their post notify them with an email
    if email is not None:
        msg = Message(subject='You were tagged in a post on Chitter', body=f'{username} tagged you in their post. Here is what they wrote:\n\n{message}', sender = 'hello@chitter.com', recipients = [f'{email}'])
        mail.send(msg)  
    repository.create(post)
    return redirect('/')


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
