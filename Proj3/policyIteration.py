from copy import copy
import math


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


def update_policy(states, noises, discount, grid_size):
    old_states = states.copy()
    no_policy_change = True
    for state in states.values():
        if state.best_policy:
            break
        if state.is_terminal:
            continue
        better_dir = -1
        max_next_step = 0 - math.inf
        waiting_states = [copy(state), copy(state), copy(state), copy(state)]
        for i in range(4):
            waiting_states[i].update_policy(i, noises)
            return_res = update_state(waiting_states[i], old_states, discount, grid_size)
            if return_res > max_next_step:
                max_next_step = return_res
                better_dir = i
        del waiting_states, max_next_step
        if no_policy_change and state.policy_dir != better_dir:
            no_policy_change = False
        state.update_policy(better_dir, noises)
    if no_policy_change:
        for state in states.values():
            state.final_policy()


def policy_iteration(discount, noises, states, grid_size, difference_allowed):
    old_states = states.copy()
    max_difference = 0
    for state in states.values():
        if state.is_terminal:
            continue
        state.val = update_state(state, old_states, discount, grid_size)
        max_difference = max(max_difference, abs(state.val - old_states[state.row_index, state.col_index].val))
    if max_difference < difference_allowed:
        update_policy(states, noises, discount, grid_size)


def init_policy(states, noises):
    for state in states.values():
        state.set_init_policy(noises)
ß

def do_several_policy_iterations(times, discount, noises, states, grid_size):
    return_states = copy(states)
    init_policy(return_states, noises)
    difference_allowed = 0.0001
    for time in range(0, times):
        policy_iteration(discount,noises, return_states, grid_size, difference_allowed)
    return return_states
