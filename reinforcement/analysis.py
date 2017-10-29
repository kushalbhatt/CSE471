# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0.0
    return answerDiscount, answerNoise

def question3a():
    '''To prefer +1 reward over +10: gamma should be < 1
       to risk cliffs living cost should be high enough to avoid longer route'''
    answerDiscount = 0.8
    answerNoise = 0.2
    answerLivingReward = -3
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    '''To prefer +1 reward over +10: gamma should be < 1
           to avoid risking cliffs living cost should be lower (that is reward be higher.  >=0 best)'''
    answerDiscount = 0.35
    answerNoise = 0.2
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    '''To go to +10: gamma should be higher to make +10 worth than +1
           to risk cliffs living cost should be high enough to avoid longer route'''
    answerDiscount = 1.0
    answerNoise = 0.1
    answerLivingReward = -3
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 1.0
    answerNoise = 0.1
    answerLivingReward = -0.2
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    '''To avoid exit states= living reward should be +ve, no discount factor, and more deterministic actions
        This is like infinite exploration'''
    answerDiscount = 1.0
    answerNoise = 0.3
    answerLivingReward = 2.0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    answerEpsilon = None
    answerLearningRate = None
    ''' Maybe the episodes are not very well... So learning is very limited. None of the cominations is working'''
    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
