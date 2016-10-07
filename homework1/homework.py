import heapq

class PriorityQueue:
	'''
	Data Structure to hold nodes such that the one with the lowest distance is removed first
	Members:
		self.pq :- 	the list which holds tuples of the form (distance, self.counter, node) 
					where distance is the accumulated distance till now and node is the state with which the distance is associated
		self.counter :- used in case of breaking ties due to same distance. It starts from zero and is icremented on every insertion.
						Thus, the one which was inserted earlier (with the lowest self.counter value) will be removed 
						if there are 2 or more nodes with same distance.
	'''
	def __init__(self):
		self.pq = []
		self.counter = 0

	def insert(self, distance, node):
		'''
		inserts the tuple (distance, self.counter, node) in the PriorityQueue self.pq
		'''
		heapq.heappush(self.pq, (distance, self.counter, node))
		self.counter += 1

	def delete(self):
		'''
		deletes and removes the tuple with the minimum distance. In case of ties, self.counter is used. The one with the lowest counter
		will be returned i.e. the one which was inserted earlier.
		'''
		distance, _, node = heapq.heappop(self.pq)
		return distance, node

	def length(self):
		'''
		returns the length of the PriorityQueue
		'''
		return len(self.pq)	

	def findOpenNodes(self):
		'''
		returns the node names which are present in the PriorityQueue
		'''
		return [x[2] for x in self.pq]

	def replaceDecision(self, node, cost, parent, traceParentsWithCost):
		'''
		It makes a decision whether to replace a node on the basis of its associated distance in the PriorityQueue 
		and the distance of the same node which was newly generated in the caller function.
		It first finds the node with which the distance is to be compared.
		If the new distance is less than the present distance, the node is first removed from the PriorityQueue and 
		the new distance and the node are inserted. This operation changes the sorting in the array and that is why, 
		we need to call the heapify method to sort the PriorityQueue once again.
		The last step is to update the traceParentsWithCost array to reflect this change
		'''
		for presentNode in self.pq:
			if presentNode[2] == node:
				if cost < presentNode[0]:
					self.pq.remove(presentNode)
					self.insert(cost, node)
					heapq.heapify(self.pq)
					traceParentsWithCost[node] = (parent, cost)
					break

	def printqueue(self):
		print self.pq				

def getSolution(traceParentsWithCost, state):
	'''
	Helper method to find the correct order of states to be travelled from the startState to the goalState
	Arguments:
		traceParentsWithCost :- keeps track of the parents of every generated node along with the associated cost
		state :- the latest state that was expanded during search
	Returns:
		solution :- a string which contains a series of nodes along with the corresponding accumulated cost from the startState 
		for each node
	Details:
		Backtracks using the keys stored in the dictionary which are the states that were expanded while searching
		Forms a string in the format that is required to be output in the file
		Also appends the startState  with cost = 0 at the beginning of the list after the while loop is completed
	'''
	solution = ''
	temp = state
	while traceParentsWithCost.has_key(temp):
		parent, cost = traceParentsWithCost[temp]
		solution = '\n' + temp + ' ' + str(cost) + solution
		temp = parent
	solution = temp + ' 0' + solution
	return solution	

def getAstarSolution(traceParentsWithCost, state, sundayTrafficLines):
	'''
	Helper method to find the correct order of states to be travelled from the startState to the goalState for A* search algorithm
	Arguments:
		traceParentsWithCost :- keeps track of the parents of every generated node along with the associated cost
		state :- the latest state that was expanded during search
		sundayTrafficLines :- the heuristic function for this problem
	Returns:
		solution :- a string which contains a series of nodes along with the corresponding accumulated cost from the startState 
		for each node
	Details:
		Backtracks using the keys stored in the dictionary which are the states that were expanded while searching
		Forms a string in the format that is required to be output in the file
		Also appends the startState  with cost = 0 at the beginning of the list after the while loop is completed
	'''
	solution = ''
	temp = state
	while traceParentsWithCost.has_key(temp):
		parent, cost = traceParentsWithCost[temp]
		solution = '\n' + temp + ' ' + str(cost-sundayTrafficLines[temp]) + solution
		temp = parent
	solution = temp + ' 0' + solution
	return solution	

