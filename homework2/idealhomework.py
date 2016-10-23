'''
a copy of homework.py in which the getPossibleActions function has been changed to take a particular position (x, y)
and it can be only one of the 2 actions: stake or raid.
also, while running alpha-beta, the raid actions have been considered before stake actions
'''

import copy
import time
'''
Global variables to keep track of MAX and Min nodes, initially both the variables will be undefined
'''
MAX, MIN = None, None
count1, count2, pruneCount, countRaid, countStake = 0, 0, 0, 0, 0
#chosenAction = None

def terminalState(currentDepth, depth, boardState):
	'''
	Helper method which helps takes in a boardState and returns whether it is a terminal state or not
	Arguments:
		currentDepth :- the current depth of the minimax tree
		depth :- the cutoff limit for the minimax tree
		boardState :- the current state of the board
	Returns:
		True if boardState is a terminal state, otherwise False
	Details:
		A given boardState is a terminal state if there are no vacant positions i.e. it doesn't contain a single '.'
		or if the current depth of the minimax tree has reached its cutoff limit
	'''
	if currentDepth == depth:
		return True
	N = len(boardState)
	#print N
	#print boardState
	for x in xrange(N):
		for y in xrange(N):
			#print x, ' ', y
			if boardState[x][y] == '.':
				return False
	return True

def evaluateScore(boardState, boardValues):
	'''
	Helper method which helps in calculating the score of a given boardState
	Arguments:
		boardState :- the current state of the board
		boardValues :- contains the score for each cell on the board
	Returns:
		score :- score of the current boardState
	Details:
		score represents the difference between the sum of values of cells occupied by the player and 
		the sum of values of cells occupied by the opponent
	'''
	score = 0
	global MAX, MIN
	length = len(boardState)
	for x in xrange(length):
		for y in xrange(length):
			if boardState[x][y] == MAX:
				score += boardValues[x][y]
			elif boardState[x][y] == MIN:
				score -= boardValues[x][y]
	#print boardState
	#print score
	#print '\n\n'
	return score

def checkBounds(x, y, length):
	'''
	helper method which checks if the given location of the cell is within the bounds of the boardState
	Arguments:
		x :- row of the board
		y :- column of the board
		length :- max length and column of the board
	Returns:
		True if x and y are within the bounds, otherwise returns False
	Details:
		x and y should lie within 0 and length-1 (both inclusive)
	'''
	return x >= 0 and x < length and y >= 0 and y < length

def getEmptyAdjacentPositions(agent, boardState, x, y):
	'''
	Helper method which finds empty cells which are adjacent to a particular cell
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
		boardState :- the current state of the board
		x :- row of the board
		y :- column of the board
	Returns:
		positions :- a list which contains the positions of the vacant cells which are adjacent to a particular cell
	Details:
		there could be at the most 4 adjacent positions to a given cell with the coordinates (x, y-1), (x-1, y), (x, y+1), (x+1, y)
	'''
	positions = list()
	length = len(boardState)
	if checkBounds(x, y-1, length) and boardState[x][y-1] == '.':
		positions.append((x, y-1))
	if checkBounds(x-1, y, length) and boardState[x-1][y] == '.':
		positions.append((x-1, y))
	if checkBounds(x, y+1, length) and boardState[x][y+1] == '.':
		positions.append((x, y+1))
	if checkBounds(x+1, y, length) and boardState[x+1][y] == '.':
		positions.append((x+1, y))
	return positions	

def isRaidPossible(agent, length, boardState, (x, y)):
	'''
	Helper method which determines whether the 'raid' operation is possible or not
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
		length :- max length and column of the board
		boardState :- the current state of the board
		(x, y) :- position of the considered cell
	Returns:
		True if raid is possible, otherwise False
	Details:
		it considers the adjacent positions to the given cell which could be at the most 4 positions
		it first makes sure that the adjacent position is whithin the limits of the board and then
		checks to see if the adjacent cell is occupied by the agent	
	'''
	#opponent = getOpponent(agent)
	if checkBounds(x, y-1, length) and boardState[x][y-1] == agent:
		return True
	if checkBounds(x-1, y, length) and boardState[x-1][y] == agent:
		return True
	if checkBounds(x, y+1, length) and boardState[x][y+1] == agent:
		return True
	if checkBounds(x+1, y, length) and boardState[x+1][y] == agent:
		return True
	return False


