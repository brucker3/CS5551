
# square - a number between 1 and 35, that isn't divisible by 9:
#    . 32  . 31  . 30  . 29
#   28  . 27  . 26  . 25  .
#    . 24  . 23  . 22  . 21
#   20  . 19  . 18  . 17  .
#    . 16  . 15  . 14  . 13
#   12  . 11  . 10  . 9  .
#    .  8  .  7  .  6  .  5
#    4  .  3  .  2  .  1  .
# Pay attention that in this representation, the numbers that are
# divisible by 9 are skipped - thus, two squares are adjacents if and
# only if their difference is 4 or 5. 

# move - a tuple of squares - the first square is the piece we want to
#     move, and the others are the sequence of moves. Usually that tuple
#     is 2 squares long - it's only longer if the player made a multiple
#     jump.

# In some places of the program, the word "edges" will mean pairs of
# squares that have only one reachable square between them (in a
# diagonal line), so you can jump between them if they are both empty
# and there is an opponent's piece in the middle.
# The square in the middle of the two edges will just be called
# "the middle".
from collections import namedtuple
import itertools 
import json
SQUARES = [s for s in range(1, 36) if s%9 != 0]

# a "jump" means both single and multiple jumps.


class MovingErrors:
    """A namespace for error constants for illegal moves."""
    NotASquare = "The move included a number that is not a square."
    TooShort = ("The move should start at one square and finish at "
                "another one.")
    NotYourPiece = "The player should move his own piece."
    MoveToPiece = "The player should move to an empty square."
    LongSimpleMove = "A simple move must include exactly 2 squares in it."
    NotKing = "Only a king can move backwards."
    JumpAvaliable = ("If a player can jump, he must do it; And if a player"
                     " can make multiple jumps, he must make all available"
                     " jumps in the sequence he chose.")
    JumpThroughKingRow = ("If a man jumps to the king's row, the move"
                          " terminates immediately.")
    SometimesJumps = ("If a move starts with a jump, ALL of it should be"
                      " composed of jumps.")
    WeirdCapturing = ("You have to capture your opponent's piece - not "
                      "empty pieces and not your own ones")
    JustInvalid = ("A simple move should move a piece to an adjacent")

### Checkers Stuff ###

