from utils import *
from valueIteration import do_several_value_iterations
from policyIteration import do_several_policy_iterations

file_path = './grids/grid1.txt'
grid_info = generate_grid_world(file_path)

discount = grid_info[0]
noises = grid_info[1]
states = grid_info[2]
size = grid_info[3]

k = 500

print(f'The following is the output of the value iteration when k = {k}: ')
states_after_value_iterations = do_several_value_iterations(k, discount, noises, states, size)
print_states(states_after_value_iterations, size)

print(f'The following is the output of the policy iteration when k = {k}: ')
states_after_policy_iterations = do_several_policy_iterations(k, discount, noises, states, size)
print_states(states_after_policy_iterations, size)
