'''
Reference from https://wasimlorgat.com/posts/editor.html#scroll-the-window-to-the-cursor
'''
class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        return self.lines[index]

    @property
    def bottom(self):
        return len(self) - 1

class Window:

    def __init__(self, win, n_rows, n_cols, row=0, col=0):
        self.curses_win = win
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.row = row
        self.col = col
    
    def set_win(self, ):
        win = self.curses_win
        # win.immedok(True) # auto refresh, bug may cause performance issue
        win.box()

    @property
    def bottom(self):
        return self.row + self.n_rows - 1

    def up(self, cursor):
        if cursor.row == self.row - 1 and self.row > 0:
            self.row -= 1

    def down(self, buffer, cursor):
        if cursor.row == self.bottom + 1 and self.bottom < buffer.bottom:
            self.row += 1

    def translate(self, cursor):
        return cursor.row - self.row, cursor.col - self.col
    
    def write(self, *args, **kwargs):
        self.curses_win.addstr(*args, **kwargs)
    
    def refresh(self, ):
        self.curses_win.refresh()


class Cursor:
    def __init__(self, row=0, col=0, col_hint=None):
        self.row = row
        self._col = col
        self._col_hint = col if col_hint is None else col_hint

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col
        self._col_hint = col


    def up(self, buffer):
        if self.row > 0:
            self.row -= 1
            self._clamp_col(buffer)

    def down(self, buffer):
        if self.row < buffer.bottom:
            self.row += 1
            self._clamp_col(buffer)

    def _clamp_col(self, buffer):        
        self.col = min(self.col, len(buffer[self.row]))

    def left(self, buffer):
        if self.col > 0:
            self.col -= 1
        elif self.row > 0:
            self.row -= 1
            self.col = len(buffer[self.row])

    def right(self, buffer):
        # print(self.col, len(buffer[self.row]))
        if self.col < len(buffer[self.row]):
            self.col += 1
        elif self.row < buffer.bottom:
            self.row += 1
            self.col = 0