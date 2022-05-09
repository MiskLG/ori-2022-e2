from abc import *
import numpy as np


class State(object):
    """
    Apstraktna klasa koja opisuje stanje pretrage.
    """

    @abstractmethod
    def __init__(self, board, parent=None, position=None, goal_position=None):
        """
        :param board: Board (tabla)
        :param parent: roditeljsko stanje
        :param position: pozicija stanja
        :param goal_position: pozicija krajnjeg stanja
        :return:
        """
        self.board = board
        self.parent = parent  # roditeljsko stanje
        self.eaten_boxes = []
        self.yellow_boxes = 0
        self.blue_boxes = 0
        self.all_boxes = []
        self.all_boxes_checked = []
        if self.parent is None:  # ako nema roditeljsko stanje, onda je ovo inicijalno stanje
            self.position = board.find_position(self.get_agent_code())  # pronadji pocetnu poziciju
            self.goal_position = board.find_position(self.get_agent_goal_code())  # pronadji krajnju poziciju
            self.all_boxes, self.all_boxes_checked = self.find_all_boxes(['b', 'y'])
        else:  # ako ima roditeljsko stanje, samo sacuvaj vrednosti parametara
            self.position = position
            self.goal_position = goal_position
            self.yellow_boxes = parent.yellow_boxes
            self.blue_boxes = parent.blue_boxes
            self.eaten_boxes = parent.eaten_boxes.copy()
            self.all_boxes = parent.all_boxes.copy()
            self.all_boxes_checked = parent.all_boxes_checked.copy()
        self.depth = parent.depth + 1 if parent is not None else 1  # povecaj dubinu/nivo pretrage

    def get_next_states(self):
        new_positions = self.get_legal_positions()  # dobavi moguce (legalne) sledece pozicije iz trenutne pozicije
        next_states = []
        # napravi listu mogucih sledecih stanja na osnovu mogucih sledecih pozicija
        for new_position in new_positions:
            next_state = self.__class__(self.board, self, new_position, self.goal_position)
            next_states.append(next_state)
        return next_states

    @abstractmethod
    def get_agent_code(self):
        """
        Apstraktna metoda koja treba da vrati kod agenta na tabli.
        :return: str
        """
        pass

    @abstractmethod
    def get_agent_goal_code(self):
        """
        Apstraktna metoda koja treba da vrati kod agentovog cilja na tabli.
        :return: str
        """
        pass

    @abstractmethod
    def get_legal_positions(self):
        """
        Apstraktna metoda koja treba da vrati moguce (legalne) sledece pozicije na osnovu trenutne pozicije.
        :return: list
        """
        pass

    @abstractmethod
    def is_final_state(self):
        """
        Apstraktna metoda koja treba da vrati da li je treuntno stanje zapravo zavrsno stanje.
        :return: bool
        """
        pass

    @abstractmethod
    def unique_hash(self):
        """
        Apstraktna metoda koja treba da vrati string koji je JEDINSTVEN za ovo stanje
        (u odnosu na ostala stanja).
        :return: str
        """
        pass
    
    @abstractmethod
    def get_cost(self):
        """
        Apstraktna metoda koja treba da vrati procenu cene
        (vrednost heuristicke funkcije) za ovo stanje.
        Koristi se za vodjene pretrage.
        :return: float
        """
        pass
    
    @abstractmethod
    def get_current_cost(self):
        """
        Apstraktna metoda koja treba da vrati stvarnu trenutnu cenu za ovo stanje.
        Koristi se za vodjene pretrage.
        :return: float
        """
        pass