def raidSquares(agent, boardState, (x, y)):
	'''
	Helper method which changes the current boardState by raiding the opponent cells
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
		boardState :- the current state of the board
		(x, y) :- position of the considered cell
	Returns:
		boardState :- the updated boardState
	Details:
		it considers the adjacent positions to the given cell which could be at the most 4 positions
		it first makes sure that the adjacent position is whithin the limits of the board and then
		checks to see if the adjacent cell is occupied by the opponent
		if it is occupied by the opponent then it raids that particular cell
	'''
	opponent = getOpponent(agent)
	length = len(boardState)
	if checkBounds(x, y-1, length) and boardState[x][y-1] == opponent:
		boardState[x][y-1] = agent
	if checkBounds(x-1, y, length) and boardState[x-1][y] == opponent:
		boardState[x-1][y] = agent
	if checkBounds(x, y+1, length) and boardState[x][y+1] == opponent:
		boardState[x][y+1] = agent
	if checkBounds(x+1, y, length) and boardState[x+1][y] == opponent:
		boardState[x+1][y] = agent
	return boardState

def getPossibleActions(agent, boardState):
	'''
	Helper mehod which finds the possible actions that the agent can take given the current boardState
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
		boardState :- the current state of the board
	Returns:
		actions :- the list of actions that the agent can take in this turn
	Details:
		actions are of 2 types 'Stake' and 'Raid'
		stake action can be performed on every unoccupied cell while raid action can be performed only if 
		there is an agent cell beside it and playing that action actually helps in raiding atleast one 
		opponent cell
		the last condition is important because otherwise it is as good as a stake operation which has been
		already accounted for
	'''
	actions = dict()
	actions['Stake'] = []
	actions['Raid'] = []
	length = len(boardState)
	for x in xrange(length):
		for y in xrange(length):
			if boardState[x][y] == '.':
				actions['Stake'].append((x, y))
				if isRaidPossible(agent, length, boardState, (x, y)) and isRaidPossible(getOpponent(agent), length, boardState, (x, y)) and (x, y) not in actions['Raid']:
					actions['Raid'].append((x, y))
	return actions

def getOpponent(agent):
	'''
	Helper method which gives us the opponent for a particular agent
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
	Returns:
		'X' if the current agent is 'O', otherwise it returns 'O'
	'''
	return 'X' if agent == 'O' else 'O'

def generateSuccessorState(agent, boardState, actionType, action):
	'''
	Helper method which generates the next state given the current state and the action to be performed
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
		boardState :- the current state of the board
		actionType :- the type of action to be performed i.e. 'Stake' or 'Raid'
		action :- the position at which the type of action is to be performed
	Returns:
		newBoardState :- the new board state obtained after operating the action on the current board state
	'''
	newBoardState = copy.deepcopy(boardState)
	if actionType == 'Stake':
		newBoardState[action[0]][action[1]] = agent
	else:
		newBoardState[action[0]][action[1]] = agent
		newBoardState = raidSquares(agent, newBoardState, action)	
	#print '\n\n'
	#print newBoardState
	#print action, ' ', actionType
	return newBoardState	

def maxValue(agent, currentDepth, depth, boardState, boardValues):
	'''
	the max part of the Minimax Algorithm
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
		currentDepth :- the current depth in the minimax tree
		depth :- the cutoff limit for the minimax tree
		boardState :- the current state of the board
		boardValues :- contains the score for each cell on the board
	Returns:
		one of the two things:
			v :- the max evaluation score for this node in the minimax tree
			chosenAction :- if it's the first node in the minimax tree, then it returns a tuple which contains
				the type of action to take and the position where the action needs to be performed which will 
				maximize the score of our max agent
	'''
	global count1, countRaid, countStake
	#print "\n\nCurrent depth: ", currentDepth
	if terminalState(currentDepth, depth, boardState):
		return evaluateScore(boardState, boardValues)
	v = -float('inf')
	vPrev = v
	actions = getPossibleActions(agent, boardState)
	actionTypes = ['Stake', 'Raid']
	chosenAction = None
	'''
	print '\n'
	print 'depth ', currentDepth
	print 'current boardState'
	print boardState
	print 'actions: ', actions
	'''
	countStake += len(actions['Stake'])
	countRaid += len(actions['Raid'])
	for actionType in actionTypes:
		for a in actions[actionType]:
			count1+= 1
			v = max(v, minValue(getOpponent(agent), currentDepth + 1, depth, generateSuccessorState(agent, boardState, actionType, a), boardValues))
			if vPrev != v:
				vPrev = v
				chosenAction = (actionType, a)
	#print '\nmax actions for depth: ', currentDepth, '\n', actions, '\n'							
	if currentDepth == 0:
		#print actions
		print 'vPrev ', vPrev
		return chosenAction
	return v				

