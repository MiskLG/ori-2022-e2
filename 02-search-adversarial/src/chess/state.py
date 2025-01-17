import copy
import random


class State(object):
    """
    Klasa koja opisuje stanje table.
    """

    def __init__(self, board, history_moves, parent=None):
        """
        :param board: Board (tabla)
        :param parent: roditeljsko stanje
        :return:
        """
        self.history_moves = history_moves
        self.pos = None
        self.board = board  # sahovska tabla koja opisuje trenutno stanje
        self.parent = parent  # roditeljsko stanje
        if parent is not None:
            if parent.pos is not None:
                self.history_moves.append(parent.pos)
        self.value = 0.  # "vrednost" stanja - racuna ga evaluaciona funkcija calculate_value()

    def generate_next_states(self, max_player):
        """
        Generise moguca sledeca stanja (table) na osnovu svih mogucih poteza (u zavisnosti koji je igrac na potezu).
        :param max_player: bool. Da li je MAX igrac (crni)?
        :return: list. Lista mogucih sledecih stanja.
        """
        next_states = []
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                piece = self.board.determine_piece(row, col)  # odredi koja je figura
                if piece is None:
                    continue
                # generisi za crne ako je max igrac na potezu, generisi za bele ako je min igrac na potezu
                if (max_player and piece.side == 'b') or (not max_player and piece.side == 'w'):
                    legal_moves = piece.get_legal_moves(self.history_moves)  # svi moguci potezi za figuru
                    for legal_move in legal_moves:
                        new_board = copy.deepcopy(self.board)
                        self.pos = new_board.move_piece(row, col, legal_move[0], legal_move[1])
                        next_state = State(new_board, copy.deepcopy(self.history_moves), self)
                        next_states.append(next_state)
        random.shuffle(next_states)
        return next_states

    def calculate_value(self):
        """
        Evaluaciona funkcija za stanje.
        :return:
        """
        for row in range(0, self.board.rows):
            for col in range(0, self.board.cols):
                piece = self.board.determine_piece(row, col)
                if piece is not None:
                    self.value += piece.get_value_()
        return self.value

    def calculate_value_based_on_color(self, black):
        for row in range(0, self.board.rows):
            for col in range(0, self.board.cols):
                piece = self.board.determine_piece(row, col)
                if piece is not None:
                    if black:
                        if piece.side == 'w':
                            self.value += piece.get_value_()
                    else:
                        if piece.side == 'b':
                            self.value += piece.get_value_()
        return self.value

    def is_final_state(self):
        white_lost = True
        black_lost = True
        for row in range(0, self.board.rows):
            for col in range(0, self.board.cols):
                piece = self.board.determine_piece(row, col)
                if piece is not None:
                    if piece.side == 'w' and piece.get_value_() == 1000:
                        white_lost = False
                    if piece.side == 'b' and piece.get_value_() == 1000:
                        black_lost = False

        return white_lost + black_lost
