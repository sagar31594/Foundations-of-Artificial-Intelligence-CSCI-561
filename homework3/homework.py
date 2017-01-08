import copy
import re
import time

#exp = 'D(x,y) & F(y) => C(x) | D(x,y)'
#exp = 'D(x,y) & F(y) => C(x,y)'

gd = {}
count = 0
tempKB = []
varcount = 0
var = 'x'
availableTime = 200
start = 0
timePerClause = 0

def rep(m):
	global gd, count
	key = m.group(0)
	if gd.has_key(key):
		return gd[key]
	else:
		gd[key] = str(count)
		count += 1
	return gd[key]

#matches = re.sub(r'[A-Z][a-z]*\(.*?\)', rep, '(D(x,y) & F(y)) => C(x,y)')

def negate(exp):
	if len(exp) == 1:
		#print '\n'
		#print 'exp inside len == 1: ', exp
		exp = [exp]
		exp.insert(0, '~')
	elif len(exp) == 2:
		#print 'exp: ', exp
		#print 'inside negate'
		exp = exp[1]
		#print 'after changing: ', exp
	else:
		exp[0] = '&' if exp[0] == '|' else '|'
		exp[1] = negate(exp[1])
		exp[2] = negate(exp[2])
	return exp

def removeImplications(exp):
	if len(exp) < 2:
		return exp
	opr = exp[0]
	if opr == '~':
		exp[1] = removeImplications(exp[1])
	else:
		exp[1] = removeImplications(exp[1])
		exp[2] = removeImplications(exp[2])
	if opr == '#':
		exp[0] = '|'
		'''
		print '\n'
		print 'inside removeImplications: '
		print 'exp: ', exp[1]
		print '\n'
		'''
		exp[1] = negate(exp[1])
		#print exp
	return exp

def moveNegationInwards(exp):
	if len(exp) < 2:
		return exp
	opr = exp[0]
	if opr == '~':
		exp[1] = moveNegationInwards(exp[1])
	else:
		exp[1] = moveNegationInwards(exp[1])
		exp[2] = moveNegationInwards(exp[2])
	if opr == '~' and len(exp[1]) > 1:
		exp = exp[1]
		exp = negate(exp)
	return exp

def distributeOrOverAnd(exp):
	if len(exp) < 2:
		return exp
	opr = exp[0]
	if opr == '~':
		exp[1] = distributeOrOverAnd(exp[1])
	else:
		exp[1] = distributeOrOverAnd(exp[1])
		exp[2] = distributeOrOverAnd(exp[2])
	if opr == '|':
		a = exp[1]
		b = exp[2]
		if a[0] == '&':
			temp1 = ['|', a[1], b]
			temp2 = ['|', a[2], b]
			exp[0] = '&'
			exp[1] = temp1
			exp[2] = temp2
			distributeOrOverAnd(exp)
		elif b[0] == '&':
			temp1 = ['|', a, b[1]]
			temp2 = ['|', a, b[2]]
			exp[0] = '&'
			exp[1] = temp1
			exp[2] = temp2
			distributeOrOverAnd(exp)
	#print '\nInside distributeOrOverAnd: '
	#print exp
	return exp

def add(exp, sentence=None):
	global tempKB
	if len(exp) == 1:
		if sentence == None:
			sentence = {}
			sentence[exp[0]] = [False]
			tempKB.append(sentence)
		else:
			sentence[exp[0]] = [False]
	elif len(exp) == 2:
		if sentence == None:
			sentence = {}
			sentence[exp[1][0]] = [True]
			tempKB.append(sentence)
		else:
			sentence[exp[1][0]] = [True]
	else:
		if exp[0] == '&':
			add(exp[1])
			add(exp[2])
		else:
			if sentence == None:
				sentence = {}
				add(exp[1], sentence)
				add(exp[2], sentence)
				tempKB.append(sentence)
			else:
				add(exp[1], sentence)
				add(exp[2], sentence)

def findPredicate(searchValue):
	global gd
	#print searchValue
	#print gd
	predicate = None
	#print 'gd: ', gd
	#print 'searchValue: ', searchValue
	for key, value in gd.iteritems():
		if value == searchValue:
			predicate = key
			break
	#print 'predicate: ', predicate
	predicate = predicate.split('(')
	#print predicate
	args = predicate[1].split(',')
	args[-1] = args[-1][:-1]
	predicate = predicate[0]
	return (predicate, args)

