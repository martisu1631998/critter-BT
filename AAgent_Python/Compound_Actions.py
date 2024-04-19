import py_trees as pt 
from py_trees import common
import Sensors
import asyncio
from Goals_BT import *
from Base_Actions import *

'''
All the main behaviour tree's action leaves.
They represent different actions that the agent can perform.
'''


'''
Function so that the agent centers its body towards a detected flower, when it is hungry
'''
class TurnToFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing turning to flower...")
        self.my_agent = aagent
        super(TurnToFlower, self).__init__("TurnToFlower")
        self.logger.debug("TurnToFlower")
        
    
    def initialise(self):
        self.direction = self.my_agent.i_state.flowerDirection[0]
        self.degree_rotation = self.my_agent.i_state.flowerDirection[1]
        direction = self.my_agent.i_state.flowerDirection
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
            
    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate TurnToFlower")
        self.my_goal.cancel()



class GoToFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing going to the flower...")
        self.my_agent = aagent
        super(GoToFlower, self).__init__("GoToFlower")
        self.logger.debug("GoToFlower")
    
    def initialise(self):
        self.distance = self.my_agent.i_state.flowerDistance
        self.my_goal = asyncio.create_task(ForwardDist(self.my_agent, self.distance, -1, 1).run())
    
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

class Eating(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing eating...")
        self.my_agent = aagent
        # self.i_state = aagent.i_state
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
                self.my_agent.isHungry = False
                return pt.common.Status.SUCCESS
            else:
                print("Eating completed with FAILURE")
                return pt.common.Status.FAILURE
            
    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate Eating")
        self.my_goal.cancel()


class TurnToAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing TurnToAstronaut")
        super(TurnToAstronaut, self).__init__("TurnToAstronaut")
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
        super(GoToAstronaut, self).__init__("GoToAstronaut")
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
