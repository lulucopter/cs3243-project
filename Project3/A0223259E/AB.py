import sys
from random import choice, seed
from copy import deepcopy

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

config = {
    # black
    ('d', 6): ('King', 'Black'),
    ('c', 6): ('Queen', 'Black'),
    ('b', 6): ('Bishop', 'Black'),
    ('a', 6): ('Knight', 'Black'),
    ('g', 6): ('Rook', 'Black'),
    ('e', 6): ('Princess', 'Black'),
    ('f', 6): ('Empress', 'Black'),
    ('b', 5): ('Pawn', 'Black'),
    ('c', 5): ('Pawn', 'Black'),
    ('d', 5): ('Pawn', 'Black'),
    ('e', 5): ('Pawn', 'Black'),
    ('f', 5): ('Pawn', 'Black'),
    ('a', 5): ('Ferz', 'Black'),
    ('g', 5): ('Ferz', 'Black'),
    # white
    ('d', 0): ('King', 'White'),
    ('c', 0): ('Queen', 'White'),
    ('b', 0): ('Bishop', 'White'),
    ('a', 0): ('Knight', 'White'),
    ('g', 0): ('Rook', 'White'),
    ('e', 0): ('Princess', 'White'),
    ('f', 0): ('Empress', 'White'),
    ('b', 1): ('Pawn', 'White'),
    ('c', 1): ('Pawn', 'White'),
    ('d', 1): ('Pawn', 'White'),
    ('e', 1): ('Pawn', 'White'),
    ('f', 1): ('Pawn', 'White'),
    ('a', 1): ('Ferz', 'White'),
    ('g', 1): ('Ferz', 'White')
}


# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
class Piece:
    pass


def not_valid(action, col, row):
    return action[1] >= col or action[1] < 0 or action[0] < 0 or action[0] >= row


def king_actions(y, x, board: dict, row, col, colour):
    right = (y, x + 1)
    diag_right_up = (y + 1, x + 1)
    left = (y, x - 1)
    diag_left_up = (y + 1, x - 1)
    down = (y - 1, x)
    diag_left_down = (y - 1, x - 1)
    diag_right_down = (y - 1, x + 1)
    up = (y + 1, x)

    ls = [right, diag_right_up, left, diag_left_up, down, diag_left_down, diag_right_down, up]

    actions = ls.copy()
    for action in ls:
        if not_valid(action, col, row):
            actions.remove(action)

    # remove actions in obstacles
    copy_actions = actions.copy()
    for action in copy_actions:
        if board[action]:
            if board[action][1] == colour:
                actions.remove(action)
    return actions


def rook_actions(y, x, board: dict, row, col, colour):
    actions = []

    for i in range(x - 1, -1, -1):
        action = (y, i)
        if board[action]:
            if board[action][1] == colour:
                break  # cannot move past or capture own piece
            else:
                actions.append(action)  # capturing opponent piece
                break
        actions.append(action)

    for i in range(x + 1, col):
        action = (y, i)
        if board[action]:
            if board[action][1] == colour:
                break  # cannot move past or capture own piece
            else:
                actions.append(action)  # capturing opponent piece
                break
        actions.append(action)

    for i in range(y - 1, -1, -1):
        action = (i, x)
        if board[action]:
            if board[action][1] == colour:
                break  # cannot move past or capture own piece
            else:
                actions.append(action)  # capturing opponent piece
                break
        actions.append(action)

    for i in range(y + 1, row):
        action = (i, x)
        if board[action]:
            if board[action][1] == colour:
                break  # cannot move past or capture own piece
            else:
                actions.append(action)  # capturing opponent piece
                break
        actions.append(action)
    return actions


