var socket = io();
/*   
creates a socket from the client (this html) to the server. 
then creates a listener with socket.onand when a message is sent, 
appends it to the list of messages and displays it 
*/
// AES ECB encryption key (must be 16 characters for AES128)
var encryptionKey = CryptoJS.enc.Utf8.parse('AAAAAAAAAAAAAAAA');

// Function to encrypt data using AES ECB mode
function encrypt(raw) {
    var encrypted = CryptoJS.AES.encrypt(raw, encryptionKey, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString();
}
// Function to decrypt data using AES ECB mode
function decrypt(encrypted) {
    var decrypted = CryptoJS.AES.decrypt(encrypted, encryptionKey, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return decrypted.toString(CryptoJS.enc.Utf8);
}

// Function to calculate SHA-256 hash
function calculateHash(data) {
    var hash = CryptoJS.SHA256(data).toString();
    console.log("client hash", hash);
    return hash;
}

// Listener for incoming messages
socket.on('message', function (encryptedMsg) {
    var li = document.createElement('li');
    li.textContent = encryptedMsg;
    document.getElementById('messages').appendChild(li);
});
/*
function sendMessage is called when the button is clicked. grabs text in box, 
clears text box,and sends message through socket to server
*/
function sendMessage() {
    var input = document.getElementById('input');
    var message = input.value;
    var messageHash = calculateHash(message); // Calculate hash of original message

    // Encrypt the message
    var encryptedMessage = encrypt(message);

    var data = {
        encrypted_message: encryptedMessage,
        message_hash: messageHash // Send hash of original message
    };

    input.value = '';
    socket.emit('message', data);
}

/*
Sends username to the server when button is pressed
*/
function sendUsername() {
    var usernameInput = document.getElementById('usernameInput');
    var username = usernameInput.value.trim();
    if (username) {
        var encryptedUsername = encrypt(username);
        socket.emit('set_username', encryptedUsername);
        usernameInput.value = '';
    }
}
