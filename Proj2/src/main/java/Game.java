import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map.Entry;
import java.util.concurrent.TimeUnit;
import com.alibaba.fastjson.*;
import java.lang.Math;

public class Game {
    private final static int MAX_DEPTH = 3;
    private final int TIMER = 150; // Each step in 180 seconds (Make sure searching would not exceed the time limit)
    private final int TEAM_ID = 1197;

    private Requests requests;
    private int gameId;
    private int boardSize;
    private int target; // Get target in a row to win
    private String selfSymbol; // Either "X" (Second to move) or "O" (First to move)
    private int[][] board; // 0: none, 1: "O", 2: "X"
    private int[][][] boardSum; // [x][y][4]: The sum of symbol at (x, y) in a row in 4 directions
    private int turn;
    private int threadNo;
    private ArrayList<Node> searchList;
    private int optimalX, optimalY;
    private int[] evalScore;
    private ThreadSearch[] threadList;
    private int winOrLoseImmediately; // 0: no win or lose, 1: win, -1: lose

    private int prunedChildren;

    /**
     * Join a game
     * @param gameId
     * @param boardSize
     * @param target
     * @param selfSymbol
     * @throws InterruptedException
     * @throws Exception
     */
    public Game(int gameId, int boardSize, int target, String selfSymbol) throws InterruptedException, IOException {
        this.gameId = gameId;
        this.boardSize = boardSize;
        this.target = target;
        this.selfSymbol = selfSymbol;
        this.requests = new Requests();
        this.threadNo = Math.max(Runtime.getRuntime().availableProcessors(), 2);
        this.board = new int[boardSize][boardSize];
        this.boardSum = new int[boardSize][boardSize][4];
        this.searchList = new ArrayList<Node>();
        this.evalScore = new int[target];
        for (int i = 0; i < target; i++) {
            if (i < target - 3) {
                this.evalScore[i] = (int) (Math.pow(2, i) * 10);
            } else if (i == target - 3) {
                this.evalScore[i] = (int) (Math.pow(2, i) * 50);
            } else if (i == target - 2) {
                this.evalScore[i] = (int) (Math.pow(2, i) * 250);
            } else {
                this.evalScore[i] = (int) (Math.pow(2, i) * 2000);
            }
        }
        this.threadList = new ThreadSearch[this.threadNo];
        for (int i = 0; i < this.threadNo; i++) {
            this.threadList[i] = new ThreadSearch();
            this.threadList[i].start();
            this.threadList[i].join();
        }
        this.winOrLoseImmediately = 0;

        initBoard();
        System.out.println("INFO: Finished initialization");
        printBoard();
    }

    /**
     * Control the process of game till end
     * @throws Exception
     */
    public void start() throws Exception {
        // If someone's win, exit
        while (this.checkEnd() == false) {
            if ((this.turn % 2 == 0 && selfSymbol.equals("O")) || (this.turn % 2 == 1 && selfSymbol.equals("X"))) {
                // If it's opponent's turn, keep querying every second until they make a move
                String move;
                do {
                    TimeUnit.SECONDS.sleep(1);
                    move = getLastMove();
                } while (move.startsWith(selfSymbol) || move.equals(""));
                String[] temp = move.split(",");
                System.out.println("INFO: Turn " + Integer.toString(this.turn));
                System.out.println("Opponent move = " + "(" + temp[1] + ", " + temp[2] + ")");
                this.updateBoard(Integer.parseInt(temp[1]), Integer.parseInt(temp[2]), temp[0]);
                printBoard();
            } else {
                // If it's our turn, think and make move
                makeMove();
            }
            this.turn += 1;
        }
    }

    /**
     * Initialize the board and boardSum with the given game
     */
    private void initBoard() throws IOException {
        HashMap<String, String> params = new HashMap<String, String>();
        params.put("type", "boardMap");
        params.put("gameId", Integer.toString(this.gameId));
        String result = this.requests.get(params);

        JSONObject parsedResult = JSON.parseObject(result);
        String outputString = parsedResult.getString("output");
        if (outputString == null) {
            this.turn = 1;
            return;
        }

        JSONObject output = JSON.parseObject(outputString);
        int count = 1;
        for (Entry<String, Object> e : output.entrySet()) {
            String key = e.getKey(), value = (String) e.getValue();
            String[] xy = key.split(",");
            int x = Integer.parseInt(xy[0]), y = Integer.parseInt(xy[1]);
            this.updateBoard(x, y, value);
            count++;
        }
        this.turn = count;
    }

