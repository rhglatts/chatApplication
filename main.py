import hashlib
import base64
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cs3800!'
chatapp = SocketIO(app)

# AES ECB encryption key (must be 16 characters for AES128)
encryption_key = 'AAAAAAAAAAAAAAAA'

# Function to encrypt data using AES ECB mode
def encrypt(raw):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(encryption_key.encode('utf-8'), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))

# Function to decrypt data using AES ECB mode
def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(encryption_key.encode('utf-8'), AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16)

# Function to calculate SHA-256 hash
def calculate_hash(data):
    print("server hash:", hashlib.sha256(data.encode()).hexdigest())
    return hashlib.sha256(data.encode()).hexdigest()

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
    encrypted_message, message_hash = message['encrypted_message'], message['message_hash']
    
    # Decrypt the message
    decrypted_message = decrypt(encrypted_message).decode("utf-8", "ignore")
    
    # Verify message integrity
    if calculate_hash(decrypted_message) == message_hash:
        # shows in terminal
        print("decrypted message:")
        print(f'{username}: {decrypted_message}')
        # for flask html side
        emit('message', f'{username}: {decrypted_message}', broadcast=True)
    else:
        print("Message integrity compromised")

# Gets username from HTML and binds username to session id in dictionary
@chatapp.on('set_username')
def set_username(username):
    session_id = request.sid
    username = decrypt(username).decode("utf-8", "ignore")
    usernames[session_id] = username

# runs the flask app
if __name__ == '__main__':
    chatapp.run(app, host='0.0.0.0', port=80)