def bishop_actions(y, x, board: dict, row, col, colour):
    actions = []

    step_left = 0
    for i in range(x - 1, - 1, -1):
        step_left -= 1
        new_y = y + step_left
        if col > new_y:
            action = (new_y, i)
            if new_y < 0:  # out of range
                break
            elif board[action]:  # non empty tile
                if board[action][1] == colour:  # cannot move past own piece
                    break
                else:
                    actions.append(action)  # capturing opponent piece
                    break
            actions.append(action)

    step_right = 0
    for i in range(x + 1, col):
        step_right += 1
        new_y = y + step_right
        if row > new_y:
            action = (new_y, i)
            if board[action]:  # non empty tile
                if board[action][1] == colour:  # cannot move past own piece
                    break
                else:
                    actions.append(action)  # capturing opponent piece
                    break
            actions.append(action)

    step_down = 0
    for i in range(y - 1, - 1, -1):
        step_down += 1
        new_x = x + step_down
        if col > new_x:
            action = (i, new_x)
            if board[action]:  # non empty tile
                if board[action][1] == colour:  # cannot move past own piece
                    break
                else:
                    actions.append(action)  # capturing opponent piece
                    break
            actions.append(action)

    step_up = 0
    for i in range(y + 1, row):
        step_up += 1
        new_x = x - step_up
        if new_x >= 0:
            action = (i, new_x)
            if board[action]:  # non empty tile
                if board[action][1] == colour:  # cannot move past own piece
                    break
                else:
                    actions.append(action)  # capturing opponent piece
                    break
            actions.append(action)
    return actions


def queen_actions(y, x, board: dict, row, col, colour):
    actions = []
    actions.extend(rook_actions(y, x, board, row, col, colour))
    actions.extend(bishop_actions(y, x, board, row, col, colour))
    return actions


def knight_actions(y, x, board: dict, row, col, colour):
    ls = []

    top_left = (y + 2, x - 1)
    top_right = (y + 2, x + 1)
    bottom_left = (y - 2, x - 1)
    bottom_right = (y - 2, x + 1)
    left_top = (y + 1, x - 2)
    left_bottom = (y - 1, x - 2)
    right_top = (y + 1, x + 2)
    right_bottom = (y - 1, x + 2)

    temp = [top_left, top_right, bottom_left, bottom_right, left_top, left_bottom, right_top, right_bottom]
    ls.extend(temp)

    actions = ls.copy()
    for action in ls:
        if not_valid(action, col, row):
            actions.remove(action)

    # remove actions in obstacles
    copy_actions = actions.copy()
    for action in copy_actions:
        if board[action]:
            if board[action][1] == colour:
                actions.remove(action)
    return actions


def ferz_actions(y, x, board: dict, row, col, colour):
    diag_left_up = (y + 1, x - 1)
    diag_right_up = (y + 1, x + 1)
    diag_left_down = (y - 1, x - 1)
    diag_right_down = (y - 1, x + 1)

    ls = [diag_left_up, diag_right_up, diag_left_down, diag_right_down]

    actions = ls.copy()
    for action in ls:
        if not_valid(action, col, row):
            actions.remove(action)

    # remove actions in obstacles
    copy_actions = actions.copy()
    for action in copy_actions:
        if board[action]:
            if board[action][1] == colour:
                actions.remove(action)
    return actions


def princess_actions(y, x, board: dict, row, col, colour):
    actions = []
    actions.extend(bishop_actions(y, x, board, row, col, colour))
    actions.extend(knight_actions(y, x, board, row, col, colour))
    return actions


def empress_actions(y, x, board: dict, row, col, colour):
    actions = []
    actions.extend(rook_actions(y, x, board, row, col, colour))
    actions.extend(knight_actions(y, x, board, row, col, colour))
    return actions


def pawn_actions(y, x, board: dict, row, col, colour):
    actions = []
    if colour == "White":
        # move forward
        action = (y, x + 1)
        if x + 1 < row and not board[action]:  # valid move and not blocked
            actions.append(action)
        # capture diagonally
        action = (y + 1, x + 1)
        if x + 1 < row and y + 1 < col and board[action] and board[action][1] == "Black":
            actions.append(action)
        action = (y - 1, x + 1)
        if x + 1 < row and y - 1 >= 0 and board[action] and board[action][1] == "Black":
            actions.append(action)

    elif colour == "Black":
        # move forward
        action = (y, x - 1)
        if x - 1 >= 0 and not board[action]:
            actions.append(action)
        # capture diagonally
        action = (y + 1, x - 1)
        if x - 1 >= 0 and y + 1 < col and board[action] and board[action][1] == "White":
            actions.append(action)
        action = (y - 1, x - 1)
        if x - 1 >= 0 and y - 1 >= 0 and board[action] and board[action][1] == "White":
            actions.append(action)
    else:
        # raise Exception("Invalid colour")
        return "Invalid colour"

    return actions


