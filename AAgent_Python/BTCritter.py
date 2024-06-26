import asyncio
import time
import py_trees as pt 
from Conditions_BT import *
from Actions_BT import *
from Goals_BT import *

'''
Main behaviour tree that models the movements of our agent, the critter.
It consists of a selector with multiple options based on the observations that the agent makes of its environment.
It can avoid obstacles encountered, avoid critters encountered, eat flowers, follow the astronaut and roam around.
'''
class GlobalBT:
    def __init__(self, aagent):
        # Initialize agent atributes
        self.aagent = aagent
        self.aagent.i_state.initTime = time.time()               
        
        ''' Create subtrees '''
        # Avoid critters
        critter = pt.composites.Sequence(name="Avoid critters", memory=True)
        critter.add_children([Is_Critter(aagent), 
                              BN_Turn(aagent, -1, 360), 
                              BN_Turn(aagent, 1, 90), 
                              BN_Forward(aagent)])

        # Eat flowers
        eat = pt.composites.Sequence("Eat flowers", memory=True)
        eat.add_children([Is_Hungry(aagent), Is_Flower(aagent), TurnToFlower(aagent), GoToFlower(aagent), Eating(aagent)])

        # Follow astronaut
        follow = pt.composites.Sequence("Follow astronaut", memory=True)
        follow.add_children([Is_Astronaut(aagent), TurnToAstronaut(aagent), GoToAstronaut(aagent)])
 
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

        # Roam around
        roaming = pt.composites.Parallel("Roam around", policy=pt.common.ParallelPolicy.SuccessOnAll())
        roaming.add_children([BN_Forward(aagent), BN_Turn(aagent)])

        # Tree root selector
        self.root = pt.composites.Selector(name="Main", memory=False)
        self.root.add_children([critter, eat, follow, obstacle, roaming])
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