def simplifySentence(exp):
	global gd, count
	gd = {}
	count = 0
	exp = exp.replace(" ", "")
	#print 'after removing spaces: ', exp
	exp = re.sub(r'[A-Z][A-Za-z]*\(.*?\)', rep, exp)
	#print exp
	#print gd
	prec = {'~' : 4, '&' : 3, '|' : 2, '#' : 1, '(' : 0, ')' : 0}

	#exp = '~(0 & 1) => 2'
	#exp = '0 & 1 => ~(2 | 3)'
	#exp = '(A & B) | (C & D)'
	exp = exp.replace('=>', '#')
	#print 'exp: ', exp
	index = 0
	temp = []
	prev = False
	diffcount = 0
	while True:
		if index == len(exp):
			break
		if not exp[index].isdigit():
			temp.append(exp[index])
			index += 1
			prev = False
			diffcount += 1
		else:
			if prev:
				temp[diffcount-1] += exp[index]
				index += 1
			else:
				temp.append(exp[index])
				index += 1
				diffcount += 1
				prev = True
	#print 'temp: ', temp
	temp = temp[::-1]
	stack = []
	#prefix = ''
	prefix = []
	for ch in temp:
		if ch == ')':
			stack.insert(0, ch)
			'''
			print '\n'
			print 'inserted: ', ch
			print 'stack: ', stack
			print '\n'
			'''
		elif ch not in prec:
			#prefix += ch# + prefix 
			prefix.append(ch)
			'''
			print '\n'
			print 'added to prefix: ', ch
			print 'prefix: ', prefix
			'''
		elif ch == '(':
			while len(stack) != 0 and stack[0] !=  ')':
				#prefix += stack.pop(0)# + prefix
				prefix.append(stack.pop(0))
			stack.pop(0)
		elif ch in prec:
			#opr = stack[0]
			while len(stack) != 0 and prec[ch] < prec[stack[0]]:
				#prefix += stack.pop(0)# + prefix
				prefix.append(stack.pop(0))
			stack.insert(0, ch)
	while len(stack) != 0:
		#prefix += stack.pop(0) 
		prefix.append(stack.pop(0))
	#print prefix
	stack = []
	for ch in prefix:
		if ch not in prec:
			stack.insert(0, [ch])
		else:
			if ch == '~':
				lst = [ch, stack.pop(0)]
				stack.insert(0, lst)
			else:
				lst = [ch, stack.pop(0), stack.pop(0)]
				stack.insert(0, lst)
	#print 'stack[0]: ', stack[0]
	return stack[0]

def convertToCNF(exp):
	newexp = removeImplications(exp)
	#print 'after removing implications'
	#print newexp
	newexp = moveNegationInwards(newexp)
	#print '\nafter moveNegationInwards: '
	#print newexp
	newexp = distributeOrOverAnd(newexp)
	#print '\nafter distributeOrOverAnd: '
	#print newexp	
	return newexp

def findVariables(clause):
	varlist = []
	for predicate in clause:
		for i in range(len(clause[predicate])):
			for variable in clause[predicate][i][1]:
				if variable not in varlist and variable[0].islower():
					varlist.append(variable)
	return varlist

def replaceVariables(clause):
	global varcount, var
	newvars = {}
	varlist = findVariables(clause)
	for variable in varlist:
		if variable not in newvars:
			newvars[variable] = var + str(varcount)
			varcount += 1
	for predicate in clause:
		for j in range(len(clause[predicate])):
			for i in range(len(clause[predicate][j][1])):
				if clause[predicate][j][1][i][0].islower():
					clause[predicate][j][1][i] = newvars[clause[predicate][j][1][i]]

def tellKB(KB, exp, flag=False):
	#global gd, count, tempKB
	global tempKB
	tempKB = []
	newexp = simplifySentence(exp)
	newexp = convertToCNF(newexp)
	if flag:
		#print 'negate'
		newexp = negate(newexp)
	add(newexp)
	#print '\nafter adding to tempKB'
	#print tempKB

	for i in tempKB:
		keys = i.keys()
		for key in keys:
			predicate, args = findPredicate(key)
			if predicate not in i:
				i[predicate] = []
				i[predicate].append(i.pop(key))
				i[predicate][0].append(args)
			else:
				value = i.pop(key)
				value.append(args)
				i[predicate].append(value)
	#print 'after making changes: '
	#print tempKB
	for clause in tempKB:
		replaceVariables(clause)
	KB += tempKB
		#print '\nAfter changing to predicates: '
		#print tempKB

def findComplements(clause1, clause2):
	keys = []
	pos = []
	for key in clause1:
		if key in clause2:
			for i in range(len(clause1[key])):
				for j in range(len(clause2[key])):
					if (clause1[key][i][0] ==  (not clause2[key][j][0])):
						keys.append(key)
						pos.append([i, j])
	return keys, pos

def hasConstants(predicate, pos, clause):
	for var in clause[predicate][pos][1]:
		if var[0].isupper():
			return True

def find(variable, theta):
	index = -1
	for i in range(len(theta)):
		if theta[i][0] == variable:
			index = i
			break
	return index

