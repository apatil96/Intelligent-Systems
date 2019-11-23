from eightPuzzle import eightPuzzle
'''
    This file contains the main class
    It references eightPuzzle,Astar and node class
    It will print the final output
'''
def parseInput():
    row1 = input()
    row2 = input()
    row3 = input()
    myinputlist = [list(map(int, row1.split(' '))),list(map(int, row2.split(' '))),list(map(int, row3.split(' ')))]
    return myinputlist

if __name__ == '__main__':
    print('Enter input:')
    inputState = parseInput()
    print('Enter goal:')
    goalState = parseInput()
    checkinglenInputList = inputState[0]+inputState[1]+inputState[2]
    checkinglenGoalList = goalState[0]+goalState[1]+goalState[2]
    if len(checkinglenInputList) != 9 or len(checkinglenGoalList) !=9:
        print('improper input')
    elif len(set(checkinglenInputList) - set([0,1,2,3,4,5,6,7,8])) != 0 or len(set(checkinglenGoalList) - set([0,1,2,3,4,5,6,7,8])) != 0:
        print('improper goal input')
    else:
        isManhattanDistance = False
        ChoiceOfHueristic = input('Select Heuristic Function\n1.Manhattan Distance \n2.Misplaced Tiles\n')
        ChoiceOFHueristic = int(ChoiceOfHueristic)
        if ChoiceOfHueristic == 1:
            isManhattanDistance = True
        solution = eightPuzzle(inputState,goalState,isManhattanDistance)
        #A* algorithm
        goal_Node = solution.AstarSearch()
        #print the path from the input state to the goal state
        solution.printPath(goal_Node)
        print('The number of nodes generated =', solution.NodesGenerated)
        print('The number of nodes expanded =', len(solution.expanded)+1)
