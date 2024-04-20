import asyncio
import time
import py_trees as pt 
from py_trees import common 
from Goals_BT import *

'''
All the main behaviour tree's action leaves.
They represent the different activities, more or less complex, that the agent can perform.
'''

# class ManageObs(pt.behaviour.Behaviour):
#     """
#     Manage Obstacle:
#     This behaviour tree (together witth IsObstacle) only modifies the behaviour of the 
#     critter when it has an obstacleright in front. When it has an obstacle close on the 
#     right or in the left, it walks forward but it remembers where the obstacle is, in order
#     to turn the opposite side when it cannot advance.
#     """
#     def __init__(self, aagent):
#         self.my_goal = None
#         print("Initializing ManageObs")
#         super(ManageObs, self).__init__("ManageObs")
#         self.logger.debug("Initializing ManageObs")
#         self.my_agent = aagent

#     def initialise(self):
#         # No immediate obstacle --> do nothing
#         if self.my_agent.i_state.obstacleInfo[1] == 0:
#             print("Ignore Obstacle", self.my_agent.i_state.obstacleInfo)
#             self.my_goal = asyncio.create_task(Goals_BT.ForwardDist(self.my_agent, -1, 1, 5).run())
        
#         # Obstacles on the left --> turn right
#         elif self.my_agent.i_state.obstacleInfo[0] == 1:
#             print("Obstacle on the left", self.my_agent.i_state.obstacleInfo)
#             self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent,
#                                                               direction=1,
#                                                               rotation_amount=15).run())
#         # Obstacles on the right --> turn left
#         elif self.my_agent.i_state.obstacleInfo[2] == 1:
#             print("Obstacle on the right", self.my_agent.i_state.obstacleInfo)
#             self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent,
#                                                              direction=-1,
#                                                              rotation_amount=15).run())
        
#         elif self.my_agent.i_state.obstacleInfo[1] == 1:
#             print("Obstacle on the middle", self.my_agents.i_state.obstacleInfo)
#             self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent,
#                                                              direction=1,
#                                                              rotation_amount=15))
        
#     def update(self):
#         if not self.my_goal.done():
#             return pt.common.Status.RUNNING
#         else:
#             res = self.my_goal.result()
#             if res:
#                 print("ManageObs completed with SUCCESS")
#                 return pt.common.Status.SUCCESS
#             else:
#                 print("ManageObs completed with FAILURE")
#                 return pt.common.Status.FAILURE

#     def terminate(self, new_status: common.Status):
#         # Finishing the behaviour, therefore we have to stop the associated task
#         self.logger.debug("Terminate ManageObs")
#         self.my_goal.cancel()