def unify_var(var, x, theta):
	varind = find(var, theta)
	xind = find(x, theta)
	if varind != -1:
		return newunify(theta[varind][1], x, theta)
	elif xind != -1:
		return newunify(var, theta[xind][1], theta)
	else:
		theta.append([var, x])
		return theta

def newunify(x, y, theta):
	#print '\nx: ', x
	#print 'y: ', y
	#print 'theta: ', theta
	if theta == 'failure':
		return 'failure'
	elif x == y:
		return theta
	elif type(x) is str and x[0].islower():
		return unify_var(x, y, theta)
	elif type(y) is str and y[0].islower():
		return unify_var(y, x, theta)
	elif type(x) is list and type(y) is list:
		if len(x) == 1 and len(y) == 1:
			return newunify(x[0], y[0], theta)
		else:
			return newunify(x[1:], y[1:], newunify(x[0], y[0], theta))
	else:
		return 'failure'

def unify(keys, pos, clause1, clause2):
	global start, timePerClause
	resolvents = []
	for k, p in zip(keys, pos):
		if time.time() - start >= timePerClause:
			return [-1]
		#if len(sublst) == len(set(primary[k][p[0]][1])):
		theta = newunify(clause1[k][p[0]][1], clause2[k][p[1]][1], [])
		#print 'final theta: ', theta
		if theta != 'failure':
			newclause1 = copy.deepcopy(clause1)
			newclause2 = copy.deepcopy(clause2)
			#print 'newclause1: ', newclause1
			#print 'newclause2: ', newclause2
			for subvar in theta:
				for predicate in newclause1:
					for i in range(len(newclause1[predicate])):
						for j in range(len(newclause1[predicate][i][1])):
							if newclause1[predicate][i][1][j] == subvar[0]:
								newclause1[predicate][i][1][j] = subvar[1]
				for predicate in newclause2:
					for i in range(len(newclause2[predicate])):
						for j in range(len(newclause2[predicate][i][1])):
							if newclause2[predicate][i][1][j] == subvar[0]:
								newclause2[predicate][i][1][j] = subvar[1]
			#print 'newclause1 after substitution: ', newclause1
			#print 'newclause2 after substitution: ', newclause2
			if len(newclause1[k]) == 1:
				del newclause1[k]
			else:
				newclause1[k].pop(p[0])
			if len(newclause2[k]) == 1:
				del newclause2[k]
			else:
				newclause2[k].pop(p[1])
			#print 'newclause1 after deletion: ', newclause1
			#print 'newclause2 after deletion: ', newclause2
			for predicate in newclause2.keys():
				if predicate not in newclause1:
					newclause1[predicate] = newclause2.pop(predicate)
				else:
					newclause1[predicate] += newclause2.pop(predicate)
			#print 'newclause1 after removing negated predicates: ', newclause1
			#deleteDuplicateEntries = []
			newclause = {}
			for predicate in newclause1:
				#print 'predicate: ', predicate
				#for i in range(len(newclause1[predicate])-1):
				for i in range(len(newclause1[predicate])):
					#print 'hi'
					flag = False
					for j in range(i+1, len(newclause1[predicate])):
						if newclause1[predicate][i] == newclause1[predicate][j]: #and (predicate, i) not in deleteDuplicateEntries:
							flag = True
							#deleteDuplicateEntries.append((predicate, i))
					if not flag:
						if predicate not in newclause:
							newclause[predicate] = []
							newclause[predicate].append(newclause1[predicate][i])
						else:
							newclause[predicate].append(newclause1[predicate][i])
			#print 'newclause after removing any duplicate entries: ', newclause
			'''
			for i in deleteDuplicateEntries:
				newclause1[predicate].pop(i)
			'''
			replaceVariables(newclause)
			resolvents.append(newclause)
		#else:
			#resolvents.append({})
	return resolvents

def resolve(clause1, clause2):
	keys, pos = findComplements(clause1, clause2)
	#print 'keys to be resolved: ', keys, ' ', pos
	if len(keys) != 0:
		return unify(keys, pos, clause1, clause2)

def tokenMapping(clause, varlist):
	for predicate in clause.keys():
		for i in range(len(clause[predicate])):
			for j in range(len(clause[predicate][i][1])):
				if clause[predicate][i][1][j] not in varlist:
					varlist[clause[predicate][i][1][j]] = []
					#varlist[clause[predicate][i][1][j]].append((predicate, clause[predicate][i][0], i, j))
					varlist[clause[predicate][i][1][j]].append((predicate, clause[predicate][i][0], j))
				else:
					#varlist[clause[predicate][i][1][j]].append((predicate, clause[predicate][i][0], i, j))
					varlist[clause[predicate][i][1][j]].append((predicate, clause[predicate][i][0], j))