class State(namedtuple('State', 'turn reds whites kings')):
    """A state in the English Checkers game.

    The board is always represented in the red's point of view, so the
    1-4 rank is the closest rank to the red's side, and the 32-35 rank
    is the closest rank to the white's side.

    Attributes:
        turn - the player that should play now - either State.RED or
            State.WHITE.
        reds, whites - frozensets of squares, where there are red and
            white pieces accordingly.
        kings - the squares where there are kings (red and white).
    These 4 attributes can also be like elements of a tuple - so you can
    unpack them:
        >>> turn, reds, whites, kings = state
    and you can access them also by doing state[n]. This is useful,
    because State.RED is 1 and State.WHITE is 2 - thus state[state.turn]
    will return all of the squares that belong to the current player.

    Other Attributes:
        opponent - the player that shouldn't play now, the opposite of
            self.turn.
        These attributes can't be accessed like in a tuple.

    Main Methods:
        state.move(move) - return a new state, that describes the game
            after the current player has made the given move.
        state.did_end() - True if the game ended, False otherwise.

    Other Methods:
        simple_move_avaliable(pieces) - return True if any of the given
            pieces can make a simple move. (The returned value may be
            incorrect if any piece can make a jump)
        jump_avaliable(pieces) - return True if any of the given
            pieces can make a jump.
        farther(s1, s2) - True if s1 is farther from the current player
            than the second square, False otherwise.
        pieces_after_simple_move(move) - Return a tuple of (red pieces,
            white pieces, kings), that describes the board's pieces after
            the given (not necessarily legal) simple move.
        pieces_after_jump(move) - Return a tuple of (red pieces,
            white pieces, kings), that describes the board's pieces
            after the given (not necessarily legal) jump.
    """

    RED, WHITE = 1, 2  # pay attention that state[RED] == state.reds and
                       # state[WHITE] == state.whites
    KINGS_ROW = {RED: frozenset(range(32, 36)), WHITE: frozenset(range(1, 5))}

    def __new__(cls, turn, reds, whites, kings):
        # now you can create a new state by passing any kind of iterable
        # as pieces
        pieces = [frozenset(filter(is_square, xs))
                  for xs in (reds, whites, kings)]
        self = super(State, cls).__new__(cls, turn, *pieces)
        self.opponent = cls.WHITE if turn == cls.RED else cls.RED
        return self

    def move(self, move):
        """If the given move is legal, make it and return the new state,
        after the move. If it is illegal, raise ValueError with an
        appropriate error message from MovingErrors."""
        self.errors(move)

        if are_adjacents(*move[0:2]):  # Simple move
            if len(move) > 2:
                raise ValueError(MovingErrors.LongSimpleMove)
            if self.jump_avaliable(self[self.turn]):
                raise ValueError(MovingErrors.JumpAvaliable)
            return State(self.opponent, *self.pieces_after_simple_move(move))

        elif are_edges(*move[0:2]):  # jump
            if not is_jump(move[2:]):
                raise ValueError(MovingErrors.SometimesJumps)
            if any(s in self.KINGS_ROW[self.turn] and s not in self.kings
                   for s in move[1:-1]):
                raise ValueError(MovingErrors.JumpThroughKingRow)
            if any(middle(*pair) not in self[self.opponent]
                   for pair in pairs(move)):
                raise ValueError(MovingErrors.WeirdCapturing)
            # If a man jumps to the king's row, he can't make more jumps.
            # Otherwise, if he can make more jumps the player must do them.
            new_board = self.pieces_after_jump(move)
            if (move[-1] in self.KINGS_ROW[self.turn] and
                    move[0] not in self.kings):
                return State(self.opponent, *new_board)
            temp_state = State(self.turn, *new_board)
            if temp_state.jump_avaliable([move[-1]]):
                raise ValueError(MovingErrors.JumpAvaliable)
            return State(self.opponent, *new_board)

        # Not a simple move, and not a jump
        raise ValueError(MovingErrors.JustInvalid)

        # Phew.

    def errors(self, move):
        """If the move has an "stupid error" (explained later), raise
        ValueError with that error from MovingErrors. Otherwise, do
        nothing.

        Stupid error - TooShort, NotASquare, NotYourPiece, MoveToPiece,
            NotKing.
        """
        if len(move) <= 1:
            raise ValueError(MovingErrors.TooShort)
        if not all(is_square(k) for k in move):
            raise ValueError(MovingErrors.NotASquare)
        if move[0] not in self[self.turn]:
            raise ValueError(MovingErrors.NotYourPiece)
        if any(s in self.reds|self.whites for s in move[1:]):
            raise ValueError(MovingErrors.MoveToPiece)
        if move[0] not in self.kings and not self.farther(move[1], move[0]):
            raise ValueError(MovingErrors.NotKing)

    def did_end(self):
        """Return True if the game has ended, and False if the player
        can do a move."""
        return (not self.simple_move_avaliable(self[self.turn]) and
                not self.jump_avaliable(self[self.turn]))

    def simple_move_avaliable(self, pieces):
        """Return True if any piece from the given iterable of pieces can
        make a simple move, False otherwise. It doesn't check if all of
        the given pieces exist. Also, if a jump is avaliable it won't
        return False because of that, so the returned value would be
        incorrect in that case."""
        assert all(piece in self[self.turn] for piece in pieces)
        for piece in pieces:
            for adj in adjacents(piece):
                if adj not in self.reds | self.whites:
                    return True
        return False

    def jump_avaliable(self, pieces):
        """Return True if any piece from the given iterable of pieces can
        do a jump, False otherwise. It doesn't check if all of the given
        pieces exist."""
        assert all(piece in self[self.turn] for piece in pieces)
        for piece in pieces:
            # Every jump starts with a single jump.
            for edge, mid in edges_middles(piece):
                if (edge not in self[self.turn] | self[self.opponent] and
                        mid in self[self.opponent] and
                        (piece in self.kings or self.farther(edge, piece))):
                    return True
        return False

    def farther(self, s1, s2):
        """Return True if the first square is farther than the second one
        (so the second square is closer to the current player's side),
        False otherwise."""
        return s1 > s2 if self.turn == self.RED else s1 < s2

    def pieces_after_simple_move(self, move):
        """Return a tuple of (red pieces, white pieces, kings),
        that describes the board's pieces after the given simple move.

        This method doesn't check that the given move is simple, or even
        legal, and won't necessarily raise an exception.
        """
        assert (move[0] in self[self.turn] and
                move[1] not in self.reds | self.whites and len(move) == 2)
        player = self[self.turn] - {move[0]} | {move[1]}
        if move[0] in self.kings:
            kings = self.kings - {move[0]} | {move[1]}
        else:
            kings = self.kings | ({move[1]} & self.KINGS_ROW[self.turn])
        return ((player, self[self.opponent], kings) if self.turn == self.RED
                else (self[self.opponent], player, kings))

    def pieces_after_jump(self, move):
        """Return a tuple of (red pieces, white pieces, kings),
        that describes the board's pieces after the given jump.

        This method doesn't check that the given move is a jump, or even
        legal, and won't necessarily raise an exception.
        """
        assert is_jump(move)
        single_jumps = pairs(move)
        captured = {middle(*p) for p in single_jumps}
        player = self[self.turn] - {move[0]} | {move[-1]}
        opponent = self[self.opponent] - captured
        if move[0] in self.kings:
            kings = self.kings - {move[0]} | {move[-1]}
        else:
            kings = self.kings | ({move[-1]} & self.KINGS_ROW[self.turn])
        kings = kings - captured
        return ((player, opponent, kings) if self.turn == self.RED
                else (opponent, player, kings))