def bfs(startState, goalState, trafficLines):
	'''
	Implements Breadth First Search to find the shortest path from startState to goalState using trafficLines
	Arguments:
		startState :- the start state of the path
		goalState :- the destination of the path
		trafficLines :- the edges in the graph along with the associated costs
	Returns:
		solution :- a string which contains a series of nodes along with the corresponding accumulated cost from the startState 
		for each node
	Details:
		Returns the solution directly if startState and goalState are the same
		Otherwise creates a list 'frontier' which is a FIFO queue to store newly generated states (initially startState) along with the
		accumulated cost till that state and a list 'explored' which handles the already explored states
		It keeps track of the depth traversed using the variable 'cost'
		It keeps track of the parents of every generated node along with the associated cost using the dictionary traceParentsWithCost
	'''
	cost = 0
	if startState == goalState:
		return startState + ' ' + str(cost)
	frontier = list()
	explored = list()
	traceParentsWithCost = dict()
	frontier.append((startState, cost))
	while len(frontier) != 0:
		node, cost = frontier.pop(0)
		cost += 1
		explored.append(node)
		'''
		had to do this because frontier contains two-element tuples (node, cost) so we can't check if the first element is in a list of tuples 
		and it didn't work on the file 'input3.txt'
		example: frontier: [('C', 1), ('D', 2)] and we are checking if 'D' not in frontier ('D' is there in frontier but it will obviously return false), 
		you just can't check if an element is in a list of tuples
		so, we have to make a temp list of openNodes which has all the nodes from frontier
		'''
		openNodes = [x[0] for x in frontier]
		for trafficLine in trafficLines[node]:
			if trafficLine[0] not in openNodes and trafficLine[0] not in explored:
				traceParentsWithCost[trafficLine[0]] = (node, cost)
				if trafficLine[0] == goalState:
					solution = getSolution(traceParentsWithCost, trafficLine[0])
					return solution
				else:
					frontier.append((trafficLine[0], cost))

def dfs(startState, goalState, trafficLines):
	'''
	Implements Depth First Search to find the path from startState to goalState using trafficLines
	Arguments:
		startState :- the start state of the path
		goalState :- the destination of the path
		trafficLines :- the edges in the graph along with the associated costs
	Returns:
		solution :- a string which contains a series of nodes along with the corresponding accumulated cost from the startState 
		for each node
	Details:
		Returns the solution directly if startState and goalState are the same
		Otherwise creates a list 'frontier' which is a LIFO stack to store newly generated states (initially startState) along with the
		accumulated cost till that state and a list 'explored' which handles the already explored states
		It keeps track of the depth traversed using the variable 'cost'
		It keeps track of the parents of every generated node along with the associated cost using the dictionary traceParentsWithCost
	'''	
	cost = 0
	if startState == goalState:
		return startState + ' ' + str(cost)
	frontier = list()
	explored = list()
	traceParentsWithCost = dict()
	frontier.insert(0, (startState, cost))
	while len(frontier) != 0:
		node, cost = frontier.pop(0)
		if node == goalState:
			solution = getSolution(traceParentsWithCost, node)
			return solution
		cost += 1
		explored.append(node)
		tempChildrenList = list()
		openNodes = [x[0] for x in frontier]
		for trafficLine in trafficLines[node]:
			if trafficLine[0] not in openNodes and trafficLine[0] not in explored:
				traceParentsWithCost[trafficLine[0]] = (node, cost)
				'''
				Moved goal test out of here since we check that when new children are generated in bfs not in dfs. We get a wrong solution
				for the file 'input2.txt'.
				'''
				tempChildrenList.append((trafficLine[0], cost))
		frontier = tempChildrenList + frontier			