    /**
     * Print out the game board
     */
    private void printBoard() {
        System.out.print("  ");
        for (int i = 0; i < this.boardSize; i++) {
            if (i < 10) {
                System.out.print(" " + Integer.toString(i) + " ");
            } else {
                System.out.print(" " + Integer.toString(i));
            }
        }
        System.out.println();
        for (int i = 0; i < this.boardSize; i++) {
            if (i < 10) {
                System.out.print(Integer.toString(i) + " ");
            } else {
                System.out.print(Integer.toString(i));
            }
            for (int j = 0; j < this.boardSize; j++) {
                if (this.board[i][j] == 0) {
                    System.out.print(" - ");
                } else if (this.board[i][j] == 1) {
                    System.out.print(" O ");
                } else {
                    System.out.print(" X ");
                }
            }
            System.out.println();
        }
        System.out.println();
    }

//    private void printBoardSum() {
//        for (int i = 0; i < this.boardSize; i++) {
//            for (int j = 0; j < this.boardSize; j++) {
//                System.out.print(" " + Arrays.toString(this.boardSum[i][j]));
//            }
//            System.out.println();
//        }
//        System.out.println();
//    }

    /**
     * Confirm a move, send wih API and update the board
     * @param x
     * @param y
     * @throws Exception
     */
    private void confirmMove(int x, int y) throws Exception {
        String move = Integer.toString(x) + "," + Integer.toString(y);
        HashMap<String, String> params = new HashMap<String, String>();
        params.put("type", "move");
        params.put("teamId", Integer.toString(this.TEAM_ID));
        params.put("gameId", Integer.toString(this.gameId));
        params.put("move", move);
        String result = this.requests.post(params);

        JSONObject parsedResult = JSON.parseObject(result);
        if (!parsedResult.getString("code").contains("OK")) {
            throw new Exception("ERROR: making move: " + result);
        } else {
            this.updateBoard(x, y, this.selfSymbol);
        }
    }

    /**
     * Get the last move
     * @return String in format "symbol,X,Y" or "" if no move
     * @throws Exception
     */
    private String getLastMove() throws Exception {
        HashMap<String, String> params = new HashMap<String, String>();
        params.put("type", "moves");
        params.put("gameId", Integer.toString(this.gameId));
        params.put("count", Integer.toString(1));
        String result = this.requests.get(params);

        JSONObject parsedResult = JSON.parseObject(result);
        if (!parsedResult.getString("code").equals("OK")) {
            if (parsedResult.getString("message").equals("No moves")) {
                return "";
            } else {
                throw new Exception("ERROR: getting last move: " + result);
            }
        } else {
            JSONObject temp = JSON.parseObject(parsedResult.get("moves").toString().replace("[", "").replace("]", ""));
            return temp.get("symbol") + "," + temp.get("moveX") + "," + temp.get("moveY");
        }
    }

