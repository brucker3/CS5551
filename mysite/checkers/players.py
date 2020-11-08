class Player(object):
    """" this is a plyaer class for our checkers game
    
    Attributes:
        name: a string  players name
        email: a string the email the player used to sign into the app
        active_game: boolen that should if player is playing a game
        game_color: string that references witch color pieces the player is using
        piece_count: list of the number of pices a player has and there locaiton on the board
    """

    def __init__(self, name, email):
        self.name = name 
        self.email = email
        self.game_color = "none"
        self.active_game = False
        self.piece_count= []

    "simple funciton to assign a player to a new game"
    def new_game(self,pieces, color):
        if(self.active_game == False):
            self.active_game = True 
            self.piece_count = pieces
            self.game_color = color
        else:
            print("player is currently in a game")

    " simple set of getter functions"
    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def is_active(self):
        return self.active_game

    def player_color(self):
        return self.game_color

    def player_pieces(self):
        return self.piece_count


# need modifiers plus an end game funciton to 
# reset the player


