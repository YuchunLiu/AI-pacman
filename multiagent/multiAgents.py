# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

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

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor) 
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #currentPostion = currentGameState.getPacmanPosition()
        
       
        if successorGameState.isWin() == True:
            return 1000000
        
        score = 0
        #get the nearest food distance into consideration
        foodlist = currentFood.asList()
        #FoodDist = []
        for food in foodlist:
            dist = manhattanDistance(newPos, food)
            if dist == 0:
                score += 1000
            else:
                score -= dist
            
        GhostDist = []
        #get the farest ghost distance into consideration 
        for ghost in newGhostStates:
            
            dist = manhattanDistance(newPos, ghost.getPosition())
            GhostDist.append(dist)
        
            if dist <4:
                score -= 5000
            else:
                score += dist
        
        if action == Directions.STOP:
            score -= 300
        #get the distance of capsules 
        
        
        if newPos in currentCapsules:
            score += 120
        else:
            for capsule in currentCapsules:
                score -= manhattanDistance(newPos, capsule)
                
        
        return score
        

    
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
        
        def get_Max(gameState, depth):
            if (depth==0 or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState), "noMove"
            Actions = gameState.getLegalActions(self.index)
            Scores=[]
            for action in Actions:
                Scores.append(get_Min(1,gameState.generateSuccessor(self.index, action), depth))
            MaxScore = max(Scores)
            maxIndex = Scores.index(MaxScore)
            return MaxScore, Actions[maxIndex]
        
        def get_Min( agentIndex, gameState, depth):
            Actions = gameState.getLegalActions(agentIndex)
            Scores=[]
            if (depth==0 or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState), "noMove"
            for action in Actions:
                if (agentIndex!= gameState.getNumAgents()-1):
                    Scores.append(get_Min(agentIndex+1, gameState.generateSuccessor(agentIndex, action), depth)[0])
                else:
                    Scores.append(get_Max(gameState.generateSuccessor(agentIndex,action),(depth-1))[0] )
            MinScore = min(Scores)
            minIndex = Scores.index(MinScore)
            return MinScore, Actions[minIndex]
        
        score, action=get_Max(gameState,self.depth)
        return action
        

       
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"


        def get_Max(gameState,alpha, beta, depth):
            if (depth==0 or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState), "noMove"
            Actions = gameState.getLegalActions(self.index)
            
            maxScore = -(float("inf"))
            maxAction = Directions.STOP
            for action in Actions:
                v = get_Min(gameState.generateSuccessor(self.index, action), alpha, beta, 1, depth)
                if v >= maxScore:
                    maxScore = v
                    maxAction = action
                if maxScore > beta:
                    return maxScore, maxAction
                alpha = max(alpha, maxScore)
            
            return maxScore, maxAction
        
        def get_Min(gameState, alpha, beta, agentIndex, depth):
            if (depth==0 or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            numAgent = gameState.getNumAgents() - 1
            Actions = gameState.getLegalActions(agentIndex)
            
            minScore = float("inf")
            
            for action in Actions:
                if (agentIndex!= numAgent):
                    v = get_Min( gameState.generateSuccessor(agentIndex, action),alpha, beta, agentIndex+1, depth)
                    if v < minScore:
                        minScore = v
                    if minScore < alpha:
                        return minScore
                    beta = min(beta, v)
                else:
                    v = get_Max(gameState.generateSuccessor(agentIndex,action), alpha, beta, (depth-1))[0] 
                    if v < minScore:
                        minScore = v
                    if minScore < alpha:
                        return minScore
                    beta = min(beta, v)
            return minScore
        
        alpha = -(float("inf"))
        beta = float("inf")
        score, action =get_Max(gameState, alpha, beta, self.depth)
        return action
        
       

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        def get_Max(gameState, depth):
            if (depth==0 or gameState.isWin() or gameState.isLose()):
                return list((self.evaluationFunction(gameState),"noMove"))
            Actions = gameState.getLegalActions(self.index)
            Scores=[]
            for action in Actions:
                Scores.append(get_Exp(1,gameState.generateSuccessor(self.index, action), depth))
            MaxScore = max(Scores)
            maxIndex = Scores.index(MaxScore)
            return MaxScore, Actions[maxIndex]
        
        def get_Exp( agentIndex, gameState, depth):
            if (depth==0 or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            Scores = 0
            Actions = gameState.getLegalActions(agentIndex)
            
            for action in Actions:
                if (agentIndex!= gameState.getNumAgents()-1):
                    Scores += get_Exp(agentIndex+1, gameState.generateSuccessor(agentIndex, action), depth)
                else:
                    Scores += get_Max(gameState.generateSuccessor(agentIndex,action),(depth-1))[0]
                    
            return Scores / len(Actions)
        
        score, action=get_Max(gameState,self.depth)
        return action
        
    
    
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
      return float("inf")
    if currentGameState.isLose():
      return - float("inf")
    
    score = 5*scoreEvaluationFunction(currentGameState)
    
    foodPos = currentGameState.getFood().asList()
    foodDist = []
    for food in foodPos:
        dist = util.manhattanDistance(currentGameState.getPacmanPosition(), food)
        foodDist.append(dist)
    minFoodDist = min(foodDist)
    numFoods = len(foodDist)
    
    numCapsules = len(currentGameState.getCapsules())
    countEatGhost = 0
    
    for ghost in currentGameState.getGhostStates():
        dist = util.manhattanDistance(currentGameState.getPacmanPosition(), ghost.getPosition())
        if ghost.scaredTimer >= 0:
            score -= 200 *dist
            countEatGhost +=1
        else:
            score += 4*max(dist,3) 
    
    score -= 5*minFoodDist
    score -= 5* numFoods
    score -= 40* numCapsules
    score += 100*countEatGhost
    return score
            
# Abbreviation
better = betterEvaluationFunction
class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
    
        util.raiseNotDefined()

