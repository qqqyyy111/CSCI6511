from utils import *
from viterbiAlg import viterbi_dp

input_file = './dice/hmm_dice_1586654620140.txt'
hmm = file_reader(input_file)
start_prob = [1/3, 1/3, 1/3]
sequence_info = viterbi_dp(start_prob, hmm)
print(hmm)
print("Sequence probabilities: " + str(sequence_info[0]))
sequence = ''
for s in sequence_info[1]:
    sequence += str(s)
    sequence += ' '
print("Sequence: \n" + sequence)
