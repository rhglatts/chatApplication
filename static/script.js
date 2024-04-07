var socket = io();
/*   
creates a socket from the client (this html) to the server. 
then creates a listener with socket.onand when a message is sent, 
appends it to the list of messages and displays it 
*/
socket.on('message', function(msg){
    var li = document.createElement('li');
    li.textContent = msg;
    document.getElementById('messages').appendChild(li);
});

/*
function sendMessage is called when the button is clicked. grabs text in box, 
clears text box,and sends message through socket to server
*/
function sendMessage(){
    var input = document.getElementById('input');
    var message = input.value;
    input.value = '';
    socket.emit('message', message);
}

/*
Sends username to the server when button is pressed
*/
function sendUsername(){
    var usernameInput = document.getElementById('usernameInput');
    var username = usernameInput.value.trim(); 
    if (username) {
        socket.emit('set_username', username);
        usernameInput.value = '';
    }
}