class RobotState(State):
    def __init__(self, board, parent=None, position=None, goal_position=None):
        super(self.__class__, self).__init__(board, parent, position, goal_position)
        row, col = self.position

        if not self.game_finished():
            if self.board.data[row][col] == 'b':
                if self.blue_boxes < 3:
                    leave = False
                    for box in self.eaten_boxes:
                        box_row, box_col = box
                        if box_row == row and box_col == col:
                            leave = True
                    if not leave:
                        index = self.all_boxes.index([row, col])
                        self.all_boxes_checked[index] = 1
                        self.blue_boxes += 1
                        self.eaten_boxes.append([row, col])
            if self.board.data[row][col] == 'y':
                if self.yellow_boxes < 2:
                    leave = False
                    for box in self.eaten_boxes:
                        box_row, box_col = box
                        if box_row == row and box_col == col:
                            leave = True
                    if not leave:
                        index = self.all_boxes.index([row, col])
                        self.all_boxes_checked[index] = 1
                        self.yellow_boxes += 1
                        self.eaten_boxes.append([row, col])

    def get_agent_code(self):
        return 'r'

    def get_agent_goal_code(self):
        return 'g'

    def get_legal_positions(self):
        # d_rows (delta rows), d_cols (delta columns)
        # moguci smerovi kretanja robota (desno, levo, dole, gore)

        if not self.game_finished():
            data = self.get_legal_moves_vertical(self.board, self.position, ['.', 'y', 'b', 'g'], [], 1,
                                                 self.board.cols,
                                                 [True, True, True, True])
            data2 = self.get_legal_moves_diagonal(self.board, self.position, ['.', 'y', 'b', 'g'], [], 1,
                                                  self.board.cols,
                                                  [True, True, True, True])
            new_positions = data
            new_positions.extend(data2)
        else:
            data2 = self.get_legal_moves_diagonal(self.board, self.position, ['.', 'y', 'b', 'g'], [], 1,
                                                  2,
                                                  [True, True, True, True])
            new_positions = data2



        return new_positions

    def is_final_state(self):
        return self.position == self.goal_position and self.blue_boxes == 3 and self.yellow_boxes == 2

    def unique_hash(self):
        return str(self.position) + str(self.all_boxes_checked)

    def get_cost(self):
        return ((self.position[0] - self.goal_position[0]) ** 2 + (
                    self.position[1] - self.goal_position[1]) ** 2) ** 0.5

    def get_current_cost(self):
        value = 10


        if self.game_finished():
            return self.depth - 0.1*value
        return self.depth + 0.1*value

    def game_finished(self):
        if self.blue_boxes >= 3 and self.yellow_boxes >= 2:
            return True
        return False

    def find_all_boxes(self, boxes):
        """
            boxes parameter takes all points of interest as an array. Ex. ['bb', 'ob']
        """
        all_boxes = []
        checked_boxes = []

        for rows in range(0,self.board.rows):
            for cols in range(0,self.board.cols):
                tile = self.board.data[rows][cols]
                if tile in boxes:
                    all_boxes.append([rows,cols])
                    checked_boxes.append(0)

        return all_boxes, checked_boxes

    def get_legal_moves_vertical(self, board, current_position, good_characters, ending_characters, start, finish, sides):
        """
            COPY THIS TO STATE.PY OR ANYWHERE YOU NEED IT
            Board - board.py object - uses method data
            Current position, tuple - (row, col)
            Takes array of good characters - '.', 'bb' for example also add end here
            Takes array of ending characters - ex. list of black pieces when player is white (can move to them but not past them)
            First number of moves available - first , rook example 1
            Last number of moves available - end , rook example 8 (if board is size of 8) last number is not included
            Array of sides to go to - [False,False,True,Ture] will cover right and bottom [Left,Top,Right,Bottom]
        """
        row, col = current_position
        legal_moves = []
        d_rows = []
        d_cols = []

        fails = [0, 0, 0, 0]
        for current in range(start, finish):

            if sides[1]:
                if row - current >= 0:
                    if board.data[row - current][col] in good_characters and fails[0] == 0:
                        d_rows.append(-current)
                        d_cols.append(0)
                    elif board.data[row - current][col] in ending_characters and fails[0] == 0:
                        d_rows.append(-current)
                        d_cols.append(0)
                        fails[0] = 1
                    else:
                        fails[0] = 1
            # dole
            if sides[3]:
                if row + current < board.rows:
                    if board.data[row + current][col] in good_characters and fails[1] == 0:
                        d_rows.append(current)
                        d_cols.append(0)
                    elif board.data[row + current][col] in ending_characters and fails[1] == 0:
                        d_rows.append(current)
                        d_cols.append(0)
                        fails[1] = 1
                    else:
                        fails[1] = 1
            #  levo
            if sides[0]:
                if col - current >= 0:
                    if board.data[row][col - current] in good_characters and fails[2] == 0:
                        d_rows.append(0)
                        d_cols.append(-current)
                    elif self.board.data[row][col - current] in ending_characters and fails[2] == 0:
                        d_rows.append(0)
                        d_cols.append(-current)
                        fails[2] = 1
                    else:
                        fails[2] = 1
            # desno
            if sides[2]:
                if col + current < board.cols:
                    if board.data[row][col + current] in good_characters and fails[3] == 0:
                        d_rows.append(0)
                        d_cols.append(current)
                    elif board.data[row][col + current] in ending_characters and fails[3] == 0:
                        d_rows.append(0)
                        d_cols.append(current)
                        fails[3] = 1
                    else:
                        fails[3] = 1

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < board.rows and 0 <= new_col < board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves


    def get_legal_moves_diagonal(self, board, current_position, good_characters, ending_characters, start, finish, sides):
        """
            COPY THIS TO STATE.PY OR ANYWHERE YOU NEED IT
            Board - board.py object - uses method data
            Current position, tuple - (row, col)
            Takes array of good characters - '.', 'bb' for example and goal here too
            Takes array of ending characters - ex. list of black pieces when player is white (can move to them but not past them)
            First number of moves available - first , bishop example 1
            Last number of moves available - end , bishop example 8 (if board is size of 8) last number is not included
            Array of sides to go to - [False,False,True,Ture] will cover top right and bottom right [TopLeft,TopRight,BottomRight,BottomLeft]
        """
        row, col = current_position
        legal_moves = []
        d_rows = []
        d_cols = []

        fails = [0, 0, 0, 0]
        for current in range(start, finish):

            # gore desno
            if sides[1]:
                if col + current < board.cols and row - current >= 0:
                    if board.data[row - current][col + current] in good_characters and fails[0] == 0:
                        d_rows.append(-current)
                        d_cols.append(current)
                    elif board.data[row - current][col + current] in ending_characters and fails[0] == 0:
                        d_rows.append(-current)
                        d_cols.append(current)
                        fails[0] = 1
                    else:
                        fails[0] = 1
            # dole levo
            if sides[3]:
                if col - current >= 0 and row + current < board.rows:
                    if board.data[row + current][col - current] in good_characters and fails[1] == 0:
                        d_rows.append(current)
                        d_cols.append(-current)
                    elif board.data[row + current][col - current] in ending_characters and fails[1] == 0:
                        d_rows.append(current)
                        d_cols.append(-current)
                        fails[1] = 1
                    else:
                        fails[1] = 1
            #  gore levo
            if sides[0]:
                if col - current >= 0 and row - current >= 0:
                    if board.data[row - current][col - current] in good_characters and fails[2] == 0:
                        d_rows.append(-current)
                        d_cols.append(-current)
                    elif board.data[row - current][col - current] in ending_characters and fails[2] == 0:
                        d_rows.append(-current)
                        d_cols.append(-current)
                        fails[2] = 1
                    else:
                        fails[2] = 1
            # dole desno
            if sides[2]:
                if col + current < board.cols and row + current < board.rows:
                    if board.data[row + current][col + current] in good_characters and fails[3] == 0:
                        d_rows.append(current)
                        d_cols.append(current)
                    elif board.data[row + current][col + current] in ending_characters and fails[3] == 0:
                        d_rows.append(current)
                        d_cols.append(current)
                        fails[3] = 1
                    else:
                        fails[3] = 1

        for d_row, d_col in zip(d_rows, d_cols):
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row < board.rows and 0 <= new_col < board.cols:
                legal_moves.append((new_row, new_col))

        return legal_moves


