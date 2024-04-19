import asyncio
import random
import time
import py_trees as pt 
from py_trees import common
from Conditions import *
import Goals_BT
import Sensors
from Base_Actions import *
from Compound_Actions import *


'''
Main behaviour tree that models the movements of our agent, the critter.
It consists of a selector with multiple options based on the observations that the agent makes of its environment.
It can avoid obstacles encountered, avoid critters encountered, eat flowers, follow or search the astronaut and roam around.
'''
class GlobalBT:
    def __init__(self, aagent):
        # Initialize variables and agent atributes
        self.aagent = aagent
        self.initTime = time.time()    
        self.aagent.isFollowing = False
        self.aagent.isHungry = False
        self.aagent.timecount = 0.0
        self.aagent.obstacleInfo = [0,0,0] #[Obstacle_left, Obstacle_front, Obstacle_right]    
        self.aagent.flowerDirection = (0,0)
        self.aagent.flowerDistance = 0
        self.aagent.astronautDirection = [0,0]
        self.aagent.astronautDistance = 0       
         
        # Create sub-trees

        # Avoid critters
        critter = pt.composites.Sequence(name="Avoid critter", memory=True)
        critter.add_children([Is_Critter(aagent), 
                              BN_Turn(aagent, -1, 45), 
                              BN_Turn(aagent, 1, 90), 
                              BN_Forward(aagent)])

        # Eat flowers
        eat = pt.composites.Sequence("Eat", memory=True)
        eat.add_children([Is_Hungry(aagent), 
                          Is_Flower(aagent), 
                          BN_Turn(aagent, self.aagent.flowerDirection[0], self.aagent.flowerDirection[1]), 
                          BN_Forward(aagent, self.aagent.flowerDistance), 
                          Eating(aagent)])
 
        # Avoid obstacles
        front = pt.composites.Sequence("Avoid front", memory=True)
        front.add_children([Is_Obstacle(aagent, 5, 6), BN_Turn(aagent, 1)])

        right = pt.composites.Sequence("Avoid right", memory=True)
        right.add_children([Is_Obstacle(aagent, 6, 7), BN_Turn(aagent, -1)])

        left = pt.composites.Sequence("Avoid left", memory=True)
        left.add_children([Is_Obstacle(aagent, 4, 5), BN_Turn(aagent, 1)])

        Avoid_Obs = pt.composites.Selector("Avoiding", memory=False)
        Avoid_Obs.add_children([left, front, right])

        obstacle = pt.composites.Sequence("Avoid obstacles", memory=True)
        obstacle.add_children([Is_Obstacle(aagent, 4, 7), Avoid_Obs])

        # # Follow astronaut
        # follow = pt.composites.Sequence("Follow astronaut", memory=True)
        # follow.add_children([Is_Astronaut(aagent), Following(aagent)])

        # # Search astronaut
        # search = pt.composites.Sequence("Search astronaut", memory=True)
        # search.add_children([Is_Following(aagent), Searching(aagent)])

        # Roam around
        roam = pt.composites.Parallel("Roam aroud", policy=pt.common.ParallelPolicy.SuccessOnAll())
        roam.add_children([BN_Forward(aagent), BN_Turn(aagent)])

        # Tree root selector
        self.root = pt.composites.Selector(name="Selector", memory=False)
        #self.root.add_children([critter, eat, obstacle, follow, search, roam])
        self.root.add_children([critter, eat, obstacle, roam])
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





