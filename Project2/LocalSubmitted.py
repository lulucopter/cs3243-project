port
copy
import sys
from random import shuffle


# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
class Piece:
    def __init__(self, piece_name, x, y, cols, rows, grid):
        self.piece_name = piece_name
        self.x = x
        self.y = y
        self.cols = cols
        self.rows = rows
        self.grid = grid

    def __repr__(self):
        return "{piece_name} : [{x}, {y}]".format(piece_name=self.piece_name, x=self.x, y=self.y)

    def get_coord(self):
        return chr(self.x + 97), self.y

    def get_coord_swapped(self):
        return chr(self.y + 97), self.x

    def get_num_coord(self):
        return self.y, self.x

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_max_cols(self):
        return self.cols

    def get_max_rows(self):
        return self.rows

    def get_grid(self):
        return self.grid

    def get_piece_name(self):
        return self.piece_name

    def get_points(self):
        return self.points

    def is_not_valid(self, action):
        return action[1] >= self.get_max_cols() \
               or action[1] < 0 \
               or action[0] < 0 \
               or action[0] >= self.get_max_rows()

    def is_obstacle(self, y, x):
        return self.grid[y][x] == -1


class King(Piece):
    def __init__(self, x, y, cols, rows, grid):
        super().__init__('King', x, y, cols, rows, grid)

    def get_actions(self):

        right = (self.get_y(), self.get_x() + 1)
        diag_right_up = (self.get_y() + 1, self.get_x() + 1)
        left = (self.get_y(), self.get_x() - 1)
        diag_left_up = (self.get_y() + 1, self.get_x() - 1)
        down = (self.get_y() - 1, self.get_x())
        diag_left_down = (self.get_y() - 1, self.get_x() - 1)
        up = (self.get_y() + 1, self.get_x())
        diag_right_down = (self.get_y() - 1, self.get_x() + 1)

        actions = [right, diag_right_up, left, diag_left_up, down, diag_left_down, diag_right_down, up]

        copy_actions = actions.copy()
        for action in copy_actions:
            # assume a is start
            if self.is_not_valid(action):
                actions.remove(action)

        # remove actions in obstacles
        copy_actions = actions.copy()
        for action in copy_actions:
            y = action[0]
            x = action[1]
            if self.is_obstacle(y, x):
                actions.remove(action)

        return actions


class Rook(Piece):
    def __init__(self, x, y, cols, rows, grid):
        super().__init__('Rook', x, y, cols, rows, grid)

    def get_actions(self):
        actions = []

        for i in range(self.get_x() - 1, -1, -1):
            y = self.get_y()
            x = i
            if self.is_obstacle(y, x):
                break
            action = (self.get_y(), i)
            actions.append(action)

        for i in range(self.get_x() + 1, self.get_max_cols()):
            y = self.get_y()
            x = i
            if self.is_obstacle(y, x):
                break
            action = (self.get_y(), i)
            actions.append(action)

        for i in range(self.get_y() - 1, -1, -1):
            y = i
            x = self.get_x()
            if self.is_obstacle(y, x):
                break
            action = (i, self.get_x())
            actions.append(action)

        for i in range(self.get_y() + 1, self.get_max_rows()):
            y = i
            x = self.get_x()
            if self.is_obstacle(y, x):
                break
            action = (i, self.get_x())
            actions.append(action)
        return actions


class Bishop(Piece):
    def __init__(self, x, y, cols, rows, grid):
        super().__init__('Bishop', x, y, cols, rows, grid)

    def get_actions(self):
        actions = []

        step_left = 0
        for i in range(self.get_x() - 1, - 1, -1):
            step_left -= 1
            y = self.get_y() + step_left
            x = i
            if len(self.grid) > y:
                self.is_obstacle(y, x)
                if y < 0 or self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        step_right = 0
        for i in range(self.get_x() + 1, self.get_max_cols()):
            step_right += 1
            y = self.get_y() + step_right
            x = i
            if len(self.grid) > y:
                if self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        step_down = 0
        for i in range(self.get_y() - 1, - 1, -1):
            step_down += 1
            y = i
            x = self.get_x() + step_down
            if len(self.grid[0]) > x:
                if self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        step_up = 0
        for i in range(self.get_y() + 1, self.get_max_rows()):
            step_up += 1
            y = i
            x = self.get_x() - step_up
            if x >= 0:
                if self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)
        return actions


