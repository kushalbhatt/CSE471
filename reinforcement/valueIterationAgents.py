# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        self.policies = util.Counter()

        '''dict with  state:{state_value} pairs'''
        last_iteration = util.Counter()
        for i in range(iterations):
            cur_iteration = util.Counter()
            for state in mdp.getStates():

                if(not mdp.isTerminal(state)):
                    '''Find "value" of doing each action and store it in dict as value:action pair'''
                    action_values = {}
                    for action in mdp.getPossibleActions(state):
                        successors = mdp.getTransitionStatesAndProbs(state, action)
                        val = 0.0
                        for nextstate,prob in successors:
                            ''' Vk = T(s,a,s') * { R()+ ( discount * Vk-1 (nextstate) ) } '''
                            val+= prob * (mdp.getReward(state,action,nextstate) + (discount * last_iteration[nextstate]) )
                        action_values[val]=action
                    '''Find the action that gives best value and store it in last_iteration as state:(value,action)'''
                    best_val = max(action_values)
                    cur_iteration[state] = best_val
                    self.policies[state]= action_values[best_val]
            last_iteration = cur_iteration.copy()

        self.values = last_iteration


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        successors = self.mdp.getTransitionStatesAndProbs(state, action)
        val = 0
        for nextstate, prob in successors:
            ''' Q(s,a) = T(s,a,s') * { R()+ ( discount * Q^(nextstate) ) } '''
            val += prob * (self.mdp.getReward(state, action, nextstate) + (self.discount * self.values[nextstate]))

        #print state,', ',action,' : successors = ',successors,'     :: value= ',val
        return val
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        action_values = {}
        for action in self.mdp.getPossibleActions(state):
            val = self.computeQValueFromValues(state,action)
            action_values[val]=action

        best = max(action_values)
        best_action = action_values[best]

        return best_action
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
