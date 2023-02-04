import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os

from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    
    def __init__(self, brainID):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK(f"brain{brainID}.nndf")
        os.system(f"rm brain{brainID}.nndf")
        self.brainID = brainID
        self.fitness = 0
        self.current = 0

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuron in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuron):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuron)
                desiredAngle = self.nn.Get_Value_Of(neuron) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Current_Fitness(self):
        for sensor in self.sensors:
            if not sensor == 'Torso' and pyrosim.Get_Touch_Sensor_Value_For_Link(sensor) == 1:
                self.current = 0
                return

        self.current += 1
        if self.current > self.fitness:
            self.fitness = self.current

        # basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        # basePosition = basePositionAndOrientation[0]
        # if (basePosition[2] > self.fitness):
        #     self.fitness = basePosition[2]

    def Get_Fitness(self):
        f = open(f"tmp{self.brainID}.txt", "w")
        f.write(str(self.fitness))
        f.close()
        os.system(f"mv tmp{self.brainID}.txt fitness{self.brainID}.txt")
