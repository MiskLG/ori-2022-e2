from pieces import *

class Board:
    """
    Klasa koja implementira strukturu table.
    """

    def __init__(self, rows=20, cols=20):
        self.rows = rows  # broj redova
        self.cols = cols  # broj kolona
        self.elems = ['.',   # prazno polje
                      'bp',  # crni pijun
                      'br',  # crni top
                      'bn',  # crni konj
                      'bb',  # crni lovac
                      'bk',  # crni kralj
                      'bq',  # crna kraljica
                      'wp',  # beli pijun
                      'wr',  # beli top
                      'wn',  # beli konj
                      'wb',  # beli lovac
                      'wk',  # beli kralj
                      'wq']  # beli kraljica

        self.data = [['.'] * cols for _ in range(rows)]

    def load_from_file(self, file_path):
        """
        Ucitavanje table iz fajla.
        :param file_path: putanja fajla.
        """
        board_f = open(file_path, 'r')
        row = board_f.readline().strip('\n')
        self.data = []
        while row != '':
            self.data.append(list(row.split()))
            row = board_f.readline().strip('\n')
        board_f.close()

    def save_to_file(self, file_path):
        """
        Snimanje table u fajl.
        :param file_path: putanja fajla.
        """
        if file_path:
            f = open(file_path, 'w')
            for row in range(self.rows):
                f.write(''.join(self.data[row]) + '\n')
            f.close()

    def move_piece(self, from_row, from_col, to_row, to_col):
        """
        Pomeranje figure.
        :param from_row: prethodni red figure.
        :param from_col: prethodna kolona figure.
        :param to_row: novi red figure.
        :param to_col: nova kolona figure.
        """
        # checking if its en-pasant from white
        if from_row == 3 and to_row == 2:
            if self.data[to_row][to_col] == '.':
                if self.data[from_row][from_col][1] == 'p':
                    t = self.data[from_row][from_col]
                    self.data[from_row][from_col] = '.'
                    self.data[to_row][to_col] = t
                    self.data[to_row+1][to_col] = '.'
                    return t, from_row, from_col, to_row, to_col, 1

        if from_row == 4 and to_row == 5:
            if self.data[to_row][to_col] == '.':
                if self.data[from_row][from_col][1] == 'p':
                    t = self.data[from_row][from_col]
                    self.data[from_row][from_col] = '.'
                    self.data[to_row][to_col] = t
                    self.data[to_row-1][to_col] = '.'
                    return t, from_row, from_col, to_row, to_col, 2

        # checking if castle was made from white
        if (from_row == 7 or from_row == 0) and (to_row == 7 or to_row == 0) and from_col == 4:
            if self.data[from_row][from_col][1] == 'k':
                color = self.data[from_row][from_col][0]
                # to the left
                if to_col == 2:
                    t = self.data[from_row][from_col]
                    self.data[from_row][from_col] = '.'
                    self.data[to_row][to_col] = t
                    self.data[from_row][0] = '.'
                    self.data[from_row][3] = color + 'r'
                    return t, from_row, from_col, to_row, to_col, 3
                elif to_col == 6:
                    t = self.data[from_row][from_col]
                    self.data[from_row][from_col] = '.'
                    self.data[to_row][to_col] = t
                    self.data[from_row][7] = '.'
                    self.data[from_row][5] = color + 'r'
                    return t, from_row, from_col, to_row, to_col, 4

        if to_row < len(self.data) and to_col < len(self.data[0]):
            t = self.data[from_row][from_col]
            self.data[from_row][from_col] = '.'
            self.data[to_row][to_col] = t
            return t, from_row, from_col, to_row, to_col, -1

    def clear(self):
        """
        Ciscenje sadrzaja cele table.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                self.data[row][col] = '.'

    def find_position(self, element):
        """
        Pronalazenje specificnog elementa unutar table.
        :param element: kod elementa.
        :returns: tuple(int, int)
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == element:
                    return row, col
        return None, None

    def determine_piece(self, row, col):
        """
        Odredjivanje koja je figura na odredjenoj poziciji na tabli.
        :param row: red.
        :param col: kolona.
        :return: objekat figure (implementacija klase Piece).
        """
        elem = self.data[row][col]
        if elem != '.':
            side = elem[0]  # da li je crni (b) ili beli (w)
            piece = elem[1]  # kod figure
            if piece == 'p':
                return Pawn(self, row, col, side)
            if piece == 'n':
                return Knight(self, row, col, side)
            if piece == 'k':
                return King(self, row, col, side)
            if piece == 'r':
                return Rook(self, row, col, side)
            if piece == 'b':
                return Bishop(self, row, col, side)
            if piece == 'q':
                return Queen(self, row, col, side)
