from abc import *


class Piece(object):
    """
    Apstraktna klasa za sahovske figure.
    """
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.side = side

    @abstractmethod
    def get_legal_moves(self):
        """
        Apstraktna metoda koja treba da za konkretnu figuru vrati moguce sledece poteze (pozicije).
        """
        pass

    def get_value(self):
        """
        Vrednost figure modifikovana u odnosu na igraca.
        Figure crnog (MAX igrac) imaju pozivitnu vrednost, a belog (MIN igrac) negativnu.
        :return: float
        """
        return self.get_value_() if self.side == 'b' else self.get_value_() * -1.

    @abstractmethod
    def get_value_(self):
        """
        Apstraktna metoda koja treba da vrati vrednost za konkretnu figuru.
        """
        pass


class Pawn(Piece):
    """
    Pijun
    """

    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        if side == 'w':  # beli pijun
            # jedan unapred, ako je polje prazno
            if row > 0 and self.board.data[row-1][col] == '.':
                d_rows.append(-1)
                d_cols.append(0)
            # dva unapred, ako je pocetna pozicija i ako je polje prazno
            if row == self.board.rows - 2 and self.board.data[row-1][col] == '.' and self.board.data[row-2][col] == '.':
                d_rows.append(-2)
                d_cols.append(0)
            # ukoso levo, jede crnog
            if col > 0 and row > 0 and self.board.data[row-1][col-1].startswith('b'):
                d_rows.append(-1)
                d_cols.append(-1)
            # ukoso desno, jede crnog
            if col < self.board.cols - 1 and row > 0 and self.board.data[row-1][col+1].startswith('b'):
                d_rows.append(-1)
                d_cols.append(1)
        else:  # crni pijun
            if row < self.board.rows - 1 and self.board.data[row + 1][col] == '.':
                d_rows.append(1)
                d_cols.append(0)
            # dva unapred, ako je pocetna pozicija i ako je polje prazno
            if row == 1 and self.board.data[row + 1][col] == '.' and self.board.data[row + 2][col] == '.':
                d_rows.append(2)
                d_cols.append(0)
            # ukoso levo, jede belog
            if col > 0 and row < self.board.rows - 1 and self.board.data[row + 1][col - 1].startswith('w'):
                d_rows.append(1)
                d_cols.append(-1)
            # ukoso desno, jede belog
            if col < self.board.cols - 1 and row < self.board.rows - 1 and self.board.data[row + 1][col + 1].startswith('w'):
                d_rows.append(1)
                d_cols.append(1)

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves

    def get_value_(self):
        return 1.  # pijun ima vrednost 1


class Knight(Piece):
    """
    Konj
    """
    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []
        # moze i da se stavi bez ovog pocetnog if-a i da se uvek ubacuje side kao boja umesto hard-
        # codovanog w i b
        if side == 'w':  # beli konj
            # gore desno
            if col > 0 and row > 1 and not self.board.data[row - 2][col - 1].startswith('w'):
                d_rows.append(-2)
                d_cols.append(-1)
            # gore levo
            if col < self.board.cols - 1 and row > 1 and not self.board.data[row - 2][col + 1].startswith('w'):
                d_rows.append(-2)
                d_cols.append(1)

            # desno gore
            if col < self.board.cols - 2 and row > 0 and not self.board.data[row - 1][col + 2].startswith('w'):
                d_rows.append(-1)
                d_cols.append(2)
            # levo gore
            if col > 1 and row > 0 and not self.board.data[row - 1][col - 2].startswith('w'):
                d_rows.append(-1)
                d_cols.append(-2)

            # desno dole
            if col < self.board.cols - 2 and row < self.board.rows - 1 and not self.board.data[row + 1][col + 2].startswith('w'):
                d_rows.append(1)
                d_cols.append(2)
            # levo dole
            if col > 1 and row < self.board.rows - 1 and not self.board.data[row + 1][col - 2].startswith('w'):
                d_rows.append(1)
                d_cols.append(-2)

            # dole desno
            if col > 0 and row < self.board.rows - 1 and not self.board.data[row + 2][col - 1].startswith('w'):
                d_rows.append(2)
                d_cols.append(-1)
            # dole levo
            if col < self.board.cols - 1 and row < self.board.rows - 1 and not self.board.data[row + 2][col + 1].startswith('w'):
                d_rows.append(2)
                d_cols.append(1)

        else:  # crni konj
            # gore desno
            if col > 0 and row > 1 and not self.board.data[row - 2][col - 1].startswith('b'):
                d_rows.append(-2)
                d_cols.append(-1)
            # gore levo
            if col < self.board.cols - 1 and row > 1 and not self.board.data[row - 2][col + 1].startswith('b'):
                d_rows.append(-2)
                d_cols.append(1)

            # desno gore
            if col < self.board.cols - 2 and row > 0 and not self.board.data[row - 1][col + 2].startswith('b'):
                d_rows.append(-1)
                d_cols.append(2)
            # levo gore
            if col > 1 and row > 0 and not self.board.data[row - 1][col - 2].startswith('b'):
                d_rows.append(-1)
                d_cols.append(-2)

            # desno dole
            if col < self.board.cols - 2 and row < self.board.rows - 1 and not self.board.data[row + 1][col + 2].startswith('b'):
                d_rows.append(1)
                d_cols.append(2)
            # levo dole
            if col > 1 and row < self.board.rows - 1 and not self.board.data[row + 1][col - 2].startswith('b'):
                d_rows.append(1)
                d_cols.append(-2)

            # dole desno
            if col > 0 and row < self.board.rows - 1 and not self.board.data[row + 2][col - 1].startswith('b'):
                d_rows.append(2)
                d_cols.append(-1)
            # dole levo
            if col < self.board.cols - 1 and row < self.board.rows - 1 and not self.board.data[row + 2][col + 1].startswith('b'):
                d_rows.append(2)
                d_cols.append(1)
        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves

    def get_value_(self):
        return 3  # neka vrednost za konja


