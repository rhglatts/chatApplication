from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cs3800!'
chatapp = SocketIO(app)

#displays the index.html page when the address is set to / (aka default)
#index.html is our main chatroom page
@app.route('/')
def index():
    return render_template('index.html')

#recieves the messages and displays them
@chatapp.on('message')
def handle_message(message):
    #shows in terminal
    print('received message: ' + message)
    #for flask html side
    emit('message', message, broadcast=True)

#runs the flask app
if __name__ == '__main__':
    chatapp.run(app)
