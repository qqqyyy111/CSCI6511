Description:
    1. In the value iteration, for each state, I calculate the 4 possible results, according to the results from the
    k-1 iteration, with noises and discount, then I compare these 4 values and leave the largest value.
    2. In the policy iteration, I set a policy that all go left first. Initially, the iteration will follow the the
    policy until the convergence, then the program will check the results from one-step ahead, then update the new
    policy according to the largest result. After that, the program will repeat the previous steps until the policy not
    change anymore


How to Run:
    1. open the app.py file
    2. change the file_path to the test file path(the sample in project 3 introduction are already pre-load in grids folder)
    3. change the k value if you want(the default value of k is 500)
    4. run the app.py file
