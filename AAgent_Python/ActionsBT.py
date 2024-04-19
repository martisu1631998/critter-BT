import asyncio
import random
import py_trees
import py_trees as pt
from py_trees import common
import Goals_BT
import Sensors
import time

'''
All the main behaviour tree's action leaves.
They represent different actions that the agent can perform.
'''

class ManageObs(pt.behaviour.Behaviour):
    """
    Manage Obstacle:
    This behaviour tree (together witth IsObstacle) only modifies the behaviour of the 
    critter when it has an obstacleright in front. When it has an obstacle close on the 
    right or in the left, it walks forward but it remembers where the obstacle is, in order
    to turn the opposite side when it cannot advance.
    """
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing ManageObs")
        super(ManageObs, self).__init__("ManageObs")
        self.logger.debug("Initializing ManageObs")
        self.my_agent = aagent

    def initialise(self):
        # No immediate obstacle --> do nothing
        if self.my_agent.i_state.obstacleInfo[1] == 0:
            print("Ignore Obstacle", self.my_agent.i_state.obstacleInfo)
            self.my_goal = asyncio.create_task(Goals_BT.ForwardDist(self.my_agent, -1, 1, 5).run())
        
        # Obstacles on the left --> turn right
        elif self.my_agent.i_state.obstacleInfo[0] == 1:
            print("Obstacle on the left", self.my_agent.i_state.obstacleInfo)
            self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent,
                                                              direction=1,
                                                              rotation_amount=15).run())
        # Obstacles on the right --> turn left
        elif self.my_agent.i_state.obstacleInfo[2] == 1:
            print("Obstacle on the right", self.my_agent.i_state.obstacleInfo)
            self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent,
                                                             direction=-1,
                                                             rotation_amount=15).run())
        
        elif self.my_agent.i_state.obstacleInfo[1] == 1:
            print("Obstacle on the middle", self.my_agents.i_state.obstacleInfo)
            self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent,
                                                             direction=1,
                                                             rotation_amount=15))
        
    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_ManageObstacle completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_ManageObstacle completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_ManageObstacle")
        self.my_goal.cancel()


# class TurnToFlower()

# class GoToFlower()

# class Eating()

class TurnToAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing TurnToAstronaut")
        super(ManageObs, self).__init__("TurnToAstronaut")
        self.logger.debug("TurnToAstronaut")
        self.my_agent = aagent

    def initialise(self):
        direction = self.my_agent.i_state.astronautDirection
        self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent, *direction).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("TurnToAstronaut completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("TurnToAstronaut completed with FAILURE")
                return pt.common.Status.FAILURE
            
    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate TurnToAstronaut")
        self.my_goal.cancel()


class GoToAstronaut(pt.Behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing GoToAstronaut")
        super(ManageObs, self).__init__("GoToAstronaut")
        self.logger.debug("GoToAstronaut")
        self.my_agent = aagent

    def initialise(self):
        distance = self.my_agent.i_state.astronautDistance
        self.my_goal = asyncio.create_task(Goals_BT.ForwardDist(self.my_agent, distance, -1, 1).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_ManageObstacle completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_ManageObstacle completed with FAILURE")
                return pt.common.Status.FAILURE
            
    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate GoToAstronaut")
        self.my_goal.cancel()