    /**
     * Search for the best option and make a move
     * @throws Exception
     */
    private void makeMove() throws Exception {
        System.out.println("INFO: Turn " + Integer.toString(this.turn));
        long startTime = System.currentTimeMillis() / 1000;
        if (this.turn == 1) {
            // First turn, go center
            this.optimalX = (int) (Math.ceil(this.boardSize / 2));
            this.optimalY = (int) (Math.ceil(this.boardSize / 2));
        } else if (this.turn == 2 || this.turn == 3) {
            // Second or third turn, go 1 unit from center
            do {
                this.optimalX = (int) (Math.ceil(this.boardSize / 2)) + (int) Math.floor(Math.random() * 3 - 1);
                this.optimalY = (int) (Math.ceil(this.boardSize / 2)) + (int) Math.floor(Math.random() * 3 - 1);
            } while (board[this.optimalX][this.optimalY] != 0);
        } else {
            // Search with multiple threads (Number of threads depends on the power of CPU)
            searchList.clear();
            this.prunedChildren = 0;
            winOrLoseImmediately = 0;
            Node root = new Node();
            root.createChildren();

            if (this.winOrLoseImmediately == 0) {
                System.out.println("Created " + Integer.toString(searchList.size()) + " leaf nodes");
                for (ThreadSearch ts: this.threadList) {
                    ts.setStartTime(startTime);
                    ts.run();
                    ts.join();
                }
                System.out.println("Pruned " + Integer.toString(this.prunedChildren) + " leaf nodes");

                System.out.println("Max score = " + Integer.toString(root.minOrMaxVal));
                if (root.minOrMaxVal == Integer.MIN_VALUE) {
                    // Would lose anyway so play randomly
                    do {
                        this.optimalX = (int) (Math.random() * (double) this.boardSize);
                        this.optimalY = (int) (Math.random() * (double) this.boardSize);
                    } while (board[this.optimalX][this.optimalY] != 0);
                } else {
                    // Select the move which have both the greatest temporary score and overall score
                    int tempOptimalScore = Integer.MIN_VALUE;
                    for (Node l1Node : root.children) {
                        for (int i = 0; i < MAX_DEPTH; i += 2) {
                            if (Arrays.equals(root.optimalMoves[i], l1Node.newMoves[0])) {
                                int l2MaxScore = Integer.MAX_VALUE;
                                for (Node l2Node: l1Node.children) {
                                    int temp = l2Node.evaluate();
                                    l2MaxScore = Math.min(l2MaxScore, temp);
                                }
                                if (tempOptimalScore < l2MaxScore) {
                                    tempOptimalScore = l2MaxScore;
                                    this.optimalX = l1Node.newMoves[0][0];
                                    this.optimalY = l1Node.newMoves[0][1];
                                }
                            }
                            // if (root.optimalMoves[i][0] == child.newMoves[0][0] && root.optimalMoves[i][1] == child.newMoves[0][1]) {
                            //     int score = child.evaluate();
                            //     if (score > tempOptimalScore) {
                            //         this.optimalX = child.newMoves[0][0];
                            //         this.optimalY = child.newMoves[0][1];
                            //         tempOptimalScore = score;
                            //     }
                            //     break;
                            // }
                        }
                    }
                }
            }
        }
        String choice = "(" + Integer.toString(this.optimalX) + ", " + Integer.toString(this.optimalY) + ")";
        System.out.println("Move = " + choice + ", time cost of move = "
                + Long.toString(System.currentTimeMillis() / 1000 - startTime) + " seconds");
        confirmMove(this.optimalX, this.optimalY);
        printBoard();
    }

    /**
     * Update the board and boardSum with the newest move
     * @param x
     * @param y
     * @param symbol
     */
    private void updateBoard(int x, int y, String symbol) {
        // update board
        int symbolInt;
        if (symbol.equals("O")) {
            symbolInt = 1;
        } else {
            symbolInt = 2;
        }
        this.board[x][y] = symbolInt;

        // update boardSum of (x, y)
        int[][] fourDirection = { { -1, 0 }, { 0, -1 }, { -1, -1 }, { -1, 1 } };
        for (int dir = 0; dir < 4; dir++) {
            int xx = x + fourDirection[dir][0], yy = y + fourDirection[dir][1];
            if (this.getOnBoard(xx, yy) == symbolInt) {
                this.boardSum[x][y][dir] = this.boardSum[xx][yy][dir] + 1;
            } else {
                this.boardSum[x][y][dir] = 1;
            }
        }

        // update boardSum of others in 4 directions
        for (int dir = 0; dir < 4; dir++) {
            int count = -1;
            while (true) {
                int xx = x + fourDirection[dir][0] * count, yy = y + fourDirection[dir][1] * count;
                if (this.getOnBoard(xx, yy) == symbolInt) {
                    this.boardSum[xx][yy][dir] = this.boardSum[xx + fourDirection[dir][0]][yy + fourDirection[dir][1]][dir] + 1;
                    count -= 1;
                } else {
                    break;
                }
            }
        }
    }

    /**
     * Pop out the first item thread-safely
     * @return The first item in searchList of null if none
     */
    private synchronized Node popSearchList() {
        if (searchList.size() > 0) {
            return searchList.remove(0);
        } else {
            return null;
        }
    }

    /**
     * Check if the play ends (win, lose or draw)
     * @return
     */
    private boolean checkEnd() {
        int countNull = 0;
        for (int i = 0; i < this.boardSize; i++) {
            for (int j = 0; j < this.boardSize; j++) {
                if (this.board[i][j] > 0) {
                    for (int l = 0; l < 4; l++) {
                        if (this.boardSum[i][j][l] == this.target) {
                            if ((this.board[i][j] == 1 && this.selfSymbol.equals("O")) || (this.board[i][j] == 2 && this.selfSymbol.equals("X"))) {
                                System.out.println("WIN!");
                            } else {
                                System.out.println("LOSE!");
                            }
                            return true;
                        }
                    }
                } else {
                    countNull += 1;
                }
            }
        }
        if (countNull == 0) {
            System.out.println("DRAW!");
            return true;
        }
        return false;
    }