def minValue(agent, currentDepth, depth, boardState, boardValues):
	'''
	the min part of the Minimax Algorithm
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
		currentDepth :- the current depth in the minimax tree
		depth :- the cutoff limit for the minimax tree
		boardState :- the current state of the board
		boardValues :- contains the score for each cell on the board
	Returns:
		v :- the minimum evaluation score for this node in the minimax tree
	'''
	global count1, countRaid, countStake
	#print "\n\nCurrent depth: ", currentDepth
	if terminalState(currentDepth, depth, boardState):
		return evaluateScore(boardState, boardValues)
	v = float('inf')
	#print 'min agent ', agent
	actions = getPossibleActions(agent, boardState)
	actionTypes = ['Stake', 'Raid']
	#chosenAction = None
	'''
	print '\n'
	print 'depth ', currentDepth
	print 'current boardState'
	print boardState
	print 'actions: ', actions
	'''
	countStake += len(actions['Stake'])
	countRaid += len(actions['Raid'])
	for actionType in actionTypes:
		for a in actions[actionType]:
			count1 += 1
			v = min(v, maxValue(getOpponent(agent), currentDepth + 1, depth, generateSuccessorState(agent, boardState, actionType, a), boardValues))

			#if vPrev != v:
			#	vPrev = v
				#chosenAction = (actionType, a)
	#if currentDepth == 0:
	#	return chosenAction
	#print '\nmin actions for depth: ', currentDepth, '\n', actions, '\n'
	return v				

def alphabetaMaxValue(agent, currentDepth, depth, boardState, boardValues, alpha, beta):
	'''
	the max part of the Minimax Algorithm which also employs alphabeta pruning
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
		currentDepth :- the current depth in the minimax tree
		depth :- the cutoff limit for the minimax tree
		boardState :- the current state of the board
		boardValues :- contains the score for each cell on the board
		alpha :- the max score till now on the path to the root
		beta :- the min score till now on the path to the root
	Returns:
		one of the two things:
			v :- the max evaluation score for this node in the minimax tree
			chosenAction :- if it's the first node in the minimax tree, then it returns a tuple which contains
				the type of action to take and the position where the action needs to be performed which will 
				maximize the score of our max agent
	'''
	global count2, pruneCount
	if terminalState(currentDepth, depth, boardState):
		return evaluateScore(boardState, boardValues)
	v = -float('inf')
	vPrev = v
	actions = getPossibleActions(agent, boardState)
	actionTypes = ['Stake', 'Raid']
	#actionTypes = ['Raid', 'Stake']
	#print actions
	#print 'depth ', depth
	#print 'current boardState'
	#print boardState
	chosenAction = None
	for actionType in actionTypes:
		for a in actions[actionType]:
			v = max(v, alphabetaMinValue(getOpponent(agent), currentDepth + 1, depth, generateSuccessorState(agent, boardState, actionType, a), boardValues, alpha, beta))
			count2 += 1
			if vPrev != v:
				vPrev = v
				chosenAction = (actionType, a)
			if v >= beta:
				#print "pruned"
				pruneCount += 1
				return v
			alpha = max(alpha, v)
	#print '\nmax actions for depth: ', currentDepth, '\n', actions, '\n'				
	if currentDepth == 0:
		#print actions
		print 'vPrev ', vPrev
		return chosenAction
	return v				

