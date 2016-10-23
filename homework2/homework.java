import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.ArrayList;

class idealhomework{

	static String MAXPlayer = "";
	static String MINPlayer = "";
	static int count = 0, prunecount = 0, count1 = 0, count3 = 0;

	static void print2Darray(String [][]arr) {
		int N = arr.length;
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				System.out.print(arr[i][j] + " ");
			}
			System.out.println();
		}
	}
	static void print2Dintarray(int [][]arr) {
		int N = arr.length;
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				System.out.print(arr[i][j] + " ");
			}
			System.out.println();
		}
	}

	static String getOpponent(String agent) {
		return agent.equalsIgnoreCase("O") ? "X" : "O";
	}

	static boolean terminalState(int currentDepth, int depth, String [][]boardState) {
		if (currentDepth == depth) {
			return true;
		}
		int N = boardState.length;
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				if (boardState[i][j].equalsIgnoreCase(".")) {
					return false;
				}
			}
		}
		return true;
	}

	static int evaluateScore(String [][]boardState, int [][]boardValues) {
		int score = 0;
		int N = boardState.length;
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				if (boardState[i][j].equalsIgnoreCase(MAXPlayer)) {
					score += boardValues[i][j];
				}
				else if (boardState[i][j].equalsIgnoreCase(MINPlayer)) {
					score -= boardValues[i][j];
				}
			}
		}
		return score;
	}

	static boolean isRaidPossible(String agent, int N, String [][]boardState, ArrayList<Integer> pos) {
		if (checkBounds(pos.get(0), pos.get(1)-1, N) && boardState[pos.get(0)][pos.get(1)-1].equalsIgnoreCase(agent)) {
			return true;
		}
		if (checkBounds(pos.get(0)-1, pos.get(1), N) && boardState[pos.get(0)-1][pos.get(1)].equalsIgnoreCase(agent)) {
			return true;
		}
		if (checkBounds(pos.get(0), pos.get(1)+1, N) && boardState[pos.get(0)][pos.get(1)+1].equalsIgnoreCase(agent)) {
			return true;
		}
		if (checkBounds(pos.get(0)+1, pos.get(1), N) && boardState[pos.get(0)+1][pos.get(1)].equalsIgnoreCase(agent)) {
			return true;
		}
		return false;
	}

	static ArrayList<ArrayList<ArrayList<Integer>>> getPossibleActions(String agent, String [][]boardState) {
		ArrayList<ArrayList<ArrayList<Integer>>> actions = new ArrayList<ArrayList<ArrayList<Integer>>>();
		ArrayList<ArrayList<Integer>> stake = new ArrayList<ArrayList<Integer>>();
		ArrayList<ArrayList<Integer>> raid = new ArrayList<ArrayList<Integer>>();
		int N = boardState.length;
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				if (boardState[i][j].equalsIgnoreCase(".")) {
					ArrayList<Integer> pos = new ArrayList<Integer>();
					pos.add(new Integer(i));
					pos.add(new Integer(j));
					stake.add(pos);
					if (isRaidPossible(agent, N, boardState,  pos) && isRaidPossible(getOpponent(agent), N, boardState,  pos)) {
						raid.add(pos);
					}
				}
			}
		}
		actions.add(stake);
		actions.add(raid);
		count3 += stake.size();
		count3 += raid.size();
		return actions;

	}

	static boolean checkBounds(int x, int y, int N) {
		return x >= 0 && x < N && y >= 0 && y < N;
	}

	static String[][] raidSquares(String agent, String [][]boardState, ArrayList<Integer> pos) {
		String opponent = getOpponent(agent);
		int N = boardState.length;
		if (checkBounds(pos.get(0), pos.get(1)-1, N) && boardState[pos.get(0)][pos.get(1)-1].equalsIgnoreCase(opponent)) {
			boardState[pos.get(0)][pos.get(1)-1] = new String(agent);
		}
		if (checkBounds(pos.get(0)-1, pos.get(1), N) && boardState[pos.get(0)-1][pos.get(1)].equalsIgnoreCase(opponent)) {
			boardState[pos.get(0)-1][pos.get(1)] = new String(agent);
		}
		if (checkBounds(pos.get(0), pos.get(1)+1, N) && boardState[pos.get(0)][pos.get(1)+1].equalsIgnoreCase(opponent)) {
			boardState[pos.get(0)][pos.get(1)+1] = new String(agent);
		}
		if (checkBounds(pos.get(0)+1, pos.get(1), N) && boardState[pos.get(0)+1][pos.get(1)].equalsIgnoreCase(opponent)) {
			boardState[pos.get(0)+1][pos.get(1)] = new String(agent);
		}
		return boardState;
	}

	static String[][] generateSuccessorState(String agent, String [][]boardState, int actionType, ArrayList<Integer> pos) {
		int N = boardState.length;
		String [][]newBoardState = new String[N][N];
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				newBoardState[i][j] = new String(boardState[i][j]);
			}
		}
		if (actionType == 0) {
			newBoardState[pos.get(0)][pos.get(1)] = new String(agent);
		}
		else {
			newBoardState[pos.get(0)][pos.get(1)] = new String(agent);
			newBoardState = raidSquares(agent, newBoardState, pos);
		}
		return newBoardState;
	}

	static double alphabetaMaxValue(String agent, int currentDepth, int depth, String [][]boardState, int [][]boardValues, double alpha, double beta) {
		if (terminalState(currentDepth, depth, boardState)) {
			return evaluateScore(boardState, boardValues);
		}
		double v = Double.NEGATIVE_INFINITY;
		double vPrev = v;
		ArrayList<ArrayList<ArrayList<Integer>>> actions = getPossibleActions(agent, boardState);
		//count3 += actions.size();
		int chosenAction[] = {0, 0, 0};
		for (int i = 0; i < 2; i++) {
			ArrayList<ArrayList<Integer>> actionList = actions.get(i);
			int actionLength = actionList.size();
			//count3 += actionLength;
			for (int j = 0; j < actionLength; j++) {
				v = Math.max(v, alphabetaMinValue(getOpponent(agent), currentDepth + 1, depth, generateSuccessorState(agent, boardState, i, actionList.get(j)), boardValues, alpha, beta));
				count++;
				if (vPrev != v) {
					vPrev = v;
					chosenAction[0] = i;
					chosenAction[1] = actionList.get(j).get(0);
					chosenAction[2] = actionList.get(j).get(1);
				}
				if (v >= beta) {
					prunecount++;
					return v;
				}
				alpha = Math.max(alpha, v);
			}
		}
		if (currentDepth == 0) {
			printOutput(boardState, chosenAction);
		}
		return v;
	}

	static double alphabetaMinValue(String agent, int currentDepth, int depth, String [][]boardState, int [][]boardValues, double alpha, double beta) {
		if (terminalState(currentDepth, depth, boardState)) {
			return evaluateScore(boardState, boardValues);
		}
		double v = Double.POSITIVE_INFINITY;
		ArrayList<ArrayList<ArrayList<Integer>>> actions = getPossibleActions(agent, boardState);
		//count3 += actions.size();
		for (int i = 0; i < 2; i++) {
			ArrayList<ArrayList<Integer>> actionList = actions.get(i);
			int actionLength = actionList.size();
			//count3 += actionLength;
			for (int j = 0; j < actionLength; j++) {
				v = Math.min(v, alphabetaMaxValue(getOpponent(agent), currentDepth + 1, depth, generateSuccessorState(agent, boardState, i, actionList.get(j)), boardValues, alpha, beta));
				count++;
				if (v <= alpha) {
					//prunecount++;
					return v;
				}
				beta = Math.min(beta, v);
			}
		}
		return v;
	}

	static double maxValue(String agent, int currentDepth, int depth, String [][]boardState, int [][]boardValues) {
		if (terminalState(currentDepth, depth, boardState)) {
			return evaluateScore(boardState, boardValues);
		}
		double v = Double.NEGATIVE_INFINITY;
		double vPrev = v;
		ArrayList<ArrayList<ArrayList<Integer>>> actions = getPossibleActions(agent, boardState);
		int chosenAction[] = {0, 0, 0};
		for (int i = 0; i < 2; i++) {
			ArrayList<ArrayList<Integer>> actionList = actions.get(i);
			int actionLength = actionList.size();
			for (int j = 0; j < actionLength; j++) {
				v = Math.max(v, minValue(getOpponent(agent), currentDepth + 1, depth, generateSuccessorState(agent, boardState, i, actionList.get(j)), boardValues));
				count1++;
				if (vPrev != v) {
					vPrev = v;
					chosenAction[0] = i;
					chosenAction[1] = actionList.get(j).get(0);
					chosenAction[2] = actionList.get(j).get(1);
				}
			}
		}
		if (currentDepth == 0) {
			printOutput(boardState, chosenAction);
		}
		return v;
	}

	static double minValue(String agent, int currentDepth, int depth, String [][]boardState, int [][]boardValues) {
		if (terminalState(currentDepth, depth, boardState)) {
			return evaluateScore(boardState, boardValues);
		}
		double v = Double.POSITIVE_INFINITY;
		ArrayList<ArrayList<ArrayList<Integer>>> actions = getPossibleActions(agent, boardState);
		for (int i = 0; i < 2; i++) {
			ArrayList<ArrayList<Integer>> actionList = actions.get(i);
			int actionLength = actionList.size();
			for (int j = 0; j < actionLength; j++) {
				v = Math.min(v, maxValue(getOpponent(agent), currentDepth + 1, depth, generateSuccessorState(agent, boardState, i, actionList.get(j)), boardValues));
				count1++;
			}
		}
		return v;
	}

	static void printOutput(String [][]boardState, int []chosenAction) {
		int N = boardState.length;
		System.out.println("\n");
		String output = "";
		int x = chosenAction[1];
		int y = chosenAction[2];
		String action = chosenAction[0] == 1 ? "Raid" : "Stake";
		boardState[x][y] = new String(MAXPlayer);
		if (chosenAction[0] == 1) {
			ArrayList<Integer> pos = new ArrayList<Integer>();
			pos.add(new Integer(x));
			pos.add(new Integer(y));
			boardState = raidSquares(MAXPlayer, boardState, pos);
		}
		output += String.valueOf((char)(y+65)) + String.valueOf(x+1) + " " + action;
		for (int i = 0; i < N; i++) {
			output += "\n";
			for (int j = 0; j < N; j++) {
				output += boardState[i][j];
			}
		}
		System.out.println(output);
	}

	public static void main(String[] args) throws Exception{
		//List<String> lines = Files.readAllLines(Paths.get("TestCasesHW2/Test10/input.txt"), StandardCharsets.UTF_8);
		List<String> lines = Files.readAllLines(Paths.get("input1.txt"), StandardCharsets.UTF_8);
		//System.out.println(lines);
		int N = Integer.parseInt(lines.get(0));
		String mode = lines.get(1);
		String player = lines.get(2);
		int depth = Integer.parseInt(lines.get(3));
		int boardValues[][] = new int[N][N];
		String boardState[][] = new String[N][N];
		for (int i = 0; i < N; i++) {
			String values[] = lines.get(i+4).split(" ");
			for (int j = 0; j < N; j++) {
				boardValues[i][j] = Integer.parseInt(values[j]);
			}
		}
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				boardState[i][j] = String.valueOf(lines.get(i+N+4).charAt(j));
			}
		}
		String [][]newBoardState = new String[N][N];
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				newBoardState[i][j] = new String(boardState[i][j]);
			}
		}
		MAXPlayer = player;
		MINPlayer = getOpponent(player);
		double score;
		long startTime;
		if (mode.equalsIgnoreCase("MINIMAX")) {
			System.out.println("Minimax");
			startTime = System.currentTimeMillis();
			score = maxValue(player, 0, depth, boardState, boardValues);
			System.out.println(score);
			System.out.println((System.currentTimeMillis() - startTime)/1000.0);
			System.out.println("nodes expanded: " + count1);	
		}
		else {
			System.out.println("Alpha Beta Pruning");
			startTime = System.currentTimeMillis();
			score = alphabetaMaxValue(player, 0, depth, newBoardState, boardValues, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY);
			System.out.println(score);
			System.out.println((System.currentTimeMillis() - startTime)/1000.0);
			System.out.println("nodes expanded: " + count);
			System.out.println("pruned nodes: " + prunecount);
		}
		System.out.println("new actions: " + count3);
		//print2Darray(boardState);
		//print2Dintarray(boardValues);






	}
}