'''
Makes the agent rotate the necessary amount of degrees to be directly looking at the detected flower
'''
class TurnToFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        self.direction = None
        self.degree_rotation = None        
        print("Initializing TurnToFlower")        
        super(TurnToFlower, self).__init__("TurnToFlower")
        self.logger.debug("TurnToFlower")        
    
    def initialise(self):
        self.direction = self.my_agent.i_state.flowerDirection[0]
        self.degree_rotation = self.my_agent.i_state.flowerDirection[1]        
        self.my_goal = asyncio.create_task(Turn(self.my_agent, self.direction, self.degree_rotation).run())
        
    def update(self):
        if not self.my_goal.done():            
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("TurnToFlower completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("TurnToFlower completed with FAILURE")
                return pt.common.Status.FAILURE
            
    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate TurnToFlower")
        self.my_goal.cancel()


'''
Executed after the TurnToFlower action. It moves forward until the distance that separates the
agent from the detected flower is covered
'''
class GoToFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        self.distance = None
        print("Initializing GoToFlower")        
        super(GoToFlower, self).__init__("GoToFlower")
        self.logger.debug("GoToFlower")
    
    def initialise(self):
        self.distance = self.my_agent.i_state.flowerDistance
        self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, int(self.distance), -1, 1).run())
    
    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("GoToFlower completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("GoToFlower completed with FAILURE")
                return pt.common.Status.FAILURE
            
    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate GoToFlower")
        self.my_goal.cancel()


'''
Executed after GoToFlower. The agent waits for five secons and is not hungry anymore
'''
class Eating(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        print("Initializing Eating")        
        super(Eating, self).__init__("Eating")
        self.logger.debug("Eating")        
        
    def initialise(self):
        self.my_goal = asyncio.create_task(DoNothing(self.my_agent).run())
    
    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("1...")
                time.sleep(1)
                print("2...")
                time.sleep(1)
                print("3...")
                time.sleep(1)
                print("4...")
                time.sleep(1)
                print("5...")
                time.sleep(1)
                print("Eating completed with SUCCESS")
                print("Not hungry anymore :)")
                self.my_agent.i_state.isHungry = False
                self.my_agent.i_state.initTime = time.time()
                return pt.common.Status.SUCCESS
            else:
                print("Eating completed with FAILURE")
                return pt.common.Status.FAILURE
            
    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate Eating")
        self.my_goal.cancel()


'''
Makes the agent rotate the necessary amount of degrees to be directly looking at the detected astronaut
'''
class TurnToAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        self.direction = None
        self.degree_rotation = None
        print("Initializing TurnToAstronaut")
        super(TurnToAstronaut, self).__init__("TurnToAstronaut")
        self.logger.debug("TurnToAstronaut")        
                    
    def initialise(self):
        self.direction = self.my_agent.i_state.astronautDirection[0]
        self.degree_rotation = self.my_agent.i_state.astronautDirection[1]
        self.my_goal = asyncio.create_task(Turn(self.my_agent, self.direction, self.degree_rotation).run())

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


'''
Executed after the TurnToAstronaut action. It moves forward until the distance that separates the
agent from the detected astronaut is covered
'''
class GoToAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        self.distance = None
        print("Initializing GoToAstronaut")
        super(GoToAstronaut, self).__init__("GoToAstronaut")
        self.logger.debug("GoToAstronaut")        

    def initialise(self):
        self.distance = self.my_agent.i_state.astronautDistance
        self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, int(self.distance), -1, 1).run())

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
  

'''
An action that just makes the agent do nothing
'''
class BN_DoNothing(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        print("Initializing BN_DoNothing")
        super(BN_DoNothing, self).__init__("BN_DoNothing")

    def initialise(self):
        self.my_goal = asyncio.create_task(DoNothing(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                print("BN_DoNothing completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_DoNothing completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.my_goal.cancel()


'''
An action that makes the agent move forward the specified distance. If no distance is entered,
the agent advances a random distance
'''
class BN_Forward(pt.behaviour.Behaviour):
    def __init__(self, aagent, dist=-1):
        self.my_agent = aagent
        self.dist = dist
        self.my_goal = None        
        print("Initializing BN_Forward")
        super(BN_Forward, self).__init__("BN_Forward")
        self.logger.debug("Initializing BN_Forward")        

    def initialise(self):
        self.logger.debug("Create ForwardDist task")
        self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, self.dist, 1, 5).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                self.logger.debug("BN_Forward completed with SUCCESS")
                print("BN_Forward completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                self.logger.debug("BN_Forward completed with FAILURE")
                print("BN_Forward completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_Forward")
        self.my_goal.cancel()


'''
An action that makes the agent turn in a certain direction a certain amount of degrees. If some variable
is not passed, it is randomy defined
'''
class BN_Turn(pt.behaviour.Behaviour):
    def __init__(self, aagent, direction=None, degree=None):
        self.my_agent = aagent
        self.direction = direction
        self.degree = degree
        self.my_goal = None
        print("Initializing BN_Turn")
        super(BN_Turn, self).__init__("BN_Turn")

    def initialise(self):
        self.my_goal = asyncio.create_task(Turn(self.my_agent, self.direction, self.degree).run())

    def update(self):              
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                self.logger.debug("BN_Turn completed with SUCCESS")
                print("BN_Turn completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                self.logger.debug("BN_Turn completed with FAILURE")
                print("BN_Turn completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_Turn")
        self.my_goal.cancel()