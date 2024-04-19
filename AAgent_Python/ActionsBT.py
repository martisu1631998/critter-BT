import asyncio
import random
import py_trees
import py_trees as pt
from py_trees import common
import Goals_BT
import Sensors
import time
import asyncio
from Goals_BT import *
from Base_Actions import *

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


class TurnToFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing turning to flower...")
        self.my_agent = aagent
        super(TurnToFlower, self).__init__("TurnToFlower")
        
    
    def initialise(self):
        self.direction = self.my_agent.i_state.flowerDirection[0]
        self.degree_rotation = self.my_agent.i_state.flowerDirection[1]
        self.my_goal = asyncio.create_task(Turn(self.my_agent, self.direction, self.degree_rotation).run())
        
    def update(self):
        if not self.my_goal.done():
            print("Still running...")
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("TurnToFlower completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("TurnToFlower completed with FAILURE")
                return pt.common.Status.FAILURE
            
    def terminate(self):
        # Finishing the behaviour, therefore we have to stop the associated task
        print("Terminating TurnToFlower...")
        # self.logger.debug("Terminate TurnToFlower")
        # self.my_goal.cancel()

class GoToFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing going to the flower...")
        self.my_agent = aagent
        super(GoToFlower, self).__init__("GoToFlower")
    
    def initialise(self):
        self.distance = self.my_agent.i_state.flowerDistance
        self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, self.distance).run())
    
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
            
    def terminate(self):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate GoToFlower")
        self.my_goal.cancel()

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


class GoToAstronaut(pt.behaviour.Behaviour):
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
  
        
""""
class Approach_Flower(pt.behaviour.Behaviour):
    STOPPED = 0
    TURNING = 1
    MOVING_FORWARD = 2
    
    def __init__(self, aagent):
        self.my_goal = None
        print("Approaching flower...")
        super(Approach_Flower, self).__init__("Approach_Flower")
        self.my_agent = aagent
        self.rays = 0
        self.state = self.STOPPED
        self.distance = None
        self.i_state = aagent.i_state
        
    def initialise(self):
        pass
        # self.my_goal = asyncio.create_task(Goals_BT.ForwardDist(self.my_agent, -1, -1, 10).run())

    def update(self):
        left = [0,1,2,3]
        middle = [4,5,6]
        right = [7,8,9,10,11]
        
        if self.state == self.STOPPED:
            print("Initializing things...")
            self.direction = self.i_state.flowerDirection[0]
            self.degree_rotation = self.i_state.flowerDirection[1]
            self.distance = self.i_state.flowerDistance
            self.state = self.TURNING
        
        elif self.state == self.TURNING:
            BN_Turn(self.my_agent, self.direction, self.degree_rotation)
            print("Successfully turned to the flower!")
            self.state = self.MOVING_FORWARD
            
        elif self.state == self.MOVING_FORWARD:
            BN_Forward(self.my_agent, self.distance)    
            print("Approach_Flower SUCCESS")
            return pt.common.Status.SUCCESS
    

    
        if self.state == self.STOPPED:
            sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
            for index, value in enumerate(sensor_obj_info):
                if value:
                    if value["tag"] == "Flower":
                        if index not in middle:
                            self.rays = index
                            self.state = self.TURNING
        
        elif self.state == self.TURNING:
            if self.rays in left:
                self.my_goal = asyncio.create_task(Turn(self.my_agent, direction=-1, rotation_amount=45).run())
                print("Successfully turned to the left")
                self.state = self.MOVING_FORWARD
            
            elif self.rays in right:
                self.my_goal = asyncio.create_task(Turn(self.my_agent, direction=1, rotation_amount=45).run())
                print("Successfully turned to the right")
                self.state = self.MOVING_FORWARD
                
            sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
            for index, value in enumerate(sensor_obj_info):
                if value:
                    if value["tag"] == "Flower":
                        if index not in middle:
                            self.distance = value["distance"]
        
        elif self.state == self.MOVING_FORWARD:
            self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, self.distance, -1, 10).run())     
            print("Approach_Flower SUCCESS")
            return pt.common.Status.SUCCESS
        
        
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:
                if value["tag"] == "Flower":
                    print("Turning to the flower....")
                    # Turn if the flower is not in front of the critter
                    if index in left:
                        self.my_goal = asyncio.create_task(Turn(self.my_agent, direction=1, rotation_amount=45).run())
                        print("Successfully turned")
                                
                    if index in right:
                        self.my_goal = asyncio.create_task(Turn(self.my_agent, direction=-1, rotation_amount=-45).run())
                        print("Successfully turned")
                    
                    self.rays = index    
                    
                    break
                          
        # When the flower is in front of the critter, move towards it.
        if self.rays in middle:
            self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, value["distance"], -1, 10).run())     
            print("Approach_Flower SUCCESS")
            return pt.common.Status.SUCCESS
        
        print("Approach_Flower completed with FAILURE")
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass
        # self.logger.debug("Terminate BN_DetectFlower")
        # self.my_goal.cancel()
"""