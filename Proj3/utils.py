from State import State


def generate_grid_world(input_file):
    f = open(input_file, 'r')
    file_info = f.readlines()
    grid_size = int(file_info[0])
    discount = float(file_info[1])
    noises_info = file_info[2].split(', ')
    noises = []
    for float_num in noises_info:
        noises.append(float(float_num))
    grid_info = file_info[4:]
    states = {}
    for row_index, grid_line_info in enumerate(grid_info):
        grid_states = grid_line_info.split(',')
        for col_index, grid_state in enumerate(grid_states):
            state_value = 0
            is_terminal = False
            if grid_state != 'X':
                is_terminal = True
                state_value = int(grid_state)
            states[(row_index, col_index)] = State(state_value, is_terminal, row_index, col_index)
    return discount, noises, states, grid_size


