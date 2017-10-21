# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #print [action for action in legalMoves],scores," action=",legalMoves[chosenIndex]
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        if not newFood:
            return score

        for ghost in newGhostStates:
            ghost_pac = manhattanDistance(newPos, ghost.getPosition())
            #discourage going near ghost
            if(ghost_pac)<=2 and ghost.scaredTimer<3 :
                score-=25

        max_score = 0;
        for food in newFood:
            pac_food = manhattanDistance(food,newPos)
            value = 1/float(pac_food)
            if(value>max_score):
                max_score=value
        score+=(value*10)

        return score
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getMin_Max(self,node,depth):

        #last min level exploration? or a terminal state?
        if depth==0 or node.state.isWin() or node.state.isLose():
            return node
        #if max node?
        '''generate sucessors for pacman
               add them as children and  with "min" Nodes,depth
               make a recursive call for each child
               Return Max(returned values from children)
        '''
        if node.agent == 0:
            actions = node.state.getLegalActions(0)
            #print depth,":   Pacman actions: ", actions
            for act in actions:
                successor = node.state.generateSuccessor(0, act)
                min_node = Node(successor, act, 1)
                node.add_child(min_node)
            best = node
            max_ = -10000
            for child in node.children:
                child_node = self.getMin_Max(child,depth)
                value = self.evaluationFunction(child_node.state)
                if(value>max_):
                    max_=value
                    best=child_node
                    if(depth!=self.depth):
                        best.action=node.action
            return best

        else:
            ghosts = node.state.getNumAgents()
            actions = node.state.getLegalActions(node.agent)
            #print "\t((",(node.agent)%ghosts,"))ghost actions: ",actions
            for act in actions:
                successor = node.state.generateSuccessor(node.agent, act)
                next_node = Node(successor, node.action, (node.agent+1)%ghosts)
                node.add_child(next_node)
            values = {}
            for child in node.children:
                child_node = None
                #next max(Pacman) node?
                if(node.agent == ghosts-1):
                    child_node = self.getMin_Max(child, depth - 1)
                else:
                    child_node = self.getMin_Max(child, depth)
                values[self.evaluationFunction(child_node.state)] = child_node
            #print "Min returns ",min(values)
            return values[min(values)]

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        root = Node(gameState, None, 0)
        temp = root
        #print "Ghost Agents:", gameState.getNumAgents() - 1
        next = self.getMin_Max(root,self.depth)
        #print "Possible actions: ",gameState.getLegalActions(0)
        #print "\tAction: ",next.action,"  minmax score = ",self.evaluationFunction(next.state)
        return next.action
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getalpha_beta(self,node,depth,alpha,beta):
        # last min level exploration? or a terminal state?
        # get scores of successors
        if depth == 0 or node.state.isWin() or node.state.isLose():
            return self.evaluationFunction(node.state)
        # if max node?
        '''generate sucessors for pacman
               add them as children and  with "min" Nodes,depth
               make a recursive call for each child
               Return Max(returned values from children)
        '''
        if node.agent == 0:
            #print("Depth:", depth, " alpha= ", alpha, " beta= ", beta)
            actions = node.state.getLegalActions(0)
            max_ = -10000
            for act in actions:
                successor = node.state.generateSuccessor(0, act)
                min_node = Node(successor, act, 1)

                value = self.getalpha_beta(min_node, depth,alpha,beta)
                if (value > max_):
                    max_ = value
                #prunning? No need to explore more...
                if max_ > beta:
                    return max_
                alpha = max(alpha,max_)
            return max_

        else:
            ghosts = node.state.getNumAgents()
            actions = node.state.getLegalActions(node.agent)
            min_ = 10000
            for act in actions:
                successor = node.state.generateSuccessor(node.agent, act)
                next_node = Node(successor, node.action, (node.agent + 1) % ghosts)
                # next level is max(Pacman) node?
                if (node.agent == ghosts - 1):
                    score = self.getalpha_beta(next_node, depth - 1,alpha,beta)
                else:
                    score = self.getalpha_beta(next_node, depth,alpha,beta)
                #print "\t at node:", score, "current beta = ", beta
                min_ = min(min_,score)
                #prunning? Max node is never going to be interested in this ?
                if min_ < alpha:
                    return min_
                beta = min(min_,beta)
            return min_

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        root = Node(gameState, None, 0)
        actions = gameState.getLegalActions(0)
        scores = []
        #allpha = -infinity  beta= +infinity
        alpha = -10000
        beta = 10000
        # First min level (Pacman -root will pick max of returned values)
        for act in actions:
            successor = gameState.generateSuccessor(0, act)
            min_node = Node(successor, act, 1)
            score = self.getalpha_beta(min_node, self.depth,alpha,beta)
            scores.append(score)
            #update alpha value if required
            alpha = max(alpha,score)

        return actions[scores.index(max(scores))]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getExpectiMax(self,node,depth):

        #last min level exploration? or a terminal state?
        #get scores of successors
        if depth==0 or node.state.isWin() or node.state.isLose():
            return self.evaluationFunction(node.state)
        #if max node?
        '''generate sucessors for pacman
               add them as children and  with "min" Nodes,depth
               make a recursive call for each child
               Return Max(returned values from children)
        '''
        if node.agent == 0:
            actions = node.state.getLegalActions(0)
            for act in actions:
                successor = node.state.generateSuccessor(0, act)
                min_node = Node(successor, act, 1)
                node.add_child(min_node)
            best = node
            max_ = -10000
            for child in node.children:
                value = self.getExpectiMax(child,depth)
                if(value>max_):
                    max_=value
            return max_

        else:
            ghosts = node.state.getNumAgents()
            actions = node.state.getLegalActions(node.agent)
            for act in actions:
                successor = node.state.generateSuccessor(node.agent, act)
                next_node = Node(successor, node.action, (node.agent+1)%ghosts)
                node.add_child(next_node)
            values = []
            for child in node.children:
                #next level after this is max(Pacman) node?
                if(node.agent == ghosts-1):
                    score = self.getExpectiMax(child, depth - 1)
                else:
                    score = self.getExpectiMax(child, depth)
                values.append(score)
            #compute average over this values = Expectimax
            probab = 1.0/len(actions)
            expected = 0.0
            for v in values:
                expected =expected +(probab*v)
            return expected

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        root = Node(gameState, None, 0)
        actions = gameState.getLegalActions(0)

        #First min level (Pacman -root will pick max of returned values)
        scores=[]
        for act in actions:
            successor = gameState.generateSuccessor(0, act)
            min_node = Node(successor, act, 1)
            scores.append(self.getExpectiMax(min_node, self.depth))

        # print "Possible actions: ",gameState.getLegalActions(0)
        # print "\tAction: ",next.action,"  minmax score = ",self.evaluationFunction(next.state)
        return actions[scores.index(max(scores))]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    max_score = -10000

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()

    score = currentGameState.getScore()
    #nothing fency be real
    if currentGameState.isWin() or currentGameState.isLose():
        return score

    # discourage going near any ghost
    for ghost in newGhostStates:
        ghost_pac = manhattanDistance(newPos, ghost.getPosition())
        if (ghost_pac) <= 2 and ghost.scaredTimer < 3:
            score -= 25
    max_ = -1000
    #find the farthest food score
    for food in newFood:
        pac_food = manhattanDistance(food, newPos)
        value = 1 / float(pac_food)
        if (value > max_):
            max_ = value
    score += max_*10
    max_score = max(max_score, score)
    #print "Score = ",max_score
    return max_score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
'''Helper class / data structure for min-max'''
class Node(object):
    def __init__(self, gameState, action,agent):
        self.state = gameState
        self.action = action
        self.children = []
        self.agent = agent #0for pacman, 1,2.. for ghosts

    def add_child(self, obj):
        self.children.append(obj)
