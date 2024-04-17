import asyncio
import random
import py_trees
import py_trees as pt
from py_trees import common
import Goals_BT
import Sensors
import BTRoam
import time

class BTRoam:
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
        detection = pt.composites.Sequence(name="DetectFlower", memory=True)
        detection.add_children([BN_DetectFlower(aagent), BN_DoNothing(aagent)])

        roaming = pt.composites.Parallel("Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        roaming.add_children([BN_ForwardRandom(aagent), BN_TurnRandom(aagent)])

        self.root = pt.composites.Selector(name="Selector", memory=False)
        self.root.add_children([detection, roaming])

        self.behaviour_tree = pt.trees.BehaviourTree(self.root)

        self.initTime = time.time() # This will be updated every time hungry is set to false again
        self.timer = 0 # This will be initialized every time hungry is set to false again

    # Function to set invalid state for a node and its children recursively
    def set_invalid_state(self, node):
        node.status = pt.common.Status.INVALID
        for child in node.children:
            self.set_invalid_state(child)

    def stop_behaviour_tree(self):
        # Setting all the nodes to invalid, we force the associated asyncio tasks to be cancelled
        self.set_invalid_state(self.root)

    async def tick(self):
        self.timer = time.time() - self.initTime
        if self.timer < 15:
            self.hungry = False
        else:
            self.hungry = True
        self.behaviour_tree.tick()
        await asyncio.sleep(0)
