import asyncio
import random
import time
import py_trees as pt 
from py_trees import common
import Goals_BT
import Sensors


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

        # Avoid critters
        avoid = pt.composites.Sequence(name="Avoid critter", memory=True)
        avoid.add_children([Is_Critter(aagent), Avoiding(aagent)])

        # Eat flowers
        eat = pt.composites.Sequence("Eat", memory=True)
        eat.add_children([Is_Hungry(aagent), Is_Flower(aagent), Eating(aagent)])

        # Avoid obstacles
        follow = pt.composites.Sequence("Follow astronaut", memory=True)
        follow.add_children([Is_Astronaut(aagent), Following(aagent)])

        # Follow astronaut
        follow = pt.composites.Sequence("Follow astronaut", memory=True)
        follow.add_children([Is_Astronaut(aagent), Following(aagent)])

        # Search astronaut
        search = pt.composites.Sequence("Search astronaut", memory=True)
        search.add_children([Is_Following(aagent), Searching(aagent)])

        # Tree root selector
        self.root = pt.composites.Selector(name="Selector", memory=False)
        self.root.add_children([avoid(aagent), eat(aagent), follow(aagent), search(aagent), roam(aagent)])

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
        self.timer = time.time() - self.initTime
        if self.time < 15:
            self.hungry = False
        else:
            self.hungry = True
        self.behaviour_tree.tick()
        await asyncio.sleep(0)