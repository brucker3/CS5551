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
const gameHistoryFile = JSON.parse(document.getElementById('game-history-file').textContent).split("\n");
const lastLine = gameHistoryFile.length - 2;
let current_line = lastLine;
console.log(yourUsername);

update_board(current_line);
//function which called when message is recieved


//function when socket is closed


let translation_dict = {};var k =1;for (var i=0; i<8; i++){	for (var j=0; j<8; j++){if (((j+i))%2!=0){translation_dict[k]=[j,i];k+=1;}}}

function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] == value);
}

function goBack() {
	if(current_line>0){
		current_line-=1;
	}
	update_board(current_line);
}

function goForward() {
	if(current_line<lastLine){
	current_line+=1;
	}
	update_board(current_line);
}

function goFirst() {
	current_line=0;
	update_board(current_line);
}

function goLast() {
	current_line=lastLine;
	update_board(current_line);
}

function startAutoplay(){
	autoplayVar = setInterval(function(){
		if(current_line<lastLine){
			current_line+=1;
			update_board(current_line);
		}
	}, 800);
	$("#autoplay").attr("onclick","stopAutoplay()");
	$("#autoplay-text").html("Stop Autoplay");
	$("#autoplay-spinner").addClass("spinner-grow spinner-grow-sm");
	
}

function stopAutoplay(){
	$("#autoplay").attr("onclick","startAutoplay()");
    $("#autoplay-text").html("Start Autoplay");
	$("#autoplay-spinner").removeClass("spinner-grow spinner-grow-sm");
	clearInterval(autoplayVar);
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

function update_board(board_history_line){
	//create vue object for every position and use that object to manipulate output
	recieved_data = JSON.parse(gameHistoryFile[board_history_line]);
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
		}
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



