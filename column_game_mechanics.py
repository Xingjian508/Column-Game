class ColumnState:
    def __init__(self):
        self._board = []
        self._faller = Faller()
        self._backup_faller = Faller()
        self._landed = False

    def empty_setup(self, num_rows: int, num_cols: int) -> None:
        each_col = []
        for j in range(num_rows):
            each_col.append(' ')
        for i in range(num_cols):
            self._board.append(list(each_col))

    def get_board(self) -> list:
        output_board = []
        for col in self._board:
            output_board.append(list(col))
        return output_board

    def load_initial_content(self, given_board: list) -> None:
        # Gives the board its initial, given content.
        for i in range(len(given_board)):
            for j in range(len(given_board[0])):
                self._board[i][j] = given_board[i][j]

    def adjust_fall(self) -> None:
        num_cols = len(self._board)
        col_index = len(self._board[0])
        for i in range(num_cols):
            for j in range(col_index):
                if self._board[i][col_index-j-1] == ' ':
                    k = col_index-j-1
                    while k >= 0:
                        if self._board[i][k] != ' ':
                            self._board[i][col_index-j-1] = self._board[i][k]
                            self._board[i][k] = ' '
                            break
                        k -= 1

    def initialize_faller(self, col: int, jewels: tuple) -> None:
        self._faller.setup(col, jewels)
        self._paint_faller()
        if self._predict_another_fall():
            self._landed = False
        else:
            # Faller has simply landed.
            self._landed = True

    def faller_fall(self) -> bool:
        col = self._faller.get_col()
        lowest_pos = self._faller.get_lowest_pos()
        if col != None and lowest_pos != None:
            if lowest_pos+1 < len(self._board[0]) and self._board[col][lowest_pos+1] == ' ':
                self._erase_faller()
                self._faller.fall()
                self._paint_faller()
                if self._predict_another_fall():
                    self._landed = False
                else:
                    # Faller has simply landed.
                    self._landed = True
            else:
                # Check if game ends because not all faller elements are displayed.
                if lowest_pos-2 < 0:
                    return False
                else:
                    # Faller has simply landed.
                    self._faller = Faller()
                    self._landed = False
        return True

    def faller_move_left(self):
        col = self._faller.get_col()
        lowest_pos = self._faller.get_lowest_pos()
        if col != None and lowest_pos != None and col-1 >= 0 and self._board[col-1][lowest_pos] == ' ':
            self._erase_faller()
            self._faller.move_left()
            self._paint_faller()
            if self._predict_another_fall():
                self._landed = False
            else:
                # Faller has simply landed.
                self._landed = True

    def faller_move_right(self):
        col = self._faller.get_col()
        lowest_pos = self._faller.get_lowest_pos()
        if col != None and lowest_pos != None and col+1 < len(self._board) and self._board[col+1][lowest_pos] == ' ':
            self._erase_faller()
            self._faller.move_right()
            self._paint_faller()
            if self._predict_another_fall():
                self._landed = False
            else:
                # Faller has simply landed.
                self._landed = True

    def faller_rotate(self):
        self._erase_faller()
        self._faller.rotate()
        self._paint_faller()

    def check_and_mark_matchings(self) -> bool:
        different = False
        board = self._board
        sub_board = []
        for col in board:
            sub_board.append(list(col))
        # Check vertically.
        for i in range(len(board)):
            for j in range(len(board[i])-2):
                if board[i][j] != ' ' and board[i][j] == board[i][j+1] and board[i][j] == board[i][j+2]:
                    sub_board[i][j] = '*' + sub_board[i][j]
                    sub_board[i][j+1] = '*' + sub_board[i][j]
                    sub_board[i][j+2] = '*' + sub_board[i][j]
        # Check horizontally.
        for j in range(len(board[i])):
            for i in range(len(board)-2):
                if board[i][j] != ' ' and board[i][j] == board[i+1][j] and board[i][j] == board[i+2][j]:
                    sub_board[i][j] = '*' + sub_board[i][j]
                    sub_board[i+1][j] = '*' + sub_board[i][j]
                    sub_board[i+2][j] = '*' + sub_board[i][j]
        # Check diagonally, top left to bottom right.
        for i in range(len(board)-2):
            for j in range(len(board[i])-2):
                if board[i][j] != ' ' and board[i][j] == board[i+1][j+1] and board[i][j] == board[i+2][j+2]:
                    sub_board[i][j] = '*' + sub_board[i][j]
                    sub_board[i+1][j+1] = '*' + sub_board[i][j]
                    sub_board[i+2][j+2] = '*' + sub_board[i][j]
        # Check diagonally, top right to bottom left.
        for i in range(len(board)-2):
            for j in range(len(board[i])-2):
                if board[len(board)-i-1][j] != ' ' and board[len(board)-i-1][j] == board[len(board)-i-2][j+1] and board[len(board)-i-1][j] == board[len(board)-i-3][j+2]:
                    sub_board[len(board)-i-1][j] = '*' + sub_board[len(board)-i-1][j]
                    sub_board[len(board)-i-2][j+1] = '*' + sub_board[len(board)-i-1][j]
                    sub_board[len(board)-i-3][j+2] = '*' + sub_board[len(board)-i-1][j]
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != sub_board[i][j]:
                    different = True
                board[i][j] = sub_board[i][j]
        return different

    def check_and_erase_matchings(self):
        board = self._board
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j][0] == '*':
                    board[i][j] = ' '

    def get_faller(self):
        return self._faller

    def get_backup_faller(self):
        return self._backup_faller

    def get_landed(self):
        if self._landed:
            return True
        return False

    def _erase_faller(self):
        # Erases the faller.
        col = self._faller.get_col()
        lowest_pos = self._faller.get_lowest_pos()
        if col != None and lowest_pos != None:
            for i in range(3):
                self._board[col][lowest_pos] = ' '
                lowest_pos -= 1
                if lowest_pos < 0:
                    break

    def _paint_faller(self):
        col = self._faller.get_col()
        lowest_pos = self._faller.get_lowest_pos()
        if col != None and lowest_pos != None:
            for i in range(3):
                self._board[col][lowest_pos] = self._faller.get_jewel(3-i-1)
                lowest_pos -= 1
                if lowest_pos < 0:
                    break

    def _predict_another_fall(self) -> bool:
        col = self._faller.get_col()
        lowest_pos = self._faller.get_lowest_pos()
        if col != None and lowest_pos != None:
            if lowest_pos+1 < len(self._board[0]) and self._board[col][lowest_pos+1] == ' ':
                return True
            else:
                return False
        return False

class Faller:
    def __init__(self):
        self._col = None
        self._lowest_pos = None
        self._jewels = None

    def setup(self, col, jewels: tuple):
        self._col = col
        self._lowest_pos = 0
        self._jewels = jewels

    def fall(self):
        self._lowest_pos += 1

    def move_left(self):
        self._col -= 1

    def move_right(self):
        self._col += 1

    def rotate(self):
        self._jewels = (self._jewels[2], self._jewels[0], self._jewels[1])

    def get_col(self):
        return self._col

    def get_lowest_pos(self):
        return self._lowest_pos

    def get_jewel(self, pos: int):
        return self._jewels[pos]