class Bishop(Piece):
    """
    Lovac
    """
    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        fails = [0, 0, 0, 0]
        for current in range(1, 8):

            # gore desno
            if col + current < self.board.cols and row - current >= 0:
                if self.board.data[row - current][col + current].startswith('.') and fails[0] == 0:
                    d_rows.append(-current)
                    d_cols.append(current)
                elif not self.board.data[row - current][col + current].startswith(side) and fails[0] == 0:
                    d_rows.append(-current)
                    d_cols.append(current)
                    fails[0] = 1
                else:
                    fails[0] = 1
            # dole levo
            if col - current >= 0 and row + current < self.board.rows:
                if self.board.data[row + current][col - current].startswith('.') and fails[1] == 0:
                    d_rows.append(current)
                    d_cols.append(-current)
                elif not self.board.data[row + current][col - current].startswith(side) and fails[1] == 0:
                    d_rows.append(current)
                    d_cols.append(-current)
                    fails[1] = 1
                else:
                    fails[1] = 1
            # gore levo
            if col - current >= 0 and row - current >= 0:
                if self.board.data[row - current][col - current].startswith('.') and fails[2] == 0:
                    d_rows.append(-current)
                    d_cols.append(-current)
                elif not self.board.data[row - current][col - current].startswith(side) and fails[2] == 0:
                    d_rows.append(-current)
                    d_cols.append(-current)
                    fails[2] = 1
                else:
                    fails[2] = 1
            # dole desno
            if col + current < self.board.cols and row + current < self.board.rows:
                if self.board.data[row + current][col + current].startswith('.') and fails[3] == 0:
                    d_rows.append(current)
                    d_cols.append(current)
                elif not self.board.data[row + current][col + current].startswith(side) and fails[3] == 0:
                    d_rows.append(current)
                    d_cols.append(current)
                    fails[3] = 1
                else:
                    fails[3] = 1
        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves

    def get_value_(self):
        return 3 # lovac ce imati istu vrednost kao konj


