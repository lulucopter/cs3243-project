import sys
import heapq

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

    def get_num_coord(self): #y, x
        return self.get_y(), self.get_x()

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
        for i in range(self.get_y() + 1, self.board.get_num_rows()):
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
        for i in range(self.get_x() + 1, self.board.get_num_cols()):
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
        for i in range(self.get_x() + 1, self.board.get_num_cols()):
            steps_up_right += 1
            x = i
            y = self.get_y() + steps_up_right
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Bishop(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the down right
        steps_down_right = 0
        for i in range(self.get_x() + 1, self.board.get_num_cols()):
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
        for i in range(self.get_y() + 1, self.board.get_num_rows()):
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
        for i in range(self.get_x() + 1, self.board.get_num_cols()):
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
        for i in range(self.get_x() + 1, self.board.get_num_cols()):
            steps_up_right += 1
            x = i
            y = self.get_y() + steps_up_right
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Queen(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the down right
        steps_down_right = 0
        for i in range(self.get_x() + 1, self.board.get_num_cols()):
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
        for i in range(self.get_x() + 1, self.board.get_num_cols()):
            steps_up_right += 1
            x = i
            y = self.get_y() + steps_up_right
            if (not self.board.is_open_square(x, y)) and self.board.is_in_board(x, y):
                break
            piece = Princess(x, y, self.get_board())
            moves.append(piece)

        # generate diagonals to the down right
        steps_down_right = 0
        for i in range(self.get_x() + 1, self.board.get_num_cols()):
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
        for i in range(self.get_y() + 1, self.board.get_num_rows()):
            x = self.get_x()
            y = i
            if not self.board.is_open_square(x, y):
                break
            piece = Empress(x, y, self.get_board())
            moves.append(piece)

        # down
        for i in range(self.get_y() - 1, -1, -1):
            x = self.get_x()
            y = i
            if not self.board.is_open_square(x, y):
                break
            piece = Empress(x, y, self.get_board())
            moves.append(piece)

        # right
        for i in range(self.get_x() + 1, self.board.get_num_cols()):
            x = i
            y = self.get_y()
            if not self.board.is_open_square(x, y):
                break
            piece = Empress(x, y, self.get_board())
            moves.append(piece)

        # left
        for i in range(self.get_x() - 1, -1, -1):
            x = i
            y = self.get_y()
            if not self.board.is_open_square(x, y):
                break
            piece = Empress(x, y, self.get_board())
            moves.append(piece)

        return moves






#############################################################################
######## Board
#############################################################################
class Board:
    def __init__(self, grid):
        self.grid = grid

    def get_num_rows(self):
        return len(self.grid)

    def get_num_cols(self):
        return len(self.grid[0])

    def is_in_board(self, x, y):
        x_check = (x >= 0) and (x < self.get_num_cols())
        y_check = (y >= 0) and (y < self.get_num_rows())
        return x_check and y_check

    def get_cost(self, x, y):
        return self.grid[y][x]

    def is_open_square(self, x, y):
        return self.grid[y][x] != -1

    def generate_unsafe_grid(self, enemy_pieces):
        total_enemy_moves = [e.get_num_coord() for e in enemy_pieces]
        for enemy in enemy_pieces:
            # (y, x)
            enemy_moves = [e.get_num_coord() for e in enemy.get_actions()]
            total_enemy_moves.extend(enemy_moves)

        # remove duplicates
        total_enemy_moves = list(set(total_enemy_moves))
        new_grid = self.grid.copy()
        for coord in total_enemy_moves:
            # set as invalid square
            new_grid[coord[0]][coord[1]] = -1
        return new_grid

#############################################################################
######## State
#############################################################################
class State:
    def __init__(self, piece_itself, board, goals, path, cost):
        self.piece_itself = piece_itself
        self.board = board
        self.goals = goals
        self.path = path
        self.cost = cost

    def get_path(self):
        return self.path

    def get_total_cost(self):
        return self.cost

    def is_goal(self):
        for goal in self.goals:
            if self.piece_itself.get_num_coord() == goal:
                return True
        return False

    def get_actions(self):
        moves = set(self.piece_itself.get_actions())
        return list(moves).copy()

    def get_transitions(self):
        transitions = []
        for piece in self.piece_itself.get_actions():
            if piece.location_is_valid():
                x = self.piece_itself.get_x()
                y = self.piece_itself.get_y()
                new_cost = self.cost + self.board.get_cost(x, y)
                new_path = self.path.copy()
                new_path.append([self.piece_itself.get_board_position(), piece.get_board_position()])
                transitions.append(State(piece, self.board, self.goals, new_path, new_cost))
        return transitions


    def __lt__(self, other):
        return self.cost < other.cost



#############################################################################
######## Implement Search Algorithm
#############################################################################


def search(rows, cols, grid, enemy_pieces, own_pieces, goals):
    board = Board(grid)
    enemy_pieces_list = []
    for enemy in enemy_pieces:
        x = enemy[1][1]
        y = enemy[1][0]
        enemy_name = enemy[0]
        piece = "null piece"
        if enemy_name == "King":
            piece = King(x, y, board)
        if enemy_name == "Rook":
            piece = Rook(x, y, board)
        if enemy_name == "Bishop":
            piece = Bishop(x, y, board)
        if enemy_name == "Queen":
            piece = Queen(x, y, board)
        if enemy_name == "Knight":
            piece = Knight(x, y, board)
        if enemy_name == "Ferz":
            piece = Ferz(x, y, board)
        if enemy_name == "Princess":
            piece = Princess(x, y, board)
        if enemy_name == "Empress":
            piece = Empress(x, y, board)
        enemy_pieces_list.append(piece)
    safe_board = Board(board.generate_unsafe_grid(enemy_pieces_list))
    king_piece = own_pieces[0]
    king_x = king_piece[1][1]
    king_y = king_piece[1][0]
    piece_itself = King(king_x, king_y, safe_board)
    start_path = []
    start_cost = 0
    start_state = State(piece_itself, safe_board, goals, start_path, start_cost)
    visited = [[False for i in range(cols)] for j in range(rows)]
    # path_cost_grid = [[-1 for i in range(cols)] for j in range(rows)]
    pq = [start_state]

    while pq:
        curr_state = heapq.heappop(pq)
        if curr_state.is_goal():
            return curr_state.get_path(), curr_state.get_total_cost()
        piece = curr_state.piece_itself
        x = piece.get_x()
        y = piece.get_y()
        if not visited[y][x]:
            visited[y][x] = True
            frontier = curr_state.get_transitions()
            for each in frontier:
                heapq.heappush(pq, each)

    return [], 0 # if no valid path found





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

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_UCS():
    testcase = sys.argv[1]
    rows, cols, grid, enemy_pieces, own_pieces, goals = parse(testcase)
    moves, pathcost = search(rows, cols, grid, enemy_pieces, own_pieces, goals)
    return moves, pathcost
