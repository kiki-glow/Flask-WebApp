from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
import bcrypt
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24).hex())  # Set a default for development

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.flask_db
users_collection = db.users
contacts_collection = db.contacts
messages_collection = db.messages  # New collection for chat messages

# Flask-Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# SocketIO setup
socketio = SocketIO(app)

# Routes
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        # Check if user already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        # Hash the password and store it
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = users_collection.find_one({'username': username})

        if user and bcrypt.checkpw(password, user['password']):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = users_collection.find_one({'email': email})

        if user:
            token = str(ObjectId())
            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
            msg.body = f'Click the link to reset your password: {reset_link}'
            mail.send(msg)
            flash('Password reset email sent', 'success')
        else:
            flash('No user found with that email address', 'danger')

    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
        # Update user's password
        flash('Password updated successfully', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if 'user' in session:
        if request.method == 'POST':
            mobile = request.form['mobile']
            email = request.form['email']
            address = request.form['address']
            reg_number = request.form['reg_number']

            contacts_collection.insert_one({
                'mobile': mobile,
                'email': email,
                'address': address,
                'reg_number': reg_number,
                'user': session['user']
            })
            flash('Contact added successfully', 'success')
            return redirect(url_for('index'))

        return render_template('contact_form.html')
    else:
        return redirect(url_for('login'))

@app.route('/search_contact', methods=['GET', 'POST'])
def search_contact():
    if 'user' in session:
        if request.method == 'POST':
            reg_number = request.form['reg_number']
            contact = contacts_collection.find_one({'reg_number': reg_number, 'user': session['user']})

            if contact:
                return render_template('search_contact.html', contact=contact)
            else:
                flash('Contact not found', 'danger')

        return render_template('search_contact.html')
    else:
        return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    else:
        return redirect(url_for('login'))


# WebSocket Event Handlers
@socketio.on('message')
def handle_message(msg):
    """Handle incoming messages from clients."""
    print(f"Received message: {msg}")
    # Save the message to MongoDB
    messages_collection.insert_one({"message": msg, "user": session.get('user', 'Anonymous')})
    # Broadcast the message to all connected clients
    emit('response', {'user': session.get('user', 'Anonymous'), 'message': msg}, broadcast=True)


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print("Client connected")
    emit('response', {'user': 'Server', 'message': 'A new user has connected!'}, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print("Client disconnected")


# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    socketio.run(app, debug=True)
