import sys

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
class Piece:
    def __init__(self, piece_name, x, y, board):
        self.piece_name = piece_name
        self.x = x
        self.y = y
        self.board = board

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_board_position(self):
        return chr(self.get_x() + 97), self.get_y()

    def get_num_coord(self):
        return self.get_x(), self.get_y()

    def get_board(self):
        return self.board

    def location_is_valid(self):
        return self.board.is_in_board(self.get_x(), self.get_y()) \
               and self.board.is_open_square(self.get_x(), self.get_y())


class King(Piece):
    def __init__(self, x, y, board):
        super().__init__("King", x, y, board)

    def get_actions(self):
        up = King(self.get_x(), self.get_y() + 1, self.get_board())
        diag_right_up = King(self.get_x() + 1, self.get_y() + 1, self.get_board())
        right = King(self.get_x() + 1, self.get_y(), self.get_board())
        diag_right_down = King(self.get_x() + 1, self.get_y() - 1, self.get_board())
        down = King(self.get_x(), self.get_y() - 1, self.get_board())
        diag_left_down = King(self.get_x() - 1, self.get_y() - 1, self.get_board())
        left = King(self.get_x() - 1, self.get_y(), self.get_board())
        diag_left_up = King(self.get_x() - 1, self.get_y() + 1,self.get_board())

        pieces = [up, diag_right_up, right, diag_right_down, down, diag_left_down, left, diag_left_up]
        moves = pieces.copy()
        for move in pieces:  # iterate copy
            if not (move.location_is_valid()):  # remove piece if not valid
                moves.remove(move)

        # pieces are now all valid within the board
        return moves


class Knight(Piece):
    def __init__(self, x, y, board):
        super().__init__("Knight", x, y, board)

    def get_actions(self):
        up_right = Knight(self.get_x() + 1, self.get_y() + 2, self.get_board())
        up_left = Knight(self.get_x() - 1, self.get_y() + 2, self.get_board())
        right_up = Knight(self.get_x() + 2, self.get_y() + 1, self.get_board())
        right_down = Knight(self.get_x() + 2, self.get_y() - 1, self.get_board())
        down_right = Knight(self.get_x() + 1, self.get_y() - 2, self.get_board())
        down_left = Knight(self.get_x() - 1, self.get_y() - 2, self.get_board())
        left_up = Knight(self.get_x() - 2, self.get_y() + 1, self.get_board())
        left_down = Knight(self.get_x() - 2, self.get_y() - 1, self.get_board())

        pieces = [up_right, up_left, right_up, right_down, down_right, down_left, left_up, left_down]
        moves = pieces.copy()
        for move in pieces:  # iterate copy
            if not (move.location_is_valid()):  # remove piece if not valid
                moves.remove(move)
        # pieces are now all valid within the board
        return moves


class Rook(Piece):
    def __init__(self, x, y, board):
        super().__init__("Rook", x, y, board)

    def get_actions(self):
        moves = []

        ## create piece for each valid square up to first obstacle encountered
        # up
        for i in range(self.get_y() + 1, self.board.get_num_rows):
            x = self.get_x()
            y = i
            if not self.board.is_open_square(x, y):
                break
            piece = Rook(x, y, self.get_board())
            moves.append(piece)

        # down
        for i in range(self.get_y() - 1, -1, -1):
            x = self.get_x()
            y = i
            if not self.board.is_open_square(x, y):
                break
            piece = Rook(x, y, self.get_board())
            moves.append(piece)

        # right
        for i in range(self.get_x() + 1, self.board.get_num_cols):
            x = i
            y = self.get_y()
            if not self.board.is_open_square(x, y):
                break
            piece = Rook(x, y, self.get_board())
            moves.append(piece)

        # right
        for i in range(self.get_x() - 1, -1, -1):
            x = i
            y = self.get_y()
            if not self.board.is_open_square(x, y):
                break
            piece = Rook(x, y, self.get_board())
            moves.append(piece)

        return moves


