from copy import copy


def update_policy():
    print()


def policy_iteration(discount, states, grid_size):
    old_states = states.copy()
    for state in states.values():
        if state.is_terminal:
            continue
        final_val = 0
        if not state.col_index - 1 < 0:
            final_val += old_states[(state.row_index, state.col_index - 1)].val * states.noises[0] * discount
        else:
            final_val += state.val * state.noises[0] * discount
        if not state.row_index - 1 < 0:
            final_val += old_states[(state.row_index - 1, state.col_index)].val * state.noises[1] * discount
        else:
            final_val += state.val * state.noises[1] * discount
        if state.col_index + 1 < grid_size:
            final_val += old_states[(state.row_index, state.col_index + 1)].val * states.noises[2] * discount
        else:
            final_val += state.val * state.noises[2] * discount
        if state.row_index + 1 < grid_size:
            final_val += old_states[(state.row_index + 1, state.col_index)].val * state.noises[1] * discount
        else:
            final_val += state.val * state.noises[3] * discount
        state.val = final_val


def do_several_policy_iterations(times, discount, noises, states, grid_size):
    return_states = copy(states)
    update_policy()
    for time in range(0, times):
        policy_iteration(discount,return_states, grid_size)
    return return_states
