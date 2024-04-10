from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cs3800!'
chatapp = SocketIO(app)

# this is the new route for the home screen
@app.route('/')
def home():
    return render_template('home.html')

# this is the updated route for the chatroom now under '/chatroom'
@app.route('/chatroom')
def chatroom():
    return render_template('index.html')

usernames = {}

# receives the messages and displays them
@chatapp.on('message')
def handle_message(message):
    session_id = request.sid
    username = usernames.get(session_id, 'Anonymous')
    # shows in terminal
    print(f'{username}: {message}')
    # for flask html side
    emit('message', f'{username}: {message}', broadcast=True)

# Gets username from HTML and binds username to session id in dictionary
@chatapp.on('set_username')
def set_username(username):
    session_id = request.sid
    usernames[session_id] = username

# runs the flask app
if __name__ == '__main__':
    chatapp.run(app, host='0.0.0.0', port=80)
