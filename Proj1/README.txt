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
    4. if you want to run multiple cases, uncomment 'from test import *', and choose one of the test method to run,
        there is a sample test code at the button for pathfinder from 0 to 1000~1500. Before running the test, please
        uncomment the normal output lines(23 ~ 39)
    5. run the app.py file

Output:
    1. A star optimal distance
    2. A star time cost
    3. A star algorithm step cost
    4. Dijkstra optimal distance
    5. Dijkstra time cost
    6. Dijkstra algorithm step cost

Comparision:
    Both Dijkstra and A star will get the optimal result, but not like dijkstra will take steady time, the calculate
    time of a star is not unsteady, it really depends on the value of h, so for same file with different h calculation
    methods, time cost will be different. Theologically, A* with priority queue will take O(e + vlogv), and Dijkstra
    with priority queue should be O(v + elogv). It should works pretty good in puzzles and maze game. However, since
    we need to concern that the first goal node we get in A star is not the optimal result since key of the priority
    queue is the f, which f = g + h. So, sometimes, especially the map we generated, the time cost will be highly
    affected by the f, since the path first time A star reach the goal is not the optimal path, and the distance(g) is
    not the optimal distance, which A star will take more time to get the optimal result than Dijkstra.
