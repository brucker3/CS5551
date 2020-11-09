# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import logging
logger = logging.getLogger("mylogger")
from .game import Game
from .models import *
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
import codecs,pickle
#this class is about websocket communication
# when websocket is connected disconnects and message is received respective fuctions is triggered 
class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.auth_user = str(self.scope['user'])
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_id = 'game_%s' % self.game_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_id,
            self.channel_name
        )
		#call some function here which return board according to the room and player who is requesting
        logger.info('connected to websocket')
		
        global game
        game_record = Game_Session.objects.get(game_id = self.game_id)
        game = pickle.loads(codecs.decode(game_record.game_object.encode(), "base64"))
        game.player1 = game_record.player1_username
        game.player2 = game_record.player2_username		
        game.event_loop()
        board, moves, selected_piece = game.update()
        print (board)
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_id,
            {
                'type': 'game_message',
                'message': board,
				'moves': moves,
				'selected_piece' : selected_piece,
				'turn': game.turn,
				'winner': game.winner,
            }
        )
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_id,
            self.channel_name
        )
        logger.info('websocket disconnected and saves last game to database')
        record_edit = Game_Session.objects.get(game_id = self.game_id)
        record_edit.game_object = game_object = codecs.encode(pickle.dumps(game), "base64").decode()
        record_edit.save()

    # Receive message from WebSocket
    def receive(self, text_data):
        global game
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
		#below line check if click is coming from correct person or not
        if (game.turn == 'D' and self.auth_user==game.player1) or (game.turn == 'L' and self.auth_user==game.player2):
            if message != [-1,-1]:
                game.event_loop(message)
                board, moves, selected_piece = game.update()
        # logger.info(text_data)
        #click is recieved here are update board is sent back
        board, moves, selected_piece = game.update()
        self.send(text_data=json.dumps({
						 'message': board, 
						 'moves': moves, 
						 'selected_piece' : selected_piece,
						 'game_id':self.game_id,
						 'turn': game.turn,
						 'winner': game.winner,
						 }))
        
    
    # Receive message from room group
    def game_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))
        # logger.info('game_message funcion')
        # logger.info(event)
		

