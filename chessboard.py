from tkinter import *
from PIL import Image, ImageTk
import random

import os
from os import path

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
window.geometry("{0}x{1}".format(WINDOW_WIDTH, WINDOW_HEIGHT))

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

return_path = path.join(path.dirname(__file__), 'PNG')

window.title("Chess AI")


class Chessboard():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.turn_colour = None
        self.status_label = None
        self.selected_square = None
        self.valid_moves = []

        # IMPORTANT the code assumes WHITE is always at the bottom of the board
        # Things will go wrong if we mess with that assumption!!!
        self.initial_layout = [
            ["br", "bkn", "bb", "bq", "bk", "bb", "bkn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wkn", "wb", "wq", "wk", "wb", "wkn", "wr"],
        ]
        # Create our canvas
        self.canvas = Canvas(window, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg='red',
                             highlightbackground='black',
                             highlightthickness=BOARD_BORDER_THICKNESS)
        # Handle mouse clicks
        self.canvas.bind('<Button-1>', self.handle_left_click)
        self.canvas.pack(expand=True)

        # Build and setup board
        self.squares = self.create_board()
        self.setup_board(self.squares, self.initial_layout)

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
            "br": [Rook, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "b_rook.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "bkn": [Knight, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "b_knight.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "bb": [Bishop, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "b_bishop.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "bq": [Queen, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "b_queen.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "bk": [King, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "b_king.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "bp": [Pawn, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "b_pawn.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "wr": [Rook, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "w_rook.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "wkn": [Knight, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "w_knight.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "wb": [Bishop, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "w_bishop.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "wq": [Queen, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "w_queen.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "wk": [King, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "w_king.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))],
            "wp": [Pawn, ImageTk.PhotoImage(
                Image.open(os.path.join(return_path, "w_pawn.png")).resize((IMAGE_WIDTH, IMAGE_HEIGHT)))]
        }

        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                piece_type = layout[row][col]
                if piece_type != " ":
                    if piece_type[0] == 'w':
                        colour = WHITE_PIECE
                    else:
                        colour = BLACK_PIECE
                    squares[row][col].current_piece = piece_types[piece_type][0](self.squares,
                                                                                 piece_type,
                                                                                 piece_types[piece_type][1],
                                                                                 colour, row, col)

    def draw(self):
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                self.squares[row][col].draw()
        self.set_next_turn()

    def handle_left_click(self, event):
        # TODO: Remove print statements
        #print("Mouse position: (%s %s)" % (event.x, event.y))
        row = int(event.y / ROW_HEIGHT)
        col = int(event.x / COL_WIDTH)
        #print("Row.col: (%s %s)" % (row, col))

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

    def is_valid_destination(self, row, col):
        # NOTE: We could just flag individual squares as valid destination, when we highlight/un-highlight
        for move in self.valid_moves:
            if move.row == row and move.col == col:
                return True
        return False

    def clear_current_moves(self):
        self.selected_square.highlight(False)
        for destination in self.valid_moves:
            self.squares[destination.row][destination.col].highlight(False)
        self.valid_moves = []

    def do_move(self, row, col):
        self.clear_current_moves()
        piece = self.selected_square.current_piece
        self.selected_square.set_current_piece(None)
        self.squares[row][col].set_current_piece(piece)
        self.selected_square = None
        if not self.check_game_state():
            self.set_next_turn()

    def remove_self_checking_moves(self, moving_square, moves):
        # Pick up the piece which will move
        moving_piece = moving_square.current_piece
        moving_square.current_piece = None

        checking_moves = []
        for move in moves:
            taken_piece = self.squares[move.row][move.col].current_piece
            self.squares[move.row][move.col].current_piece = moving_piece
            if self.is_checked(self.turn_colour):
                checking_moves.append(move)
            # Replace anything we temporarily took
            self.squares[move.row][move.col].current_piece = taken_piece

        # Put the moving piece back
        moving_square.current_piece = moving_piece

        # Remove any bad moves from valid_moves
        for bad_move in checking_moves:
            moves.remove(bad_move)
        
        return moves
    
    def check_game_state(self):
        # TODO: Check for check, mate, and draw/stalemate
        # return True if game finished
        return False

    def set_next_turn(self):
        last_turn_colour = self.turn_colour
        if self.turn_colour == WHITE_PIECE:
            self.turn_colour = BLACK_PIECE
        else:
            self.turn_colour = WHITE_PIECE

        if self.is_checkmated(self.turn_colour):
            # THE END! (no valid moves found)
            self.turn_colour = None
            message = 'CHECKMATE! GAME OVER! {0} WINS!'.format(last_turn_colour.upper())
        else:
            message = 'Next move: {0}'.format(self.turn_colour.upper())
        if self.status_label is None:
            self.status_label = Label(window, justify=CENTER, font=("Helvetica", 24))
        self.status_label.configure(text=message)
        self.status_label.pack()

    def is_checkmated(self, colour):
        if not self.is_checked(colour):
            return False
        for row in self.squares:
            for square in row:
                try:
                    if self.remove_self_checking_moves(square, square.valid_moves(colour)):
                        return False
                except AttributeError:
                    pass

        return True
    def is_checked(self, colour):
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
            king_type = "wk"
        else:
            king_type = "bk"
        for row in self.squares:
            for square in row:
                try:
                    # Expect an exception if there is no piece in the square
                    if square.current_piece.type == king_type:
                        return Move(square.row, square.col)
                except AttributeError:
                    pass
        return None

class Square():
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


class Piece():
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
        canvas.create_image(x, y, image=self.image, anchor="center")
        canvas.pack()


class Move():
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other_move):
        return self.row == other_move.row and self.col == other_move.col
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
        for col in range(self.col + 1, 8):
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
        for row in range(self.row + 1, 8):
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
        for row in range(self.row + 1, 8):
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

        # CHECK HORIZONTAL MOVES
        # Get right-up moves
        row = self.row
        for col in range(self.col + 1, 8):
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
        for row in range(self.row + 1, 8):
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
        for row in range(self.row + 1, 8):
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
chessboard = Chessboard(BOARD_WIDTH, BOARD_HEIGHT)
chessboard.draw()

window.mainloop()
