class State:
    def __init__(self, val, is_terminal, row_index, col_index):
        self.val = val
        self.is_terminal = is_terminal
        self.col_index = col_index
        self.row_index = row_index

    def update(self, up, left, right, down, discount, states, grid_size):
        up_row_index = self.row_index
        down_row_index = self.row_index
        left_col_index = self.col_index
        right_col_index = self.col_index
        if not up_row_index - 1 < 0:
            up_row_index -= 1
            self.val += (states[(up_row_index, self.col_index)] * up * discount)
        if down_row_index + 1 < grid_size:
            down_row_index += 1
            self.val += (states[(down_row_index, self.col_index)] * down * discount)
        if not left_col_index - 1 < 0:
            left_col_index -= 1
            self.val += (states[(self.row_index, left_col_index)] * left * discount)
        if right_col_index + 1 < grid_size:
            right_col_index += 1
            self.val += (states[(self.row_index, right_col_index)] * right * discount)


