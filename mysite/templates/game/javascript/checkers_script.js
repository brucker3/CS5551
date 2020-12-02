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
const gameId = JSON.parse(document.getElementById('game-id').textContent);
let gameSocket = new ReconnectingWebSocket( 'ws://' + window.location.host + '/ws/game/' + gameId + '/' );

console.log(yourUsername);
gameSocket.onopen = function(e){
	$('.main').css('display','block'); //show whole table on loss of connection
	$('#network-error').css('display','none'); //hide error message on loss of connection
}

//function which called when message is recieved
gameSocket.onmessage = function(e) {
	let data = JSON.parse(e.data);
	//console.log(data['player1_username'],data['player2_username']);
	//console.log(data); // print incoming data from backend
	var board = JSON.parse(data['message']);
	var moves = data['moves'];
	var sel_piece = data['selected_piece'];
	hide_possible_squares();
	update_board(board);
	// show_turn_text(data['turn']);
	show_moves(board,moves,sel_piece);
	update_turn_text(data.turn);
	if (check_for_winner(data['winner'])){
		update_winner_ui(data['winner'],data['player1_username'],data['player2_username']);
	}
		
	add_username_to_turn_text(data['player1_username'],data['player2_username']);
	change_board_orientation(yourUsername, data['player1_username'],data['player2_username'])
};

//function when socket is closed
gameSocket.onclose = function(e) {
	// add something which shows to user that network connection is broken
	//console.error('Game socket closed unexpectedly');
	$('.main').css('display','none'); //hide whole table on loss of connection
	$('#network-error').text('Please Check your network connection!');
	$('#network-error').css({'display':'block', 'color':'red'}); //show error message on loss of connection
};


let translation_dict = {};var k =1;for (var i=0; i<8; i++){	for (var j=0; j<8; j++){if (((j+i))%2!=0){translation_dict[k]=[j,i];k+=1;}}}

function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] == value);
}

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

function show_moves(board, moves, sel_piece){
	if (sel_piece!= null){		
		vue_board[sel_piece-1].selection = 'selected';
		selected_piece = vue_board[sel_piece-1];
		for (var i in moves){
			show_possible_square(moves[i],sel_piece)
		}
	}
}

function update_board(recieved_data){
	//create vue object for every position and use that object to manipulate output
		
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
			if (selected_piece != null) {
				selected_piece.selection = 'not-selected';
				hide_possible_squares()
			}
			var position_number = parseInt(event.target.id.split("-")[1]);
			gameSocket.send(JSON.stringify({
				'message': translation_dict[position_number],
				'selected_piece' : translation_dict[position_number],
				'game_id':gameId,
			}));
			
		}
		
	}
}


function update_turn_text(turn_text_letter){
	if (turn_text_letter=="D"){
		$('.dark-turn-text').css('color','black');
		$('.light-turn-text').css('color','lightgray');
	}
	else if (turn_text_letter=="L"){
		$('.light-turn-text').css('color','black');
		$('.dark-turn-text').css('color','lightgray');
	}
}

function add_username_to_turn_text(player1_username, player2_username){
	$('.dark-turn-text').text("Dark's turn ("+player1_username+")");
	if (player2_username==''){
		$('.light-turn-text').text("Light's turn (Waiting for other player to join)");
	}else{
		$('.light-turn-text').text("Light's turn ("+player2_username+")");
	}
}


function show_possible_square(target_position,current_position){
	vue_board[target_position-1].possible_square = "possible-move";
	/*add move function here where possible moves are shown on board*/
	vue_board[target_position-1].select_piece = function(event){
		gameSocket.send(JSON.stringify({
				'message': translation_dict[target_position],
				'selected_piece' : translation_dict[current_position],
				'game_id':gameId
			}));
		hide_possible_squares();
	}	
}

function hide_possible_squares(){
	for (var k=0;k<vue_board.length;k++){
		vue_board[k].possible_square = 'not-possible-move';
		vue_board[k].selection = 'not-selected';
	}
}

function change_board_orientation(username, player1_username, player2_username){
	//default is player1 as dark is down side
	if(username==player2_username){
		$("table").css({
			"-webkit-transform": "scale(-1)",
			"-moz-transform": "scale(-1)",
			"-ms-transform": "scale(-1)",
			"-o-transform": "scale(-1)",
			"transform": "scale(-1)",
		});
	}
}

function check_for_winner(winner_color){
	if (winner_color=="DARK" || winner_color=="LIGHT"){
		return true;
	}
	else {
		return false;
	}
}

function update_winner_ui(winner_color, player1_username, player2_username){
	if (winner_color=="DARK"){
		var winner_player = player1_username;
	}
	else if (winner_color=="LIGHT"){
		var winner_player = player2_username;
	}

	if ((winner_color=="DARK" && player1_username==yourUsername) || 
		(winner_color=="LIGHT" && player2_username==yourUsername))
		{
		$('#network-error').text('Awesome! YOU WON');
		$('#network-error').css({'display':'block', 'color':'green'});
	}
	else if ((winner_color=="DARK" && player2_username==yourUsername) || 
			(winner_color=="LIGHT" && player1_username==yourUsername))
	{
		$('#network-error').text('You Lost, Better luck next time!');
		$('#network-error').css({'display':'block', 'color':'red'});
	}
	else {
		console.log(winner_player);
		$('#network-error').text('Winner: '+ winner_player );
		$('#network-error').css({'display':'block', 'color':'blue'});
	}
	$('.light-turn-text').css('color','lightgray');
	$('.dark-turn-text').css('color','lightgray');
}



