from Astar import Astar
from node import node
import heapq
import copy
'''
    This class is derived from the Astar class.
    goal state is given by the user
    start state is also given by user
    it uses manhattan distance if no heuristic is selected
'''

class eightPuzzle(Astar):
    def __init__(self,inputState,goalState,isManhattanDistance):
        Astar.__init__(self,inputState)
        self.NodesGenerated = 0
        self.goalState = goalState
        self.dimension = 3
        self.isManhattanDistance = isManhattanDistance
        n = self.createNode()
        heapq.heappush(self.fringe,(n.f, n))

    def createNode(self,state=None,parent=None):
        self.NodesGenerated += 1
        if state is None:
            state = self.inputState
            n = node(state)
            n.g = 0
            n.h = self.calculateH(state)
            n.f = self.calF(n)
            return n
        else:
            n = node(state, parent)
            n.g = self.calG(parent)
            n.h = self.calculateH(state)
            n.f = self.calF(n)
            return n

    def calG(self, parent):
        return parent.g+1

    def calculateH(self,state):
        if(self.isManhattanDistance):
            return self.calculateHvalueManhattan(state)
        else:
            return self.calculateHvalueMisplacedTiles(state)

    def isGoalState(self,state):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if state[i][j] != self.goalState[i][j]:
                    return False
        return True

    def isTwoStatesEqual(self,state1,state2):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if state1[i][j] != state2[i][j]:
                    return False
        return True
    def findIndex(self,state,number):
        for i, row in enumerate(state):
            try:
                j = row.index(number)
            except ValueError:
                continue
            return i, j

    def calculateHvalueMisplacedTiles(self,state):
        hvalue = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if ((state[i][j] !=0) and  (state[i][j] != self.goalState[i][j])):
                    hvalue +=1
        return hvalue

    def calculateHvalueManhattan(self,state):
        hvalue = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if (state[i][j] != 0):
                    (goalRow,goalColumn) = self.findIndex(self.goalState,state[i][j])
                    hvalue += abs(goalColumn - j) + abs(goalRow - i)
        return hvalue

    def printstate(self,state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    print(' ',end=' ')
                else:
                    print(state[i][j], end=' ')
            print()
        print()

    def printNode(self,n):
        print('The values are g=',n.g,' f=',n.f,' h=',n.h,' state = ',n.state)

    def printPath(self,n):
        path = []
        while(True):
            if(n is None):
                break
            else:
                path.append(n.state)
                n = n.parent
        print('The Path length = ',len(path))
        print('Path Trace')
        for state in reversed(path):
            self.printstate(state)

    def generatechilds(self,n):
        childs = []
        i,j = self.findIndex(n.state,0)
        #generate the valid indexes
        #The sequence is up,left,down,right
        validindexes = []
        if i-1 >=0:
            validindexes.append((i-1,j))
        if j-1 >=0:
            validindexes.append((i,j-1))
        if i+1 <3:
            validindexes.append((i+1,j))
        if j+1 <3:
            validindexes.append((i,j+1))
        for index,(row,col) in enumerate(validindexes):
            state = copy.deepcopy(n.state)
            temp = state[i][j]
            state[i][j] = state[row][col]
            state[row][col] = temp
            childs.append(self.createNode(state,n))
        return childs

    def checkifSameStateExistswithLowerFvalue(self,lists,n):
        for i,l in lists:
            if self.isTwoStatesEqual(l.state,n.state):
               if(l.f>n.f):
                    l = n
                    return True
               else:
                   return True
        return False
