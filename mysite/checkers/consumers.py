# chat/consumers.py
import json,codecs,pickle,collections
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import logging
logger = logging.getLogger("mylogger")
from .game import Game
from .models import *
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from .aiplayer import *
global games, aiplayer, spectator_list
games = {}
spectator_list = collections.defaultdict(list)
#this class is about websocket communication
# when websocket is connected disconnects and message is received respective fuctions is triggered
class GameConsumer(WebsocketConsumer):
    def connect(self):
        global games, spectator_list
        self.auth_user = str(self.scope['user'])
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_id = 'game_%s' % self.game_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_id,
            self.channel_name
        )
        spectator_list[self.game_group_id].append(self.channel_name)
		#call some function here which return board according to the room and player who is requesting
        logger.info('connected to websocket')
        # if server restarts unsaved game will be lost!!!!
        #following condition is to avoid conflict of object retriveing from database and object currently in use
        # other condition to let other player in when player2 joins
        if self.game_id not in games or games[self.game_id].player2 == '':
            game_record = Game_Session.objects.get(game_id = self.game_id)
            games[self.game_id] = pickle.loads(codecs.decode(game_record.game_object.encode(), "base64"))
            games[self.game_id].player1 = game_record.player1_username
            games[self.game_id].player2 = game_record.player2_username
            games[self.game_id].update_game_object()
        print ("Current games being played: ", len(games)) # showing number of games being played simultaneously
        self.send_update_message()
        self.accept()

    def disconnect(self, close_code):
        global spectator_list
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_id,
            self.channel_name
        )
        spectator_list[self.game_group_id].remove(self.channel_name)
        self.send_update_message()
        logger.info('websocket disconnected and saves last game to database')
        record_edit = Game_Session.objects.get(game_id = self.game_id)
        record_edit.game_object = game_object = codecs.encode(pickle.dumps(games[self.game_id]), "base64").decode()
        record_edit.save()


    # Receive message from WebSocket
    def receive(self, text_data):
        global games,aiplayer, spectator_list
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
		#below line check if click is coming from correct person or not
        if (games[self.game_id].turn == 'D' and self.auth_user==games[self.game_id].player1) or (games[self.game_id].turn == 'L' and self.auth_user==games[self.game_id].player2):
            games[self.game_id].update_game_object(message)
        # logger.info(text_data)
        # new condition for ai player 
        self.send_update_message()
        while( games[self.game_id].player2 == "Computer" and games[self.game_id].turn == "L" and games[self.game_id].winner == ''):
            logger.info("ai game loop ai player move")
            aiplayer = Aiplayer(games[self.game_id].get_board())
            aiplayer.minmax(games[self.game_id].get_board(),10)
            move = aiplayer.get_move()
            games[self.game_id].update_game_object(move[1])
            games[self.game_id].update_game_object(move[0])
        if games[self.game_id].winner != '':
            self.save_winner()
        #click is recieved here are update board is sent back
        self.send_update_message()


    # Receive message from room group
    def game_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))
        # logger.info('game_message funcion')
        # logger.info(event)

    def send_update_message(self):
        board, moves, selected_piece = games[self.game_id].get_update()
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_id,
            {
                'type': 'game_message',
                'message': board,
				'moves': moves,
				'selected_piece' : selected_piece,
				'turn': games[self.game_id].turn,
                'winner': games[self.game_id].winner,
                'player1_username': games[self.game_id].player1,
                'player2_username': games[self.game_id].player2,
                'current_watchers': len(spectator_list[self.game_group_id]),
            }
        )

    def save_winner(self):
        if (games[self.game_id].winner == 'DARK'):
            Winner(game_id = self.game_id, winner_user = games[self.game_id].player1).save()

        if (games[self.game_id].winner == 'LIGHT'):
            Winner(game_id = self.game_id, winner_user = games[self.game_id].player2).save()
        game_record = Game_Session.objects.get(game_id = self.game_id)
        game_record.is_active = False
        game_record.save()

    def ai_game(self):
        aiplayer = Aiplayer()
        games[self.game_id].player2 = aiplayer