def alphabetaMinValue(agent, currentDepth, depth, boardState, boardValues, alpha, beta):
	'''
	the min part of the Minimax Algorithm which also employs alphabeta pruning
	Arguments:
		agent :- the game playing agent for the current turn, could be either 'X' or 'O'
		currentDepth :- the current depth in the minimax tree
		depth :- the cutoff limit for the minimax tree
		boardState :- the current state of the board
		boardValues :- contains the score for each cell on the board
		alpha :- the max score till now on the path to the root
		beta :- the min score till now on the path to the root
	Returns:	
		v :- the minimum evaluation score for this node in the minimax tree
	'''
	global count2, pruneCount
	if terminalState(currentDepth, depth, boardState):
		return evaluateScore(boardState, boardValues)
	v = float('inf')
	#print 'min agent ', agent
	actions = getPossibleActions(agent, boardState)
	actionTypes = ['Stake', 'Raid']
	#print 'depth ', depth
	#print 'current boardState'
	#print boardState
	#actionTypes = ['Raid', 'Stake']
	#chosenAction = None
	for actionType in actionTypes:
		for a in actions[actionType]:
			v = min(v, alphabetaMaxValue(getOpponent(agent), currentDepth + 1, depth, generateSuccessorState(agent, boardState, actionType, a), boardValues, alpha, beta))
			count2 += 1
			if v <= alpha:
				#print "pruned"
				pruneCount += 1
				return v
			beta = min(beta, v)	
			#if vPrev != v:
			#	vPrev = v
				#chosenAction = (actionType, a)
	#if currentDepth == 0:
	#	return chosenAction
	#print '\nmin actions for depth: ', currentDepth, '\n', actions, '\n'
	return v				

def printOutput(boardState, chosenAction):
	'''
	Helper method to print the final solution
	Arguments:
		boardState :- the current state of the board
		chosenAction :- a two element tuple which contains the type of action to be taken and the position where
			the action needs to be performed
	Returns:
		output :- a string which contains the final solution to be printed
	'''
	print '\n\n\n\n'
	global MAX, MIN
	(x, y) = chosenAction[1]
	output = ''
	boardState[x][y] = MAX
	if chosenAction[0] == 'Raid':
		boardState = raidSquares(MAX, boardState, (x, y))
	output += chr(y+65) + str(x+1) + ' ' + chosenAction[0]
	for i in boardState:
		output += '\n' + ''.join(i)
	print output		

def main():
	'''
	Takes input from the file 'input.txt' which is in the following format and saves them in the following variables:
	N 							:- <N> which is the length and column of N*N board
	mode 						:- <MODE> which could be either 'MINIMAX' or 'ALPHABETA'
	player	 					:- <YOUPLAY> which is the symbol that you play which could be either 'X' or 'O'
	depth 						:- <DEPTH> which is the depth of the search tree
	boardValues (list of lists)	:- <... CELL VALUES ...> which represents the value of each N*N cells
	boardState 					:- <... BOARD STATE ...> which represents the current state of the board
	'''
	global MAX, MIN
	f = open('input.txt', 'r')
	N = int(f.readline())
	mode = f.readline().rstrip()
	player = f.readline().rstrip()
	depth = int(f.readline())
	#print depth
	boardValues = list()
	boardState = list()
	for x in xrange(N):
		boardValues.append(map(int, f.readline().rstrip().split()))
	for x in xrange(N):
		boardState.append(list(f.readline().rstrip()))
	f.close()
	enemy = getOpponent(player)
	MAX, MIN = player, enemy
	newBoardState = copy.deepcopy(boardState)
	#print mode
	#setAgents(player, opponent)
	#player = GameAgent(youplay, 'MAX', N, boardState, boardValues)
	#opponent = GameAgent('X' if youplay == 'O' else 'O', 'MIN', N, boardState, boardValues)
	global count1, countRaid
	if mode == 'MINIMAX':
		startTime = time.time()
		print '\nMinimax Algorithm'
		chosenAction = maxValue(player, 0, depth, boardState, boardValues)
		print 'chosenAction ', chosenAction
		printOutput(boardState, chosenAction)
		print "states expanded", count1
		print 'raid count: ', countRaid
		print 'stake count: ', countStake
		print "Time: ", time.time() - startTime
	
	#print '\n\nboardState'
	#print boardState
	else:
		startTime = time.time()
		print '\nAlpha Beta pruning'
		chosenAction = alphabetaMaxValue(player, 0, depth, newBoardState, boardValues, -float('inf'), float('inf'))
		print 'chosenAction ', chosenAction
		printOutput(newBoardState, chosenAction)
		print "Time: ", time.time() - startTime
		global count2, pruneCount
		print "states expanded: ", count2, ' ', pruneCount
	#board = [['X', '.', 'X'], ['.', 'O', '.'], ['.', '.', '.']]
	#print '\n\n'
	#print getPossibleActions('X', board)
main()