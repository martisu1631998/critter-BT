import asyncio
import py_trees as pt
from py_trees import common
from Goals_BT import *
import Sensors
import time
from Conditions_BT import *
# from Compound_Actions import *

'''
The atomic actions that integrate more complex actions.
These are the real leaves of the behaviour tree.
'''


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
An action that makes the agent move forward
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
An action that makes the agent turn
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


