import asyncio
import random
import py_trees
import py_trees as pt
from py_trees import common
import Goals_BT
import Sensors
import BTRoam
import time


class BN_DetectObstacle(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectFlower")
        super(BN_DetectObstacle, self).__init__("BN_DetectObstacle")
        self.my_agent = aagent
        self.always_avoid = ["AAgentCritterMantaRay", "Rock", "Wall", "Machine"]

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] in self.always_avoid: # If it's one of the things we always want to avoid
                    print("BN_DetectObstacle completed with SUCCESS")
                    return pt.common.Status.SUCCESS
                if value["tag"] == "Flower":
                    if not hungry:
                        return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass



class BN_AvoidObstacle(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_AvoidObstacle")
        super(BN_AvoidObstacle, self).__init__("BN_AvoidObstacle")
        self.logger.debug("Initializing BN_AvoidObstacle")
        self.my_agent = aagent

    def initialise(self):
        self.logger.debug("Create Goals_BT.AvoidObs task")
        self.my_goal = asyncio.create_task(Goals_BT.AvoidObst(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                self.logger.debug("BN_ForwardRandom completed with SUCCESS")
                print("BN_ForwardRandom completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                self.logger.debug("BN_ForwardRandom completed with FAILURE")
                print("BN_ForwardRandom completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_ForwardRandom")
        self.my_goal.cancel()