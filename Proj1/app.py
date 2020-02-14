import random
import time
import utils
from uninformedSearch import dijkstra
from informedSearch import a_star


# set the files path and generate the map
vertices_number = '2000'
file_version = '0.3'
vertices_file = './graphs/graph' + vertices_number + '_' + file_version + '/v.txt'
edges_file = './graphs/graph' + vertices_number + '_' + file_version + '/e.txt'
vertices = utils.generate_map(vertices_file,edges_file)

# get the random start point and end point
start_point = str(random.randint(0, int(vertices_number)))
end_point = str(random.randint(0, int(vertices_number) - 1))
# set the specific start point and end point (! both types should be str)
# start_point = '222'
# end_point = '887'


# informed search - A*
informed_search_start_time = time.time()
informed_search_res = a_star(start_point, end_point, vertices)
informed_search_end_time = time.time()
informed_search_cost = informed_search_end_time - informed_search_start_time
print(f'With the informed search A-star, the minimum distance from {start_point} to {end_point} '
      f'is {informed_search_res} and its time cost is {informed_search_cost}')

# uninformed search - Dijkstra
uninformed_search_start_time = time.time()
uninformed_search_res = dijkstra(start_point, vertices)
uninformed_search_res_distance = uninformed_search_res[end_point]
uninformed_search_end_time = time.time()
uninformed_search_cost = uninformed_search_end_time - uninformed_search_start_time
print(f'With the uninformed search Dijkstra, the minimum distance from {start_point} to {end_point} '
      f'is {uninformed_search_res_distance} and its time cost is {uninformed_search_cost}')


