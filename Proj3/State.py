class State:
    def __init__(self, val, is_terminal, row_index, col_index):
        self.val = val
        self.is_terminal = is_terminal
        self.col_index = col_index
        self.row_index = row_index
        self.noises = {
        }

    def set_init_policy(self, noises):
        self.noises[0] = noises[0]
        self.noises[1] = noises[1]
        self.noises[3] = noises[2]
        self.noises[2] = 0
        if noises[3]:
            self.noises[2] = noises[3]

    def update_policy(self, direction, noises):
        self.noises[direction] = noises[0]
        self.noises[(direction + 2) % 4] = noises[3]
        self.noises[(direction + 1) % 4] = noises[1]
        self.noises[(direction + 3) % 4] = noises[2]

