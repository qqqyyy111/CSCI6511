from copy import copy
import math


def update_policy(states, noises, grid_size):
    for state in states.values():
        better_dir = -1
        larger_val = 0 - math.inf
        if not state.col_index - 1 < 0:
            better_dir = 0
            larger_val = states[(state.row_index, state.col_index - 1)].val
        if (not state.row_index - 1 < 0) and (states[(state.row_index - 1, state.col_index)].val > larger_val):
            better_dir = 1
            larger_val = states[(state.row_index - 1, state.col_index)].val
        if (state.col_index + 1 < grid_size) and (states[(state.row_index, state.col_index + 1)].val > larger_val):
            better_dir = 2
            larger_val = states[(state.row_index, state.col_index + 1)].val
        if (state.row_index + 1 < grid_size) and (states[(state.row_index + 1, state.col_index)].val > larger_val):
            better_dir = 3
        state.update_policy(better_dir, noises)


def update_state(state, old_states, discount, grid_size):
    final_val = 0
    if not state.col_index - 1 < 0:
        final_val += old_states[(state.row_index, state.col_index - 1)].val * state.noises[0] * discount
    else:
        final_val += state.val * state.noises[0] * discount
    if not state.row_index - 1 < 0:
        final_val += old_states[(state.row_index - 1, state.col_index)].val * state.noises[1] * discount
    else:
        final_val += state.val * state.noises[1] * discount
    if state.col_index + 1 < grid_size:
        final_val += old_states[(state.row_index, state.col_index + 1)].val * state.noises[2] * discount
    else:
        final_val += state.val * state.noises[2] * discount
    if state.row_index + 1 < grid_size:
        final_val += old_states[(state.row_index + 1, state.col_index)].val * state.noises[3] * discount
    else:
        final_val += state.val * state.noises[3] * discount
    return final_val


def policy_iteration(discount, states, grid_size):
    old_states = states.copy()
    for state in states.values():
        if state.is_terminal:
            continue
        state.val = update_state(state, old_states, discount, grid_size)


def init_policy(states, noises):
    for state in states.values():
        state.set_init_policy(noises)


def do_several_policy_iterations(times, discount, noises, states, grid_size):
    return_states = copy(states)
    init_policy(return_states, noises)
    for time in range(0, times):
        policy_iteration(discount,return_states, grid_size)
        update_policy(return_states, noises, grid_size)
    return return_states
