import pybullet as p
import pybullet_data
import time
import constants as c

from world import WORLD
from simulator.robot import ROBOT

class SIMULATION:
    
    def __init__(self, direct, brainID):
        self.physicsClient = p.connect(p.DIRECT) if direct == 'DIRECT' else p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        self.robot = ROBOT(brainID)
        self.directOrGUI = direct

    def __del__(self):
        p.disconnect()

    def Run(self):
        for t in range(c.steps):
            p.stepSimulation()
            
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)

            if self.directOrGUI == 'GUI':
                time.sleep(c.sleep)

    def Get_Fitness(self):
        self.robot.Get_Fitness()