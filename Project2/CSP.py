import sys
import heapq


# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
class Piece:
    pass


def not_valid(action, col, row):
    return action[1] >= col or action[1] < 0 or action[0] < 0 or action[0] >= row


def king_actions(y, x, grid, row, col):
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
        new_y = action[0]
        new_x = action[1]
        if grid[new_y][new_x] == -1:
            actions.remove(action)

    actions.append((y, x))
    return actions


def rook_actions(y, x, grid, row, col):
    actions = []

    for i in range(x - 1, -1, -1):
        if grid[y][i] == -1:
            break
        action = (y, i)
        actions.append(action)

    for i in range(x + 1, col):
        if grid[y][i] == -1:
            break
        action = (y, i)
        actions.append(action)

    for i in range(y - 1, -1, -1):
        if grid[i][x] == - 1:
            break
        action = (i, x)
        actions.append(action)

    for i in range(y + 1, row):
        if grid[i][x] == - 1:
            break
        action = (i, x)
        actions.append(action)

    actions.append((y, x))
    return actions


def bishop_actions(y, x, grid, row, col):
    actions = []

    step_left = 0
    for i in range(x - 1, - 1, -1):
        step_left -= 1
        new_y = y + step_left
        if new_y < col:
            if new_y < 0 or grid[new_y][i] == - 1:
                break
            piece = (new_y, i)
            actions.append(piece)

    step_right = 0
    for i in range(x + 1, col):
        step_right += 1
        new_y = y + step_right
        if new_y < row:
            if grid[new_y][i] == - 1:
                break
            piece = (new_y, i)
            actions.append(piece)

    step_down = 0
    for i in range(y - 1, - 1, -1):
        step_down += 1
        new_x = x + step_down
        if new_x < col:
            if grid[i][new_x] == -1:
                break
            piece = (i, new_x)
            actions.append(piece)

    step_up = 0
    for i in range(y + 1, row):
        step_up += 1
        new_x = x - step_up
        if new_x >= 0:
            if grid[i][new_x] == -1:
                break
            piece = (i, new_x)
            actions.append(piece)

    actions.append((y, x))
    return actions


def queen_actions(y, x, grid, row, col):
    actions = []

    # rook
    for i in range(x - 1, -1, -1):
        if grid[y][i] == -1:
            break
        action = (y, i)
        actions.append(action)

    for i in range(x + 1, col):
        if grid[y][i] == -1:
            break
        action = (y, i)
        actions.append(action)

    for i in range(y - 1, -1, -1):
        if grid[i][x] == - 1:
            break
        action = (i, x)
        actions.append(action)

    for i in range(y + 1, row):
        if grid[i][x] == - 1:
            break
        action = (i, x)
        actions.append(action)

    # bishop
    step_left = 0
    for i in range(x - 1, - 1, -1):
        step_left -= 1
        new_y = y + step_left
        if new_y < col:
            if new_y < 0 or grid[new_y][i] == - 1:
                break
            piece = (new_y, i)
            actions.append(piece)

    step_right = 0
    for i in range(x + 1, col):
        step_right += 1
        new_y = y + step_right
        if new_y < row:
            if grid[new_y][i] == - 1:
                break
            piece = (new_y, i)
            actions.append(piece)

    step_down = 0
    for i in range(y - 1, - 1, -1):
        step_down += 1
        new_x = x + step_down
        if new_x < col:
            if grid[i][new_x] == -1:
                break
            piece = (i, new_x)
            actions.append(piece)

    step_up = 0
    for i in range(y + 1, row):
        step_up += 1
        new_x = x - step_up
        if new_x >= 0:
            if grid[i][new_x] == -1:
                break
            piece = (i, new_x)
            actions.append(piece)

    actions.append((y, x))
    return actions


def knight_actions(y, x, grid, row, col):
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
        new_y = action[0]
        new_x = action[1]
        if grid[new_y][new_x] == -1:
            actions.remove(action)

    actions.append((y, x))
    return actions


def ferz_actions(y, x, grid, row, col):
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
        new_y = action[0]
        new_x = action[1]
        if grid[new_y][new_x] == -1:
            actions.remove(action)

    actions.append((y, x))
    return actions


def princess_actions(y, x, grid, row, col):
    ls = []

    step_left = 0
    for i in range(x - 1, - 1, -1):
        step_left -= 1
        new_y = y + step_left
        if new_y < col:
            if new_y < 0 or grid[new_y][i] == - 1:
                break
            piece = (new_y, i)
            ls.append(piece)

    step_right = 0
    for i in range(x + 1, col):
        step_right += 1
        new_y = y + step_right
        if new_y < row:
            if grid[new_y][i] == - 1:
                break
            piece = (new_y, i)
            ls.append(piece)

    step_down = 0
    for i in range(y - 1, - 1, -1):
        step_down += 1
        new_x = x + step_down
        if new_x < col:
            if grid[i][new_x] == -1:
                break
            piece = (i, new_x)
            ls.append(piece)

    step_up = 0
    for i in range(y + 1, row):
        step_up += 1
        new_x = x - step_up
        if new_x >= 0:
            if grid[i][new_x] == -1:
                break
            piece = (i, new_x)
            ls.append(piece)

    # knight
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
        new_y = action[0]
        new_x = action[1]
        if grid[new_y][new_x] == -1:
            actions.remove(action)

    actions.append((y, x))
    return actions


def empress_actions(y, x, grid, row, col):
    ls = []

    # rook
    for i in range(x - 1, -1, -1):
        if grid[y][i] == -1:
            break
        action = (y, i)
        ls.append(action)

    for i in range(x + 1, col):
        if grid[y][i] == -1:
            break
        action = (y, i)
        ls.append(action)

    for i in range(y - 1, -1, -1):
        if grid[i][x] == - 1:
            break
        action = (i, x)
        ls.append(action)

    for i in range(y + 1, row):
        if grid[i][x] == - 1:
            break
        action = (i, x)
        ls.append(action)

    # knight
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
        new_y = action[0]
        new_x = action[1]
        if grid[new_y][new_x] == -1:
            actions.remove(action)

    actions.append((y, x))
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
    def __init__(self, num_pieces_placed, num_free_tiles, free_tiles, path):
        self.num_pieces_placed = num_pieces_placed
        self.num_free_tiles = num_free_tiles
        self.free_tiles = free_tiles
        self.path = path

    def __lt__(self, other):
        return self.num_pieces_placed > other.num_pieces_placed or (
                self.num_pieces_placed == other.num_pieces_placed and self.num_free_tiles > other.num_free_tiles)

    def get_num_pieces_placed(self):
        return self.num_pieces_placed

    def get_num_free_tiles(self):
        return self.num_free_tiles

    def get_free_tiles(self):
        return self.free_tiles

    def get_path(self):
        return self.path

    def answer(self):
        ans = {}
        for key, value in self.path.items():
            y = key[0]
            x = chr(key[1] + 97)
            ans[(x, y)] = value
        return ans


#############################################################################
######## Implement Search Algorithm
#############################################################################

def update_pieces(ls, num_pieces, string):
    for i in range(num_pieces):
        ls.append(string)
    return ls


def get_piece_action(piece_name, y, x, grid, row, col):
    if piece_name == "Queen":
        return queen_actions(y, x, grid, row, col)
    elif piece_name == "Empress":
        return empress_actions(y, x, grid, row, col)
    elif piece_name == "Princess":
        return princess_actions(y, x, grid, row, col)
    elif piece_name == "Rook":
        return rook_actions(y, x, grid, row, col)
    elif piece_name == "Bishop":
        return bishop_actions(y, x, grid, row, col)
    elif piece_name == "Knight":
        return knight_actions(y, x, grid, row, col)
    elif piece_name == "King":
        return king_actions(y, x, grid, row, col)
    elif piece_name == "Ferz":
        return ferz_actions(y, x, grid, row, col)


def next_state(state, piece, actions, coord):
    # if piece is attacking another piece, break
    for key in state.get_path():
        for action in actions:
            if key == action:
                return State(-1, -1, {}, {})
    dic = {}
    curr_no_free_tiles = state.get_num_free_tiles()

    for key, value in state.get_free_tiles().items():
        dic[key] = value

    for action in actions:
        if dic[action]:
            dic[action] = False
            curr_no_free_tiles -= 1

    # deep copy
    curr_path = {}
    for key, value in state.get_path().items():
        curr_path[key] = value
    curr_no_pieces = state.get_num_pieces_placed()
    curr_path[coord] = piece
    curr_no_pieces += 1

    return State(curr_no_pieces, curr_no_free_tiles, dic, curr_path)


def search(rows, cols, grid, num_pieces):
    pieces = []
    total_required_pieces = sum(num_pieces)
    num_king = num_pieces[0]
    num_queen = num_pieces[1]
    num_bishop = num_pieces[2]
    num_rook = num_pieces[3]
    num_knight = num_pieces[4]
    num_ferz = num_pieces[5]
    num_princess = num_pieces[6]
    num_empress = num_pieces[7]
    # order of adding add queen, empress, princess, rook, bishop, knight, king, ferz
    pieces = update_pieces(pieces, num_queen, "Queen")
    pieces = update_pieces(pieces, num_empress, "Empress")
    pieces = update_pieces(pieces, num_princess, "Princess")
    pieces = update_pieces(pieces, num_rook, "Rook")
    pieces = update_pieces(pieces, num_bishop, "Bishop")
    pieces = update_pieces(pieces, num_knight, "Knight")
    pieces = update_pieces(pieces, num_king, "King")
    pieces = update_pieces(pieces, num_ferz, "Ferz")

    free_tiles = {}
    num_free_tiles = rows * cols
    # init free tiles dict
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # stored in y, x format
            coord = (j, i)
            if grid[j][i] == -1:
                free_tiles[coord] = False
                num_free_tiles -= 1
            else:
                free_tiles[coord] = True
    pq = []

    init_state = State(0, num_free_tiles, free_tiles, {})
    heapq.heappush(pq, init_state)
    while not len(pq) == 0:
        curr_state = heapq.heappop(pq)
        for key, value in curr_state.get_free_tiles().items():
            if value:
                piece_string = pieces[curr_state.get_num_pieces_placed()]
                actions = get_piece_action(piece_string, key[0], key[1], grid, rows, cols)
                state = next_state(curr_state, piece_string, actions, key)
                if state.get_num_pieces_placed() == -1:
                    continue
                elif state.get_num_pieces_placed() == total_required_pieces:
                    return state.answer()
                heapq.heappush(pq, state)


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

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()

    piece_nums = get_par(handle.readline()).split()
    num_pieces = [int(x) for x in piece_nums]  # List in the order of King, Queen, Bishop, Rook, Knight

    return rows, cols, grid, num_pieces


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
def run_CSP():
    testcase = sys.argv[1]  # Do not remove. This is your input testfile.
    rows, cols, grid, num_pieces = parse(testcase)
    goalstate = search(rows, cols, grid, num_pieces)
    return goalstate  # Format to be returned

#print(run_CSP())