#############################################################################
######## Board
#############################################################################
class Board:
    pass


#############################################################################
######## State
#############################################################################
class State:
    def __init__(self, max_rows: int, max_cols: int, board: dict, player_turn: int, is_terminal: bool):
        self.max_rows = max_rows
        self.max_cols = max_cols
        self.board = board
        self.player_turn = player_turn
        self.is_terminal = is_terminal

    def get_player_turn_num(self):
        return self.player_turn % 2

    def get_player_turn_name(self):
        return "White" if self.get_player_turn_num() == 0 \
            else "Black" if self.get_player_turn_num() == 1 \
            else "None"

    def get_actions(self, player_turn):
        moves = {  # list of moves for each piece type
            "King": [],
            "Queen": [],
            "Rook": [],
            "Bishop": [],
            "Knight": [],
            "Pawn": [],
            "Ferz": [],
            "Princess": [],
            "Empress": [],
        }
        for num_coord, piece in self.board.items():
            if piece:
                piece_type = piece[0]
                curr_player_turn = piece[1]
                if curr_player_turn == player_turn:  # piece[1] is the player that owns the piece
                    actions = get_piece_actions(num_coord, piece_type, curr_player_turn, self.board)
                    moves[piece_type].extend(actions)

        all_possible_actions = []
        for piece_type_actions in moves.values():
            all_possible_actions.extend(piece_type_actions)
        return all_possible_actions

    def move(self, coord: (tuple, tuple)):
        if not coord:
            # raise Exception("Invalid move given: no coord given")
            return "Invalid move given: no coord given"
        old_pos, new_pos = coord
        piece_to_move = self.board[old_pos]
        is_terminal = False
        new_tile = self.board[new_pos]
        if new_tile and new_tile[0] == "King" and new_tile[1] != piece_to_move[1]:
            is_terminal = True  # game is over if opponent king is captured
        new_board = deepcopy(self.board)
        new_board[old_pos] = None
        new_board[new_pos] = piece_to_move
        new_state = State(self.max_rows, self.max_cols, new_board, self.player_turn + 1, is_terminal)
        return new_state

    def utility(self) -> int:
        board = self.board
        piece_values = {
            "King": 300,
            "Queen": 8.375,
            "Rook": 5,
            "Bishop": 3.375,
            "Knight": 3,
            "Pawn": 1,
            "Ferz": 2,
            "Princess": 6.375,
            "Empress": 8,
            "influence": 0.1
        }
        piece_count = {
            "King": 0,
            "Queen": 0,
            "Rook": 0,
            "Bishop": 0,
            "Knight": 0,
            "Pawn": 0,
            "Ferz": 0,
            "Princess": 0,
            "Empress": 0,
            "influence": len(self.get_actions("White")) - len(self.get_actions("Black"))
            # possible movement locations of white - black; len(white_actions) - len(black_actions)
            # => influence/power of piece based on its position
        }
        for piece in board.values():
            if piece:
                p_name = piece[0]
                colour = piece[1]
                if colour == "White":
                    piece_count[p_name] += 1
                elif colour == "Black":
                    piece_count[p_name] -= 1
                else:
                    # raise Exception("Error in util count")
                    return "Error in util count"
        total = 0
        for piece, count in piece_count.items():
            total += piece_values[piece] * count
        return count


########################

def old_to_new_tile(num_coord, actions):
    new_tiles = []
    for action in actions:
        new_tiles.append((num_coord, action))
    return new_tiles


