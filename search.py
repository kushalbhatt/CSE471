# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import *


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    ###################Recursive Solution##########
    '''print "Is the start a goal?", problem.isGoalState(problem.getStartState())    
    print "Start's successors:",x
    x = problem.getSuccessors(start)
    depthFirstSearch.visited.append(start)
    #start = problem.getStartState()
    for i in x:
        if problem.isGoalState(i[0]):
            print "--------------------------------------- path found: ",i
            return [i[1]]
        if i[0] not in depthFirstSearch.visited:
            print '\t\tgoing: ',i[1]
            problem.startState = i[0]
            current = [i[1]]
            ans = depthFirstSearch(problem)
            if ans:
                print start,"Found = ",(current + ans)
                return current + ans
            #else:
            #    print i[0],'xxxxxxxxxxxx couldn\'t find: xxxxxxxx'
        #else:
            #print '\t\t\talready visited: ',i[0]
    return []       
'''
    visited=[]
    start = problem.getStartState()
    # print "Start:", start
    # initialize stack
    queue = Stack()
    #expand first node and put children on stack initially
    ans = []

    queue.push((start,[],0))
    while (not queue.isEmpty()):
        current = queue.pop()
        if problem.isGoalState(current[0]):
            # print 'Found:',current
            return current[1]

        #no need to expand?
        if current in visited:
            continue

        #mark visited
        visited.append(current[0])
        #explore
        x = problem.getSuccessors(current[0])
        # print '\t',current[0],' successors: ',x

        for i in x:
            if i[0] not in visited:
                # can't assign on tupple
                i = list(i)
                i[1] = current[1] + [i[1]]
                queue.push(i)

    # print ans
    return ans
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    Q = Queue()
    start = problem.getStartState()
    Q.push([start, [], 0])
    ans = []
    visited =[]
    while (not Q.isEmpty()):
        current = Q.pop()
        # mark visited
        if problem.isGoalState(current[0]):
            print 'Found:',current
            return current[1]

        if current[0] in visited:
            continue
        #mark visited
        visited.append(current[0])
        #explore
        #print current
        x = problem.getSuccessors(current[0])
        #print 'current = ', current
        for i in x:
            if i[0] not in visited:
                #print "\tsucessor :", i
                # can't assign on tupple
                i = list(i)
                i[1] = current[1] + [i[1]]
                #if this is goal then stop
                Q.push(i)
    # print ans
    return ans
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pQ = PriorityQueue()
    start = problem.getStartState()
    pQ.push([start, [], 0], 0)
    ans = []
    visited = []
    while (not pQ.isEmpty()):
        current = pQ.pop()
        # mark visited
        if problem.isGoalState(current[0]):
            # print 'Found:',current,' cost = ',problem.getCostOfActions(i[1].split('-'))
            return current[1]

        #no need to expand?
        if current[0] in visited:
            continue

        #mark visited
        visited.append(current[0])
        #expand
        x = problem.getSuccessors(current[0])
        for i in x:
            if i[0] not in visited:
                i = list(i)
                i[1] = current[1] + [i[1]]
                # Compute g(n) = how far have we come and push items with priority g(n)
                new_cost = problem.getCostOfActions(i[1])
                pQ.push(i, new_cost)

    return ans
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pQ = PriorityQueue()
    start = problem.getStartState()
    pQ.push([start, [], 0], 0)
    ans = []
    visited = []

    while (not pQ.isEmpty()):
        current = pQ.pop()
        if problem.isGoalState(current[0]):
            # print 'Found:',current,' cost = ',problem.getCostOfActions(i[1].split('-'))
            ans = current[1]
            return ans

        #no need to expand?
        if current[0] in visited:
            continue

        #mark visited
        visited.append(current[0])

        #expand
        x = problem.getSuccessors(current[0])
        for i in x:
            if i[0] not in visited:
                i = list(i)
                i[1] = current[1] + [i[1]]
                # push items with priority  = cost so far g(n) + heuristic f(n)
                new_cost = problem.getCostOfActions(i[1]) + heuristic(i[0],problem)
                pQ.push(i, new_cost)

    # ans = ans.split('-')
    # print ans
    return ans
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
