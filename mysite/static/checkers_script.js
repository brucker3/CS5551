/*----------- Game State Data ----------*/
//top left box is blank, number start from top left to end at bottom right numbers from 1 to 32 OR if using array 0 to 31
//every piece has id 1 to 12 with there color code in front e.g. D4 (dark 4)(L for light side; D fro dark side)
//top side of game is always light side
//element of of array are in string format
//if piece id is end by K e.g. "L11K" that means it is king
/* board positon look like
.	1	.	2	.	3	.	4
5	.	6	.	7	.	8	.
.	9	.	10	.	11	.	12
13	.	14	.	15	.	16	.
.	17	.	18	.	19	.	20
21	.	22	.	23	.	24	.
.	25	.	26	.	27	.	28
29	.	30	.	31	.	32	.
*/

//initialize variables and empty board				
let selected_piece, recieved_data={};
let vue_board = [];
initialize_board();

//Initialize game socket
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const gameSocket = new WebSocket( 'ws://' + window.location.host + '/ws/game/' + roomName + '/' );

//function which called when message is recieved
gameSocket.onmessage = function(e) {
	let data = JSON.parse(e.data);
	console.log(data);
	data = (data['message']);

	recieved_data = format_incoming_data(data);
	
	recieved_data = {
			1:['L1'], 2:['L2'], 3:['L3'], 4:['L4'],
			5:['L5'], 6:['L6'], 7:['L7'], 8:['L8'],
			9:['L9',13,14], 10:['L10',14,15], 11:['L11K',15,16], 12:['L12',16],
			13:['X'], 14:['X'], 15:['X'], 16:['X'],
			17:['X'], 18:['X'], 19:['X'], 20:['X'],
			21:['D1',17], 22:['D2',17,18], 23:['D3K',18,19], 24:['D4'],
			25:['D5'], 26:['D6'], 27:['D7'], 28:['D8'],
			29:['D9'], 30:['D10'], 31:['D11'], 32:['D12']
			};

	update_board(recieved_data);
	function verify_recived_data(input_dictionary){
		//Complete this function
		return 0
	}	

};

//function when socket is closed
gameSocket.onclose = function(e) {
	console.error('Game socket closed unexpectedly');
};

/*
following recived data is dictionary object which will be communicated between serve and client in order to sync game
key of the dictionary is position of board square and value is array which contain piece id as first element and 
other element as its possible moves.
*/



function initialize_board(){
	for (var i=1; i<=32; i++){
		var position = "#position-"+i.toString();
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
	}
}

function format_incoming_data(data){
	var temp_data = {};
	for (var i=0; i<data.length; i++){
		if (data[i]=='.'){
			temp_data[i+1]=['X'];
		} else if (data[i]=='x'){
			temp_data[i+1]=['D'+i];					
		} else if (data[i]=='X'){
			temp_data[i+1]=['D'+i+'K'];					
		} else if (data[i]=='y'){
			temp_data[i+1]=['L'+i];					
		} else if (data[i]=='Y'){
			temp_data[i+1]=['L'+i+'K'];					
		}
	}
	return temp_data
}

function update_board(recieved_data){
	//create vue object for every position and use that object to manipulate output
	if (selected_piece != null) {
			selected_piece.selection = 'not-selected';
			hide_possible_squares()
	}
	
	for (var i in recieved_data){
	// console.log(i,recieved_data[i]);
		if (recieved_data[i][0].includes('K')){
			vue_board[i-1].piece_type = "king";
		}
		else if (recieved_data[i][0].includes('X')){
			vue_board[i-1].piece_color= 'empty';
			vue_board[i-1].piece_type= 'empty';
			vue_board[i-1].selection= 'not-selected';
			vue_board[i-1].possible_square= 'not-possible-move';
		}
		else{
			vue_board[i-1].piece_type = "normal";
		}
		
		if (recieved_data[i][0].includes('L')){
			vue_board[i-1].piece_color = 'light-piece';
		}
		else if (recieved_data[i][0].includes('D')){
			vue_board[i-1].piece_color = 'dark-piece';
		}
		
		vue_board[i-1].select_piece = function (event){
			// console.log(event.target);
			if (selected_piece != null) {
				selected_piece.selection = 'not-selected';
				hide_possible_squares()
			}
			var position_number = parseInt(event.target.id.split("-")[1]);
			console.log(recieved_data[position_number],i);
			if (recieved_data[position_number].length>1){
				this.selection = 'selected';
				selected_piece = this;
				for (var j =1;j<recieved_data[position_number].length;j++){
					target_position = recieved_data[position_number][j];
					show_possible_square(target_position, position_number);
				}
			}
		}
		
	}
}


function show_possible_square(target_position,current_position){
	vue_board[target_position-1].possible_square = "possible-move";
	/*add move function here where possible moves are shown on board*/
	vue_board[target_position-1].select_piece = function(event){
		console.log(current_position+'-'+target_position);
		
		recieved_data[target_position] = [recieved_data[current_position][0]];
		recieved_data[current_position] = ['X'];
		
		gameSocket.send(JSON.stringify({
			'message': current_position+'-'+target_position,
			'room-name':roomName
		}));
		update_board(recieved_data);
	}	
}

function hide_possible_squares(){
	for (var k=0;k<vue_board.length;k++){
		vue_board[k].possible_square = 'not-possible-move';
	}
	
}

	








