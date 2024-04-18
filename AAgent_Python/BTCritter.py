import asyncio
import random
import py_trees # type: ignore
import py_trees as pt # type: ignore
from py_trees import common # type: ignore
import Goals_BT
import Sensors
from BTRoam import *
import time


class BN_DetectObstacle(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectObstacle")
        super(BN_DetectObstacle, self).__init__("BN_DetectObstacle")
        self.my_agent = aagent
        self.always_avoid = ["AAgentCritterMantaRay", "Rock", "Wall", "Machine"]
        self.hits = [0,0,0]

    def initialise(self):
        self.hits = [0,0,0]

    def updateObstacleInfo(self):
        # It has to be updated following these rules so the critter doesn't get stuck.
        prev = self.my_agent.i_state.obstacleInfo
        curr = self.hits
        # If there's obstacles on both sides or none, set the 'obstacle' in the left so it always turns right
        if prev == [0,0,0] and curr == [1,0,1]:
            self.my_agent.i_state.obstacleInfo = [1,0,0]
        elif prev == [0,0,0] and (curr == [1,1,1] or curr == [0,1,0]):
            self.my_agent.i_state.obstacleInfo = [1,1,0]
        # If there were not detected obstacles, update normally
        elif prev == [0,0,0]:
            self.my_agent.i_state.obstacleInfo = curr
        elif prev[1] == 0 and curr[1] == 1:
            self.my_agent.i_state.obstacleInfo[1] = 1


    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        detected = False
        # Only trigger if the object is detected by the 3 central rays.
        # Otherways, it's not an obstacle
        for i in [4,5,6]:
            if sensor_obj_info[i]:
                if sensor_obj_info[i]["tag"] in self.always_avoid:
                    print("BN_DetectObstacle completed with SUCCESS")
                    # From i in [4,5,6] to i in [0,1,2]
                    self.hits[i-4] = 1
                    detected = True                    
                elif (sensor_obj_info[i]["tag"] == "Flower") and (not self.my_agent.i_state.isHungry):
                    print("BN_DetectObstacle completed with SUCCESS")
                    # From i in [4,5,6] to i in [0,1,2]
                    self.hits[i-4] = 1
                    detected = True
        if detected:
            self.updateObstacleInfo()
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


class BN_NoObstacle(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_NoObstacle")
        super(BN_NoObstacle, self).__init__("BN_NoObstacle")
        self.my_agent = aagent
        self.always_avoid = ["AAgentCritterMantaRay", "Rock", "Wall", "Machine"]

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        # Only trigger if the object is detected by the 3 central rays. Otherways, it's not an obstacle
        for i in [4,5,6]:
            if sensor_obj_info[i]:
                if sensor_obj_info[i]["tag"] in self.always_avoid:
                    print("BN_DetectObstacle completed with SUCCESS")
                    return pt.common.Status.FAILURE
                elif (sensor_obj_info[i]["tag"] == "Flower") and (not self.my_agent.i_state.isHungry):
                    print("BN_DetectObstacle completed with SUCCESS")
                    return pt.common.Status.FAILURE
        self.my_agent.i_state.obstacleInfo = [0,0,0]
        return pt.common.Status.SUCCESS
    


class BN_ManageObstacle(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_ManageObstacle")
        super(BN_ManageObstacle, self).__init__("Normal")
        self.my_agent = aagent
        

    def initialise(self):
        pass

    def update(self):
        print('Siuu')
        return pt.common.Status.SUCCESS

    def terminate(self, new_status: common.Status):
        pass



class BTRoamAdvanced:
    def __init__(self, aagent):
        # py_trees.logging.level = py_trees.logging.Level.DEBUG

        self.aagent = aagent

        # VERSION 1
        # self.root = pt.composites.Sequence(name="Sequence", memory=True)
        # self.root.add_children([BN_TurnRandom(aagent),
        #                         BN_ForwardRandom(aagent),
        #                         BN_DoNothing(aagent)])

        # VERSION 2
        # self.root = pt.composites.Parallel("Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        # self.root.add_children([BN_ForwardRandom(aagent), BN_TurnRandom(aagent)])

        # VERSION 3 (with DetectFlower)
        flower_detection = pt.composites.Sequence(name="DetectFlower", memory=True)
        flower_detection.add_children([BN_DetectFlower(aagent), BN_DoNothing(aagent)])

        roaming = pt.composites.Parallel("Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        roaming.add_children([BN_ForwardRandom(aagent), BN_TurnRandom(aagent)])

        no_problem = pt.composites.Selector(name="Selector", memory=False)
        no_problem.add_children([flower_detection, roaming])

        obstacle = pt.composites.Sequence(name="DetectObstacle", memory=False)
        obstacle.add_children([BN_DetectObstacle(aagent), BN_ManageObstacle(aagent)])

        free_way = pt.composites.Selector(name="Selector", memory=False)
        free_way.add_children([BN_NoObstacle(aagent), obstacle])

        self.root = pt.composites.Sequence(name="Sequence", memory=False)
        self.root.add_children([free_way, no_problem])

        self.behaviour_tree = pt.trees.BehaviourTree(self.root)

    # Function to set invalid state for a node and its children recursively
    def set_invalid_state(self, node):
        node.status = pt.common.Status.INVALID
        for child in node.children:
            self.set_invalid_state(child)

    def stop_behaviour_tree(self):
        # Setting all the nodes to invalid, we force the associated asyncio tasks to be cancelled
        self.set_invalid_state(self.root)

    async def tick(self):
        self.behaviour_tree.tick()
        await asyncio.sleep(0)