def get_piece_actions(num_coord, piece_type, curr_player_turn, board):
    y = num_coord[0]
    x = num_coord[1]
    if piece_type == "Queen":
        return old_to_new_tile(num_coord, queen_actions(y, x, board, 7, 7, curr_player_turn))
    elif piece_type == "Empress":
        return old_to_new_tile(num_coord, empress_actions(y, x, board, 7, 7, curr_player_turn))
    elif piece_type == "Princess":
        return old_to_new_tile(num_coord, princess_actions(y, x, board, 7, 7, curr_player_turn))
    elif piece_type == "Rook":
        return old_to_new_tile(num_coord, rook_actions(y, x, board, 7, 7, curr_player_turn))
    elif piece_type == "Bishop":
        return old_to_new_tile(num_coord, bishop_actions(y, x, board, 7, 7, curr_player_turn))
    elif piece_type == "Knight":
        return old_to_new_tile(num_coord, knight_actions(y, x, board, 7, 7, curr_player_turn))
    elif piece_type == "King":
        return old_to_new_tile(num_coord, king_actions(y, x, board, 7, 7, curr_player_turn))
    elif piece_type == "Ferz":
        return old_to_new_tile(num_coord, ferz_actions(y, x, board, 7, 7, curr_player_turn))
    elif piece_type == "Pawn":
        return old_to_new_tile(num_coord, pawn_actions(y, x, board, 7, 7, curr_player_turn))
    else:
        # raise Exception("Invalid piece type given")
        return "Invalid piece type given"


def to_chess_coord(num_coord):
    return chr(num_coord[0] + 97), num_coord[1]


def maximise(state, alpha, beta, depth):
    move = None
    # leave of ab tree
    if depth == 0 or state.is_terminal:
        return state.utility(), None
    value = -float("inf")
    for action in state.get_actions(state.get_player_turn_name()):
        new_value, _ = minimise(state.move(action), alpha, beta, depth - 1)
        if new_value > value:
            value, move = new_value, action
            alpha = max(alpha, value)
        if value >= beta:  # prune subtrees
            return value, move
    return value, move


def minimise(state, alpha, beta, depth):
    move = None
    # leave of ab tree
    if depth == 0 or state.is_terminal:
        return state.utility(), None
    value = float("inf")
    for action in state.get_actions(state.get_player_turn_name()):
        new_value, _ = maximise(state.move(action), alpha, beta, depth - 1)
        if new_value < value:
            value, move = new_value, action
            beta = min(beta, value)
        if value <= alpha:  # prune subtrees
            return value, move
    return value, move


# Implement your minimax with alpha-beta pruning algorithm here.
  # no way my bday makes me lucky right? LOL
def ab(state, chosen_depth):

    # ab search
    alpha_init = -float("inf")
    beta_init = float("inf")
    _, move = maximise(state, alpha_init, beta_init, chosen_depth)
    old_pos, new_pos = move
    return to_chess_coord(old_pos), to_chess_coord(new_pos)


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# Return number of rows, cols, grid containing obstacles and step costs of coordinates, enemy pieces, own piece, and goal positions
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))  # Integer
    cols = int(get_par(handle.readline()))  # Integer
    gameboard = {}

    enemy_piece_nums = get_par(handle.readline()).split()
    num_enemy_pieces = 0  # Read Enemy Pieces Positions
    for num in enemy_piece_nums:
        num_enemy_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_enemy_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "Black")

    own_piece_nums = get_par(handle.readline()).split()
    num_own_pieces = 0  # Read Own Pieces Positions
    for num in own_piece_nums:
        num_own_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_own_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "White")

    return rows, cols, gameboard


def add_piece(comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r, c), piece]


def from_chess_coord(ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)


# You may call this function if you need to set up the board
def setUpBoard():
    config = sys.argv[1]
    rows, cols, gameboard = parse(config)


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook, Princess, Empress, Ferz, Pawn (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new ending position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    # hyper param
    ROWS = 7
    COLS = 7
    DEPTH = [3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

    chosen_depth = choice(DEPTH)

    # state init
    my_board = {}
    for col in range(COLS):
        for row in range(ROWS):
            my_board[(row, col)] = None  # no piece in tile
    for key, value in gameboard.items():
        my_board[(ord(key[0]) - 97, key[1])] = value
    state = State(ROWS, COLS, my_board, 0, False)

    move = ab(state, chosen_depth)
    return move  # Format to be returned (('a', 0), ('b', 3))
seed(4200)
#print(studentAgent(config))