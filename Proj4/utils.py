from HMM import HMM


def file_reader(input_file):
    f = open(input_file, 'r')
    file_info = f.readlines()
    row_index = 0
    states = [1, 2, 3]

    while '#' in file_info[row_index]:
        row_index += 1
    p = float(file_info[row_index])
    row_index += 1
    while '#' in file_info[row_index]:
        row_index += 1
    emission_prob = {}
    for i in range(0,3):
        emission_info = file_info[row_index + i].split(' ')
        for j in range(0,3):
            emission_prob[(states[i], states[j])] = float(emission_info[j])
    row_index += 3
    while '#' in file_info[row_index]:
        row_index += 1
    observations_info = file_info[row_index].split(',')
    observations = []
    for obs in observations_info:
        observations.append(float(obs))

    res = HMM(states, observations, emission_prob)
    res.calc_trans_prob(p)

    return res