def ucs(startState, goalState, trafficLines):
	'''
	Implements Uniform Cost Search to find the path with as less cost as possible from startState to goalState using trafficLines
	Arguments:
		startState :- the start state of the path
		goalState :- the destination of the path
		trafficLines :- the edges in the graph along with the associated costs
	Returns:
		solution :- a string which contains a series of nodes along with the corresponding accumulated cost from the startState 
		for each node
	Details:
		Returns the solution directly if startState and goalState are the same
		Otherwise creates a PriorityQueue 'frontier' which is a priority queue to store newly generated states (initially startState) where the 
		accumulated cost till that state is the priority and a list 'explored' which handles the already explored states
		It keeps track of the distance traversed till the current state using the variable 'cost'
		It keeps track of the parents of every generated node along with the associated accumulated cost using the dictionary traceParentsWithCost
	'''	
	cost = 0
	if startState == goalState:
		return startState + ' ' + str(cost)
	frontier = PriorityQueue()
	'''
	Correction:
	We need to consider the following case as well. Thus, explored has been changed to a dict from a list as we'll have to keep a track of the cost along with the node name
	in order to decide whether to bring it back in the frontier
	if there exists node in explored that has child's state:
		if pathcost(child) < pathcost(node):
			explored <- DeleteNode(explored, node)
			frontier <- QueuingFn(frontier, child)
	'''
	explored = dict()
	traceParentsWithCost = dict()
	frontier.insert(cost, startState)
	while frontier.length() != 0:
		cost, node = frontier.delete()
		if node == goalState:
			solution = getSolution(traceParentsWithCost, node)
			return solution
		explored[node] = cost
		openNodes = frontier.findOpenNodes()
		for trafficLine in trafficLines[node]:
			if trafficLine[0] not in explored:
				if trafficLine[0] not in openNodes:
					frontier.insert(cost+trafficLine[1], trafficLine[0])
					traceParentsWithCost[trafficLine[0]] = (node, cost+trafficLine[1])	
				else:
					frontier.replaceDecision(trafficLine[0], cost+trafficLine[1], node, traceParentsWithCost)
			else:
				if (cost+trafficLine[1]) < explored[trafficLine[0]]:
					explored.pop(trafficLine[0])
					frontier.insert(cost+trafficLine[1], trafficLine[0])
					traceParentsWithCost[trafficLine[0]] = (node, cost+trafficLine[1])	

def astar(startState, goalState, trafficLines, sundayTrafficLines):
	'''
	Implements A* Search to find the path with as less cost as possible from startState to goalState using trafficLines and a heuristic function
	In this case, sundayTrafficLines is the heuristic function which stores the time it takes to reach from a particular node to the goalState
	on a traffic free Sunday
	Arguments:
		startState :- the start state of the path
		goalState :- the destination of the path
		trafficLines :- the edges in the graph along with the associated costs
		sundayTrafficLines :- the heuristic function for this problem
	Returns:
		solution :- a string which contains a series of nodes along with the corresponding accumulated cost from the startState 
		for each node
	Details:
		Returns the solution directly if startState and goalState are the same
		Otherwise creates a PriorityQueue 'frontier' which is a priority queue to store newly generated states (initially startState) where the 
		accumulated cost plus the heuristic (at that particular state) till that state is the priority and a list 'explored' which handles the already explored states
		It keeps track of the distance traversed till the current state using the variable 'cost'
		It keeps track of the parents of every generated node along with the associated accumulated cost plus the heuristic using the dictionary traceParentsWithCost
	'''	
	cost = sundayTrafficLines[startState]
	if startState == goalState:
		return startState + ' ' + str(cost-sundayTrafficLines[startState])
	frontier = PriorityQueue()
	'''
	Correction:
	We need to consider the following case as well. Thus, explored has been changed to a dict from a list as we'll have to keep a track of the cost along with the node name
	in order to decide whether to bring it back in the frontier
	if there exists node in explored that has child's state:
		if pathcost(child) < pathcost(node):
			explored <- DeleteNode(explored, node)
			frontier <- QueuingFn(frontier, child)
	'''
	explored = dict()
	traceParentsWithCost = dict()
	frontier.insert(cost, startState)
	while frontier.length() != 0:
		cost, node = frontier.delete()
		explored[node] = cost
		cost -= sundayTrafficLines[node]
		if node == goalState:
			solution = getAstarSolution(traceParentsWithCost, node, sundayTrafficLines)
			return solution
		openNodes = frontier.findOpenNodes()
		for trafficLine in trafficLines[node]:
			if trafficLine[0] not in explored:
				if trafficLine[0] not in openNodes:
					frontier.insert(cost+trafficLine[1]+sundayTrafficLines[trafficLine[0]], trafficLine[0])
					traceParentsWithCost[trafficLine[0]] = (node, cost+trafficLine[1]+sundayTrafficLines[trafficLine[0]])	
				else:
					frontier.replaceDecision(trafficLine[0], cost+trafficLine[1]+sundayTrafficLines[trafficLine[0]], node, traceParentsWithCost)
			else:
				if (cost+trafficLine[1]+sundayTrafficLines[trafficLine[0]]) < explored[trafficLine[0]]:
					explored.pop(trafficLine[0])
					frontier.insert(cost+trafficLine[1]+sundayTrafficLines[trafficLine[0]], trafficLine[0])
					traceParentsWithCost[trafficLine[0]] = (node, cost+trafficLine[1]+sundayTrafficLines[trafficLine[0]])

