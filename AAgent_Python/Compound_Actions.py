import py_trees as pt 
from py_trees import common
import Sensors
import asyncio
from Goals_BT import *

'''
All the main behaviour tree's action leaves.
They represent different actions that the agent can perform.
'''





'''
class Approach_Object(pt.behaviour.Behaviour):
    def __init__(self, aagent, object):
        self.my_goal = None
        print("Initializing Approach_Object")
        super(Approach_Object, self).__init__("Approach_Object")
        self.my_agent = aagent  
        self.my_object = object
        self.ray = {'idx':100, 'dist':0}      
        
    def initialise(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for i in range(len(sensor_obj_info)):
            if sensor_obj_info[i]:
                if sensor_obj_info[i]['tag'] == self.my_object:
                    if abs(5 - i) < abs(5 - self.ray['idx']):
                        self.ray['idx'] = i
                        self.ray['dist'] = sensor_obj_info[i]["distance"] 

        if self.ray['idx'] == 5:
            self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, int(self.ray["dist"]), -1, 10).run()) 
                
        elif self.ray['idx'] < 5:                     
            self.my_goal = asyncio.create_task(Turn(self.my_agent, direction=-1, rotation_amount=18*(5-self.ray['idx'])).run())
            self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, int(self.ray["dist"]), -1, 10).run()) 
         
        elif self.ray['idx'] > 5:
            self.my_goal = asyncio.create_task(Turn(self.my_agent, direction=-1, rotation_amount=18*(self.ray['idx']+1)).run())
            self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, int(self.ray["dist"]), -1, 10).run()) 

    def update(self):
        if self.my_goal == None:
            print("No requested object nearby!") 
            return pt.common.Status.FAILURE   

        elif not self.my_goal.done():
            return pt.common.Status.RUNNING     

        res = self.my_goal.result()
        if res:
            print("Approached!")
            return pt.common.Status.SUCCESS
        else:
            print("Approach failed!")
            return pt.common.Status.FAILURE


    def terminate(self, new_status: common.Status):        
        self.logger.debug("Terminate BN_DetectFlower")
        self.my_goal.cancel()
'''