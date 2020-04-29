

def viterbi_dp(start_prob, hmm):
    viterbi = {}
    path = {}

    for state in hmm.states:
        viterbi[(state, 0)] = start_prob[state - 1] * hmm.emission_prob[(state, hmm.observations[0])]
        path[state] = [state]

    for j in range(1,len(hmm.observations)):
        temp = {}
        for i in hmm.states:
            prob = -1
            for z in hmm.states:
                temp_prob = viterbi[(z, j-1)] * hmm.transition_prob[(z, i)] * hmm.emission_prob[(i, hmm.observations[j-1])]
                if temp_prob > prob:
                    prob = temp_prob
                    curr_state = z
                    viterbi[(i,j)] = prob
                    temp[i] = list.copy(path[curr_state])
                    temp[i].append(i)
        path = temp
    sequence_prob = -1
    state = 1
    for w in hmm.states:
        if viterbi[(w, len(hmm.observations)-1)] > sequence_prob:
            sequence_prob = viterbi[(w, len(hmm.observations)-1)]
            state = w
    sequence = []
    for s in path[state]:
        sequence.append(s)

    return sequence_prob, sequence