    /**
     * Get point (x, y) on board
     * @param x
     * @param y
     * @return -1: not on board, 0: nothing, 1: "O", 2: "X"
     */
    private int getOnBoard(int x, int y) {
        if (x < 0 || x >= this.boardSize || y < 0 || y >= this.boardSize) {
            return -1;
        } else {
            return this.board[x][y];
        }
    }


    /**
     * Node of search tree
     * (Tried to separate it from Game class but there are a lot data commonly used. So just keep it inside)
     */
    class Node {
        protected String symbol;
        protected int[][][] nodeBoardSum;
        public boolean pruned;
        protected int minOrMaxVal; // same symbol with selfSymbol: minimum, different symbol with selfSymbol: maximum
        protected ArrayList<Node> children;
        protected Node parent;
        protected int depth;
        protected boolean isRoot;
        protected int calculatedChildren;
        protected int[][] newMoves; // int[depth][3], int[i] means ith step (x, y, symbol) since current move
        protected int[][] optimalMoves;

        /**
         * Constructor of root node
         */
        public Node() {
            this.symbol = selfSymbol;
            this.nodeBoardSum = boardSum;
            this.pruned = false;
            this.minOrMaxVal = Integer.MIN_VALUE;
            this.children = new ArrayList<Node>();
            this.parent = null;
            this.depth = 0;
            this.isRoot = true;
            this.calculatedChildren = 0;
            this.newMoves = null;
        }

        /**
         * Constructor of other nodes
         */
        public Node(Node parent, int newMoveX, int newMoveY) {
            this.nodeBoardSum = copyBoardSum(parent.nodeBoardSum);
            this.pruned = false;
            this.children = new ArrayList<Node>();
            this.parent = parent;
            this.depth = parent.depth + 1;
            this.isRoot = false;
            this.calculatedChildren = 0;
            this.newMoves = new int[this.depth][3];
            for (int i = 0; i < parent.depth; i++) {
                this.newMoves[i] = parent.newMoves[i].clone();
            }
            if (parent.symbol.equals("O")) {
                this.symbol = "X";
                this.newMoves[parent.depth] = new int[] { newMoveX, newMoveY, 1 };
            } else {
                this.symbol = "O";
                this.newMoves[parent.depth] = new int[] { newMoveX, newMoveY, 2 };
            }
            if (this.symbol.equals(selfSymbol)) {
                // max
                this.minOrMaxVal = Integer.MIN_VALUE;
            } else {
                // min
                this.minOrMaxVal = Integer.MAX_VALUE;
            }
            this.updateNodeBoard(newMoveX, newMoveY, parent.symbol);
        }

        /**
         * Update the node board and nodeBoardSum with new move
         * @param x
         * @param y
         * @param symbol
         */
        private void updateNodeBoard(int x, int y, String symbol) {
            int symbolInt;
            if (symbol.equals("O")) {
                symbolInt = 1;
            } else {
                symbolInt = 2;
            }

            // update nodeBoardSum of self
            int[][] fourDirection = { { -1, 0 }, { 0, -1 }, { -1, -1 }, { -1, 1 } };
            for (int dir = 0; dir < 4; dir++) {
                int xx = x + fourDirection[dir][0], yy = y + fourDirection[dir][1];
                if (this.getOnNodeBoard(xx, yy) == symbolInt) {
                    this.nodeBoardSum[x][y][dir] = this.nodeBoardSum[xx][yy][dir] + 1;
                } else {
                    this.nodeBoardSum[x][y][dir] = 1;
                }
            }

            // update nodeBoardSum of others in 4 directions
            for (int dir = 0; dir < 4; dir++) {
                int count = -1;
                while (true) {
                    int xx = x + fourDirection[dir][0] * count, yy = y + fourDirection[dir][1] * count;
                    if (this.getOnNodeBoard(xx, yy) == symbolInt) {
                        this.nodeBoardSum[xx][yy][dir] = this.nodeBoardSum[xx + fourDirection[dir][0]][yy + fourDirection[dir][1]][dir] + 1;
                        count -= 1;
                    } else {
                        break;
                    }
                }
            }
        }

