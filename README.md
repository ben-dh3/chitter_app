# Chitter App
Created to illustrate learning on test driven development, postgreSQL, security.
* Home page
    * Using postgreSQL to fetch a list of user posts.
    * Styling created with Tailwind CSS.
* Sign up to Chitter. 
    * Created a regex to ensure only secure passwords are accepted by the user. 
    * Regex ensures only valid email addresses are accepted. 
    * Username must be unique, database is checked to ensure this.
    * Password and username inputs are sanitized using html-sanitizer for security.
    * On successful sign up the user is automatically logged in. The session is remembered until you log out on your account page.
    * If the sign up is unsuccessful, the user is notified and reminded of the password rules.
    * If the username is not unique, the user is notified.
    * If a user has already signed up with that email, the user is notified that the account already exists.
* Account page.
    * See a list of your previous posts in reverse chronological order.
    * Create a new post and optionally tag another user. Created using Flask Mail and Mailtrap, an email is sent from Chitter to the tagged user notifying them that "username" has tagged them in a post, with their message quoted in the body of the email.
    * Log out button clears the session making it necessary to sign back in.

*In the future I intend to improve the UI by adding styling to the error pages. I also intend to add the ability for a user to retrieve a forgotten password by email.*

*Next I intend to implement CICD with github actions and hosting the website using a cloud services provider.*
## Setup

```shell

# Install dependencies and set up the virtual environment
; pipenv install

# Activate the virtual environment
; pipenv shell

# Create a test and development database
; createdb YOUR_PROJECT_NAME
; createdb YOUR_PROJECT_NAME_test

# Open lib/database_connection.py and change the database names
; open lib/database_connection.py

# Seed the development database (ensure you have run `pipenv shell` first)
; python seed_dev_database.py

# Run the tests (with extra logging)
; pytest -sv

# Run the app
; python app.py
# Now visit http://localhost:5001/ in your browser
```