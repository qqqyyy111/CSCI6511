import time
from informedSearch import a_star
from uninformedSearch import dijkstra


def test_all(start_point, range_start, range_end, map):
    for i in range(range_start, range_end):
        end_point = str(i)
        informed_search_start_time = time.time()
        informed_search_res = a_star(start_point, end_point, map)
        informed_search_end_time = time.time()
        informed_search_cost = informed_search_end_time - informed_search_start_time
        print(f'A-star   - start: {start_point} end: {end_point} '
              f'res: {informed_search_res} time cost: {informed_search_cost}')
        uninformed_search_start_time = time.time()
        uninformed_search_res = dijkstra(start_point, end_point, map)
        uninformed_search_end_time = time.time()
        uninformed_search_cost = uninformed_search_end_time - uninformed_search_start_time
        print(f'Dijkstra - start: {start_point} end: {end_point} '
              f'res: {uninformed_search_res} time cost: {uninformed_search_cost} \n')


def test_error_and_cost(start_point, range_start, range_end, map):
    error_num = 0
    cost_num = 0
    for i in range(range_start, range_end):
        end_point = str(i)
        informed_search_start_time = time.time()
        informed_search_res = a_star(start_point, end_point, map)
        informed_search_end_time = time.time()
        informed_search_cost = informed_search_end_time - informed_search_start_time
        uninformed_search_start_time = time.time()
        uninformed_search_res = dijkstra(start_point, end_point, map)
        uninformed_search_end_time = time.time()
        uninformed_search_cost = uninformed_search_end_time - uninformed_search_start_time
        # a_star_path = utils.dict_to_list(end_point, informed_search_res[1])
        if informed_search_res[0] != uninformed_search_res[0]:
            error_num += 1
            print(f'differences exist in {start_point} and {end_point} \n'
                  f'A-star: {informed_search_res} Dijkstra: {uninformed_search_res} \n')
        if informed_search_cost > uninformed_search_cost:
            cost_num += 1
    print(f'all test cases passed, {error_num} error(s), {cost_num} A star cost more time case(s)')


def test_algorithm_steps(start_point, range_start, range_end, map):
    bad_case_num = 0
    for i in range(range_start, range_end):
        end_point = str(i)
        informed_search_res = a_star(start_point, end_point, map)
        uninformed_search_res = dijkstra(start_point, end_point, map)
        a_star_step = informed_search_res[1]
        dijkstra_step = uninformed_search_res[1]
        if a_star_step > dijkstra_step:
            bad_case_num += 1
            print(f'Bad case occurs from {start_point} to {end_point}\n'
                  f'A_star step count: {a_star_step} \n'
                  f'Dijkstra step count: {dijkstra_step}')
    print(f'all test cases passed, {bad_case_num} bad case(s)')

