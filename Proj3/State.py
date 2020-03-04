class State:
    def __init__(self, val, is_terminal, row_index, col_index):
        self.val = val
        self.is_terminal = is_terminal
        self.col_index = col_index
        self.row_index = row_index
