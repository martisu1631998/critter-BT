import py_trees as pt  
from py_trees import common 
import time
import Sensors

'''
All the main behaviour tree's conditional leaves. 
They check possible conditions that trigger the different behaviours of the agent.
'''



'''
Whether the agent has detected another critter or not
'''
class Is_Critter(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        print("Initializing Is_Critter")
        super(Is_Critter, self).__init__("Is_Critter")        

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] == "CritterMantaRay":  # If it is another critter
                    print("A critter! Run!")                    
                    return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


'''
Whether the agent is hungry or not
'''
class Is_Hungry(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        print("Initializing Is_Hungry")
        super(Is_Hungry, self).__init__("Is_Hungry")        

    def initialise(self):
        pass

    def update(self):
        # Control the time passed until the agent is hungry
        timecount = time.time() - self.my_agent.i_state.initTime
        if timecount < 15:
            self.my_agent.i_state.isHungry = False
        else:
            self.my_agent.i_state.isHungry = True
        
        if self.my_agent.i_state.isHungry:            
            return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


'''
Whether the agent has detected a flower or not
'''
class Is_Flower(pt.behaviour.Behaviour):
    def __init__(self, aagent):        
        self.my_agent = aagent
        self.ray_degrees = {
            0: (-1, 90),
            1: (-1, 72),
            2: (-1, 54),
            3: (-1, 36),
            4: (-1, 18),
            5: (1, 0),
            6: (1, 18),
            7: (1, 36),
            8: (1, 54),
            9: (1, 72),
            10: (1, 90)
        }
        self.my_goal = None
        print("Initializing Is_Flower")
        super(Is_Flower, self).__init__("Is_Flower")

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] == "Flower":  # If there is a flower
                    self.my_agent.i_state.flowerDirection = self.ray_degrees[index]
                    self.my_agent.i_state.flowerDistance = value['distance']
                    print("Flower found!")                    
                    return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


'''
Whether the agent has detected an obstacle or not
'''
class Is_Obstacle(pt.behaviour.Behaviour):
    def __init__(self, aagent, i , j):
        self.my_agent = aagent
        self.i = i
        self.j = j
        self.my_goal = None
        print("Initializing Is_Obstacle")
        super(Is_Obstacle, self).__init__("Is_Obstacle")

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info[self.i:self.j]):
            if value:  # there is a hit with an object
                if (value["tag"] == "Untagged") or (value["tag"] == "Rock") or (value["tag"] == "Wall") or (value["tag"] == "Machine") or (value["tag"] == "Flower"): # If there is an obstacle
                    print("There is an obstacle!")                                        
                    return pt.common.Status.SUCCESS

        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


'''
Alternative implementation of avoid obstacles that is more precise, but also more complex and of which we are not
completely sure that is as reliable as the simpler implementation
'''
# class Is_Obstacle(pt.behaviour.Behaviour):
#     def __init__(self, aagent):
#         self.my_goal = None
#         print("Initializing Is_Obstacle")
#         super(Is_Obstacle, self).__init__("Is_Obstacle")
#         self.my_agent = aagent
#         self.always_avoid = ["Rock", "Wall", "Machine", "Flower", "Untagged"]
#         self.hits = [0,0,0]

#     def initialise(self):
#         self.hits = [0,0,0]

#     def updateObstacleInfo(self):
#         # It has to be updated following these rules so the critter doesn't get stuck.
#         prev = self.my_agent.i_state.obstacleInfo
#         curr = self.hits
#         # If there's obstacles on both sides or none, set the 'obstacle' in the left so it always turns right
#         if prev == [0,0,0] and curr == [1,0,1]:
#             self.my_agent.i_state.obstacleInfo = [1,0,0]
#         elif prev == [0,0,0] and (curr == [1,1,1] or curr == [0,1,0]):
#             self.my_agent.i_state.obstacleInfo = [1,1,0]
#         # If there were not detected obstacles, update normally
#         elif prev == [0,0,0]:
#             self.my_agent.i_state.obstacleInfo = curr
#         elif prev[1] == 0 and curr[1] == 1:
#             self.my_agent.i_state.obstacleInfo[1] = 1

#     def update(self):
#         sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
#         detected = False
#         # Only trigger if the object is detected by the 3 central rays.
#         # Otherways, it's not an obstacle
#         for i in [4,5,6]:
#             if sensor_obj_info[i]:
#                 if sensor_obj_info[i]["tag"] in self.always_avoid:
#                     print("Is_Obstacle completed with SUCCESS")
#                     # From i in [4,5,6] to i in [0,1,2]
#                     self.hits[i-4] = 1
#                     detected = True                                 
                
#         if detected:
#             self.updateObstacleInfo()
#             return pt.common.Status.SUCCESS
        
#         self.my_agent.i_state.obstacleInfo = [0,0,0]
#         return pt.common.Status.FAILURE

#     def terminate(self, new_status: common.Status):
#         pass


'''
Whether the agent has detected an astronaut or not
'''
class Is_Astronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.ray_degrees = {
            0: (-1, 90),
            1: (-1, 72),
            2: (-1, 54),
            3: (-1, 36),
            4: (-1, 18),
            5: (1, 0),
            6: (1, 18),
            7: (1, 36),
            8: (1, 54),
            9: (1, 72),
            10: (1, 90)
        }
        self.my_goal = None
        print("Initializing Is_Astronaut")
        super(Is_Astronaut, self).__init__("Is_Astronaut")

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] == "Astronaut":  # If it is the astronaut
                    self.my_agent.i_state.astronautDirection = self.ray_degrees[index]
                    self.my_agent.i_state.astronautDistance = value['distance']
                    print("Astronaut encountered!")                    
                    return pt.common.Status.SUCCESS
                
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass