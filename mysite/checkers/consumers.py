# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import logging
logger = logging.getLogger("mylogger")
from .game import Game
from .models import *
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
#this class is about websocket communication
# when websocket is connected disconnects and message is received respective fuctions is triggered 
class GameConsumer(WebsocketConsumer):
    def connect(self):
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
        print ([i.id for i in Game.instances])
		
		
        game = Game_Session.objects.get(game_id = self.game_id).game_object
        print (type(game),game)
        game.event_loop()
        board,moves, selected_piece = game.update()
        print (board)
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_id,
            {
                'type': 'game_message',
                'message': board,
				'moves': moves,
				'selected_piece' : selected_piece,
				'turn': game.turn,
            }
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_id,
            self.channel_name
        )
        logger.info('DISconnected to websocket')

    # Receive message from WebSocket
    def receive(self, text_data):
        print (get_current_authenticated_user(),get_current_user())
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        logger.info(text_data)
        #click is recieved here are update board is sent back
        global game
        if message != [-1,-1]: # when message == [-1,-1] this is only to get updated board
            game.event_loop(message)
            board, moves, selected_piece = game.update()
        if 'board' in vars():
            self.send(text_data=json.dumps({
		                     'message': board, 
		                     'moves': moves, 
		                     'selected_piece' : selected_piece,
		                     'game_id':self.game_id,
							 'turn': game.turn,}))
        
        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
            # self.room_group_name,
            # {
                # 'type': 'game_message',
                # 'message': message
            # }
        # )
    
    # Receive message from room group
    def game_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))
        # logger.info('game_message funcion')
        # logger.info(event)
		