class Queen(Piece):
    def __init__(self, x, y, cols, rows, grid):
        super().__init__("Queen", x, y, cols, rows, grid)
        self.grid = grid

    def get_actions(self):
        actions = []

        # rook
        for i in range(self.get_x() - 1, -1, -1):
            y = self.get_y()
            x = i
            if self.is_obstacle(y, x):
                break
            action = (self.get_y(), i)
            actions.append(action)

        for i in range(self.get_x() + 1, self.get_max_cols()):
            y = self.get_y()
            x = i
            if self.is_obstacle(y, x):
                break
            action = (self.get_y(), i)
            actions.append(action)

        for i in range(self.get_y() - 1, -1, -1):
            y = i
            x = self.get_x()
            if self.is_obstacle(y, x):
                break
            action = (i, self.get_x())
            actions.append(action)

        for i in range(self.get_y() + 1, self.get_max_rows()):
            y = i
            x = self.get_x()
            if self.is_obstacle(y, x):
                break
            action = (i, self.get_x())
            actions.append(action)

        # bishop
        step_left = 0
        for i in range(self.get_x() - 1, - 1, -1):
            step_left -= 1
            y = self.get_y() + step_left
            x = i
            if len(self.grid) > y:
                self.is_obstacle(y, x)
                if y < 0 or self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        step_right = 0
        for i in range(self.get_x() + 1, self.get_max_cols()):
            step_right += 1
            y = self.get_y() + step_right
            x = i
            if len(self.grid) > y:
                if self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        step_down = 0
        for i in range(self.get_y() - 1, - 1, -1):
            step_down += 1
            y = i
            x = self.get_x() + step_down
            if len(self.grid[0]) > x:
                if self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        step_up = 0
        for i in range(self.get_y() + 1, self.get_max_rows()):
            step_up += 1
            y = i
            x = self.get_x() - step_up
            if x >= 0:
                if self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        return actions


class Knight(Piece):
    def __init__(self, x, y, cols, rows, grid):
        super().__init__('Knight', x, y, cols, rows, grid)

    def get_actions(self):
        actions = []
        up_left = (self.get_y() + 2, self.get_x() - 1)
        up_right = (self.get_y() + 2, self.get_x() + 1)
        down_left = (self.get_y() - 2, self.get_x() - 1)
        down_right = (self.get_y() - 2, self.get_x() + 1)
        left_up = (self.get_y() + 1, self.get_x() - 2)
        left_down = (self.get_y() - 1, self.get_x() - 2)
        right_up = (self.get_y() + 1, self.get_x() + 2)
        right_down = (self.get_y() - 1, self.get_x() + 2)

        temp = [up_left, up_right, right_up, right_down, down_right, down_left, left_down, left_up]

        actions.extend(temp)
        copy_actions = actions.copy()
        for action in copy_actions:
            # assume a is start
            if self.is_not_valid(action):
                actions.remove(action)

        # remove actions in obstacles
        copy_actions = actions.copy()
        for action in copy_actions:
            y = action[0]
            x = action[1]
            if self.is_obstacle(y, x):
                actions.remove(action)

        return actions


class Ferz(Piece):
    def __init__(self, x, y, cols, rows, grid):
        super().__init__('Ferz', x, y, cols, rows, grid)

    def get_actions(self):
        diag_left_up = (self.get_y() + 1, self.get_x() - 1)
        diag_right_up = (self.get_y() + 1, self.get_x() + 1)
        diag_left_down = (self.get_y() - 1, self.get_x() - 1)
        diag_right_down = (self.get_y() - 1, self.get_x() + 1)

        actions = [diag_left_up, diag_right_up, diag_left_down, diag_right_down]
        copy_actions = actions.copy()
        for action in copy_actions:
            # assume a is start
            if self.is_not_valid(action):
                actions.remove(action)

        # remove actions in obstacles
        copy_actions = actions.copy()
        for action in copy_actions:
            y = action[0]
            x = action[1]
            if self.is_obstacle(y, x):
                actions.remove(action)
        return actions


