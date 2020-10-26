# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import logging
from .checkers_game_engine import *
logger = logging.getLogger("mylogger")
from .rules import Game

#this class is about websocket communication
# when websocket is connected disconnects and message is received respective fuctions is triggered 
class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'game_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
		#call some function here which return board according to the room and player who is requesting
        logger.info('connected to websocket')
        # board = play_display_checkers(UserPlayer, UserPlayer, upper_color=State.WHITE)
        global game
        game = Game()
        game.event_loop()
        board,moves, selected_piece = game.update()
        print (board)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': board,
				'moves': moves,
				'selected_piece' : selected_piece
            }
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        logger.info('DISconnected to websocket')

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        logger.info(text_data)
        #do some thing here
        global game
        game.event_loop(message)
        board, moves, selected_piece = game.update()
        print (board)
        self.send(text_data=json.dumps({
		                     'message': board, 
		                     'moves': moves, 
		                     'selected_piece' : selected_piece,
		                     'room_name':self.room_name}))
        
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
        print (event)
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))
        logger.info('game_message funcion')
        logger.info(event)
		