### Square Stuff ###

def are_adjacents(s1, s2):
    """Return True if the two given squares are diagonally adjacent,
    False otherwise."""
    return abs(s1-s2) in (4, 5)

def are_edges(s1, s2):
    """Return True if two given squares are edges, False otherwise."""
    return abs(s1-s2) in (8, 10)

def middle(edge1, edge2):
    """Return the middle of the two given edges."""
    assert are_edges(edge1, edge2)
    return (edge1 + edge2) / 2

def edges_middles(s):
    """Return a list of all (edge, middle) tuples, where `edge` is
    another square that is an edge with the given square, and middle is
    the middle square of `s` and `edge`."""
    edges = [s + n for n in (8, 10, -8, -10)]
    middles = [middle(s, edge) for edge in edges]
    tuples = zip(edges, middles)
    return [t for t in tuples if is_square(t[0]) and is_square(t[1])]

def adjacents(s):
    """Return a list of all of the adjacent squares to the given square."""
    return [s+n for n in (4, 5, -4, -5) if is_square(s+n)]

def is_square(n):
    """Return True if the given number represents a square, False if it
    doesn't."""
    return 1 <= n <= 35 and n % 9 != 0

def is_jump(move):
    """Return True if each pair in the given sequence of squares is a
    pair of edges. False otherwise."""
    return all(are_edges(a, b) for a, b in pairs(move))