class Rook(Piece):
    """
    Top
    """
    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        fails = [0, 0, 0, 0]
        for current in range(1, 8):

            # gore
            if row - current >= 0:
                if self.board.data[row - current][col].startswith('.') and fails[0] == 0:
                    d_rows.append(-current)
                    d_cols.append(0)
                elif not self.board.data[row - current][col].startswith(side) and fails[0] == 0:
                    d_rows.append(-current)
                    d_cols.append(0)
                    fails[0] = 1
                else:
                    fails[0] = 1
            # dole
            if row + current < self.board.rows:
                if self.board.data[row + current][col].startswith('.') and fails[1] == 0:
                    d_rows.append(current)
                    d_cols.append(0)
                elif not self.board.data[row + current][col].startswith(side) and fails[1] == 0:
                    d_rows.append(current)
                    d_cols.append(0)
                    fails[1] = 1
                else:
                    fails[1] = 1
            #  levo
            if col - current >= 0:
                if self.board.data[row][col - current].startswith('.') and fails[2] == 0:
                    d_rows.append(0)
                    d_cols.append(-current)
                elif not self.board.data[row][col - current].startswith(side) and fails[2] == 0:
                    d_rows.append(0)
                    d_cols.append(-current)
                    fails[2] = 1
                else:
                    fails[2] = 1
            # desno
            if col + current < self.board.cols:
                if self.board.data[row][col + current].startswith('.') and fails[3] == 0:
                    d_rows.append(0)
                    d_cols.append(current)
                elif not self.board.data[row][col + current].startswith(side) and fails[3] == 0:
                    d_rows.append(0)
                    d_cols.append(current)
                    fails[3] = 1
                else:
                    fails[3] = 1

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves

    def get_value_(self):
        # TODO
        return 5 # top vrednost 5


class Queen(Piece):
    """
    Kraljica
    """
    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        fails = [0, 0, 0, 0]
        fails_b = [0, 0, 0, 0]
        for current in range(1, 8):

            # gore
            if row - current >= 0:
                if self.board.data[row - current][col].startswith('.') and fails[0] == 0:
                    d_rows.append(-current)
                    d_cols.append(0)
                elif not self.board.data[row - current][col].startswith(side) and fails[0] == 0:
                    d_rows.append(-current)
                    d_cols.append(0)
                    fails[0] = 1
                else:
                    fails[0] = 1
            # dole
            if row + current < self.board.rows:
                if self.board.data[row + current][col].startswith('.') and fails[1] == 0:
                    d_rows.append(current)
                    d_cols.append(0)
                elif not self.board.data[row + current][col].startswith(side) and fails[1] == 0:
                    d_rows.append(current)
                    d_cols.append(0)
                    fails[1] = 1
                else:
                    fails[1] = 1
            #  levo
            if col - current >= 0:
                if self.board.data[row][col - current].startswith('.') and fails[2] == 0:
                    d_rows.append(0)
                    d_cols.append(-current)
                elif not self.board.data[row][col - current].startswith(side) and fails[2] == 0:
                    d_rows.append(0)
                    d_cols.append(-current)
                    fails[2] = 1
                else:
                    fails[2] = 1
            # desno
            if col + current < self.board.cols:
                if self.board.data[row][col + current].startswith('.') and fails[3] == 0:
                    d_rows.append(0)
                    d_cols.append(current)
                elif not self.board.data[row][col + current].startswith(side) and fails[3] == 0:
                    d_rows.append(0)
                    d_cols.append(current)
                    fails[3] = 1
                else:
                    fails[3] = 1
                    # gore desno
            if col + current < self.board.cols and row - current >= 0:
                if self.board.data[row - current][col + current].startswith('.') and fails_b[0] == 0:
                    d_rows.append(-current)
                    d_cols.append(current)
                elif not self.board.data[row - current][col + current].startswith(side) and fails_b[0] == 0:
                    d_rows.append(-current)
                    d_cols.append(current)
                    fails_b[0] = 1
                else:
                    fails_b[0] = 1
            # dole levo
            if col - current >= 0 and row + current < self.board.rows:
                if self.board.data[row + current][col - current].startswith('.') and fails_b[1] == 0:
                    d_rows.append(current)
                    d_cols.append(-current)
                elif not self.board.data[row + current][col - current].startswith(side) and fails_b[1] == 0:
                    d_rows.append(current)
                    d_cols.append(-current)
                    fails_b[1] = 1
                else:
                    fails_b[1] = 1
            # gore levo
            if col - current >= 0 and row - current >= 0:
                if self.board.data[row - current][col - current].startswith('.') and fails_b[2] == 0:
                    d_rows.append(-current)
                    d_cols.append(-current)
                elif not self.board.data[row - current][col - current].startswith(side) and fails_b[2] == 0:
                    d_rows.append(-current)
                    d_cols.append(-current)
                    fails_b[2] = 1
                else:
                    fails_b[2] = 1
            # dole desno
            if col + current < self.board.cols and row + current < self.board.rows:
                if self.board.data[row + current][col + current].startswith('.') and fails_b[3] == 0:
                    d_rows.append(current)
                    d_cols.append(current)
                elif not self.board.data[row + current][col + current].startswith(side) and fails_b[3] == 0:
                    d_rows.append(current)
                    d_cols.append(current)
                    fails_b[3] = 1
                else:
                    fails_b[3] = 1
        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves

    def get_value_(self):
        return 10 # kraljica vrednost 10


