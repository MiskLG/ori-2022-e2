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