class Princess(Piece):
    def __init__(self, x, y, cols, rows, grid):
        super().__init__('Princess', x, y, cols, rows, grid)

    def get_actions(self):
        actions = []
        # bishop
        step_left = 0
        for i in range(self.get_x() - 1, - 1, -1):
            step_left -= 1
            y = self.get_y() + step_left
            x = i
            if len(self.grid) > y:
                self.is_obstacle(y, x)
                if y < 0 or self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        step_right = 0
        for i in range(self.get_x() + 1, self.get_max_cols()):
            step_right += 1
            y = self.get_y() + step_right
            x = i
            if len(self.grid) > y:
                if self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        step_down = 0
        for i in range(self.get_y() - 1, - 1, -1):
            step_down += 1
            y = i
            x = self.get_x() + step_down
            if len(self.grid[0]) > x:
                if self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        step_up = 0
        for i in range(self.get_y() + 1, self.get_max_rows()):
            step_up += 1
            y = i
            x = self.get_x() - step_up
            if x >= 0:
                if self.is_obstacle(y, x):
                    break
                action = (y, x)
                actions.append(action)

        up_left = (self.get_y() + 2, self.get_x() - 1)
        up_right = (self.get_y() + 2, self.get_x() + 1)
        down_left = (self.get_y() - 2, self.get_x() - 1)
        down_right = (self.get_y() - 2, self.get_x() + 1)
        left_up = (self.get_y() + 1, self.get_x() - 2)
        left_down = (self.get_y() - 1, self.get_x() - 2)
        right_up = (self.get_y() + 1, self.get_x() + 2)
        right_down = (self.get_y() - 1, self.get_x() + 2)

        temp = [up_left, up_right, right_up, right_down, down_right, down_left, left_down, left_up]

        actions.extend(temp)
        copy_actions = actions.copy()
        for action in copy_actions:
            # assume a is start
            if self.is_not_valid(action):
                actions.remove(action)

        # remove actions in obstacles
        copy_actions = actions.copy()
        for action in copy_actions:
            y = action[0]
            x = action[1]
            if self.is_obstacle(y, x):
                actions.remove(action)
        return actions


class Empress(Piece):
    def __init__(self, x, y, cols, rows, grid):
        super().__init__('Empress', x, y, cols, rows, grid)

    def get_actions(self):
        actions = []
        # rook
        for i in range(self.get_x() - 1, -1, -1):
            y = self.get_y()
            x = i
            if self.is_obstacle(y, x):
                break
            action = (self.get_y(), i)
            actions.append(action)

        for i in range(self.get_x() + 1, self.get_max_cols()):
            y = self.get_y()
            x = i
            if self.is_obstacle(y, x):
                break
            action = (self.get_y(), i)
            actions.append(action)

        for i in range(self.get_y() - 1, -1, -1):
            y = i
            x = self.get_x()
            if self.is_obstacle(y, x):
                break
            action = (i, self.get_x())
            actions.append(action)

        for i in range(self.get_y() + 1, self.get_max_rows()):
            y = i
            x = self.get_x()
            if self.is_obstacle(y, x):
                break
            action = (i, self.get_x())
            actions.append(action)

        up_left = (self.get_y() + 2, self.get_x() - 1)
        up_right = (self.get_y() + 2, self.get_x() + 1)
        down_left = (self.get_y() - 2, self.get_x() - 1)
        down_right = (self.get_y() - 2, self.get_x() + 1)
        left_up = (self.get_y() + 1, self.get_x() - 2)
        left_down = (self.get_y() - 1, self.get_x() - 2)
        right_up = (self.get_y() + 1, self.get_x() + 2)
        right_down = (self.get_y() - 1, self.get_x() + 2)

        temp = [up_left, up_right, right_up, right_down, down_right, down_left, left_down, left_up]

        actions.extend(temp)
        copy_actions = actions.copy()
        for action in copy_actions:
            # assume a is start
            if self.is_not_valid(action):
                actions.remove(action)

        # remove actions in obstacles
        copy_actions = actions.copy()
        for action in copy_actions:
            y = action[0]
            x = action[1]
            if self.is_obstacle(y, x):
                actions.remove(action)

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
    def __init__(self, pieces):
        self.pieces = pieces
        self.cost = self.generate_cost()

    def generate_cost(self):
        attacking = {}
        for piece in self.pieces:
            attacking[piece.get_num_coord()] = piece.get_actions()
        value = 0
        for to_attack in attacking.values():
            for curr_attack in to_attack:
                if curr_attack in attacking.keys():
                    value += 1
        return value

    def answer(self):
        answer = {}
        for piece in self.get_pieces():
            answer[piece.get_coord()] = piece.get_piece_name()
        return answer

    def get_cost(self):
        return self.cost

    def get_pieces(self):
        return self.pieces

    def num_pieces_left(self):
        return len(self.pieces)

    def is_goal(self):
        return self.get_cost() == 0