class King(Piece):
    """
    Kralj
    """

    def get_legal_moves(self):
        row = self.row
        col = self.col
        side = self.side
        legal_moves = []
        d_rows = []
        d_cols = []

        fails = [0, 0, 0, 0]
        fails_b = [0, 0, 0, 0]
        for current in range(1, 2):

            # gore
            if row - current >= 0:
                if self.board.data[row - current][col].startswith('.') and fails[0] == 0:
                    d_rows.append(-1)
                    d_cols.append(0)
                elif not self.board.data[row - current][col].startswith(side) and fails[0] == 0:
                    d_rows.append(-1)
                    d_cols.append(0)
                    fails[0] = 1
                else:
                    fails[0] = 1
            # dole
            if row + current < self.board.rows:
                if self.board.data[row + current][col].startswith('.') and fails[1] == 0:
                    d_rows.append(1)
                    d_cols.append(0)
                elif not self.board.data[row + current][col].startswith(side) and fails[1] == 0:
                    d_rows.append(1)
                    d_cols.append(0)
                    fails[1] = 1
                else:
                    fails[1] = 1
            #  levo
            if col - current >= 0:
                if self.board.data[row][col - current].startswith('.') and fails[2] == 0:
                    d_rows.append(0)
                    d_cols.append(-1)
                elif not self.board.data[row][col - current].startswith(side) and fails[2] == 0:
                    d_rows.append(0)
                    d_cols.append(-1)
                    fails[2] = 1
                else:
                    fails[2] = 1
            # desno
            if col + current < self.board.cols:
                if self.board.data[row][col + current].startswith('.') and fails[3] == 0:
                    d_rows.append(0)
                    d_cols.append(1)
                elif not self.board.data[row][col + current].startswith(side) and fails[3] == 0:
                    d_rows.append(0)
                    d_cols.append(1)
                    fails[3] = 1
                else:
                    fails[3] = 1
                    # gore desno
            if col + current < self.board.cols and row - current >= 0:
                if self.board.data[row - current][col + current].startswith('.') and fails_b[0] == 0:
                    d_rows.append(-1)
                    d_cols.append(1)
                elif not self.board.data[row - current][col + current].startswith(side) and fails_b[0] == 0:
                    d_rows.append(-1)
                    d_cols.append(1)
                    fails_b[0] = 1
                else:
                    fails_b[0] = 1
            # dole levo
            if col - current >= 0 and row + current < self.board.rows:
                if self.board.data[row + current][col - current].startswith('.') and fails_b[1] == 0:
                    d_rows.append(1)
                    d_cols.append(-1)
                elif not self.board.data[row + current][col - current].startswith(side) and fails_b[1] == 0:
                    d_rows.append(1)
                    d_cols.append(-1)
                    fails_b[1] = 1
                else:
                    fails_b[1] = 1
            # gore levo
            if col - current >= 0 and row - current >= 0:
                if self.board.data[row - current][col - current].startswith('.') and fails_b[2] == 0:
                    d_rows.append(-1)
                    d_cols.append(-1)
                elif not self.board.data[row - current][col - current].startswith(side) and fails_b[2] == 0:
                    d_rows.append(-1)
                    d_cols.append(-1)
                    fails_b[2] = 1
                else:
                    fails_b[2] = 1
            # dole desno
            if col + current < self.board.cols and row + current < self.board.rows:
                if self.board.data[row + current][col + current].startswith('.') and fails_b[3] == 0:
                    d_rows.append(1)
                    d_cols.append(1)
                elif not self.board.data[row + current][col + current].startswith(side) and fails_b[3] == 0:
                    d_rows.append(1)
                    d_cols.append(1)
                    fails_b[3] = 1
                else:
                    fails_b[3] = 1
        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves

    def get_value_(self):

        return 1000
