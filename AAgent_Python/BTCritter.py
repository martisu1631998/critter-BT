import asyncio
import random
import py_trees # type: ignore
import py_trees as pt # type: ignore
from py_trees import common # type: ignore
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
                    if not self.my_agent.i_state.isHungry:
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
        print(sensor_obj_info)
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] in self.always_avoid: # If it's one of the things we always want to avoid
                    # print("BN_NoObstacle completed with SUCCESS")
                    return pt.common.Status.SUCCESS
                if value["tag"] == "Flower":
                    if not self.my_agent.i_state.isHungry:
                        return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE
    


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