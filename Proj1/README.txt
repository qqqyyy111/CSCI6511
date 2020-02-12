Zhechao Wang
CSCI 6511 - GWU

Intro:
    Dijkstra (Uninformed Search):
        I used a dictionary contains the possible next move as key and the move cost as value to check which is the
        best next move. Every time I make a move, I will add the current node to the visited list, remove the node from
        the unvisited list, and update the open list, which also include the necessary method that check the distances to
        the neighbors of current node are the shortest distances.

    A Star (Informed Search):
        Pretty similar  to the Dijkstra, but as dijkstra use the cost from start vertex to the current vertex as the
        condition for how to make the next move, a star use the cost (g(n)) from start node to the goal node, like
        dijkstra uses, and use the further cost (h(n)) as the other condition to make the next move decision

    (You can find you details in the program comments)

How to run:
    1. open the app.py file
    2. edit the vertices number and file version (like vertices_number = 1000, file version = 0.1, the program will run
        with the files in the graph1000_0.1 fold, which is in the graphs fold)
    3. it program is set to run with random start point and end point, if you want to run with specific points, comments
        the random start point and end point generate lines, and de-comment the points specifying lines, then change the
        point index to the index you want to test(please use str for index)
    4. run the app.py file

Comparision:
    Both Dijkstra and A star will get the optimal result, but not like dijkstra will take steady time, the calculate
    time of a star is not unsteady, it really depends on the value of h, so for same file with different h calculation
    methods, time cost will be different. But mostly, the total time cost of A star should be smaller than dijkstra.