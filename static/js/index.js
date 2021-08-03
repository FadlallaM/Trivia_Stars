//for solo play
function on() {
    document.getElementById("overlay").style.display = "block";
}
  
function off() {
    document.getElementById("overlay").style.display = "none";
}


//For create multiplayer
function on_1() {
    document.getElementById("overlay_1").style.display = "block";
}
  
function off_1() {
    document.getElementById("overlay_1").style.display = "none";
}


//For join game
function on_2() {
    document.getElementById("overlay_2").style.display = "block";
}
  
function off_2() {
    document.getElementById("overlay_2").style.display = "none";
}


//Websockets for multiplayer
//function to start the quiz
//const newGameBtn = document.getElementById('create_game');
//const joinGameBtn = document.getElementById('join_game');
//create game session

var socket = io()
var $startForm = $('#create_game_id')
var $closebutton = $('#closebtn')
var $newRoomField = $('#createCodeInput')
var $beginButton = $('#begin')
var $panel = $('#panel')
var newData = { room: null }


$('body').addClass('body--admin')



$startForm.on('submit', function(event) {
    event.preventDefault()
    newData.room = $newRoomField.val()
    
    socket.emit('create', newData)
});

socket.on('create', function(success) {
    if (success) {
        $closebutton.hide()
        $startForm.hide()
        $panel.show()
    }
    else {
        alert('That room is taken')
    }
});

$beginButton.on('click', async function() { 
    let reset_data = newData
    socket.emit('reset', reset_data)
    window.location = '/quiz' + newData.room
});


//Join game session
var $joinForm = $('#join_game_id')
var $roomField = $('#gameCodeInput')
var data = { room: null }
$('body').addClass('center')

$joinForm.on('submit', function(event) {
  event.preventDefault()
  data.room = $roomField.val()
  
  socket.emit('exists', data)
})

socket.on('exists', function(exists) {
  if (exists) {
    window.location = '/quiz' + data.room
  }
  else {
    alert('That game doesn\'t exist!')
  }
})

//join game session 