def rank(s):
    """Return the rank of the given squares. Counting starts from zero."""
    return ((s-s//9)-1) // 4

def human_square_to_normal(human_s):
    """Convert the given square from human representation (where squares
    are identified by numbers 1-32 and squares that are divisible by 9
    aren't skipped) to the normal program's representation.
    Raise KeyError if the square doesn't exist."""
    return SQUARES[human_s-1]


### Playing Stuff ###

# starting position of checkers
START = State(State.RED, range(1, 14), range(23, 36), [])

def checkers(red, white):
    """Play English Checkers between the two given players - red makes
    the first move. After each turn, yield the move.

    A player is a function that has two parameters - a state, and an
    optional parameter of an error. The state is an instance of the State
    class, that describes the current game, and the player should return
    its move, given that state. If the player gets the `error`
    parameter, it means that in the previous time it was called, it
    returned an illegal move - so it is called again, with the same state,
    and with an error from MovingErrors.
    """
    state = START
    yield None, state
    for player in itertools.cycle((red, white)):
        if state.did_end():
            return
        move = player(state)
        while True:
            try:
                state = state.move(move)
            except ValueError as err:
                move = player(state, str(err))
            else:
                break
        yield move, state

def display_checkers(game, upper_color=State.RED):
    """Display each state in the given game, from the first one to the
    last. The "game" is an iterable of (move, state) pairs (the state is
    the state of the game after the move), for example the one that is
    returned by the function `checkers`.

    `upper_color` is the color that its player's side appears at the
    top of the displayed boards. It can get one of two values:
    State.RED or State.WHITE.
    """
    for _, state in game:
        return print_board(state, upper_color)

def play_display_checkers(red, white, upper_color=State.RED):
    """Play a game of checkers with the given players `red` and `white`,
    and display every new board.
    `upper_color` is the color that appears at the top of the displayed
    boards. (color = either State.RED or State.WHITE)
    See the docstring of `checkers` for more information about players.
    """
    return display_checkers(checkers(red, white), upper_color)

def UserPlayer(dummy_state, error=None):
    """A player function that uses the protocol of the `checkers` function.
    It doesn't display the board to the user, but if there is an error, it
    will print it.
    It asks the user for a move in a human notation (where the squares are
    identified by numbers 1-32, instead of 1-35, and squares that are
    divisible by 9 aren't skipped). It returns the move in the program's
    notation.
    """
    if error is not None:
        print (error)
    inp = input("What's your move? Seperate the squares by dashes (-). ")

    while True:
        try:
            human_squares = map(int, inp.split('-'))
            move = map(human_square_to_normal, human_squares)
        except ValueError:
            inp = input('Invalid input. Try again: ')
        except KeyError:  # Because of human_square_to_normal
            print (MovingErrors.NotASquare)
            inp = input('Try again: ')
        else:
            break
    return tuple(move)


### Utilities ###

def pairs(seq):
    """Return a list of all of the consecutive pairs in the sequence.
    Each element (except the first and the last ones) appears in exactly
    two pairs: one where it is the first element, and another one where
    it is the second one."""
    return [(seq[i], seq[i+1]) for i in range(len(seq)-1)]

def print_board(state, upper_color=State.RED):
    """Print the given state to the user as a board."""
    line = []
    # the first squares should be the upper ones.
    squares = SQUARES if upper_color == State.RED else SQUARES[::-1]
    # zip(*[iterator]*n) clusters the iterator elements into n-length groups.
    rows = zip(*[iter(squares)]*4)
    whole_board = ''
    for row in rows:
        for square in row:
            player_ch = ('x' if square in state.reds
                         else 'y' if square in state.whites else '.')
            char = player_ch.upper() if square in state.kings else player_ch
            # == is used as an XNOR operator here
            if (rank(square) % 2 == 1) == (upper_color == State.WHITE):
                line.append('   {}'.format(char))
            else:
                line.append(' {}  '.format(char))
        # print (''.join(line))
        board = (''.join(line))
        # print (board)
        json_board = json.dumps(board)
        print(json_board)
        whole_board += json_board.strip('"').replace(' ','')
        line = []
    return whole_board

###############

# if __name__ == '__main__':
    # play_display_checkers(UserPlayer, UserPlayer, upper_color=State.WHITE)