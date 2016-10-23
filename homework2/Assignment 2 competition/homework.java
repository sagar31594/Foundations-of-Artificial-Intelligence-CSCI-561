import java.util.ArrayList;
import java.io.FileWriter;
import java.io.RandomAccessFile;

class homework{

	static String MAXPlayer = "";
	static String MINPlayer = "";
	static int count = 0, prunecount = 0;

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
					if (isRaidPossible(agent, N, boardState,  pos) && isRaidPossible(getOpponent(agent), N, boardState,  pos) && !raid.contains(pos)) {
						raid.add(pos);
					}
					else {
						stake.add(pos);
					}
				}
			}
		}
		actions.add(raid);
		actions.add(stake);
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
		if (actionType == 1) {
			newBoardState[pos.get(0)][pos.get(1)] = new String(agent);
		}
		else {
			newBoardState[pos.get(0)][pos.get(1)] = new String(agent);
			newBoardState = raidSquares(agent, newBoardState, pos);
		}
		return newBoardState;
	}

	static double alphabetaMaxValue(String agent, int currentDepth, int depth, String [][]boardState, int [][]boardValues, double alpha, double beta) throws Exception{
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

	static double alphabetaMinValue(String agent, int currentDepth, int depth, String [][]boardState, int [][]boardValues, double alpha, double beta) throws Exception{
		if (terminalState(currentDepth, depth, boardState)) {
			return evaluateScore(boardState, boardValues);
		}
		double v = Double.POSITIVE_INFINITY;
		ArrayList<ArrayList<ArrayList<Integer>>> actions = getPossibleActions(agent, boardState);
		for (int i = 0; i < 2; i++) {
			ArrayList<ArrayList<Integer>> actionList = actions.get(i);
			int actionLength = actionList.size();
			for (int j = 0; j < actionLength; j++) {
				v = Math.min(v, alphabetaMaxValue(getOpponent(agent), currentDepth + 1, depth, generateSuccessorState(agent, boardState, i, actionList.get(j)), boardValues, alpha, beta));
				count++;
				if (v <= alpha) {
					prunecount++;
					return v;
				}
				beta = Math.min(beta, v);
			}
		}
		return v;
	}

	static void printOutput(String [][]boardState, int []chosenAction) throws Exception{
		FileWriter fw = new FileWriter("output.txt");
		int N = boardState.length;
		//System.out.println("\n");
		String output = "";
		int x = chosenAction[1];
		int y = chosenAction[2];
		String action = chosenAction[0] == 0 ? "Raid" : "Stake";
		boardState[x][y] = new String(MAXPlayer);
		if (chosenAction[0] == 0) {
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
		fw.write(output);
		fw.close();
	}

	static int getMaxMoves(String [][]boardState) {
		int N = boardState.length;
		int count = 0;
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				if(boardState[i][j].equalsIgnoreCase("."))
					count++;
			}
		}
		return count;
	}

	static int getDepth(String [][]boardState, double cpuTimeLeft) throws Exception{
		ArrayList<String> lines = new ArrayList<String>();
		RandomAccessFile f = new RandomAccessFile("calibrate.txt", "r");
		String line;
		while((line = f.readLine()) != null) {
			lines.add(line);
		}
		f.close();
		//List<String> lines = Files.readAllLines(Paths.get("calibrate.txt"), StandardCharsets.UTF_8);
		int N = lines.size();
		double cpuTime[] = new double[N];
		long nodesPerSecond[] = new long[N];
		//System.out.println();
		for (int i = 0; i < N; i++) {
			String values[] = lines.get(i).split(" ");
			cpuTime[i] = Double.parseDouble(values[0]);
			nodesPerSecond[i] = Long.parseLong(values[1]);
		}
		/*
		for (int i = 0; i < N; i++) {
			System.out.print(nodesPerSecond[i] + " ");
		}
		*/
		int maxMoves = getMaxMoves(boardState);
		double timeAllocatedPerMove = cpuTimeLeft / maxMoves;
		int index = 0;
		for (int i = N-1; i >= 0; i--) {
			if(timeAllocatedPerMove > cpuTime[i]) {
				index = i;
				break;
			}
		}
		//System.out.println("index: " + index);
		long total = 0;
		long product = maxMoves;
		long initialProduct = product;
		long statesThatCanBeExpanded = (long)(nodesPerSecond[index] * timeAllocatedPerMove);
		int depth = 0;
		/*
		while total < statesExpanded:
			total += product
			depth += 1
			product *= (initialProduct - depth)
		while True:
			total += product
			if total > statesExpanded:
				break
			depth += 1
			product *= (initialProduct - depth)
		*/
		//System.out.println("timeAllocatedPerMove: " + timeAllocatedPerMove);
		while(true) {
			total += product;
			depth++;
			if(total > statesThatCanBeExpanded)
				break;
			//depth++;
			product *= (initialProduct - depth);
			if (product <= 0) {
				break;
			}
		}	
		//System.out.println("timeAllocatedPerMove: " + timeAllocatedPerMove);
		//System.out.println("depth: " + depth);
		//System.out.println("total: " + total);
		//System.out.println("statesThatCanBeExpanded: " + statesThatCanBeExpanded);
		return depth;
	}

	public static void main(String[] args) throws Exception{
		//List<String> lines = Files.readAllLines(Paths.get("TestCasesHW2/Test10/inputplayer1.txt"), StandardCharsets.UTF_8);
		//System.out.println(lines);
		//List<String> lines = Files.readAllLines(Paths.get("input.txt"), StandardCharsets.UTF_8);
		ArrayList<String> lines = new ArrayList<String>();
		RandomAccessFile f = new RandomAccessFile("input.txt", "r");
		String line;
		while((line = f.readLine()) != null) {
			lines.add(line);
		}
		f.close();
		int N = Integer.parseInt(lines.get(0));
		//String mode = lines.get(1);
		lines.get(1);
		String player = lines.get(2);
		double cpuTimeLeft = Double.parseDouble(lines.get(3));
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
		//FileWriter fw = new FileWriter("outputplayer1.txt");
		int depth = getDepth(boardState, cpuTimeLeft);
		System.out.println("Alpha Beta Pruning");
		MAXPlayer = player;
		MINPlayer = getOpponent(player);
		long startTime = System.currentTimeMillis();
		double score = alphabetaMaxValue(player, 0, depth, boardState, boardValues, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY);
		//alphabetaMaxValue(player, 0, depth, boardState, boardValues, Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY);
		System.out.println(score);
		double diff = (System.currentTimeMillis() - startTime)/1000.0;
		System.out.println((System.currentTimeMillis() - startTime)/1000.0);
		System.out.println(cpuTimeLeft - diff);
		System.out.println("nodes expanded: " + count);
		System.out.println("pruned nodes: " + prunecount);

		//print2Darray(boardState);
		//print2Dintarray(boardValues);






	}
}