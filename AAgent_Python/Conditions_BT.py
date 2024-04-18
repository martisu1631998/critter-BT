import py_trees as pt  # type: ignore
from py_trees import common # type: ignore
import Sensors

'''
All the main behaviour tree's conditional leaves. 
They check possible conditions that trigger different behaviours of the agent.
'''



'''
Whether the agent has detected another critter or not
'''
class Is_Critter(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing Is_Critter")
        super(Is_Critter, self).__init__("Is_Critter")
        self.my_agent = aagent

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] == "CritterMantaRay":  # If it is another critter
                    print("A critter! Run!")
                    self.my_agent.isFollowing = False
                    return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


'''
Whether the agent is hungry or not
'''
class Is_Hungry(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing Is_Hungry")
        super(Is_Hungry, self).__init__("Is_Hungry")
        self.my_agent = aagent

    def initialise(self):
        pass

    def update(self):
        if self.my_agent.isHungry:
          print("I am hungry!")
          return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


'''
Whether the agent has detected a flower or not
'''
class Is_Flower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing Is_Flower")
        super(Is_Flower, self).__init__("Is_Flower")
        self.my_agent = aagent

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] == "Flower":  # If there is a flower
                    print("Flower found!")
                    self.my_agent.isFollowing = False
                    return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


'''
Whether the agent has detected an obstacle or not
'''
class Is_Obstacle(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing Is_Obstacle")
        super(Is_Obstacle, self).__init__("Is_Obstacle")
        self.my_agent = aagent

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if (value["tag"] == "Rock") or (value["tag"] == "Wall") or (value["tag"] == "Machine") or (value["tag"] == "Flower"): # If there is an obstacle
                    print("There is an obstacle!")                    
                    return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass

'''
Whether the agent has detected an astronaut or not
'''
class Is_Astronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing Is_Astronaut")
        super(Is_Astronaut, self).__init__("Is_Astronaut")
        self.my_agent = aagent

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] == "Astronaut":  # If it is the astronaut
                    print("Astronaut encountered!")
                    self.my_agent.isFollowing = True
                    return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass



'''
Whether the agent should search for the astronaut or not
'''
class Is_Following(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing Is_Following")
        super(Is_Following, self).__init__("Is_Following")
        self.my_agent = aagent

    def initialise(self):
        pass

    def update(self):
        if self.my_agent.isFollowing:
            print("Astronaut lost!")
            return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass