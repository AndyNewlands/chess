
import os
import time
import random
from os import path
from tkinter import *
from PIL import Image, ImageTk
from stockfish import Stockfish

window = Tk()

WHITE_PIECE = 'white'
BLACK_PIECE = 'black'

SELECTION_HIGHLIGHT = 'magenta2'
DESTINATION_HIGHLIGHT = 'green yellow'
HIGHLIGHT_THICKNESS = 4

WHITES = ['light gray', 'cyan', 'cornflower blue']
BLACKS = ['dark gray', 'dark turquoise', 'dark khaki']
WHITE_SQUARE = WHITES[random.randint(0, len(WHITES) - 1)]
BLACK_SQUARE = BLACKS[random.randint(0, len(BLACKS) - 1)]

GRAY = 'gray'

NUM_ROWS = 8
NUM_COLS = 8

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
window.geometry('{0}x{1}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

BOARD_WIDTH = 800
BOARD_HEIGHT = 800
BOARD_BORDER_THICKNESS = 4

ROW_HEIGHT = int(BOARD_WIDTH / NUM_ROWS)
COL_WIDTH = int(BOARD_HEIGHT / NUM_COLS)

IMAGE_BORDER_THICKNESS = 5

IMAGE_WIDTH = COL_WIDTH - (2 * IMAGE_BORDER_THICKNESS)
IMAGE_HEIGHT = ROW_HEIGHT - (2 * IMAGE_BORDER_THICKNESS)

BOARD_X = (WINDOW_WIDTH - BOARD_WIDTH) / 2
BOARD_Y = (WINDOW_HEIGHT - BOARD_HEIGHT) / 2

IMAGE_PATH = path.join(path.dirname(__file__), 'PNG')
STOCKFISH_PATH = path.join(path.dirname(__file__), 'stockfish\\stockfish-windows-x86-64-avx2')

window.title('Chess AssIst V1.0 by Laurie J Sullivan - Copyright 2024')

# TODO: Remove unwanted print statements & comments

AUTO_MOVE_DELAY = 1000

FEN_COL_MAP = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}

FEN_ROW_MAP = {
    '1': 7,
    '2': 6,
    '3': 5,
    '4': 4,
    '5': 3,
    '6': 2,
    '7': 1,
    '8': 0
}

COL_FEN_MAP = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h'
}

ROW_FEN_MAP = {
    0: '1',
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6',
    6: '7',
    7: '8'
}


class Move(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other_move):
        # This comparison op allows a list of Move instances to be searched for a matching Move instance
        return self.row == other_move.row and self.col == other_move.col

# Record of a piece being 'taken'
class Take(object):
    def __init__(
            self,
            taking_piece,
            taken_piece):
        # 'flattening' the pieces may make it easier to search for takes, later
        self.taking_piece = taking_piece
        self.taking_piece_type = taking_piece.type
        self.taking_piece_row = taking_piece.row
        self.taking_piece_col = taking_piece.col
        self.taking_piece_colour = taking_piece.colour
        self.taken_piece = taken_piece
        self.taken_piece_type = taken_piece.type
        self.taken_piece_row = taken_piece.row
        self.taken_piece_col = taken_piece.col
        self.taken_piece_colour = taken_piece.colour

class Chessboard(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.turn_colour = None
        self.status_label = None
        self.selected_square = None
        self.valid_moves = []
        self.taking_moves = []
        # TODO: Manage these from the menu
        self.auto_move_black = True
        self.auto_move_white = False

        # IMPORTANT the code assumes WHITE is always at the bottom of the board
        # Things will go wrong if we mess with that assumption!!!
        self.initial_layout = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
        ]
        # Create our canvas
        self.canvas = Canvas(window, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg='red',
                             highlightbackground='black',
                             highlightthickness=BOARD_BORDER_THICKNESS)
        # Handle mouse clicks
        self.canvas.bind('<Button-1>', self.handle_left_click)
        self.canvas.bind('<Button-3>', self.handle_right_click)

        self.canvas.pack(expand=True)

        # Build and setup board
        self.squares = self.create_board()
        self.setup_board(self.squares, self.initial_layout)

        # THIS is the CLEVER bit!
        self.stockfish = Stockfish(path=STOCKFISH_PATH)

    def create_board(self):
        squares = []
        for row in range(NUM_ROWS):
            current_row = []
            for col in range(NUM_COLS):
                current_row.append(Square(self.canvas, row, col, ROW_HEIGHT, COL_WIDTH))
            squares.append(current_row)
        return squares

    def setup_board(self, squares, layout):
        piece_types = {
            'br': [Rook, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'b_rook.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'bn': [Knight, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'b_knight.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'bb': [Bishop, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'b_bishop.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'bq': [Queen, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'b_queen.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'bk': [King, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'b_king.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'bp': [Pawn, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'b_pawn.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'wr': [Rook, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'w_rook.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'wn': [Knight, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'w_knight.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'wb': [Bishop, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'w_bishop.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'wq': [Queen, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'w_queen.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'wk': [King, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'w_king.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            'wp': [Pawn, ImageTk.PhotoImage(
                Image.open(os.path.join(IMAGE_PATH, 'w_pawn.png')).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))]
        }

        self.turn_colour = None
        self.status_label = None
        self.selected_square = None
        self.valid_moves = []
        self.taking_moves = []

        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                piece_type = layout[row][col]
                if piece_type != ' ':
                    if piece_type[0] == 'w':
                        colour = WHITE_PIECE
                    else:
                        colour = BLACK_PIECE

                    # For the next line of code (below)
                    # Each VALUE from the piece_types DICTIONARY is a LIST.  So...
                    # [piece_type] selects the correct LIST from the dictionary
                    # [0] selects the CLASS from the selected LIST
                    # [1] selects the piece's IMAGE from the selected LIST
                    squares[row][col].current_piece = piece_types[piece_type][0](self.squares,
                                                                                 piece_type,
                                                                                 piece_types[piece_type][1],
                                                                                 colour, row, col)

    def draw(self):
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                self.squares[row][col].draw()

    def handle_left_click(self, event):
        if (self.turn_colour == BLACK_PIECE and self.auto_move_black) or \
                (self.turn_colour == WHITE_PIECE and self.auto_move_white):
            # We'll mess things up if we process clicks while doing auto-play
            return

        row = int(event.y / ROW_HEIGHT)
        col = int(event.x / COL_WIDTH)

        if self.selected_square is not None and self.is_valid_destination(row, col):
            self.do_move(row, col)
            return

        prev_selection = self.selected_square
        sq = self.squares[row][col]
        if self.selected_square is not None:
            # If the clicked square is already selected, un-select it (and clear valid moves)
            self.clear_current_moves()
            self.selected_square = None
        if sq != prev_selection:
            # If nothing is selected, check if this square contains a piece which can move
            self.valid_moves = sq.valid_moves(self.turn_colour)

            self.remove_self_checking_moves(sq, self.valid_moves)

            if self.valid_moves:
                sq.highlight(True, SELECTION_HIGHLIGHT)
                self.selected_square = sq
                for destination in self.valid_moves:
                    self.squares[destination.row][destination.col].highlight(True, DESTINATION_HIGHLIGHT)

    def handle_right_click(self, event):
        if (self.turn_colour == BLACK_PIECE and self.auto_move_black) or \
                (self.turn_colour == WHITE_PIECE and self.auto_move_white):
            # We'll mess things up if we process clicks while doing auto-play
            return

        self.stockfish.set_fen_position(self.generate_fen_position())
        # print(self.stockfish.get_board_visual())

        # TODO: Introduce some more random play (try to avoid endless loop / stalemate / draw)
        #       Maybe something like this....?
        # fen_move = self.stockfish.get_top_moves(3)[random.randint(0,2)]['Move']
        fen_move = self.stockfish.get_best_move()
        # print(fen_move)
        self.highlight_fen_move(fen_move)

    def is_valid_destination(self, row, col):
        # NOTE: We could just flag individual squares as valid destination, when we highlight/un-highlight
        for move in self.valid_moves:
            if move.row == row and move.col == col:
                return True
        return False

    def clear_current_moves(self):
        if self.selected_square is not None:
            self.selected_square.highlight(False)
        for destination in self.valid_moves:
            self.squares[destination.row][destination.col].highlight(False)
        self.valid_moves = []

    def highlight_fen_move(self, fen_move):
        if fen_move is None or len(fen_move) != 4:
            return None
        self.clear_current_moves()
        self.selected_square = self.squares[FEN_ROW_MAP[fen_move[1]]][FEN_COL_MAP[fen_move[0]]]
        recommended_move = Move(FEN_ROW_MAP[fen_move[3]], FEN_COL_MAP[fen_move[2]])
        self.valid_moves = [recommended_move]
        self.selected_square.highlight(True, SELECTION_HIGHLIGHT)
        self.squares[recommended_move.row][recommended_move.col].highlight(True, DESTINATION_HIGHLIGHT)

    def fen_move_from_row_col(self, origin_row, origin_col, dest_row, dest_col):
        fen_move = ''
        fen_move += COL_FEN_MAP[origin_row]
        fen_move += ROW_FEN_MAP[origin_col]
        fen_move += COL_FEN_MAP[dest_row]
        fen_move += ROW_FEN_MAP[dest_col]
        return fen_move

    def do_preset_move(self):
        # Execute a specific move (stored in the first Move in self.valid moves)
        # This is usually called on a Tkinter delay (using after()) to allow the
        # display to be updated before making this move.
        self.do_move(self.valid_moves[0].row, self.valid_moves[0].col)

    def do_move(self, row, col):
        self.clear_current_moves()
        piece = self.selected_square.current_piece
        self.selected_square.set_current_piece(None)
        self.record_take(piece, self.squares[row][col].current_piece)
        self.squares[row][col].set_current_piece(piece)
        self.selected_square = None
        self.set_next_turn()

    def record_take(self, taking_piece, taken_piece):
        if taking_piece is None or taken_piece is None:
            return
        self.taking_moves.append(Take(taking_piece, taken_piece))

    def remove_self_checking_moves(self, moving_square, moves):
        # Pick up the piece which will move
        moving_piece = moving_square.current_piece
        moving_square.current_piece = None

        checking_moves = []
        for move in moves:
            taken_piece = self.squares[move.row][move.col].current_piece
            self.squares[move.row][move.col].current_piece = moving_piece
            if self.is_check(self.turn_colour):
                checking_moves.append(move)
            # Replace anything we temporarily took
            self.squares[move.row][move.col].current_piece = taken_piece

        # Put the moving piece back
        moving_square.current_piece = moving_piece

        # Remove any bad moves from valid_moves
        for bad_move in checking_moves:
            moves.remove(bad_move)
        
        return moves

    def set_next_turn(self):
        # TODO: BUG - not stopping game after detecting checkmate

        last_turn_colour = self.turn_colour
        if self.turn_colour == WHITE_PIECE:
            self.turn_colour = BLACK_PIECE
        else:
            self.turn_colour = WHITE_PIECE

        if self.is_checkmate(self.turn_colour):
            # THE END! (no valid moves found)
            message = 'CHECKMATE! GAME OVER! {0} WINS!'.format(last_turn_colour.upper())
            self.turn_colour = None
            self.show_game_takes()
            return
        else:
            if (self.turn_colour == BLACK_PIECE and self.auto_move_black) or \
                    (self.turn_colour == WHITE_PIECE and self.auto_move_white):
                mode = 'auto'
            else:
                mode = 'manual'
            message = 'Next move: {0} ({1})'.format(self.turn_colour.upper(), mode)
        if self.status_label is None:
            self.status_label = Label(window, justify=CENTER, font=('Helvetica', 24))
        self.status_label.configure(text=message)
        self.status_label.pack()

        if (self.turn_colour == BLACK_PIECE and self.auto_move_black) or \
                (self.turn_colour == WHITE_PIECE and self.auto_move_white):
            self.stockfish.set_fen_position(self.generate_fen_position())
            fen_move = self.stockfish.get_best_move()
            self.highlight_fen_move(fen_move)
            window.after(AUTO_MOVE_DELAY, self.do_preset_move)

    def show_game_takes(self):
        # TODO: Display this info on the main app window, as the game progresses (not at the end)?
        for take in self.taking_moves:
            print('Move:{0} -> {1} takes {2}'.format(
                self.fen_move_from_row_col(take.taking_piece_row, take.taking_piece_col,
                                                 take.taken_piece_row, take.taken_piece_col),
                take.taking_piece_type, take.taken_piece_type))

    def is_checkmate(self, colour):
        if not self.is_check(colour):
            return False
        for row in self.squares:
            for square in row:
                try:
                    if self.remove_self_checking_moves(square, square.valid_moves(colour)):
                        return False
                except AttributeError:
                    pass

        return True
    def is_check(self, colour):
        king_pos = self.get_king_pos(colour)
        if colour == WHITE_PIECE:
            enemy_colour = BLACK_PIECE
        else:
            enemy_colour = WHITE_PIECE
        if king_pos is None:
            raise Exception("Oops! Can't find KING!!")

        for row in self.squares:
            for square in row:
                # Expect an exception if there is no piece in the square
                moves = square.valid_moves(enemy_colour)
                if king_pos in moves:
                    return True
        return False

    def get_king_pos(self, colour):
        if colour == WHITE_PIECE:
            king_type = 'wk'
        else:
            king_type = 'bk'
        for row in self.squares:
            for square in row:
                try:
                    # Expect an exception if there is no piece in the square
                    if square.current_piece.type == king_type:
                        return Move(square.row, square.col)
                except AttributeError:
                    pass
        return None

    def generate_fen_position(self):
        fen_pos = ''
        for row in self.squares:
            for square in row:
                try:
                    piece_type = square.current_piece.type[1:]
                    if square.current_piece.colour == WHITE_PIECE:
                        fen_pos += piece_type.upper()
                    else:
                        # The piece types are already lower case
                        # but we set the case explicitly
                        # (just in case that ever changes)
                        fen_pos += piece_type.lower()
                except AttributeError:
                    # TODO: We can shorten the FEN position string by replacing
                    #       multiple '1's with a single digit, representing the
                    #       number of contiguous empty squares (we just need count them)
                    fen_pos += '1'  # Empty square
            fen_pos += '/'
        # Don't want the final '/'
        fen_pos = fen_pos[0:-1]
        if self.turn_colour == WHITE_PIECE:
            fen_pos += ' w'
        else:
            fen_pos += ' b'
        fen_pos += ' - - 0 1'
        return fen_pos


class Square(object):
    def __init__(self, canvas, row, col, height, width):
        super().__init__()
        self.canvas = canvas
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        # Add horizontal and vertical offset to allow for BOARD_BORDER_THICKNESS
        self.x_pos = (col * width) + BOARD_BORDER_THICKNESS - 1
        self.y_pos = (row * height) + BOARD_BORDER_THICKNESS - 1
        self.x_centre = self.x_pos + (width / 2)
        self.y_centre = self.y_pos + (height / 2)
        self.position = (self.row, self.col)
        total = row + col
        if total % 2 == 0:
            self.colour = WHITE_SQUARE
        else:
            self.colour = BLACK_SQUARE
        self.current_piece = None

    def valid_moves(self, turn_colour):
        if self.current_piece is None or self.current_piece.colour != turn_colour:
            return []
        return self.current_piece.valid_moves()

    def set_current_piece(self, piece):
        if self.current_piece != piece:
            self.current_piece = piece
            # TODO: Add some exception handlers to see if we gain marks for using them?
            if piece is not None:
                piece.row = self.row
                piece.col = self.col
                piece.has_moved = True
            self.draw()

    def draw(self):
        self.canvas.create_rectangle(self.x_pos, self.y_pos, self.x_pos + self.width, self.y_pos + self.height,
                                     fill=self.colour)
        if self.current_piece is not None:
            self.current_piece.draw(self.canvas, self.x_centre, self.y_centre)

    def highlight(self, do_highlight, colour=None):
        if do_highlight:
            outline_colour = colour
        else:
            outline_colour = self.colour  # This overwrites highlight with the square's colour (erases the highlight)
        adjustment = HIGHLIGHT_THICKNESS / 2
        self.canvas.create_rectangle(self.x_pos + adjustment + 1, self.y_pos + adjustment + 1,
                                     self.x_pos + self.width - adjustment, self.y_pos + self.height - adjustment,
                                     outline=outline_colour, width=HIGHLIGHT_THICKNESS)


class Piece(object):
    def __init__(self, board_squares, type, image, colour, row, col):
        super().__init__()
        self.board_squares = board_squares
        self.type = type
        self.image = image
        self.colour = colour
        self.has_moved = False
        self.captured = False
        self.row = row
        self.col = col

    def set_pos(self, row, col):
        self.row = row
        self.col = col

    def valid_moves(self):
        return []

    def draw(self, canvas, x, y):
        canvas.create_image(x, y, image=self.image, anchor='center')
        canvas.pack()


class Rook(Piece):
    def __init__(self, board_squares, type, image, colour, row, col):
        super().__init__(board_squares, type, image, colour, row, col)

    def valid_moves(self):
        moves = []
        # CHECK HORIZONTAL MOVES
        # Get right-moves
        for col in range(self.col + 1, 8):
            if self.board_squares[self.row][col].current_piece is not None:
                if self.board_squares[self.row][col].current_piece.colour != self.colour:
                    moves.append(Move(self.row, col))
                break
            else:
                moves.append(Move(self.row, col))
        # Get left-moves
        for col in range(self.col - 1, -1, -1):
            if self.board_squares[self.row][col].current_piece is not None:
                if self.board_squares[self.row][col].current_piece.colour != self.colour:
                    moves.append(Move(self.row, col))
                break
            else:
                moves.append(Move(self.row, col))
        # CHECK VERTICAL MOVES
        # Get down-moves
        for row in range(self.row + 1, 8):
            if self.board_squares[row][self.col].current_piece is not None:
                if self.board_squares[row][self.col].current_piece.colour != self.colour:
                    moves.append(Move(row, self.col))
                break
            else:
                moves.append(Move(row, self.col))
        # Get down-moves
        for row in range(self.row - 1, -1, -1):
            if self.board_squares[row][self.col].current_piece is not None:
                if self.board_squares[row][self.col].current_piece.colour != self.colour:
                    moves.append(Move(row, self.col))
                break
            else:
                moves.append(Move(row, self.col))

        return moves


class Knight(Piece):
    RELATIVE_MOVES = [
        (-2, 1),
        (-1, 2),
        (-2, -1),
        (-1, -2),
        (2, 1),
        (1, 2),
        (2, -1),
        (1, -2)
    ]
    def __init__(self, board_squares, type, image, colour, row, col):
        super().__init__(board_squares, type, image, colour, row, col)

    def valid_moves(self):
        moves = []
        for move in Knight.RELATIVE_MOVES:
            x = move[0]
            y = move[1]
            move_row = self.row + y
            move_col = self.col + x
            # Keep on the board
            if move_col < 0 or move_col >= NUM_COLS or move_row < 0 or move_row >= NUM_ROWS:
                continue
            if self.board_squares[move_row][move_col].current_piece is not None:
                if self.board_squares[move_row][move_col].current_piece.colour != self.colour:
                    moves.append(Move(move_row, move_col))
            else:
                moves.append(Move(move_row, move_col))

        return moves


class Bishop(Piece):
    def __init__(self, board_squares, type, image, colour, row, col):
        super().__init__(board_squares, type, image, colour, row, col)

    def valid_moves(self):
        moves = []
        # CHECK HORIZONTAL MOVES
        # Get right-up moves
        row = self.row
        for col in range(self.col + 1, NUM_COLS):
            row -= 1
            if row < 0:
                break
            if self.board_squares[row][col].current_piece is not None:
                if self.board_squares[row][col].current_piece.colour != self.colour:
                    moves.append(Move(row, col))
                break
            else:
                moves.append(Move(row, col))
        # Get left-up moves
        row = self.row
        for col in range(self.col - 1, -1, -1):
            row -= 1
            if row < 0:
                break
            if self.board_squares[row][col].current_piece is not None:
                if self.board_squares[row][col].current_piece.colour != self.colour:
                    moves.append(Move(row, col))
                break
            else:
                moves.append(Move(row, col))
        # CHECK VERTICAL MOVES
        # Get right-down moves
        col = self.col
        for row in range(self.row + 1, NUM_COLS):
            col += 1
            if col >= NUM_COLS:
                break
            if self.board_squares[row][col].current_piece is not None:
                if self.board_squares[row][col].current_piece.colour != self.colour:
                    moves.append(Move(row, col))
                break
            else:
                moves.append(Move(row, col))
        # Get left-down moves
        col = self.col
        for row in range(self.row + 1, NUM_COLS):
            col -= 1
            if col < 0:
                break
            if self.board_squares[row][col].current_piece is not None:
                if self.board_squares[row][col].current_piece.colour != self.colour:
                    moves.append(Move(row, col))
                break
            else:
                moves.append(Move(row, col))

        return moves


class Pawn(Piece):
    def __init__(self, board_squares, type, image, colour, row, col):
        super().__init__(board_squares, type, image, colour, row, col)

    def valid_moves(self):
        moves = []
        if self.colour == WHITE_PIECE:
            direction = -1
        else:
            direction = 1

        if not self.has_moved:
            forward_limit = 2
        else:
            forward_limit = 1

        for row in range(self.row + direction, self.row + (direction * (forward_limit + 1)), direction):
            if self.board_squares[row][self.col].current_piece is not None:
                break
            moves.append(Move(row, self.col))

        # Look for diagonal take options

        # RIGHT
        if self.col + 1 < 8 and self.board_squares[self.row + direction][self.col + 1].current_piece is not None and \
                self.board_squares[self.row + direction][self.col + 1].current_piece.colour != self.colour:
            moves.append(Move(self.row + direction, self.col + 1))

        # LEFT
        if self.col - 1 >= 0 and self.board_squares[self.row + direction][self.col - 1].current_piece is not None and \
                self.board_squares[self.row + direction][self.col - 1].current_piece.colour != self.colour:
            moves.append(Move(self.row + direction, self.col - 1))

        return moves


class Queen(Piece):
    def __init__(self, board_squares, type, image, colour, row, col):
        super().__init__(board_squares, type, image, colour, row, col)

    def valid_moves(self):
        moves = []
        # CHECK HORIZONTAL MOVES
        # Get right-moves
        for col in range(self.col + 1, NUM_COLS):
            if self.board_squares[self.row][col].current_piece is not None:
                if self.board_squares[self.row][col].current_piece.colour != self.colour:
                    moves.append(Move(self.row, col))
                break
            else:
                moves.append(Move(self.row, col))
        # Get left-moves
        for col in range(self.col - 1, -1, -1):
            if self.board_squares[self.row][col].current_piece is not None:
                if self.board_squares[self.row][col].current_piece.colour != self.colour:
                    moves.append(Move(self.row, col))
                break
            else:
                moves.append(Move(self.row, col))
        # CHECK VERTICAL MOVES
        # Get down-moves
        for row in range(self.row + 1, NUM_COLS):
            if self.board_squares[row][self.col].current_piece is not None:
                if self.board_squares[row][self.col].current_piece.colour != self.colour:
                    moves.append(Move(row, self.col))
                break
            else:
                moves.append(Move(row, self.col))
        # Get down-moves
        for row in range(self.row - 1, -1, -1):
            if self.board_squares[row][self.col].current_piece is not None:
                if self.board_squares[row][self.col].current_piece.colour != self.colour:
                    moves.append(Move(row, self.col))
                break
            else:
                moves.append(Move(row, self.col))

        # CHECK HORIZONTAL MOVES
        # Get right-up moves
        row = self.row
        for col in range(self.col + 1, NUM_COLS):
            row -= 1
            if row < 0:
                break
            if self.board_squares[row][col].current_piece is not None:
                if self.board_squares[row][col].current_piece.colour != self.colour:
                    moves.append(Move(row, col))
                break
            else:
                moves.append(Move(row, col))
        # Get left-up moves
        row = self.row
        for col in range(self.col - 1, -1, -1):
            row -= 1
            if row < 0:
                break
            if self.board_squares[row][col].current_piece is not None:
                if self.board_squares[row][col].current_piece.colour != self.colour:
                    moves.append(Move(row, col))
                break
            else:
                moves.append(Move(row, col))
        # CHECK VERTICAL MOVES
        # Get right-down moves
        col = self.col
        for row in range(self.row + 1, NUM_COLS):
            col += 1
            if col >= 8:
                break
            if self.board_squares[row][col].current_piece is not None:
                if self.board_squares[row][col].current_piece.colour != self.colour:
                    moves.append(Move(row, col))
                break
            else:
                moves.append(Move(row, col))
        # Get left-down moves
        col = self.col
        for row in range(self.row + 1, NUM_COLS):
            col -= 1
            if col < 0:
                break
            if self.board_squares[row][col].current_piece is not None:
                if self.board_squares[row][col].current_piece.colour != self.colour:
                    moves.append(Move(row, col))
                break
            else:
                moves.append(Move(row, col))

        return moves


class King(Piece):
    def __init__(self, board_squares, type, image, colour, row, col):
        super().__init__(board_squares, type, image, colour, row, col)

    def valid_moves(self):
        moves = []
        for row in range (self.row - 1, self.row + 2):
            for col in range (self.col - 1, self.col + 2):
                if row >=0 and row < NUM_ROWS and col >=0 and col < NUM_COLS:
                    if self.board_squares[row][col].current_piece is not None:
                        if self.board_squares[row][col].current_piece.colour != self.colour:
                            moves.append(Move(row, col))
                    else:
                        moves.append(Move(row, col))

        return moves


# New board-instance
chessboard = Chessboard(BOARD_WIDTH, BOARD_HEIGHT)
# Draw the board
chessboard.draw()
# Start the game
chessboard.set_next_turn()

window.mainloop()
