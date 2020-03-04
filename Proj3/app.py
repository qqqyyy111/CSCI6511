from utils import *
from valueIteration import do_several_value_iterations

file_path = './grids/grid2.txt'
grid_info = generate_grid_world(file_path)

discount = grid_info[0]
noises = grid_info[1]
states = grid_info[2]
size = grid_info[3]

times = 10

states_after_value_iterations = do_several_value_iterations(times, discount, noises, states, size)
print_states(states_after_value_iterations, size)