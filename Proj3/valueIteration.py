from copy import copy


def value_iteration(discount, noises, states, grid_size):
    old_states = states.copy()
    for state in states.values():
        if state.is_terminal:
            continue
        waiting_states = [copy(state), copy(state), copy(state), copy(state)]
        # left -> up -> right -> down
        update(waiting_states[0], noises[0], noises[1], noises[3], noises[2], discount, old_states, grid_size)
        update(waiting_states[1], noises[1], noises[0], noises[2], noises[3], discount, old_states, grid_size)
        update(waiting_states[2], noises[3], noises[1], noises[0], noises[2], discount, old_states, grid_size)
        update(waiting_states[3], noises[1], noises[3], noises[2], noises[0], discount, old_states, grid_size)
        max_state = waiting_states[0]
        for waiting_state in waiting_states:
            if max_state.val < waiting_state.val:
                max_state = waiting_state
        states[(state.row_index, state.col_index)] = copy(max_state)
        del waiting_states


# update the state value with max(Q)
def update(this_state, left, up, right, down, discount, states, grid_size):
    up_row_index = this_state.row_index
    down_row_index = this_state.row_index
    left_col_index = this_state.col_index
    right_col_index = this_state.col_index
    final_result = 0
    if not up_row_index - 1 < 0:
        up_row_index -= 1
        final_result += (states[(up_row_index, this_state.col_index)].val * up * discount)
    else:
        final_result += (this_state.val * up * discount)
    if down_row_index + 1 < grid_size:
        down_row_index += 1
        final_result += (states[(down_row_index, this_state.col_index)].val * down * discount)
    else:
        final_result += (this_state.val * down * discount)
    if not left_col_index - 1 < 0:
        left_col_index -= 1
        final_result += (states[(this_state.row_index, left_col_index)].val * left * discount)
    else:
        final_result += (this_state.val * left * discount)
    if right_col_index + 1 < grid_size:
        right_col_index += 1
        final_result += (states[(this_state.row_index, right_col_index)].val * right * discount)
    else:
        final_result += (this_state.val * right * discount)
    this_state.val = final_result


def do_several_value_iterations(times, discount, noises, states, grid_size):
    return_states = copy(states)
    for time in range(0, times):
        value_iteration(discount, noises, return_states, grid_size)
    return return_states

