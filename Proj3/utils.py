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
    if len(noises) < 4:
        noises.append(0)
    grid_info = file_info[4:]
    states = {}
    for row_index, grid_line_info in enumerate(grid_info):
        grid_line_info = grid_line_info.split('\n')[0]
        grid_states = grid_line_info.split(',')
        for col_index, grid_state in enumerate(grid_states):
            state_value = float(0)
            is_terminal = False
            if grid_state != 'X':
                is_terminal = True
                state_value = int(grid_state)
            states[(row_index, col_index)] = State(state_value, is_terminal, row_index, col_index)
    return discount, noises, states, grid_size


def convert_dict_to_2d_list(object_dict, row_size, col_size):
    res_list = []
    for i in range(row_size):
        row = []
        for j in range(col_size):
            cell = object_dict[(i, j)]
            if cell.is_terminal:
                row.append(cell.val)
            else:
                row.append(format(cell.val, '.2f'))
        res_list.append(row)
    return res_list


def print_states(states, grid_size):
    for row_index in range(0, grid_size):
        row_str = ''
        for col_index in range(0, grid_size):
            if not states[(row_index, col_index)].is_terminal:
                row_str += str(format(states[(row_index, col_index)].val, '.2f'))
                row_str += ' '
            else:
                row_str += str(states[(row_index, col_index)].val)
                row_str += ' '
        print(row_str)


def print_states_neatly(states, grid_size):
    converted_list = convert_dict_to_2d_list(states, grid_size, grid_size)
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in converted_list]))
    s = [[str(cell) for cell in row] for row in converted_list]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))
