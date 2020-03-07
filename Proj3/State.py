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
        if direction == 0:
            self.noises[0] = noises[0]
            self.noises[1] = noises[1]
            self.noises[2] = noises[3]
            self.noises[3] = noises[2]
        elif direction == 1:
            self.noises[0] = noises[1]
            self.noises[1] = noises[0]
            self.noises[2] = noises[2]
            self.noises[3] = noises[3]
        elif direction == 2:
            self.noises[0] = noises[3]
            self.noises[1] = noises[1]
            self.noises[2] = noises[0]
            self.noises[3] = noises[2]
        else:
            self.noises[0] = noises[1]
            self.noises[1] = noises[3]
            self.noises[2] = noises[2]
            self.noises[3] = noises[0]
        # self.noises[direction] = noises[0]
        # self.noises[(direction + 2) % 3] = noises[3]
        # self.noises[(direction + 1) % 3] = noises[1]
        # self.noises[(direction + 3) % 3] = noises[2]