def main():
	'''
	Takes input from the file 'input.txt' which is in the following format and saves them in the following variables:
	algo 								:- <ALGO>
	startState 							:- <START STATE>
	goalState 							:- <GOAL STATE>
	noOfLiveTrafficLines 				:- <NUMBER OF LIVE TRAFFIC LINES>
	trafficLines (dictionary of lists)	:- <... LIVE TRAFFIC LINES ...>
	noOfSundayTrafficLines 				:- <NUMBER OF SUNDAY TRAFFIC LINES>
	sundayTrafficLines (dictionary)		:- <... SUNDAY TRAFFIC LINES ...>
	'''
	
	f = open('input.txt', 'r')
	algo = f.readline().rstrip().upper()
	startState = f.readline().rstrip()
	goalState = f.readline().rstrip()
	noOfLiveTrafficLines = int(f.readline().rstrip())
	trafficLines = dict()
	solution = ''
	for _ in range(noOfLiveTrafficLines):
		line = f.readline().rstrip().split(' ')
		if not trafficLines.has_key(line[0]):
			trafficLines[line[0]] = list()
		trafficLines[line[0]].append((line[1], int(line[2])))
		if not trafficLines.has_key(line[1]):
			trafficLines[line[1]] = list()
	noOfSundayTrafficLines = int(f.readline().rstrip())
	sundayTrafficLines = dict()
	for _ in range(noOfSundayTrafficLines):
		line = f.readline().rstrip().split(' ')
		sundayTrafficLines[line[0]] = int(line[1])
	f.close()
	if algo == 'BFS':
		solution = bfs(startState, goalState, trafficLines)
	elif algo == 'DFS':
		solution = dfs(startState, goalState, trafficLines)	
	elif algo == 'UCS':
		solution = ucs(startState, goalState, trafficLines)
	elif algo == 'A*':
		solution = astar(startState, goalState, trafficLines, sundayTrafficLines)
	f = open('output.txt', 'w')
	f.write(solution)
	f.close()	
	
	#For tesing purposes
	'''
	for i in range(190):
		s = "input" + str(i) + ".txt"
		#s = 'input100.txt'
		#print s
		#s = "input20.txt"
		f = open(s, 'r')
		algo = f.readline().rstrip()
		startState = f.readline().rstrip()
		goalState = f.readline().rstrip()
		noOfLiveTrafficLines = int(f.readline().rstrip())
		trafficLines = dict()
		for _ in range(noOfLiveTrafficLines):
			line = f.readline().rstrip().split(' ')
			if not trafficLines.has_key(line[0]):
				trafficLines[line[0]] = list()
			trafficLines[line[0]].append((line[1], int(line[2])))
			if not trafficLines.has_key(line[1]):
				trafficLines[line[1]] = list()
		noOfSundayTrafficLines = int(f.readline().rstrip())
		sundayTrafficLines = dict()
		for _ in range(noOfSundayTrafficLines):
			line = f.readline().rstrip().split(' ')
			sundayTrafficLines[line[0]] = int(line[1])
		f.close()
		print ''
		print s
		print 'BFS'
		solution = bfs(startState, goalState, trafficLines)
		print solution
		#print '\n\n'
		print 'DFS'
		solution = dfs(startState, goalState, trafficLines)
		print solution
		#print '\n\n'
		print 'UCS'
		solution = ucs(startState, goalState, trafficLines)
		print solution
		#print '\n\n'	
		print 'A*'
		solution = astar(startState, goalState, trafficLines, sundayTrafficLines)
		print solution
		#print '\n\n'
		'''

main()