class Bishop(Piece):
    def __init__(self, x, y, board):
        super().__init__("Bishop", x, y, board)

    def get_actions(self):
        moves = []

        # generate diagonals to the up right
        steps_up_right = 0
        for i in range(self.get_x() + 1, self.board.get_num_cols):
            steps_up_right += 1
            x = i
            y = self.get_y() + steps_up_right
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Bishop(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the down right
        steps_down_right = 0
        for i in range(self.get_x() + 1, self.board.get_num_cols):
            steps_down_right += 1
            x = i
            y = self.get_y() - steps_down_right
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Bishop(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the up left
        steps_up_left = 0
        for i in range(self.get_x() - 1, -1, -1):
            steps_up_left += 1
            x = i
            y = self.get_y() + steps_up_left
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Bishop(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the down left
        steps_down_left = 0
        for i in range(self.get_x() - 1, -1, -1):
            steps_down_left += 1
            x = i
            y = self.get_y() - steps_down_left
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Bishop(x, y, self.get_board())
            moves.append(piece)

        return moves


class Queen(Piece):
    def __init__(self, x, y, board):
        super().__init__("Queen", x, y, board)

    def get_actions(self):
        moves = []

        ## Rook's moves
        # up
        for i in range(self.get_y() + 1, self.board.get_num_rows):
            x = self.get_x()
            y = i
            if not self.board.is_open_square(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # down
        for i in range(self.get_y() - 1, -1, -1):
            x = self.get_x()
            y = i
            if not self.board.is_open_square(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # right
        for i in range(self.get_x() + 1, self.board.get_num_cols):
            x = i
            y = self.get_y()
            if not self.board.is_open_square(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # right
        for i in range(self.get_x() - 1, -1, -1):
            x = i
            y = self.get_y()
            if not self.board.is_open_square(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        ## Bishop's moves

        # generate diagonals to the up right
        steps_up_right = 0
        for i in range(self.get_x() + 1, self.board.get_num_cols):
            steps_up_right += 1
            x = i
            y = self.get_y() + steps_up_right
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the down right
        steps_down_right = 0
        for i in range(self.get_x() + 1, self.board.get_num_cols):
            steps_down_right += 1
            x = i
            y = self.get_y() - steps_down_right
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the up left
        steps_up_left = 0
        for i in range(self.get_x() - 1, -1, -1):
            steps_up_left += 1
            x = i
            y = self.get_y() + steps_up_left
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the down left
        steps_down_left = 0
        for i in range(self.get_x() - 1, -1, -1):
            steps_down_left += 1
            x = i
            y = self.get_y() - steps_down_left
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        return moves

class Ferz(Piece):
    def __init__(self, x, y, board):
        super().__init__("Ferz", x, y, board)

    def get_actions(self):
        diag_right_up = Ferz(self.get_x() + 1, self.get_y() + 1, self.get_board())
        diag_right_down = Ferz(self.get_x() + 1, self.get_y() - 1, self.get_board())
        diag_left_down = Ferz(self.get_x() - 1, self.get_y() - 1, self.get_board())
        diag_left_up = Ferz(self.get_x() - 1, self.get_y() + 1,self.get_board())

        pieces = [diag_right_up, diag_right_down, diag_left_down, diag_left_up]
        moves = pieces.copy()
        for move in pieces:  # iterate copy
            if not (move.location_is_valid()):  # remove piece if not valid
                moves.remove(move)

        # pieces are now all valid within the board
        return moves


class Princess(Piece):
    def __init__(self, x, y, board):
        super().__init__("Princess", x, y, board)

    def get_actions(self):
        moves = []

        ## knight's moves
        up_right = Princess(self.get_x() + 1, self.get_y() + 2, self.get_board())
        up_left = Princess(self.get_x() - 1, self.get_y() + 2, self.get_board())
        right_up = Princess(self.get_x() + 2, self.get_y() + 1, self.get_board())
        right_down = Princess(self.get_x() + 2, self.get_y() - 1, self.get_board())
        down_right = Princess(self.get_x() + 1, self.get_y() - 2, self.get_board())
        down_left = Princess(self.get_x() - 1, self.get_y() - 2, self.get_board())
        left_up = Princess(self.get_x() - 2, self.get_y() + 1, self.get_board())
        left_down = Princess(self.get_x() - 2, self.get_y() - 1, self.get_board())

        pieces = [up_right, up_left, right_up, right_down, down_right, down_left, left_up, left_down]
        moves = pieces.copy()
        for move in pieces:  # iterate copy
            if not (move.location_is_valid()):  # remove piece if not valid
                moves.remove(move)
        # moves are now all valid within the board

        ## Bishop's moves

        # generate diagonals to the up right
        steps_up_right = 0
        for i in range(self.get_x() + 1, self.board.get_num_cols):
            steps_up_right += 1
            x = i
            y = self.get_y() + steps_up_right
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Princess(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the down right
        steps_down_right = 0
        for i in range(self.get_x() + 1, self.board.get_num_cols):
            steps_down_right += 1
            x = i
            y = self.get_y() - steps_down_right
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Princess(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the up left
        steps_up_left = 0
        for i in range(self.get_x() - 1, -1, -1):
            steps_up_left += 1
            x = i
            y = self.get_y() + steps_up_left
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Princess(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the down left
        steps_down_left = 0
        for i in range(self.get_x() - 1, -1, -1):
            steps_down_left += 1
            x = i
            y = self.get_y() - steps_down_left
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Princess(x, y, self.get_board())
            moves.append(piece)

        return moves

class Empress(Piece):
    def __init__(self, x, y, board):
        super().__init__("Empress", x, y, board)

    def get_actions(self):
        moves = []

        ## knight's moves
        up_right = Empress(self.get_x() + 1, self.get_y() + 2, self.get_board())
        up_left = Empress(self.get_x() - 1, self.get_y() + 2, self.get_board())
        right_up = Empress(self.get_x() + 2, self.get_y() + 1, self.get_board())
        right_down = Empress(self.get_x() + 2, self.get_y() - 1, self.get_board())
        down_right = Empress(self.get_x() + 1, self.get_y() - 2, self.get_board())
        down_left = Empress(self.get_x() - 1, self.get_y() - 2, self.get_board())
        left_up = Empress(self.get_x() - 2, self.get_y() + 1, self.get_board())
        left_down = Empress(self.get_x() - 2, self.get_y() - 1, self.get_board())

        pieces = [up_right, up_left, right_up, right_down, down_right, down_left, left_up, left_down]
        moves = pieces.copy()
        for move in pieces:  # iterate copy
            if not (move.location_is_valid()):  # remove piece if not valid
                moves.remove(move)
        # moves are now all valid within the board

        ## Rook's moves
        # up
        for i in range(self.get_y() + 1, self.board.get_num_rows):
            x = self.get_x()
            y = i
            if not self.board.is_open_square(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # down
        for i in range(self.get_y() - 1, -1, -1):
            x = self.get_x()
            y = i
            if not self.board.is_open_square(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # right
        for i in range(self.get_x() + 1, self.board.get_num_cols):
            x = i
            y = self.get_y()
            if not self.board.is_open_square(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # right
        for i in range(self.get_x() - 1, -1, -1):
            x = i
            y = self.get_y()
            if not self.board.is_open_square(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        return moves






#############################################################################
######## Board
#############################################################################
class Board:
    def __init__(self, grid, pieces):
        self.grid = grid
        self.pieces = pieces

    def get_num_rows(self):
        return len(self.grid)

    def get_num_cols(self):
        return len(self.grid[0])

    def is_in_board(self, x, y):
        x_check = (x >= 0) and (x < self.get_num_cols())
        y_check = (y >= 0) and (y < self.get_num_rows())
        return x_check and y_check

    def is_open_square(self, x, y):
        return self.grid[y][x] == 1

#############################################################################
######## State
#############################################################################
class State:
    pass

#############################################################################
######## Implement Search Algorithm
#############################################################################
def search(rows, cols, grid, enemy_pieces, own_pieces, goals):
    pass


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# Return number of rows, cols, grid containing obstacles and step costs of coordinates, enemy pieces, own piece, and goal positions
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline())) # Integer
    cols = int(get_par(handle.readline())) # Integer
    grid = [[1 for j in range(cols)] for i in range(rows)] # Dictionary, label empty spaces as 1 (Default Step Cost)
    enemy_pieces = [] # List
    own_pieces = [] # List
    goals = [] # List

    handle.readline()  # Ignore number of obstacles
    for ch_coord in get_par(handle.readline()).split():  # Init obstacles
        r, c = from_chess_coord(ch_coord)
        grid[r][c] = -1 # Label Obstacle as -1

    handle.readline()  # Ignore Step Cost header
    line = handle.readline()
    while line.startswith("["):
        line = line[1:-2].split(",")
        r, c = from_chess_coord(line[0])
        grid[r][c] = int(line[1]) if grid[r][c] == 1 else grid[r][c] #Reinitialize step cost for coordinates with different costs
        line = handle.readline()
    
    line = handle.readline() # Read Enemy Position
    while line.startswith("["):
        line = line[1:-2]
        piece = add_piece(line)
        enemy_pieces.append(piece)
        line = handle.readline()

    # Read Own King Position
    line = handle.readline()[1:-2]
    piece = add_piece(line)
    own_pieces.append(piece)

    # Read Goal Positions
    for ch_coord in get_par(handle.readline()).split():
        r, c = from_chess_coord(ch_coord)
        goals.append((r, c))
    
    return rows, cols, grid, enemy_pieces, own_pieces, goals

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [piece, (r,c)]

def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

#############################################################################
######## Main function to be called
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# To return: List of moves
# Return Format Example: [[('a', 0), ('a', 1)], [('a', 1), ('c', 3)], [('c', 3), ('d', 5)]]
def run_BFS():    
    testcase = sys.argv[1]
    rows, cols, grid, enemy_pieces, own_pieces, goals = parse(testcase)
    print(rows, cols, grid, enemy_pieces, own_pieces, goals)
    moves = search(rows, cols, grid, enemy_pieces, own_pieces, goals)
    return moves

run_BFS()