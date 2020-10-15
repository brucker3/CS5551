/*----------- Game State Data ----------*/
//top left box is blank, number start from top left to end at bottom right numbers from 1 to 32 OR if using array 0 to 31
//every piece has id 1 to 12 with there color code in front e.g. D4 (dark 4)(L for light side; D fro dark side)
//top side of game is always light side
//element of of array are in string format
//if piece id is end by K e.g. "L11K" that means it is king


//following about data recieving and sending
const roomName = JSON.parse(document.getElementById('room-name').textContent);
        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/game/'
            + roomName
            + '/'
        );

        chatSocket.onmessage = function(e) {
            let data = JSON.parse(e.data);
            document.querySelector('#game-log').value += (data.message + '\n');
			data = (data['message']);
			////
			var recieved_data = {};
			for (var i=0; i<data.length; i++){
				if (data[i]=='.'){
					recieved_data[i+1]=['X'];
				} else if (data[i]=='x'){
					recieved_data[i+1]=['D'+i];					
				} else if (data[i]=='X'){
					recieved_data[i+1]=['D'+i+'K'];					
				} else if (data[i]=='y'){
					recieved_data[i+1]=['L'+i];					
				} else if (data[i]=='Y'){
					recieved_data[i+1]=['L'+i+'K'];					
				}
			}
// var recieved_data = {
					// 1:['L1'], 2:['L2'], 3:['L3'], 4:['L4'],
					// 5:['L5'], 6:['L6'], 7:['L7'], 8:['L8'],
					// 9:['L9',13,14], 10:['L10',14,15], 11:['L11K',15,16], 12:['L12',16],
					// 13:['X'], 14:['X'], 15:['X'], 16:['X'],
					// 17:['X'], 18:['X'], 19:['X'], 20:['X'],
					// 21:['D1',17], 22:['D2',17,18], 23:['D3K',18,19], 24:['D4'],
					// 25:['D5'], 26:['D6'], 27:['D7'], 28:['D8'],
					// 29:['D9'], 30:['D10'], 31:['D11'], 32:['D12']
					// };
console.log(recieved_data);					
let selected_piece;
let vue_board = [];

//create vue object for every position and use that object to manupulate output
function verify_recived_data(input_dictionary){
	//Complete this function
	return 0
}					
var i;
for (i=1;i<=Object.keys(recieved_data).length;i++){
	// console.log(i,recieved_data[i]);
	var position = "#position-"+i.toString();
	if (recieved_data[i][0].includes('X')){
		var temp = new Vue({
			el:position,
			data: {
				piece_color: 'empty',
				piece_type: 'empty',
				selection: 'not-selected',
				possible_square: 'not-possible-move'
				},
			methods: {
				select_piece:function (event){}
			}
		})
		vue_board.push(temp);
		continue;
	}
	else{
		if (recieved_data[i][0].includes('K')){
			var type = "king";
		}
		else{
			var type = "normal";
		}
		
		if (recieved_data[i][0].includes('L')){
			var color = 'light-piece';
		}
		else{
			var color = 'dark-piece';
		}
	
	var temp = new Vue({
		el:position,
		data: {
			piece_color: color,
			piece_type: type,
			selection: 'not-selected',
			possible_square: 'not-possible-move'
			},
		methods: {
			select_piece:function (event){
				// console.log(event.target);
				if (selected_piece != null) {
					selected_piece.selection = 'not-selected';
					hide_possible_squares()
					}
				
				var position_number = parseInt(event.target.id.split("-")[1]);
				console.log(recieved_data[position_number]);
				if (recieved_data[position_number].length>1){
					this.selection = 'selected';
					selected_piece = this;
					
					for (var j =1;j<recieved_data[position_number].length;j++){
						position = recieved_data[position_number][j];
						show_possible_square(position);
					}
				}
			}
		}
	})
	
	vue_board.push(temp);
	}
}
////////////////////			
			
        };

        chatSocket.onclose = function(e) {
            console.error('Game socket closed unexpectedly');
        };

        document.querySelector('#game-message-input').focus();
        document.querySelector('#game-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#game-message-submit').click();
            }
        };

        document.querySelector('#game-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#game-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
/*
following recived data is dictionary object which will be communicated between serve and client in order to sync game
key of the dictionary is position of board square and value is array which contain piece id as first element and 
other element as its possible moves.
*/


function show_possible_square(position){
	vue_board[position-1].possible_square = "possible-move";
	/*add move function here where possible moves are shown on board*/
	// vue_board[position-1].select_piece = function(){}
	
}

function hide_possible_squares(){
	for (var k=0;k<vue_board.length;k++){
		vue_board[k].possible_square = 'not-possible-move';
	}
	
}

	








