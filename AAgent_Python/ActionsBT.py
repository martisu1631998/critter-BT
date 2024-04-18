import py_trees as pt 
from py_trees import common
import Sensors
import asyncio
from Goals_BT import *

'''
All the main behaviour tree's action leaves.
They represent different actions that the agent can perform.
'''
class Approach_Flower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Approaching flower...")
        super(Approach_Flower, self).__init__("Approach_Flower")
        self.my_agent = aagent
        self.rays = 0
        
    def initialise(self):
        pass
        # self.my_goal = asyncio.create_task(Goals_BT.ForwardDist(self.my_agent, -1, -1, 10).run())

    # async def update(self):
    def update(self):
        left = [0,1,2,3]
        middle = [4,5,6]
        right = [7,8,9,10,11]
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