def subset(newlyGeneratedResolvents, newKB):
	global start, timePerClause
	matched = []
	for c1 in newlyGeneratedResolvents:
		#found = False
		found = []
		for c2 in newKB:
			if time.time() - start >= timePerClause:
				return True
			if len(c1) == len(c2):
				'''
				print '\n'
				print 'c1: ', c1
				print 'c2: ', c2
				'''
				t1 = sorted(c1.keys())
				t2 = sorted(c2.keys())
				'''
				print '\n'
				print 't1: ', t1
				print 't2: ', t2
				'''
				if t1 == t2:
					varlist1 = {}
					varlist2 = {}
					tokenMapping(c1, varlist1)
					tokenMapping(c2, varlist2)
					#print 'varlist1: ', varlist1
					#print 'varlist2: ', varlist2
					matchedVars = []
					for i in varlist1:
						for j in varlist2:
							if j in matchedVars:
								continue
							if len(varlist1[i]) == 1 and len(varlist2[j]) == 1:
								if varlist1[i] == varlist2[j] and i[0].islower() and j[0].islower():
									matchedVars.append(j)
								elif i[0].isupper() and j[0].isupper() and (i == j) and (varlist1[i] == varlist2[j]):
									matchedVars.append(j)
							else:
								templist1 = sorted(varlist1[i])
								templist2 = sorted(varlist2[j])
								if templist1 == templist2 and i[0].islower() and j[0].islower():
									matchedVars.append(j)
								elif i[0].isupper() and j[0].isupper() and (i == j) and (templist1 == templist2):
									matchedVars.append(j)
					if len(matchedVars) == len(varlist1) and len(matchedVars) == len(varlist2):
						matched.append(True)
						break
	return len(matched) == len(newlyGeneratedResolvents)

def union(newKB, newlyGeneratedResolvents):
	global start, timePerClause
	#print 'newlyGeneratedResolvents: ', newlyGeneratedResolvents
	#print 'length: ', len(newlyGeneratedResolvents)
	#raw_input()
	for clause in newlyGeneratedResolvents:
		temp = [clause]
		#print 'temp in union: ', temp
		if time.time() - start >= timePerClause:
			return
		if not subset(temp, newKB):
			newKB += temp
			#print 'after adding ', temp, ' to newKB:'
			#print newKB

def resolution(c, KB):
	global start, timePerClause
	newKB = copy.deepcopy(KB)
	tellKB(newKB, c, True)
	#print 'newKB: ', len(newKB)
	#print newKB
	advance = 1
	while True:
		#print '\n\n'
		#print 'newKB: ', newKB
		#print 'len: ', len(newKB)
		newlyGeneratedResolvents = []
		for i in range(len(newKB)-1):
			for j in range(i+1, len(newKB)):
				if time.time() - start >= timePerClause:
					return False
				if j < advance:
					continue
				resolvents = resolve(newKB[i], newKB[j])
				#print '\n\nnewlyGeneratedResolvents: ', newlyGeneratedResolvents
				if resolvents != None and -1 in resolvents:
					return False
				#print '\nresolvents: ', resolvents
				if resolvents != None and {} in resolvents:
					return True
				if resolvents != None:
					newlyGeneratedResolvents += resolvents
				#print 'newlyGeneratedResolvents: ', newlyGeneratedResolvents
		#print 'outside 2 for loops:'
		if subset(newlyGeneratedResolvents, newKB):
			return False
		advance = len(newKB)
		union(newKB, newlyGeneratedResolvents)

def main():
	global availableTime, start, timePerClause
	KB = list()
	#filename = 'IO/input' + str(count) + '.txt'
	#print 'Filename: ', filename
	f = open('input.txt', 'r')
	N = int(f.readline().rstrip())
	conclusions = []
	for _ in range(N):
		conclusions.append(f.readline().rstrip())
	KBCount = int(f.readline().rstrip())
	for _ in range(KBCount):
		tellKB(KB, f.readline().rstrip())
	#raw_input()
	#print len(KB)
	#print KB
	ans=[]
	remainingConclusions = N + 1
	#conclusions = [conclusions[0]]
	timePerClause = availableTime / remainingConclusions
	#print 'timePerClause: ', timePerClause
	for c in conclusions:
		#raw_input()
		start = time.time()
		#print 'start: ', start
		ans.append(resolution(c, KB))
		end = time.time()
		#print 'end: ', end
		#print 'time spent: ', end - start
		remainingConclusions -= 1
		availableTime -= end - start
		#print 'availableTime: ', availableTime
		timePerClause = availableTime if remainingConclusions == 0 else availableTime / remainingConclusions 
		#print 'new timePerClause: ', timePerClause
		#print '\n\n'
	#print '\n\n\n\n'
	#print 'ans: ', ans
	#print '\n\n\n\n'
	f = file('output.txt', 'w')
	for i in ans:
		f.write(str(i).upper() + '\n')
	f.close()
#for i in range(27):
#	main(i)
main()