#############################################################################
######## Implement Search Algorithm
#############################################################################

def get_neighbour(pieces, i):
    piece_to_remove_coord = pieces[i].get_num_coord()
    remaining_pieces = []

    # deep copy
    for piece in pieces:
        if not piece.get_num_coord() == piece_to_remove_coord:
            remaining_pieces.append(piece)

    return State(remaining_pieces)


def best_neighbour(state):
    best_state = state

    for i in range(state.num_pieces_left()):
        curr_state = get_neighbour(state.get_pieces(), i)
        if best_state.get_cost() >= curr_state.get_cost():
            best_state = curr_state

    return best_state


def search(rows, cols, grid, pieces, k):
    pieces_list = []

    for coord in pieces:
        piece_name = pieces[coord]
        y = coord[1]
        x = coord[0]
        if piece_name == "King":
            piece = King(y, x, cols, rows, grid)
        elif piece_name == "Rook":
            piece = Rook(y, x, cols, rows, grid)
        elif piece_name == "Bishop":
            piece = Bishop(y, x, cols, rows, grid)
        elif piece_name == "Queen":
            piece = Queen(y, x, cols, rows, grid)
        elif piece_name == "Knight":
            piece = Knight(y, x, cols, rows, grid)
        elif piece_name == "Ferz":
            piece = Ferz(y, x, cols, rows, grid)
        elif piece_name == "Princess":
            piece = Princess(y, x, cols, rows, grid)
        elif piece_name == "Empress":
            piece = Empress(y, x, cols, rows, grid)
        pieces_list.append(piece)

    possible = []

    for i in range(len(pieces_list)):
        state = get_neighbour(pieces_list, i)
        possible.append(state)
    shuffle(possible)

    for i in range(len(possible)):
        state = possible[i]
        while state.num_pieces_left() > int(k):
            state = best_neighbour(state)
            if state.is_goal():
                return state.answer()


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))
    cols = int(get_par(handle.readline()))
    grid = [[0 for j in range(cols)] for i in range(rows)]
    k = 0
    pieces = {}

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()

    k = handle.readline().split(":")[1].strip()  # Read in value of k

    piece_nums = get_par(handle.readline()).split()
    num_pieces = 0
    for num in piece_nums:
        num_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        pieces[coords] = piece

    return rows, cols, grid, pieces, k


def add_piece(comma_seperated):
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r, c), piece]


# Returns row and col index in integers respectively
def from_chess_coord(ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces (String): King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    testcase = sys.argv[1]  # Do not remove. This is your input testfile.
    rows, cols, grid, pieces, k = parse(testcase)
    goalstate = search(rows, cols, grid, pieces, k)
    return goalstate  # Format to be returned

# print(run_local())