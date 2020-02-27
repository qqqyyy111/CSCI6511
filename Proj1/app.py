import random
import time
import utils
from uninformedSearch import dijkstra
from informedSearch import a_star
from test import *


# set the files path and generate the map
vertices_number = '2000'
file_version = '0.3'
vertices_file = './graphs/graph' + vertices_number + '_' + file_version + '/v.txt'
edges_file = './graphs/graph' + vertices_number + '_' + file_version + '/e.txt'
map = utils.generate_map(vertices_file,edges_file)

# get the random start point and end point
start_point = str(random.randint(0, int(vertices_number)))
end_point = str(random.randint(0, int(vertices_number) - 1))
# set the specific start point and end point (! both types should be str)
# start_point = '0'
# end_point = '99'

# informed search - A*
informed_search_start_time = time.time()
informed_search_res = a_star(start_point, end_point, map)
informed_search_end_time = time.time()
informed_search_cost = informed_search_end_time - informed_search_start_time
print(f'With the informed search A-star, the minimum distance from {start_point} to {end_point} '
      f'is {informed_search_res[0]} and its time cost is {informed_search_cost} \n'
      f'Algorithm Step: {informed_search_res[1]}')

# uninformed search - Dijkstra
uninformed_search_start_time = time.time()
uninformed_search_res = dijkstra(start_point, end_point, map)
uninformed_search_end_time = time.time()
uninformed_search_cost = uninformed_search_end_time - uninformed_search_start_time
print(f'With the uninformed search Dijkstra, the minimum distance from {start_point} to {end_point} '
      f'is {uninformed_search_res[0]} and its time cost is {uninformed_search_cost} \n'
      f'Algorithm Step: {uninformed_search_res[1]}')

# test case sample
# test_algorithm_steps('0', 1000, 1500, map)
