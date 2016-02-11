__author__ = 'Michael Burdick and Steven Hogue'

import queue
import sys

class Move:
    def __init__(self, state, moved = None, prevState = None, depth = 0, accumulatedCost = 0, cost = 0):
        self.state = state # list of tiles
        self.prevState = prevState # prev move object
        self.moved = moved # index of tile that moved to get this state
        self.depth = depth
        self.accumulatedCost = accumulatedCost # accumulated cost of previous moves
        self.cost = cost
        
    # successor function
    def move(self):
        # from left look at each tile
        # if tile is out of place move it to blank tile
        # create new move object for each one of these
            # init with which tile moved, the prevState (move object), depth, accumulated cost, cost
            # accumulated cost and cost necessary only if isCostOn, but could just do it to keep it simple
            # accumulated cost is the cost() of the previous move
            # cost is the amount of tiles the move is over
        return None
    
    # h(n)
    def outOfPlace(self):
        sideLength = len(self.state) // 2
        leftMax = sideLength #B
        rightMin = sideLength + 2 #W
        outOfPlace = 0
        for i in self.state:
            if i == "B" and i.index() > leftMax:
                outOfPlace += 1
            elif i == "W" and i.index() < rightMin:
                outOfPlace += 1
        return outOfPlace
    
    # g(n)
    def cost(self, isCostOn):
        if isCostOn:
            return self.cost + self.accumulatedCost
        else:
            return self.depth

class StateQueue(queue.PriorityQueue):
    searchType = None
    isCostOn = False
    
    def pop(self):
        return self.get()
    
    def push(self, move):
        self.put((self.f(move), move))
    
    def f(self, move):
        if self.searchType == "BFS":
            return move.depth
        elif self.searchType == "DFS":
            return 1 / move.depth
        elif self.searchType == "UCS":
            return move.cost() 
        elif self.searchType == "GS":
            return move.outOfPlace()
        elif self.searchType == "A-star":
            return move.outOfPlace() + move.cost()
        
    
def search(start, goal):
    queue = StateQueue()
    queue.push(Move(start))
    while not queue.empty():
        current = queue.pop()
        
        # current[1] is necessary because we put the move object in queue using (f(n), move) tuple
        if cmp(current[1].state, goal) == 0: 
            return current
        else:
            successors = current[1].move()
            for i in successors:
                queue.push(i)
    return None

def setGoal(length):
    half = length // 2
    goal = []
    for _ in range(half):
        goal.append("B")
    
    goal.append("x")
    
    for _ in range(half):
        goal.append("W")
    
    return goal

def printResult(move):
    stack = [move]
    prev = move.prevState
    while prev:
        stack.append(prev)
        prev = prev.prevState
    
    # print initial state
    move = stack.pop()
    print("Step 0: {}".format, move.state.join())
    
    # print the path
    i = 1
    while stack:
        move = stack.pop()
        if not StateQueue.isCostOn:
            print("Step {}: move {} {}".format(i, move.moved, move.state.join()))
        else:
            print("Step {}: move {} {} (c={})".format(i, move.moved, move.state.join(), move.cost))

# Script beginning
types = ["BFS", "DFS", "UCS", "GS", "A-star"]

inputFile = ""

sys.argv.pop(0) # get rid of the filename

for arg in sys.argv:
    if arg == "-cost":
        StateQueue.isCostOn = True
    elif arg in types:
        StateQueue.searchType = arg
    else:
        inputFile = arg
        
if inputFile == "":
    print("No input file")

fin = open(inputFile)
initialState = list(fin.read())

goalState = setGoal(len(initialState))

result = search(initialState, goalState)
