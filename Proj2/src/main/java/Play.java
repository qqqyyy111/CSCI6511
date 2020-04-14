import java.util.HashMap;
import java.util.Scanner;

import com.alibaba.fastjson.*;

public class Play {
    public static void main(String[] args) throws Exception {
        Scanner myObj = new Scanner(System.in);

        System.out.println("Have you already created a game? (Y/N)");
        String yn = myObj.nextLine();

        if (yn.toLowerCase().equals("y")) {
            System.out.println("Please enter the game id, board size, target and priority of our team (1 or 2) to join in (each element separated by space): ");
            String[] inputSplit = myObj.nextLine().split(" ");
            String gameId = inputSplit[0].trim();
            int boardSize = Integer.parseInt(inputSplit[1]), target = Integer.parseInt(inputSplit[2]), priority = Integer.parseInt(inputSplit[3]);
            if (priority == 1) {
                Game game = new Game(Integer.parseInt(gameId), boardSize, target, "O");
                game.start();
            } else if (priority == 2) {
                Game game = new Game(Integer.parseInt(gameId), boardSize, target, "X");
                game.start();
            }
        } else if (yn.toLowerCase().equals("n")) {
            System.out.println("Please enter the team id of opponent, board size, target and priority of our team (1 or 2) to create a game (each element separated by space): ");
            String[] inputSplit = myObj.nextLine().split(" ");
            String opponentTeamId = inputSplit[0].trim();
            int boardSize = Integer.parseInt(inputSplit[1]), target = Integer.parseInt(inputSplit[2]), priority = Integer.parseInt(inputSplit[3]);
            int gameId = createGame(opponentTeamId, boardSize, target, priority);
            if (priority == 1) {
                Game game = new Game(gameId, boardSize, target, "O");
                game.start();
            } else if (priority == 2) {
                Game game = new Game(gameId, boardSize, target, "X");
                game.start();
            }
        }
    }


    /**
     * Create a game with API
     * @param opponentTeamId
     * @param boardSize
     * @param target
     * @return
     * @throws Exception
     */
    public static int createGame(String opponentTeamId, int boardSize, int target, int priority) throws Exception {
        Requests requests = new Requests();
        HashMap<String, String> params = new HashMap<String, String>();
        params.put("type", "game");
        if (priority == 1) {
            // Move first
            params.put("teamId1", "1197");
            params.put("teamId2", opponentTeamId);
        } else if (priority == 2) {
            // Move second
            params.put("teamId1", opponentTeamId);
            params.put("teamId2", "1197");
        }
        params.put("gameType", "TTT");
        params.put("boardSize", Integer.toString(boardSize));
        params.put("target", Integer.toString(target));
        String result = requests.post(params);

        JSONObject parsedResult = JSON.parseObject(result);
        if (!parsedResult.getString("code").equals("OK")) {
            throw new Exception("ERROR in game creation: " + result);
        } else {
            System.out.println("New game " + Integer.toString(parsedResult.getInteger("gameId")));
            return parsedResult.getInteger("gameId");
        }
    }
}