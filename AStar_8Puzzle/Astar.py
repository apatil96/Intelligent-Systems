import heapq

class Astar:
    def __init__(self,inputState):
        self.inputState = inputState
        self.expanded = []
        self.fringe = []

    def isGoalState(self,state):
        pass

    def calG(self,parent):
        pass

    def calF(self,n):
        return n.g+n.h

    def generatechilds(self,n):
        pass

    def printNode(self, n):
        pass

    def printPath(self,n):
        pass

    def checkifSameStateExistswithLowerFvalue(self,lists,n):
        pass

    def isTwoStatesEqual(self, state1, state2):
        pass

    def AstarSearch(self):
        if(self.isGoalState(self.inputState)):
            print('This is the goal State itself')
            return None
        while len(self.fringe) != 0:
            #remove node from fringe
            f, n = heapq.heappop(self.fringe)
            childs = self.generatechilds(n)
            for child in childs:
                if(self.isGoalState(child.state)):
                    #reached goal state
                    print('Goal Found ',child.state)
                    return child
                if self.checkifSameStateExistswithLowerFvalue(self.fringe,child) == False:
                    heapq.heappush(self.fringe,(child.f,child))
                elif self.checkifSameStateExistswithLowerFvalue(self.expanded,child) == False:
                    heapq.heappush(self.fringe,(child.f,child))
            heapq.heappush(self.expanded,(n.f,n))
        return None
