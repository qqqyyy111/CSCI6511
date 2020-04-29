class HMM:
    def __init__(self, states, observations, emission_prob):
        self.states = states
        self.observations = observations
        self.transition_prob = {}
        self.emission_prob = emission_prob

    def calc_trans_prob(self, p):
        for i in range(1,4):
            for j in range(1,4):
                if i == j:
                    self.transition_prob[(i, j)] = p
                else:
                    self.transition_prob[(i, j)] = (1 - p) / 2

    def __str__(self):
        res_p1 = "States: " + str(self.states) + "\n"
        res_p2 = "Transition probabilities:  \n"
        for i in range(1,4):
            for j in range(1,4):
                res_p2 += str(self.transition_prob[(i,j)])
                res_p2 += " "
            res_p2 += "\n"
        res_p3 = "Emission probabilities: \n"
        for i in range(1,4):
            for j in range(1,4):
                res_p3 += str(self.emission_prob[(i,j)])
                res_p3 += " "
            res_p3 += "\n"
        return res_p1 + res_p2 + res_p3
