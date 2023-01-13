import constants as c
import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.amplitude = c.frontAmplitude
        self.frequency = c.frontFrequency
        self.offset = c.frontPhaseOffset
        if jointName == b'Torso_BackLeg':
            self.motorValues = self.amplitude * numpy.sin(numpy.linspace(0, c.steps, c.steps) / c.steps * 2 * numpy.pi * self.frequency + self.offset)
        else:
            self.motorValues = self.amplitude * numpy.sin(numpy.linspace(0, c.steps, c.steps) / c.steps * 2 * numpy.pi * self.frequency/2 + self.offset)

    def Set_Value(self, robotId, t):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motorValues[t],
            maxForce = c.frontMaxForce)

    def Save_Values(self):
        numpy.save(f"./data/{self.jointName}.npy", self.motorValues)