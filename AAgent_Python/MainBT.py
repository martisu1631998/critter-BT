import asyncio
import random
import time
import py_trees as pt 
from py_trees import common
from BTRoam import *
from Conditions_BT import *
from ActionsBT import *
from Goals_BT import *
import Sensors
from ActionsBT import *


'''
Main behaviour tree that models the movements of our agent, the critter.
It consists of a selector with multiple options based on the observations that the agent makes of its environment.
It can avoid obstacles encountered, avoid critters encountered, eat flowers, follow or search the astronaut and roam around.
'''
class GlobalBT:
    def __init__(self, aagent):
        # Initialize agent atributes
        self.aagent = aagent
        self.initTime = time.time()               
        
        # Create sub-trees

        # Eat flowers
        eat = pt.composites.Sequence("Eat", memory=True)
        eat.add_children([Is_Hungry(aagent), Is_Flower(aagent), TurnToFlower(aagent), GoToFlower(aagent), Eating(aagent)])
 
        # Avoid obstacles
        obstacle = pt.composites.Sequence("Avoid obstacles", memory=True)
        follow.add_children([Is_Obstacle(aagent), ManageObs(aagent)])

        # Follow astronaut
        follow = pt.composites.Sequence("Follow astronaut", memory=True)
        follow.add_children([Is_Astronaut(aagent), TurnToAstronaut(aagent), GoToAstronaut(aagent)])

        # # Search astronaut
        # search = pt.composites.Sequence("Search astronaut", memory=True)
        # search.add_children([Is_Following(aagent), Searching(aagent)])

        # Roam around
        roaming = pt.composites.Parallel("Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        roaming.add_children([BN_ForwardRandom(aagent), BN_TurnRandom(aagent)])

        # Tree root selector
        self.root = pt.composites.Selector(name="Selector", memory=False)
        self.root.add_children([eat(aagent), obstacle(aagent), follow(aagent), roaming(aagent)]) # search(aagent)

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
        # Control the time passed until the agent is hungry
        self.aagent.timecount = time.time() - self.initTime
        if self.aagent.timecount < 15:
            self.aagent.isHungry = False
        else:
            self.aagent.isHungry = True

        self.behaviour_tree.tick()
        await asyncio.sleep(0)



xd = GlobalBT(aagent={})