        /**
         * Create a search tree from root. Find a way to win (or lose) immediately if possible
         */
        private void createChildren() {
            int win = this.checkWin();
            if (win == 1) {
                winOrLoseImmediately = 1;
                optimalX = this.newMoves[0][0];
                optimalY = this.newMoves[0][1];
            } else if (win == -1 && winOrLoseImmediately != 1) {
                winOrLoseImmediately = -1;
                optimalX = this.newMoves[1][0];
                optimalY = this.newMoves[1][1];
            } else if (win == 0) {
                for (int i = 0; i < boardSize; i++) {
                    for (int j = 0; j < boardSize; j++) {
                        // If the place is suitable, add to search tree
                        if (this.getOnNodeBoard(i, j) == 0 && this.checkAround(i, j)) {
                            Node temp = new Node(this, i, j);
                            this.children.add(temp);
                            if (this.depth == MAX_DEPTH - 1) {
                                searchList.add(temp);
                            } else if (this.depth < MAX_DEPTH - 1) {
                                temp.createChildren();
                            }
                        }
                    }
                }
            }
        }

        /**
         * Check if any piece in 1 unit or any 2 pieces in 2 units around (i, j)
         * @param i
         * @param j
         * @return
         */
        private boolean checkAround(int i, int j) {
            for (int a = -1; a <= 1; a++) {
                for (int b = -1; b <= 1; b++) {
                    if (this.getOnNodeBoard(i + a, j + b) > 0) {
                        return true;
                    }
                }
            }

            int have2Around = 0;
            for (int a = -2; a <= 2; a+=2) {
                for (int b = -2; b <= 2; b+=2) {
                    if (this.getOnNodeBoard(i + a, j + b) > 0) {
                        have2Around += 1;
                    }
                }
            }
            return (have2Around >= 2);
        }

        /**
         * Check if any player wins
         * @return 0: no one win, 1: win, -1: lose
         */
        private int checkWin() {
            for (int i = 0; i < boardSize; i++) {
                for (int j = 0; j < boardSize; j++) {
                    int temp = this.getOnNodeBoard(i, j);
                    if (temp > 0) {
                        for (int l = 0; l < 4; l++) {
                            if (this.nodeBoardSum[i][j][l] == target) {
                                if ((temp == 1 && selfSymbol.equals("O")) || (temp == 2 && selfSymbol.equals("X"))) {
                                    return 1;
                                } else {
                                    return -1;
                                }
                            }
                        }
                    }
                }
            }
            return 0;
        }

        private int[][][] copyBoardSum(int[][][] boardSum) {
            int[][][] boardSumCopy = new int[boardSize][boardSize][];
            for (int i = 0; i < boardSize; i++) {
                for (int j = 0; j < boardSize; j++) {
                    boardSumCopy[i][j] = boardSum[i][j].clone();
                }
            }
            return boardSumCopy;
        }

        /**
         * Get point (x, y) on node board
         * @param x
         * @param y
         * @return -1: not on board, 0: nothing, 1: "O", 2: "X"
         */
        private int getOnNodeBoard(int x, int y) {
            if (x < 0 || x >= boardSize || y < 0 || y >= boardSize) {
                return -1;
            } else {
                if (this.newMoves != null) {
                    for (int[] newMove: this.newMoves) {
                        if (newMove[0] == x && newMove[1] == y) {
                            return newMove[2];
                        }
                    }
                }
                return board[x][y];
            }
        }

        private int getOnNodeBoardSum(int x, int y, int dir) {
            if (x < 0 || x >= boardSize || y < 0 || y >= boardSize) {
                return -1;
            } else {
                return this.nodeBoardSum[x][y][dir];
            }
        }

        /**
         * Cut all the unnecessary nodes
         */
        private synchronized void pruneChildren() {
            if (!this.pruned) {
                this.calculatedChildren = this.children.size();
                this.pruned = true;
                for (Node childNode : this.children) {
                    childNode.pruneChildren();
                }
            }
        }

        /**
         * Update the search tree and do alpha-beta pruning if possible
         * @param score
         * @param childMoves
         */
        public synchronized void childUpdate(int score, int[][] childMoves) {
            this.calculatedChildren++;
            if (this.symbol.equals(selfSymbol)) {
                // max
                if (score >= this.minOrMaxVal) {
                    this.minOrMaxVal = score;
                    this.optimalMoves = childMoves;
                }
                // if this.max >= parent.min, prune
                if (this.parent != null && this.minOrMaxVal >= this.parent.minOrMaxVal) {
                    this.pruneChildren();
                }
            } else {
                // min
                if (score <= this.minOrMaxVal) {
                    this.minOrMaxVal = score;
                    this.optimalMoves = childMoves;
                }
                // if this.min <= parent.max, prune
                if (this.parent != null && this.minOrMaxVal <= this.parent.minOrMaxVal) {
                    this.pruneChildren();
                }
            }

            if (this.calculatedChildren == this.children.size() && this.parent != null) {
                this.parent.childUpdate(this.minOrMaxVal, this.optimalMoves);
            }
        }

        /**
         * Evaluate the score of self for each node
         * @return
         */
        public int evaluate() {
            int wouldWinOrLose = this.checkWin();
            if ((wouldWinOrLose == 1 && this.parent.symbol.equals(selfSymbol)) || (wouldWinOrLose == -1 && this.symbol.equals(selfSymbol))) {
                return Integer.MAX_VALUE;
            } else if ((wouldWinOrLose == 1 && this.symbol.equals(selfSymbol)) || (wouldWinOrLose == -1 && this.parent.symbol.equals(selfSymbol))) {
                return Integer.MIN_VALUE;
            }

            int[] nodeScores = new int[2]; // score[0] = score of "O", score[1] = score of "X"
            int[][] fourDirection = { { -1, 0 }, { 0, -1 }, { -1, -1 }, { -1, 1 } };
            for (int i = 0; i < boardSize; i++) {
                for (int j = 0; j < boardSize; j++) {
                    // Go through board
                    int temp = this.getOnNodeBoard(i, j);
                    if (temp > 0) {
                        // Not empty
                        int currentIndex = temp - 1;
                        for (int dir = 0; dir < 4; dir++) {
                            int next = this.getOnNodeBoard(i - fourDirection[dir][0], j - fourDirection[dir][1]);
                            if (next != temp) {
                                // It is the end of a row, update score
                                int tempLen = this.getOnNodeBoardSum(i, j, dir);
                                if (tempLen > 1) {
                                    int lengthBeforeStart = 0, lengthAfterStop = 0;
                                    while (this.getOnNodeBoard(i + fourDirection[dir][0] * (tempLen + lengthBeforeStart), j + fourDirection[dir][1] * (tempLen + lengthBeforeStart)) == 0) {
                                        lengthBeforeStart++;
                                    }
                                    while (this.getOnNodeBoard(i - fourDirection[dir][0] * (1 + lengthAfterStop), j - fourDirection[dir][1] * (1 + lengthAfterStop)) == 0) {
                                        lengthAfterStop++;
                                    }

                                    if (lengthBeforeStart + lengthAfterStop + tempLen >= 6) {
                                        int before = this.getOnNodeBoard(i + fourDirection[dir][0] * tempLen, j + fourDirection[dir][1] * tempLen);
                                        if (before == 0 && next == 0) {
                                            // live
                                            nodeScores[currentIndex] += evalScore[tempLen - 1];
                                        } else if (before != 0 && next != 0) {
                                            // dead
                                            nodeScores[currentIndex] += 0;
                                        } else {
                                            // sleep
                                            // nodeScores[currentIndex] += evalScore[tempLen - 1] / 2;
                                            nodeScores[currentIndex] += evalScore[tempLen - 2];
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // If the next move belongs to you, then give you more score (potential benefits).
            // Otherwise give you a less score (potential threats).
            double coefficient;
            if (this.depth % 2 == 0) {
                coefficient = 1.2;
            } else {
                coefficient = 0.8;
            }
            if (selfSymbol.equals("O")) {
                return (int) (nodeScores[0] * coefficient - nodeScores[1]);
            } else {
                return (int) (nodeScores[1] * coefficient - nodeScores[0]);
            }
        }
    }

    /**
     * Multi-thread for searching
     */
    class ThreadSearch extends Thread {
        long startTime;

        public void setStartTime(long startTime) {
            this.startTime = startTime;
        }

        @Override
        public void run() {
            while ((long) (System.currentTimeMillis() / 1000) - this.startTime < TIMER) {
                Node tempLeaf;
                do {
                    tempLeaf = popSearchList();
                    if (tempLeaf == null) {
                        return;
                    }
                    prunedChildren++;
                } while (tempLeaf.pruned == true);

                prunedChildren--;
                // Node tempLeaf = popSearchList();
                // if (tempLeaf == null) {
                // 	return;
                // }
                int score = tempLeaf.evaluate();
                tempLeaf.parent.childUpdate(score, tempLeaf.newMoves);
            }
        }
    }
}